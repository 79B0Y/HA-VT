#!/bin/bash
set -e

# 自动安装虚拟设备模拟系统（包含核心、后端与前端）

ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT_DIR"

echo "🔧 安装系统依赖..."
sudo apt-get update
# 安装 MongoDB、Mosquitto、Node.js 及 npm，如果尚未安装
sudo apt-get install -y mosquitto-clients nodejs npm python3-venv

# 安装核心程序并配置 systemd 服务
cd core
./install.sh

# 使用核心虚拟环境安装后端依赖
source .venv/bin/activate
cd ../backend
pip install -r requirements.txt

# 安装并构建前端
cd ../frontend
npm install
npm run build

deactivate

cd "$ROOT_DIR"
echo "✅ 所有组件安装完成"
