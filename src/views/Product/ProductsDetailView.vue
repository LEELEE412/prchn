<template>
  <div v-if="product" class="product-detail">
    <!-- 상품 타입 표시 -->
    <h2 class="product-type">
      {{ product.name.includes('예금') ? '정기예금' : '정기적금' }}
    </h2>

    <!-- 상세 정보 -->
    <div class="detail-item"><strong>공시 제출월:</strong> {{ product.dcls_month }}</div>
    <div class="detail-item"><strong>금융회사명:</strong> {{ product.bank_name }}</div>
    <div class="detail-item"><strong>상품명:</strong> {{ product.name }}</div>
    <div class="detail-item"><strong>가입제한:</strong> {{ product.join_deny === 'Y' ? '제한' : '가능' }}</div>
    <div class="detail-item"><strong>가입방법:</strong> {{ product.join_way }}</div>
    <div class="detail-item"><strong>우대이율:</strong> {{ product.supr_rate }}%</div>
    <div class="detail-item">
      <strong>우대조건:</strong>
      <ul>
        <li v-for="(cond, idx) in specialConditions" :key="idx">{{ cond }}</li>
      </ul>
    </div>
    <div class="detail-item"><strong>기타 안내:</strong> {{ product.etc_note }}</div>

    <!-- 가입하기 버튼 또는 가입된 상품 레이블 -->
    <div class="action-area">
      <button
        v-if="userStore.isLogin && !isSubscribed"
        class="subscribe-btn"
        @click="onSubscribe"
      >
        가입하기
      </button>
      <span
        v-else-if="userStore.isLogin && isSubscribed"
        class="subscribed-label"
      >
        가입된 상품
      </span>
      <RouterLink v-else to="/login" class="subscribe-btn">
        로그인 후 가입
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/stores/productStore'
import { useUserStore } from '@/stores/userStore'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()
const userStore = useUserStore()

// 상세 상품 데이터 로드
onMounted(() => {
  productStore.fetchProduct(route.params.id)
})

const product = computed(() => productStore.detail)

// 특수 조건 문자열 분리
const specialConditions = computed(() => {
  const raw = product.value?.spcl_cnd || ''
  return raw.split(';').filter(Boolean)
})

// 이미 구독된 상품인지 체크 (숫자형 PK)
const isSubscribed = computed(() =>
  userStore.subscribed?.includes(Number(route.params.id))
)

// 가입하기 핸들러
async function onSubscribe() {
  try {
    await productStore.subscribe(route.params.id)
    router.push({ name: 'MyProducts' })
  } catch (err) {
    const msg = err.response?.data?.detail || err.message || '가입 중 오류가 발생했습니다.'
    alert(msg)
  }
}
</script>

<style scoped>
.product-detail {
  max-width: 700px;
  margin: 2rem auto;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}
.product-type {
  font-size: 1.5rem;
  font-weight: bold;
  color: #004080;
  margin-bottom: 1rem;
}
.detail-item {
  margin-bottom: 0.75rem;
  line-height: 1.5;
}
.detail-item strong {
  display: inline-block;
  width: 100px;
}
.action-area {
  margin-top: 1.5rem;
}
.subscribe-btn {
  padding: 0.75rem 2rem;
  border: none;
  background-color: #0073e6;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}
.subscribe-btn:hover {
  background-color: #005bb5;
}
.subscribed-label {
  display: inline-block;
  padding: 0.75rem 2rem;
  background-color: #e0e0e0;
  color: #555;
  border-radius: 4px;
  font-weight: 500;
}
</style>