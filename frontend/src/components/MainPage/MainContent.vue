<template>
    <div class="main">

        <div class="panels">
            <div class="panels-left">
                <div>
                    <AppButton text="Category" :iconRight="mdiMenuDown" :iconLeft="mdiLogout" :withFilling="true"
                        :noShadow="false" />
                </div>
                <div>
                    <AppButton text="45" :iconRight="mdiMenuDown" :withFilling="false" :noShadow="false" title="Pace" />
                </div>
                <div>
                    <AppButton text="45" :iconRight="mdiMenuDown" :withFilling="false" :noShadow="false" title="Rest" />
                </div>
            </div>
            <div class="panels-right">
                <div class="expand-button">
                    <ButtonOne :iconPath="mdiArrowExpand" @clickEvent="toggleFullscreen" />
                </div>
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
                <svg-icon class="button-icons" type="mdi" :path="isRunning ? mdiPause : mdiPlay"
                    @click="isRunning ? pauseTimer() : startTimer()" />
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
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiArrowExpand, mdiAutorenew, mdiLogout, mdiMenuDown, mdiPause, mdiPlay, mdiStop } from '@mdi/js'
import AppButton from '../Buttons/AppButton.vue'
import ButtonOne from '../Buttons/ButtonOne.vue'

import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

const milliseconds = ref(0)
const isRunning = ref(false)
let intervalId = null

const toggleFullscreen = () => {
    console.log("toggleFullscreen")
    // TODO: Add expand, make main content area take the whole screen
}

const startTimer = () => {
    if (!isRunning.value) {
        isRunning.value = true
        intervalId = setInterval(() => {
            milliseconds.value += 10
        }, 10)
    }
}

const pauseTimer = () => {
    isRunning.value = false
    clearInterval(intervalId)
    localStorage.setItem('timerMilliseconds', milliseconds.value.toString())
}

const resetTimer = () => {
    pauseTimer()
    milliseconds.value = 0
    localStorage.removeItem('timerMilliseconds')
}

const stopTimer = () => {
    pauseTimer()
    console.log('TODO: send to backend', milliseconds.value)
    milliseconds.value = 0
    localStorage.removeItem('timerMilliseconds')
}

const hours = computed(() => Math.floor(milliseconds.value / 3600000))
const minutes = computed(() => Math.floor(milliseconds.value / 60000))
const seconds = computed(() => Math.floor((milliseconds.value % 60000) / 1000))

const hoursStr = computed(() => hours.value.toString().padStart(2, '0'))
const minutesStr = computed(() => minutes.value.toString().padStart(2, '0'))
const secondsStr = computed(() => seconds.value.toString().padStart(2, '0'))

onMounted(() => {
    const saved = localStorage.getItem('timerMilliseconds')
    if (saved !== null && !isNaN(parseInt(saved))) {
        milliseconds.value = parseInt(saved)
    }
})
onBeforeUnmount(() => {
    clearInterval(intervalId)
    if (milliseconds.value > 0) {
        localStorage.setItem('timerMilliseconds', milliseconds.value.toString())
    }
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
    bottom: 13px;
    right: -75px;
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
    font-size: 32px;
    font-weight: 400;
    color: var(--color-text-mute);
    width: 30px;
    text-align: center;
}

.expand-button {
    width: 40px;
    height: 40px;
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
    /* чуть увеличиваем */
    cursor: pointer;
}

.tooltip {
    position: relative;
    display: inline-block;
    display: flex;
}

.tooltip::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 135%;
    /* немного выше кнопки */
    left: 50%;
    transform: translateX(-50%);
    background-color: #333;
    color: white;
    padding: 6px 10px;
    border-radius: 4px;
    white-space: nowrap;
    font-size: 12px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease, transform 0.3s ease;
    z-index: 100;
}

.tooltip:hover::after {
    opacity: 1;
    transform: translateX(-50%) translateY(-4px);
}
</style>