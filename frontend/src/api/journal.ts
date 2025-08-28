import { http } from '@/lib/http'

const JOURNAL_ROOT = '/journal'

export type JournalCreatePayload = {
  title: string
  content: string
}

export type JournalUpdatePayload = Partial<JournalCreatePayload>

export interface JournalEntryDTO {
  id: number
  title: string
  content: string
  created_at: string
  user_id: number
}

export async function listJournalEntries(include_archived = false) {
  return http.get(`${JOURNAL_ROOT}/entries`, { params: { include_archived } })
}

export async function createJournalEntry(data: JournalCreatePayload) {
  return http.post(`${JOURNAL_ROOT}/entries`, data)
}

export async function getJournalEntry(id: number) {
  return http.get(`${JOURNAL_ROOT}/entries/${id}`)
}

export async function updateJournalEntry(id: number, data: JournalUpdatePayload) {
  return http.put(`${JOURNAL_ROOT}/entries/${id}`, data)
}

export async function deleteJournalEntry(id: number) {
  return http.delete(`${JOURNAL_ROOT}/entries/${id}`)
}

export async function searchJournalEntries(q: string, include_archived = false) {
  return http.get(`${JOURNAL_ROOT}/search`, { params: { q, include_archived } })
}
