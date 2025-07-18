<template>
    <div class="calendar-main">
        <div class="top-panel">
            <div class="calendar-title-primary">Calendar</div>
            <div class="calendar-title-secondary">Your {{ mode }} activity</div>

            <div class="calendar-switch">
                <button :class="{ active: mode === 'year' }" @click="mode = 'year'">Year</button>
                <button :class="{ active: mode === 'week' }" @click="mode = 'week'">Week</button>
            </div>
        </div>

        <div class="calendar-container" v-if="mode === 'year'">
            <HeatmapTable :data="sampleData" :emptyColor="'var(--color-background-mute)'" />
        </div>

        <div v-else>
            <WeeklyChart />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import HeatmapTable from "vue-heatmap-table";
import WeeklyChart from './WeeklyChart.vue';

const mode = ref('year')

const sampleData = {
    "2025-01-01": 1,
    "2025-02-03": 3,
    "2025-04-15": 6,
    "2025-12-31": 2,
};


</script>

<style scoped>
.calendar-main {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    min-height: 250px;
    /* или auto, но с transition */
    transition: all 0.3s ease;
}

.calendar-switch {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.calendar-switch button {
    padding: 4px 12px;
    border: none;
    background: #ddd;
    cursor: pointer;
    border-radius: 4px;
}

.calendar-switch button.active {
    background: #42b883;
    color: white;
}

.top-panel {
    display: flex;
    flex-direction: column;
    line-height: 1.2;
    width: 100%;
}

.calendar-title-primary {
    font-size: 14px;
}

.calendar-title-secondary {
    font-size: 14px;
    color: var(--color-text-mute);
}

.calendar-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: row;
    padding: 0px 20px;
    padding-top: 15px;
    padding-bottom: 5px;
    width: 100%;
    max-width: 750px;
    /* min-width: 650px; */
    align-items: center;
    /* border: 1px solid var(--color-border); */
    border-radius: 6px;
    /* background-color: var(--color-background); */
    padding-bottom: 20px;
}

:deep(.vch__legend) {

    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-end;
    gap: 6px;
    margin-top: 2px;
    font-size: 14px;
    color: var(--color-text-mute);
}

:deep(.vch__external-legend-wrapper svg) {
    /* display: flex;
    align-items: flex-end;
    justify-content: center; */
    /* left: 0; */
}

:deep(.vch__wrapper) {
    /* min-width: auto;
    min-width: auto; */
}

:deep(.vch__container) {
    /* width: auto;
    height: auto; */
}


:deep(.vch__day__square:hover) {
    cursor: pointer;
    stroke: var(--color-text);
    stroke-width: 1;
}

:deep(.vch__day__square) {
    /* width: 10ppx;
    height: 10ppx; */
}

:deep(.vch__month__label),
:deep(.vch__day__label) {
    font-size: 12px;
    fill: var(--color-text);
}

:deep(.vch__months__labels__wrapper) {
    padding-bottom: 10px;

}
</style>