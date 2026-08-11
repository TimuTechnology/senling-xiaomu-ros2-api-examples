#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小木编程示例五：智能聊天机器人
XiaoMu Programming Example 5: Smart Chatbot

学习目标：综合运用所有技能，创建一个能听、能说、能动的智能机器人
Learning Goal: Comprehensive application - listen, speak, and move intelligently

⚠️ 重要提示 / Important Note：
运行此示例前，请确保 language 参数与小木机器人当前语言一致！
Before running this example, make sure the language parameter matches XiaoMu's current language!
"""

import rclpy
import time
import random
from rclpy.node import Node
from robot_interfaces.msg import Listen, Speak, Action, Servo, Touch


class XiaoMuChat(Node):
    def __init__(self):
        super().__init__('xiaomu_chat')
        
        self.declare_parameter('language', 'en')
        self.language = self.get_parameter('language').value
        
        self.get_logger().info(f'✅ XiaoMu Chatbot started, language: {self.language}')
        
        self.listen_sub = self.create_subscription(Listen, 'listen', self.listen_callback, 10)
        self.touch_sub = self.create_subscription(Touch, 'touch', self.touch_callback, 10)
        self.speak_pub = self.create_publisher(Speak, 'speak', 10)
        self.action_pub = self.create_publisher(Action, 'action', 10)
        
        self.last_touch_time = 0
        self._speak(self._get_text('welcome'))
    
    def _get_text(self, key, **kwargs):
        """获取对应语言的文本 / Get text in current language"""
        texts = {
            'en': {
                'en': 'How are you!',
                'welcome': 'Hello, I am XiaoMu! Nice to meet you!',
                'head_touch': 'Hehe, patting my head feels so good',
                'belly_touch': 'Hee hee, that tickles',
                'understand': 'Hmm... I don\'t quite understand',
                'repeat': 'Could you say that again?',
                'greeting': 'Hello! Nice to see you',
                'goodbye': 'Goodbye, see you next time',
                'thanks': 'You\'re welcome',
            },
            'zh-Hans': {
                'en': '有啥事？',
                'welcome': '你好，我是小木！很高兴认识你！',
                'head_touch': '嘿嘿，摸头好舒服呀',
                'belly_touch': '嘻嘻，好痒啊',
                'understand': '嗯...我不太明白你的意思',
                'repeat': '能再说一遍吗？',
                'greeting': '你好！很高兴见到你',
                'goodbye': '再见，下次见',
                'thanks': '不客气',
            },
        }
        lang_dict = texts.get(self.language, texts['en'])
        text = lang_dict.get(key, '')
        return text.format(**kwargs) if kwargs else text
    
    def _speak(self, text):
        """让小木说话 / Make XiaoMu speak"""
        msg = Speak()
        msg.text = text
        self.speak_pub.publish(msg)
        self.get_logger().info(f'💬 XiaoMu said: {text}')
        time.sleep(len(text) * 0.08)
    
    def _execute(self, servos, duration=0.5):
        """执行动作 / Execute action"""
        action = Action()
        action.time = duration
        action.type = Action.TYPE_RELATIVE_MOVE
        action.servos = servos
        self.action_pub.publish(action)
    
    def _nod(self):
        """点头 / Nod"""
        servos = []
        servo = Servo()
        servo.index = Action.INDEX_HEAD_PITCH
        servo.angle = -15
        servos.append(servo)
        self._execute(servos, 0.4)
    
    def _shake_head(self):
        """摇头 / Shake head"""
        servos = []
        servo = Servo()
        servo.index = Action.INDEX_HEAD_YAW
        servo.angle = -30
        servos.append(servo)
        self._execute(servos, 0.3)
        servos = []
        servo = Servo()
        servo.index = Action.INDEX_HEAD_YAW
        servo.angle = 60
        servos.append(servo)
        self._execute(servos, 0.6)
    
    def _wave(self):
        """挥手 / Wave"""
        servos = []
        servo = Servo()
        servo.index = Action.INDEX_RIGHT_HAND_YAW
        servo.angle = 45
        servos.append(servo)
        self._execute(servos, 0.5)
    
    def listen_callback(self, msg):
        """语音识别回调 / Speech recognition callback"""
        text = msg.data
        self.get_logger().info(f'🎤 Heard: {text}')
        if msg.type == Listen.WAKE_UP:
            self.get_logger().info('i hear call me, stop everything')
            self._speak(self._get_text('en'))
        elif msg.type != Listen.GUESS_TEXT:
            if 'hello' in text or 'hi' in text or '你好' in text:
                self._speak(self._get_text('greeting'))
                self._wave()
            elif 'bye' in text or 'goodbye' in text or '再见' in text:
                self._speak(self._get_text('goodbye'))
                self._wave()
            elif 'thank' in text or 'thanks' in text or '谢谢' in text:
                self._speak(self._get_text('thanks'))
                self._nod()
            else:
                responses = [self._get_text('understand'), self._get_text('repeat')]
                self._speak(random.choice(responses))
                self._shake_head()
    
    def touch_callback(self, msg):
        """触摸回调 / Touch callback"""
        import time
        now = time.time()
        if now - self.last_touch_time < 1:
            return
        self.last_touch_time = now
        
        if msg.head_touch_state == Touch.TOUCH_SINGLE:
            self._speak(self._get_text('head_touch'))
            self._nod()
        elif msg.belly_touch_state == Touch.TOUCH_SINGLE:
            self._speak(self._get_text('belly_touch'))


def main(args=None):
    rclpy.init(args=args)
    node = XiaoMuChat()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
