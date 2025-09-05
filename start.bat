@echo off
echo ========================================
echo    JSON to Excel 转换服务启动脚本
echo ========================================
echo.

echo 正在检查Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未检测到Docker，请先安装Docker Desktop
    pause
    exit /b 1
)

echo ✅ Docker已安装
echo.

echo 正在启动服务...
docker-compose up -d

if errorlevel 1 (
    echo ❌ 启动失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo ✅ 服务启动成功！
echo.
echo 📊 Excel服务: http://localhost:5000
echo 🖥️  MinIO控制台: http://localhost:9001
echo 👤 MinIO用户名: minioadmin
echo 🔑 MinIO密码: minioadmin
echo.
echo 💡 提示:
echo - 运行 test_example.py 来测试服务
echo - 使用 docker-compose logs 查看日志
echo - 使用 docker-compose down 停止服务
echo.
pause
