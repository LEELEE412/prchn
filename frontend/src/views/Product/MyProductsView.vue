```vue
<template>
  <div class="my-products">
    <h2>내가 가입한 상품</h2>
    
    <!-- 예금 상품 섹션 -->
    <section v-if="depositSubscriptions.length" class="product-section">
      <h3>가입한 예금 상품</h3>
      <div class="products-grid">
        <div
          v-for="sub in depositSubscriptions"
          :key="sub.id"
          class="product-card"
          @click="showSubscriptionDetail(sub)"
        >
          <div class="product-info">
            <h4>{{ sub.bank_name }}</h4>
            <p class="product-name">{{ sub.product_name }}</p>
            <div class="subscription-details">
              <p>가입기간: {{ sub.term_months }}개월</p>
              <p>시작일: {{ formatDate(sub.start_date) }}</p>
              <p>만기일: {{ formatDate(sub.end_date) }}</p>
              <p class="remaining-days">
                남은 기간: {{ sub.remaining_days }}일
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 적금 상품 섹션 -->
    <section v-if="savingSubscriptions.length" class="product-section">
      <h3>가입한 적금 상품</h3>
      <div class="products-grid">
        <div
          v-for="sub in savingSubscriptions"
          :key="sub.id"
          class="product-card"
          @click="showSubscriptionDetail(sub)"
        >
          <div class="product-info">
            <h4>{{ sub.bank_name }}</h4>
            <p class="product-name">{{ sub.product_name }}</p>
            <div class="subscription-details">
              <p>가입기간: {{ sub.term_months }}개월</p>
              <p>시작일: {{ formatDate(sub.start_date) }}</p>
              <p>만기일: {{ formatDate(sub.end_date) }}</p>
              <p class="remaining-days">
                남은 기간: {{ sub.remaining_days }}일
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <p v-if="!depositSubscriptions.length && !savingSubscriptions.length" class="no-products">
      아직 가입한 상품이 없습니다.
    </p>

    <!-- 구독 상세 모달 -->
    <SubscriptionDetailModal
      v-if="selectedSubscription"
      :subscription="selectedSubscription"
      @close="selectedSubscription = null"
      @cancelled="loadSubscriptions"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import dayjs from 'dayjs'
import api from '@/lib/axios'
import SubscriptionDetailModal from '@/components/ProductDetailModal/SubscriptionDetailModal.vue'

const depositSubscriptions = ref([]);
const savingSubscriptions = ref([]);
const selectedSubscription = ref(null);

async function loadSubscriptions() {
  try {
    const response = await api.get('/accounts/profile/')
    const allSubscriptions = response.data.active_subscriptions || [];
    
    // 예금과 적금 상품 분리
    depositSubscriptions.value = allSubscriptions.filter(sub => 
      sub.product_name.includes('예금')
    );
    savingSubscriptions.value = allSubscriptions.filter(sub => 
      sub.product_name.includes('적금')
    );
  } catch (err) {
    console.error('Failed to fetch subscriptions:', err)
  }
}

function showSubscriptionDetail(subscription) {
  selectedSubscription.value = subscription;
}

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD')
}

onMounted(loadSubscriptions)
</script>

<style scoped>
.my-products {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.my-products h2 {
  margin-bottom: 2rem;
  font-size: 1.75rem;
  color: #004080;
  text-align: center;
}

.product-section {
  margin-bottom: 3rem;
}

.product-section h3 {
  font-size: 1.4rem;
  color: #2563eb;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.product-card {
  background-color: #f7f9fc;
  border: 1px solid #e0e6ed;
  border-radius: 8px;
  padding: 1.5rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.product-info h4 {
  color: #004080;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.product-name {
  color: #333;
  font-size: 1rem;
  margin-bottom: 0.75rem;
  font-weight: 500;
}

.subscription-details {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e0e6ed;
}

.subscription-details p {
  margin: 0.25rem 0;
  color: #666;
}

.remaining-days {
  font-weight: 500;
  color: #004080 !important;
  margin-top: 0.5rem !important;
}

.no-products {
  text-align: center;
  color: #666666;
  font-size: 1.1rem;
  margin-top: 2rem;
  font-style: italic;
}
</style>
```