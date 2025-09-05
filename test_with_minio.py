#!/usr/bin/env python3
"""
使用MinIO测试 /make-xlsx-url 接口
"""

import requests
import json
import os

def test_make_xlsx_url_with_minio():
    """使用MinIO测试生成Excel并返回下载URL"""
    print("=== 使用MinIO测试 /make-xlsx-url 接口 ===")
    
    # 测试数据
    test_data = {
        "财务报表": [
            {"项目": "营业收入", "金额": 1000000, "占比": "100%"},
            {"项目": "营业成本", "金额": 600000, "占比": "60%"},
            {"项目": "毛利润", "金额": 400000, "占比": "40%"}
        ],
        "月度趋势": [
            {"月份": "1月", "收入": 80000, "支出": 60000, "净收入": 20000},
            {"月份": "2月", "收入": 90000, "支出": 65000, "净收入": 25000}
        ]
    }
    
    try:
        print("📤 发送请求...")
        response = requests.post(
            "http://localhost:5000/make-xlsx-url",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📋 响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 成功生成Excel下载URL")
            print(f"📁 文件名: {result.get('filename', 'N/A')}")
            print(f"🔗 下载URL: {result.get('download_url', 'N/A')}")
            print(f"⏰ 过期时间: {result.get('expires_at', 'N/A')}")
            print(f"⏳ 有效期: {result.get('expires_in_hours', 'N/A')} 小时")
            return True
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"📝 错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def main():
    """主函数"""
    print("🚀 使用MinIO测试 JSON to Excel 转换服务")
    print("=" * 50)
    
    # 检查MinIO是否运行
    print("🔍 检查MinIO状态...")
    try:
        response = requests.get("http://localhost:9002/minio/health/live", timeout=5)
        if response.status_code == 200:
            print("✅ MinIO服务正常运行")
        else:
            print(f"⚠️ MinIO响应异常: {response.status_code}")
    except Exception as e:
        print(f"❌ MinIO连接失败: {e}")
        print("💡 请确保MinIO正在运行: docker ps")
        return
    
    # 测试接口
    test_make_xlsx_url_with_minio()
    
    print("\n🎉 测试完成！")
    print("\n💡 提示:")
    print("- MinIO控制台: http://localhost:9003")
    print("- MinIO用户名: minioadmin")
    print("- MinIO密码: minioadmin")

if __name__ == "__main__":
    main()
