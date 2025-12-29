import { View, Image, Text, RichText } from '@tarojs/components'
import { useState } from 'react'
import Taro, { useLoad, useRouter } from '@tarojs/taro'
import { eventService, configService } from '../../services'
import { IEvent, ICustomerService } from '../../types'
import { getImageUrl } from '../../utils/request'
import { parseMarkdown } from '../../utils/markdown'
import './index.scss'

export default function EventDetail() {
  const router = useRouter()
  const [event, setEvent] = useState<IEvent | null>(null)
  const [customerService, setCustomerService] = useState<ICustomerService | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // 加载赛事详情
  const loadEventDetail = async (id: number) => {
    try {
      setLoading(true)
      setError('')

      // 并行加载赛事详情和客服配置
      const [eventData, csData] = await Promise.all([
        eventService.getEventDetail(id),
        configService.getCustomerService()
      ])

      setEvent(eventData)
      setCustomerService(csData)

      // 增加浏览量
      eventService.increaseViewCount(id).catch(err => {
        console.error('增加浏览量失败:', err)
      })
    } catch (err: any) {
      console.error('加载赛事详情失败:', err)
      setError(err.message || '加载失败')
    } finally {
      setLoading(false)
    }
  }

  // 页面加载
  useLoad(() => {
    console.log('赛事详情页面加载', router.params)
    const eventId = parseInt(router.params.id || '0')
    
    if (eventId) {
      loadEventDetail(eventId)
    } else {
      setError('赛事ID无效')
    }
  })

  // 格式化发布时间
  const formatPublishTime = (dateStr: string) => {
    const date = new Date(dateStr)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${year}-${month}-${day} ${hours}:${minutes}`
  }

  // 渲染加载状态
  const renderLoading = () => (
    <View className='event-detail__loading'>
      <Text className='event-detail__loading-text'>加载中...</Text>
    </View>
  )

  // 渲染错误状态
  const renderError = () => (
    <View className='event-detail__error'>
      <Text className='event-detail__error-icon'>⚠️</Text>
      <Text className='event-detail__error-text'>{error}</Text>
      <View className='event-detail__error-btn' onClick={() => Taro.navigateBack()}>
        <Text>返回</Text>
      </View>
    </View>
  )

  // 渲染内容
  const renderContent = () => {
    if (!event) return null

    return (
      <View className='event-detail__content'>
        {/* 赛事信息 */}
        <View className='event-detail__info'>
          {/* 标题 */}
          <Text className='event-detail__title'>{event.title}</Text>

          {/* 元信息 */}
          <View className='event-detail__meta'>
            <View className='event-detail__meta-item'>
              <Text className='event-detail__meta-icon'>🕐</Text>
              <Text className='event-detail__meta-text'>发布于 {formatPublishTime(event.created_at)}</Text>
            </View>
            <View className='event-detail__meta-item'>
              <Text className='event-detail__meta-icon'>👁</Text>
              <Text className='event-detail__meta-text'>{event.view_count} 次浏览</Text>
            </View>
          </View>

          {/* 赛事内容 */}
          {event.content && (
            <View className='event-detail__body'>
              <RichText nodes={parseMarkdown(event.content)} />
            </View>
          )}
        </View>

        {/* 客服信息 */}
        {customerService && (
          <View className='event-detail__customer-service'>
            <View className='event-detail__cs-header'>
              <Text className='event-detail__cs-title'>客服信息</Text>
            </View>
            <View className='event-detail__cs-content'>
              <View className='event-detail__cs-qrcode'>
                <Image
                  className='event-detail__cs-image'
                  src={getImageUrl(customerService.qr_code_url)}
                  mode='aspectFit'
                  showMenuByLongpress
                />
                <Text className='event-detail__cs-tip'>长按保存二维码</Text>
              </View>
            </View>
          </View>
        )}
      </View>
    )
  }

  return (
    <View className='event-detail'>
      {loading ? renderLoading() : error ? renderError() : renderContent()}
    </View>
  )
}

