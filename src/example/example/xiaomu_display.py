#Xiaomu supports the use of the Pygame framework for customizing screen display content. #For users who need to customize the screen display, please contact us to obtain sudo #permissions (subject to compliance with our relevant confidentiality agreement). If you #prefer to use other UI frameworks, you may install the relevant third-party libraries #on your own after obtaining sudo permissions.
#Since screen display content varies significantly among different users, this sample code is provided primarily for reference purposes.
#
import rclpy
from rclpy.node import Node
from robot_interfaces.msg import Emotion
import sys
import time
import io
from PIL import Image
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
import threading
import os
import json
import cProfile
import pstats
import subprocess

import subprocess
import time

def rotate_screen():
    """旋转屏幕 DSI-1 向左旋转 90 度"""
    try:
        # 先尝试直接执行
        result = subprocess.run(
            ['xrandr', '--output', 'DSI-1', '--rotate', 'left'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("✅ 屏幕旋转成功")
            return True
        else:
            print(f"❌ 旋转失败: {result.stderr}")
            # 如果失败，可能因为 X 未就绪，尝试带延迟重试
            return False
            
    except Exception as e:
        print(f"⚠️ 执行出错: {e}")
        return False

def rotate_screen_with_retry(retries=3, delay=1):
    """带重试机制的屏幕旋转"""
    for i in range(retries):
        if rotate_screen():
            return True
        print(f"第 {i+1} 次尝试失败，{delay}秒后重试...")
        time.sleep(delay)
    return False

# 使用
rotate_screen_with_retry()

lock = threading.Lock()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
os.environ['LP_NUM_THREADS'] = '2'

import pygame
pygame.display.init()

class Animation(pygame.sprite.Sprite):
    def __init__(self, x, y, _type, images, layer = -1):
        super().__init__()
        self._layer = layer
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.current_frame = 0
        self.animation_speed = 10
        self.display_count = 0
        self.max_display_count = 0
        self._type = _type
        self.expired_time = None

    def update(self):
        self.current_frame = (self.current_frame + 1) % len(self.images)
        self.image = self.images[self.current_frame]
        if self.current_frame == (len(self.images) -1):
            self.display_count += 1
    
    def get_display_count(self):
        return self.display_count
    
    def reset_display_count(self):
        self.display_count = 0
    
    def get_type(self):
        return self._type
    
    def reset_params(self, max_display_count, expired_time):
        self.max_display_count = max_display_count
        self.expired_time = expired_time
        
    def get_expired_time(self):
        return self.expired_time
        
    def get_max_display_count(self):
        return self.max_display_count

class RobotEmotion(Node):
    def __init__(self):
        super().__init__('RobotEmotion')
        
        self.callback_group = ReentrantCallbackGroup()
        
        self._start()
        
    def _start(self):
        self.see_thread = threading.Thread(target=self.show_emotion, name="robot-emotion-thread")
        self.see_thread.start()
    
    def initAsset(self, right_eye_pos, width, height):
        self.blink1 = pygame.transform.smoothscale(pygame.image.load("blink1.png").convert_alpha(), (self.render_width, self.render_height))
        
        self.blink_animation = Animation(right_eye_pos[0], right_eye_pos[1], Emotion.EMOTION_USUAL, [
        self.blink1
        ])
    
    def show_emotion(self):
        self.print_thread_id()
        
        clock = pygame.time.Clock()
        
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        self.get_logger().info('screen widh:"%s" height:"%s"' %(screen_width, screen_height))
        white = (255, 255, 255)
        black = (0 , 0 ,0)
        right_eye_pos = (0, 0)
        
        scale_factor = 0.5
        self.render_width = int(screen_width * scale_factor)
        self.render_height = int(screen_height * scale_factor)
        
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
        render_surface = pygame.Surface((self.render_width, self.render_height)).convert_alpha()
        
        screen.fill(black)
        pygame.display.flip()   # 立即刷新
        
        self.initAsset(right_eye_pos, self.render_width, self.render_height)
        
        ani_to_remove = []
        ani_to_add = []
        target_frame_time = 1.0 / 10  # 10fps
        self.get_logger().info('show_emotion start....')
        while True:
            frame_start = time.time()
            for animate in self.all_sprites:
                expired_time = animate.get_expired_time()
                if expired_time:
                    if expired_time < time.time():
                        ani_to_remove.append(animate)
                        animate.reset_params(0, None) #reset to none
                else:
                    if animate.get_display_count() >= animate.get_max_display_count():
                        ani_to_remove.append(animate)
                        animate.reset_params(0, None) #reset to none
            
            if len(ani_to_remove) > 0:
                with lock:
                    self.all_sprites.remove(ani_to_remove)
                ani_to_remove = []
            if len(ani_to_add) > 0:
                with lock:        
                    self.all_sprites.add(ani_to_add)
                ani_to_add = []
            
                
            for event in pygame.event.get():
                #print(event)
                #print(pygame.K_ESCAPE, pygame.KEYDOWN)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        return;
                        
            render_surface.fill(black)
            self.all_sprites.update()
            for sprite in self.all_sprites:
                render_surface.blit(sprite.image, sprite.rect)
            
            scaled_surface = pygame.transform.smoothscale(render_surface, (screen_width, screen_height))
            screen.blit(scaled_surface, (0,0))
            pygame.display.flip()  # 更新屏幕显示
            
            elapsed = time.time() - frame_start
            sleep_time = target_frame_time - elapsed
            if sleep_time > target_frame_time:
                sleep_time = target_frame_time
            if sleep_time > 0:
                time.sleep(sleep_time) 
            
        

def main(args=None):
    rclpy.init(args=args)
    
    robot_emotion = RobotEmotion()
    rclpy.spin(robot_emotion)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pygame.quit()
    robot_emotion.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

