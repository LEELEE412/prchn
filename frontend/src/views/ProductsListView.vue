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

      <label class="ml-4">상품 유형:</label>
      <select v-model="productType">
        <option value="all">전체</option>
        <option value="deposit">예금</option>
        <option value="saving">적금</option>
      </select>
    </div>

    <!-- 상품 목록 테이블 -->
    <table class="rates-table">
      <thead>
        <tr>
          <th>은행명</th>
          <th>상품명</th>
          <th>가입기간</th>
          <th>기본금리</th>
          <th>우대금리</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in filteredProducts" :key="product.fin_prdt_cd" 
            @click="showProductDetail(product)"
            class="clickable-row">
          <td>{{ product.kor_co_nm }}</td>
          <td>{{ product.fin_prdt_nm }}</td>
          <td>
            <span v-if="product.options && product.options.length">
              {{ getTermRange(product) }}
            </span>
          </td>
          <td>
            <span class="rate">{{ getBaseRate(product) }}%</span>
          </td>
          <td>
            <span class="rate preferential">{{ getMaxRate(product) }}%</span>
          </td>
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
const productType = ref('all');

// 은행 목록 계산
const banks = computed(() => {
  return [...new Set(products.value.map(p => p.kor_co_nm))].sort();
});

// 상품 필터링
const filteredProducts = computed(() => {
  let filtered = products.value;
  
  // 은행 필터 적용
  if (bankFilter.value) {
    filtered = filtered.filter(p => p.kor_co_nm === bankFilter.value);
  }
  
  // 상품 유형 필터 적용
  if (productType.value !== 'all') {
    filtered = filtered.filter(p => {
      const isDeposit = p.fin_prdt_nm.includes('예금');
      return productType.value === 'deposit' ? isDeposit : !isDeposit;
    });
  }
  
  return filtered;
});

// 가입기간 범위 표시
function getTermRange(product) {
  if (!product.options?.length) return '-';
  const terms = product.options.map(o => o.save_trm).sort((a, b) => a - b);
  return `${terms[0]}~${terms[terms.length - 1]}개월`;
}

// 기본금리 계산
function getBaseRate(product) {
  const rates = product.options?.map(o => o.intr_rate) || [];
  return rates.length ? Math.max(...rates).toFixed(2) : '0.00';
}

// 우대금리 계산
function getMaxRate(product) {
  const rates = product.options?.map(o => o.intr_rate2) || [];
  return rates.length ? Math.max(...rates).toFixed(2) : '0.00';
}

// 상품 상세 표시
function showProductDetail(product) {
  selectedProduct.value = product;
}

// 데이터 로드
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

.filters label {
  font-weight: 500;
  color: #666;
}

.ml-4 {
  margin-left: 1rem;
}

.rates-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.rates-table th,
.rates-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.rates-table th {
  background-color: #f5f7fa;
  font-weight: 600;
  color: #2c3e50;
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.clickable-row:hover {
  background-color: #f8fafc;
}

.rate {
  font-weight: 500;
  color: #2563eb;
}

.rate.preferential {
  color: #16a34a;
}
</style>