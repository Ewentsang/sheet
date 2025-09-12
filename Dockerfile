FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖（包括curl用于健康检查）
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录并设置权限
RUN mkdir -p temp_uploads && chown -R app:app /app

# 切换到非root用户
USER app

# 暴露端口
EXPOSE 5014

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5014/health || exit 1

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5014", "--workers", "4", "--timeout", "120", "app:app"]
