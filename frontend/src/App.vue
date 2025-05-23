<template>
  <nav class="navbar">
    <div class="container">
      <!-- 브랜드 로고 및 이름 -->
      <RouterLink to="/" class="logo">
        <span class="logo-primary">Fin</span><span class="logo-secondary">Trust</span>
      </RouterLink>

<!-- 네비게이션 링크 -->
  <ul class="nav-links">
    <li><RouterLink to="/">홈</RouterLink></li>
    <!-- 로그인 시에만 금융상품 목록 및 상세 링크 -->
    <li v-if="userStore.isLogin"><RouterLink to="/products">금리비교</RouterLink></li>
    <li v-if="userStore.isLogin"><RouterLink to="/my-products">내가 가입한 상품</RouterLink></li>
  </ul>

  <!-- 인증 버튼 -->
  <div class="auth-buttons">
    <template v-if="userStore.isLogin">
      <button @click="userStore.logOut">로그아웃</button>
    </template>
    <template v-else>
      <RouterLink to="/signup">회원가입</RouterLink>
      <RouterLink to="/login">로그인</RouterLink>
    </template>
      </div>
    </div>
  </nav>
  <RouterView />
</template>

<script setup>
import { useUserStore } from '@/stores/userStore'
const userStore = useUserStore()
</script>

<style scoped>
.navbar {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
}
.logo {
  font-size: 1.75rem;
  font-weight: bold;
  text-decoration: none;
}
.logo-primary {
  color: #004080; /* 진한 파란색 */
}
.logo-secondary {
  color: #0073e6; /* 밝은 파란색 */
}
.nav-links {
  list-style: none;
  display: flex;
  gap: 1.25rem;
  margin: 0;
  padding: 0;
}
.nav-links a {
  color: #333333;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}
.nav-links a:hover {
  color: #0073e6;
}
.auth-buttons {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.auth-buttons button,
.auth-buttons a {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  border: 1px solid #0073e6;
  background-color: #fff;
  color: #0073e6;
  font-weight: 500;
  text-decoration: none;
  transition: background-color 0.2s ease, color 0.2s ease;
}
.auth-buttons button:hover,
.auth-buttons a:hover {
  background-color: #0073e6;
  color: #ffffff;
}
</style>