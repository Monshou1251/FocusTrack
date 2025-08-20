//src\composables\useSprint.ts
import { sprintApi, SprintPayload } from '@/api/sprintApi'

import { useCategoryStore } from '@/store/categories'
import { useSprintStore } from '@/store/sprints'
import { useTimerStore } from '@/store/timer'

export async function saveSprint(opts?: { force?: boolean; payload?: SprintPayload }) {
  const timeStore = useTimerStore()
  const categoryStore = useCategoryStore()
  const sprintStore = useSprintStore()

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

  try {
    await sprintApi(payload)
    timeStore.savedToDB = true
    await sprintStore.fetchSprints()
  } catch (err: any) {
    // If unauthorized, queue locally to retry after re-login
    if (err?.response?.status === 401) {
      const queueRaw = localStorage.getItem('pending_sprints')
      const queue: SprintPayload[] = queueRaw ? JSON.parse(queueRaw) : []
      queue.push(payload)
      localStorage.setItem('pending_sprints', JSON.stringify(queue))
      // mark as not saved; will be flushed later
    }
    throw err
  }
}

export async function flushPendingSprints() {
  const queueRaw = localStorage.getItem('pending_sprints')
  if (!queueRaw) return
  let queue: SprintPayload[] = []
  try {
    queue = JSON.parse(queueRaw)
  } catch {
    localStorage.removeItem('pending_sprints')
    return
  }
  if (!Array.isArray(queue) || queue.length === 0) return
  const failed: SprintPayload[] = []
  for (const payload of queue) {
    try {
      await sprintApi(payload)
    } catch (e) {
      failed.push(payload)
    }
  }
  if (failed.length > 0) {
    localStorage.setItem('pending_sprints', JSON.stringify(failed))
  } else {
    localStorage.removeItem('pending_sprints')
  }
}
