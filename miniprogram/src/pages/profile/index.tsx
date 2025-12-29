import { View, Image, Text, Button, Input } from '@tarojs/components'
import { useState } from 'react'
import Taro, { useLoad } from '@tarojs/taro'
import { QRCodeModal } from '../../components'
import { authService, configService } from '../../services'
import { IUserInfo, ICustomerService } from '../../types'
import './index.scss'

export default function Profile() {
  const [userInfo, setUserInfo] = useState<IUserInfo | null>(null)
  const [customerService, setCustomerService] = useState<ICustomerService | null>(null)
  const [showQRCode, setShowQRCode] = useState(false)
  const [isAuthorized, setIsAuthorized] = useState(false)
  const [isEditingNickname, setIsEditingNickname] = useState(false)
  const [newNickname, setNewNickname] = useState('')

  // 加载用户信息
  const loadUserInfo = () => {
    const localUserInfo = authService.getLocalUserInfo()
    if (localUserInfo) {
      setUserInfo(localUserInfo)
      setIsAuthorized(true)
    }
  }

  // 加载客服配置
  const loadCustomerService = async () => {
    try {
      const csData = await configService.getCustomerService()
      setCustomerService(csData)
    } catch (error) {
      console.error('加载客服配置失败:', error)
    }
  }

  // 页面加载
  useLoad(() => {
    console.log('个人中心页面加载')
    loadUserInfo()
    loadCustomerService()
  })

  // 处理授权登录
  const handleAuthorize = async () => {
    try {
      // 获取用户授权信息
      const userProfile = await authService.getUserProfile()
      
      // 调用微信登录
      const userData = await authService.wxLogin(userProfile)
      
      setUserInfo(userData)
      setIsAuthorized(true)
      
      Taro.showToast({
        title: '登录成功',
        icon: 'success'
      })
    } catch (error: any) {
      console.error('授权登录失败:', error)
      
      if (error.message !== '用户拒绝授权') {
        Taro.showToast({
          title: '登录失败',
          icon: 'none'
        })
      }
    }
  }

  // 显示客服二维码
  const handleShowQRCode = () => {
    if (customerService) {
      setShowQRCode(true)
    } else {
      Taro.showToast({
        title: '客服信息加载中',
        icon: 'none'
      })
    }
  }

  // 关闭二维码弹窗
  const handleCloseQRCode = () => {
    setShowQRCode(false)
  }

  // 开始编辑昵称
  const handleStartEditNickname = () => {
    if (userInfo) {
      setNewNickname(userInfo.nick_name)
      setIsEditingNickname(true)
    }
  }

  // 保存昵称
  const handleSaveNickname = async () => {
    if (!userInfo) return

    const trimmedNickname = newNickname.trim()
    
    // 验证昵称
    if (!trimmedNickname) {
      Taro.showToast({
        title: '昵称不能为空',
        icon: 'none'
      })
      return
    }

    if (trimmedNickname.length > 20) {
      Taro.showToast({
        title: '昵称不能超过20个字符',
        icon: 'none'
      })
      return
    }

    try {
      const updatedUser = await authService.updateNickname(userInfo.open_id, trimmedNickname)
      setUserInfo(updatedUser)
      setIsEditingNickname(false)
      
      Taro.showToast({
        title: '昵称修改成功',
        icon: 'success'
      })
    } catch (error) {
      console.error('修改昵称失败:', error)
    }
  }

  // 取消编辑昵称
  const handleCancelEditNickname = () => {
    setIsEditingNickname(false)
    setNewNickname('')
  }

  return (
    <View className='profile'>
      {/* 用户信息区域 */}
      <View className='profile__header'>
        <View className='profile__user'>
          {/* 头像 */}
          <Image
            className='profile__avatar'
            src={userInfo?.avatar_url || 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="200"%3E%3Crect fill="%23ddd" width="200" height="200"/%3E%3Ctext fill="%23999" font-family="sans-serif" font-size="60" dy="10.5" font-weight="bold" x="50%25" y="50%25" text-anchor="middle"%3E%E6%9C%AA%E7%99%BB%E5%BD%95%3C/text%3E%3C/svg%3E'}
            mode='aspectFill'
          />
          
          {/* 昵称 */}
          <View className='profile__info'>
            {!isEditingNickname ? (
              <>
                <Text className='profile__nickname'>
                  {userInfo?.nick_name || '未登录'}
                </Text>
                {isAuthorized && (
                  <Text 
                    className='profile__edit-btn'
                    onClick={handleStartEditNickname}
                  >
                    编辑昵称
                  </Text>
                )}
              </>
            ) : (
              <View className='profile__nickname-edit'>
                <Input
                  className='profile__nickname-input'
                  value={newNickname}
                  onInput={(e) => setNewNickname(e.detail.value)}
                  placeholder='请输入昵称'
                  maxlength={20}
                />
                <View className='profile__nickname-actions'>
                  <Text 
                    className='profile__nickname-action profile__nickname-action--cancel'
                    onClick={handleCancelEditNickname}
                  >
                    取消
                  </Text>
                  <Text 
                    className='profile__nickname-action profile__nickname-action--save'
                    onClick={handleSaveNickname}
                  >
                    保存
                  </Text>
                </View>
              </View>
            )}
            {!isAuthorized && (
              <Text className='profile__tip'>点击下方按钮授权登录</Text>
            )}
          </View>
        </View>

        {/* 授权按钮 */}
        {!isAuthorized && (
          <Button
            className='profile__auth-btn'
            onClick={handleAuthorize}
          >
            微信授权登录
          </Button>
        )}
      </View>

      {/* 功能菜单 */}
      <View className='profile__menu'>
        {/* 我的客服 */}
        <View className='profile__menu-item' onClick={handleShowQRCode}>
          <View className='profile__menu-icon'>💬</View>
          <View className='profile__menu-content'>
            <Text className='profile__menu-title'>我的客服</Text>
            <Text className='profile__menu-desc'>联系客服获取帮助</Text>
          </View>
          <View className='profile__menu-arrow'>›</View>
        </View>

        {/* 联系我们 */}
        <View className='profile__menu-item' onClick={handleShowQRCode}>
          <View className='profile__menu-icon'>📞</View>
          <View className='profile__menu-content'>
            <Text className='profile__menu-title'>联系我们</Text>
            <Text className='profile__menu-desc'>扫码添加客服微信</Text>
          </View>
          <View className='profile__menu-arrow'>›</View>
        </View>
      </View>

      {/* 客服二维码弹窗 */}
      {customerService && (
        <QRCodeModal
          visible={showQRCode}
          qrCodeUrl={customerService.qr_code_url}
          onClose={handleCloseQRCode}
        />
      )}
    </View>
  )
}

