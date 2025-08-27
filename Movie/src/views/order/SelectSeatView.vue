<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import apiClient from '@/services/api.ts'

interface MovieInfo { name: string; }
interface ScreenInfo {
  id: number;
  cinema_name: string;
  hall_name: string;
  start_time: string;
  price: number;
  movie: MovieInfo;
}

const route = useRoute()
const screenInfo = ref<ScreenInfo | null>(null)
const isLoading = ref(true)
const errorMessage = ref('')
const seatLayout = ref<number[][]>([])
const selectedSeats = ref<string[]>([])

onMounted(async () => {
  const screenId = route.params.id
  try {
    const [screenResponse, seatsResponse] = await Promise.all([
        apiClient.get(`/screens/${screenId}`),
        apiClient.get(`/screens/${screenId}/seats`)
    ]);
    screenInfo.value = screenResponse.data
    seatLayout.value = seatsResponse.data.seat_layout
  } catch (error) {
    errorMessage.value = '无法加载场次信息，请返回重试。'
  } finally {
    isLoading.value = false
  }
})

const handleSeatClick = (rowIndex: number, colIndex: number) => {
  if (seatLayout.value[rowIndex][colIndex] === 1) return
  const seatId = `${rowIndex + 1}排${colIndex + 1}座`
  const seatStatus = seatLayout.value[rowIndex][colIndex]
  const seatIndex = selectedSeats.value.indexOf(seatId)
  if (seatStatus === 0) {
    if (selectedSeats.value.length >= 4) {
      alert('最多只能选择4个座位')
      return
    }
    seatLayout.value[rowIndex][colIndex] = 2
    selectedSeats.value.push(seatId)
  } else if (seatStatus === 2) {
    seatLayout.value[rowIndex][colIndex] = 0
    if (seatIndex > -1) {
      selectedSeats.value.splice(seatIndex, 1)
    }
  }
}

const totalPrice = computed(() => {
  if (!screenInfo.value) return 0
  return selectedSeats.value.length * screenInfo.value.price
})

const formatTime = (datetime: string) => new Date(datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
</script>

<template>
  <div class="p-4 md:p-8">
    <div v-if="isLoading" class="text-center text-gray-500">正在加载场次信息...</div>
    <div v-if="errorMessage" class="p-4 text-red-700 bg-red-100 rounded-md">{{ errorMessage }}</div>
    
    <div v-if="screenInfo" class="text-center mb-6">
      <h1 class="text-2xl font-bold">{{ screenInfo.movie.name }}</h1>
      <p class="text-gray-600">{{ screenInfo.cinema_name }} {{ screenInfo.hall_name }}</p>
      <p class="text-gray-500">{{ formatTime(screenInfo.start_time) }}</p>
    </div>

    <div v-if="screenInfo" class="flex flex-col items-center">
      <div class="bg-gray-300 w-3/4 h-2 mb-4 rounded text-center text-sm text-gray-600">银幕</div>
      <div class="space-y-2">
            <div v-for="(row, rowIndex) in seatLayout" :key="rowIndex" class="flex space-x-2">
              <div
                v-for="(seat, colIndex) in row"
                :key="colIndex"
                @click="handleSeatClick(rowIndex, colIndex)"
                class="w-8 h-8 rounded-md flex items-center justify-center text-xs cursor-pointer"
                :class="{
                  'bg-gray-200': seat === 0,
                  'bg-red-500 text-white': seat === 1,
                  'bg-green-500 text-white': seat === 2,
                  'pointer-events-none': seat === 1
                }"
              >
                {{ colIndex + 1 }}
              </div>
            </div>
      </div>
    </div>
    
    <div v-if="screenInfo" class="flex justify-center space-x-4 mt-6 text-sm">
      <div class="flex items-center"><div class="w-4 h-4 bg-gray-200 rounded mr-2"></div>可选</div>
      <div class="flex items-center"><div class="w-4 h-4 bg-red-500 rounded mr-2"></div>已售</div>
      <div class="flex items-center"><div class="w-4 h-4 bg-green-500 rounded mr-2"></div>已选</div>
    </div>

    <div v-if="selectedSeats.length > 0" class="mt-8 p-4 bg-white rounded-lg shadow-md">
      <h3 class="font-bold">已选座位</h3>
      <p class="text-gray-600">{{ selectedSeats.join(', ') }}</p>
      <div class="mt-4 flex justify-between items-center">
        <span class="text-xl font-bold">总计：¥{{ totalPrice.toFixed(2) }}</span>
        <router-link
          :to="{ 
            name: 'confirm-order', 
            params: { id: route.params.id }, 
            query: { seats: selectedSeats.join(', '), totalPrice: totalPrice } 
          }"
          class="bg-red-600 text-white font-semibold py-2 px-6 rounded-lg hover:bg-red-700"
        >
          确认选座
        </router-link>
      </div>
    </div>
  </div>
</template>
