// 轮播图相关服务
import { get } from '../utils/request'
import { IBanner } from '../types'

/**
 * 获取轮播图列表
 */
export const getBanners = async (): Promise<IBanner[]> => {
  return await get<IBanner[]>('/api/banners', {
    is_active: true
  })
}

export default {
  getBanners
}
