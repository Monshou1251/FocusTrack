// src/store/auth.js
import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const username = ref(null)
  const email = ref(null)
  const avatarUrl = ref(null)
  const DEFAULT_AVATAR_URL = 'https://i.pravatar.cc/100?img=5'

  const fetchCurrentUser = async () => {
    const res = await axios.get('/api/auth/me', { withCredentials: true })
    const user = res.data

    username.value = user.username
    email.value = user.email
    avatarUrl.value = user.avatar_url || DEFAULT_AVATAR_URL
  }

  const logout = async () => {
    await axios.post('/api/auth/logout', null, { withCredentials: true })
    username.value = null
    email.value = null
    avatarUrl.value = null
  }

  return {
    username,
    email,
    avatarUrl,
    fetchCurrentUser,
    logout,
    isAuthenticated: computed(() => !!username.value)
  }
})
