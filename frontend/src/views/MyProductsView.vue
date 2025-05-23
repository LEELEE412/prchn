<template>
  <div class="my-products">
    <h2>내가 가입한 상품</h2>
    <ul v-if="myList.length">
      <li v-for="p in myList" :key="p.id">
        <RouterLink :to="{ name: 'ProductsDetail', params: { id: p.id } }">
          {{ p.bank_name }} – {{ p.name }}
        </RouterLink>
      </li>
    </ul>
    <p v-else>아직 가입한 상품이 없습니다.</p>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useProductStore } from '@/stores/productStore'
import { useUserStore }    from '@/stores/userStore'

const productStore = useProductStore()
const userStore    = useUserStore()

onMounted(() => {
  if (!productStore.products.length) {
    productStore.fetchProducts()
  }
})

const myList = computed(() =>
  productStore.products.filter(p =>
    userStore.subscribed.includes(p.id)
  )
)
</script>

<style scoped>
.my-products {
  max-width: 800px;
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

.my-products ul {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.my-products li {
  background-color: #f7f9fc;
  border: 1px solid #e0e6ed;
  border-radius: 6px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.my-products li:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.my-products li a {
  display: block;
  padding: 1rem 1.25rem;
  color: #333333;
  font-weight: 500;
  text-decoration: none;
}

.my-products li a:hover {
  color: #0073e6;
}

.my-products p {
  text-align: center;
  color: #666666;
  margin-top: 2rem;
}
</style>

