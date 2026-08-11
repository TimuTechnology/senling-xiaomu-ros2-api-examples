#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小木编程示例六：视觉识别控制
XiaoMu Programming Example 6: Vision Recognition Control

学习目标：控制小木的视觉模块，识别人脸情绪、距离以及各种物体
Learning Goal: Control XiaoMu's vision module to recognize face emotions, distance and various objects

视觉指令说明 / Vision Commands:
    See.COMMAND_START_SEE  - 开启视觉识别 / Start vision recognition
    See.COMMAND_STOP_SEE   - 关闭视觉识别 / Stop vision recognition

识别结果会自动通过 /saw 话题发布，无需手动获取
Recognition results are automatically published via /saw topic, no manual fetch needed

复位指令说明 / Reset Command:
    Action.TYPE_RESET - 复位所有伺服电机到初始位置

⚠️ 重要提示 / Important Note：
运行此示例前，请确保 language 参数与小木机器人当前语言一致！
Before running this example, make sure the language parameter matches XiaoMu's current language!
"""

import rclpy
import time
from rclpy.node import Node
from robot_interfaces.msg import See, Saw, Speak, Action, Servo


# ============================================================
# 视觉常量定义 / Vision Constants Definition
# ============================================================

# 情绪类型 / Emotion Types
PERSON_HAPPY = 1
PERSON_SAD = 2
PERSON_SURPRISE = 3
PERSON_ANGER = 4
PERSON_DISGUST = 5
PERSON_FEAR = 6
PERSON_CONTEMPT = 7
PERSON_NEUTRAL = 8

# 位置常量 / Position Constants
POSITION_RIGHT = 1
POSITION_LEFT = 2
POSITION_UP = 4
POSITION_DOWN = 8

# 物体类型常量 / Object Type Constants
TYPE_PERSON = "person"
TYPE_BICYCLE = "bicycle"
TYPE_CAR = "car"
TYPE_MOTORBIKE = "motorbike"
TYPE_AEROPLANE = "aeroplane"
TYPE_BUS = "bus"
TYPE_TRAIN = "train"
TYPE_TRUCK = "truck"
TYPE_BOAT = "boat"
TYPE_TRAFFIC_LIGHT = "traffic light"
TYPE_FIRE_HYDRANT = "fire hydrant"
TYPE_STOP_SIGN = "stop sign"
TYPE_PARKING_METER = "parking meter"
TYPE_BENCH = "bench"
TYPE_BIRD = "bird"
TYPE_CAT = "cat"
TYPE_DOG = "dog"
TYPE_HORSE = "horse"
TYPE_SHEEP = "sheep"
TYPE_COW = "cow"
TYPE_ELEPHANT = "elephant"
TYPE_BEAR = "bear"
TYPE_ZEBRA = "zebra"
TYPE_GIRAFFE = "giraffe"
TYPE_BACKPACK = "backpack"
TYPE_UMBRELLA = "umbrella"
TYPE_HANDBAG = "handbag"
TYPE_TIE = "tie"
TYPE_SUITCASE = "suitcase"
TYPE_FRISBEE = "frisbee"
TYPE_SKIS = "skis"
TYPE_SNOWBOARD = "snowboard"
TYPE_SPORTS_BALL = "sports ball"
TYPE_KITE = "kite"
TYPE_BASEBALL_BAT = "baseball bat"
TYPE_BASEBALL_GLOVE = "baseball glove"
TYPE_SKATEBOARD = "skateboard"
TYPE_SURFBOARD = "surfboard"
TYPE_TENNIS_RACKET = "tennis racket"
TYPE_BOTTLE = "bottle"
TYPE_WINE_GLASS = "wine glass"
TYPE_CUP = "cup"
TYPE_FORK = "fork"
TYPE_KNIFE = "knife"
TYPE_SPOON = "spoon"
TYPE_BOWL = "bowl"
TYPE_BANANA = "banana"
TYPE_APPLE = "apple"
TYPE_SANDWICH = "sandwich"
TYPE_ORANGE = "orange"
TYPE_BROCCOLI = "broccoli"
TYPE_CARROT = "carrot"
TYPE_HOT_DOG = "hot dog"
TYPE_PIZZA = "pizza"
TYPE_DONUT = "donut"
TYPE_CAKE = "cake"
TYPE_CHAIR = "chair"
TYPE_SOFA = "sofa"
TYPE_POTTEDPLANT = "pottedplant"
TYPE_BED = "bed"
TYPE_DININGTABLE = "diningtable"
TYPE_TOILET = "toilet"
TYPE_TVMONITOR = "tvmonitor"
TYPE_LAPTOP = "laptop"
TYPE_MOUSE = "mouse"
TYPE_REMOTE = "remote"
TYPE_KEYBOARD = "keyboard"
TYPE_CELLPHONE = "cell phone"
TYPE_MICROWAVE = "microwave"
TYPE_OVEN = "oven"
TYPE_TOASTER = "toaster"
TYPE_SINK = "sink"
TYPE_REFRIGERATOR = "refrigerator"
TYPE_BOOK = "book"
TYPE_CLOCK = "clock"
TYPE_VASE = "vase"
TYPE_SCISSORS = "scissors"
TYPE_TEDDY_BEAR = "teddy bear"
TYPE_HAIR_DRIER = "hair drier"
TYPE_TOOTHBRUSH = "toothbrush"


class XiaoMuVision(Node):
    def __init__(self):
        super().__init__('xiaomu_vision')
        
        # 获取语言参数（默认英文）/ Get language parameter (default: English)
        self.declare_parameter('language', 'en')
        self.language = self.get_parameter('language').value
        
        self.get_logger().info(f'✅ XiaoMu Vision started, language: {self.language}')
        
        # 创建发布者 / Create publishers 
        self.eye_pub = self.create_publisher(See, 'eye', 10)
        self.speak_pub = self.create_publisher(Speak, 'speak', 10)
        self.action_pub = self.create_publisher(Action, 'action', 10)
        
        # 订阅视觉识别结果 / Subscribe to vision recognition results
        self.saw_sub = self.create_subscription(Saw, 'saw', self.saw_callback, 10)
        
        # 状态变量 / State variables
        self.is_vision_on = False
        
        self.get_logger().info('📷 Vision module ready')
        self._speak(self._get_text('ready'))
    
    # ============================================================
    # 复位功能 / Reset Function
    # ============================================================
    
    def reset(self, duration=1.0):
        """
        复位所有伺服电机到初始位置
        Reset all servo motors to initial position
        
        参数 / Args:
            duration: 复位动作执行时间（秒）/ Reset action duration (seconds)
        """
        action = Action()
        action.time = float(duration)
        action.type = Action.TYPE_RESET
        
        self.action_pub.publish(action)
        self.get_logger().info(f'🔄 Reset command sent, duration: {duration}s')
        time.sleep(duration + 0.1)
    
    # ============================================================
    # 辅助函数 / Helper Functions
    # ============================================================
    
    def _get_emotion_name(self, emotion_code):
        """获取情绪名称 / Get emotion name"""
        emotions = {
            PERSON_HAPPY: self._get_text('emotion_happy'),
            PERSON_SAD: self._get_text('emotion_sad'),
            PERSON_SURPRISE: self._get_text('emotion_surprise'),
            PERSON_ANGER: self._get_text('emotion_anger'),
            PERSON_DISGUST: self._get_text('emotion_disgust'),
            PERSON_FEAR: self._get_text('emotion_fear'),
            PERSON_CONTEMPT: self._get_text('emotion_contempt'),
            PERSON_NEUTRAL: self._get_text('emotion_neutral'),
        }
        return emotions.get(emotion_code, self._get_text('emotion_unknown'))
    
    def _get_position_name(self, position_code):
        """获取位置名称 / Get position name"""
        positions = []
        if position_code & POSITION_RIGHT:
            positions.append(self._get_text('pos_right'))
        if position_code & POSITION_LEFT:
            positions.append(self._get_text('pos_left'))
        if position_code & POSITION_UP:
            positions.append(self._get_text('pos_up'))
        if position_code & POSITION_DOWN:
            positions.append(self._get_text('pos_down'))
        return ', '.join(positions) if positions else self._get_text('pos_center')
    
    def _get_thing_name(self, thing_type):
        """
        获取物体类型的本地化名称 / Get localized thing name
        
        参数 / Args:
            thing_type: 物体类型常量 / Thing type constant
        
        返回 / Returns:
            本地化的物体名称 / Localized thing name
        """
        thing_names = {
            'en': {
                'person': 'person',
                'bicycle': 'bicycle',
                'car': 'car',
                'motorbike': 'motorbike',
                'aeroplane': 'aeroplane',
                'bus': 'bus',
                'train': 'train',
                'truck': 'truck',
                'boat': 'boat',
                'traffic light': 'traffic light',
                'fire hydrant': 'fire hydrant',
                'stop sign': 'stop sign',
                'parking meter': 'parking meter',
                'bench': 'bench',
                'bird': 'bird',
                'cat': 'cat',
                'dog': 'dog',
                'horse': 'horse',
                'sheep': 'sheep',
                'cow': 'cow',
                'elephant': 'elephant',
                'bear': 'bear',
                'zebra': 'zebra',
                'giraffe': 'giraffe',
                'backpack': 'backpack',
                'umbrella': 'umbrella',
                'handbag': 'handbag',
                'tie': 'tie',
                'suitcase': 'suitcase',
                'frisbee': 'frisbee',
                'skis': 'skis',
                'snowboard': 'snowboard',
                'sports ball': 'sports ball',
                'kite': 'kite',
                'baseball bat': 'baseball bat',
                'baseball glove': 'baseball glove',
                'skateboard': 'skateboard',
                'surfboard': 'surfboard',
                'tennis racket': 'tennis racket',
                'bottle': 'bottle',
                'wine glass': 'wine glass',
                'cup': 'cup',
                'fork': 'fork',
                'knife': 'knife',
                'spoon': 'spoon',
                'bowl': 'bowl',
                'banana': 'banana',
                'apple': 'apple',
                'sandwich': 'sandwich',
                'orange': 'orange',
                'broccoli': 'broccoli',
                'carrot': 'carrot',
                'hot dog': 'hot dog',
                'pizza': 'pizza',
                'donut': 'donut',
                'cake': 'cake',
                'chair': 'chair',
                'sofa': 'sofa',
                'pottedplant': 'potted plant',
                'bed': 'bed',
                'diningtable': 'dining table',
                'toilet': 'toilet',
                'tvmonitor': 'TV monitor',
                'laptop': 'laptop',
                'mouse': 'mouse',
                'remote': 'remote control',
                'keyboard': 'keyboard',
                'cell phone': 'cell phone',
                'microwave': 'microwave',
                'oven': 'oven',
                'toaster': 'toaster',
                'sink': 'sink',
                'refrigerator': 'refrigerator',
                'book': 'book',
                'clock': 'clock',
                'vase': 'vase',
                'scissors': 'scissors',
                'teddy bear': 'teddy bear',
                'hair drier': 'hair drier',
                'toothbrush': 'toothbrush',
            },
            'zh-Hans': {
                'person': '人',
                'bicycle': '自行车',
                'car': '汽车',
                'motorbike': '摩托车',
                'aeroplane': '飞机',
                'bus': '公交车',
                'train': '火车',
                'truck': '卡车',
                'boat': '船',
                'traffic light': '红绿灯',
                'fire hydrant': '消防栓',
                'stop sign': '停车标志',
                'parking meter': '停车计时器',
                'bench': '长椅',
                'bird': '鸟',
                'cat': '猫',
                'dog': '狗',
                'horse': '马',
                'sheep': '羊',
                'cow': '牛',
                'elephant': '大象',
                'bear': '熊',
                'zebra': '斑马',
                'giraffe': '长颈鹿',
                'backpack': '背包',
                'umbrella': '雨伞',
                'handbag': '手提包',
                'tie': '领带',
                'suitcase': '行李箱',
                'frisbee': '飞盘',
                'skis': '滑雪板',
                'snowboard': '单板滑雪板',
                'sports ball': '运动球',
                'kite': '风筝',
                'baseball bat': '棒球棒',
                'baseball glove': '棒球手套',
                'skateboard': '滑板',
                'surfboard': '冲浪板',
                'tennis racket': '网球拍',
                'bottle': '瓶子',
                'wine glass': '酒杯',
                'cup': '杯子',
                'fork': '叉子',
                'knife': '刀',
                'spoon': '勺子',
                'bowl': '碗',
                'banana': '香蕉',
                'apple': '苹果',
                'sandwich': '三明治',
                'orange': '橙子',
                'broccoli': '西兰花',
                'carrot': '胡萝卜',
                'hot dog': '热狗',
                'pizza': '披萨',
                'donut': '甜甜圈',
                'cake': '蛋糕',
                'chair': '椅子',
                'sofa': '沙发',
                'pottedplant': '盆栽植物',
                'bed': '床',
                'diningtable': '餐桌',
                'toilet': '马桶',
                'tvmonitor': '电视显示器',
                'laptop': '笔记本电脑',
                'mouse': '鼠标',
                'remote': '遥控器',
                'keyboard': '键盘',
                'cell phone': '手机',
                'microwave': '微波炉',
                'oven': '烤箱',
                'toaster': '烤面包机',
                'sink': '水槽',
                'refrigerator': '冰箱',
                'book': '书',
                'clock': '时钟',
                'vase': '花瓶',
                'scissors': '剪刀',
                'teddy bear': '泰迪熊',
                'hair drier': '吹风机',
                'toothbrush': '牙刷',
            },
        }
        lang_dict = thing_names.get(self.language, thing_names['en'])
        return lang_dict.get(thing_type, thing_type)
    
    def _get_text(self, key, **kwargs):
        """获取对应语言的文本 / Get text in current language"""
        texts = {
            'en': {
                'ready': 'Vision module is ready',
                'vision_on': 'Vision recognition started, I can see you now',
                'vision_off': 'Vision recognition stopped',
                # Emotions
                'emotion_happy': 'happy',
                'emotion_sad': 'sad',
                'emotion_surprise': 'surprised',
                'emotion_anger': 'angry',
                'emotion_disgust': 'disgusted',
                'emotion_fear': 'fearful',
                'emotion_contempt': 'contemptuous',
                'emotion_neutral': 'neutral',
                'emotion_unknown': 'unknown',
                # Positions
                'pos_right': 'right',
                'pos_left': 'left',
                'pos_up': 'up',
                'pos_down': 'down',
                'pos_center': 'center',
                # Reactions
                'see_person': 'I see a person',
                'see_thing': 'I see a {thing}',
                'person_emotion': 'The person looks {emotion}',
                'person_distance': 'The person is {distance:.1f} meters away',
                'person_position': 'The person is on the {position}',
                'greeting': 'Hello! Nice to see you',
                'happy_response': 'You look happy! That makes me happy too',
                'sad_response': 'You look sad. I am here for you',
                'wave': 'I see you, let me wave to you',
            },
            'zh-Hans': {
                'ready': '视觉模块已就绪',
                'vision_on': '视觉识别已开启，我能看到你了',
                'vision_off': '视觉识别已关闭',
                # Emotions
                'emotion_happy': '开心',
                'emotion_sad': '难过',
                'emotion_surprise': '惊讶',
                'emotion_anger': '生气',
                'emotion_disgust': '厌恶',
                'emotion_fear': '害怕',
                'emotion_contempt': '轻蔑',
                'emotion_neutral': '平静',
                'emotion_unknown': '未知',
                # Positions
                'pos_right': '右边',
                'pos_left': '左边',
                'pos_up': '上方',
                'pos_down': '下方',
                'pos_center': '中间',
                # Reactions
                'see_person': '我看到一个人',
                'see_thing': '我看到了{thing}',
                'person_emotion': '这个人看起来{emotion}',
                'person_distance': '这个人距离{distance:.1f}米',
                'person_position': '这个人在{position}',
                'greeting': '你好！很高兴见到你',
                'happy_response': '你看起来很开心！我也跟着开心起来了',
                'sad_response': '你看起来有点难过，我会一直陪着你的',
                'wave': '我看到你了，给你挥个手',
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
        action.time = float(duration)  # 强制转换为 float
        action.type = Action.TYPE_RELATIVE_MOVE
        action.servos = servos
        self.action_pub.publish(action)
    
    def _wave(self):
        """挥手 / Wave"""
        servos = []
        servo = Servo()
        servo.index = Action.INDEX_RIGHT_HAND_YAW
        servo.angle = 35
        servos.append(servo)
        self._execute(servos, 0.5)
        # 复位 / Reset
        servos = []
        servo = Servo()
        servo.index = Action.INDEX_RIGHT_HAND_YAW
        servo.angle = -35
        servos.append(servo)
        self._execute(servos, 0.3)
        self.get_logger().info('👋 Wave')
    
    def _nod(self):
        """点头 / Nod (向下转)"""
        servos = []
        servo = Servo()
        servo.index = Action.INDEX_HEAD_PITCH
        servo.angle = 10  # 正值 = 向下转（低头）
        servos.append(servo)
        self._execute(servos, 0.4)
        # 复位 / Reset
        servos = []
        servo = Servo()
        servo.index = Action.INDEX_HEAD_PITCH
        servo.angle = -10
        servos.append(servo)
        self._execute(servos, 0.2)
    
    def _look_up(self):
        """向上看 / Look up (负值 = 向上仰)"""
        servos = []
        servo = Servo()
        servo.index = Action.INDEX_HEAD_PITCH
        servo.angle = -25  # 负值 = 向上仰
        servos.append(servo)
        self._execute(servos, 0.4)
        # 复位 / Reset
        servos = []
        servo = Servo()
        servo.index = Action.INDEX_HEAD_PITCH
        servo.angle = 25
        servos.append(servo)
        self._execute(servos, 0.2)
    
    def _look_at(self, position_code):
        """看向指定方向 / Look at specified direction"""
        servos = []
        
        # 水平方向控制 / Horizontal control
        if position_code & POSITION_LEFT:
            servo = Servo()
            servo.index = Action.INDEX_HEAD_YAW
            servo.angle = -30
            servos.append(servo)
        elif position_code & POSITION_RIGHT:
            servo = Servo()
            servo.index = Action.INDEX_HEAD_YAW
            servo.angle = 30
            servos.append(servo)
        
        # 垂直方向控制 / Vertical control
        # 注意：负值向上仰，正值向下转
        if position_code & POSITION_UP:
            servo = Servo()
            servo.index = Action.INDEX_HEAD_PITCH
            servo.angle = -15  # 向上看
            servos.append(servo)
        elif position_code & POSITION_DOWN:
            servo = Servo()
            servo.index = Action.INDEX_HEAD_PITCH
            servo.angle = 15  # 向下看
            servos.append(servo)
        
        self.reset()
    
    # ============================================================
    # 视觉控制函数 / Vision Control Functions
    # ============================================================
    
    def start_vision(self):
        """开启视觉识别 / Start vision recognition"""
        if not self.is_vision_on:
            see = See()
            see.command = See.COMMAND_START_SEE
            self.eye_pub.publish(see)
            self.is_vision_on = True
            self.get_logger().info('📷 Vision ON command sent to /eye topic')
            self._speak(self._get_text('vision_on'))
            time.sleep(0.5)
    
    def stop_vision(self):
        """关闭视觉识别 / Stop vision recognition"""
        if self.is_vision_on:
            see = See()
            see.command = See.COMMAND_STOP_SEE
            self.eye_pub.publish(see)
            self.is_vision_on = False
            self.get_logger().info('📷 Vision OFF command sent to /eye topic')
            self._speak(self._get_text('vision_off'))
    
    def saw_callback(self, saw_data):
        """
        视觉识别结果回调 / Vision recognition result callback
        
        识别结果包含 / Recognition result contains:
            saw_data.persons[]   - 检测到的人 / Detected persons
            saw_data.things[]    - 检测到的物体 / Detected things
        """
        self.get_logger().info('👁️ Received vision result')
        
        # ============================================================
        # 处理检测到的人 / Process detected persons
        # ============================================================
        if saw_data.persons:
            self.get_logger().info(f'👤 Detected {len(saw_data.persons)} person(s)')
            
            for person in saw_data.persons:
                # 获取情绪名称 / Get emotion name
                emotion_name = self._get_emotion_name(person.emotion)
                self.get_logger().info(f'  - Emotion: {emotion_name} (code: {person.emotion}, intensity: {person.emotion_point}')
                
                # 获取距离 / Get distance
                self.get_logger().info(f'  - Distance: {person.distance:.2f}m')
                
                # 获取位置 / Get position
                position_name = self._get_position_name(person.position)
                self.get_logger().info(f'  - Position: {position_name}')
                
                # 获取边界框 / Get bounding box
                if len(person.bound) >= 4:
                    self.get_logger().info(f'  - Bounding box: left={person.bound[0]:.0f}, top={person.bound[1]:.0f}, '
                                          f'right={person.bound[2]:.0f}, bottom={person.bound[3]:.0f}')
                
                # 根据情绪和距离做出反应 / React based on emotion and distance
                self._react_to_person(person)
        
        # ============================================================
        # 处理检测到的物体 / Process detected things
        # ============================================================
        if saw_data.things:
            self.get_logger().info(f'📦 Detected {len(saw_data.things)} thing(s)')
            
            for thing in saw_data.things:
                # 获取本地化的物体名称 / Get localized thing name
                thing_name = self._get_thing_name(thing.type)
                self.get_logger().info(f'  - Type: {thing.type} -> {thing_name}')
                
                # 获取边界框 / Get bounding box
                if len(thing.bound) >= 4:
                    self.get_logger().info(f'  - Bounding box: left={thing.bound[0]:.0f}, top={thing.bound[1]:.0f}, '
                                          f'right={thing.bound[2]:.0f}, bottom={thing.bound[3]:.0f}')
                
                # 根据物体类型做出反应 / React based on object type
                self._react_to_thing(thing, thing_name)
    
    def _react_to_person(self, person):
        """根据检测到的人做出反应 / React to detected person"""
        emotion_name = self._get_emotion_name(person.emotion)
        
        # 报告看到人 / Report seeing a person
        self._speak(self._get_text('see_person'))
        
        # 报告情绪 / Report emotion
        self._speak(self._get_text('person_emotion', emotion=emotion_name))
        
        
        # 报告位置 / Report position
        if person.position != 0:
            position_name = self._get_position_name(person.position)
            self._speak(self._get_text('person_position', position=position_name))
        
        # 根据情绪做出不同反应 / React differently based on emotion
        if person.emotion == PERSON_HAPPY:
            self._speak(self._get_text('happy_response'))
            self._wave()
        elif person.emotion == PERSON_SAD:
            self._speak(self._get_text('sad_response'))
            self._nod()
        elif person.emotion == PERSON_SURPRISE:
            self._speak(self._get_text('greeting'))
            self._wave()
        elif person.emotion == PERSON_ANGER:
            self._speak(self._get_text('greeting'))
        else:
            self._wave()
        
        # 看向人的方向 / Look at the person's direction
        if person.position != 0:
            self._look_at(person.position)
    
    def _react_to_thing(self, thing, thing_name):
        """根据检测到的物体做出反应 / React to detected object"""
        # 报告看到的物体 / Report seeing an object (使用本地化名称)
        self._speak(self._get_text('see_thing', thing=thing_name))
        
        # 针对特定物体的反应 / Specific object reactions
        if thing.type == TYPE_DOG or thing.type == TYPE_CAT:
            if self.language == 'zh-Hans':
                self._speak("好可爱的小动物呀")
            else:
                self._speak("What a cute little animal")
        elif thing.type == TYPE_CELLPHONE:
            if self.language == 'zh-Hans':
                self._speak("哦，是一部手机")
            else:
                self._speak("Oh, a cell phone")
        elif thing.type == TYPE_BOOK:
            if self.language == 'zh-Hans':
                self._speak("读书是很好的习惯")
            else:
                self._speak("Reading is a good habit")


def main(args=None):
    rclpy.init(args=args)
    node = XiaoMuVision()
    
    # 演示视觉功能 / Demonstrate vision functions
    node.start_vision()
    
    # 等待一段时间观察结果 / Wait for results
    try:
        rclpy.spin(node)
    finally:
        node.stop_vision()
        node.reset(2.0)
    
    
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()
