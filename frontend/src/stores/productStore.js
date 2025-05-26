import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/axios'
import { useUserStore } from './userStore'

export const useProductStore = defineStore('product', () => {
  const products = ref([])
  const detail = ref(null)

  async function fetchProducts() {
    const res = await api.get('/api/v1/products/')
    products.value = res.data
  }

  async function fetchProduct(id) {
    const res = await api.get(`/api/v1/products/${id}/`)
    detail.value = res.data
  }

  async function subscribe({ productId, term }) {
    const userStore = useUserStore()
    if (!userStore.isLogin) {
      alert('로그인 후 이용해주세요.')
      return
    }
    try {
      await api.post(`/api/v1/products/${productId}/subscribe/`, { term })
      userStore.subscribed.push(Number(productId))
      alert('가입이 완료되었습니다.')
    } catch (err) {
      console.error(err)
      throw err
    }
  }

  async function unsubscribe(productId) {
    const userStore = useUserStore()
    try {
      await api.delete(`/api/v1/products/${productId}/subscribe/`)
      userStore.subscribed = userStore.subscribed.filter(id => id !== Number(productId))
      alert('가입이 취소되었습니다.')
    } catch (err) {
      console.error(err)
      throw err
    }
  }

  return {
    products,
    detail,
    fetchProducts,
    fetchProduct,
    subscribe,
    unsubscribe
  }
})