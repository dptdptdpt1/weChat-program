import { View, Input } from '@tarojs/components'
import { useState, useEffect, useRef } from 'react'
import './index.scss'

interface SearchBarProps {
  placeholder?: string
  value?: string
  onSearch?: (keyword: string) => void
  onClear?: () => void
  debounceTime?: number
}

/**
 * 搜索栏组件
 * 支持实时搜索(debounce 优化)和清空搜索
 */
export default function SearchBar({
  placeholder = '搜索赛事',
  value = '',
  onSearch,
  onClear,
  debounceTime = 500
}: SearchBarProps) {
  const [keyword, setKeyword] = useState(value)
  const timerRef = useRef<NodeJS.Timeout | null>(null)

  // 监听外部 value 变化
  useEffect(() => {
    setKeyword(value)
  }, [value])

  // 处理输入变化
  const handleInput = (e: any) => {
    const newKeyword = e.detail.value
    setKeyword(newKeyword)

    // 清除之前的定时器
    if (timerRef.current) {
      clearTimeout(timerRef.current)
    }

    // 设置新的定时器,实现 debounce
    timerRef.current = setTimeout(() => {
      if (onSearch) {
        onSearch(newKeyword)
      }
    }, debounceTime)
  }

  // 处理清空
  const handleClear = () => {
    setKeyword('')
    
    // 清除定时器
    if (timerRef.current) {
      clearTimeout(timerRef.current)
    }

    // 触发清空回调
    if (onClear) {
      onClear()
    } else if (onSearch) {
      onSearch('')
    }
  }

  // 组件卸载时清除定时器
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current)
      }
    }
  }, [])

  return (
    <View className='search-bar'>
      <View className='search-bar__container'>
        {/* 搜索图标 */}
        <View className='search-bar__icon'>🔍</View>

        {/* 输入框 */}
        <Input
          className='search-bar__input'
          type='text'
          placeholder={placeholder}
          value={keyword}
          onInput={handleInput}
          confirmType='search'
        />

        {/* 清空按钮 */}
        {keyword && (
          <View className='search-bar__clear' onClick={handleClear}>
            ✕
          </View>
        )}
      </View>
    </View>
  )
}
