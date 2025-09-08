#!/usr/bin/env python3
"""
测试美观Excel生成效果
"""

import requests
import json

def test_beautiful_excel():
    """测试美观Excel生成"""
    print("=== 测试美观Excel生成 ===")
    
    # 测试数据：包含中英文混合，长文本等
    test_data = {
        "员工信息表": [
            {
                "员工编号": "EMP001", 
                "姓名": "张三", 
                "部门": "技术开发部", 
                "职位": "高级软件工程师", 
                "入职日期": "2023-01-15",
                "薪资": 15000,
                "备注": "负责后端开发，技术能力强，团队协作良好"
            },
            {
                "员工编号": "EMP002", 
                "姓名": "李四", 
                "部门": "产品设计部", 
                "职位": "UI/UX设计师", 
                "入职日期": "2023-03-20",
                "薪资": 12000,
                "备注": "擅长用户界面设计，有丰富的移动端设计经验"
            },
            {
                "员工编号": "EMP003", 
                "姓名": "王五", 
                "部门": "市场营销部", 
                "职位": "市场推广专员", 
                "入职日期": "2023-06-10",
                "薪资": 8000,
                "备注": "负责线上推广活动策划，熟悉社交媒体营销"
            },
            {
                "员工编号": "EMP004", 
                "姓名": "赵六", 
                "部门": "人力资源部", 
                "职位": "HR专员", 
                "入职日期": "2023-02-28",
                "薪资": 9000,
                "备注": "负责招聘和员工关系管理，沟通能力强"
            },
            {
                "员工编号": "EMP005", 
                "姓名": "孙七", 
                "部门": "财务部", 
                "职位": "会计", 
                "入职日期": "2023-04-15",
                "薪资": 10000,
                "备注": "负责公司财务核算和报表编制，工作细致认真"
            }
        ],
        "销售数据": [
            {
                "月份": "2024年1月",
                "产品名称": "智能手机",
                "销售数量": 1500,
                "单价": 2999,
                "总销售额": 4498500,
                "利润率": "25%",
                "销售区域": "华东地区",
                "备注": "春节促销活动效果显著，销量超出预期"
            },
            {
                "月份": "2024年2月",
                "产品名称": "笔记本电脑",
                "销售数量": 800,
                "单价": 5999,
                "总销售额": 4799200,
                "利润率": "30%",
                "销售区域": "华南地区",
                "备注": "商务客户采购增加，企业订单占比提升"
            },
            {
                "月份": "2024年3月",
                "产品名称": "平板电脑",
                "销售数量": 1200,
                "单价": 1999,
                "总销售额": 2398800,
                "利润率": "20%",
                "销售区域": "华北地区",
                "备注": "教育行业采购需求增长，学生群体购买力增强"
            }
        ],
        "项目进度": [
            {
                "项目名称": "电商平台重构项目",
                "项目经理": "张三",
                "开始日期": "2024-01-01",
                "预计完成": "2024-06-30",
                "当前进度": "60%",
                "状态": "进行中",
                "团队成员": "8人",
                "项目描述": "对现有电商平台进行技术架构升级，提升系统性能和用户体验"
            },
            {
                "项目名称": "移动APP开发",
                "项目经理": "李四",
                "开始日期": "2024-02-15",
                "预计完成": "2024-08-15",
                "当前进度": "30%",
                "状态": "进行中",
                "团队成员": "6人",
                "项目描述": "开发公司官方移动应用，支持iOS和Android双平台"
            }
        ]
    }
    
    try:
        print("📤 发送请求生成美观Excel...")
        response = requests.post(
            "http://localhost:5000/make-xlsx-bytes",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            # 保存文件
            filename = "beautiful_excel_demo.xlsx"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            print("✅ 美观Excel生成成功！")
            print(f"📁 文件已保存为: {filename}")
            print(f"📏 文件大小: {len(response.content)} 字节")
            print(f"📋 Content-Type: {response.headers.get('content-type')}")
            
            print("\n🎨 美观效果包括:")
            print("   • 表头：深蓝底 + 白字 + 加粗，行高22")
            print("   • 斑马条纹：内容区隔行底色")
            print("   • 边框与对齐：细边框 + 垂直居中，文本自动换行")
            print("   • 智能列宽：根据中英文宽度估算，8-40字符范围")
            
            return True
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"📝 错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_simple_data():
    """测试简单数据的美观效果"""
    print("\n=== 测试简单数据美观效果 ===")
    
    simple_data = {
        "基本信息": {
            "公司名称": "示例科技有限公司",
            "成立时间": "2020年1月",
            "注册资本": "1000万元",
            "员工人数": "150人",
            "主营业务": "软件开发、技术咨询、系统集成",
            "公司地址": "北京市朝阳区科技园区创新大厦A座1001室",
            "联系电话": "010-12345678",
            "官方网站": "https://www.example.com"
        }
    }
    
    try:
        print("📤 发送简单数据请求...")
        response = requests.post(
            "http://localhost:5000/make-xlsx-bytes",
            json=simple_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            filename = "simple_beautiful_demo.xlsx"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            print("✅ 简单数据美观Excel生成成功！")
            print(f"📁 文件已保存为: {filename}")
            return True
        else:
            print(f"❌ 简单数据测试失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 简单数据测试错误: {e}")
        return False

def main():
    """主函数"""
    print("🎨 美观Excel生成测试")
    print("=" * 50)
    
    # 检查服务状态
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("✅ 服务运行正常")
        else:
            print("❌ 服务异常，请先启动服务")
            return
    except Exception as e:
        print(f"❌ 无法连接到服务: {e}")
        print("💡 请先运行: python app.py")
        return
    
    # 运行测试
    test_beautiful_excel()
    test_simple_data()
    
    print("\n🎉 测试完成！")
    print("\n💡 请打开生成的Excel文件查看美观效果:")
    print("   • beautiful_excel_demo.xlsx - 复杂数据示例")
    print("   • simple_beautiful_demo.xlsx - 简单数据示例")

if __name__ == "__main__":
    main()

