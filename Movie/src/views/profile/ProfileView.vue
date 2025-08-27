<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { RouterLink } from 'vue-router'

const authStore = useAuthStore()
// 为空头像提供一个默认图片
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
</script>

<template>
  <div class="p-4 md:p-8">
    <div class="p-6 bg-white rounded-lg shadow-md flex items-center space-x-4">
      <img
        :src="authStore.user?.avatar || defaultAvatar"
        alt="User Avatar"
        class="w-16 h-16 rounded-full border-2 border-gray-200"
      >
      <div>
        <h2 class="text-2xl font-bold text-gray-800">{{ authStore.user?.username }}</h2>
        <p class="text-gray-500">{{ authStore.user?.phone }}</p>
      </div>
    </div>

    <div class="mt-8 bg-white rounded-lg shadow-md">
      <ul class="divide-y divide-gray-200">
        <router-link to="/profile/orders" custom v-slot="{ navigate }">
          <li @click="navigate" role="link" class="p-4 flex justify-between items-center cursor-pointer hover:bg-gray-50">
            <span>我的订单</span>
            <span>&gt;</span>
          </li>
        </router-link>

        <router-link to="/profile/coupons" custom v-slot="{ navigate }">
          <li @click="navigate" role="link" class="p-4 flex justify-between items-center cursor-pointer hover:bg-gray-50">
            <span>我的优惠券</span>
            <span>&gt;</span>
          </li>
        </router-link>

        <router-link to="/profile/favorites" custom v-slot="{ navigate }">
          <li @click="navigate" role="link" class="p-4 flex justify-between items-center cursor-pointer hover:bg-gray-50">
            <span>想看的电影</span>
            <span>&gt;</span>
          </li>
        </router-link>
        
        <router-link to="/profile/favorites" custom v-slot="{ navigate }">
          <li @click="navigate" role="link" class="p-4 flex justify-between items-center cursor-pointer hover:bg-gray-50">
            <span>看过的电影</span>
            <span>&gt;</span>
          </li>
        </router-link>
      </ul>
    </div>
  </div>
</template>
