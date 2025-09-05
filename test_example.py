#!/usr/bin/env python3
"""
测试示例：展示如何使用JSON to Excel转换服务
"""

import requests
import json

# 服务地址
BASE_URL = "http://localhost:5000"

def test_health():
    """测试健康检查"""
    print("=== 测试健康检查 ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"错误: {e}")
    print()

def test_make_xlsx_bytes():
    """测试直接返回Excel二进制文件"""
    print("=== 测试直接返回Excel文件 ===")
    
    # 测试数据
    test_data = {
        "用户信息": [
            {"姓名": "张三", "年龄": 25, "城市": "北京", "职业": "工程师"},
            {"姓名": "李四", "年龄": 30, "城市": "上海", "职业": "设计师"},
            {"姓名": "王五", "年龄": 28, "城市": "深圳", "职业": "产品经理"}
        ],
        "销售数据": [
            {"月份": "1月", "销售额": 10000, "利润": 2000, "增长率": "15%"},
            {"月份": "2月", "销售额": 12000, "利润": 2400, "增长率": "20%"},
            {"月份": "3月", "销售额": 15000, "利润": 3000, "增长率": "25%"}
        ],
        "产品列表": [
            {"产品名": "产品A", "价格": 100, "库存": 50, "状态": "在售"},
            {"产品名": "产品B", "价格": 200, "库存": 30, "状态": "在售"},
            {"产品名": "产品C", "价格": 150, "库存": 0, "状态": "缺货"}
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/make-xlsx-bytes",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            # 保存文件
            filename = "test_output.xlsx"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Excel文件已保存为: {filename}")
            print(f"文件大小: {len(response.content)} 字节")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
    print()

def test_make_xlsx_url():
    """测试生成Excel并返回下载URL"""
    print("=== 测试生成Excel下载URL ===")
    
    # 测试数据
    test_data = {
        "财务报表": [
            {"项目": "营业收入", "金额": 1000000, "占比": "100%"},
            {"项目": "营业成本", "金额": 600000, "占比": "60%"},
            {"项目": "毛利润", "金额": 400000, "占比": "40%"},
            {"项目": "运营费用", "金额": 200000, "占比": "20%"},
            {"项目": "净利润", "金额": 200000, "占比": "20%"}
        ],
        "月度趋势": [
            {"月份": "1月", "收入": 80000, "支出": 60000, "净收入": 20000},
            {"月份": "2月", "收入": 90000, "支出": 65000, "净收入": 25000},
            {"月份": "3月", "收入": 100000, "支出": 70000, "净收入": 30000}
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/make-xlsx-url",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 成功生成Excel下载URL")
            print(f"文件名: {result['filename']}")
            print(f"下载URL: {result['download_url']}")
            print(f"过期时间: {result['expires_at']}")
            print(f"有效期: {result['expires_in_hours']} 小时")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
    print()

def test_different_formats():
    """测试不同的JSON格式"""
    print("=== 测试不同JSON格式 ===")
    
    # 测试1: 简单列表
    print("测试1: 简单列表格式")
    simple_list = ["苹果", "香蕉", "橙子", "葡萄"]
    try:
        response = requests.post(
            f"{BASE_URL}/make-xlsx-bytes",
            json=simple_list,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ 简单列表格式测试成功")
        else:
            print(f"❌ 简单列表格式测试失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    # 测试2: 嵌套字典
    print("测试2: 嵌套字典格式")
    nested_dict = {
        "基本信息": {"公司名": "示例公司", "成立时间": "2020年", "员工数": 100},
        "联系方式": {"电话": "010-12345678", "邮箱": "info@example.com", "地址": "北京市朝阳区"}
    }
    try:
        response = requests.post(
            f"{BASE_URL}/make-xlsx-bytes",
            json=nested_dict,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ 嵌套字典格式测试成功")
        else:
            print(f"❌ 嵌套字典格式测试失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print()

def main():
    """主函数"""
    print("🚀 JSON to Excel 转换服务测试")
    print("=" * 50)
    
    # 运行所有测试
    test_health()
    test_make_xlsx_bytes()
    test_make_xlsx_url()
    test_different_formats()
    
    print("🎉 测试完成！")
    print("\n💡 提示:")
    print("1. 确保服务正在运行 (docker-compose up -d)")
    print("2. 检查生成的Excel文件")
    print("3. 如果使用URL接口，确保S3/MinIO配置正确")

if __name__ == "__main__":
    main()
