import axios from 'axios'

// 创建一个 axios 实例
const apiClient = axios.create({
  // 我们的后端 API 基础 URL
  baseURL: 'http://127.0.0.1:5000/api',
  // 允许跨域请求携带 cookie
  withCredentials: true
})

// 你可以在这里添加拦截器等，用于处理请求前和响应后的逻辑
// 例如，统一处理错误信息

export default apiClient
