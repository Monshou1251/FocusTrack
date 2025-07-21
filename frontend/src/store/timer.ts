import { defineStore } from 'pinia'
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const STORAGE_KEYS = {
  pace: 'currentPace',
  rest: 'currentRest',
  phase: 'timerPhase',
  timer: 'currentTimer'
}

export const useTimerStore = defineStore('timer', () => {
  const paceOptions = ref<number[]>([0.1, 15, 30, 45, 60, 75, 90])
  const restOptions = ref<number[]>([0.05, 5, 10, 15, 20, 25, 30])

  const currentPace = ref<number>(
    Number(localStorage.getItem(STORAGE_KEYS.pace)) || paceOptions.value[0]
  )
  console.log('currentPace:', currentPace.value)
  const currentRest = ref<number>(
    Number(localStorage.getItem(STORAGE_KEYS.rest)) || restOptions.value[0]
  )

  const phase = ref<'focus' | 'rest'>(
    (localStorage.getItem(STORAGE_KEYS.phase) as 'focus' | 'rest') || 'focus'
  )

  const isRunning = ref(false)
  const remainingTime = ref(currentPace.value * 60 * 1000)
  const startTimestamp = ref(0)
  let manuallyPaused = false

  let intervalId: ReturnType<typeof setInterval> | null = null

  const limitMs = computed(() =>
    phase.value === 'focus' ? currentPace.value * 60 * 1000 : currentRest.value * 60 * 1000
  )

  const update = () => {
    const elapsed = Date.now() - startTimestamp.value
    remainingTime.value = Math.max(limitMs.value - elapsed, 0)

    if (remainingTime.value <= 0) {
      pauseTimer()

      phase.value = phase.value === 'focus' ? 'rest' : 'focus'
      remainingTime.value = limitMs.value
    }
  }

  const actualLimitMs = ref(limitMs.value)

  const startTimer = () => {
    if (isRunning.value) return

    isRunning.value = true
    startTimestamp.value = Date.now() - (limitMs.value - remainingTime.value)

    intervalId = setInterval(update, 100)
  }

  let pausedRemaining: number | null = null

  const pauseTimer = () => {
    if (!isRunning.value) return

    isRunning.value = false
    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
    }
  }

  const toggleTimer = () => {
    if (isRunning.value) {
      manuallyPaused = true
      pauseTimer()
      manuallyPaused = false
    } else {
      startTimer()
    }
  }

  const resetTimer = () => {
    console.log('Timer reseted')

    pauseTimer()

    phase.value = 'focus'
    pausedRemaining = null

    actualLimitMs.value = limitMs.value
    remainingTime.value = actualLimitMs.value
  }

  const resetRestTimer = () => {
    console.log('Rest Timer reseted')

    pauseTimer()

    // phase.value = 'focus'
    pausedRemaining = null

    actualLimitMs.value = limitMs.value
    remainingTime.value = actualLimitMs.value
  }

  const stopTimer = () => {
    pauseTimer()
    resetTimer()
  }

  const minutesStr = computed(() => {
    const mins = Math.floor(remainingTime.value / 60000)
    return mins.toString().padStart(2, '0')
  })

  const secondsStr = computed(() => {
    const secs = Math.floor((remainingTime.value % 60000) / 1000)
    return secs.toString().padStart(2, '0')
  })

  watch(currentPace, (newVal) => {
    pauseTimer()
    remainingTime.value = newVal * 60 * 1000
    localStorage.setItem(STORAGE_KEYS.pace, String(newVal))
    console.log('currentPace changed: ', newVal)
  })

  watch(currentRest, (val) => {
    localStorage.setItem(STORAGE_KEYS.rest, String(val))
  })

  watch(phase, (val) => {
    localStorage.setItem(STORAGE_KEYS.phase, val)
  })

  onMounted(() => {
    const savedPace = localStorage.getItem(STORAGE_KEYS.pace)
    console.log('savedPace: ', savedPace)
    if (savedPace !== null && !isNaN(parseFloat(savedPace))) {
      currentPace.value = parseFloat(savedPace)
    }

    const savedRest = localStorage.getItem(STORAGE_KEYS.rest)
    console.log('savedRest: ', savedRest)
    if (savedRest !== null && !isNaN(parseFloat(savedRest))) {
      currentRest.value = parseFloat(savedRest)
    }

    const savedTime = localStorage.getItem(STORAGE_KEYS.timer)
    if (savedTime) {
      remainingTime.value = parseInt(savedTime)
    }
    window.addEventListener('beforeunload', saveTimerToStorage)
  })

  onMounted(() => {})

  onBeforeUnmount(() => {
    window.removeEventListener('beforeunload', saveTimerToStorage)
  })

  function saveTimerToStorage() {
    pauseTimer()
    localStorage.setItem(STORAGE_KEYS.timer, String(remainingTime.value))
    localStorage.setItem(STORAGE_KEYS.phase, phase.value)
  }

  return {
    // state
    paceOptions,
    currentPace,
    restOptions,
    currentRest,
    phase,
    isRunning,
    remainingTime,
    minutesStr,
    secondsStr,
    actualLimitMs,

    // actions
    toggleTimer,
    resetTimer,
    stopTimer,
    pauseTimer,
    startTimer,
    resetRestTimer
  }
})
