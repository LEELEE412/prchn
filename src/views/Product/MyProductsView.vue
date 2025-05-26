```vue
<template>
  <div class="my-products">
    <h2>내가 가입한 상품</h2>
    
    <div v-if="myList.length" class="products-grid">
      <div
        v-for="product in myList"
        :key="product.id"
        class="product-card"
        @click="showProductDetail(product)"
      >
        <div class="product-info">
          <h3>{{ product.bank_name }}</h3>
          <p>{{ product.name }}</p>
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
import { onMounted, ref, computed } from 'vue'
import { useProductStore } from '@/stores/productStore'
import { useUserStore } from '@/stores/userStore'
import ProductDetailModal from '@/components/ProductDetailModal.vue'

const productStore = useProductStore()
const userStore = useUserStore()
const selectedProduct = ref(null)

onMounted(() => {
  if (!productStore.products.length) {
    productStore.fetchProducts()
  }
})

const myList = computed(() =>
  productStore.products.filter(p =>
    userStore.subscribed?.includes(p.id)
  )
)

function showProductDetail(product) {
  selectedProduct.value = product
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

.product-info p {
  color: #666;
  font-size: 1rem;
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
```