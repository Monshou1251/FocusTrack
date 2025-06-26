import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useTimerStore = defineStore('timer', () => {
  const paceOptions = ref([0.1, 15, 30, 45, 60, 75, 90])
  const currentPace = ref(paceOptions.value[0])

  const restOptions = ref([0.2, 5, 10, 15, 20, 25, 30])
  const currentRest = ref(restOptions.value[0])

  const phase = ref('focus')

  return {
    paceOptions,
    currentPace,
    restOptions,
    currentRest,
    phase
  }
})
