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
            <div class="time-center">
                <div class="digits">
                    <span class="digit">{{ hoursStr[0] }}</span>
                    <span class="digit">{{ hoursStr[1] }}</span>
                </div>
                <span class="separator">:</span>
                <div class="digits">
                    <span class="digit">{{ minutesStr[0] }}</span>
                    <span class="digit">{{ minutesStr[1] }}</span>
                </div>
                <div class="time-seconds">
                    <span class="seconds">{{ secondsStr[0] }}</span>
                    <span class="seconds">{{ secondsStr[1] }}</span>
                </div>
            </div>
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
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiArrowExpand, mdiAutorenew, mdiLogout, mdiMenuDown, mdiPause, mdiPlay, mdiStop } from '@mdi/js'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import ButtonOne from '../Buttons/ButtonOne.vue'
import CategoriesButton from '../Buttons/CategoriesButton.vue'
import PaceButton from '../Buttons/PaceButton.vue'
import RestButton from '../Buttons/RestButton.vue'

const isRunning = ref(false)
const startTime = ref(0)
const elapsed = ref(0)
const milliseconds = ref(0)
let rafId = null
const categoryStore = useCategoryStore()
const selectedCategory = categoryStore.categories

const paceOptions = [15, 30, 45, 60, 75, 90]
const restOptions = [5, 10, 15, 20, 25, 30]

const update = () => {
    const now = performance.now()
    milliseconds.value = elapsed.value + (now - startTime.value)
    rafId = requestAnimationFrame(update)
}

const startTimer = () => {
    if (!isRunning.value) {
        isRunning.value = true
        startTime.value = performance.now()
        update()
    }
}

const pauseTimer = () => {
    if (isRunning.value) {
        isRunning.value = false
        elapsed.value += performance.now() - startTime.value
        cancelAnimationFrame(rafId)
        localStorage.setItem('timerMilliseconds', milliseconds.value.toString())
    }
}

const toggleTimer = () => {
    isRunning.value ? pauseTimer() : startTimer()
}

const resetTimer = () => {
    pauseTimer()
    milliseconds.value = 0
    elapsed.value = 0
    localStorage.removeItem('timerMilliseconds')
}

const stopTimer = () => {
    pauseTimer()
    console.log('TODO: send to backend', milliseconds.value)
    resetTimer()
}

const hours = computed(() => Math.floor(milliseconds.value / 3600000))
const minutes = computed(() => Math.floor(milliseconds.value / 60000) % 60)
const seconds = computed(() => Math.floor((milliseconds.value % 60000) / 1000))

const hoursStr = computed(() => hours.value.toString().padStart(2, '0'))
const minutesStr = computed(() => minutes.value.toString().padStart(2, '0'))
const secondsStr = computed(() => seconds.value.toString().padStart(2, '0'))

const toggleFullscreen = () => {
    console.log("toggleFullscreen")
    // Реализуй переход в полноэкранный режим здесь
}

onMounted(() => {
    const saved = localStorage.getItem('timerMilliseconds')
    if (saved !== null && !isNaN(parseFloat(saved))) {
        elapsed.value = parseFloat(saved)
        milliseconds.value = elapsed.value
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