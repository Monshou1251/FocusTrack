import axios from 'axios'

const rawBase = import.meta.env.VITE_API_URL ?? '/api'
const baseURL = String(rawBase).replace(/\/$/, '')

export const http = axios.create({
  baseURL,
  timeout: 10000,
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' }
})
