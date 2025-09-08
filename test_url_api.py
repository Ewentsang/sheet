#!/usr/bin/env python3
"""
测试 /make-xlsx-url 接口
"""

import requests
import json

def test_make_xlsx_url():
    """测试生成Excel并返回下载URL"""
    print("=== 测试 /make-xlsx-url 接口 ===")
    
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
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误，请确保服务正在运行")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def test_make_xlsx_bytes():
    """测试直接返回Excel二进制文件"""
    print("\n=== 测试 /make-xlsx-bytes 接口 ===")
    
    # 测试数据
    test_data = {
        "用户信息": [
            {"姓名": "张三", "年龄": 25, "城市": "北京"},
            {"姓名": "李四", "年龄": 30, "城市": "上海"}
        ]
    }
    
    try:
        print("📤 发送请求...")
        response = requests.post(
            "http://localhost:5000/make-xlsx-bytes",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📋 Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            print("✅ 成功生成Excel文件")
            print(f"📁 文件大小: {len(response.content)} 字节")
            
            # 保存文件
            filename = "test_output.xlsx"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"💾 文件已保存为: {filename}")
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
    print("🚀 JSON to Excel 转换服务测试")
    print("=" * 50)
    
    # 测试健康检查
    print("=== 测试健康检查 ===")
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("✅ 服务健康检查通过")
            print(f"📊 响应: {response.json()}")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return
    
    # 测试两个接口
    test_make_xlsx_bytes()
    test_make_xlsx_url()
    
    print("\n🎉 测试完成！")
    print("\n💡 提示:")
    print("- 如果 /make-xlsx-url 失败，可能是因为没有配置S3/MinIO")
    print("- 可以检查生成的 test_output.xlsx 文件")
    print("- 查看服务日志了解详细错误信息")

if __name__ == "__main__":
    main()

