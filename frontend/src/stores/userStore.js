import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/lib/axios";

export const useUserStore = defineStore("user", () => {
  const token = ref(localStorage.getItem("token") || "");
  const userId = ref(localStorage.getItem("userId") || null);
  const username = ref(localStorage.getItem("username") || "");
  const subscribed_deposit_products = ref([]);
  const subscribed_saving_products = ref([]);

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
    subscribed_deposit_products.value = [];
    subscribed_saving_products.value = [];
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
    
    subscribed_deposit_products.value = me.data.subscribed_deposit_products || [];
    subscribed_saving_products.value = me.data.subscribed_saving_products || [];
  }

  async function signUp(payload) {
    await api.post("/accounts/registration/", payload);
  }

  function logOut() {
    _clearAll();
  }

  return {
    token,
    userId,
    username,
    subscribed_deposit_products,
    subscribed_saving_products,
    isLogin,
    logIn,
    signUp,
    logOut,
  };
});