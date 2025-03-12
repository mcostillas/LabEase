import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('labease_auth_token') || null)
  const userData = ref(JSON.parse(localStorage.getItem('labease_user_data') || 'null'))

  const isAuthenticated = computed(() => !!token.value)

  function setAuth(authToken, user) {
    token.value = authToken
    userData.value = user
    localStorage.setItem('labease_auth_token', authToken)
    localStorage.setItem('labease_user_data', JSON.stringify(user))
  }

  function clearAuth() {
    token.value = null
    userData.value = null
    localStorage.removeItem('labease_auth_token')
    localStorage.removeItem('labease_user_data')
  }

  return {
    token,
    userData,
    isAuthenticated,
    setAuth,
    clearAuth
  }
})
