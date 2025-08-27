<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '@/services/api.ts'
import { useAuthStore } from '@/stores/auth'

// 定义数据类型
interface MovieInfo {
  name: string;
  cover: string;
}
interface ScreenInfo {
  id: number;
  cinema_name: string;
  hall_name: string;
  start_time: string;
  price: number;
  movie: MovieInfo;
}

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const screenInfo = ref<ScreenInfo | null>(null)
const isLoading = ref(true)
const errorMessage = ref('')

// 从路由的查询参数中获取座位和总价信息
const seats = ref(route.query.seats as string || '')
const totalPrice = ref(Number(route.query.totalPrice) || 0)

// 计算已选座位的数量
const selectedSeatsCount = computed(() => seats.value ? seats.value.split(',').length : 0)

onMounted(async () => {
  const screenId = route.params.id
  try {
    const response = await apiClient.get(`/screens/${screenId}`)
    screenInfo.value = response.data
  } catch (error) {
    errorMessage.value = '无法加载订单信息，请返回重试。'
  } finally {
    isLoading.value = false
  }
})

// 处理确认订单的函数
const handleConfirmOrder = async () => {
  if (!screenInfo.value) return

  isLoading.value = true
  errorMessage.value = ''
  
  const result = await authStore.createOrder(
    screenInfo.value.id,
    seats.value,
    totalPrice.value
  )

  isLoading.value = false

  if (result.success) {
    alert('订单创建成功！')
    // 成功后跳转到个人中心页面，未来可以跳转到我的订单页
    router.push('/profile') 
  } else {
    errorMessage.value = result.message || '创建订单失败。'
  }
}
</script>

<template>
  <div class="p-4 md:p-8">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">确认订单信息</h1>
    
    <div v-if="isLoading" class="text-center text-gray-500">正在加载...</div>
    <div v-if="errorMessage" class="p-4 text-red-700 bg-red-100 rounded-md">{{ errorMessage }}</div>

    <div v-if="screenInfo" class="bg-white rounded-lg shadow-md p-6">
      <div class="flex items-center pb-4 border-b">
        <img :src="screenInfo.movie.cover || 'https://via.placeholder.com/100x150'" :alt="screenInfo.movie.name" class="w-16 rounded">
        <div class="ml-4">
          <h2 class="text-xl font-bold">{{ screenInfo.movie.name }}</h2>
          <p class="text-sm text-gray-600">{{ new Date(screenInfo.start_time).toLocaleString() }}</p>
          <p class="text-sm text-gray-500">{{ screenInfo.cinema_name }} {{ screenInfo.hall_name }}</p>
        </div>
      </div>
      
      <div class="py-4 border-b">
        <h3 class="font-semibold">座位</h3>
        <p class="text-gray-800">{{ seats }}</p>
      </div>

      <div class="py-4">
        <div class="flex justify-between items-center">
          <span class="text-gray-600">票价</span>
          <span>{{ selectedSeatsCount }} 张 x ¥{{ screenInfo.price.toFixed(2) }}</span>
        </div>
        <div class="flex justify-between items-center mt-2 font-bold text-xl">
          <span>总计</span>
          <span class="text-red-600">¥{{ totalPrice.toFixed(2) }}</span>
        </div>
      </div>

      <div class="mt-6">
        <button 
          @click="handleConfirmOrder"
          :disabled="isLoading"
          class="w-full bg-red-600 text-white font-semibold py-3 px-4 rounded-lg hover:bg-red-700 disabled:bg-gray-400"
        >
          {{ isLoading ? '正在提交...' : '确认并支付' }}
        </button>
      </div>
    </div>
  </div>
</template>
