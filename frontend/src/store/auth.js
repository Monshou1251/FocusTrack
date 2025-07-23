// src/store/auth.js
import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'

export const useAuthStore = defineStore('auth', () => {
  const username = ref(null)
  const email = ref(null)
  const avatarUrl = ref(null)
  const DEFAULT_AVATAR_URL = 'https://i.pravatar.cc/100?img=5'

  const fetchCurrentUser = async () => {
    const res = await axios.get(`${API_BASE}/auth/me`, { withCredentials: true })
    const user = res.data

    username.value = user.username
    email.value = user.email
    avatarUrl.value = user.avatar_url || DEFAULT_AVATAR_URL
  }

  const logout = async () => {
    await axios.post(`${API_BASE}/auth/logout`, null, { withCredentials: true })
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
