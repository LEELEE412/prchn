import { createRouter, createWebHistory } from 'vue-router'
import HomeView           from '@/views/HomeView.vue'
import ProductsListView   from '@/views/ProductsListView.vue'
import ProductsDetailView from '@/views/ProductsDetailView.vue'
import MyProductsView     from '@/views/MyProductsView.vue'
import LogInView          from '@/views/LogInView.vue'
import SignUpView         from '@/views/SignUpView.vue'
import { useUserStore }   from '@/stores/userStore'

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
  },
  {
    path: '/products',
    name: 'ProductsList',
    component: ProductsListView
  },
  {
    path: '/products/:id',
    name: 'ProductsDetail',
    component: ProductsDetailView,
    meta: { requiresAuth: true }   // 상세조회(구독) 시 로그인 필요
  },
  {
    path: '/my-products',
    name: 'MyProducts',
    component: MyProductsView
  },
  {
    path: '/login',
    name: 'LogInView',
    component: LogInView
  },
  {
    path: '/signup',
    name: 'SignUpView',
    component: SignUpView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 전역 네비게이션 가드
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLogin) {
    // 로그인 안 된 상태에서 상세조회(구독) 접근 시 로그인 페이지로
    next({ name: 'LogInView' })
  } else {
    next()
  }
})

export default router
