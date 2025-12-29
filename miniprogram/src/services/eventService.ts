import { get, post } from '../utils/request'
import { IEvent, IPaginatedResponse, IEventListQuery } from '../types'

/**
 * 赛事服务
 */
class EventService {
  /**
   * 获取赛事列表
   * @param params 查询参数
   * @returns 赛事列表和分页信息
   */
  async getEvents(params: IEventListQuery = {}): Promise<IPaginatedResponse<IEvent>> {
    const { page = 1, page_size = 10, keyword } = params
    
    return get<IPaginatedResponse<IEvent>>('/api/events', {
      page,
      page_size,
      keyword
    })
  }

  /**
   * 获取赛事详情
   * @param id 赛事ID
   * @returns 赛事详情
   */
  async getEventDetail(id: number): Promise<IEvent> {
    return get<IEvent>(`/api/events/${id}`, undefined, true)
  }

  /**
   * 增加赛事浏览量
   * @param id 赛事ID
   * @returns 更新后的赛事信息
   */
  async increaseViewCount(id: number): Promise<IEvent> {
    return post<IEvent>(`/api/events/${id}/view`)
  }
}

export default new EventService()
