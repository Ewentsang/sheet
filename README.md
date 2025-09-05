# JSON to Excel 转换服务

这是一个可部署的微服务，用于将JSON数据转换为多sheet的Excel文件。支持两种接口：直接返回二进制文件流或上传到S3/MinIO并返回下载URL。

## 功能特性

- 🚀 **快速转换**: 将JSON数据快速转换为Excel文件
- 📊 **多Sheet支持**: 自动创建多个工作表，每个JSON键对应一个sheet
- 🎨 **美观样式**: 自动应用表头样式、列宽调整等
- ☁️ **云存储支持**: 支持AWS S3和MinIO对象存储
- 🔗 **预签名URL**: 生成短期有效的下载链接
- 🐳 **容器化部署**: 支持Docker和Docker Compose部署

## API接口

### 1. POST /make-xlsx-bytes
直接返回Excel二进制文件流，适合直接下载使用。

**请求示例:**
```bash
curl -X POST http://localhost:5000/make-xlsx-bytes \
  -H "Content-Type: application/json" \
  -d '{
    "用户数据": [
      {"姓名": "张三", "年龄": 25, "城市": "北京"},
      {"姓名": "李四", "年龄": 30, "城市": "上海"}
    ],
    "产品信息": [
      {"产品名": "产品A", "价格": 100, "库存": 50},
      {"产品名": "产品B", "价格": 200, "库存": 30}
    ]
  }'
```

**响应:** 直接返回Excel文件流，Content-Type为xlsx

### 2. POST /make-xlsx-url
生成Excel并上传到S3/MinIO，返回短期签名下载URL。

**请求示例:**
```bash
curl -X POST http://localhost:5000/make-xlsx-url \
  -H "Content-Type: application/json" \
  -d '{
    "销售数据": [
      {"日期": "2024-01-01", "销售额": 1000, "利润": 200},
      {"日期": "2024-01-02", "销售额": 1200, "利润": 240}
    ]
  }'
```

**响应:**
```json
{
  "success": true,
  "download_url": "https://...",
  "filename": "excel_20241201_143022.xlsx",
  "expires_in_hours": 24,
  "expires_at": "2024-12-02T14:30:22"
}
```

### 3. GET /health
健康检查接口，用于监控服务状态。

## 支持的JSON格式

### 字典格式（推荐）
```json
{
  "Sheet1名称": [
    {"列1": "值1", "列2": "值2"},
    {"列1": "值3", "列2": "值4"}
  ],
  "Sheet2名称": [
    {"A": 1, "B": 2},
    {"A": 3, "B": 4}
  ]
}
```

### 列表格式
```json
[
  {"姓名": "张三", "年龄": 25},
  {"姓名": "李四", "年龄": 30}
]
```

### 简单值
```json
"简单文本内容"
```

## 部署方式

### 方式1: Docker Compose（推荐）

1. 克隆项目并进入目录
```bash
git clone <repository-url>
cd sheet
```

2. 启动服务
```bash
docker-compose up -d
```

3. 访问服务
- Excel服务: http://localhost:5000
- MinIO控制台: http://localhost:9001 (用户名/密码: minioadmin/minioadmin)

### 方式2: 直接运行

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 设置环境变量
```bash
cp env.example .env
# 编辑.env文件，填入你的配置
```

3. 运行服务
```bash
python app.py
```

### 方式3: Docker镜像

1. 构建镜像
```bash
docker build -t excel-service .
```

2. 运行容器
```bash
docker run -p 5000:5000 \
  -e S3_BUCKET=your-bucket \
  -e S3_ACCESS_KEY=your-key \
  -e S3_SECRET_KEY=your-secret \
  excel-service
```

## 环境变量配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `S3_BUCKET` | S3存储桶名称 | `excel-files` |
| `S3_REGION` | S3区域 | `us-east-1` |
| `S3_ACCESS_KEY` | S3访问密钥 | 必需 |
| `S3_SECRET_KEY` | S3秘密密钥 | 必需 |
| `S3_ENDPOINT_URL` | MinIO端点URL | 可选 |
| `URL_EXPIRY_HOURS` | URL过期时间（小时） | `24` |
| `PORT` | 服务端口 | `5000` |

## 在Dify中使用

在Dify的HTTP节点中调用此服务：

### 节点1: 生成Excel
- **URL**: `http://your-service:5000/make-xlsx-url`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**: 你的JSON数据

### 节点2: 处理响应
- 从响应中提取 `download_url`
- 可以发送给用户或进行后续处理

## 性能优化

- 使用Gunicorn多进程部署
- 支持大文件处理（内存优化）
- 自动列宽调整
- 异步S3上传（可扩展）

## 监控和日志

- 健康检查端点: `/health`
- 结构化日志记录
- 错误处理和状态码
- 支持Prometheus指标（可扩展）

## 故障排除

### 常见问题

1. **S3连接失败**
   - 检查网络连接和防火墙设置
   - 验证访问密钥和权限
   - 确认存储桶存在

2. **内存不足**
   - 减少并发请求数量
   - 增加服务器内存
   - 优化JSON数据结构

3. **文件上传失败**
   - 检查MinIO服务状态
   - 验证存储桶权限
   - 查看服务日志

### 日志查看

```bash
# Docker Compose
docker-compose logs excel-service

# 直接运行
tail -f app.log
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
