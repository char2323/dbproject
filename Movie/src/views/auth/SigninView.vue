<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // 导入我们创建的 auth store

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const router = useRouter()
const authStore = useAuthStore() // 获取 auth store 的实例

const handleLogin = async () => {
  if (!username.value || !password.value) {
    errorMessage.value = '用户名和密码不能为空'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  // 调用 auth store 中的 login action
  const result = await authStore.login(username.value, password.value)

  isLoading.value = false

  if (result.success) {
    // 登录成功，跳转到首页
    console.log('登录成功!', authStore.user)
    router.push('/')
  } else {
    // 登录失败，显示后端返回的错误信息
    errorMessage.value = result.message || '登录失败'
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-800">猿眼电影</h1>
        <p class="mt-2 text-gray-500">登录您的账户</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="username" class="text-sm font-medium text-gray-700">用户名</label>
          <input
            v-model="username"
            id="username"
            name="username"
            type="text"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="请输入用户名"
          />
        </div>

        <div>
          <label for="password" class="text-sm font-medium text-gray-700">密码</label>
          <input
            v-model="password"
            id="password"
            name="password"
            type="password"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="请输入密码"
          />
        </div>

        <div v-if="errorMessage" class="p-3 text-sm text-red-700 bg-red-100 rounded-md">
          {{ errorMessage }}
        </div>

        <div>
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full px-4 py-2 font-semibold text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-gray-400"
          >
            {{ isLoading ? '登录中...' : '登 录' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
