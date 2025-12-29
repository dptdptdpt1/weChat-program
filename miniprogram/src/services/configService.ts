import { get } from '../utils/request'
import { ICustomerService } from '../types'

/**
 * 配置服务
 */
class ConfigService {
  /**
   * 获取客服配置
   * @returns 客服配置信息
   */
  async getCustomerService(): Promise<ICustomerService> {
    return get<ICustomerService>('/api/config/customer-service')
  }
}

export default new ConfigService()
