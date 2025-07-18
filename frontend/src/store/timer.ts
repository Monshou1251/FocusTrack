import { defineStore } from 'pinia'
import { computed, onMounted, ref, watch } from 'vue'

const STORAGE_KEYS = {
  pace: 'currentPace',
  rest: 'currentRest',
  phase: 'timerPhase'
}

export const useTimerStore = defineStore('timer', () => {
  const paceOptions = ref<number[]>([0.1, 15, 30, 45, 60, 75, 90])
  const restOptions = ref<number[]>([0.2, 5, 10, 15, 20, 25, 30])

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

  let intervalId: ReturnType<typeof setInterval> | null = null

  const limitMs = computed(() =>
    phase.value === 'focus' ? currentPace.value * 60 * 1000 : currentRest.value * 60 * 1000
  )

  const paceLimitMs = computed(() => currentPace.value * 60 * 1000)
  const restLimitMs = computed(() => currentRest.value * 60 * 1000)

  const update = () => {
    const passed = Date.now() - startTimestamp.value
    remainingTime.value = Math.max(actualLimitMs.value - passed, 0)

    if (remainingTime.value <= 0) {
      pauseTimer()

      if (phase.value === 'focus') {
        phase.value = 'rest'
        actualLimitMs.value = restLimitMs.value
        remainingTime.value = actualLimitMs.value
      } else {
        phase.value = 'focus'
        actualLimitMs.value = paceLimitMs.value
        remainingTime.value = actualLimitMs.value
      }
    }
  }

  const actualLimitMs = ref(limitMs.value) // будет использоваться в таймере

  watch([phase, currentPace, currentRest], () => {
    if (!isRunning.value) {
      actualLimitMs.value = limitMs.value
    }
  })

  const startTimer = () => {
    if (!isRunning.value) {
      isRunning.value = true
      startTimestamp.value = Date.now()

      if (pausedRemaining !== null) {
        actualLimitMs.value = pausedRemaining
        pausedRemaining = null
      }

      intervalId = setInterval(update, 100)
    }
  }

  let pausedRemaining: number | null = null

  const pauseTimer = () => {
    if (isRunning.value) {
      isRunning.value = false
      if (intervalId !== null) {
        clearInterval(intervalId)
        intervalId = null
      }
      // сохраняем сколько осталось
      pausedRemaining = remainingTime.value
    }
  }

  const toggleTimer = () => {
    console.log('Toggling timer')
    isRunning.value ? pauseTimer() : startTimer()
  }

  const resetTimer = () => {
    pauseTimer()
    remainingTime.value = paceLimitMs.value
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
    // Восстановить текущий pace (в минутах)
    const savedPace = localStorage.getItem(STORAGE_KEYS.pace)
    if (savedPace !== null && !isNaN(parseFloat(savedPace))) {
      currentPace.value = parseFloat(savedPace)
    }

    // Восстановить оставшееся время таймера
    const savedTime = localStorage.getItem(STORAGE_KEYS.phase)
    console.log('savedTime: ', savedTime)
    if (savedTime !== null && !isNaN(parseFloat(savedTime))) {
      remainingTime.value = parseFloat(savedTime)
    } else {
      remainingTime.value = currentPace.value * 60 * 1000
    }
  })

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

    // actions
    toggleTimer,
    resetTimer,
    stopTimer,
    pauseTimer,
    startTimer
  }
})
