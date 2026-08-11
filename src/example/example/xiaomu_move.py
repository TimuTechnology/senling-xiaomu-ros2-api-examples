#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小木编程示例四：动作控制
XiaoMu Programming Example 4: Motion Control

学习目标：控制伺服电机，让小木做各种动作
Learning Goal: Control servo motors to make XiaoMu move

⚠️ 重要提示 / Important Note：
运行此示例前，请确保 language 参数与小木机器人当前语言一致！
Before running this example, make sure the language parameter matches XiaoMu's current language!
"""

import rclpy
import time
from rclpy.node import Node
from robot_interfaces.msg import Action, Servo, Speak


class XiaoMuMove(Node):
    def __init__(self):
        super().__init__('xiaomu_move')
        
        self.declare_parameter('language', 'en')
        self.language = self.get_parameter('language').value
        
        self.get_logger().info(f'✅ XiaoMu Motion started, language: {self.language}')
        
        self.action_pub = self.create_publisher(Action, 'action', 10)
        self.speak_pub = self.create_publisher(Speak, 'speak', 10)
    
    def _get_text(self, key, **kwargs):
        """获取对应语言的文本 / Get text in current language"""
        texts = {
            'en': {
                'greeting': 'Hello everyone, I am Xiao Mu!',
                'nice_to_see': 'Nice to see you',
                'thank_you': 'Thank you',
                'goodbye': 'Goodbye, see you next time',
            },
            'zh-Hans': {
                'greeting': '大家好，我是小木！',
                'nice_to_see': '很高兴见到你',
                'thank_you': '谢谢大家',
                'goodbye': '再见，下次见',
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
    
    def _execute(self, servos, duration=1.0):
        """执行动作 / Execute action"""
        action = Action()
        action.time = float(duration)
        action.type = Action.TYPE_RELATIVE_MOVE
        action.servos = servos
        self.action_pub.publish(action)
        time.sleep(duration + 0.1)
    
    def nod(self):
        """点头 / Nod"""
        servos = []
        servo = Servo()
        servo.index = Action.INDEX_HEAD_PITCH
        servo.angle = 10
        servos.append(servo)
        self._execute(servos, 0.4)
        self.get_logger().info('🙂 Nod')
    
    def shake_head(self):
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
        self.get_logger().info('🙂 Shake head')
    
    def wave(self):
        """挥手 / Wave"""
        servos = []
        servo = Servo()
        servo.index = Action.INDEX_RIGHT_HAND_YAW
        servo.angle = 45
        servos.append(servo)
        self._execute(servos, 0.5)
        self.get_logger().info('👋 Wave')
    
    def reset(self, duration):
        action = Action()
        action.time = float(duration)
        action.type = Action.TYPE_RESET
        
        self.action_pub.publish(action)
        time.sleep(duration + 0.1)
    
    def greet(self):
        """打招呼组合动作 / Greeting combination"""
        self._speak(self._get_text('greeting'))
        self.wave()
        self.nod()
    
    def say_thanks(self):
        """说谢谢 / Say thank you"""
        self._speak(self._get_text('thank_you'))
        self.nod()
    
    def say_goodbye(self):
        """说再见 / Say goodbye"""
        self._speak(self._get_text('goodbye'))
        self.wave()


def main(args=None):
    rclpy.init(args=args)
    xiaomu = XiaoMuMove()
    
    xiaomu.greet()
    time.sleep(1)
    xiaomu.say_thanks()
    time.sleep(1)
    xiaomu.say_goodbye()
    xiaomu.reset(1)
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()
