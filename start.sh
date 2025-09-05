#!/bin/bash

echo "========================================"
echo "   JSON to Excel 转换服务启动脚本"
echo "========================================"
echo

echo "正在检查Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未检测到Docker，请先安装Docker"
    exit 1
fi

echo "✅ Docker已安装"
echo

echo "正在检查Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    echo "❌ 错误: 未检测到Docker Compose，请先安装Docker Compose"
    exit 1
fi

echo "✅ Docker Compose已安装"
echo

echo "正在启动服务..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ 启动失败，请检查错误信息"
    exit 1
fi

echo
echo "✅ 服务启动成功！"
echo
echo "📊 Excel服务: http://localhost:5000"
echo "🖥️  MinIO控制台: http://localhost:9001"
echo "👤 MinIO用户名: minioadmin"
echo "🔑 MinIO密码: minioadmin"
echo
echo "💡 提示:"
echo "- 运行 python test_example.py 来测试服务"
echo "- 使用 docker-compose logs 查看日志"
echo "- 使用 docker-compose down 停止服务"
echo
