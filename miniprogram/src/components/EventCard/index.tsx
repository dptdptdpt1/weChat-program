import { View, Image, Text } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { IEvent } from '../../types'
import { getImageUrl } from '../../utils/request'
import './index.scss'

interface EventCardProps {
  event: IEvent
  onClick?: (event: IEvent) => void
}

/**
 * 赛事卡片组件
 * 显示赛事缩略图、标题、日期、浏览量
 */
export default function EventCard({ event, onClick }: EventCardProps) {
  // 处理点击事件
  const handleClick = () => {
    if (onClick) {
      onClick(event)
    } else {
      // 默认跳转到详情页
      Taro.navigateTo({
        url: `/pages/event-detail/index?id=${event.id}`
      })
    }
  }

  // 格式化日期
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${month}-${day}`
  }

  // 格式化浏览量
  const formatViewCount = (count: number) => {
    if (count >= 10000) {
      return `${(count / 10000).toFixed(1)}万`
    }
    return count.toString()
  }

  return (
    <View className='event-card' onClick={handleClick}>
      {/* 缩略图 */}
      <View className='event-card__image-wrapper'>
        {event.cover_image ? (
          <Image
            className='event-card__image'
            src={getImageUrl(event.cover_image)}
            mode='aspectFill'
            lazyLoad
          />
        ) : (
          <View className='event-card__placeholder'>
            <Text>📷</Text>
          </View>
        )}
      </View>

      {/* 内容区域 */}
      <View className='event-card__content'>
        {/* 标题 */}
        <Text className='event-card__title'>{event.title}</Text>

        {/* 底部信息 */}
        <View className='event-card__footer'>
          {/* 日期 */}
          <View className='event-card__date'>
            <Text className='event-card__date-icon'>📅</Text>
            <Text className='event-card__date-text'>{formatDate(event.date)}</Text>
          </View>

          {/* 浏览量 */}
          <View className='event-card__views'>
            <Text className='event-card__views-icon'>👁</Text>
            <Text className='event-card__views-text'>{formatViewCount(event.view_count)}</Text>
          </View>
        </View>
      </View>
    </View>
  )
}
