
<script setup lang="ts">
import { RouterView, useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Home, User, LogOut } from 'lucide-vue-next' // 使用图标库

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/signin')
}

// 判断当前路由是否活跃
const isActive = (path: string) => route.path === path
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <main class="flex-1 pb-20">
      <RouterView />
    </main>

    <footer class="fixed bottom-0 left-0 right-0 bg-white border-t shadow-md">
      <nav class="flex justify-around">
        <router-link
          to="/"
          class="flex flex-col items-center justify-center py-2 text-gray-500 hover:text-indigo-600 transition-colors duration-200"
          :class="{ 'text-indigo-600 font-semibold': isActive('/') }"
        >
          <Home class="w-5 h-5 mb-1" />
          <span class="text-xs">电影资讯</span>
        </router-link>

        <router-link
          to="/profile"
          class="flex flex-col items-center justify-center py-2 text-gray-500 hover:text-indigo-600 transition-colors duration-200"
          :class="{ 'text-indigo-600 font-semibold': isActive('/profile') }"
        >
          <User class="w-5 h-5 mb-1" />
          <span class="text-xs">个人中心</span>
        </router-link>

        <button
          @click="handleLogout"
          class="flex flex-col items-center justify-center py-2 text-gray-500 hover:text-red-500 transition-colors duration-200"
        >
          <LogOut class="w-5 h-5 mb-1" />
          <span class="text-xs">退出登录</span>
        </button>
      </nav>
    </footer>
  </div>
</template>

<style scoped>
footer nav > * {
  flex: 1; /* 平分宽度 */
}
button {
  background: none;
  border: none;
  outline: none;
}
</style>
