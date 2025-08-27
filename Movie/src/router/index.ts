import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import SigninView from '@/views/auth/SigninView.vue'
import MoviesView from '@/views/movie/MoviesView.vue'
import ProfileView from '@/views/profile/ProfileView.vue'
import MovieDetailView from '@/views/movie/MovieDetailView.vue'
import SelectScreenView from '@/views/order/SelectScreenView.vue'
import SelectSeatView from '@/views/order/SelectSeatView.vue'
import ConfirmOrderView from '@/views/order/ConfirmOrderView.vue'
import MyOrdersView from '@/views/profile/MyOrdersView.vue'
import MyCouponsView from '@/views/profile/MyCouponsView.vue'
import MyFavoritesView from '@/views/profile/MyFavoritesView.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView,
      children: [
        { path: '', name: 'movies', component: MoviesView },
        { path: 'profile', name: 'profile', component: ProfileView }
      ]
    },
    {
      path: '/signin',
      name: 'signin',
      component: SigninView
    },
    {
      path: '/movie/:id',
      name: 'movie-detail',
      component: MovieDetailView
    },
    {
      path: '/movie/:id/select-screen',
      name: 'select-screen',
      component: SelectScreenView
    },
    {
      path: '/screen/:id/select-seat',
      name: 'select-seat',
      component: SelectSeatView
    },
    {
      path: '/screen/:id/confirm',
      name: 'confirm-order',
      component: ConfirmOrderView
    },
    {
      path: '/profile/orders',
      name: 'my-orders',
      component: MyOrdersView
    },
    {
      path: '/profile/coupons',
      name: 'my-coupons',
      component: MyCouponsView
    },
    {
      path: '/profile/favorites',
      name: 'my-favorites',
      component: MyFavoritesView
    }
  ]
})

// 全局前置路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const publicPages = ['signin']
  const authRequired = !publicPages.includes(to.name as string)

  if (authRequired && !authStore.isAuthenticated) {
    return next({ name: 'signin' })
  }

  next()
})

export default router
