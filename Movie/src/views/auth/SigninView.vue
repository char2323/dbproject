<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const showPassword = ref(false)

const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  if (!username.value || !password.value) {
    errorMessage.value = '用户名和密码不能为空'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  const result = await authStore.login(username.value, password.value)
  isLoading.value = false

  if (result.success) {
    router.push('/')
  } else {
    errorMessage.value = result.message || '登录失败'
  }
}
</script>

<template>
  <div class="login-bg">
    <main class="card">
      <h1 class="brand">猿眼电影</h1>
      <p class="subtitle">登录您的账户</p>

      <form @submit.prevent="handleLogin" class="form">
        <label class="label">用户名</label>
        <div class="field">
          <input v-model="username" type="text" placeholder="请输入用户名" class="input" required />
        </div>

        <label class="label">密码</label>
        <div class="field">
          <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="请输入密码" class="input" required />
          <button type="button" class="toggle-pass" @click="showPassword = !showPassword">
            {{ showPassword ? '🙈' : '👁️' }}
          </button>
        </div>

        <div v-if="errorMessage" class="error-box">{{ errorMessage }}</div>

        <button type="submit" class="btn" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '登 录' }}
        </button>

        <p class="footnote">
          还没有账号？
          <router-link to="/signup">立即注册</router-link>
        </p>
      </form>
    </main>
  </div>
</template>

<style scoped>
.login-bg {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: url('/src/assets/bg.png') no-repeat center center/cover;
}

.card {
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(12px);
  padding: 40px;
  border-radius: 16px;
  text-align: center;
  width: 360px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.brand {
  font-size: 2rem;
  color: #fff;
  margin-bottom: 10px;
}

.subtitle {
  color: #eee;
  margin-bottom: 20px;
}

.field {
  position: relative;
  margin-bottom: 15px;
}

.input {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: none;
  outline: none;
  background: rgba(255,255,255,0.2);
  color: #fff;
}

.input::placeholder {
  color: #ddd;
}

.toggle-pass {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #fff;
  cursor: pointer;
}

.error-box {
  background: rgba(255,0,0,0.2);
  color: #ff4d4f;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 10px;
}

.btn {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: none;
  background-color: #4cafef;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

.btn:disabled {
  background-color: gray;
  cursor: not-allowed;
}

.footnote {
  margin-top: 15px;
  color: #ccc;
}

.footnote a {
  color: #4cafef;
}
</style>
