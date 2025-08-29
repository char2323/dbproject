
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api.ts'

const username = ref('')
const password = ref('')
const phone = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const showPassword = ref(false)

const router = useRouter()

const handleSignup = async () => {
  if (!username.value || !password.value || !phone.value) {
    errorMessage.value = '所有字段均为必填项'
    return
  }
  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await apiClient.post('/users/', {
      username: username.value,
      password: password.value,
      phone: phone.value
    })

    successMessage.value = '注册成功！正在跳转到登录页面...'

    setTimeout(() => {
      router.push('/signin')
    }, 2000)

  } catch (error: any) {
    errorMessage.value = error.response?.data?.message || '注册失败，请检查您的输入'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-bg">
    <main class="card">
      <h1 class="brand">创建新账户</h1>
      <p class="subtitle">加入猿眼电影</p>

      <div v-if="successMessage" class="success-box">{{ successMessage }}</div>
      <div v-if="errorMessage" class="error-box">{{ errorMessage }}</div>

      <form @submit.prevent="handleSignup" class="form">
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

        <label class="label">手机号</label>
        <div class="field">
          <input v-model="phone" type="tel" placeholder="请输入手机号" class="input" required />
        </div>

        <button type="submit" class="btn" :disabled="isLoading">
          {{ isLoading ? '注册中...' : '注 册' }}
        </button>
      </form>
    </main>
  </div>
</template>

<style scoped>
/* 与登录页一致的玻璃态样式 */
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

.success-box {
  background: rgba(0,255,0,0.2);
  color: #00ff88;
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
</style>
