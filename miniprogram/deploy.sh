#!/bin/bash

# 微信小程序快速部署脚本

echo "======================================"
echo "  宝利足球赛事通 - 小程序部署脚本"
echo "======================================"
echo ""

# 检查是否在 miniprogram 目录
if [ ! -f "package.json" ]; then
    echo "❌ 错误：请在 miniprogram 目录下运行此脚本"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误：未安装 Node.js"
    echo "请访问 https://nodejs.org/ 下载安装"
    exit 1
fi

# 检查 pnpm
if ! command -v pnpm &> /dev/null; then
    echo "⚠️  警告：未安装 pnpm，将使用 npm"
    PKG_MANAGER="npm"
else
    PKG_MANAGER="pnpm"
fi

echo "📦 使用包管理器: $PKG_MANAGER"
echo ""

# 询问是否需要安装依赖
read -p "是否需要安装/更新依赖？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📥 正在安装依赖..."
    $PKG_MANAGER install
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖安装完成"
    echo ""
fi

# 询问 API 地址
echo "🔧 配置 API 地址"
echo "当前配置请查看: src/utils/request.ts"
read -p "是否需要修改 API 地址？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "请输入生产环境 API 地址 (如 https://api.example.com): " API_URL
    if [ ! -z "$API_URL" ]; then
        # 使用 sed 修改 API_BASE_URL
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s|const API_BASE_URL = .*|const API_BASE_URL = '$API_URL'|" src/utils/request.ts
        else
            # Linux
            sed -i "s|const API_BASE_URL = .*|const API_BASE_URL = '$API_URL'|" src/utils/request.ts
        fi
        echo "✅ API 地址已更新为: $API_URL"
    fi
    echo ""
fi

# 清理旧的构建文件
echo "🧹 清理旧的构建文件..."
rm -rf dist
echo "✅ 清理完成"
echo ""

# 构建生产版本
echo "🔨 开始构建生产版本..."
$PKG_MANAGER run build:weapp

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 构建失败！"
    echo "请检查错误信息并修复后重试"
    exit 1
fi

echo ""
echo "======================================"
echo "  ✅ 构建成功！"
echo "======================================"
echo ""
echo "📁 构建文件位置: $(pwd)/dist"
echo ""
echo "📱 下一步操作："
echo "1. 打开微信开发者工具"
echo "2. 导入项目，选择 dist 目录"
echo "3. 填入你的小程序 AppID"
echo "4. 预览测试功能是否正常"
echo "5. 点击上传按钮上传代码"
echo "6. 在微信公众平台提交审核"
echo ""
echo "📖 详细部署指南请查看: DEPLOYMENT.md"
echo ""
