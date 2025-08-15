//src\composables\useSprint.ts
import { sprintApi, SprintPayload } from '@/api/sprintApi'

import { useCategoryStore } from '@/store/categories'
import { useTimerStore } from '@/store/timer'

export async function saveSprint(opts?: { force?: boolean; payload?: SprintPayload }) {
  const timeStore = useTimerStore()
  const categoryStore = useCategoryStore()

  if (!categoryStore.selectedCategory) {
    throw new Error('Category is not selected')
  }

  if (!opts?.force) {
    if (timeStore.savedToDB) return
    if (!timeStore.hasEnoughFocus) return
  }

  const payload: SprintPayload = opts?.payload ?? {
    category: categoryStore.selectedCategory.name,
    duration: timeStore.getActualFocusDuration(),
    started_at: new Date().toISOString()
  }

  await sprintApi(payload)
  timeStore.savedToDB = true
}
