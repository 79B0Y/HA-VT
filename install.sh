#!/bin/bash

set -e

echo "🔧 开始安装虚拟设备模拟系统..."

# 检查并安装 MongoDB
if ! command -v mongod &> /dev/null; then
    echo "⚠️ 未检测到 MongoDB，正在安装..."
    sudo apt-get update
    sudo apt-get install -y mongodb
else
    echo "✅ MongoDB 已安装"
fi

# 检查并安装 Mosquitto MQTT Broker
if ! command -v mosquitto &> /dev/null; then
    echo "⚠️ 未检测到 mosquitto，正在安装..."
    sudo apt-get update
    sudo apt-get install -y mosquitto mosquitto-clients
else
    echo "✅ Mosquitto 已安装"
fi

# 设置 Python 虚拟环境
echo "📦 设置 Python 虚拟环境..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 创建日志目录
mkdir -p logs

# 创建 systemd 服务
SERVICE_PATH="/etc/systemd/system/virtual-device-simulator.service"
echo "📋 创建 Systemd 服务文件: $SERVICE_PATH"
sudo tee $SERVICE_PATH > /dev/null <<EOF
[Unit]
Description=Virtual Device Simulator
After=network.target

[Service]
Type=simple
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/.venv/bin/python main.py
Restart=always
StandardOutput=append:$(pwd)/logs/stdout.log
StandardError=append:$(pwd)/logs/stderr.log

[Install]
WantedBy=multi-user.target
EOF

# 启用并启动服务
echo "🚀 启用并启动 virtual-device-simulator.service"
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable virtual-device-simulator.service
sudo systemctl restart virtual-device-simulator.service

# 完成提示
echo "✅ 安装完成并设置开机启动，可使用以下命令查看状态："
echo "  sudo systemctl status virtual-device-simulator.service"
