# 开发指南

## 快速开始

### 1. 环境准备

**后端环境:**
- Python 3.9+
- pip

**前端环境:**
- Node.js 14+
- npm 或 yarn
- 微信开发者工具

### 2. 后端启动

```bash
# 进入 API 目录
cd api

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动开发服务器
uvicorn main:app --reload
```

后端服务将在 http://localhost:8000 启动

### 3. 前端启动

```bash
# 进入小程序目录
cd miniprogram

# 安装依赖
npm install

# 启动微信小程序开发模式
npm run dev:weapp
```

使用微信开发者工具打开 `miniprogram` 目录

## 开发流程

### 添加新的 API 端点

1. **创建数据模型** (如果需要)
   ```python
   # api/app/models/your_model.py
   from sqlalchemy import Column, Integer, String
   from app.utils.database import Base
   
   class YourModel(Base):
       __tablename__ = "your_table"
       id = Column(Integer, primary_key=True)
       name = Column(String(100))
   ```

2. **创建 Pydantic Schema**
   ```python
   # api/app/schemas/your_schema.py
   from pydantic import BaseModel
   
   class YourSchema(BaseModel):
       id: int
       name: str
       
       class Config:
           from_attributes = True
   ```

3. **创建服务层**
   ```python
   # api/app/services/your_service.py
   class YourService:
       @staticmethod
       def get_data(db: Session):
           return db.query(YourModel).all()
   ```

4. **创建路由**
   ```python
   # api/app/routes/your_route.py
   from fastapi import APIRouter, Depends
   from sqlalchemy.orm import Session
   
   router = APIRouter()
   
   @router.get("/")
   def get_data(db: Session = Depends(get_db)):
       data = YourService.get_data(db)
       return ApiResponse(code=200, message="成功", data=data)
   ```

5. **注册路由**
   ```python
   # api/main.py
   from app.routes import your_route
   app.include_router(your_route.router, prefix="/api/your-path", tags=["标签"])
   ```

### 添加新的小程序页面

1. **创建页面目录**
   ```
   miniprogram/src/pages/your-page/
   ├── index.tsx        # 页面组件
   ├── index.scss       # 页面样式
   └── index.config.ts  # 页面配置
   ```

2. **实现页面组件**
   ```typescript
   // index.tsx
   import { View, Text } from '@tarojs/components'
   import { useLoad } from '@tarojs/taro'
   import './index.scss'
   
   export default function YourPage() {
     useLoad(() => {
       console.log('页面加载')
     })
     
     return (
       <View className='your-page'>
         <Text>Your Content</Text>
       </View>
     )
   }
   ```

3. **配置页面**
   ```typescript
   // index.config.ts
   export default definePageConfig({
     navigationBarTitleText: '页面标题'
   })
   ```

4. **注册页面路由**
   ```typescript
   // src/app.config.ts
   export default defineAppConfig({
     pages: [
       'pages/index/index',
       'pages/your-page/index'  // 添加新页面
     ]
   })
   ```

### 添加新的组件

1. **创建组件目录**
   ```
   miniprogram/src/components/YourComponent/
   ├── index.tsx   # 组件实现
   └── index.scss  # 组件样式
   ```

2. **实现组件**
   ```typescript
   // index.tsx
   import { View, Text } from '@tarojs/components'
   import './index.scss'
   
   interface YourComponentProps {
     title: string
   }
   
   export default function YourComponent({ title }: YourComponentProps) {
     return (
       <View className='your-component'>
         <Text>{title}</Text>
       </View>
     )
   }
   ```

3. **导出组件**
   ```typescript
   // components/index.ts
   export { default as YourComponent } from './YourComponent'
   ```

## 调试技巧

### 后端调试

1. **查看日志**
   ```bash
   # 日志会输出到控制台
   uvicorn main:app --reload --log-level debug
   ```

2. **使用 Swagger UI**
   - 访问 http://localhost:8000/docs
   - 直接测试 API 端点

3. **Python 调试器**
   ```python
   import pdb; pdb.set_trace()
   ```

### 前端调试

1. **微信开发者工具控制台**
   - 查看 console.log 输出
   - 查看网络请求
   - 查看存储数据

2. **真机调试**
   - 点击"预览"生成二维码
   - 使用微信扫码在真机上测试

3. **调试技巧**
   ```typescript
   // 打印状态
   console.log('State:', state)
   
   // 打印 API 响应
   console.log('API Response:', response)
   ```

## 常见问题

### 1. 跨域问题

**问题**: 前端请求后端 API 时出现跨域错误

**解决**: 
- 确保后端已配置 CORS 中间件
- 检查 `api/main.py` 中的 CORS 配置
- 开发环境可以设置 `allow_origins=["*"]`

### 2. 微信登录失败

**问题**: 调用微信登录 API 失败

**解决**:
- 检查是否配置了正确的 AppID 和 AppSecret
- 确保在微信公众平台配置了服务器域名
- 开发环境可以使用模拟数据测试

### 3. 图片不显示

**问题**: 小程序中图片无法显示

**解决**:
- 检查图片 URL 是否正确
- 确保图片域名在微信公众平台配置了下载域名
- 开发环境可以勾选"不校验合法域名"

### 4. 数据库连接失败

**问题**: 后端启动时数据库连接失败

**解决**:
- 确保已运行 `python init_db.py` 初始化数据库
- 检查数据库文件路径是否正确
- 查看错误日志定位问题

## 代码规范

### Python 代码规范

- 使用 snake_case 命名变量和函数
- 使用 PascalCase 命名类
- 添加中文注释说明功能
- 使用类型提示

```python
def get_user_info(user_id: int) -> dict:
    """获取用户信息"""
    pass
```

### TypeScript 代码规范

- 使用 camelCase 命名变量和函数
- 使用 PascalCase 命名组件和类型
- 接口以 I 开头
- 添加中文注释

```typescript
interface IUserInfo {
  id: number
  name: string
}

function getUserInfo(userId: number): IUserInfo {
  // 获取用户信息
}
```

## 性能优化建议

1. **图片优化**
   - 使用缩略图显示列表
   - 启用图片懒加载
   - 压缩图片大小

2. **请求优化**
   - 使用分页加载
   - 实现搜索防抖
   - 缓存常用数据

3. **渲染优化**
   - 避免不必要的重渲染
   - 使用 React.memo 优化组件
   - 合理使用 useCallback 和 useMemo

## 测试

### 后端测试

```bash
# 运行所有测试
python test_all_apis.py

# 运行特定测试
python test_events_api.py
python test_auth_api.py
python test_config_api.py
```

### 前端测试

目前前端测试为可选任务,可以根据需要添加:
- 组件单元测试
- 页面集成测试
- E2E 测试

## 部署准备

### 后端部署检查清单

- [ ] 配置生产环境数据库
- [ ] 设置环境变量
- [ ] 配置 CORS 允许的域名
- [ ] 启用 HTTPS
- [ ] 配置日志记录
- [ ] 设置错误监控

### 前端部署检查清单

- [ ] 配置生产环境 API 地址
- [ ] 准备 TabBar 图标资源
- [ ] 配置微信 AppID
- [ ] 在微信公众平台配置服务器域名
- [ ] 测试所有功能
- [ ] 构建生产版本

## 获取帮助

- 查看项目文档: `PROJECT_SUMMARY.md`
- 查看需求文档: `.kiro/specs/football-event-miniapp/requirements.md`
- 查看设计文档: `.kiro/specs/football-event-miniapp/design.md`
- 查看任务列表: `.kiro/specs/football-event-miniapp/tasks.md`
