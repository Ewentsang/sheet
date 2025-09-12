#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件上传和重命名功能的脚本
"""

import requests
import json
import os

def test_upload_file():
    """测试文件上传和重命名功能"""
    
    # 服务器地址
    base_url = "http://localhost:5000"
    
    print("=== 测试文件上传和重命名功能 ===")
    
    # 测试文件路径（使用项目中现有的文件）
    test_file_path = "beautiful_excel_demo.xlsx"
    new_filename = "新年好"
    
    print(f"测试文件: {test_file_path}")
    print(f"新文件名: {new_filename}")
    print()
    
    # 检查测试文件是否存在
    if not os.path.exists(test_file_path):
        print(f"❌ 测试文件不存在: {test_file_path}")
        return
    
    try:
        # 准备文件上传
        with open(test_file_path, 'rb') as f:
            files = {'file': f}
            data = {'new_filename': new_filename}
            
            # 发送POST请求
            response = requests.post(
                f"{base_url}/copy-file",
                files=files,
                data=data
            )
        
        print(f"HTTP状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("\n✅ 文件上传并重命名成功!")
                print(f"原文件名: {result.get('original_filename')}")
                print(f"新文件名: {result.get('new_filename')}")
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
                print("❌ 文件上传失败")
        else:
            print("❌ 请求失败")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器正在运行")
        print("提示: 运行 python app.py 启动服务器")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")

def test_upload_file_with_extension():
    """测试带扩展名的文件上传"""
    print("\n=== 测试带扩展名的文件上传 ===")
    
    base_url = "http://localhost:5000"
    test_file_path = "simple_beautiful_demo.xlsx"
    new_filename = "新年好.xlsx"  # 明确指定扩展名
    
    print(f"测试文件: {test_file_path}")
    print(f"新文件名: {new_filename}")
    
    if not os.path.exists(test_file_path):
        print(f"❌ 测试文件不存在: {test_file_path}")
        return
    
    try:
        with open(test_file_path, 'rb') as f:
            files = {'file': f}
            data = {'new_filename': new_filename}
            
            response = requests.post(
                f"{base_url}/copy-file",
                files=files,
                data=data
            )
        
        print(f"HTTP状态码: {response.status_code}")
        result = response.json()
        print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200 and result.get('success'):
            print("✅ 带扩展名的文件上传成功!")
            new_file_path = result.get('new_file')
            if os.path.exists(new_file_path):
                print(f"✅ 新文件存在: {new_file_path}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    # 测试不带扩展名的文件名
    test_upload_file()
    
    # 测试带扩展名的文件名
    test_upload_file_with_extension()

