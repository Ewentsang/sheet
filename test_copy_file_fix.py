#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import tempfile

def test_copy_file_api():
    """测试修复后的 copy-file API"""
    
    # 创建一个测试文件
    test_content = "这是一个测试文件内容\nHello World!"
    test_filename = "test_original.txt"
    
    # 创建临时文件
    with open(test_filename, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        # 准备请求数据
        url = "http://localhost:5000/copy-file"
        
        with open(test_filename, 'rb') as f:
            files = {'file': f}
            data = {'new_filename': '新年好.txt'}
            
            print("发送请求到:", url)
            print("文件:", test_filename)
            print("新文件名:", data['new_filename'])
            
            # 发送请求
            response = requests.post(url, files=files, data=data)
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                # 检查是否是文件下载
                content_type = response.headers.get('content-type', '')
                if 'application/octet-stream' in content_type or 'text/plain' in content_type:
                    print("✅ 成功！返回的是文件下载")
                    print(f"文件大小: {len(response.content)} 字节")
                    
                    # 保存下载的文件
                    with open('downloaded_file.txt', 'wb') as f:
                        f.write(response.content)
                    print("文件已保存为: downloaded_file.txt")
                else:
                    print("❌ 返回的不是文件，而是:", response.text)
            else:
                print(f"❌ 请求失败: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器正在运行")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
    finally:
        # 清理测试文件
        if os.path.exists(test_filename):
            os.remove(test_filename)
        if os.path.exists('downloaded_file.txt'):
            os.remove('downloaded_file.txt')

if __name__ == "__main__":
    test_copy_file_api()
