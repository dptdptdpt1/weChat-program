import Taro from '@tarojs/taro'
import { post, get, put } from '../utils/request'
import { IUserInfo, IWxLoginRequest } from '../types'

/**
 * 用户认证服务
 */
class AuthService {
  // 本地存储的 key
  private readonly USER_INFO_KEY = 'userInfo'
  private readonly OPEN_ID_KEY = 'openId'

  /**
   * 微信登录
   * @param userProfile 用户信息(可选)
   * @returns 用户信息
   */
  async wxLogin(userProfile?: { nickName?: string; avatarUrl?: string }): Promise<IUserInfo> {
    try {
      // 1. 调用微信登录获取 code
      const loginRes = await Taro.login()
      
      if (!loginRes.code) {
        throw new Error('微信登录失败')
      }

      // 2. 调用后端接口,用 code 换取用户信息
      const loginData: IWxLoginRequest = {
        code: loginRes.code,
        nick_name: userProfile?.nickName,
        avatar_url: userProfile?.avatarUrl
      }

      const userInfo = await post<IUserInfo>('/api/auth/login', loginData, true)

      // 3. 保存用户信息到本地
      this.saveUserInfo(userInfo)

      return userInfo
    } catch (error) {
      console.error('微信登录失败:', error)
      throw error
    }
  }

  /**
   * 获取用户信息
   * @param openId 用户 openId
   * @returns 用户信息
   */
  async getUserInfo(openId: string): Promise<IUserInfo> {
    return get<IUserInfo>('/api/auth/user', { open_id: openId })
  }

  /**
   * 修改用户昵称
   * @param openId 用户 openId
   * @param nickName 新昵称
   * @returns 更新后的用户信息
   */
  async updateNickname(openId: string, nickName: string): Promise<IUserInfo> {
    const userInfo = await put<IUserInfo>(
      `/api/auth/user/nickname?open_id=${openId}&nick_name=${encodeURIComponent(nickName)}`,
      null,
      true
    )
    
    // 更新本地存储
    this.saveUserInfo(userInfo)
    
    return userInfo
  }

  /**
   * 获取用户授权信息
   * @returns 用户授权信息
   */
  async getUserProfile(): Promise<{ nickName: string; avatarUrl: string }> {
    try {
      const res = await Taro.getUserProfile({
        desc: '用于完善用户资料'
      })

      return {
        nickName: res.userInfo.nickName,
        avatarUrl: res.userInfo.avatarUrl
      }
    } catch (error) {
      console.error('获取用户授权失败:', error)
      throw new Error('用户拒绝授权')
    }
  }

  /**
   * 保存用户信息到本地存储
   * @param userInfo 用户信息
   */
  saveUserInfo(userInfo: IUserInfo) {
    try {
      Taro.setStorageSync(this.USER_INFO_KEY, userInfo)
      Taro.setStorageSync(this.OPEN_ID_KEY, userInfo.open_id)
    } catch (error) {
      console.error('保存用户信息失败:', error)
    }
  }

  /**
   * 从本地存储获取用户信息
   * @returns 用户信息或 null
   */
  getLocalUserInfo(): IUserInfo | null {
    try {
      return Taro.getStorageSync(this.USER_INFO_KEY)
    } catch (error) {
      console.error('获取本地用户信息失败:', error)
      return null
    }
  }

  /**
   * 从本地存储获取 openId
   * @returns openId 或 null
   */
  getLocalOpenId(): string | null {
    try {
      return Taro.getStorageSync(this.OPEN_ID_KEY)
    } catch (error) {
      console.error('获取本地 openId 失败:', error)
      return null
    }
  }

  /**
   * 清除本地用户信息
   */
  clearUserInfo() {
    try {
      Taro.removeStorageSync(this.USER_INFO_KEY)
      Taro.removeStorageSync(this.OPEN_ID_KEY)
    } catch (error) {
      console.error('清除用户信息失败:', error)
    }
  }

  /**
   * 检查是否已登录
   * @returns 是否已登录
   */
  isLoggedIn(): boolean {
    return !!this.getLocalOpenId()
  }
}

export default new AuthService()
