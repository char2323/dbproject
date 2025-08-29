
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import apiClient from '@/services/api.ts'

interface Coupon {
  id: number;
  name: string;
  discount: number;
  min_spend: number;
  expiry_date: string;
  is_used: boolean;
}

const coupons = ref<Coupon[]>([])
const isLoading = ref(true)
const errorMessage = ref('')

onMounted(async () => {
  try {
    const response = await apiClient.get('/coupons/')
    coupons.value = response.data
  } catch {
    errorMessage.value = '无法加载优惠券列表，请稍后再试。'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="p-4 md:p-8">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">我的优惠券</h1>

    <div v-if="isLoading" class="text-center text-gray-500">正在加载...</div>
    <div v-else-if="errorMessage" class="p-4 text-red-700 bg-red-100 rounded-md">{{ errorMessage }}</div>

    <div v-else-if="coupons.length > 0" class="space-y-4">
      <div v-for="coupon in coupons" :key="coupon.id"
           class="p-4 bg-white rounded-xl shadow-md border-l-4 transition hover:shadow-lg"
           :class="coupon.is_used ? 'border-gray-300 opacity-70' : 'border-yellow-400'">
        <div class="flex justify-between items-center">
          <div>
            <h3 class="font-bold text-lg text-gray-800">{{ coupon.name }}</h3>
            <p class="text-sm text-gray-600">满 {{ coupon.min_spend }} 元可用</p>
            <p class="text-xs text-gray-400 mt-2">有效期至：{{ new Date(coupon.expiry_date).toLocaleDateString() }}</p>
          </div>
          <div class="text-right">
            <span class="text-2xl font-bold text-red-600"><span class="text-lg">¥</span>{{ coupon.discount }}</span>
            <p class="text-sm text-red-500">{{ coupon.is_used ? '已使用' : '优惠券' }}</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center text-gray-500 mt-8">您当前没有任何优惠券</div>
  </div>
</template>
