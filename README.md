# XiaoMu Robot Programming Edition – SDK & ROS 2 API Examples
Official API documentation and ready-to-run demo codes for Senling XiaoMu Coding Edition — a compact AI-powered robot platform for makers, students, educators, and robotics researchers.

## 📦 What's Inside
| Directory | Description |
| ---- | ---- |
| `/src/example/example/` | Python demo nodes (speech, motion, vision, sensors) |
| `/launch/` | ROS 2 launch scripts for each demo |
| `/src/example/setup.py` | Package entry point configuration |
| `/src/example/package.xml` | Package dependencies declaration |

## ✨ Key Features
- Native Python 3.9 – Full SDK with clean, documented APIs
- ROS 2 (Iron) Support – Complete message interface for sensor data and motion control
- Open Hardware Interfaces – Exposed hardware interfaces for custom sensors/actuators
- Offline Edge AI – On-device NPU for edge AI inference, no cloud dependency

## 📡 ROS 2 Message Interface
XiaoMu communicates through ROS 2 topics. Subscribe to sensor data or publish control commands.

### Subscribe (Sensor Data)
| Topic | Message Type |
| ---- | ---- |
| `/sensor` | Sensor (temperature, humidity) |
| `/imu` | Imu (attitude) |
| `/touch` | Touch |
| `/listen` | Listen (speech recognition) |
| `/rifd` | Rifd |
| `/battery` | BatteryStatus |
| `/saw` | Saw (vision results) |

### Publish (Control Commands)
| Topic | Message Type |
| ---- | ---- |
| `/speak` | Speak (speech output) |
| `/action` | Action (motion control) |
| `/eye` | See (vision control) |

## 🚀 Ready-to-Run Demo Examples
| Demo File | Description |
| ---- | ---- |
| `simple.py` | Subscribe to all sensor topics |
| `xiaomu_speak.py` | Make XiaoMu speak |
| `xiaomu_touch.py` | Respond when head or belly is touched |
| `xiaomu_sense.py` | Read temperature, humidity, IMU and announce |
| `xiaomu_move.py` | Motion control: nod, shake head, wave |
| `xiaomu_chat.py` | Full interaction: speech, motion, touch |
| `xiaomu_vision.py` | Face emotion and object recognition |

## ⚡ Quick Start
### Prerequisites
- XiaoMu Robot (powered on)
- Wi-Fi router
- Computer (Windows / macOS / Linux)

#### Step 1: Connect XiaoMu to Wi-Fi
Start XiaoMu following the user manual. Enter network configuration mode, select your Wi-Fi network, enter password, and wait for voice prompt: "Network connected".

#### Step 2: Get Robot IP Address
Check your router's "Connected Devices" or "DHCP Client List" for a device named linaro-alip. Record its IP (e.g., 192.168.1.101).

#### Step 3: SSH into the Robot
```bash
ssh linaro@<robot-ip>
