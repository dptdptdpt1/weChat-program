import { View, Image, Text } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { getImageUrl } from '../../utils/request'
import './index.scss'

interface QRCodeModalProps {
  visible: boolean
  qrCodeUrl: string
  onClose: () => void
}

/**
 * 客服二维码弹窗组件
 * 显示客服二维码图片,支持长按保存图片
 */
export default function QRCodeModal({
  visible,
  qrCodeUrl,
  onClose
}: QRCodeModalProps) {
  if (!visible) {
    return null
  }

  // 处理长按保存图片
  const handleLongPress = () => {
    Taro.showModal({
      title: '保存二维码',
      content: '是否保存二维码到相册?',
      success: (res) => {
        if (res.confirm) {
          saveImage()
        }
      }
    })
  }

  // 保存图片到相册
  const saveImage = async () => {
    try {
      // 获取完整的图片 URL
      const fullUrl = getImageUrl(qrCodeUrl)
      
      // 下载图片
      const downloadRes = await Taro.downloadFile({
        url: fullUrl
      })

      if (downloadRes.statusCode === 200) {
        // 保存到相册
        await Taro.saveImageToPhotosAlbum({
          filePath: downloadRes.tempFilePath
        })

        Taro.showToast({
          title: '保存成功',
          icon: 'success'
        })
      } else {
        throw new Error('下载失败')
      }
    } catch (error: any) {
      console.error('保存图片失败:', error)
      
      if (error.errMsg && error.errMsg.includes('auth deny')) {
        // 用户拒绝授权
        Taro.showModal({
          title: '需要授权',
          content: '请在设置中允许访问相册',
          confirmText: '去设置',
          success: (res) => {
            if (res.confirm) {
              Taro.openSetting()
            }
          }
        })
      } else {
        Taro.showToast({
          title: '保存失败',
          icon: 'none'
        })
      }
    }
  }

  // 处理遮罩点击
  const handleMaskClick = () => {
    onClose()
  }

  // 阻止内容区域点击冒泡
  const handleContentClick = (e: any) => {
    e.stopPropagation()
  }

  return (
    <View className='qrcode-modal' onClick={handleMaskClick}>
      <View className='qrcode-modal__content' onClick={handleContentClick}>
        {/* 标题 */}
        <View className='qrcode-modal__title'>
          <Text>联系客服</Text>
        </View>

        {/* 二维码图片 */}
        <View className='qrcode-modal__qrcode' onLongPress={handleLongPress}>
          <Image
            className='qrcode-modal__image'
            src={getImageUrl(qrCodeUrl)}
            mode='aspectFit'
            showMenuByLongpress
          />
        </View>

        {/* 提示文字 */}
        <View className='qrcode-modal__tip'>
          <Text>长按二维码保存到相册</Text>
        </View>

        {/* 关闭按钮 */}
        <View className='qrcode-modal__close' onClick={onClose}>
          <Text>✕</Text>
        </View>
      </View>
    </View>
  )
}
