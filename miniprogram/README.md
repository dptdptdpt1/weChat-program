# 宝利足球赛事通小程序

基于 Taro + React + TypeScript 开发的微信小程序。

## 项目结构

```
src/
├── pages/              # 页面
│   ├── index/         # 首页
│   ├── proposal/      # 今日方案
│   ├── profile/       # 个人中心
│   └── event-detail/  # 赛事详情
├── components/        # 通用组件
├── services/          # API 服务
├── types/             # TypeScript 类型定义
├── utils/             # 工具函数
├── assets/            # 静态资源
│   └── icons/        # 图标文件
├── app.config.ts      # 应用配置
├── app.scss           # 全局样式
└── app.ts             # 应用入口
```

## 开发命令

```bash
# 安装依赖
npm install

# 微信小程序开发模式
npm run dev:weapp

# 构建生产版本
npm run build:weapp

# 类型检查
npm run type-check
```

## 开发说明

### 页面说明

1. **首页 (index)**: 展示赛事列表,支持下拉刷新
2. **今日方案 (proposal)**: 展示赛事列表,支持搜索
3. **个人中心 (profile)**: 用户信息和客服入口
4. **赛事详情 (event-detail)**: 展示赛事详细信息

### TabBar 图标

需要准备以下图标文件(81px * 81px PNG):
- home.png / home-active.png
- proposal.png / proposal-active.png  
- profile.png / profile-active.png

图标文件放置在 `src/assets/icons/` 目录下。

### API 配置

后端 API 地址配置在 `config/` 目录:
- `config/dev.ts` - 开发环境
- `config/prod.ts` - 生产环境

## 注意事项

1. 使用微信开发者工具打开项目根目录
2. 需要配置小程序 AppID
3. 确保后端 API 服务已启动
4. 开发时使用开发环境 API 地址
