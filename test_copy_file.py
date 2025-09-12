#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件复制功能的脚本
"""

import requests
import json
import os

def test_copy_file_function():
    """测试文件复制功能"""
    
    # 测试数据
    test_data = {
        "source_file_path": "beautiful_excel_demo.xlsx",  # 使用项目中现有的文件
        "new_filename": "copied_file.xlsx"
    }
    
    # 服务器地址
    base_url = "http://localhost:5000"
    
    print("=== 测试文件复制功能 ===")
    print(f"源文件: {test_data['source_file_path']}")
    print(f"新文件名: {test_data['new_filename']}")
    print()
    
    try:
        # 发送POST请求
        response = requests.post(
            f"{base_url}/copy-file",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"HTTP状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("\n✅ 文件复制成功!")
                print(f"新文件路径: {result.get('new_file')}")
                
                # 检查文件是否真的存在
                new_file_path = result.get('new_file')
                if os.path.exists(new_file_path):
                    print(f"✅ 新文件确实存在: {new_file_path}")
                    file_size = os.path.getsize(new_file_path)
                    print(f"文件大小: {file_size} 字节")
                else:
                    print(f"❌ 新文件不存在: {new_file_path}")
            else:
                print("❌ 文件复制失败")
        else:
            print("❌ 请求失败")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器正在运行")
        print("提示: 运行 python app.py 启动服务器")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")

def test_copy_file_function_direct():
    """直接测试文件复制函数（不通过HTTP）"""
    print("\n=== 直接测试文件复制函数 ===")
    
    try:
        # 导入函数
        from app import copy_file_with_new_name
        
        # 测试参数
        source_file = "beautiful_excel_demo.xlsx"
        new_filename = "direct_copy_test.xlsx"
        
        print(f"源文件: {source_file}")
        print(f"新文件名: {new_filename}")
        
        # 检查源文件是否存在
        if not os.path.exists(source_file):
            print(f"❌ 源文件不存在: {source_file}")
            return
        
        # 调用函数
        new_file_path = copy_file_with_new_name(source_file, new_filename)
        
        print(f"✅ 文件复制成功!")
        print(f"新文件路径: {new_file_path}")
        
        # 验证文件
        if os.path.exists(new_file_path):
            print(f"✅ 新文件确实存在")
            file_size = os.path.getsize(new_file_path)
            print(f"文件大小: {file_size} 字节")
        else:
            print(f"❌ 新文件不存在")
            
    except Exception as e:
        print(f"❌ 直接测试失败: {e}")

if __name__ == "__main__":
    # 先测试直接函数调用
    test_copy_file_function_direct()
    
    # 再测试HTTP API
    test_copy_file_function()

