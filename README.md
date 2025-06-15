# 虚拟设备模拟系统开发设计文档

## 📘 项目简介

本项目旨在构建一个可运行于 Ubuntu 系统的虚拟设备模拟平台，支持多种智能家居设备的模拟，如空调、灯光、温湿度传感器、人体感应器等。模拟设备通过 MQTT 接入 Home Assistant 并支持实时状态查看、MongoDB 数据持久化及 Web 前端可视化。

---

## 📁 项目目录结构

```
virtual-device-simulator/
├── config.yaml                 # 配置文件（MQTT、MongoDB、设备列表等）
├── install.sh                 # 自动安装脚本
├── main.py                    # 主程序入口
├── devices/                   # 各类虚拟设备模拟模块
│   ├── __init__.py
│   ├── air_conditioner.py
│   ├── light.py
│   └── sensor.py
├── mqtt/                      # MQTT 客户端封装
│   └── client.py
├── storage/                   # MongoDB 存储模块
│   └── mongo.py
├── frontend/                  # 前端可视化仪表板（Vue 或 React）
│   └── (Web项目目录)
├── logs/                      # 日志目录
│   └── simulator.log
├── requirements.txt           # Python依赖列表
└── docker-compose.yml         # 一键部署脚本
```

---

## 📋 项目需求说明

### 功能需求

- 模拟设备：空调、灯、传感器（温湿度、人感）
- 配置驱动运行，支持热加载配置
- 设备通过 MQTT 接入 Home Assistant，支持自动发现（MQTT Discovery）
- 状态自动上报 + MongoDB 持久化
- 前端面板查看设备状态、MQTT连接、MongoDB状态
- 错误日志记录，支持分级输出
- 自动安装脚本与系统服务自启动支持

### 非功能性需求

- 高可配置性：通过 YAML 文件集中管理
- 可扩展性：模块化设备模拟插件
- 部署简便：支持 Docker + Systemd
- 稳定性：多线程模拟，服务自动重启

---

## 🔧 核心模块说明

### 1. config.yaml 配置管理
集中配置：
- MQTT broker 地址、端口、用户名密码
- MongoDB 地址与库名
- 每类设备的数量、更新间隔、模拟范围
- PID/DID 自动生成逻辑

### 2. 设备模拟模块（devices/）
每种类型设备为独立模块，支持：
- 定时状态更新
- 状态变化模拟策略（随机、静态、表达式）
- MQTT 发布与控制指令处理

### 3. MQTT通信模块（mqtt/client.py）
- 初始化连接
- 自动重连、心跳包、LWT
- 设备发现消息构造与发送
- 状态消息的发布与订阅

### 4. 数据存储模块（storage/mongo.py）
- MongoDB 连接管理
- 状态上报写入
- 索引自动创建
- TTL（过期）数据清理支持

### 5. 前端仪表盘（frontend/）
- 显示所有设备状态
- 展示 MQTT Broker/MongoDB 连接状态
- 图表化展示传感器数据
- WebSocket 实时刷新

### 6. 日志系统（logs/）
- 控制台输出 + 文件记录
- 日志分级：INFO / WARN / ERROR
- 持久存储与错误追踪

---

## 🚀 安装与使用指南

### 1. 执行自动安装脚本

```bash
chmod +x install.sh
./install.sh
```

### 2. 注册系统服务（自启动）

```bash
sudo cp virtual-device-simulator.service /etc/systemd/system/
sudo systemctl enable virtual-device-simulator.service
sudo systemctl start virtual-device-simulator.service
```

### 3. 查看状态与日志

```bash
sudo systemctl status virtual-device-simulator.service
tail -f logs/simulator.log
```

### 4. Home Assistant 中自动发现
- 设备将通过 `homeassistant/<component>/<pid>/<did>/config` 注册
- 相关消息格式参见 `HA MQTT.md` 文档说明

---

## 🧪 示例配置 config.yaml

```yaml
mqtt:
  host: "127.0.0.1"
  port: 1883
  username: "user"
  password: "pass"

database:
  mongo_url: "mongodb://localhost:27017"
  db_name: "virtual_devices"

devices:
  air_conditioners:
    pid: 1101
    auto_update:
      count: 2           # 自动更新的设备数量
      update_interval: 10
    static:
      count: 1           # 非自动更新（只注册不自动变化）的设备数量
  lights:
    pid: 1201
    auto_update:
      count: 5
      update_interval: 5
    static:
      count: 2
  temperature_sensors:
    pid: 1301
    auto_update:
      count: 4
      update_interval: 6
      range: [18, 32]
    static:
      count: 2
```

### 🔧 DID 自动分配说明

- 每个设备由程序自动分配唯一 `did`（设备ID），例如：`temp_0001`, `light_0003`。
- DID 生成格式可基于：设备类型前缀 + 自增编号
- 所有自动与静态设备的 `did` 均唯一，不重用
mqtt:
  host: "127.0.0.1"
  port: 1883
  username: "user"
  password: "pass"

database:
  mongo_url: "mongodb://localhost:27017"
  db_name: "virtual_devices"

devices:
  air_conditioners:
    pid: 1101
    count: 2
    update_interval: 10
  lights:
    pid: 1201
    count: 5
    update_interval: 5
  temperature_sensors:
    pid: 1301
    count: 4
    range: [18, 32]
    update_interval: 6
```

---

## 📝 License

MIT License

© 2025 LinknLink. This project is free to use, modify, and distribute under the terms of the MIT license.

---

## 👨‍💻 贡献建议

欢迎提交以下内容：
- 新设备模拟插件（如窗帘、插座等）
- 前端功能增强（地图、图表、控制台）
- 性能优化 PR
- 文档改进与多语言支持

如需参与，请 Fork 并提交 Pull Request，感谢贡献！

---
