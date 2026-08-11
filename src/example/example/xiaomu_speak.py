#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小木编程示例一：让小木说话
XiaoMu Programming Example 1: Make XiaoMu Speak

学习目标：掌握ROS 2节点创建、消息发布
Learning Goal: Master ROS 2 node creation and message publishing

⚠️ 重要提示 / Important Note：
运行此示例前，请确保 language 参数与小木机器人当前语言一致！
Before running this example, make sure the language parameter matches XiaoMu's current language!

查看小木当前语言 / Check XiaoMu's current language:
    ros2 param get /emotion language
"""

import rclpy
from rclpy.node import Node
from robot_interfaces.msg import Speak


class XiaoMuSpeak(Node):
    def __init__(self):
        super().__init__('xiaomu_speak')
        
        # 获取语言参数（默认英文）/ Get language parameter (default: English)
        self.declare_parameter('language', 'en')
        self.language = self.get_parameter('language').value
        
        self.get_logger().info(f'✅ XiaoMu started, language: {self.language}')
        
        self.speak_pub = self.create_publisher(Speak, 'speak', 10)
        self._say_welcome()
    
    def _get_text(self, key, **kwargs):
        """获取对应语言的文本 / Get text in current language"""
        texts = {
            'en': {
                'welcome': 'Hello everyone, I am XiaoMu!',
                'nice_to_meet': 'Nice to meet you all',
                'learn_together': 'Let\'s learn robot programming together',
            },
            'zh-Hans': {
                'welcome': '大家好，我是小木！',
                'nice_to_meet': '很高兴认识你们',
                'learn_together': '让我们一起学习机器人编程吧',
            },
        }
        lang_dict = texts.get(self.language, texts['en'])
        text = lang_dict.get(key, '')
        return text.format(**kwargs) if kwargs else text
    
    def _say_welcome(self):
        """说欢迎语 / Say welcome message"""
        self.say(self._get_text('welcome'))
        self.say(self._get_text('nice_to_meet'))
    
    def say(self, text):
        """让小木说话 / Make XiaoMu speak"""
        msg = Speak()
        msg.text = text
        self.speak_pub.publish(msg)
        self.get_logger().info(f'💬 XiaoMu said: {text}')
    
    def learn(self):
        """演示学习功能 / Demonstrate learning feature"""
        self.say(self._get_text('learn_together'))


def main(args=None):
    rclpy.init(args=args)
    xiaomu = XiaoMuSpeak()
    xiaomu.learn()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
