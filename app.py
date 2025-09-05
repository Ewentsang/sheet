from flask import Flask, request, send_file, jsonify
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
import json
import io
import os
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError
import logging
from pathlib import Path
from dotenv import load_dotenv

# 确保加载的是和 app.py 同一目录下的 .env
load_dotenv(dotenv_path=Path(__file__).with_name('.env'))



# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"pong": True})
    
@app.route("/debug/env", methods=["GET"])
def debug_env():
    return jsonify({
        "S3_ENDPOINT_URL": os.getenv("S3_ENDPOINT_URL"),
        "S3_BUCKET": os.getenv("S3_BUCKET"),
        "S3_ACCESS_KEY": "****" if os.getenv("S3_ACCESS_KEY") else None,
        "S3_SECRET_KEY": "****" if os.getenv("S3_SECRET_KEY") else None,
        "S3_REGION": os.getenv("S3_REGION"),
        "URL_EXPIRY_HOURS": os.getenv("URL_EXPIRY_HOURS")
    })

# 配置
S3_BUCKET = os.getenv('S3_BUCKET', 'excel-files')
S3_REGION = os.getenv('S3_REGION', 'us-east-1')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')  # 用于MinIO
URL_EXPIRY_HOURS = int(os.getenv('URL_EXPIRY_HOURS', '24'))

def create_excel_from_json(data):
    """
    从JSON数据创建Excel工作簿
    支持多sheet，每个sheet对应JSON中的一个键
    """
    wb = Workbook()
    
    # 移除默认的Sheet
    wb.remove(wb.active)
    
    if isinstance(data, dict):
        # 如果是字典，每个键创建一个sheet
        for sheet_name, sheet_data in data.items():
            create_sheet(wb, sheet_name, sheet_data)
    elif isinstance(data, list):
        # 如果是列表，创建一个默认sheet
        create_sheet(wb, "Sheet1", data)
    else:
        # 如果是单个值，创建一个默认sheet
        create_sheet(wb, "Sheet1", [{"value": data}])
    
    return wb

def create_sheet(wb, sheet_name, data):
    """创建单个sheet"""
    # 清理sheet名称（Excel sheet名称限制）
    safe_name = sheet_name[:31].replace('/', '_').replace('\\', '_').replace('*', '_').replace('?', '_').replace('[', '_').replace(']', '_')
    
    ws = wb.create_sheet(title=safe_name)
    
    if isinstance(data, list) and len(data) > 0:
        # 如果是列表，第一行作为表头
        if isinstance(data[0], dict):
            headers = list(data[0].keys())
            # 写入表头
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")
            
            # 写入数据
            for row, row_data in enumerate(data, 2):
                for col, header in enumerate(headers, 1):
                    value = row_data.get(header, "")
                    ws.cell(row=row, column=col, value=value)
        else:
            # 如果是简单列表，直接写入
            for row, value in enumerate(data, 1):
                ws.cell(row=row, column=1, value=value)
    elif isinstance(data, dict):
        # 如果是字典，创建键值对格式
        headers = ["Key", "Value"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")
        
        for row, (key, value) in enumerate(data.items(), 2):
            ws.cell(row=row, column=1, value=key)
            ws.cell(row=row, column=2, value=value)
    else:
        # 单个值
        ws.cell(row=1, column=1, value="Value")
        ws.cell(row=2, column=1, value=data)
    
    # 自动调整列宽
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width

def upload_to_s3(excel_bytes, filename):
    """上传Excel文件到S3/MinIO"""
    try:
        if S3_ENDPOINT_URL:
            # MinIO配置
            s3_client = boto3.client(
                's3',
                endpoint_url=S3_ENDPOINT_URL,
                aws_access_key_id=S3_ACCESS_KEY,
                aws_secret_access_key=S3_SECRET_KEY,
                region_name=S3_REGION
            )
        else:
            # AWS S3配置
            s3_client = boto3.client(
                's3',
                aws_access_key_id=S3_ACCESS_KEY,
                aws_secret_access_key=S3_SECRET_KEY,
                region_name=S3_REGION
            )
        
        # 上传文件
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=filename,
            Body=excel_bytes,
            ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        # 生成预签名URL
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': filename},
            ExpiresIn=URL_EXPIRY_HOURS * 3600
        )
        
        return presigned_url
        
    except ClientError as e:
        logger.error(f"S3上传错误: {e}")
        raise Exception(f"S3上传失败: {str(e)}")
    except Exception as e:
        logger.error(f"上传错误: {e}")
        raise Exception(f"上传失败: {str(e)}")

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/make-xlsx-bytes', methods=['POST'])
def make_xlsx_bytes():
    """直接返回Excel二进制文件流"""
    try:
        # 获取JSON数据
        if request.is_json:
            data = request.get_json()
        else:
            # 如果不是JSON，尝试解析表单数据
            data_str = request.form.get('data') or request.data.decode('utf-8')
            data = json.loads(data_str)
        
        # 创建Excel
        wb = create_excel_from_json(data)
        
        # 保存到内存
        excel_buffer = io.BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"excel_{timestamp}.xlsx"
        
        return send_file(
            excel_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except json.JSONDecodeError as e:
        return jsonify({"error": f"JSON解析错误: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"生成Excel错误: {e}")
        return jsonify({"error": f"生成Excel失败: {str(e)}"}), 500

@app.route('/make-xlsx-url', methods=['POST'])
def make_xlsx_url():
    """生成Excel并上传到S3，返回下载URL"""
    try:
        # 获取JSON数据
        if request.is_json:
            data = request.get_json()
        else:
            # 如果不是JSON，尝试解析表单数据
            data_str = request.form.get('data') or request.data.decode('utf-8')
            data = json.loads(data_str)
        
        # 检查S3配置
        if not S3_ACCESS_KEY or not S3_SECRET_KEY:
            return jsonify({"error": "S3配置缺失"}), 500
        
        # 创建Excel
        wb = create_excel_from_json(data)
        
        # 保存到内存
        excel_buffer = io.BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)
        excel_bytes = excel_buffer.getvalue()
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"excel_{timestamp}.xlsx"
        
        # 上传到S3
        download_url = upload_to_s3(excel_bytes, filename)
        
        return jsonify({
            "success": True,
            "download_url": download_url,
            "filename": filename,
            "expires_in_hours": URL_EXPIRY_HOURS,
            "expires_at": (datetime.now() + timedelta(hours=URL_EXPIRY_HOURS)).isoformat()
        })
        
    except json.JSONDecodeError as e:
        return jsonify({"error": f"JSON解析错误: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"生成Excel URL错误: {e}")
        return jsonify({"error": f"生成Excel URL失败: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "接口不存在"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "服务器内部错误"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


