import Taro from '@tarojs/taro'

// API 基础地址 - 从编译时配置中获取
// @ts-ignore
const API_BASE_URL = `${process.env.API_BASE_URL || 'http://localhost:8000'}/api`

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  header?: Record<string, string>
}

export async function request<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { method = 'GET', data, header = {} } = options

  try {
    const response = await Taro.request({
      url: `${API_BASE_URL}${endpoint}`,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        ...header
      }
    })

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return response.data as T
    } else {
      throw new Error(`Request failed with status ${response.statusCode}`)
    }
  } catch (error) {
    console.error('API request error:', error)
    throw error
  }
}

export const api = {
  get: <T>(endpoint: string) => request<T>(endpoint, { method: 'GET' }),
  post: <T>(endpoint: string, data: any) => request<T>(endpoint, { method: 'POST', data }),
  put: <T>(endpoint: string, data: any) => request<T>(endpoint, { method: 'PUT', data }),
  delete: <T>(endpoint: string) => request<T>(endpoint, { method: 'DELETE' })
}
