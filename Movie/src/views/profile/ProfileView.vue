
<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { RouterLink } from 'vue-router'
import { User, Ticket, Star, Film } from 'lucide-vue-next' // 图标库

const authStore = useAuthStore()
// 默认头像
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部背景 -->
    <div class="bg-gradient-to-r from-indigo-500 to-purple-600 h-40 relative">
      <div class="absolute -bottom-12 left-1/2 transform -translate-x-1/2">
        <img
          :src="authStore.user?.avatar || defaultAvatar"
          alt="User Avatar"
          class="w-24 h-24 rounded-full border-4 border-white shadow-lg object-cover"
        />
      </div>
    </div>

    <!-- 用户信息 -->
    <div class="mt-16 text-center">
      <h2 class="text-2xl font-bold text-gray-800">{{ authStore.user?.username }}</h2>
      <p class="text-gray-500">{{ authStore.user?.phone || '暂无绑定手机号' }}</p>
    </div>

    <!-- 功能菜单 -->
    <div class="mt-10 max-w-md mx-auto bg-white rounded-2xl shadow-md overflow-hidden">
      <ul class="divide-y divide-gray-200">
        <router-link to="/profile/orders" custom v-slot="{ navigate }">
          <li @click="navigate" class="p-4 flex justify-between items-center hover:bg-gray-50 cursor-pointer">
            <div class="flex items-center space-x-3">
              <Ticket class="w-5 h-5 text-indigo-500" />
              <span class="text-gray-700 font-medium">我的订单</span>
            </div>
            <span class="text-gray-400">&gt;</span>
          </li>
        </router-link>

        <router-link to="/profile/coupons" custom v-slot="{ navigate }">
          <li @click="navigate" class="p-4 flex justify-between items-center hover:bg-gray-50 cursor-pointer">
            <div class="flex items-center space-x-3">
              <Star class="w-5 h-5 text-yellow-500" />
              <span class="text-gray-700 font-medium">我的优惠券</span>
            </div>
            <span class="text-gray-400">&gt;</span>
          </li>
        </router-link>

        <router-link to="/profile/favorites" custom v-slot="{ navigate }">
          <li @click="navigate" class="p-4 flex justify-between items-center hover:bg-gray-50 cursor-pointer">
            <div class="flex items-center space-x-3">
              <Film class="w-5 h-5 text-pink-500" />
              <span class="text-gray-700 font-medium">想看的电影</span>
            </div>
            <span class="text-gray-400">&gt;</span>
          </li>
        </router-link>

        <router-link to="/profile/favorites" custom v-slot="{ navigate }">
          <li @click="navigate" class="p-4 flex justify-between items-center hover:bg-gray-50 cursor-pointer">
            <div class="flex items-center space-x-3">
              <User class="w-5 h-5 text-green-500" />
              <span class="text-gray-700 font-medium">看过的电影</span>
            </div>
            <span class="text-gray-400">&gt;</span>
          </li>
        </router-link>
      </ul>
    </div>
  </div>
</template>
