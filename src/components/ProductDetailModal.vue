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

        <!-- 가입하기 버튼 영역 -->
        <div class="action-area">
          <button
            v-if="userStore.isLogin && !isSubscribed"
            class="subscribe-btn"
            @click="subscribe"
          >
            가입하기
          </button>
          <span
            v-else-if="userStore.isLogin && isSubscribed"
            class="subscribed-label"
          >
            가입된 상품
          </span>
          <RouterLink
            v-else
            to="/login"
            class="login-btn"
          >
            로그인 후 가입
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useUserStore } from '@/stores/userStore';
import { useRouter } from 'vue-router';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const router = useRouter();
const userStore = useUserStore();

// 가입기간 순으로 정렬된 옵션
const sortedOptions = computed(() => {
  return [...(props.product.options || [])].sort((a, b) => a.save_trm - b.save_trm);
});

// 이미 구독한 상품인지 확인
const isSubscribed = computed(() => {
  return userStore.subscribed?.includes(props.product.id);
});

// 가입하기 처리
async function subscribe() {
  try {
    await userStore.subscribe(props.product.id);
    alert('상품 가입이 완료되었습니다.');
    router.push('/my-products');
  } catch (err) {
    console.error('가입 실패:', err);
    alert(err.response?.data?.detail || '가입 처리 중 오류가 발생했습니다.');
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

.action-area {
  margin-top: 2rem;
  text-align: center;
}

.subscribe-btn, .login-btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

.subscribe-btn {
  background-color: #2563eb;
  color: white;
}

.subscribe-btn:hover {
  background-color: #1d4ed8;
}

.login-btn {
  background-color: #e5e7eb;
  color: #374151;
}

.login-btn:hover {
  background-color: #d1d5db;
}

.subscribed-label {
  display: inline-block;
  padding: 0.75rem 2rem;
  background-color: #10b981;
  color: white;
  border-radius: 6px;
  font-weight: 500;
}
</style>