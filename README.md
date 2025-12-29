# 微信小程序项目

Taro + React + TypeScript + FastAPI 全栈项目

## 项目结构

```
├── miniprogram/    # 小程序前端 (Taro)
└── api/           # 后端 API (FastAPI)
```

## 快速开始

### 前端开发

```bash
cd miniprogram
npm install
npm run dev:weapp
```

然后使用微信开发者工具打开 `miniprogram` 目录。

### 后端开发

```bash
cd api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python main.py
```

API 文档: http://localhost:8000/docs

## 技术栈

- **前端**: Taro 3.x + React + TypeScript
- **后端**: FastAPI + Python 3.9+
- **开发工具**: 微信开发者工具 + VS Code

## 开发规范

详见 `.kiro/steering/` 目录下的文档。
