<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import apiClient from '@/services/api.ts'
import { useAuthStore } from '@/stores/auth'

// --- 类型定义 ---
interface Movie { id: number; name: string; cover: string; description: string; release_date: string; duration_mins: number; }
interface Comment { id: number; content: string; rating: number; create_time: string; user: { username: string }; }

const route = useRoute()
const authStore = useAuthStore()

// --- 响应式变量 ---
const movie = ref<Movie | null>(null)
const comments = ref<Comment[]>([])
const isLoading = ref(true)
const errorMessage = ref('')
const favoriteStatus = ref(0) // 0: 未操作, 1: 想看, 2: 已看

// 评论表单
const newCommentContent = ref('')
const newCommentRating = ref(5)
const isSubmittingComment = ref(false)

const movieId = Number(route.params.id)

// --- 数据获取 ---
onMounted(async () => {
  try {
    const [movieResponse, statusResponse, commentsResponse] = await Promise.all([
      apiClient.get(`/movies/${movieId}`),
      apiClient.get(`/favorites/status/${movieId}`),
      apiClient.get(`/comments/movie/${movieId}`)
    ]);
    movie.value = movieResponse.data
    favoriteStatus.value = statusResponse.data.status
    comments.value = commentsResponse.data
  } catch (error) {
    errorMessage.value = '无法加载电影详情，请稍后再试。'
  } finally {
    isLoading.value = false
  }
})

// --- 方法 ---
const handleFavorite = async (status: number) => {
  const isCanceling = favoriteStatus.value === status;
  try {
    if (isCanceling) {
      await apiClient.delete(`/favorites/${movieId}`)
      favoriteStatus.value = 0
    } else {
      await apiClient.post('/favorites/', {
        movie_id: movieId,
        status: status
      })
      favoriteStatus.value = status
    }
  } catch (error) {
    alert('操作失败，请重试')
  }
}

const handleSubmitComment = async () => {
  if (!newCommentContent.value || newCommentRating.value < 1) {
    alert('请填写评论内容和评分！')
    return
  }
  isSubmittingComment.value = true
  try {
    const response = await apiClient.post(`/comments/movie/${movieId}`, {
      content: newCommentContent.value,
      rating: newCommentRating.value
    })
    comments.value.unshift(response.data)
    newCommentContent.value = ''
    newCommentRating.value = 5
  } catch (error) {
    alert('发表评论失败，请重试。')
  } finally {
    isSubmittingComment.value = false
  }
}
</script>

<template>
  <div class="p-4 md:p-8">
    <div v-if="isLoading" class="text-center text-gray-500">正在加载详情...</div>
    <div v-if="errorMessage" class="p-4 text-red-700 bg-red-100 rounded-md">{{ errorMessage }}</div>

    <div v-if="movie">
      <div class="max-w-4xl mx-auto">
        <div class="md:flex">
          <div class="md:flex-shrink-0">
            <img :src="movie.cover || 'https://via.placeholder.com/400x600'" :alt="movie.name" class="rounded-lg w-full md:w-64">
          </div>
          <div class="mt-4 md:mt-0 md:ml-6 flex flex-col w-full">
            <h1 class="text-3xl font-bold text-gray-900">{{ movie.name }}</h1>
            <p class="text-gray-600 mt-2">时长: {{ movie.duration_mins }} 分钟</p>
            <p class="text-gray-600">上映日期: {{ movie.release_date }}</p>
            <p class="mt-4 text-gray-700 flex-grow">{{ movie.description }}</p>

            <div class="mt-6 flex space-x-4">
              <button 
                @click="handleFavorite(1)"
                class="flex-1 border py-2 px-4 rounded-lg transition-colors"
                :class="favoriteStatus === 1 ? 'bg-yellow-400 border-yellow-400 text-white' : 'bg-white border-gray-300 hover:bg-gray-100'"
              >
                {{ favoriteStatus === 1 ? '已想看' : '想看' }}
              </button>
              <button 
                @click="handleFavorite(2)"
                class="flex-1 border py-2 px-4 rounded-lg transition-colors"
                :class="favoriteStatus === 2 ? 'bg-green-500 border-green-500 text-white' : 'bg-white border-gray-300 hover:bg-gray-100'"
              >
                {{ favoriteStatus === 2 ? '已看过' : '看过' }}
              </button>
            </div>
            
            <router-link
              :to="`/movie/${movie.id}/select-screen`"
              class="mt-4 block text-center w-full bg-red-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-red-700"
            >
              立即购票
            </router-link>
          </div>
        </div>
      </div>

      <div class="max-w-4xl mx-auto mt-12">
        <h2 class="text-2xl font-bold mb-4 border-b pb-2">观众评论</h2>

        <div v-if="authStore.isAuthenticated" class="bg-white p-4 rounded-lg shadow-md mb-6">
          <h3 class="font-semibold mb-2">发表你的看法</h3>
          <textarea 
            v-model="newCommentContent"
            rows="3"
            class="w-full p-2 border rounded-md"
            placeholder="说点什么吧..."
          ></textarea>
          <div class="flex justify-between items-center mt-2">
            <div>
              <label class="mr-2">评分:</label>
              <select v-model.number="newCommentRating" class="p-1 border rounded-md">
                <option>5</option>
                <option>4</option>
                <option>3</option>
                <option>2</option>
                <option>1</option>
              </select>
            </div>
            <button 
              @click="handleSubmitComment" 
              :disabled="isSubmittingComment"
              class="bg-blue-600 text-white font-semibold py-2 px-6 rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
            >
              {{ isSubmittingComment ? '提交中...' : '发表' }}
            </button>
          </div>
        </div>

        <div v-if="comments.length > 0" class="space-y-4">
          <div v-for="comment in comments" :key="comment.id" class="bg-white p-4 rounded-lg shadow-md">
            <div class="flex justify-between items-center">
              <span class="font-semibold">{{ comment.user.username }}</span>
              <span class="text-yellow-500 font-bold">评分: {{ comment.rating }}/5</span>
            </div>
            <p class="text-gray-700 mt-2">{{ comment.content }}</p>
            <p class="text-xs text-gray-400 text-right mt-2">{{ new Date(comment.create_time).toLocaleString() }}</p>
          </div>
        </div>
        <div v-else class="text-center text-gray-500 py-8">
          <p>暂无评论，快来抢沙发吧！</p>
        </div>
      </div>
    </div>
  </div>
</template>
