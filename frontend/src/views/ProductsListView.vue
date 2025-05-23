<template>
  <div class="products-list">
    <h2>{{ title }}</h2>

    <!-- 필터 영역 -->
    <div class="filters">
      <label>은행:</label>
      <select v-model="bankFilter">
        <option value="">전체 은행</option>
        <option v-for="b in banks" :key="b">{{ b }}</option>
      </select>

      <label>상품 타입:</label>
      <select v-model="typeFilter">
        <option value="">전체</option>
        <option value="deposit">정기예금</option>
        <option value="saving">정기적금</option>
      </select>

      <label>기간:</label>
      <select v-model.number="periodFilter">
        <option :value="0">전체 기간</option>
        <option v-for="p in periods" :key="p" :value="p">{{ p }}개월까지</option>
      </select>
    </div>

    <!-- 금리 비교 테이블 -->
    <table class="rates-table">
      <thead>
        <tr>
          <th>상품명</th>
          <th v-for="p in selectedPeriods" :key="p">{{ p }}개월</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in displayList" :key="item.product_id">
          <td>
            <RouterLink :to="{ name: 'ProductsDetail', params: { id: item.id } }">
              {{ item.bank_name }} – {{ item.name }}
            </RouterLink>
          </td>
          <td v-for="p in selectedPeriods" :key="p">
            {{ item.rates[p] != null ? item.rates[p] + '%' : '-' }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProductStore } from '@/stores/productStore'

const store        = useProductStore()
const bankFilter   = ref('')
const typeFilter   = ref('')
const periodFilter = ref(0)
const periods      = [6, 12, 24, 36]

onMounted(() => {
  store.fetchProducts()
})

const banks = computed(() =>
  [...new Set(store.products.map(p => p.bank_name))]
)

const title = computed(() => {
  if (typeFilter.value === 'deposit') return '정기예금 금리 비교'
  if (typeFilter.value === 'saving')  return '정기적금 금리 비교'
  return '예·적금 금리 비교'
})

// 헤더에 표시할 기간 배열
const selectedPeriods = computed(() =>
  periods.filter(p => periodFilter.value === 0 || p <= periodFilter.value)
)

// 행 데이터: 은행·타입 필터만 적용한 후, 기간별 rates 매핑
const displayList = computed(() => {
  const filtered = store.products.filter(p =>
    (!bankFilter.value || p.bank_name === bankFilter.value) &&
    (!typeFilter.value ||
      (typeFilter.value === 'deposit' && p.name.includes('예금')) ||
      (typeFilter.value === 'saving'  && p.name.includes('적금'))
    )
  )
  const map = {}
  filtered.forEach(p => {
    if (!map[p.product_id]) {
      map[p.product_id] = {
        id: p.id,
        product_id: p.product_id,
        bank_name: p.bank_name,
        name: p.name,
        rates: {}
      }
    }
    if (periods.includes(p.save_trm)) {
      map[p.product_id].rates[p.save_trm] = p.intr_rate
    }
  })
  return Object.values(map)
})
</script>

<style scoped>
.products-list { max-width: 900px; margin: 2rem auto; }
.filters { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem; }
.filters label { font-weight: 500; }
.filters select { padding: 0.4rem; border: 1px solid #ccc; border-radius: 4px; }
.rates-table { width: 100%; border-collapse: collapse; }
.rates-table th,
.rates-table td { border: 1px solid #ddd; padding: 0.75rem; text-align: center; }
.rates-table th { background: #f7f7f7; }
</style>
