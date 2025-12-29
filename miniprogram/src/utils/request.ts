import Taro from '@tarojs/taro'
import { IApiResponse } from '../types'

// API 基础地址 - 开发环境
// 生产环境需要修改为实际的服务器地址
const API_BASE_URL = 'http://localhost:8000'

/**
 * 获取完整的图片 URL
 * 将相对路径转换为完整的后端 URL
 */
export function getImageUrl(path: string): string {
  if (!path) return ''
  
  // 如果已经是完整 URL，直接返回
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  
  // 如果是相对路径，拼接后端地址
  if (path.startsWith('/')) {
    return `${API_BASE_URL}${path}`
  }
  
  return `${API_BASE_URL}/${path}`
}

/**
 * 导出 API 基础地址供其他模块使用
 */
export { API_BASE_URL }

// 请求配置接口
interface RequestConfig {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  header?: Record<string, string>
  showLoading?: boolean
  loadingText?: string
}

/**
 * 统一请求封装
 */
export async function request<T = any>(config: RequestConfig): Promise<T> {
  const {
    url,
    method = 'GET',
    data,
    header = {},
    showLoading = false,
    loadingText = '加载中...'
  } = config

  // 显示加载提示
  if (showLoading) {
    Taro.showLoading({
      title: loadingText,
      mask: true
    })
  }

  try {
    // 发起请求
    const response = await Taro.request({
      url: `${API_BASE_URL}${url}`,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        ...header
      },
      timeout: 10000
    })

    // 隐藏加载提示
    if (showLoading) {
      Taro.hideLoading()
    }

    // 处理响应
    const result = response.data as IApiResponse<T>

    // 检查业务状态码
    if (result.code === 200) {
      return result.data
    } else {
      // 业务错误
      throw new Error(result.message || '请求失败')
    }
  } catch (error: any) {
    // 隐藏加载提示
    if (showLoading) {
      Taro.hideLoading()
    }

    // 处理错误
    handleError(error)
    throw error
  }
}

/**
 * 统一错误处理
 */
function handleError(error: any) {
  let message = '网络请求失败'

  if (error.errMsg) {
    // Taro 请求错误
    if (error.errMsg.includes('timeout')) {
      message = '请求超时,请检查网络'
    } else if (error.errMsg.includes('fail')) {
      message = '网络连接失败'
    }
  } else if (error.message) {
    // 业务错误
    message = error.message
  }

  // 显示错误提示
  Taro.showToast({
    title: message,
    icon: 'none',
    duration: 2000
  })

  console.error('请求错误:', error)
}

/**
 * GET 请求
 */
export function get<T = any>(url: string, params?: any, showLoading = false): Promise<T> {
  // 构建查询字符串
  if (params) {
    const queryString = Object.keys(params)
      .filter(key => params[key] !== undefined && params[key] !== null)
      .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
      .join('&')
    
    if (queryString) {
      url = `${url}?${queryString}`
    }
  }

  return request<T>({
    url,
    method: 'GET',
    showLoading
  })
}

/**
 * POST 请求
 */
export function post<T = any>(url: string, data?: any, showLoading = false): Promise<T> {
  return request<T>({
    url,
    method: 'POST',
    data,
    showLoading
  })
}

/**
 * PUT 请求
 */
export function put<T = any>(url: string, data?: any, showLoading = false): Promise<T> {
  return request<T>({
    url,
    method: 'PUT',
    data,
    showLoading
  })
}

/**
 * DELETE 请求
 */
export function del<T = any>(url: string, showLoading = false): Promise<T> {
  return request<T>({
    url,
    method: 'DELETE',
    showLoading
  })
}
