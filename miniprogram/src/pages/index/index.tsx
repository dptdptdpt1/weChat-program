import { View, Text, ScrollView, Swiper, SwiperItem, Image } from '@tarojs/components'
import { useState, useCallback } from 'react'
import Taro, { useLoad, usePullDownRefresh } from '@tarojs/taro'
import { EventCard } from '../../components'
import { eventService, bannerService } from '../../services'
import { IEvent, IBanner } from '../../types'
import { getImageUrl } from '../../utils/request'
import './index.scss'

export default function Index() {
  const [events, setEvents] = useState<IEvent[]>([])
  const [banners, setBanners] = useState<IBanner[]>([])
  const [loading, setLoading] = useState(false)
  const [isEmpty, setIsEmpty] = useState(false)
  const [error, setError] = useState('')

  // 加载轮播图
  const loadBanners = useCallback(async () => {
    try {
      const result = await bannerService.getBanners()
      setBanners(result)
    } catch (err: any) {
      console.error('加载轮播图失败:', err)
      // 轮播图加载失败不影响主要功能，只记录错误
    }
  }, [])

  // 加载赛事列表
  const loadEvents = useCallback(async () => {
    try {
      setLoading(true)
      setError('')
      
      const result = await eventService.getEvents({
        page: 1,
        page_size: 20
      })
      
      setEvents(result.items)
      setIsEmpty(result.items.length === 0)
    } catch (err: any) {
      console.error('加载赛事列表失败:', err)
      setError(err.message || '加载失败')
      setEvents([])
    } finally {
      setLoading(false)
    }
  }, [])

  // 页面加载时获取数据
  useLoad(() => {
    console.log('首页加载')
    loadBanners()
    loadEvents()
  })

  // 下拉刷新
  usePullDownRefresh(async () => {
    console.log('下拉刷新')
    await Promise.all([loadBanners(), loadEvents()])
    Taro.stopPullDownRefresh()
  })

  // 渲染空状态
  const renderEmpty = () => (
    <View className='index__empty'>
      <Text className='index__empty-icon'>📭</Text>
      <Text className='index__empty-text'>暂无赛事</Text>
    </View>
  )

  // 渲染错误状态
  const renderError = () => (
    <View className='index__error'>
      <Text className='index__error-icon'>⚠️</Text>
      <Text className='index__error-text'>{error}</Text>
      <View className='index__error-btn' onClick={loadEvents}>
        <Text>重新加载</Text>
      </View>
    </View>
  )

  // 渲染加载状态
  const renderLoading = () => (
    <View className='index__loading'>
      <Text className='index__loading-text'>加载中...</Text>
    </View>
  )

  return (
    <View className='index'>
      {/* 头部标题 */}
      <View className='index__header'>
        <Text className='index__title'>赛事列表</Text>
        <Text className='index__subtitle'>最新足球赛事资讯</Text>
      </View>

      {/* 轮播图 */}
      <View className='index__banner'>
        <Swiper
          className='index__swiper'
          indicatorColor='rgba(255, 255, 255, 0.5)'
          indicatorActiveColor='#fff'
          circular
          autoplay
          interval={3000}
          duration={500}
        >
          {banners.map(banner => (
            <SwiperItem key={banner.id}>
              <View className='index__banner-item'>
                <Image
                  className='index__banner-image'
                  src={getImageUrl(banner.image_url)}
                  mode='aspectFill'
                />
              </View>
            </SwiperItem>
          ))}
        </Swiper>
      </View>

      {/* 内容区域 */}
      <ScrollView
        className='index__content'
        scrollY
        enableBackToTop
      >
        {loading && events.length === 0 ? (
          renderLoading()
        ) : error ? (
          renderError()
        ) : isEmpty ? (
          renderEmpty()
        ) : (
          <View className='index__list'>
            {events.map(event => (
              <EventCard key={event.id} event={event} />
            ))}
          </View>
        )}
      </ScrollView>
    </View>
  )
}

