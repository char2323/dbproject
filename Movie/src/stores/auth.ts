import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@/services/api.ts'

// 使用 defineStore 创建一个 store
export const useAuthStore = defineStore('auth', () => {
  // state: 使用 ref() 定义状态
  const user = ref(null)
  const isAuthenticated = ref(false)

  // action: 定义一个登录的 action
  async function login(username, password) {
    try {
      // 调用我们创建的 apiClient 来发送 POST 请求到后端的 /session/login
      const response = await apiClient.post('/session/login', {
        username: username,
        password: password
      })

      // 登录成功，更新 state
      user.value = response.data
      isAuthenticated.value = true

      // 返回成功结果
      return { success: true }
    } catch (error: any) {
      // 登录失败，重置 state
      user.value = null
      isAuthenticated.value = false

      // 返回失败结果和错误信息
      const errorMessage = error.response?.data?.message || '登录时发生未知错误'
      return { success: false, message: errorMessage }
    }
  }

  // action: 定义一个退出登录的 action
  async function logout() {
    await apiClient.post('/session/logout')
    user.value = null
    isAuthenticated.value = false
  }
  
  async function createOrder(screenId: number, seats: string, totalPrice: number) {
    if (!isAuthenticated.value) {
      return { success: false, message: 'User is not logged in.' }
    }
    try {
      const response = await apiClient.post('/orders/', {
        screen_id: screenId,
        seats: seats,
        total_price: totalPrice,
      })
      return { success: true, order: response.data }
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Failed to create order.'
      return { success: false, message: errorMessage }
    }
  }

  // 将 state 和 actions return 出去，以便组件中使用
  return { user, isAuthenticated, login, logout, createOrder }
})
