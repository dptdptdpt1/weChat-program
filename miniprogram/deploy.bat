@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 微信小程序快速部署脚本 (Windows)

echo ======================================
echo   宝利足球赛事通 - 小程序部署脚本
echo ======================================
echo.

REM 检查是否在 miniprogram 目录
if not exist "package.json" (
    echo ❌ 错误：请在 miniprogram 目录下运行此脚本
    pause
    exit /b 1
)

REM 检查 Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 错误：未安装 Node.js
    echo 请访问 https://nodejs.org/ 下载安装
    pause
    exit /b 1
)

REM 检查 pnpm
where pnpm >nul 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  警告：未安装 pnpm，将使用 npm
    set PKG_MANAGER=npm
) else (
    set PKG_MANAGER=pnpm
)

echo 📦 使用包管理器: %PKG_MANAGER%
echo.

REM 询问是否需要安装依赖
set /p INSTALL_DEPS="是否需要安装/更新依赖？(y/n) "
if /i "%INSTALL_DEPS%"=="y" (
    echo 📥 正在安装依赖...
    call %PKG_MANAGER% install
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
    echo.
)

REM 询问 API 地址
echo 🔧 配置 API 地址
echo 当前配置请查看: src\utils\request.ts
set /p CHANGE_API="是否需要修改 API 地址？(y/n) "
if /i "%CHANGE_API%"=="y" (
    set /p API_URL="请输入生产环境 API 地址 (如 https://api.example.com): "
    if not "!API_URL!"=="" (
        echo ℹ️  请手动修改 src\utils\request.ts 中的 API_BASE_URL
        echo    修改为: const API_BASE_URL = '!API_URL!'
        pause
    )
    echo.
)

REM 清理旧的构建文件
echo 🧹 清理旧的构建文件...
if exist "dist" (
    rmdir /s /q dist
)
echo ✅ 清理完成
echo.

REM 构建生产版本
echo 🔨 开始构建生产版本...
call %PKG_MANAGER% run build:weapp

if %errorlevel% neq 0 (
    echo.
    echo ❌ 构建失败！
    echo 请检查错误信息并修复后重试
    pause
    exit /b 1
)

echo.
echo ======================================
echo   ✅ 构建成功！
echo ======================================
echo.
echo 📁 构建文件位置: %cd%\dist
echo.
echo 📱 下一步操作：
echo 1. 打开微信开发者工具
echo 2. 导入项目，选择 dist 目录
echo 3. 填入你的小程序 AppID
echo 4. 预览测试功能是否正常
echo 5. 点击上传按钮上传代码
echo 6. 在微信公众平台提交审核
echo.
echo 📖 详细部署指南请查看: DEPLOYMENT.md
echo.
pause
