<template>
    <div class="buttons">
        <div class="tooltip" data-tooltip="Play / Pause">
            <svg-icon class="button-icons" type="mdi" :path="timerStore.isRunning ? mdiPause : mdiPlay"
                @click="timerStore.toggleTimer()" />
        </div>
        <div class="tooltip" data-tooltip="Stop and reset">
            <svg-icon class="button-icons" type="mdi" :path="mdiStop" @click="timerStore.stopTimer()" />
        </div>
        <div class="tooltip" data-tooltip="Reset">
            <svg-icon class="button-icons" type="mdi" :path="mdiAutorenew" @click="timerStore.resetTimer()" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useTimerStore } from '@/store/timer';
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiAutorenew, mdiPause, mdiPlay, mdiStop } from '@mdi/js';


const timerStore = useTimerStore()

</script>


<style scoped>
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
