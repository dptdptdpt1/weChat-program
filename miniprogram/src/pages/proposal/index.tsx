import { View, Text, ScrollView } from '@tarojs/components'
import { useState, useCallback } from 'react'
import Taro, { useLoad, usePullDownRefresh } from '@tarojs/taro'
import { EventCard, SearchBar } from '../../components'
import { eventService } from '../../services'
import { IEvent } from '../../types'
import './index.scss'

export default function Proposal() {
  const [events, setEvents] = useState<IEvent[]>([])
  const [loading, setLoading] = useState(false)
  const [isEmpty, setIsEmpty] = useState(false)
  const [error, setError] = useState('')
  const [keyword, setKeyword] = useState('')

  // 加载赛事列表
  const loadEvents = useCallback(async (searchKeyword = '') => {
    try {
      setLoading(true)
      setError('')
      
      const result = await eventService.getEvents({
        page: 1,
        page_size: 20,
        keyword: searchKeyword || undefined
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
    console.log('今日方案页面加载')
    loadEvents()
  })

  // 下拉刷新
  usePullDownRefresh(async () => {
    console.log('下拉刷新')
    await loadEvents(keyword)
    Taro.stopPullDownRefresh()
  })

  // 处理搜索
  const handleSearch = (searchKeyword: string) => {
    console.log('搜索:', searchKeyword)
    setKeyword(searchKeyword)
    loadEvents(searchKeyword)
  }

  // 处理清空搜索
  const handleClear = () => {
    console.log('清空搜索')
    setKeyword('')
    loadEvents('')
  }

  // 渲染空状态
  const renderEmpty = () => (
    <View className='proposal__empty'>
      <Text className='proposal__empty-icon'>
        {keyword ? '🔍' : '📭'}
      </Text>
      <Text className='proposal__empty-text'>
        {keyword ? '未找到相关赛事' : '暂无赛事'}
      </Text>
    </View>
  )

  // 渲染错误状态
  const renderError = () => (
    <View className='proposal__error'>
      <Text className='proposal__error-icon'>⚠️</Text>
      <Text className='proposal__error-text'>{error}</Text>
      <View className='proposal__error-btn' onClick={() => loadEvents(keyword)}>
        <Text>重新加载</Text>
      </View>
    </View>
  )

  // 渲染加载状态
  const renderLoading = () => (
    <View className='proposal__loading'>
      <Text className='proposal__loading-text'>加载中...</Text>
    </View>
  )

  return (
    <View className='proposal'>
      {/* 头部标题 */}
      <View className='proposal__header'>
        <Text className='proposal__title'>今日方案</Text>
        <Text className='proposal__subtitle'>搜索您感兴趣的赛事</Text>
      </View>

      {/* 搜索栏 */}
      <SearchBar
        value={keyword}
        onSearch={handleSearch}
        onClear={handleClear}
      />

      {/* 内容区域 */}
      <ScrollView
        className='proposal__content'
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
          <View className='proposal__list'>
            {events.map(event => (
              <EventCard key={event.id} event={event} />
            ))}
          </View>
        )}
      </ScrollView>
    </View>
  )
}

