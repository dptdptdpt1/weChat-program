# Design Document: 宝利足球赛事通小程序

## Overview

宝利足球赛事通是一个基于 Taro + React + TypeScript 开发的微信小程序，后端使用 FastAPI (Python) 提供 RESTful API 服务。系统采用前后端分离架构，专注于足球赛事信息的展示和浏览功能。

**核心特性：**
- 简洁的赛事列表和详情展示
- 实时搜索功能
- 微信授权登录
- 客服二维码支持
- 响应式图片加载

## Architecture

### 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                    微信小程序前端                          │
│                  (Taro + React + TS)                    │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │   首页    │  │ 今日方案  │  │   我的    │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│                                                         │
│  ┌─────────────────────────────────────────┐           │
│  │         API Client (Taro.request)        │           │
│  └─────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────┘
                         │
                         │ HTTPS/JSON
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   后端 API 服务器                         │
│                    (FastAPI + Python)                   │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │  API Routes  │  │   Services   │                   │
│  └──────────────┘  └──────────────┘                   │
│          │                 │                           │
│          └────────┬────────┘                           │
│                   ▼                                    │
│          ┌──────────────┐                             │
│          │   Database   │                             │
│          │  (SQLite)    │                             │
│          └──────────────┘                             │
└─────────────────────────────────────────────────────────┘
```

### 技术栈

**前端：**
- Taro 3.x (React 模式)
- TypeScript
- Taro UI / NutUI (UI 组件库)
- Taro.request (HTTP 客户端)

**后端：**
- Python 3.9+
- FastAPI (Web 框架)
- SQLAlchemy (ORM)
- SQLite (数据库)
- Pydantic (数据验证)

## Components and Interfaces

### 前端组件结构

```
miniprogram/src/
├── pages/
│   ├── index/              # 首页
│   │   ├── index.tsx
│   │   ├── index.scss
│   │   └── index.config.ts
│   ├── proposal/           # 今日方案页
│   │   ├── index.tsx
│   │   ├── index.scss
│   │   └── index.config.ts
│   ├── profile/            # 我的页面
│   │   ├── index.tsx
│   │   ├── index.scss
│   │   └── index.config.ts
│   └── event-detail/       # 赛事详情页
│       ├── index.tsx
│       ├── index.scss
│       └── index.config.ts
├── components/
│   ├── EventCard/          # 赛事卡片组件
│   │   ├── index.tsx
│   │   └── index.scss
│   ├── SearchBar/          # 搜索栏组件
│   │   ├── index.tsx
│   │   └── index.scss
│   └── QRCodeModal/        # 二维码弹窗组件
│       ├── index.tsx
│       └── index.scss
├── services/
│   ├── apiClient.ts        # API 客户端封装
│   ├── eventService.ts     # 赛事服务
│   └── authService.ts      # 认证服务
├── types/
│   └── index.ts            # TypeScript 类型定义
├── utils/
│   ├── request.ts          # 请求工具
│   └── storage.ts          # 存储工具
└── app.config.ts           # 应用配置
```

### 后端模块结构

```
api/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── event.py        # 赛事模型
│   │   └── user.py         # 用户模型
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── events.py       # 赛事路由
│   │   └── auth.py         # 认证路由
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── event.py        # 赛事数据模式
│   │   └── user.py         # 用户数据模式
│   ├── services/
│   │   ├── __init__.py
│   │   ├── event_service.py    # 赛事业务逻辑
│   │   └── auth_service.py     # 认证业务逻辑
│   └── utils/
│       ├── __init__.py
│       ├── database.py     # 数据库连接
│       └── wechat.py       # 微信 API 工具
├── main.py                 # 应用入口
└── requirements.txt        # 依赖列表
```

### 核心接口定义

#### 前端 TypeScript 类型

```typescript
// types/index.ts

// 赛事信息
interface IEvent {
  id: number;
  title: string;
  date: string;
  imageUrl: string;
  thumbnailUrl: string;
  viewCount: number;
  createdAt: string;
}

// 用户信息
interface IUserInfo {
  openId: string;
  nickName: string;
  avatarUrl: string;
}

// API 响应
interface IApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

// 分页响应
interface IPaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}
```

#### 后端 API 端点

**赛事相关：**
- `GET /api/events` - 获取赛事列表（支持分页和搜索）
- `GET /api/events/{id}` - 获取赛事详情
- `POST /api/events/{id}/view` - 增加浏览量

**认证相关：**
- `POST /api/auth/login` - 微信登录（使用 code 换取 openid）
- `GET /api/auth/user` - 获取用户信息

**系统相关：**
- `GET /api/config/customer-service` - 获取客服配置（二维码 URL、在线时间）

## Data Models

### 数据库模型

#### Event (赛事表)

```python
class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    date = Column(Date, nullable=False)
    image_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### User (用户表)

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    open_id = Column(String(100), unique=True, nullable=False, index=True)
    nick_name = Column(String(100))
    avatar_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, default=datetime.utcnow)
```

#### CustomerService (客服配置表)

```python
class CustomerService(Base):
    __tablename__ = "customer_service"
    
    id = Column(Integer, primary_key=True)
    qr_code_url = Column(String(500), nullable=False)
    online_time = Column(String(100), default="10:00-23:00")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Pydantic 数据模式

```python
# schemas/event.py

class EventBase(BaseModel):
    title: str
    date: date
    image_url: str
    thumbnail_url: str

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    view_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class EventListResponse(BaseModel):
    items: List[EventResponse]
    total: int
    page: int
    page_size: int
    has_more: bool
```

## Correctness Properties

*属性（Property）是关于系统行为的形式化陈述，应该在所有有效执行中保持为真。属性是人类可读规范和机器可验证正确性保证之间的桥梁。*


### Property 1: 赛事列表渲染完整性

*对于任意*赛事数据列表，渲染后的列表组件应该包含每个赛事的缩略图、标题、日期和浏览量信息

**Validates: Requirements 1.1**

### Property 2: 下拉刷新触发数据重载

*对于任意*赛事列表页面，执行下拉刷新操作应该触发数据重新加载请求

**Validates: Requirements 1.2**

### Property 3: 赛事详情页渲染完整性

*对于任意*赛事数据，详情页应该显示完整图片、标题、客服信息和在线时间

**Validates: Requirements 2.2, 2.3**

### Property 4: 图片点击触发预览

*对于任意*赛事详情页的图片，点击应该触发图片预览和缩放功能

**Validates: Requirements 2.4, 9.3**

### Property 5: 搜索结果匹配关键词

*对于任意*搜索关键词和赛事列表，搜索返回的所有结果的标题都应该包含该关键词

**Validates: Requirements 3.1**

### Property 6: 清空搜索恢复完整列表

*对于任意*赛事列表，在执行搜索后清空搜索框应该恢复显示原始的完整列表

**Validates: Requirements 3.3**

### Property 7: 个人中心显示用户信息

*对于任意*已授权的用户，个人中心页面应该显示该用户的微信头像和昵称

**Validates: Requirements 4.1, 5.3**

### Property 8: 授权成功后本地存储用户信息

*对于任意*用户授权成功的场景，用户信息应该被保存到本地存储，并且可以被正确读取

**Validates: Requirements 5.2**

### Property 9: 导航栏在所有主页面显示

*对于所有*主要页面（首页、今日方案、我的），底部都应该显示包含三个标签的导航栏

**Validates: Requirements 6.1, 6.2**

### Property 10: 导航标签点击切换页面

*对于任意*导航标签，点击应该切换到对应的页面，并高亮显示该标签

**Validates: Requirements 6.3, 6.4**

### Property 11: API 响应格式一致性

*对于任意*API 请求，响应应该是有效的 JSON 格式，并包含标准的状态码和消息字段

**Validates: Requirements 8.2, 8.3**

### Property 12: 分页查询返回正确数量

*对于任意*有效的页码和页大小参数，API 分页查询应该返回不超过指定页大小的数据项数量

**Validates: Requirements 8.4**

### Property 13: 图片加载显示占位符

*对于任意*正在加载的图片，在加载完成前应该显示加载占位符

**Validates: Requirements 9.1**

## Error Handling

### 前端错误处理

**网络请求错误：**
- 使用统一的请求拦截器捕获网络错误
- 显示用户友好的错误提示（如"网络连接失败，请稍后重试"）
- 提供重试机制

**数据加载失败：**
- 显示空状态页面或错误提示
- 提供刷新按钮让用户重新加载

**图片加载失败：**
- 显示默认占位图
- 记录错误日志用于调试

**授权失败：**
- 用户拒绝授权时显示默认头像和昵称
- 允许用户以游客身份浏览内容
- 在需要授权的操作时再次提示授权

### 后端错误处理

**HTTP 状态码规范：**
- 200: 成功
- 400: 请求参数错误
- 401: 未授权
- 404: 资源不存在
- 500: 服务器内部错误

**错误响应格式：**
```json
{
  "code": 400,
  "message": "参数错误：缺少必需字段 'title'",
  "data": null
}
```

**异常处理策略：**
- 使用 FastAPI 的异常处理器统一处理异常
- 记录详细的错误日志
- 返回用户友好的错误信息（不暴露内部实现细节）

**数据库错误：**
- 捕获数据库连接错误
- 处理数据完整性约束违反
- 实现事务回滚机制

## Testing Strategy

### 测试方法

本项目采用**双重测试策略**，结合单元测试和属性测试来确保代码质量：

**单元测试（Unit Tests）：**
- 验证特定示例和边界情况
- 测试错误条件和异常处理
- 测试组件的集成点
- 使用 Jest (前端) 和 pytest (后端)

**属性测试（Property-Based Tests）：**
- 验证通用属性在所有输入下都成立
- 通过随机化实现全面的输入覆盖
- 每个属性测试至少运行 100 次迭代
- 使用 fast-check (前端) 和 Hypothesis (后端)

### 前端测试

**测试框架：**
- Jest: 单元测试框架
- @testing-library/react: React 组件测试
- fast-check: 属性测试库

**测试覆盖范围：**

1. **组件测试：**
   - EventCard 组件渲染测试
   - SearchBar 搜索功能测试
   - QRCodeModal 弹窗显示测试

2. **服务测试：**
   - API 客户端请求测试
   - 数据转换和验证测试

3. **工具函数测试：**
   - 请求工具测试
   - 存储工具测试

**属性测试示例：**
```typescript
// 测试 Property 1: 赛事列表渲染完整性
// Feature: football-event-miniapp, Property 1: 赛事列表渲染完整性
test('event list renders all required fields', () => {
  fc.assert(
    fc.property(
      fc.array(eventArbitrary),
      (events) => {
        const rendered = renderEventList(events);
        return events.every(event => 
          rendered.includes(event.thumbnailUrl) &&
          rendered.includes(event.title) &&
          rendered.includes(event.date) &&
          rendered.includes(event.viewCount.toString())
        );
      }
    ),
    { numRuns: 100 }
  );
});
```

### 后端测试

**测试框架：**
- pytest: 单元测试框架
- pytest-asyncio: 异步测试支持
- Hypothesis: 属性测试库
- httpx: HTTP 客户端测试

**测试覆盖范围：**

1. **API 端点测试：**
   - 赛事列表查询测试
   - 赛事详情获取测试
   - 用户认证测试

2. **服务层测试：**
   - 业务逻辑测试
   - 数据验证测试

3. **数据库测试：**
   - 模型创建和查询测试
   - 数据完整性测试

**属性测试示例：**
```python
# 测试 Property 12: 分页查询返回正确数量
# Feature: football-event-miniapp, Property 12: 分页查询返回正确数量
@given(
    page=st.integers(min_value=1, max_value=100),
    page_size=st.integers(min_value=1, max_value=50)
)
@settings(max_examples=100)
def test_pagination_returns_correct_count(page, page_size):
    response = client.get(f"/api/events?page={page}&page_size={page_size}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= page_size
```

### 测试数据生成

**前端数据生成器（fast-check）：**
```typescript
const eventArbitrary = fc.record({
  id: fc.integer({ min: 1 }),
  title: fc.string({ minLength: 1, maxLength: 100 }),
  date: fc.date(),
  imageUrl: fc.webUrl(),
  thumbnailUrl: fc.webUrl(),
  viewCount: fc.integer({ min: 0 })
});
```

**后端数据生成器（Hypothesis）：**
```python
@st.composite
def event_strategy(draw):
    return {
        "title": draw(st.text(min_size=1, max_size=200)),
        "date": draw(st.dates()),
        "image_url": draw(st.from_regex(r'https?://[^\s]+')),
        "thumbnail_url": draw(st.from_regex(r'https?://[^\s]+')),
    }
```

### 集成测试

**端到端测试：**
- 使用微信开发者工具进行小程序真机测试
- 测试完整的用户流程（浏览 → 搜索 → 查看详情 → 授权）

**API 集成测试：**
- 测试前后端接口对接
- 验证数据格式和字段匹配
- 测试错误处理流程

### 测试执行

**前端测试命令：**
```bash
# 运行所有测试
npm test

# 运行属性测试
npm test -- --testNamePattern="property"

# 生成覆盖率报告
npm test -- --coverage
```

**后端测试命令：**
```bash
# 运行所有测试
pytest

# 运行属性测试
pytest -m property

# 生成覆盖率报告
pytest --cov=app --cov-report=html
```

### 持续集成

- 在 Git 提交前运行测试
- 使用 GitHub Actions 或类似 CI 工具自动运行测试
- 要求所有测试通过才能合并代码
- 维护测试覆盖率在 80% 以上
