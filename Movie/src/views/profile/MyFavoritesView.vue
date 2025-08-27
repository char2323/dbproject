<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import apiClient from '@/services/api.ts'

interface Favorite {
  movie: {
    id: number;
    name: string;
    cover: string;
  };
  status: number;
}

const favorites = ref<Favorite[]>([])
const isLoading = ref(true)
const errorMessage = ref('')

onMounted(async () => {
  try {
    const response = await apiClient.get('/favorites/')
    favorites.value = response.data
  } catch (error) {
    errorMessage.value = '无法加载列表，请稍后再试。'
  } finally {
    isLoading.value = false
  }
})

const wantToWatchList = computed(() => favorites.value.filter(fav => fav.status === 1))
const haveWatchedList = computed(() => favorites.value.filter(fav => fav.status === 2))
</script>

<template>
  <div class="p-4 md:p-8">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">我的电影收藏</h1>

    <div v-if="isLoading" class="text-center text-gray-500">正在加载...</div>
    <div v-if="errorMessage" class="p-4 text-red-700 bg-red-100 rounded-md">{{ errorMessage }}</div>

    <div v-if="!isLoading">
      <section>
        <h2 class="text-xl font-semibold mb-4 text-gray-700">想看的电影</h2>
        <div v-if="wantToWatchList.length > 0" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <router-link v-for="fav in wantToWatchList" :key="fav.movie.id" :to="`/movie/${fav.movie.id}`">
            <div class="bg-white rounded-lg shadow-md overflow-hidden h-full cursor-pointer hover:shadow-xl transition-shadow">
              <img :src="fav.movie.cover" :alt="fav.movie.name" class="w-full h-auto object-cover">
              <div class="p-2">
                <h3 class="font-semibold text-sm truncate">{{ fav.movie.name }}</h3>
              </div>
            </div>
          </router-link>
        </div>
        <p v-else class="text-gray-500">暂无想看的电影。</p>
      </section>

      <section class="mt-8">
        <h2 class="text-xl font-semibold mb-4 text-gray-700">看过的电影</h2>
        <div v-if="haveWatchedList.length > 0" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <router-link v-for="fav in haveWatchedList" :key="fav.movie.id" :to="`/movie/${fav.movie.id}`">
            <div class="bg-white rounded-lg shadow-md overflow-hidden h-full cursor-pointer hover:shadow-xl transition-shadow">
              <img :src="fav.movie.cover" :alt="fav.movie.name" class="w-full h-auto object-cover">
              <div class="p-2">
                <h3 class="font-semibold text-sm truncate">{{ fav.movie.name }}</h3>
              </div>
            </div>
          </router-link>
        </div>
        <p v-else class="text-gray-500">暂无看过的电影。</p>
      </section>
    </div>
  </div>
</template>
