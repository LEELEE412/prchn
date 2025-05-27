<template>
  <div class="my-products">
    <h2>내가 가입한 상품</h2>
    
    <!-- 예금 상품 섹션 -->
    <div v-if="depositProducts.length" class="product-section">
      <h3>예금 상품</h3>
      <div class="products-grid">
        <div
          v-for="product in depositProducts"
          :key="product.fin_prdt_cd"
          class="product-card"
        >
          <div class="product-info">
            <h4>{{ product.kor_co_nm }}</h4>
            <p class="product-name">{{ product.fin_prdt_nm }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 적금 상품 섹션 -->
    <div v-if="savingProducts.length" class="product-section">
      <h3>적금 상품</h3>
      <div class="products-grid">
        <div
          v-for="product in savingProducts"
          :key="product.fin_prdt_cd"
          class="product-card"
        >
          <div class="product-info">
            <h4>{{ product.kor_co_nm }}</h4>
            <p class="product-name">{{ product.fin_prdt_nm }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 가입된 상품 상세 정보 -->
    <div v-if="subscriptions.length" class="subscriptions-section">
      <h3>가입 상세 정보</h3>
      <div class="products-grid">
        <div
          v-for="sub in subscriptions"
          :key="sub.id"
          class="product-card"
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
    </div>
    
    <p v-if="!depositProducts.length && !savingProducts.length && !subscriptions.length" class="no-products">
      아직 가입한 상품이 없습니다.
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import dayjs from 'dayjs'
import api from '@/lib/axios'

const depositProducts = ref([])
const savingProducts = ref([])
const subscriptions = ref([])

onMounted(async () => {
  try {
    const { data } = await api.get('/accounts/profile/')
    depositProducts.value = data.subscribed_deposit_products || []
    savingProducts.value = data.subscribed_saving_products || []
    subscriptions.value = data.active_subscriptions || []
  } catch (err) {
    console.error('Failed to fetch products:', err)
  }
})

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD')
}
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
  margin-bottom: 2rem;
}

.product-section h3 {
  color: #004080;
  font-size: 1.4rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e0e6ed;
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

.subscriptions-section {
  margin-top: 3rem;
}
</style>