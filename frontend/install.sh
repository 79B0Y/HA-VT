# frontend/install.sh

#!/bin/bash

set -e

echo "📦 安装前端依赖..."
cd frontend

if ! command -v npm &> /dev/null; then
  echo "❌ 未检测到 npm，请先安装 Node.js 和 npm"
  exit 1
fi

npm install
npm run build

echo "✅ 前端构建完成，生成在 frontend/dist/"
