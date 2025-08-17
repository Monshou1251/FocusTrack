// sprintApi.ts
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'

export async function sprintApi(data: { category: string; duration: number; started_at: string }) {
  return axios.post(`${API_BASE}/focus/save_sprint`, data)
}

export async function getSprintsApi() {
  return axios.get(`${API_BASE}/focus/sprints`)
}

export type SprintPayload = {
  category: string
  duration: number
  started_at: string
}

export interface Sprint {
  id: string
  duration: string
  started_at: string
}
