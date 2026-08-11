#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小木编程示例三：读取传感器数据
XiaoMu Programming Example 3: Read Sensor Data

学习目标：读取温湿度、IMU等传感器数据
Learning Goal: Read temperature, humidity, and IMU sensor data

⚠️ 重要提示 / Important Note：
运行此示例前，请确保 language 参数与小木机器人当前语言一致！
Before running this example, make sure the language parameter matches XiaoMu's current language!
"""

import rclpy
import math
from rclpy.node import Node
from robot_interfaces.msg import Sensor, Imu, Speak


class XiaoMuSensor(Node):
    def __init__(self):
        super().__init__('xiaomu_sensor')
        
        self.declare_parameter('language', 'en')
        self.language = self.get_parameter('language').value
        
        self.get_logger().info(f'✅ XiaoMu Sensor started, language: {self.language}')
        
        self.sensor_sub = self.create_subscription(Sensor, 'sensor', self.sensor_callback, 10)
        self.imu_sub = self.create_subscription(Imu, 'imu', self.imu_callback, 10)
        self.speak_pub = self.create_publisher(Speak, 'speak', 10)
        
        self.last_temp = 0
        self.last_humidity = 0
    
    def _get_text(self, key, **kwargs):
        """获取对应语言的文本 / Get text in current language"""
        texts = {
            'en': {
                'temp_report': 'Current temperature is {temp:.1f} degrees Celsius',
                'humidity_report': 'Current humidity is {humidity:.1f} percent',
                'hot_warning': 'It\'s so hot, please cool me down',
                'cold_warning': 'It\'s a bit cold, maybe turn on the heater',
            },
            'zh-Hans': {
                'temp_report': '当前温度为{temp:.1f}摄氏度',
                'humidity_report': '当前湿度为百分之{humidity:.1f}',
                'hot_warning': '好热啊，快帮我降降温吧',
                'cold_warning': '有点冷，是不是该开暖气了',
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
    
    def sensor_callback(self, msg):
        """温湿度传感器回调 / Temperature and humidity sensor callback"""
        temp = msg.temperature
        humidity = msg.humidity
        self.last_temp = temp
        self.last_humidity = humidity
        
        self.get_logger().info(f'🌡️ Temperature: {temp:.1f}°C, Humidity: {humidity:.1f}%')
        
        if temp > 35:
            self._speak(self._get_text('hot_warning'))
        elif temp < 10:
            self._speak(self._get_text('cold_warning'))
    
    def imu_callback(self, msg):
        """IMU传感器回调 / IMU sensor callback"""
        ax, ay, az = msg.accel_x, msg.accel_y, msg.accel_z
        pitch = math.atan2(ax, az) * 180 / math.pi
        
        self.get_logger().info(f'📐 Pitch angle: {pitch:.1f}°')
        
        if abs(ax) > 0.5 or abs(ay) > 0.5:
            self.get_logger().info('✈️ Movement detected!')
    
    def report_environment(self):
        """报告环境状况 / Report environment status"""
        self._speak(self._get_text('temp_report', temp=self.last_temp))
        self._speak(self._get_text('humidity_report', humidity=self.last_humidity))


def main(args=None):
    rclpy.init(args=args)
    node = XiaoMuSensor()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
