import requests
import json

print("=== 测试单层表头和多层表头的行高一致性 ===")

# 测试数据1: 单层表头（字典列表格式）
single_header_data = {
    "单层表头测试": [
        {"姓名": "张三", "部门": "技术部", "工资": 8000},
        {"姓名": "李四", "部门": "销售部", "工资": 7000},
        {"姓名": "王五", "部门": "技术部", "工资": 9000}
    ]
}

# 测试数据2: 多层表头（二维数组格式）
multi_header_data = {
    "多层表头测试": [
        ["", "2025-09-29", "", "2025-09-30"],
        ["", "BROADCAST", "", "OPEN"],
        ["姓名", "数量", "百分比", "数量", "百分比"],
        ["张三", "10", "1.0", "15", "1.0"],
        ["李四", "8", "0.8", "12", "1.0"]
    ]
}

url = "http://localhost:5014/make-xlsx-bytes"

# 生成单层表头Excel
print("1. 生成单层表头Excel...")
try:
    response1 = requests.post(url, json=single_header_data, headers={"Content-Type": "application/json"})
    if response1.status_code == 200:
        with open("single_header_test.xlsx", "wb") as f:
            f.write(response1.content)
        print(f"   [OK] 单层表头Excel生成成功: single_header_test.xlsx ({len(response1.content)} 字节)")
    else:
        print(f"   [ERROR] 单层表头Excel生成失败: {response1.status_code}")
except Exception as e:
    print(f"   [ERROR] 单层表头Excel生成错误: {e}")

# 生成多层表头Excel
print("2. 生成多层表头Excel...")
try:
    response2 = requests.post(url, json=multi_header_data, headers={"Content-Type": "application/json"})
    if response2.status_code == 200:
        with open("multi_header_test.xlsx", "wb") as f:
            f.write(response2.content)
        print(f"   [OK] 多层表头Excel生成成功: multi_header_test.xlsx ({len(response2.content)} 字节)")
    else:
        print(f"   [ERROR] 多层表头Excel生成失败: {response2.status_code}")
except Exception as e:
    print(f"   [ERROR] 多层表头Excel生成错误: {e}")

print("\n=== 行高设置说明 ===")
print("表头行高: 22px（手动设置）")
print("数据行高: 默认行高（Excel自动调整）")
print("现在单层表头和多层表头的数据行都使用默认行高了！")

print("\n请打开生成的Excel文件检查行高是否一致。")
