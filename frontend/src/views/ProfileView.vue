<template>
  <div class="profile-card" v-if="user">
    <img :src="user.profile_image || defaultImage" class="avatar" />
    <h2>{{ user.username }}</h2>
    <p>{{ user.email }}</p>
    <p>가입일: {{ new Date(user.date_joined).toLocaleString() }}</p>
    <p>한 줄 소개: {{ user.bio }}</p>
    <p>나이: {{ user.age }}</p>
    <p>보유 금액: {{ user.current_balance }}</p>
    <p>연봉: {{ user.salary }}</p>
    <p>회원번호: {{ user.id }}</p>
    <p>User ID: {{ user.username }}</p>
    <p>팔로워: {{ user.followers_count }}</p>
    <p>팔로잉: {{ user.following_count }}</p>
    <RouterLink to="/profile/edit" v-if="isLogin" class="btn">정보 수정</RouterLink>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/lib/axios'
import { useUserStore } from '@/stores/userStore'
import defaultImage from '@/assets/default-avatar.png'

const user = ref(null)
const store = useUserStore()
const isLogin = store.isLogin  // 로그인한 본인만 수정 가능

onMounted(async () => {
  const res = await api.get('/accounts/profile/')
  user.value = res.data
})
</script>

<style scoped>
.profile-card {
  max-width: 400px;
  margin: 2rem auto;
  padding: 1.5rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  text-align: center;
}
.avatar {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
  margin-bottom: 1rem;
}
.btn {
  display: inline-block;
  padding: 0.5rem 1.2rem;
  background: #004080;
  color: #fff;
  border-radius: 4px;
  text-decoration: none;
  margin-top: 1rem;
}
</style>
