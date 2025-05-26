import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from './userStore'

export const useProductStore = defineStore('product', () => {
  const products = ref([])
  const detail   = ref(null)
  const BASE_URL = 'http://127.0.0.1:8000/api/v1/products'

  // 전체 상품 목록 조회
  async function fetchProducts() {
    const res = await axios.get(`${BASE_URL}/`)
    products.value = res.data
  }

  // 단일 상품 상세 조회
  async function fetchProduct(id) {
    const res = await axios.get(`${BASE_URL}/${id}/`)
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
