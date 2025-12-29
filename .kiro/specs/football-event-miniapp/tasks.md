# Implementation Plan: 宝利足球赛事通小程序

## Overview

本实施计划将宝利足球赛事通小程序的开发分解为离散的编码任务。实施将采用增量方式，先搭建后端 API，再开发前端小程序，最后进行集成和测试。每个任务都引用了相应的需求，确保可追溯性。

## Tasks

- [x] 1. 搭建后端项目基础结构
  - 创建 FastAPI 应用入口和基本配置
  - 配置数据库连接（SQLite + SQLAlchemy）
  - 设置 CORS 中间件支持跨域请求
  - 创建基础的响应模型和错误处理器
  - _Requirements: 8.1, 8.2, 8.3_

- [x] 2. 实现数据库模型和迁移
  - [x] 2.1 创建 Event 模型
    - 定义赛事表结构（id, title, date, image_url, thumbnail_url, view_count, created_at, updated_at）
    - _Requirements: 1.1, 2.2_

  - [x] 2.2 创建 User 模型
    - 定义用户表结构（id, open_id, nick_name, avatar_url, created_at, last_login_at）
    - _Requirements: 4.1, 5.2_

  - [x] 2.3 创建 CustomerService 模型
    - 定义客服配置表结构（id, qr_code_url, online_time, updated_at）
    - _Requirements: 2.3, 7.2_

  - [x] 2.4 创建数据库初始化脚本
    - 实现表创建和初始数据填充
    - _Requirements: 8.1_

- [x] 3. 实现赛事相关 API 端点
  - [x] 3.1 实现 GET /api/events 端点
    - 支持分页参数（page, page_size）
    - 支持搜索参数（keyword）
    - 返回赛事列表和分页信息
    - _Requirements: 1.1, 3.1, 8.4_

  - [ ]* 3.2 编写 Property 12 的属性测试
    - **Property 12: 分页查询返回正确数量**
    - **Validates: Requirements 8.4**

  - [x] 3.3 实现 GET /api/events/{id} 端点
    - 根据 ID 获取赛事详情
    - 处理赛事不存在的情况（返回 404）
    - _Requirements: 2.1, 2.2_

  - [x] 3.4 实现 POST /api/events/{id}/view 端点
    - 增加指定赛事的浏览量
    - _Requirements: 1.1_

  - [ ]* 3.5 编写 Property 11 的属性测试
    - **Property 11: API 响应格式一致性**
    - **Validates: Requirements 8.2, 8.3**

- [x] 4. 实现用户认证 API 端点
  - [x] 4.1 实现 POST /api/auth/login 端点
    - 接收微信 code 参数
    - 调用微信 API 获取 openid 和 session_key
    - 创建或更新用户记录
    - 返回用户信息
    - _Requirements: 5.1, 5.2_

  - [x] 4.2 实现 GET /api/auth/user 端点
    - 根据 openid 获取用户信息
    - _Requirements: 4.1, 5.3_

  - [ ]* 4.3 编写用户认证的单元测试
    - 测试登录成功场景
    - 测试登录失败场景
    - _Requirements: 5.1, 5.2_

- [x] 5. 实现客服配置 API 端点
  - [x] 5.1 实现 GET /api/config/customer-service 端点
    - 返回客服二维码 URL 和在线时间
    - _Requirements: 2.3, 7.2_

  - [ ]* 5.2 编写客服配置的单元测试
    - 测试获取客服配置成功
    - _Requirements: 7.2_

- [x] 6. Checkpoint - 后端 API 测试
  - 确保所有 API 端点测试通过，使用 Postman 或 curl 手动测试基本功能，如有问题请询问用户

- [x] 7. 搭建前端小程序基础结构
  - 配置 Taro 项目和 TypeScript
  - 设置底部导航栏（首页、今日方案、我的）
  - 创建基础页面结构（index, proposal, profile, event-detail）
  - 配置 app.config.ts（页面路由、窗口样式、tabBar）
  - _Requirements: 6.1, 6.2_

- [x] 8. 实现 API 客户端和服务层
  - [x] 8.1 创建请求工具函数
    - 封装 Taro.request
    - 实现请求拦截器（添加通用 headers）
    - 实现响应拦截器（统一错误处理）
    - _Requirements: 8.2, 8.3_

  - [x] 8.2 创建 eventService
    - 实现 getEvents 方法（支持分页和搜索）
    - 实现 getEventDetail 方法
    - 实现 increaseViewCount 方法
    - _Requirements: 1.1, 2.1, 3.1_

  - [x] 8.3 创建 authService
    - 实现 wxLogin 方法（微信登录）
    - 实现 getUserInfo 方法
    - _Requirements: 5.1, 5.2_

  - [x] 8.4 创建 TypeScript 类型定义
    - 定义 IEvent, IUserInfo, IApiResponse, IPaginatedResponse 接口
    - _Requirements: 8.2_

- [x] 9. 实现通用组件
  - [x] 9.1 创建 EventCard 组件
    - 显示赛事缩略图、标题、日期、浏览量
    - 支持点击跳转到详情页
    - _Requirements: 1.1, 2.1_

  - [ ]* 9.2 编写 Property 1 的属性测试
    - **Property 1: 赛事列表渲染完整性**
    - **Validates: Requirements 1.1**

  - [x] 9.3 创建 SearchBar 组件
    - 实现搜索输入框
    - 支持实时搜索（debounce 优化）
    - 支持清空搜索
    - _Requirements: 3.1, 3.3_

  - [ ]* 9.4 编写 Property 5 和 Property 6 的属性测试
    - **Property 5: 搜索结果匹配关键词**
    - **Property 6: 清空搜索恢复完整列表**
    - **Validates: Requirements 3.1, 3.3**

  - [x] 9.5 创建 QRCodeModal 组件
    - 显示客服二维码图片
    - 显示在线时间信息
    - 支持长按保存图片
    - 支持点击关闭
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 10. 实现首页（index）
  - [x] 10.1 实现赛事列表展示
    - 调用 eventService.getEvents 获取数据
    - 使用 EventCard 组件渲染列表
    - 实现下拉刷新功能
    - 处理空状态和错误状态
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [ ]* 10.2 编写 Property 2 的属性测试
    - **Property 2: 下拉刷新触发数据重载**
    - **Validates: Requirements 1.2**

  - [x] 10.3 实现图片加载优化
    - 显示加载占位符
    - 处理图片加载失败（显示默认图）
    - _Requirements: 9.1, 9.2_

  - [ ]* 10.4 编写 Property 13 的属性测试
    - **Property 13: 图片加载显示占位符**
    - **Validates: Requirements 9.1**

- [x] 11. 实现今日方案页（proposal）
  - [x] 11.1 实现赛事列表展示
    - 复用首页的列表逻辑
    - 添加 SearchBar 组件
    - 实现搜索过滤功能
    - 处理搜索结果为空的情况
    - _Requirements: 1.1, 3.1, 3.2_

  - [ ]* 11.2 编写搜索功能的单元测试
    - 测试搜索结果为空的边界情况
    - _Requirements: 3.2_

- [x] 12. 实现赛事详情页（event-detail）
  - [x] 12.1 实现详情页面布局
    - 显示赛事完整图片
    - 显示赛事标题
    - 显示客服信息和在线时间
    - 支持图片预览和缩放
    - _Requirements: 2.2, 2.3, 2.4_

  - [ ]* 12.2 编写 Property 3 和 Property 4 的属性测试
    - **Property 3: 赛事详情页渲染完整性**
    - **Property 4: 图片点击触发预览**
    - **Validates: Requirements 2.2, 2.3, 2.4, 9.3**

  - [x] 12.3 实现浏览量增加
    - 页面加载时调用 increaseViewCount API
    - _Requirements: 1.1_

- [x] 13. 实现个人中心页（profile）
  - [x] 13.1 实现微信授权登录
    - 首次打开时请求微信授权
    - 调用 wx.getUserProfile 获取用户信息
    - 调用 authService.wxLogin 完成登录
    - 保存用户信息到本地存储
    - _Requirements: 5.1, 5.2_

  - [ ]* 13.2 编写 Property 8 的属性测试
    - **Property 8: 授权成功后本地存储用户信息**
    - **Validates: Requirements 5.2**

  - [x] 13.3 实现个人中心页面布局
    - 显示用户头像和昵称
    - 显示"我的客服"和"联系我们"入口
    - 处理未授权状态（显示默认头像）
    - _Requirements: 4.1, 4.2, 4.3, 5.3, 5.4_

  - [ ]* 13.4 编写 Property 7 的属性测试
    - **Property 7: 个人中心显示用户信息**
    - **Validates: Requirements 4.1, 5.3**

  - [x] 13.5 集成 QRCodeModal 组件
    - 点击"我的客服"显示二维码弹窗
    - 点击"联系我们"显示二维码弹窗
    - _Requirements: 4.2, 4.3, 7.1_

- [x] 14. 实现底部导航功能
  - [x] 14.1 配置 tabBar 导航
    - 确保所有主页面显示导航栏
    - 配置导航标签文字和图标
    - _Requirements: 6.1, 6.2_

  - [ ]* 14.2 编写 Property 9 和 Property 10 的属性测试
    - **Property 9: 导航栏在所有主页面显示**
    - **Property 10: 导航标签点击切换页面**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4**

- [x] 15. 实现错误处理和用户反馈
  - [x] 15.1 实现统一错误处理
    - 在请求拦截器中捕获网络错误
    - 显示用户友好的错误提示（Toast）
    - _Requirements: 1.4_

  - [x] 15.2 实现加载状态指示
    - 在数据加载时显示 loading 提示
    - _Requirements: 9.1_

  - [ ]* 15.3 编写错误处理的单元测试
    - 测试网络错误场景
    - 测试数据加载失败场景
    - _Requirements: 1.4_

- [x] 16. Checkpoint - 前端功能测试
  - 确保所有页面功能正常，在微信开发者工具中测试完整用户流程，如有问题请询问用户
  - 已创建详细的测试清单文档 (TESTING_CHECKLIST.md)

- [ ] 17. 集成测试和优化
  - [ ] 17.1 前后端联调测试
    - 测试所有 API 接口对接
    - 验证数据格式和字段匹配
    - _Requirements: 8.2, 8.3_

  - [ ] 17.2 性能优化
    - 实现图片懒加载
    - 优化列表渲染性能
    - 添加数据缓存机制
    - _Requirements: 9.1_

  - [ ]* 17.3 编写端到端集成测试
    - 测试完整的用户流程（浏览 → 搜索 → 查看详情 → 授权）
    - _Requirements: 1.1, 2.1, 3.1, 5.1_

- [ ] 18. 最终检查和文档
  - [ ] 18.1 代码审查和重构
    - 检查代码规范和最佳实践
    - 移除未使用的代码和注释
    - _Requirements: All_

  - [ ] 18.2 准备部署配置
    - 配置生产环境 API 地址
    - 准备小程序发布资料
    - _Requirements: 8.1_

  - [ ]* 18.3 编写 API 文档
    - 使用 FastAPI 自动生成 Swagger 文档
    - 添加接口使用说明
    - _Requirements: 8.1_

- [ ] 19. Final Checkpoint - 完整测试
  - 确保所有测试通过，在真机上测试小程序功能，准备提交审核

## Notes

- 任务标记 `*` 的为可选任务，可以跳过以加快 MVP 开发
- 每个任务都引用了具体的需求，确保可追溯性
- Checkpoint 任务用于增量验证，确保每个阶段的质量
- 属性测试验证通用正确性属性，单元测试验证特定示例和边界情况
- 建议按顺序执行任务，先完成后端再开发前端，最后进行集成
