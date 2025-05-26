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
<<<<<<< HEAD
=======

      <label class="ml-4">상품 유형:</label>
      <select v-model="productType">
        <option value="deposit">예금</option>
        <option value="saving">적금</option>
      </select>
>>>>>>> 7783308aeb6a82bc389d75eda9fff7072b72d990
    </div>

    <!-- 상품 목록 테이블 -->
    <table class="rates-table">
      <thead>
        <tr>
          <th>은행명</th>
          <th>상품명</th>
<<<<<<< HEAD
          <th>기본금리</th>
          <th>최고금리</th>
=======
          <th v-for="term in availableTerms" :key="term">{{ term }}개월</th>
>>>>>>> 7783308aeb6a82bc389d75eda9fff7072b72d990
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in filteredProducts" :key="product.fin_prdt_cd" 
            @click="showProductDetail(product)"
            class="clickable-row">
          <td>{{ product.kor_co_nm }}</td>
<<<<<<< HEAD
          <td>{{ product.fin_prdt_nm }}</td>
          <td>{{ getBaseRate(product) }}%</td>
          <td>{{ getMaxRate(product) }}%</td>
=======
          <td class="product-name">
            <div class="name">{{ product.fin_prdt_nm }}</div>
          </td>
          <td v-for="term in availableTerms" :key="term" class="rate-cell">
            <div class="rate-info" v-if="getRateInfo(product, term).hasRate">
              <span class="base-rate">{{ getRateInfo(product, term).baseRate }}%</span>
              <span class="pref-rate">({{ getRateInfo(product, term).prefRate }}%)</span>
            </div>
            <span v-else>-</span>
          </td>
>>>>>>> 7783308aeb6a82bc389d75eda9fff7072b72d990
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
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import ProductDetailModal from '@/components/ProductDetailModal.vue';

const products = ref([]);
const selectedProduct = ref(null);
const bankFilter = ref('');
<<<<<<< HEAD
=======
const productType = ref('deposit');

// 모든 상품의 가능한 가입기간을 추출하여 정렬
const availableTerms = computed(() => {
  const terms = new Set();
  products.value.forEach(product => {
    product.options?.forEach(option => {
      terms.add(option.save_trm);
    });
  });
  return Array.from(terms).sort((a, b) => a - b);
});
>>>>>>> 7783308aeb6a82bc389d75eda9fff7072b72d990

const banks = computed(() => {
  return [...new Set(products.value.map(p => p.kor_co_nm))].sort();
});

const filteredProducts = computed(() => {
<<<<<<< HEAD
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
=======
  let filtered = products.value;
  if (bankFilter.value) {
    filtered = filtered.filter(p => p.kor_co_nm === bankFilter.value);
  }
  return filtered;
});

// 특정 기간의 금리 정보 가져오기
function getRateInfo(product, term) {
  const option = product.options?.find(o => o.save_trm === term);
  if (!option) return { hasRate: false };
  
  return {
    hasRate: true,
    baseRate: option.intr_rate.toFixed(2),
    prefRate: option.intr_rate2.toFixed(2)
  };
>>>>>>> 7783308aeb6a82bc389d75eda9fff7072b72d990
}

function showProductDetail(product) {
  selectedProduct.value = product;
}

<<<<<<< HEAD
onMounted(async () => {
=======
// 데이터 로드
async function loadProducts() {
>>>>>>> 7783308aeb6a82bc389d75eda9fff7072b72d990
  try {
    const endpoint = productType.value === 'deposit' 
      ? 'deposit-products-with-options'
      : 'saving-products';
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/products/${endpoint}/`);
    products.value = response.data;
  } catch (error) {
    console.error('Failed to fetch products:', error);
  }
}

// 상품 유형이 변경될 때마다 데이터 다시 로드
watch(productType, loadProducts);

onMounted(loadProducts);
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

.filters label {
  font-weight: 500;
  color: #666;
}

.filters select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ddd;
}

<<<<<<< HEAD
=======
.ml-4 {
  margin-left: 1rem;
}

>>>>>>> 7783308aeb6a82bc389d75eda9fff7072b72d990
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

.product-name {
  padding: 0.75rem 1rem;
}

.product-name .name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.rate-cell {
  text-align: center;
  padding: 0.75rem 1rem;
}

.rate-info {
  font-size: 0.9em;
}

.base-rate {
  color: #2C5282;
  font-weight: 500;
}

.pref-rate {
  color: #E53E3E;
  margin-left: 0.25rem;
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.clickable-row:hover {
<<<<<<< HEAD
  background-color: #f0f7ff;
=======
  background-color: #f8fafc;
>>>>>>> 7783308aeb6a82bc389d75eda9fff7072b72d990
}
</style>