import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/lib/axios";

export const useUserStore = defineStore("user", () => {
  const token    = ref(localStorage.getItem("token") || "");
  const userId   = ref(localStorage.getItem("userId") || null);
  const username = ref(localStorage.getItem("username") || "");
  const subscribed = ref([]);  // 초기화 추가

  const isLogin = computed(() => !!token.value)

  function _saveToken(t) {
    token.value = t;
    localStorage.setItem("token", t);
  }
  function _saveUserId(id) {
    userId.value = id;
    localStorage.setItem("userId", id);
  }
  function _saveUsername(u) {
    username.value = u;
    localStorage.setItem("username", u);
  }

  function _clearAll() {
    token.value = "";
    userId.value = null;
    username.value = "";
    subscribed.value = [];  // 구독 정보도 초기화
    localStorage.removeItem("token");
    localStorage.removeItem("userId");
    localStorage.removeItem("username");
  }

  async function logIn({ username: u, password }) {
    const res = await api.post("/api-token-auth/", { username: u, password });
    _saveToken(res.data.token);

    const me = await api.get("/accounts/profile/");
    _saveUserId(me.data.pk ?? me.data.id);
    _saveUsername(me.data.username);
    
    // 구독 정보 로드
    const products = await api.get("/api/v1/products/");
    subscribed.value = products.data.filter(p => p.is_subscribed).map(p => p.id);
  }

  async function signUp(payload) {
    await api.post("/accounts/registration/", payload);
  }

  async function subscribe(productId) {
    await api.post(`/api/v1/products/${productId}/subscribe/`);
    subscribed.value.push(Number(productId));
  }

  function logOut() {
    _clearAll();
  }

  return {
    token,
    userId,
    username,
    subscribed,
    isLogin,
    logIn,
    signUp,
    subscribe,
    logOut,
  };
});