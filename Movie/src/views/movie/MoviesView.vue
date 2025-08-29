
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import apiClient from '@/services/api.ts'

interface Movie {
  id: number;
  name: string;
  cover: string;
  description: string;
}

const movies = ref<Movie[]>([])
const searchQuery = ref('') // 搜索关键字
const isLoading = ref(true)
const errorMessage = ref('')

onMounted(async () => {
  try {
    const response = await apiClient.get('/movies/')
    movies.value = response.data
  } catch (error) {
    errorMessage.value = '无法加载电影列表，请稍后再试。'
  } finally {
    isLoading.value = false
  }
})

// 根据搜索框实时过滤电影列表
const filteredMovies = computed(() => {
  if (!searchQuery.value) return movies.value
  return movies.value.filter(movie =>
    movie.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})
</script>

<template>
  <div class="p-4 md:p-8 bg-gradient-to-br from-purple-700 via-pink-600 to-indigo-700 min-h-screen">
    <h1 class="text-4xl font-extrabold mb-6 text-white text-center">正在热映 🎬</h1>

    <!-- 搜索框 -->
    <div class="max-w-md mx-auto mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索电影..."
        class="w-full p-3 rounded-lg text-gray-900 font-medium focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
    </div>

    <div v-if="isLoading" class="text-center text-white/70 text-lg mt-20">
      正在加载电影...
    </div>

    <div v-if="errorMessage" class="p-4 text-red-200 bg-red-800/30 rounded-md text-center mb-6">
      {{ errorMessage }}
    </div>

    <div v-if="!isLoading && !errorMessage" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <router-link
        v-for="movie in filteredMovies"
        :key="movie.id"
        :to="`/movie/${movie.id}`"
        class="perspective"
      >
        <div class="movie-card group">
          <img
            :src="movie.cover || 'https://via.placeholder.com/400x600'"
            :alt="movie.name"
            class="movie-cover"
          />

          <!-- 悬浮显示简介 -->
          <div class="overlay">
            <h3 class="movie-title">{{ movie.name }}</h3>
            <p class="movie-desc">{{ movie.description }}</p>
            <button class="buy-btn">立即购票</button>
          </div>
        </div>
      </router-link>
    </div>

    <div v-if="!isLoading && !errorMessage && filteredMovies.length === 0" class="text-center text-white/70 mt-20">
      未找到匹配的电影
    </div>
  </div>
</template>

<style scoped>
.perspective {
  perspective: 1000px;
}

.movie-card {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  transform-style: preserve-3d;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
}

.movie-card:hover {
  transform: rotateY(5deg) rotateX(5deg) scale(1.05);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.5);
}

.movie-cover {
  width: 100%;
  height: auto;
  aspect-ratio: 2/3;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  color: white;
  opacity: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 16px;
  transition: opacity 0.3s ease;
}

.movie-card:hover .overlay {
  opacity: 1;
}

.movie-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 6px;
}

.movie-desc {
  font-size: 0.875rem;
  color: #ddd;
  line-clamp: 3;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 12px;
}

.buy-btn {
  background: linear-gradient(90deg, #ff4d6d, #ff6fc7);
  padding: 8px 16px;
  border-radius: 24px;
  font-weight: bold;
  border: none;
  color: white;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.buy-btn:hover {
  transform: scale(1.1);
}
</style>
