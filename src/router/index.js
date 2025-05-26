import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomePage/HomeView.vue'
import ProductsListView from '@/views/Product/ProductsListView.vue'
import MyProductsView from '@/views/Product/MyProductsView.vue'
import LogInView from '@/views/HomePage/LogInView.vue'
import SignUpView from '@/views/HomePage/SignUpView.vue'
import { useUserStore } from '@/stores/userStore'
import AllDetailsView from '@/views/Product/AllDetailsView.vue'
import BankSearchView from '@/views/BankSearchView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ProfileEdit from '@/views/ProfileEditView.vue'
import UserProfileView from '@/views/UserProfileView.vue'

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
    path: '/my-products',
    name: 'MyProducts',
    component: MyProductsView,
    meta: { requiresAuth: true }
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
  },
  {
    path: '/all-details',
    name: 'AllDetails',
    component: AllDetailsView,
  },
  {
    path: '/bank-search',
    name: 'BankSearch',
    component: BankSearchView
  },
  { 
    path: '/profile',      
    name: 'Profile',     
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  { 
    path: '/profile/edit', 
    name: 'ProfileEdit', 
    component: ProfileEdit,
    meta: { requiresAuth: true }
  },
  { 
    path: '/users/:username', 
    name: 'UserProfile', 
    component: UserProfileView 
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLogin) {
    next({ name: 'LogInView' })
  } else {
    next()
  }
})

export default router