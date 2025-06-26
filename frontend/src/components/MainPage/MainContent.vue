<template>
    <div class="main">
        <div class="panels">
            <div class="panels-left">
                <CategoriesButton :iconLeft="mdiLogout" :text="selectedCategory" />
                <PaceButton :text="paceOptions" :iconRight="mdiMenuDown" :withFilling="false" title="Pace" />
                <RestButton :text="restOptions" :iconRight="mdiMenuDown" :withFilling="false" title="Rest" />
            </div>
            <div class="panels-right">
                <ButtonOne :iconPath="mdiArrowExpand" @clickEvent="toggleFullscreen" size="md" />
            </div>
        </div>

        <div class="timer">
            <div class="time-center" :class="mode == 'focus' ? null : 'rest-timer'">
                <div class="digits">
                    <span class="digit">{{ minutesStr[0] }}</span>
                    <span class="digit">{{ minutesStr[1] }}</span>
                </div>
                <span class="separator">:</span>
                <div class="digits">
                    <span class="digit">{{ secondsStr[0] }}</span>
                    <span class="digit">{{ secondsStr[1] }}</span>
                </div>
            </div>
            <!-- <div class="rest-timer">
                Rest timer
            </div> -->
        </div>

        <div class="buttons">
            <div class="tooltip" data-tooltip="Play / Pause">
                <svg-icon class="button-icons" type="mdi" :path="isRunning ? mdiPause : mdiPlay" @click="toggleTimer" />
            </div>
            <div class="tooltip" data-tooltip="Stop and reset">
                <svg-icon class="button-icons" type="mdi" :path="mdiStop" @click="stopTimer" />
            </div>
            <div class="tooltip" data-tooltip="Reset">
                <svg-icon class="button-icons" type="mdi" :path="mdiAutorenew" @click="resetTimer" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { useCategoryStore } from '@/store/categories'
import { useTimerStore } from '@/store/timer'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiArrowExpand, mdiAutorenew, mdiLogout, mdiMenuDown, mdiPause, mdiPlay, mdiStop } from '@mdi/js'
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import ButtonOne from '../Buttons/ButtonOne.vue'
import CategoriesButton from '../Buttons/CategoriesButton.vue'
import PaceButton from '../Buttons/PaceButton.vue'
import RestButton from '../Buttons/RestButton.vue'

const isRunning = ref(false)
const startTimestamp = ref(0)
const elapsed = ref(0)

const categoryStore = useCategoryStore()
const selectedCategory = categoryStore.categories

const timerStore = useTimerStore()
const paceOptions = timerStore.paceOptions
const restOptions = timerStore.restOptions
const currentPace = computed(() => timerStore.currentPace)
const paceLimitMs = computed(() => currentPace.value * 60 * 1000)

const currentRest = computed(() => timerStore.currentRest)
const restLimitMs = computed(() => currentRest.value * 60 * 1000)


const mode = ref('focus')
const limitMs = computed(() =>
    mode.value === 'focus'
        ? timerStore.currentPace * 60 * 1000
        : timerStore.currentRest * 60 * 1000
)

const remainingTime = ref(paceLimitMs.value)

const update = () => {
    const passed = Date.now() - startTimestamp.value
    remainingTime.value = Math.max(limitMs.value - passed, 0)

    if (remainingTime.value <= 0) {
        pauseTimer()

        if (mode.value === "focus") {
            mode.value = "rest"
            remainingTime.value = restLimitMs.value
        } else {
            mode.value = "focus"
            remainingTime.value = paceLimitMs.value
        }
    }
}

let intervalId = null

const startTimer = () => {
    if (!isRunning.value) {
        isRunning.value = true
        startTimestamp.value = Date.now()
        intervalId = setInterval(update, 500)
    }
}
const pauseTimer = () => {
    isRunning.value = false
    clearInterval(intervalId)
}

const toggleTimer = () => {
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

const toggleFullscreen = () => {
    console.log("toggleFullscreen")
    // TODO: переход в полноэкранный режим здесь
}

watch(currentPace, (newVal) => {
    pauseTimer()
    remainingTime.value = newVal * 60 * 1000
})

onMounted(() => {
    const saved = localStorage.getItem('timerMilliseconds')
    if (saved !== null && !isNaN(parseFloat(saved))) {
        elapsed.value = parseFloat(saved)
    }
})

onBeforeUnmount(() => {
    pauseTimer()
})
</script>



<style scoped>
.main {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    height: 100%;
}

.panels {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 8px;

}

.panels-left {
    display: flex;
    flex-direction: row;
    gap: 17px;
}

.panels-right {
    height: 30px;
    width: 30px;
}

.timer {
    display: flex;
    justify-content: center;
    position: relative;
    font-family: 'Bruno_Ace', sans-serif;
}

.rest-timer {
    /* position: absolute;
    top: 100px; */
    color: var(--yellow);
}

.time-center {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    position: relative;
}

.time-seconds {
    position: absolute;
    /* top: 20px; */
    bottom: 15px;
    right: -60px;
    display: flex;
    gap: 0.25rem;
}

.digits {
    display: flex;
}

.digit {
    font-size: 64px;
    font-weight: 400;
    width: 60px;
    text-align: center;
}

.separator {
    font-size: 64px;
    font-weight: 400;
}

.seconds {
    font-size: 28px;
    font-weight: 400;
    color: var(--color-text-mute);
    width: 23px;
    text-align: center;
}

.expand-button {
    width: 35px;
    height: 35px;
}

.buttons {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    background-color: var(--color-background-soft);
    min-width: 200px;
    height: 60px;
    border-radius: var(--border-radius-8);
    transform: translateY(-10px);

}

.button-icons {
    height: 32px;
    width: auto;
    border-radius: 4px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.button-icons:hover {
    background-color: var(--color-background-soft);
    transform: scale(1.05);
    cursor: pointer;
}
</style>