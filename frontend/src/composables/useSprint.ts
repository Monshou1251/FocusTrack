//src\composables\useSprint.ts
import { sprintApi, SprintPayload } from '@/api/sprintApi'

import { useCategoryStore } from '@/store/categories'
import { useTimerStore } from '@/store/timer'

export async function saveSprint() {
  const timeStore = useTimerStore()
  const categoryStore = useCategoryStore()

  if (!categoryStore.selectedCategory) {
    throw new Error('Category is not selected')
  }

  if (timeStore.savedToDB) return
  if (!timeStore.hasEnoughFocus) return

  const payload: SprintPayload = {
    category: categoryStore.selectedCategory,
    duration: timeStore.getActualFocusDuration(),
    started_at: new Date().toISOString()
  }

  await sprintApi(payload)
  timeStore.savedToDB = true
}
