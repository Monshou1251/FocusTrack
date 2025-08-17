<template>
    <div class="weekly-performance">
        <TopPanel title="weekly performance" :showButton="false" />

        <div class="performance-container">
            <div v-if="sprintStore.isLoading" class="loading">
                <div class="loading-spinner"></div>
            </div>
            <div v-else-if="sprintStore.error" class="error">
                <span>{{ sprintStore.error }}</span>
            </div>
            <div v-else-if="weeklyData.length === 0" class="empty-state">
                <span>No activity this week</span>
            </div>
            <div v-else class="chart-container">
                <div class="chart">
                    <div v-for="(day, index) in weeklyData" :key="index" class="bar" :style="{
                        height: `${getBarHeight(day.count)}%`,
                        backgroundColor: getBarColor(day.count)
                    }" :title="`${day.dayName}: ${formatMinutes(day.count)} focused`">
                        <span class="bar-value">{{ formatMinutes(day.count) }}</span>
                        <div v-if="day.count > 0 && day.count === getMaxCount()" class="star"
                            :title="`Most focused day: ${formatMinutes(day.count)}`">
                            ⭐
                        </div>
                    </div>
                </div>
                <div class="labels">
                    <span v-for="(day, index) in weeklyData" :key="index" class="day-label">
                        {{ day.dayShort }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSprintStore } from '@/store/sprints';
import { computed, onMounted } from 'vue';
import TopPanel from '../TopPanel/TopPanelComp.vue';

const sprintStore = useSprintStore();

const weeklyData = computed(() => {
    const today = new Date();
    const startOfWeek = new Date(today);
    startOfWeek.setDate(today.getDate() - today.getDay());

    const weekDays = [];
    const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

    for (let i = 0; i < 7; i++) {
        const date = new Date(startOfWeek);
        date.setDate(startOfWeek.getDate() + i);
        const dateStr = date.toISOString().split('T')[0];

        const daySprints = sprintStore.sprints.filter(sprint =>
            sprint.started_at.startsWith(dateStr)
        );


        const totalMilliseconds = daySprints.reduce((total, sprint) => {
            return total + parseInt(sprint.duration);
        }, 0);


        const totalMinutes = Math.round(totalMilliseconds / (1000 * 60));

        weekDays.push({
            dayName: dayNames[i],
            dayShort: dayNames[i],
            count: totalMinutes,
            date: dateStr
        });
    }

    return weekDays;
});

const getBarHeight = (count: number) => {
    const maxCount = Math.max(...weeklyData.value.map(day => day.count));
    if (maxCount === 0) return 0;
    return Math.max((count / maxCount) * 100, 10);
};

const getBarColor = (count: number) => {
    if (count === 0) return 'var(--color-background-mute)';

    const maxCount = getMaxCount();
    if (maxCount === 0) return 'var(--color-background-mute)';


    const ratio = count / maxCount;


    if (ratio <= 0.5) {

        const greenToYellow = ratio * 2; // 0 -> 1
        const r = Math.round(34 + (234 - 34) * greenToYellow);
        const g = Math.round(197 + (179 - 197) * greenToYellow);
        const b = Math.round(94 + (8 - 94) * greenToYellow);
        return `rgba(${r}, ${g}, ${b}, 0.7)`;
    } else {

        const yellowToRed = (ratio - 0.5) * 2; // 0 -> 1
        const r = Math.round(234 + (220 - 234) * yellowToRed);
        const g = Math.round(179 + (38 - 179) * yellowToRed);
        const b = Math.round(8 + (38 - 8) * yellowToRed);
        return `rgba(${r}, ${g}, ${b}, 0.7)`;
    }
};

const getMaxCount = () => {
    return Math.max(...weeklyData.value.map(day => day.count));
};

const formatMinutes = (minutes: number) => {
    if (minutes === 0) return '0h';

    const hours = minutes / 60;

    if (hours < 1) {
        return `${minutes}m`;
    }

    if (hours === Math.floor(hours)) {
        return `${hours}h`;
    }

    return `${hours.toFixed(1)}h`;
};

onMounted(async () => {
    if (sprintStore.sprints.length === 0) {
        await sprintStore.fetchSprints();
    }
});
</script>

<style scoped>
.weekly-performance {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
}

.performance-container {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    flex: 1;
    padding: 10px;
    min-height: 150px;
    padding-bottom: 20px;
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

.chart-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    width: 100%;
    height: 100%;
    gap: 8px;
}

.chart {
    display: flex;
    align-items: end;
    justify-content: space-between;
    width: 100%;
    height: 80px;
    gap: 4px;
}

.bar {
    flex: 1;
    min-width: 20px;
    border-radius: 4px 4px 0 0;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    transition: all 0.3s ease;
    cursor: pointer;
    background-image: repeating-linear-gradient(45deg,
            transparent,
            transparent 2px,
            rgba(255, 255, 255, 0.1) 2px,
            rgba(255, 255, 255, 0.1) 4px);
}

.bar:hover {
    transform: scaleY(1.02);
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.bar-value {
    font-size: 10px;
    font-weight: 600;
    color: white;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    position: absolute;
    top: 2px;
}

.star {
    position: absolute;
    top: -22px;
    /* right: -2px; */
    font-size: 12px;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
    animation: twinkle 2s ease-in-out infinite;
}

@keyframes twinkle {

    0%,
    100% {
        opacity: 1;
        transform: scale(1);
    }

    50% {
        opacity: 0.7;
        transform: scale(1.1);
    }
}

.labels {
    display: flex;
    justify-content: space-between;
    width: 100%;
    gap: 4px;
}

.day-label {
    flex: 1;
    text-align: center;
    font-size: 10px;
    color: var(--color-text-mute);
    font-weight: 500;
}
</style>
