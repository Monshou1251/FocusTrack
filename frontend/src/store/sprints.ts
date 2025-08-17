import { getSprintsApi, Sprint } from '@/api/sprintApi'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useSprintStore = defineStore('sprints', () => {
  const sprints = ref<Sprint[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchSprints = async () => {
    try {
      isLoading.value = true
      error.value = null
      const response = await getSprintsApi()
      sprints.value = response.data.sprints
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch sprints'
      console.error('Error fetching sprints:', err)
    } finally {
      isLoading.value = false
    }
  }

  const addSprint = (sprint: Sprint) => {
    sprints.value.push(sprint)
  }

  const clearSprints = () => {
    sprints.value = []
    error.value = null
  }

  const getCalendarData = computed(() => {
    const data: Record<string, number> = {}

    sprints.value.forEach((sprint) => {
      const date = new Date(sprint.started_at).toISOString().split('T')[0]
      data[date] = (data[date] || 0) + 1
    })

    return data
  })

  return {
    sprints,
    isLoading,
    error,
    fetchSprints,
    addSprint,
    clearSprints,
    getCalendarData
  }
})
