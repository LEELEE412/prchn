// src/stores/userStore.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore(
  'user',
  () => {
    const BASE_URL   = 'http://127.0.0.1:8000/api/v1'
    const token      = ref(localStorage.getItem('token') || '')
    const isLogin    = computed(() => !!token.value)
    const subscribed = ref(
      JSON.parse(localStorage.getItem('subscribed') || '[]')
    )

    function _saveToken(val) {
      token.value = val
      localStorage.setItem('token', val)
    }
    function _clearToken() {
      token.value = ''
      localStorage.removeItem('token')
    }
    function _saveSubscribed() {
      localStorage.setItem('subscribed', JSON.stringify(subscribed.value))
    }

    // 회원가입
    async function signUp(payload) {
      const url = `${BASE_URL}/accounts/registration/`
      const res = await axios.post(url, payload)
      return res.data
    }

    // 로그인
    async function logIn(payload) {
      const url = `${BASE_URL}/accounts/login/`
      const res = await axios.post(url, payload)
      _saveToken(res.data.key)
      return res.data
    }

    // 로그아웃
    function logOut() {
      _clearToken()
      subscribed.value = []
      _saveSubscribed()
    }

    // 상품 구독 (가입하기)
    async function subscribe(productId) {
      if (!isLogin.value) {
        throw new Error('로그인 후 이용해주세요.')
      }
      const url = `${BASE_URL}/products/${productId}/subscribe/`
      await axios.post(
        url,
        {},
        { headers: { Authorization: `Token ${token.value}` } }
      )
      // DB PK는 숫자형이므로 Number()로 변환해 저장
      const idNum = Number(productId)
      if (!subscribed.value.includes(idNum)) {
        subscribed.value.push(idNum)
        _saveSubscribed()
      }
    }

    return {
      token,
      isLogin,
      subscribed,
      signUp,
      logIn,
      logOut,
      subscribe,
    }
  },
  {
    persist: {
      key: 'user',
      paths: ['token', 'subscribed'],
    },
  }
)
