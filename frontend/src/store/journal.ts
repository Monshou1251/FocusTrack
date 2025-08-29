import type { JournalCreatePayload, JournalEntryDTO, JournalUpdatePayload } from '@/api/journal'
import {
  createJournalEntry,
  deleteJournalEntry,
  listJournalEntries,
  updateJournalEntry
} from '@/api/journal'
import { defineStore } from 'pinia'
import { ref } from 'vue'

// type State = {
//   entries: JournalEntryDTO[]
//   isLoading: boolean
//   error: string | null
// }

export const useJournalStore = defineStore('journal', () => {
  let entries = ref<JournalEntryDTO[]>([])
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)
  const isJournalFullscreen = ref<boolean>(false)

  const toogleJournalFullscreen = () => {
    isJournalFullscreen.value = !isJournalFullscreen.value
    console.log('isJournalFullscreen.value')
    console.log(isJournalFullscreen.value)
  }

  async function fetchEntries() {
    isLoading.value = true
    error.value = null
    try {
      const { data } = await listJournalEntries(false)
      entries.value = data
    } catch (e: any) {
      error.value = e?.message || 'Failed to load journal'
    } finally {
      isLoading.value = false
    }
  }

  async function addEntry(payload: JournalCreatePayload) {
    const { data } = await createJournalEntry(payload)
    entries.value.unshift(data)
  }

  async function editEntry(id: number, payload: JournalUpdatePayload) {
    const { data } = await updateJournalEntry(id, payload)
    const idx = entries.value.findIndex((e) => e.id === id)
    if (idx !== -1) entries.value[idx] = data
  }

  async function removeEntry(id: number) {
    const { data } = await deleteJournalEntry(id)
    if (data === true || data?.deleted === true) {
      entries.value = entries.value.filter((e) => e.id !== id)
    }
  }

  return {
    entries,
    fetchEntries,
    addEntry,
    editEntry,
    removeEntry,
    isJournalFullscreen,
    toogleJournalFullscreen,
    isLoading
  }
})
