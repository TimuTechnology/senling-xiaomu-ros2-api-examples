import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from robot_interfaces.msg import Sensor, Saw, Action, Emotion, Touch, Speak, Imu, Servo, Listen, See, Led, Rifd, BatteryStatus
import time
import math


class Simple(Node):
    def __init__(self):
        super().__init__('Simple')
        self.sensor = self.create_subscription(Sensor, 'sensor', self.sensor_callback,10)
        self.sensor  # prevent unused variable warning
        self.touch = self.create_subscription(Touch, 'touch', self.touch_callback,10)
        self.touch  # prevent unused variable warning
        self.touch = self.create_subscription(Imu, 'imu', self.imu_callback,10)
        self.touch  # prevent unused variable warning
        self.eye = self.create_subscription(Saw, 'saw', self.saw_callback,10)
        self.eye  # prevent unused variable warning
        self.ear = self.create_subscription(Listen, 'listen', self.listen_callback,10)
        self.ear# prevent unused variable warning
        self.rifd = self.create_subscription(Rifd, 'rifd', self.rifd_callback,10)
        self.rifd# prevent unused variable warning
        self.battery = self.create_subscription(BatteryStatus, 'battery', self.battery_callback,10)
        self.battery
        
        self.speak_pub = self.create_publisher(Speak, 'speak', 10)
        self.action_pub = self.create_publisher(Action, 'action', 10)
        
        self.speak_pub.publish(self._speak_text('hello, i am programmer'))
        self.get_logger().info('Simple init ...')
    
    def rifd_callback(self, rifd):
        self.get_logger().info('rifd_callback')
        self.get_logger().info('rifd_callback: %s' % rifd.rifd_uid)
    
    def touch_callback(self, touch_data):
        self.get_logger().info('touch_callback:')
        self.get_logger().info('touch_callback: %s %s' % (touch_data.head_touch_state, touch_data.belly_touch_state))
        a = 1
    
    def listen_callback(self, listen_data):
        text = listen_data.data
        self.get_logger().info('listen_callback: %s' % text)
    
    def sensor_callback(self, sensor_data):
        self.get_logger().info('sensor_callback: %s %s' % (sensor_data.humidity, sensor_data.temperature))
        
    def imu_callback(self, imu_data):
        self.get_logger().info('imu data: "%.2f" "%.2f" "%.2f"' % (imu_data.accel_x, imu_data.accel_y, imu_data.accel_z))
        self.get_logger().info('imu data: "%.2f" "%.2f" "%.2f"' % (imu_data.gyro_x, imu_data.gyro_y, imu_data.gyro_z))
    
    def saw_callback(self, saw_data):
        self.get_logger().info('I saw: %s' % (saw_data))
        '''
        following is saw_data properties:
        Person[] persons
        Thing[] things
        
        following is Person properties:
        uint8 emotion
        int64 emotion_point
        uint8 sex
        float64 distance
        uint8 head_direction
        uint8 position
        float64[] bound 人在图片中的位置
        
        following is Thing properties:
        string type
        float64[] bound 物体在图片中的位置
        '''
        
        
    def battery_callback(self, bat_status):
        self.get_logger().info('battery_callback: %s' % bat_status)
        text = ''
        if bat_status.status == BatteryStatus.STATUS_CHARGING:
            #current is charging
            pass
        elif bat_status.status == BatteryStatus.STATUS_FULL:
            #full battery
            pass
        else:
            #ballery is supplying power
            pass
    
    
    def _speak_text(self, text):
        speak = Speak()
        speak.text = text
        return speak
      
    def act_action_with_hand_relative(self, time, head_yaw_angle, head_pitch_angle, body_yaw_angle, left_hand_angle, right_hand_angle):
        self.get_logger().info('act_action_with_hand_relative: %s %s %s %s %s %s' % (time, head_yaw_angle, head_pitch_angle, body_yaw_angle, left_hand_angle, right_hand_angle))
        action = Action()
        action.time = float(time)
        action.type = Action.TYPE_RELATIVE_MOVE
        action.servos = []

        if head_yaw_angle != 0:
            servo = Servo()
            servo.index = Action.INDEX_HEAD_YAW
            servo.angle = head_yaw_angle
            action.servos.append(servo)
        if head_pitch_angle != 0:
            servo = Servo()
            servo.index = Action.INDEX_HEAD_PITCH
            servo.angle = head_pitch_angle
            action.servos.append(servo)
        if body_yaw_angle != 0:
            servo = Servo()
            servo.index = Action.INDEX_BODY_YAW
            servo.angle = body_yaw_angle
            action.servos.append(servo)
        if left_hand_angle != 0:
            servo = Servo()
            servo.index = Action.INDEX_LEFT_HAND_YAW
            servo.angle = left_hand_angle
            action.servos.append(servo)
        if right_hand_angle != 0:
            servo = Servo()
            servo.index = Action.INDEX_RIGHT_HAND_YAW
            servo.angle = right_hand_angle
            action.servos.append(servo)
        self.action_pub.publish(action)
    
    def act_led_brightness(self, time, xbrightness, bbrightness):
        self.get_logger().info("act_xled_brightness: %s %s %s" % (time, xbrightness, bbrightness))
        action = Action()
        action.time = float(time)
        action.type = Action.TYPE_RELATIVE_MOVE
        action.leds = []
        x = Led()
        x.index = Action.INDEX_X_LED
        x.bright = xbrightness
        action.leds.append(x)
        b = Led()
        b.index = Action.INDEX_B_LED
        b.bright = bbrightness
        action.leds.append(b)
        self.action_pub.publish(action)

def main(args=None):
    rclpy.init(args=args)

    simple = Simple()
    try:
        rclpy.spin(simple)
    finally:
        pass

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
