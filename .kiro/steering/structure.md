---
inclusion: always
---

# 项目结构

## 推荐的目录组织

```
project-root/
├── miniprogram/              # 小程序前端 (Taro)
│   ├── src/
│   │   ├── pages/           # 页面组件
│   │   ├── components/      # 通用组件
│   │   ├── services/        # API 服务封装
│   │   ├── utils/           # 工具函数
│   │   ├── types/           # TypeScript 类型定义
│   │   ├── store/           # 状态管理
│   │   ├── assets/          # 静态资源
│   │   ├── app.config.ts    # 应用配置
│   │   └── app.ts           # 应用入口
│   ├── config/              # Taro 配置
│   ├── package.json
│   └── tsconfig.json
│
├── api/                     # Python 后端
│   ├── app/
│   │   ├── models/         # 数据模型
│   │   ├── routes/         # API 路由
│   │   ├── services/       # 业务逻辑
│   │   ├── schemas/        # 数据验证模式
│   │   └── utils/          # 工具函数
│   ├── tests/              # 测试文件
│   ├── main.py             # 应用入口
│   ├── requirements.txt    # Python 依赖
│   └── .env                # 环境变量
│
└── docs/                   # 项目文档
```

## 命名规范

### 前端 (TypeScript/React)

- **文件名**: PascalCase 用于组件 (`UserProfile.tsx`)，camelCase 用于工具 (`apiClient.ts`)
- **组件**: PascalCase (`<UserCard />`)
- **函数/变量**: camelCase (`getUserInfo`)
- **常量**: UPPER_SNAKE_CASE (`API_BASE_URL`)
- **类型/接口**: PascalCase，接口以 `I` 开头 (`IUserInfo`)

### 后端 (Python)

- **文件名**: snake_case (`user_service.py`)
- **类名**: PascalCase (`UserService`)
- **函数/变量**: snake_case (`get_user_info`)
- **常量**: UPPER_SNAKE_CASE (`API_VERSION`)

## 代码组织原则

- 按功能模块组织代码，而非按文件类型
- 每个页面/功能独立目录，包含相关组件、样式、类型
- 共享代码放在 `components/`、`utils/`、`services/` 等公共目录
- API 调用统一封装在 `services/` 层
- 类型定义集中管理或就近放置
