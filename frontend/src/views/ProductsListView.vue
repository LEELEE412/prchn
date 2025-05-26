<template>
  <div class="products-list">
    <h2>예·적금 상품 비교</h2>

    <!-- 필터 영역 -->
    <div class="filters">
      <label>은행:</label>
      <select v-model="bankFilter">
        <option value="">전체 은행</option>
        <option v-for="bank in banks" :key="bank">{{ bank }}</option>
      </select>
    </div>

    <!-- 상품 목록 테이블 -->
    <table class="rates-table">
      <thead>
        <tr>
          <th>은행명</th>
          <th>상품명</th>
          <th>기본금리</th>
          <th>최고금리</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in filteredProducts" :key="product.fin_prdt_cd" 
            @click="showProductDetail(product)"
            class="clickable-row">
          <td>{{ product.kor_co_nm }}</td>
          <td>{{ product.fin_prdt_nm }}</td>
          <td>{{ getBaseRate(product) }}%</td>
          <td>{{ getMaxRate(product) }}%</td>
        </tr>
      </tbody>
    </table>

    <!-- 상품 상세 모달 -->
    <ProductDetailModal
      v-if="selectedProduct"
      :product="selectedProduct"
      @close="selectedProduct = null"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import ProductDetailModal from '@/components/ProductDetailModal.vue';

const products = ref([]);
const selectedProduct = ref(null);
const bankFilter = ref('');

const banks = computed(() => {
  return [...new Set(products.value.map(p => p.kor_co_nm))].sort();
});

const filteredProducts = computed(() => {
  return products.value.filter(p => 
    !bankFilter.value || p.kor_co_nm === bankFilter.value
  );
});

function getBaseRate(product) {
  const rates = product.options?.map(o => o.intr_rate) || [];
  return rates.length ? Math.max(...rates).toFixed(2) : '0.00';
}

function getMaxRate(product) {
  const rates = product.options?.map(o => o.intr_rate2) || [];
  return rates.length ? Math.max(...rates).toFixed(2) : '0.00';
}

function showProductDetail(product) {
  selectedProduct.value = product;
}

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/v1/products/deposit-products-with-options/');
    products.value = response.data;
  } catch (error) {
    console.error('Failed to fetch products:', error);
  }
});
</script>

<style scoped>
.products-list {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.filters {
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.filters select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.rates-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.rates-table th,
.rates-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.rates-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.clickable-row:hover {
  background-color: #f0f7ff;
}
</style>