<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import apiClient from '@/services/api.ts'

// 定义场次和电影的数据类型
interface Screen {
  id: number;
  cinema_name: string;
  hall_name: string;
  start_time: string;
  price: number;
}
interface Movie {
  id: number;
  name: string;
}

const route = useRoute()
const movie = ref<Movie | null>(null)
const screens = ref<Screen[]>([])
const isLoading = ref(true)
const errorMessage = ref('')

const movieId = route.params.id

onMounted(async () => {
  try {
    // 使用 Promise.all 并行获取电影详情和场次列表
    const [movieResponse, screenResponse] = await Promise.all([
      apiClient.get(`/movies/${movieId}`),
      apiClient.get(`/screens/movie/${movieId}`)
    ]);
    movie.value = movieResponse.data
    screens.value = screenResponse.data
  } catch (error) {
    errorMessage.value = '无法加载场次信息，请稍后再试。'
  } finally {
    isLoading.value = false
  }
})

// 格式化日期和时间
const formatDate = (datetime: string) => new Date(datetime).toLocaleDateString()
const formatTime = (datetime: string) => new Date(datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

</script>

<template>
  <div class="p-4 md:p-8">
    <div v-if="isLoading" class="text-center text-gray-500">正在加载...</div>
    <div v-if="errorMessage" class="p-4 text-red-700 bg-red-100 rounded-md">{{ errorMessage }}</div>
    
    <div v-if="movie">
      <h1 class="text-3xl font-bold text-gray-800">{{ movie.name }}</h1>
      <h2 class="text-xl text-gray-600 mt-2">选择场次</h2>
      
      <div class="mt-6 space-y-4">
        <div v-for="screen in screens" :key="screen.id" class="p-4 bg-white rounded-lg shadow-md flex justify-between items-center">
          <div>
            <p class="text-lg font-semibold">{{ formatTime(screen.start_time) }}</p>
            <p class="text-sm text-gray-500">{{ formatDate(screen.start_time) }}</p>
            <p class="text-sm text-gray-600 mt-1">{{ screen.cinema_name }} - {{ screen.hall_name }}</p>
          </div>
          <div>
            <span class="text-xl font-bold text-red-600">¥{{ screen.price.toFixed(2) }}</span>
            
            <router-link
              :to="`/screen/${screen.id}/select-seat`"
              class="ml-4 bg-red-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-red-700"
            >
              选座购票
            </router-link>

          </div>
        </div>
        <div v-if="!isLoading && screens.length === 0" class="text-center text-gray-500 mt-8">
            <p>该电影今日暂无场次安排</p>
        </div>
      </div>
    </div>
  </div>
</template>
