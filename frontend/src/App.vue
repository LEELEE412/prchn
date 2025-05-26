<template>
  <nav class="navbar">
    <div class="container d-flex align-items-center justify-content-between">
      <!-- 브랜드 로고 + 인사말 -->
      <div class="brand-section d-flex align-items-center">
        <RouterLink to="/" class="navbar-brand logo">
          <span class="logo-primary">Fin</span><span class="logo-secondary">Trust</span>
        </RouterLink>
        <span v-if="userStore.isLogin" class="greeting">
          {{ userStore.username }}님, 안녕하세요
        </span>
      </div>

      <!-- 네비게이션 -->
      <ul class="nav nav-pills">
        <li class="nav-item">
          <RouterLink
            to="/bank-search"
            class="nav-link"
            :class="{ active: $route.name === 'BankSearch' }"
            v-if="userStore.isLogin"
          >근처 은행 검색</RouterLink>
        </li>
        <li class="nav-item dropdown" v-if="userStore.isLogin">
          <a
            class="nav-link dropdown-toggle"
            data-bs-toggle="dropdown"
            role="button"
            aria-expanded="false"
          >예·적금</a>
          <ul class="dropdown-menu">
            <li><RouterLink to="/products" class="dropdown-item">금리비교</RouterLink></li>
            <li><RouterLink to="/my-products" class="dropdown-item">내가 가입한 상품</RouterLink></li>
          </ul>
        </li>
      </ul>

      <!-- 인증 버튼 영역 -->
      <div class="auth-buttons d-flex align-items-center">
        <RouterLink
          v-if="userStore.isLogin"
          to="/profile"
          class="btn btn-outline-secondary me-2"
        >내 프로필</RouterLink>
        <button
          v-if="userStore.isLogin"
          class="btn btn-outline-primary"
          @click="userStore.logOut"
        >로그아웃</button>
        <template v-else>
          <RouterLink to="/signup" class="btn btn-outline-primary me-2">회원가입</RouterLink>
          <RouterLink to="/login" class="btn btn-primary">로그인</RouterLink>
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
/* 기존 스타일 유지 */
</style>