<template>
    <div class="buttons" :class="{ 'fullscreen': isFullscreen }">
        <div ref="playButtonRef" class="button-wrapper">
            <svg-icon class="button-icons" type="mdi" :path="timerStore.isRunning ? mdiPause : mdiPlay"
                @click="timerStore.toggleTimer()" />
        </div>
        <div ref="stopButtonRef" class="button-wrapper">
            <svg-icon class="button-icons" type="mdi" :path="mdiStop" @click="timerStore.stopTimer()" />
        </div>
        <div ref="resetButtonRef" class="button-wrapper">
            <svg-icon class="button-icons" type="mdi" :path="mdiAutorenew" @click="timerStore.resetTimer()" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useTimerStore } from '@/store/timer';
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiAutorenew, mdiPause, mdiPlay, mdiStop } from '@mdi/js';
import { storeToRefs } from 'pinia';
import tippy from 'tippy.js';
import 'tippy.js/dist/tippy.css';
import { onBeforeUnmount, onMounted, ref } from 'vue';

const timerStore = useTimerStore()
const { isFullscreen } = storeToRefs(timerStore)

const playButtonRef = ref(null);
const stopButtonRef = ref(null);
const resetButtonRef = ref(null);

let tippyInstances: any[] = [];

onMounted(() => {
    // Initialize tooltips
    if (playButtonRef.value) {
        tippyInstances.push(tippy(playButtonRef.value, {
            content: 'Play / Pause',
            placement: 'top',
            arrow: true,
            theme: 'custom',
            animation: 'scale',
            duration: [0, 0],
            zIndex: 9999
        }));
    }

    if (stopButtonRef.value) {
        tippyInstances.push(tippy(stopButtonRef.value, {
            content: 'Stop and reset',
            placement: 'top',
            arrow: true,
            theme: 'custom',
            animation: 'scale',
            duration: [0, 0],
            zIndex: 9999
        }));
    }

    if (resetButtonRef.value) {
        tippyInstances.push(tippy(resetButtonRef.value, {
            content: 'Reset',
            placement: 'top',
            arrow: true,
            theme: 'custom',
            animation: 'scale',
            duration: [0, 0],
            zIndex: 9999
        }));
    }
});

onBeforeUnmount(() => {
    tippyInstances.forEach(instance => {
        if (instance) {
            instance.destroy();
        }
    });
});
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
    margin-bottom: 28px;
    transition: opacity 0.3s ease, background-color 0.3s ease;
}

.buttons.fullscreen {
    margin-bottom: 0;
    transform: none;
}

.button-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
}

.button-icons {
    height: 32px;
    width: auto;
    border-radius: 8px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.button-icons:hover {
    background-color: var(--color-background-soft);
    transform: scale(1.05);
    cursor: pointer;
}
</style>

<style>
/* Custom tippy theme for timer controls */
.tippy-box[data-theme~='custom'] {
    background-color: #333;
    color: white;
    border-radius: 6px;
    font-size: 12px;
    padding: 6px 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.tippy-box[data-theme~='custom'] .tippy-arrow {
    color: #333;
}

.tippy-box[data-theme~='custom'] .tippy-content {
    padding: 0;
}
</style>
