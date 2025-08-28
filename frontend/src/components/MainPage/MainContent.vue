<template>
    <div class="main" :class="{ 'fullscreen': isFullscreen }">
        <!-- Panels - hidden in fullscreen mode -->
        <div v-show="!isFullscreen" class="panels">
            <div class="panels-left">
                <CategoriesButton :iconLeft="mdiLogout" :text="selectedCategory?.name || 'Select Category'"
                    :categories="categories" :selectedCategory="selectedCategory" />
                <PaceButton :iconRight="mdiMenuDown" :withFilling="false" title="Pace" />
                <RestButton :iconRight="mdiMenuDown" :withFilling="false" title="Rest" />
            </div>
            <div class="panels-right">
                <ButtonOne :iconPath="mdiArrowExpand" @clickEvent="toggleFullscreen" size="md"
                    tooltip="Enter fullscreen" />
            </div>
        </div>

        <!-- Fullscreen exit button - visible only in fullscreen mode -->
        <div v-show="isFullscreen" class="fullscreen-exit">
            <ButtonOne :iconPath="mdiArrowCollapse" @clickEvent="toggleFullscreen" size="md" class="exit-button"
                tooltip="Exit fullscreen" />
        </div>

        <div class="timer">
            <!-- Mode indicator -->
            <div class="mode-indicator" :class="phase"
                :style="phase === 'focus' ? { '--focus-shadow': `0 4px 12px ${hexToRgba(selectedCategoryColor, 0.35)}` } : {}">
                <span class="mode-text">{{ phase === 'focus' ? 'Focus' : 'Rest' }}</span>
                <div class="mode-icon" :class="phase">
                    <svg v-if="phase === 'focus'" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path
                            d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                    </svg>
                    <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path
                            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                    </svg>
                </div>
            </div>

            <div class="time-center" :class="phase">
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
        </div>

        <div class="timer-controls-container" :class="{ 'fullscreen-controls': isFullscreen }">
            <TimerControls />
        </div>
    </div>
</template>

<script setup lang="ts">
import TimerControls from '@/components/MainPage/TimerControls.vue'
import { useCategoryStore } from '@/store/categories'
import { useTimerStore } from '@/store/timer'
import { mdiArrowCollapse, mdiArrowExpand, mdiLogout, mdiMenuDown } from '@mdi/js'
import { storeToRefs } from 'pinia'
import { computed } from 'vue'
import ButtonOne from '../Buttons/ButtonOne.vue'
import CategoriesButton from '../Buttons/CategoriesButton.vue'
import PaceButton from '../Buttons/PaceButton.vue'
import RestButton from '../Buttons/RestButton.vue'

const categoryStore = useCategoryStore()
const { categories, selectedCategory } = storeToRefs(categoryStore)

const timerStore = useTimerStore()

const {
    minutesStr,
    secondsStr,
    phase,
    isFullscreen
} = storeToRefs(timerStore)

const { toggleFullscreen } = timerStore

const selectedCategoryColor = computed(() => {
    if (!selectedCategory.value) return '#007bff'
    const idx = categories.value.findIndex(c => c.id === selectedCategory.value?.id)
    const safeIndex = idx >= 0 ? idx : 0
    return categoryStore.getColorByIndex(safeIndex)
})

function hexToRgba(hex: string, alpha: number): string {
    const sanitized = hex.replace('#', '')
    const bigint = parseInt(sanitized.length === 3
        ? sanitized.split('').map(c => c + c).join('')
        : sanitized, 16)
    const r = (bigint >> 16) & 255
    const g = (bigint >> 8) & 255
    const b = bigint & 255
    return `rgba(${r}, ${g}, ${b}, ${alpha})`
}
</script>



<style scoped>
.main {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    min-height: 100%;
    transition: opacity 0.3s ease;
    position: relative;
}

.main.fullscreen {
    justify-content: center;
    gap: 40px;
    min-height: 100vh;
    height: auto;
    padding-bottom: 20px;
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

/* Fullscreen exit button */
.fullscreen-exit {
    position: absolute;
    top: 20px;
    right: 20px;
    z-index: 100;
    padding: 10px;
}

.exit-button {
    opacity: 0.3;
    transition: all 0.3s ease;
}

.exit-button:hover {
    opacity: 1;
    transform: scale(1.1);
}

.timer {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
    font-family: 'Bruno_Ace', sans-serif;
    gap: 32px;
    flex-shrink: 0;
    transition: opacity 0.3s ease;
    padding-bottom: 18px;
}

/* Mode indicator styles */
.mode-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    margin-top: 10px;
}

.mode-indicator.focus {
    background: linear-gradient(135deg, var(--primary-color), var(--primary-color-dark));
    color: white;
    box-shadow: var(--focus-shadow, 0 4px 12px rgba(0, 123, 255, 0.3));
}

.mode-indicator.rest {
    background: linear-gradient(135deg, var(--yellow), #ffd700);
    color: #333;
    box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
}

.mode-text {
    font-weight: 600;
}

.mode-icon {
    display: flex;
    align-items: center;
    justify-content: center;
}

.time-center {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    position: relative;
    transition: all 0.3s ease;
}

.time-center.focus {
    /* Focus mode - keep default styling */
}

.time-center.rest {
    /* Rest mode - subtle visual changes */
    opacity: 0.9;
    transform: scale(0.98);
}

.time-seconds {
    position: absolute;
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
    transition: all 0.3s ease;
}

.separator {
    font-size: 64px;
    font-weight: 400;
    transition: all 0.3s ease;
}

/* Bigger timer in fullscreen */
.main.fullscreen .time-center {
    gap: 0.75rem;
}

.main.fullscreen .digit {
    font-size: 96px;
    width: 84px;
}

.main.fullscreen .separator {
    font-size: 96px;
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

.timer-controls-container {
    transition: opacity 0.3s ease;
}

.timer-controls-container.fullscreen-controls {
    opacity: 0.3;
    transition: opacity 0.3s ease;
}

.timer-controls-container.fullscreen-controls:hover {
    opacity: 1;
}
</style>