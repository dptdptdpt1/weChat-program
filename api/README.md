# 宝利足球赛事通 API

FastAPI 后端服务

## 功能特性

- ✅ FastAPI 应用入口和基本配置
- ✅ SQLite + SQLAlchemy 数据库连接
- ✅ CORS 中间件支持跨域请求
- ✅ 统一的 API 响应模型
- ✅ 全局错误处理器
- ✅ 自动生成 API 文档 (Swagger)

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境 (可选)
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并根据需要修改配置:

```bash
copy .env.example .env
```

### 3. 启动服务器

```bash
# 开发模式 (自动重载)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 或者直接运行
python main.py
```

服务器将在 http://localhost:8000 启动

### 4. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 端点

### 基础端点

- `GET /` - 欢迎信息
- `GET /api/health` - 健康检查

### 响应格式

所有 API 响应遵循统一格式:

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    // 响应数据
  }
}
```

### 错误响应

```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

## 项目结构

```
api/
├── app/
│   ├── models/          # 数据模型
│   ├── routes/          # API 路由
│   ├── schemas/         # Pydantic 模式
│   ├── services/        # 业务逻辑
│   └── utils/           # 工具函数
│       ├── database.py      # 数据库配置
│       ├── exceptions.py    # 自定义异常
│       └── error_handlers.py # 错误处理器
├── main.py              # 应用入口
├── requirements.txt     # 依赖列表
└── .env.example         # 环境变量示例
```

## 数据库

项目使用 SQLite 作为默认数据库,数据库文件为 `football_events.db`。

数据库会在应用启动时自动初始化。

## 开发

### 添加新的 API 端点

1. 在 `app/routes/` 创建新的路由文件
2. 在 `app/schemas/` 定义请求/响应模式
3. 在 `main.py` 中注册路由

### 添加数据模型

1. 在 `app/models/` 创建模型文件
2. 继承 `Base` 类定义表结构
3. 重启应用自动创建表

## 技术栈

- **FastAPI** - 现代 Web 框架
- **SQLAlchemy** - ORM
- **Pydantic** - 数据验证
- **SQLite** - 数据库
- **Uvicorn** - ASGI 服务器

## 注意事项

- 生产环境需要修改 CORS 配置,限制允许的域名
- 建议使用 PostgreSQL 或 MySQL 替代 SQLite
- 需要配置微信小程序的 AppID 和 AppSecret
