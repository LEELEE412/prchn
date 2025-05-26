<template>
  <div v-if="product" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <!-- 기존 헤더와 상품 정보는 유지 -->
      
      <!-- 가입 기간 선택 추가 -->
      <div v-if="userStore.isLogin && !isSubscribed" class="subscription-form">
        <h4>가입 기간 선택</h4>
        <select v-model="selectedTerm" class="term-select">
          <option value="">가입 기간을 선택하세요</option>
          <option 
            v-for="option in sortedOptions" 
            :key="option.save_trm" 
            :value="option.save_trm"
          >
            {{ option.save_trm }}개월 
            (기본 {{ option.intr_rate }}% / 우대 {{ option.intr_rate2 }}%)
          </option>
        </select>
      </div>

      <!-- 가입/삭제 버튼 -->
      <div class="action-area">
        <button
          v-if="userStore.isLogin && !isSubscribed"
          class="subscribe-btn"
          :disabled="!selectedTerm"
          @click="onSubscribe"
        >
          {{ selectedTerm ? `${selectedTerm}개월 가입하기` : '가입기간을 선택하세요' }}
        </button>
        <button
          v-else-if="userStore.isLogin && isSubscribed"
          class="unsubscribe-btn"
          @click="onUnsubscribe"
        >
          가입 취소
        </button>
        <RouterLink v-else to="/login" class="subscribe-btn">
          로그인 후 가입
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import { useProductStore } from '@/stores/productStore';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const router = useRouter();
const userStore = useUserStore();
const productStore = useProductStore();
const selectedTerm = ref('');

// 가입기간 순으로 정렬된 옵션
const sortedOptions = computed(() => {
  return [...(props.product.options || [])].sort((a, b) => a.save_trm - b.save_trm);
});

// 이미 구독된 상품인지 체크
const isSubscribed = computed(() => {
  const productId = props.product.id || props.product.fin_prdt_cd;
  return userStore.subscribed?.includes(Number(productId));
});

// 가입하기 핸들러
async function onSubscribe() {
  if (!selectedTerm.value) return;
  
  try {
    const productId = props.product.id || props.product.fin_prdt_cd;
    await productStore.subscribe({
      productId,
      term: selectedTerm.value
    });
    router.push({ name: 'MyProducts' });
  } catch (err) {
    const msg = err.response?.data?.detail || err.message || '가입 중 오류가 발생했습니다.';
    alert(msg);
  }
}

// 가입 취소 핸들러
async function onUnsubscribe() {
  try {
    const productId = props.product.id || props.product.fin_prdt_cd;
    await productStore.unsubscribe(productId);
    router.push({ name: 'MyProducts' });
  } catch (err) {
    alert('가입 취소 중 오류가 발생했습니다.');
  }
}
</script>

<style scoped>
/* 기존 스타일 유지 */

.subscription-form {
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
}

.term-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  margin-top: 0.5rem;
  font-size: 1rem;
}

.unsubscribe-btn {
  padding: 0.75rem 2rem;
  border: none;
  background-color: #ef4444;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}

.unsubscribe-btn:hover {
  background-color: #dc2626;
}

.subscribe-btn:disabled {
  background-color: #cbd5e1;
  cursor: not-allowed;
}
</style>
