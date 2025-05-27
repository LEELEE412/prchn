<template>
  <div class="my-products">
    <h2>내가 가입한 상품</h2>
    
    <div v-if="subscribedProducts.length" class="products-grid">
      <div
        v-for="product in subscribedProducts"
        :key="product.fin_prdt_cd"
        class="product-card"
        @click="showProductDetail(product)"
      >
        <div class="product-info">
          <h3>{{ product.kor_co_nm }}</h3>
          <p class="product-name">{{ product.fin_prdt_nm }}</p>
          <div class="product-details">
            <p class="rate-info">
              <span class="base-rate">기본금리: {{ getBaseRate(product) }}%</span>
              <span class="pref-rate">우대금리: {{ getPrefRate(product) }}%</span>
            </p>
            <p class="term-info">가입기간: {{ product.save_trm }}개월</p>
          </div>
        </div>
      </div>
    </div>
    
    <p v-else class="no-products">아직 가입한 상품이 없습니다.</p>

    <!-- 상품 상세 모달 -->
    <ProductDetailModal
      v-if="selectedProduct"
      :product="selectedProduct"
      @close="selectedProduct = null"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import ProductDetailModal from '@/components/ProductDetailModal.vue'
import api from '@/lib/axios'

const userStore = useUserStore()
const selectedProduct = ref(null)
const subscribedProducts = ref([])

onMounted(async () => {
  try {
    const response = await api.get('/accounts/profile/')
    if (response.data.subscribed_deposit_products) {
      subscribedProducts.value = response.data.subscribed_deposit_products
    }
  } catch (err) {
    console.error('Failed to fetch subscribed products:', err)
  }
})

function showProductDetail(product) {
  selectedProduct.value = product
}

function getBaseRate(product) {
  return product.options?.[0]?.intr_rate.toFixed(2) || '0.00'
}

function getPrefRate(product) {
  return product.options?.[0]?.intr_rate2.toFixed(2) || '0.00'
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
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: #004080;
  text-align: center;
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
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.product-info h3 {
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

.product-details {
  font-size: 0.9rem;
  color: #666;
}

.rate-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.base-rate {
  color: #2C5282;
}

.pref-rate {
  color: #E53E3E;
}

.term-info {
  color: #666;
  margin: 0;
}

.no-products {
  text-align: center;
  color: #666666;
  font-size: 1.1rem;
  margin-top: 2rem;
  font-style: italic;
}
</style>