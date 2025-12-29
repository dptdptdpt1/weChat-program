// 统一导出所有服务
import eventServiceInstance from './eventService'
import authServiceInstance from './authService'
import configServiceInstance from './configService'
import bannerServiceInstance from './bannerService'

export const eventService = eventServiceInstance
export const authService = authServiceInstance
export const configService = configServiceInstance
export const bannerService = bannerServiceInstance
