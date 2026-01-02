// 全局常量声明
declare const API_BASE_URL: string

// API 响应基础类型
export interface IApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// 分页响应类型
export interface IPaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  has_more: boolean
}

// 赛事类型
export interface IEvent {
  id: number
  title: string
  date: string
  content?: string
  cover_image?: string
  view_count: number
  created_at: string
  updated_at: string
}

// 用户信息类型
export interface IUserInfo {
  id: number
  open_id: string
  nick_name?: string
  avatar_url?: string
  created_at: string
  last_login_at: string
}

// 客服配置类型
export interface ICustomerService {
  id: number
  qr_code_url: string
  online_time: string
  updated_at: string
}

// 轮播图类型
export interface IBanner {
  id: number
  image_url: string
  title?: string
  link_url?: string
  sort_order: number
  is_active: boolean
  created_at: string
  updated_at: string
}

// 微信登录请求类型
export interface IWxLoginRequest {
  code: string
  nick_name?: string
  avatar_url?: string
}

// 赛事列表查询参数
export interface IEventListQuery {
  page?: number
  page_size?: number
  keyword?: string
}
