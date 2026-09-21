XiaoMu Robot Programming Edition – SDK & ROS 2 API Examples
Official API documentation and ready-to-run demo codes for Senling XiaoMu Coding Edition — a compact AI-powered robot platform for makers, students, educators, and robotics researchers.

What's Inside
Directory	Description
/src/example/example/	Python demo nodes (speech, motion, vision, sensors, etc.)
/launch/	ROS 2 launch scripts for each demo
/src/example/setup.py	Package entry point configuration
/src/example/package.xml	Package dependencies declaration
Key Features
Native Python 3.9 – Full SDK with clean, documented APIs

ROS 2 (Iron) Support – Complete message interface ecosystem for sensor data acquisition and motion control

Open Hardware Interfaces – Exposed hardware interfaces for custom sensor/actuator integration

Offline Edge AI – On-device NPU for edge AI inference, no cloud dependency

ROS 2 Message Interface
XiaoMu communicates through ROS 2 topics. Subscribe to sensor data or publish control commands:

Subscribe (Sensor)

Topic	Message Type
/sensor	Sensor (temperature, humidity)
/imu	Imu (attitude)
/touch	Touch
/listen	Listen (speech recognition)
/rifd	Rifd
/battery	BatteryStatus
/saw	Saw (vision results)
Publish (Control)

Topic	Message Type
/speak	Speak (speech output)
/action	Action (motion control)
/eye	See (vision control)
Ready-to-Run Demo Examples
Demo File	Description
simple.py	Subscribe to all sensor topics (temperature, IMU, touch, vision, speech, etc.)
xiaomu_speak.py	Make XiaoMu speak
xiaomu_touch.py	Respond when head or belly is touched
xiaomu_sense.py	Read temperature, humidity, IMU data and announce
xiaomu_move.py	Motion control: nod, shake head, wave, etc.
xiaomu_chat.py	Full interaction integrating speech recognition, motion, and touch
xiaomu_vision.py	Face emotion and object recognition with responses
Quick Start
Prerequisites
XiaoMu Robot (powered on)

Wi-Fi router

Computer (Windows / macOS / Linux)

Step 1: Connect XiaoMu to Wi-Fi
Start XiaoMu Robot following the user manual. Enter network configuration mode, select your Wi-Fi network, enter password, and wait for the voice prompt: "Network connected".

Step 2: Get Robot IP Address
Check your router's "Connected Devices" or "DHCP Client List" for a device named linaro-alip and record its IP address (e.g., 192.168.1.101).

Step 3: SSH into the Robot
bash
ssh linaro@<robot-ip>
Login Credentials:

Item	Information
Username	linaro
Password	linaro
Port	22 (default)
Step 4: Verify Python & ROS 2 Environment
bash
python3 --version    # Should show Python 3.9.2
ros2 node list       # Verify ROS 2 is running
Step 5: Build the Workspace
bash
cd /home/linaro/tm_study
colcon build --packages-select example
Step 6: Source the Environment & Run a Demo
bash
source /home/linaro/tm_study/install/setup.bash
ros2 launch launch/simple_launch.py
All available launch scripts:

bash
ros2 launch launch/simple_launch.py   # Basic sensor reading
ros2 launch launch/speak_launch.py    # Speech output
ros2 launch launch/touch_launch.py    # Touch interaction
ros2 launch launch/sense_launch.py    # Sensor reading
ros2 launch launch/move_launch.py     # Motion control
ros2 launch launch/chat_launch.py     # Intelligent chat
ros2 launch launch/vision_launch.py   # Vision recognition
API Reference
Import Message Types
python
from robot_interfaces.msg import Sensor, Imu, Touch, Speak, Listen, Action, Servo, See, Saw, BatteryStatus
Subscribe to Sensor Data
Temperature & Humidity (/sensor)

python
def sensor_callback(self, msg):
    temp = msg.temperature
    humidity = msg.humidity
    self.get_logger().info(f'Temperature: {temp:.1f}°C, Humidity: {humidity:.1f}%')
Touch Sensor (/touch) – 0 = no touch, 1 = touched

python
def touch_callback(self, msg):
    if msg.head_touch_state == 1:
        self._speak("Hehe, patting my head feels so good")
    if msg.belly_touch_state == 1:
        self._speak("Hee hee, that tickles")
Speech Recognition (/listen)

python
def listen_callback(self, msg):
    text = msg.data.lower()
    if 'hello' in text:
        self._speak("Hello! Nice to see you")
Vision Recognition (/saw) – returns persons and things lists

python
def saw_callback(self, saw_data):
    for person in saw_data.persons:
        if person.emotion == 1:
            self._wave()
            self._speak("You look happy!")
Battery Status (/battery) – 1 = charging, 2 = full

python
def battery_callback(self, msg):
    if msg.status == 1:
        self.get_logger().info('Charging')
    elif msg.status == 2:
        self.get_logger().info('Battery full')
Publish Control Commands
Speech Output (/speak)

python
def _speak(self, text):
    msg = Speak()
    msg.text = text
    self.speak_pub.publish(msg)
Motion Control (/action)

python
def _wave(self):
    action = Action()
    action.time = 0.5
    servo = Servo()
    servo.index = 4
    servo.angle = 45
    action.servos.append(servo)
    self.action_pub.publish(action)

def reset(self, duration=1.0):
    action = Action()
    action.time = float(duration)
    action.type = 2  # Reset type
    self.action_pub.publish(action)
Vision Control (/eye)

python
def start_vision(self):
    see = See()
    see.command = 1
    self.eye_pub.publish(see)
API Cheat Sheet
Function	Operation	Interface
Make XiaoMu speak	Publish	Speak
Control servos	Publish	Action + Servo
Reset servos	Publish	Action (Reset type)
Start vision	Publish	See (start command)
Read temperature & humidity	Subscribe	Sensor
Read IMU attitude	Subscribe	Imu
Read touch status	Subscribe	Touch
Read speech recognition	Subscribe	Listen
Get vision results	Subscribe	Saw
Note: Field types, constant values, and servo indexes are subject to the actual output of the ros2 interface show command.

Creating Custom Programs
1. Add a New Python File
Place your custom Python files in:

bash
/home/linaro/tm_study/src/example/example/
2. Add a Launch Script
Place launch scripts in:

bash
/home/linaro/tm_study/launch/
Launch script template:

python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='example',
            namespace='tmmini',
            executable='my_custom_node',
            name='my_custom_node'
        ),
    ])
3. Register Entry Point in setup.py
python
entry_points={
    'console_scripts': [
        'my_custom_node = example.my_custom_node:main',
    ],
}
4. Add Dependencies in package.xml
xml
<exec_depend>python3-requests</exec_depend>
<exec_depend>python3-numpy</exec_depend>
<exec_depend>python3-opencv</exec_depend>
5. Rebuild and Run
bash
cd /home/linaro/tm_study
colcon build
source install/setup.bash
ros2 launch launch/my_custom_launch.py
Important Notes
Program Conflict Handling: If your custom program conflicts with the robot's main control (e.g., occupying the same sensors), press Ctrl+C to stop your program or reboot the robot.

System Environment: Only operate in your working directory (/home/linaro/tm_study/). Do not modify system parameters, environment variables, or key system directories.

Maintenance: Do not attempt to crack system permissions or delete key system files.

Troubleshooting
Issue	Possible Cause	Solution
SSH connection failed	Wrong IP or network unreachable	Reconfirm IP via router; check same network
Incorrect password	Caps lock or typo	Password is linaro (lowercase)
SFTP transfer failed	Insufficient disk space	Run df -h to check; clean unnecessary files
Program runtime error	Missing Python dependencies	Add dependencies in package.xml and rebuild
Build failed	Wrong setup.py configuration	Check entry_points format
Launch file not found	Launch file misplaced	Confirm in /home/linaro/tm_study/launch/
Conflict with main control	Resource occupation conflict	Stop custom program or reboot robot
Who Is This For?
Audience	How XiaoMu Helps
Makers & Hobbyists	Build creative robotics projects with an affordable, extensible platform
Students & Educators	Learn ROS 2, Python, and AI through hands-on practice
Robotics Researchers	Prototype and test edge-AI algorithms on real hardware
License
Proprietary License – All rights reserved. See LICENSE file for details.

Copyright & Confidentiality: This repository contains proprietary information of Timu Technology. Unauthorized reproduction, distribution, or use is strictly prohibited.

Connect with Us
Official Website: https://store.timuai.com

Email Support: wangjing@timuai.com
