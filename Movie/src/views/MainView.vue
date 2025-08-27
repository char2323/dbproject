<script setup lang="ts">
import { RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = async () => {
  await authStore.logout()
  // 退出登录后跳转到登录页
  router.push('/signin')
}
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <main class="flex-1 pb-16">
      <RouterView />
    </main>

    <footer class="fixed bottom-0 left-0 right-0 bg-white border-t">
      <nav class="flex justify-around p-2">
        <router-link to="/" class="text-center text-gray-700 hover:text-indigo-600">
          <span class="block text-xs">电影资讯</span>
        </router-link>
        <router-link to="/profile" class="text-center text-gray-700 hover:text-indigo-600">
          <span class="block text-xs">个人中心</span>
        </router-link>
        <button @click="handleLogout" class="text-center text-gray-700 hover:text-indigo-600">
          <span class="block text-xs">退出登录</span>
        </button>
      </nav>
    </footer>
  </div>
</template>
