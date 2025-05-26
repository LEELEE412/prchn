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
            :class="{ active: $route.name === 'ProductsList' }"
            v-if="userStore.isLogin"
          >근처 은행 검색</RouterLink>
        </li>
        <li class="nav-item dropdown" v-if="userStore.isLogin">
          <a
            class="nav-link dropdown-toggle"
            data-bs-toggle="dropdown"
            role="button"
            aria-expanded="false"
          >비디오</a>
          <ul class="dropdown-menu">
            <li><RouterLink to="/search" class="dropdown-item">검색</RouterLink></li>
            <li><RouterLink to="/later"  class="dropdown-item">나중에 볼 영상</RouterLink></li>
            <li><RouterLink to="/channels" class="dropdown-item">저장된 채널</RouterLink></li>
          </ul>
        </li>
        <li class="nav-item dropdown" v-if="userStore.isLogin">
          <a
            class="nav-link dropdown-toggle"
            data-bs-toggle="dropdown"
            role="button"
            aria-expanded="false"
          >커뮤니티</a>
          <ul class="dropdown-menu">
            <li><RouterLink to="/community/create" class="dropdown-item">게시글 작성</RouterLink></li>
            <li><RouterLink to="/community" class="dropdown-item">게시글 목록</RouterLink></li>
            <li><RouterLink to="/community/mine" class="dropdown-item">내 게시글</RouterLink></li>
          </ul>
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
            <li><RouterLink to="/all-details" class="dropdown-item">금융상품 전체 보기</RouterLink></li>
          </ul>
        </li>
      </ul>

      <!-- 인증 버튼 영역: 내 프로필 / 로그아웃 or 회원가입·로그인 -->
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
.navbar {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  padding: 0.5rem 1rem;
}

/* 로고 및 인사말 */
.brand-section .logo {
  font-size: 1.75rem;
  font-weight: bold;
  text-decoration: none;
}
.brand-section .logo-primary { color: #004080; }
.brand-section .logo-secondary { color: #0073e6; }
.greeting {
  margin-left: 1rem;
  color: #333;
  font-weight: 500;
}

/* 네비게이션 텍스트 스타일 */
.nav-pills .nav-link {
  color: #004080;
  font-weight: 500;
}
.nav-pills .nav-link.active {
  background-color: #004080;
  color: #fff;
}

/* 드롭다운 메뉴 최소 너비 */
.dropdown-menu {
  min-width: 10rem;
}

/* 인증 버튼 (내 프로필, 로그아웃 등) */
.auth-buttons .btn {
  font-size: 0.9rem;
}
.auth-buttons .btn-outline-secondary {
  color: #004080;
  border-color: #004080;
}
.auth-buttons .btn-outline-secondary:hover {
  background-color: #004080;
  color: #fff;
}

/* 오른쪽 끝 정렬 */
.auth-buttons {
  margin-left: auto;
}
</style>
