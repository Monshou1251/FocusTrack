// sprintApi.ts
import { http } from '@/lib/http'

const SPRINT_ROOT = '/focus'

export type SprintPayload = {
  category: string
  duration: number
  started_at: string
}

export interface Sprint {
  id: string
  duration: string
  started_at: string
  category_id: string
}

export async function sprintApi(data: { category: string; duration: number; started_at: string }) {
  return http.post(`${SPRINT_ROOT}/save_sprint`, data)
}

export async function getSprintsApi() {
  return http.get(`${SPRINT_ROOT}/sprints`)
}
