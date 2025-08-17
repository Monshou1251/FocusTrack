<template>
    <div class="calendar-main">
        <TopPanel title="calendar" :showButton="false" />

        <div class="calendar-container">
            <div v-if="sprintStore.isLoading" class="loading">
                <div class="loading-spinner"></div>
            </div>
            <div v-else-if="sprintStore.error" class="error">
                <span>{{ sprintStore.error }}</span>
            </div>
            <div v-else-if="Object.keys(calendarData).length === 0" class="empty-state">
                <span>No activity yet</span>
            </div>
            <HeatmapTable v-else :data="calendarData" :emptyColor="'var(--color-background-mute)'" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSprintStore } from '@/store/sprints';
import { computed, onMounted } from 'vue';
import HeatmapTable from "vue-heatmap-table";
import TopPanel from '../TopPanel/TopPanelComp.vue';

const sprintStore = useSprintStore()

const calendarData = computed(() => sprintStore.getCalendarData)

onMounted(async () => {
    await sprintStore.fetchSprints()
})
</script>

<style scoped>
.calendar-main {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
}

.calendar-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex: 1;
    padding: 10px;
    min-height: 200px;
}

.loading {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-text-mute);
}

.loading-spinner {
    width: 20px;
    height: 20px;
    border: 2px solid var(--color-border);
    border-top: 2px solid var(--color-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.error {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-error);
    font-size: 12px;
}

.empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-text-mute);
    font-size: 12px;
}

:deep(.vch__legend) {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-end;
    gap: 4px;
    margin-top: 8px;
    font-size: 10px;
    color: var(--color-text-mute);
}

:deep(.vch__day__square:hover) {
    cursor: pointer;
    stroke: var(--color-text);
    stroke-width: 1;
}

:deep(.vch__month__label),
:deep(.vch__day__label) {
    font-size: 10px;
    fill: var(--color-text-mute);
}

:deep(.vch__months__labels__wrapper) {
    padding-bottom: 6px;
}

:deep(.vch__container) {
    padding: 4px;
}
</style>