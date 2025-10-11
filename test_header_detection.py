import requests
import json

# 测试数据
raw_data = {
    "result": "[[\"\", \"2025-09-29\", \"\", \"\", \"\", \"\", \"\", \"2025-09-30\", \"\", \"\", \"\", \"\", \"\", \"2025-10-01\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"2025-10-02\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"2025-10-03\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\"], [\"\", \"BROADCAST\", \"\", \"OPEN\", \"\", \"SOLVED\", \"\", \"BROADCAST\", \"\", \"OPEN\", \"\", \"SOLVED\", \"\", \"BROADCAST\", \"\", \"EXPIRED\", \"\", \"OPEN\", \"\", \"SOLVED\", \"\", \"BROADCAST\", \"\", \"EXPIRED\", \"\", \"OPEN\", \"\", \"SOLVED\", \"\", \"BROADCAST\", \"\", \"EXPIRED\", \"\", \"OPEN\", \"\", \"SOLVED\", \"\", \"\", \"\"], [\"agent_name\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"status_num\", \"percentage\", \"sum_status_num\", \"sum_percentage\"], [\"Anisyah Fitri\", \"\", \"\", \"\", \"\", \"11\", \"1\", \"\", \"\", \"\", \"\", \"9\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"15\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"11\", \"1\", \"\", \"\", \"1\", \"0.0556\", \"2\", \"0.1111\", \"15\", \"0.8333\", \"64\", \"5\"], [\"Bittang Julianus\", \"\", \"\", \"\", \"\", \"12\", \"1\", \"\", \"\", \"1\", \"0.2\", \"4\", \"0.8\", \"\", \"\", \"\", \"\", \"\", \"\", \"14\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"10\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"7\", \"1\", \"48\", \"5\"], [\"Lenggo Novelita\", \"\", \"\", \"\", \"\", \"10\", \"1\", \"\", \"\", \"\", \"\", \"9\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"19\", \"2\"], [\"Melfi Juliani\", \"\", \"\", \"\", \"\", \"8\", \"1\", \"\", \"\", \"\", \"\", \"8\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"16\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"10\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"10\", \"1\", \"52\", \"5\"], [\"Melisa Siagian\", \"\", \"\", \"\", \"\", \"8\", \"1\", \"\", \"\", \"\", \"\", \"10\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"12\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"10\", \"1\", \"\", \"\", \"1\", \"0.0769\", \"\", \"\", \"12\", \"0.9231\", \"53\", \"5\"], [\"Mesa Lestari\", \"\", \"\", \"1\", \"0.1\", \"9\", \"0.9\", \"\", \"\", \"\", \"\", \"10\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"16\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"12\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"11\", \"1\", \"59\", \"5\"], [\"Nia Fiscarina\", \"\", \"\", \"\", \"\", \"7\", \"1\", \"\", \"\", \"1\", \"0.1111\", \"8\", \"0.8889\", \"\", \"\", \"1\", \"0.0588\", \"\", \"\", \"16\", \"0.9412\", \"\", \"\", \"\", \"\", \"\", \"\", \"12\", \"1\", \"\", \"\", \"\", \"\", \"1\", \"0.0909\", \"10\", \"0.9091\", \"56\", \"5\"], [\"Poppy Amiralda\", \"\", \"\", \"1\", \"0.0769\", \"12\", \"0.9231\", \"\", \"\", \"1\", \"0.1111\", \"8\", \"0.8889\", \"\", \"\", \"\", \"\", \"\", \"\", \"14\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"13\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"12\", \"1\", \"61\", \"5\"], [\"Utari Diani\", \"\", \"\", \"\", \"\", \"10\", \"1\", \"\", \"\", \"\", \"\", \"10\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"18\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"12\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"9\", \"1\", \"59\", \"5\"], [\"Widia Ayu\", \"\", \"\", \"\", \"\", \"11\", \"1\", \"\", \"\", \"\", \"\", \"9\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"15\", \"1\", \"\", \"\", \"\", \"\", \"\", \"\", \"12\", \"1\", \"\", \"\", \"1\", \"0.0714\", \"\", \"\", \"13\", \"0.9286\", \"61\", \"5\"], [\"(空白)\", \"3347\", \"1\", \"\", \"\", \"\", \"\", \"3554\", \"0.9986\", \"5\", \"0.0014\", \"\", \"\", \"3272\", \"0.9994\", \"\", \"\", \"1\", \"0.0003\", \"1\", \"0.0003\", \"3530\", \"0.9992\", \"2\", \"0.0006\", \"1\", \"0.0003\", \"\", \"\", \"3596\", \"0.9994\", \"1\", \"0.0003\", \"1\", \"0.0003\", \"\", \"\", \"17311\", \"5.0001\"], [\"统计\", \"3347\", \"1\", \"2\", \"0.1769\", \"98\", \"9.8231\", \"3554\", \"0.9986\", \"8\", \"0.4236\", \"85\", \"9.5778\", \"3272\", \"0.9994\", \"1\", \"0.0588\", \"1\", \"0.0003\", \"137\", \"8.9415\", \"3530\", \"0.9992\", \"2\", \"0.0006\", \"1\", \"0.0003\", \"102\", \"9\", \"3596\", \"0.9994\", \"4\", \"0.2042\", \"4\", \"0.2023\", \"99\", \"8.5941\", \"17843\", \"52.0001\"]]"
}

# 解析数据
table_data = json.loads(raw_data["result"])

print("=== 智能表头检测测试 ===")
print(f"总行数: {len(table_data)}")
print()

# 模拟检测逻辑
def analyze_data_pattern(data):
    """分析数据模式"""
    print("第1列数据分析:")
    for i, row in enumerate(data):
        first_cell = row[0] if row and len(row) > 0 else ""
        print(f"  行{i}: '{first_cell}'")
        
        # 检查是否是具体数据
        if first_cell and isinstance(first_cell, str):
            if ('(' in first_cell and ')' in first_cell) or first_cell.lower() in ['统计', 'total', 'sum', '合计']:
                print(f"    -> 检测到具体数据特征，表头应该在行{i}")
                return i
    
    print("\n数值密度分析:")
    for i, row in enumerate(data):
        if not row:
            print(f"  行{i}: 空行")
            continue
        
        numeric_count = 0
        total_count = 0
        for cell in row:
            if cell and str(cell).strip():
                total_count += 1
                cell_str = str(cell).replace('%', '').replace(',', '')
                try:
                    float(cell_str)
                    numeric_count += 1
                except:
                    pass
        
        density = numeric_count / total_count if total_count > 0 else 0
        print(f"  行{i}: 数值密度 {density:.2f} ({numeric_count}/{total_count})")
        
        if i > 0 and density > 0.5:  # 数值密度高，可能是数据行
            print(f"    -> 数值密度高，可能是数据行开始")
            return i
    
    return 3  # 默认前3行

# 分析数据
detected_headers = analyze_data_pattern(table_data)
print(f"\n=== 检测结果 ===")
print(f"检测到的表头行数: {detected_headers}")
print(f"数据开始行: {detected_headers + 1}")
print()

# 显示表头和数据的分界
print("表头部分:")
for i in range(detected_headers):
    print(f"  行{i}: {table_data[i][:5]}...")  # 只显示前5列

print("\n数据部分:")
for i in range(detected_headers, min(detected_headers + 3, len(table_data))):
    print(f"  行{i}: {table_data[i][:5]}...")  # 只显示前5列

# 调用API生成Excel
request_data = {
    "Agent Statistics": table_data
}

url = "http://localhost:5014/make-xlsx-bytes"
print(f"\n正在调用 {url}...")

try:
    response = requests.post(
        url, 
        json=request_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"smart_header_detection_{timestamp}.xlsx"
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"[OK] Excel 文件已生成: {output_file}")
        print(f"  文件大小: {len(response.content)} 字节")
    else:
        print(f"[ERROR] 请求失败: {response.status_code}")
        print(f"  错误信息: {response.text}")
        
except Exception as e:
    print(f"[ERROR] 发生错误: {e}")
