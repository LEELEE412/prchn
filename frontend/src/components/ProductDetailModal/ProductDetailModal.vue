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

        <!-- 가입 기간 선택 -->
        <div v-if="userStore.isLogin && !isSubscribed" class="date-selection">
          <h4>가입 기간 선택</h4>
          <div class="date-inputs">
            <div class="form-group">
              <label>시작일</label>
              <input 
                type="date" 
                v-model="startDate"
                :min="today"
                @change="updateEndDate"
              />
            </div>
            <div class="form-group">
              <label>가입 기간</label>
              <select v-model="selectedTerm" @change="updateEndDate">
                <option v-for="option in sortedOptions" 
                        :key="option.save_trm" 
                        :value="option.save_trm">
                  {{ option.save_trm }}개월
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>만기일</label>
              <input type="date" v-model="endDate" disabled />
            </div>
          </div>
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
            @click="onSubscribe"
            :disabled="!isValidSubscription"
          >가입하기</button>
          <button 
            v-else-if="userStore.isLogin && isSubscribed"
            class="unsubscribe-btn"
            @click="onUnsubscribe"
          >가입 취소</button>
          <RouterLink v-else to="/login" class="subscribe-btn">
            로그인 후 가입
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import api from '@/lib/axios';
import dayjs from 'dayjs';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close', 'subscribe']);
const router = useRouter();
const userStore = useUserStore();

// 날짜 관련 상태
const today = dayjs().format('YYYY-MM-DD');
const startDate = ref(today);
const endDate = ref('');
const selectedTerm = ref(null);

// 가입기간 순으로 정렬된 옵션
const sortedOptions = computed(() => {
  return [...(props.product.options || [])].sort((a, b) => a.save_trm - b.save_trm);
});

// 이미 구독된 상품인지 체크
const isSubscribed = computed(() => {
  if (props.product.fin_prdt_cd) {
    return userStore.subscribed_deposit_products?.some(p => p.fin_prdt_cd === props.product.fin_prdt_cd) ||
           userStore.subscribed_saving_products?.some(p => p.fin_prdt_cd === props.product.fin_prdt_cd);
  }
  return false;
});

// 가입 가능 여부 체크
const isValidSubscription = computed(() => {
  return startDate.value && endDate.value && selectedTerm.value;
});

// 종료일 자동 계산
function updateEndDate() {
  if (startDate.value && selectedTerm.value) {
    endDate.value = dayjs(startDate.value)
      .add(selectedTerm.value, 'month')
      .format('YYYY-MM-DD');
  }
}

// 가입하기 핸들러
async function onSubscribe() {
  const subscriptionData = {
    term_months: selectedTerm.value,
    start_date: startDate.value,
    end_date: endDate.value
  };

  try {
    if (props.product.fin_prdt_cd.startsWith('S')) {
      // 적금 상품
      await api.post(`/products/saving-products/subscribe/${props.product.fin_prdt_cd}/`, subscriptionData);
    } else {
      // 예금 상품
      emit('subscribe', subscriptionData);
    }
    router.push('/my-products');
  } catch (err) {
    console.error('Subscription failed:', err);
    alert('상품 가입 중 오류가 발생했습니다.');
  }
}

// 가입 취소 핸들러
async function onUnsubscribe() {
  try {
    if (props.product.fin_prdt_cd.startsWith('S')) {
      await api.delete(`/products/saving-products/subscribe/${props.product.fin_prdt_cd}/`);
    } else {
      await api.delete(`/products/deposit-products/subscribe/${props.product.fin_prdt_cd}/`);
    }
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

.date-selection {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.date-selection h4 {
  color: #1e293b;
  margin-bottom: 1rem;
}

.date-inputs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.9rem;
  color: #4b5563;
}

.form-group input,
.form-group select {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
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

.subscribe-btn:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.subscribe-btn:not(:disabled):hover {
  background-color: #005bb5;
}

.unsubscribe-btn {
  background-color: #dc2626;
  color: #fff;
}

.unsubscribe-btn:hover {
  background-color: #b91c1c;
}
</style>