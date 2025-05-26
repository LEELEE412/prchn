<template>
  <div v-if="product" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ product.fin_prdt_nm }}</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="bank-info">
          <h3>{{ product.kor_co_nm }}</h3>
        </div>

        <!-- 금리 정보 테이블 -->
        <div class="rates-table">
          <table>
            <thead>
              <tr>
                <th>가입기간</th>
                <th>기본금리</th>
                <th>우대금리</th>
                <th>금리유형</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="option in sortedOptions" :key="option.save_trm">
                <td>{{ option.save_trm }}개월</td>
                <td>{{ option.intr_rate.toFixed(2) }}%</td>
                <td>{{ option.intr_rate2.toFixed(2) }}%</td>
                <td>{{ option.intr_rate_type_nm }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 상품 상세 정보 -->
        <div class="product-details">
          <div class="detail-section">
            <h4>가입방법</h4>
            <p>{{ product.join_way }}</p>
          </div>
          
          <div class="detail-section">
            <h4>가입대상</h4>
            <p>{{ product.join_member }}</p>
          </div>

          <div class="detail-section">
            <h4>우대조건</h4>
            <p>{{ product.spcl_cnd }}</p>
          </div>

          <div class="detail-section">
            <h4>기타 유의사항</h4>
            <p>{{ product.etc_note }}</p>
          </div>
        </div>

        <!-- 가입 기간 선택 -->
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

        <!-- 가입/취소 버튼 -->
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
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import api from '@/lib/axios';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const router = useRouter();
const userStore = useUserStore();
const selectedTerm = ref('');

// 가입기간 순으로 정렬된 옵션
const sortedOptions = computed(() => {
  return [...(props.product.options || [])].sort((a, b) => a.save_trm - b.save_trm);
});

// 이미 구독된 상품인지 체크
const isSubscribed = computed(() => {
  return userStore.subscribed?.includes(props.product.fin_prdt_cd);
});

// 가입하기 핸들러
async function onSubscribe() {
  if (!selectedTerm.value) return;
  
  try {
    await api.post(`/products/deposit-products/subscribe/${props.product.fin_prdt_cd}/`, {
      term: selectedTerm.value
    });
    userStore.subscribed.push(props.product.fin_prdt_cd);
    router.push('/my-products');
  } catch (err) {
    console.error('Subscription failed:', err);
    alert('상품 가입 중 오류가 발생했습니다.');
  }
}

// 가입 취소 핸들러
async function onUnsubscribe() {
  try {
    await api.delete(`/products/deposit-products/subscribe/${props.product.fin_prdt_cd}/`);
    userStore.subscribed = userStore.subscribed.filter(id => id !== props.product.fin_prdt_cd);
    router.push('/my-products');
  } catch (err) {
    console.error('Unsubscribe failed:', err);
    alert('가입 취소 중 오류가 발생했습니다.');
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  font-size: 1.5rem;
  color: #1a365d;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0.5rem;
}

.bank-info {
  margin-bottom: 1.5rem;
}

.bank-info h3 {
  color: #2563eb;
  font-size: 1.25rem;
}

.rates-table {
  margin: 1.5rem 0;
  overflow-x: auto;
}

.rates-table table {
  width: 100%;
  border-collapse: collapse;
}

.rates-table th,
.rates-table td {
  padding: 0.75rem 1rem;
  text-align: center;
  border: 1px solid #e5e7eb;
}

.rates-table th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #1e293b;
}

.rates-table td {
  color: #334155;
}

.product-details {
  margin-top: 2rem;
}

.detail-section {
  margin-bottom: 1.5rem;
}

.detail-section h4 {
  color: #1e293b;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.detail-section p {
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

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

.action-area {
  margin-top: 1.5rem;
  text-align: center;
}

.subscribe-btn,
.unsubscribe-btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  text-decoration: none;
  display: inline-block;
}

.subscribe-btn {
  background-color: #0073e6;
  color: #fff;
}

.subscribe-btn:hover {
  background-color: #005bb5;
}

.subscribe-btn:disabled {
  background-color: #cbd5e1;
  cursor: not-allowed;
}

.unsubscribe-btn {
  background-color: #ef4444;
  color: #fff;
}

.unsubscribe-btn:hover {
  background-color: #dc2626;
}
</style>