# 虚拟设备模拟系统开发设计文档

## 📘 项目简介

本项目旨在构建一个可运行于 Ubuntu 系统的虚拟设备模拟平台，支持多种智能家居设备的模拟，如空调、灯光、温湿度传感器、人体感应器等。模拟设备通过 MQTT 接入 Home Assistant 并支持实时状态查看、MongoDB 数据持久化及 Web 前端可视化。

---

## 📁 项目目录结构

```
virtual-device-simulator/
├── backend/                            # 后端 FastAPI 接口服务
│   ├── api.py                          # FastAPI 应用入口
│   ├── .env                            # MongoDB 配置
│   ├── requirements.txt                # 后端依赖
│   └── logs/                           # 后端日志（软链接或共享）
│       └── simulator.log
│
├── core/                               # 主程序运行逻辑（设备模拟）
│   ├── main.py                         # 启动主程序
│   ├── config.yaml                     # 主配置文件
│   ├── requirements.txt                # 主程序依赖
│   ├── install.sh                      # 安装脚本
│   ├── mqtt/                           # MQTT 客户端封装
│   │   └── client.py
│   ├── storage/                         # MongoDB 存储模块
│   │   └── mongo.py
│   ├── utils/
│   │   └── config.py
│   └── devices/                        # 各类虚拟设备模拟模块
│       ├── __init__.py
│       ├── air_conditioner.py
│       ├── light.py
│       └── sensor.py
│
├── frontend/                           # 前端仪表盘（Vue 3）
│   ├── index.html
│   ├── main.ts
│   ├── App.vue
│   ├── router.ts
│   ├── assets/
│   ├── pages/                          # 页面（首页、设备总览、日志）
│   │   ├── Dashboard.vue
│   │   ├── Devices.vue
│   │   ├── Logs.vue
│   │   └── MongoStats.vue
│   ├── store/                          # Pinia 状态管理
│   ├── utils/                          # 工具函数与接口封装
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── package.json
│
├── docker-compose.yml                  # 可选：统一部署入口
└── README.md

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
# 🚀 虚拟设备模拟系统使用说明

## 📦 安装方式

### ✅ 安装主程序与依赖（Ubuntu）
```bash
# 克隆仓库
git clone https://github.com/your-org/virtual-device-simulator.git
cd virtual-device-simulator

# 安装 Python 主程序依赖（虚拟设备模拟器）
cd core
python3 -m venv .venv
source .venv/bin/activate
mkdir -p /home/ll/HA-VT/core/logs
pip install -r requirements.txt

# 安装 MQTT Broker 与 MongoDB（如果尚未安装）
sudo apt install mosquitto mongodb -y
```

### ✅ 安装后端接口服务（FastAPI）
```bash
cd ../backend
pip install -r requirements.txt
```

### ✅ 安装前端仪表盘
```bash
cd ../frontend
npm install
npm run build
```

---

## 🧪 测试方式

### ✅ 安装测试依赖
```bash
pip install -r requirements-dev.txt
```

### ✅ 运行测试
```bash
cd tests/

# 运行 REST 接口测试
pytest test_api.py

# 运行 WebSocket 推送测试（需运行中后端服务）
pytest test_websocket.py
```

---

## 🚀 启动方式

### ✅ 启动虚拟设备模拟器
```bash
cd core
source .venv/bin/activate
python main.py
```

### ✅ 启动 FastAPI 后端接口服务
```bash
cd backend
uvicorn api:app --reload
```

### ✅ 启动前端开发服务（可选调试）
```bash
cd frontend
npm install vue-router@4
npm run dev
```

---

## 🌐 系统入口说明

- 仪表盘访问地址：`http://localhost:5173`
- 后端接口地址：`http://localhost:8000`
- WebSocket 地址：`ws://localhost:8000/ws/devices`
- 配置文件路径：`core/config.yaml`
- 日志文件路径：`core/logs/simulator.log`

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

# 前端仪表板概览（frontend/）

本目录下为虚拟设备模拟系统的前端界面代码，推荐使用 Vue 3 + TailwindCSS + Pinia + Vite 构建。

## 目录结构建议

```bash
frontend/
├── public/                  # 静态资源
├── src/
│   ├── assets/             # 图标、图片等
│   ├── components/         # 公共组件（卡片、状态块）
│   ├── pages/              # 页面（首页、设备总览、日志）
│   ├── store/              # Pinia 状态管理
│   ├── utils/              # 工具函数与接口封装
│   ├── App.vue
│   ├── main.ts
│   └── router.ts
├── tailwind.config.js
├── index.html
└── vite.config.ts
```

## 功能模块规划

| 页面             | 功能描述                                  |
|------------------|---------------------------------------------|
| 首页 Dashboard    | 展示设备总数、状态概览、连接状态、系统指标 |
| 设备列表页面     | 分类型展示设备状态，支持搜索过滤            |
| 日志页面         | 实时显示运行日志，支持级别筛选              |
| 数据库状态页面   | MongoDB连接状态、写入频率、最新数据预览    |

## 后端接口（示例）

- `GET /api/devices`：返回所有设备状态
- `GET /api/logs`：返回最新日志流
- `GET /api/mongo/stats`：返回数据库连接信息
- 使用 WebSocket 实现状态推送与设备刷新

## 启动方式

```bash
cd frontend
npm install
npm run dev
```

生产构建：
```bash
npm run build
```

## 构建工具
- Vue 3
- TailwindCSS
- Pinia
- Vite
- ECharts（可选，用于图表展示）



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
