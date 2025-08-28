import type { JournalCreatePayload, JournalEntryDTO, JournalUpdatePayload } from '@/api/journal'
import {
  createJournalEntry,
  deleteJournalEntry,
  listJournalEntries,
  updateJournalEntry
} from '@/api/journal'
import { defineStore } from 'pinia'

type State = {
  entries: JournalEntryDTO[]
  isLoading: boolean
  error: string | null
}

export const useJournalStore = defineStore('journal', {
  state: (): State => ({ entries: [], isLoading: false, error: null }),
  actions: {
    async fetchEntries() {
      this.isLoading = true
      this.error = null
      try {
        const { data } = await listJournalEntries(false)
        this.entries = data
      } catch (e: any) {
        this.error = e?.message || 'Failed to load journal'
      } finally {
        this.isLoading = false
      }
    },
    async addEntry(payload: JournalCreatePayload) {
      const { data } = await createJournalEntry(payload)
      this.entries.unshift(data)
    },
    async editEntry(id: number, payload: JournalUpdatePayload) {
      const { data } = await updateJournalEntry(id, payload)
      const idx = this.entries.findIndex((e) => e.id === id)
      if (idx !== -1) this.entries[idx] = data
    },
    async removeEntry(id: number) {
      const { data } = await deleteJournalEntry(id)
      if (data === true || data?.deleted === true) {
        this.entries = this.entries.filter((e) => e.id !== id)
      }
    }
  }
})
