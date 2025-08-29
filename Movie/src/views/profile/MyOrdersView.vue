
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import apiClient from '@/services/api.ts'

interface ScreenInfo {
  cinema_name: string;
  hall_name: string;
  start_time: string;
}
interface Order {
  id: number;
  order_number: string;
  seats: string;
  total_price: number;
  status: number;
  movie: { name: string };
  screen: ScreenInfo;
}

const orders = ref<Order[]>([])
const isLoading = ref(true)
const errorMessage = ref('')

onMounted(async () => {
  try {
    const response = await apiClient.get('/orders/')
    orders.value = response.data
  } catch {
    errorMessage.value = '无法加载订单列表，请稍后再试。'
  } finally {
    isLoading.value = false
  }
})

const getStatusText = (status: number) => {
  switch (status) {
    case 0: return '待支付'
    case 1: return '待观影'
    case 2: return '已完成'
    case 3: return '已取消'
    default: return '未知状态'
  }
}
</script>

<template>
  <div class="p-4 md:p-8">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">我的订单</h1>

    <div v-if="isLoading" class="text-center text-gray-500">正在加载订单...</div>
    <div v-else-if="errorMessage" class="p-4 text-red-700 bg-red-100 rounded-md">{{ errorMessage }}</div>

    <div v-else-if="orders.length > 0" class="space-y-4">
      <div v-for="order in orders" :key="order.id"
           class="p-4 bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow">
        <div class="flex justify-between items-center border-b pb-2 mb-2">
          <h3 class="font-bold text-lg text-gray-800">{{ order.movie.name }}</h3>
          <span class="text-sm font-semibold"
            :class="{
              'text-yellow-600': order.status === 0,
              'text-green-600': order.status === 1,
              'text-gray-500': order.status > 1
            }">
            {{ getStatusText(order.status) }}
          </span>
        </div>
        <div class="space-y-1 text-sm text-gray-600">
          <p>{{ order.screen.cinema_name }} · {{ order.screen.hall_name }}</p>
          <p>{{ new Date(order.screen.start_time).toLocaleString() }}</p>
          <p>座位：{{ order.seats }}</p>
        </div>
        <p class="text-right font-bold text-gray-800 mt-2">总计：¥{{ order.total_price.toFixed(2) }}</p>
      </div>
    </div>

    <div v-else class="text-center text-gray-500 mt-8">
      您还没有任何订单
    </div>
  </div>
</template>
