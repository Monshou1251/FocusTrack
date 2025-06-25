<template>
    <div class="calendar-main">
        <div class="top-panel">
            <!-- <TopPanel title="overall activity" :showButton="true" @click-help="callHelpWindow" /> -->
            <div class="calendar-title-primary">Calendar</div>
            <div class="calendar-title-secondary">Your yearly activity</div>
        </div>
        <div class="calendar-container">
            <calendar-heatmap dark-mode :values="activityData" :end-date="new Date().toISOString().slice(0, 10)"
                :round="2" :range-color="[
                    'var(--color-background-mute-2)',
                    'hsla(150, 30%, 85%, 0.8)',
                    'hsla(150, 30%, 70%, 0.8)',
                    'hsla(150, 30%, 55%, 0.8)',
                    'hsla(150, 30%, 40%, 0.8)',
                    'hsla(150, 30%, 25%, 0.8)'
                ]" />
        </div>
    </div>
</template>

<script setup>
import { CalendarHeatmap } from 'vue3-calendar-heatmap';


const callHelpWindow = () => {
    console.log('Kek')
}

const activityData = [
    { date: '2024-07-01', count: 2 },
    { date: '2024-07-02', count: 1 },
    { date: '2024-07-15', count: 4 },
    { date: '2024-08-04', count: 2 },
    { date: '2024-08-05', count: 3 },
    { date: '2024-08-06', count: 2 },
    { date: '2024-08-20', count: 6 },
    { date: '2024-09-10', count: 3 },
    { date: '2024-09-11', count: 4 },
    { date: '2024-09-25', count: 7 },
    { date: '2024-10-03', count: 2 },
    { date: '2024-10-04', count: 3 },
    { date: '2024-10-05', count: 1 },
    { date: '2024-10-18', count: 5 },
    { date: '2024-11-01', count: 7 },
    { date: '2024-11-02', count: 8 },
    { date: '2024-11-15', count: 4 },
    { date: '2024-12-05', count: 2 },
    { date: '2024-12-06', count: 3 },
    { date: '2024-12-20', count: 5 },
    { date: '2025-01-10', count: 3 },
    { date: '2025-01-11', count: 4 },
    { date: '2025-01-25', count: 6 },
    { date: '2025-02-05', count: 4 },
    { date: '2025-02-06', count: 5 },
    { date: '2025-02-20', count: 2 },
    { date: '2025-03-01', count: 6 },
    { date: '2025-03-02', count: 7 },
    { date: '2025-03-10', count: 8 },
    { date: '2025-03-11', count: 6 },
    { date: '2025-04-01', count: 5 },
    { date: '2025-04-02', count: 3 },
    { date: '2025-05-10', count: 7 },
    { date: '2025-05-11', count: 5 },
    { date: '2025-06-10', count: 2 },
    { date: '2025-06-11', count: 3 },
    { date: '2025-06-13', count: 4 },
];



</script>

<style scoped>
.calendar-main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
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
    /* display: flex; */
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