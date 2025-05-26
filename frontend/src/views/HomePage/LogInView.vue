<template>
  <div class="login-container">
    <h2>로그인</h2>
    <form @submit.prevent="onLogIn">
      <input v-model="username" placeholder="아이디" />
      <input v-model="password" type="password" placeholder="비밀번호" />
      <button type="submit">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()
const router = useRouter()

const username = ref('')
const password = ref('')

const onLogIn = async () => {
  try {
    await userStore.logIn({ username: username.value, password: password.value })
    router.push({ name: 'HomeView' })
  } catch (err) {
    console.error('로그인 중 오류:', err)
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 1rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.login-container h2 {
  text-align: center;
  color: #004080;
  margin-bottom: 1rem;
}
.login-container input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.login-container button {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  background-color: #0073e6;
  color: #ffffff;
  font-size: 1rem;
  cursor: pointer;
}
.login-container button:hover {
  background-color: #005bb5;
}
</style>
