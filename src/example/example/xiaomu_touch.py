#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小木编程示例二：触摸互动
XiaoMu Programming Example 2: Touch Interaction

学习目标：订阅话题、处理传感器数据、让小木对触摸做出反应
Learning Goal: Subscribe to topics, process sensor data, respond to touch

⚠️ 重要提示 / Important Note：
运行此示例前，请确保 language 参数与小木机器人当前语言一致！
Before running this example, make sure the language parameter matches XiaoMu's current language!
"""

import rclpy
from rclpy.node import Node
from robot_interfaces.msg import Touch, Speak, Action, Servo


class XiaoMuTouch(Node):
    def __init__(self):
        super().__init__('xiaomu_touch')
        
        self.declare_parameter('language', 'en')
        self.language = self.get_parameter('language').value
        
        self.get_logger().info(f'✅ XiaoMu Touch started, language: {self.language}')
        
        self.touch_sub = self.create_subscription(Touch, 'touch', self.touch_callback, 10)
        self.speak_pub = self.create_publisher(Speak, 'speak', 10)
        self.action_pub = self.create_publisher(Action, 'action', 10)
        
        self._speak(self._get_text('ready'))
    
    def _get_text(self, key, **kwargs):
        """获取对应语言的文本 / Get text in current language"""
        texts = {
            'en': {
                'ready': 'Touch me~',
                'head_single': 'Hehe, patting my head feels so good',
                'head_double': 'Oops, stop knocking',
                'head_long': 'If you keep pressing, I\'ll get dizzy',
                'belly_single': 'Hee hee, that tickles',
                'belly_long': 'Stop tickling me, it\'s so itchy',
            },
            'zh-Hans': {
                'ready': '摸摸我吧~',
                'head_single': '嘿嘿，摸头好舒服呀',
                'head_double': '哎呀，别敲了别敲了',
                'head_long': '你再按我就要晕啦',
                'belly_single': '嘻嘻，好痒啊',
                'belly_long': '不要一直摸啦，好痒好痒',
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
    
    def _nod(self):
        """点头动作 / Nod action"""
        action = Action()
        action.time = 0.5
        action.type = Action.TYPE_RELATIVE_MOVE
        action.servos = []
        servo = Servo()
        servo.index = Action.INDEX_HEAD_PITCH
        servo.angle = -15
        action.servos.append(servo)
        self.action_pub.publish(action)
    
    def _shake_head(self):
        """摇头动作 / Shake head action"""
        action = Action()
        action.time = 0.5
        action.type = Action.TYPE_RELATIVE_MOVE
        action.servos = []
        servo = Servo()
        servo.index = Action.INDEX_HEAD_YAW
        servo.angle = -25
        action.servos.append(servo)
        self.action_pub.publish(action)
    
    def touch_callback(self, msg):
        self.get_logger().info('touch_callback msg: %s' % msg)
        """触摸回调函数 / Touch callback function"""
        head_state = msg.head_touch_state
        
        if head_state == 1:
            self._speak(self._get_text('head_single'))
            self._nod()
        
        belly_state = msg.belly_touch_state
        if belly_state == 1:
            self._speak(self._get_text('belly_single'))
            self._shake_head()
        


def main(args=None):
    rclpy.init(args=args)
    node = XiaoMuTouch()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
