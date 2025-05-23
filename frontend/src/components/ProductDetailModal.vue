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

        <!-- 선택된 상품의 금리 정보 -->
        <div class="rate-info">
          <div class="rate-item">
            <span class="rate-label">기본금리</span>
            <span class="rate-value">{{ selectedOption?.intr_rate.toFixed(2) }}%</span>
          </div>
          <div class="rate-item">
            <span class="rate-label">우대금리</span>
            <span class="rate-value preferential">{{ selectedOption?.intr_rate2.toFixed(2) }}%</span>
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
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

// 가장 높은 금리의 옵션 선택
const selectedOption = computed(() => {
  if (!props.product.options?.length) return null;
  return [...props.product.options].sort((a, b) => b.intr_rate2 - a.intr_rate2)[0];
});
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
  max-width: 600px;
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

.rate-info {
  display: flex;
  gap: 2rem;
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 8px;
}

.rate-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.rate-label {
  font-size: 0.875rem;
  color: #64748b;
}

.rate-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2563eb;
}

.rate-value.preferential {
  color: #16a34a;
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
</style>