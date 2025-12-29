---
inclusion: always
---

# 技术栈

## 前端技术栈

- **框架**: Taro 3.x (React 模式)
- **语言**: TypeScript
- **UI 组件库**: Taro UI / NutUI (推荐)
- **状态管理**: Redux / Zustand (按需选择)
- **HTTP 客户端**: Taro.request
- **构建工具**: Webpack (Taro 内置)

## 后端技术栈

- **语言**: Python 3.9+
- **Web 框架**: FastAPI (推荐) 或 Flask
- **数据库**: PostgreSQL / MySQL / MongoDB (按需选择)
- **ORM**: SQLAlchemy / Tortoise ORM
- **API 文档**: FastAPI 自动生成 Swagger 文档

## 常用命令

### 前端命令 (小程序目录)

```bash
# 安装依赖
npm install

# 微信小程序开发模式
npm run dev:weapp

# 构建生产版本
npm run build:weapp

# 类型检查
npm run type-check

# 代码格式化
npm run lint
```

### 后端命令 (API 目录)

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器 (FastAPI)
uvicorn main:app --reload

# 启动开发服务器 (Flask)
python app.py

# 运行测试
pytest
```

## 开发工具

- **前端**: 微信开发者工具 + VS Code
- **后端**: VS Code / PyCharm
- **API 测试**: Postman / Apifox
- **版本控制**: Git
