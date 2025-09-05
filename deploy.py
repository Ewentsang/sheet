#!/usr/bin/env python3
"""
生产环境部署脚本
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def run_command(command, description):
    """运行命令并处理错误"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败:")
        print(f"   错误代码: {e.returncode}")
        print(f"   错误输出: {e.stderr}")
        return False

def check_docker():
    """检查Docker环境"""
    print("🔍 检查Docker环境...")
    
    if not run_command("docker --version", "检查Docker版本"):
        return False
    
    if not run_command("docker-compose --version", "检查Docker Compose版本"):
        return False
    
    return True

def build_image():
    """构建Docker镜像"""
    print("🔨 构建Docker镜像...")
    
    # 检查是否存在.env文件
    if not Path(".env").exists():
        print("⚠️  警告: 未找到.env文件，将使用默认配置")
        print("   建议复制env.example为.env并配置生产环境参数")
    
    return run_command("docker build -t excel-service:latest .", "构建镜像")

def deploy_services():
    """部署服务"""
    print("🚀 部署服务...")
    
    # 停止现有服务
    run_command("docker-compose down", "停止现有服务")
    
    # 启动服务
    if not run_command("docker-compose up -d", "启动服务"):
        return False
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    import time
    time.sleep(10)
    
    # 检查服务状态
    if not run_command("docker-compose ps", "检查服务状态"):
        return False
    
    return True

def check_health():
    """检查服务健康状态"""
    print("🏥 检查服务健康状态...")
    
    try:
        import requests
        response = requests.get("http://localhost:5000/health", timeout=10)
        if response.status_code == 200:
            print("✅ 服务健康检查通过")
            return True
        else:
            print(f"❌ 服务健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 服务健康检查失败: {e}")
        return False

def show_status():
    """显示服务状态"""
    print("\n" + "="*50)
    print("🎉 部署完成！")
    print("="*50)
    print()
    print("📊 服务信息:")
    print("   Excel服务: http://localhost:5000")
    print("   MinIO控制台: http://localhost:9001")
    print("   MinIO用户名: minioadmin")
    print("   MinIO密码: minioadmin")
    print()
    print("🔧 管理命令:")
    print("   查看日志: docker-compose logs")
    print("   停止服务: docker-compose down")
    print("   重启服务: docker-compose restart")
    print()
    print("🧪 测试服务:")
    print("   python test_example.py")
    print()

def main():
    """主函数"""
    print("🚀 JSON to Excel 转换服务部署脚本")
    print("="*50)
    print()
    
    # 检查Docker环境
    if not check_docker():
        print("❌ Docker环境检查失败，请先安装Docker和Docker Compose")
        sys.exit(1)
    
    # 构建镜像
    if not build_image():
        print("❌ 镜像构建失败")
        sys.exit(1)
    
    # 部署服务
    if not deploy_services():
        print("❌ 服务部署失败")
        sys.exit(1)
    
    # 检查健康状态
    if not check_health():
        print("❌ 服务健康检查失败")
        sys.exit(1)
    
    # 显示状态
    show_status()

if __name__ == "__main__":
    main()
