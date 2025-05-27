<template>
  <!-- Previous template code unchanged -->
</template>

<script setup>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import api from '@/lib/axios';
import dayjs from 'dayjs';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close', 'subscribe']);
const router = useRouter();
const userStore = useUserStore();

// 날짜 관련 상태
const today = dayjs().format('YYYY-MM-DD');
const startDate = ref(today);
const endDate = ref('');
const selectedTerm = ref(null);

// 가입기간 순으로 정렬된 옵션
const sortedOptions = computed(() => {
  return [...(props.product.options || [])].sort((a, b) => a.save_trm - b.save_trm);
});

// 이미 구독된 상품인지 체크
const isSubscribed = computed(() => {
  const isSavingProduct = props.product.fin_prdt_cd?.startsWith('S');
  if (isSavingProduct) {
    return userStore.subscribed_saving_products?.some(p => p.fin_prdt_cd === props.product.fin_prdt_cd);
  }
  return userStore.subscribed_deposit_products?.some(p => p.fin_prdt_cd === props.product.fin_prdt_cd);
});

// 가입 가능 여부 체크
const isValidSubscription = computed(() => {
  return startDate.value && endDate.value && selectedTerm.value;
});

// 종료일 자동 계산
function updateEndDate() {
  if (startDate.value && selectedTerm.value) {
    endDate.value = dayjs(startDate.value)
      .add(selectedTerm.value, 'month')
      .format('YYYY-MM-DD');
  }
}

// 가입하기 핸들러
async function onSubscribe() {
  const subscriptionData = {
    term_months: selectedTerm.value,
    start_date: startDate.value,
    end_date: endDate.value
  };

  try {
    const isSavingProduct = props.product.fin_prdt_cd?.startsWith('S');
    const endpoint = isSavingProduct ? 'saving-products' : 'deposit-products';
    
    await api.post(`/products/${endpoint}/subscribe/${props.product.fin_prdt_cd}/`, subscriptionData);
    router.push('/my-products');
  } catch (err) {
    console.error('Subscription failed:', err);
    alert('상품 가입 중 오류가 발생했습니다.');
  }
}

// 가입 취소 핸들러
async function onUnsubscribe() {
  try {
    const isSavingProduct = props.product.fin_prdt_cd?.startsWith('S');
    const endpoint = isSavingProduct ? 'saving-products' : 'deposit-products';
    
    await api.delete(`/products/${endpoint}/subscribe/${props.product.fin_prdt_cd}/`);
    router.push('/my-products');
  } catch (err) {
    console.error('Unsubscribe failed:', err);
    alert('가입 취소 중 오류가 발생했습니다.');
  }
}
</script>

<style scoped>
/* Previous styles unchanged */
</style>