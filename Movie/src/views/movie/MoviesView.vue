<script setup lang="ts">
import { ref, onMounted } from 'vue'
import apiClient from '@/services/api.ts'

// 定义电影数据的类型
interface Movie {
  id: number;
  name: string;
  cover: string;
  description: string;
}

const movies = ref<Movie[]>([])
const isLoading = ref(true)
const errorMessage = ref('')

// onMounted 是一个生命周期钩子，在组件挂载到页面后执行
onMounted(async () => {
  try {
    const response = await apiClient.get('/movies/')
    console.log('从后端获取到的原始数据:', response.data)
    movies.value = response.data
  } catch (error) {
    errorMessage.value = '无法加载电影列表，请稍后再试。'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="p-4 md:p-8">
    <h1 class="text-3xl font-bold mb-6 text-gray-800">正在热映</h1>

    <div v-if="isLoading" class="text-center text-gray-500">
      正在加载电影...
    </div>

    <div v-if="errorMessage" class="p-4 text-red-700 bg-red-100 rounded-md">
      {{ errorMessage }}
    </div>

    <div v-if="!isLoading && !errorMessage" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <router-link
        v-for="movie in movies"
        :key="movie.id"
        :to="`/movie/${movie.id}`"
      >
        <div class="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer hover:shadow-xl transition-shadow h-full">
          <img :src="movie.cover || 'https://via.placeholder.com/400x600'" :alt="movie.name" class="w-full h-auto object-cover">
          <div class="p-4">
            <h3 class="font-bold text-lg truncate">{{ movie.name }}</h3>
            <p class="text-gray-600 text-sm mt-1 truncate">{{ movie.description }}</p>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

