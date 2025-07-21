<template>
    <div class="main">
        <div class="panels">
            <div class="panels-left">
                <CategoriesButton :iconLeft="mdiLogout" :text="selectedCategory" />
                <PaceButton :iconRight="mdiMenuDown" :withFilling="false" title="Pace" />
                <RestButton :iconRight="mdiMenuDown" :withFilling="false" title="Rest" />
            </div>
            <div class="panels-right">
                <ButtonOne :iconPath="mdiArrowExpand" @clickEvent="toggleFullscreen" size="md" />
            </div>
        </div>

        <div class="timer">
            <div class="time-center" :class="phase == 'focus' ? null : 'rest-timer'">
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
            <div v-show="phase == 'rest'" class="rest-signal">
                Rest time
            </div>
        </div>

        <div class="buttons">
            <TimerControls />
        </div>
    </div>
</template>

<script setup lang="ts">
import TimerControls from '@/components/MainPage/TimerControls.vue'
import { useCategoryStore } from '@/store/categories'
import { useTimerStore } from '@/store/timer'
import { mdiArrowExpand, mdiLogout, mdiMenuDown } from '@mdi/js'
import { storeToRefs } from 'pinia'
import ButtonOne from '../Buttons/ButtonOne.vue'
import CategoriesButton from '../Buttons/CategoriesButton.vue'
import PaceButton from '../Buttons/PaceButton.vue'
import RestButton from '../Buttons/RestButton.vue'

const categoryStore = useCategoryStore()
const selectedCategory = categoryStore.categories

const timerStore = useTimerStore()

const {
    minutesStr,
    secondsStr,
    phase
} = storeToRefs(timerStore)


const toggleFullscreen = () => {
    console.log("toggleFullscreen")
    // TODO: переход в полноэкранный режим здесь
}
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

.rest-signal {
    position: absolute;
    top: 100px;
    color: var(--yellow);
    font-size: 18px;
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
</style>