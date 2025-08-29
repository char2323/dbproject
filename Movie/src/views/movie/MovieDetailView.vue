
<script setup lang="ts">
import { ref, onMounted } from 'vue'
// 👇 1. Import useRouter to handle navigation
import { useRoute, useRouter, RouterLink } from 'vue-router'
import apiClient from '@/services/api.ts'
import { useAuthStore } from '@/stores/auth'

// --- Type Definitions ---
interface Movie { id: number; name: string; cover: string; description: string; release_date: string; duration_mins: number; }
interface Comment { id: number; content: string; rating: number; create_time: string; user: { username: string }; }

const route = useRoute()
const router = useRouter() // <-- 2. Get the router instance
const authStore = useAuthStore()

// --- Reactive Variables ---
const movie = ref<Movie | null>(null)
const comments = ref<Comment[]>([])
const isLoading = ref(true)
const errorMessage = ref('')
const favoriteStatus = ref(0)
const newCommentContent = ref('')
const newCommentRating = ref(5)
const isSubmittingComment = ref(false)
const movieId = Number(route.params.id)

// --- Data Fetching ---
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

// --- Methods ---
const handleFavorite = async (status: number) => {
  const isCanceling = favoriteStatus.value === status;
  try {
    if (isCanceling) {
      await apiClient.delete(`/favorites/${movieId}`)
      favoriteStatus.value = 0
    } else {
      await apiClient.post('/favorites/', { movie_id: movieId, status: status })
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

// 3. Create a function to go back
const goBack = () => {
  router.push('/') // Navigate to the home page
}
</script>

<template>
  <div class="p-4 md:p-8 bg-gradient-to-br from-purple-700 via-pink-600 to-indigo-700 min-h-screen text-white relative">
    <!-- 👇 4. Add the Back Button here 👇 -->
    <button @click="goBack" class="absolute top-4 left-4 md:top-8 md:left-8 bg-black/30 text-white font-semibold py-2 px-4 rounded-full hover:bg-white/30 transition-colors z-10">
      &lt; 返回
    </button>

    <div v-if="isLoading" class="text-center text-white/70 text-lg mt-20">正在加载详情...</div>
    <div v-if="errorMessage" class="p-4 text-red-200 bg-red-800/30 rounded-md text-center mb-6">{{ errorMessage }}</div>

    <div v-if="movie" class="max-w-5xl mx-auto space-y-12">
      <!-- Movie Info Card -->
      <div class="md:flex md:space-x-8 bg-black/30 p-6 rounded-xl shadow-2xl backdrop-blur-sm">
        <img
          :src="movie.cover || 'https://via.placeholder.com/400x600'"
          :alt="movie.name"
          class="rounded-xl w-full md:w-64 object-cover shadow-lg"
        />
        <div class="mt-4 md:mt-0 flex flex-col flex-1">
          <h1 class="text-4xl font-extrabold">{{ movie.name }}</h1>
          <p class="text-gray-200 mt-2">时长: {{ movie.duration_mins }} 分钟</p>
          <p class="text-gray-200">上映日期: {{ movie.release_date }}</p>
          <p class="mt-4 text-gray-100 flex-grow">{{ movie.description }}</p>

          <div class="mt-6 flex flex-wrap gap-4">
            <button
              @click="handleFavorite(1)"
              class="flex-1 py-2 px-4 rounded-lg font-semibold transition transform hover:scale-105"
              :class="favoriteStatus === 1 ? 'bg-yellow-400 text-black' : 'bg-white/30 hover:bg-yellow-500/70'"
            >
              {{ favoriteStatus === 1 ? '已想看' : '想看' }}
            </button>
            <button
              @click="handleFavorite(2)"
              class="flex-1 py-2 px-4 rounded-lg font-semibold transition transform hover:scale-105"
              :class="favoriteStatus === 2 ? 'bg-green-500 text-white' : 'bg-white/30 hover:bg-green-500/70'"
            >
              {{ favoriteStatus === 2 ? '已看过' : '看过' }}
            </button>
          </div>

          <router-link
            :to="`/movie/${movie.id}/select-screen`"
            class="mt-4 block text-center bg-red-600 font-bold py-3 px-4 rounded-full hover:bg-red-700 transition transform hover:scale-105"
          >
            立即购票
          </router-link>
        </div>
      </div>

      <!-- Comments Section -->
      <div>
        <h2 class="text-3xl font-bold mb-6 border-b border-white/30 pb-2">观众评论</h2>

        <!-- Post Comment -->
        <div v-if="authStore.isAuthenticated" class="bg-black/30 p-4 rounded-xl backdrop-blur-sm mb-6 shadow-lg">
          <h3 class="font-semibold mb-2">发表你的看法</h3>
          <textarea
            v-model="newCommentContent"
            rows="3"
            class="w-full p-2 rounded-lg bg-white/10 border border-white/30 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-purple-400"
            placeholder="说点什么吧..."
          ></textarea>
          <div class="flex justify-between items-center mt-2">
            <div>
              <label class="mr-2">评分:</label>
              <select v-model.number="newCommentRating" class="p-1 rounded-lg bg-white/10 border border-white/30 text-white">
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
              class="bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 px-6 rounded-full disabled:bg-gray-400 transition transform hover:scale-105"
            >
              {{ isSubmittingComment ? '提交中...' : '发表' }}
            </button>
          </div>
        </div>

        <!-- Comments List -->
        <div v-if="comments.length > 0" class="space-y-4">
          <div v-for="comment in comments" :key="comment.id" class="bg-black/30 p-4 rounded-xl backdrop-blur-sm shadow-md">
            <div class="flex justify-between items-center">
              <span class="font-semibold">{{ comment.user.username }}</span>
              <span class="text-yellow-400 font-bold">评分: {{ comment.rating }}/5</span>
            </div>
            <p class="text-gray-200 mt-2">{{ comment.content }}</p>
            <p class="text-xs text-gray-400 text-right mt-2">{{ new Date(comment.create_time).toLocaleString() }}</p>
          </div>
        </div>
        <div v-else class="text-center text-white/70 py-8">
          暂无评论，快来抢沙发吧！
        </div>
      </div>
    </div>
  </div>
</template>
