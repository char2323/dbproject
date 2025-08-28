<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api.ts'

const username = ref('')
const password = ref('')
const phone = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

const router = useRouter()

const handleSignup = async () => {
  if (!username.value || !password.value || !phone.value) {
    errorMessage.value = '所有字段均为必填项'
    return
  }
  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    // 调用我们早已创建好的 POST /api/users/ 接口
    await apiClient.post('/users/', {
      username: username.value,
      password: password.value,
      phone: phone.value
    })

    successMessage.value = '注册成功！正在跳转到登录页面...'

    // 注册成功后，等待2秒，然后自动跳转到登录页
    setTimeout(() => {
      router.push('/signin')
    }, 2000)

  } catch (error: any) {
    errorMessage.value = error.response?.data?.message || '注册失败，请检查您的输入'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-800">创建新账户</h1>
        <p class="mt-2 text-gray-500">加入猿眼电影</p>
      </div>

      <div v-if="successMessage" class="p-3 text-sm text-green-700 bg-green-100 rounded-md">
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="p-3 text-sm text-red-700 bg-red-100 rounded-md">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleSignup" class="space-y-6">
        <div>
          <label for="username" class="text-sm font-medium text-gray-700">用户名</label>
          <input v-model="username" id="username" type="text" required class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500" placeholder="请输入用户名">
        </div>

        <div>
          <label for="password" class="text-sm font-medium text-gray-700">密码</label>
          <input v-model="password" id="password" type="password" required class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500" placeholder="请输入密码 (至少6位)">
        </div>

        <div>
          <label for="phone" class="text-sm font-medium text-gray-700">手机号</label>
          <input v-model="phone" id="phone" type="tel" required class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500" placeholder="请输入手机号">
        </div>

        <div>
          <button type="submit" :disabled="isLoading" class="w-full px-4 py-2 font-semibold text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-gray-400">
            {{ isLoading ? '注册中...' : '注 册' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
