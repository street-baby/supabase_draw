import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authApi from '@/api/auth'

interface User {
  id: number
  email: string
  username: string | null
  created_at: string
  last_login: string | null
}

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const loading = ref(false)
  const verificationCodeSent = ref(false)

  // getters
  const isAuthenticated = computed(() => !!token.value)
  const userEmail = computed(() => user.value?.email || '')

  // 从本地存储初始化
  const initializeAuth = async () => {
    const storedToken = localStorage.getItem('token')
    
    if (storedToken) {
      token.value = storedToken
      
      // 尝试获取用户信息
      try {
        const response = await authApi.getUserInfo()
        user.value = response.data.user
      } catch (error) {
        console.error('获取用户信息失败，可能需要重新登录', error)
        logout()
      }
    }
  }

  // 发送验证码
  const sendVerificationCode = async (email: string) => {
    loading.value = true
    
    try {
      await authApi.sendVerificationCode(email)
      verificationCodeSent.value = true
      return true
    } catch (error) {
      console.error('发送验证码失败', error)
      return false
    } finally {
      loading.value = false
    }
  }

  // 使用验证码登录
  const loginWithCode = async (email: string, code: string) => {
    loading.value = true
    
    try {
      const response = await authApi.login(email, code)
      
      // 保存认证数据
      token.value = response.data.token
      user.value = response.data.user
      
      // 存储到localStorage
      localStorage.setItem('token', response.data.token)
      
      return true
    } catch (error) {
      console.error('登录失败', error)
      return false
    } finally {
      loading.value = false
      verificationCodeSent.value = false
    }
  }
  
  // 用户注册
  const register = async (email: string, code: string, password: string) => {
    loading.value = true
    
    try {
      await authApi.register(email, code, password)
      return true
    } catch (error) {
      console.error('注册失败', error)
      return false
    } finally {
      loading.value = false
      verificationCodeSent.value = false
    }
  }
  
  // 用密码登录 (保留旧方法，以防需要)
  const login = async (email: string, password: string) => {
    console.warn('使用密码登录方法已弃用，请使用验证码登录')
    return false
  }
  
  // 登出
  const logout = () => {
    // 清除认证数据
    user.value = null
    token.value = null
    
    // 调用API登出
    authApi.logout()
  }

  return {
    user,
    token,
    loading,
    verificationCodeSent,
    isAuthenticated,
    userEmail,
    login,
    loginWithCode,
    register,
    logout,
    initializeAuth,
    sendVerificationCode
  }
}) 