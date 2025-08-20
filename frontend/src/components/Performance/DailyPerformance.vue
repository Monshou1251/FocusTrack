<template>
    <div class="daily-performance">
        <TopPanel title="daily performance" :showButton="false" />

        <div class="body">
            <div v-if="sprintStore.isLoading" class="loading">
                <div class="loading-spinner" />
            </div>
            <div v-else-if="segments.length === 0" class="empty">No activity today</div>
            <div v-else class="stacked-container" :title="`Total: ${formatMinutes(totalMinutes)} focused`">
                <div v-for="seg in segments" :key="seg.categoryId" class="segment" :style="{
                    flexGrow: seg.minutes,
                    flexBasis: '0px',
                    backgroundColor: seg.color
                }" :title="`${seg.categoryName}: ${formatMinutes(seg.minutes)}`">
                    <span class="segment-label">{{ seg.categoryShort }}</span>
                </div>
            </div>

            <div class="legend">
                <div v-for="seg in segments" :key="seg.categoryId" class="legend-item">
                    <span class="dot" :style="{ backgroundColor: seg.color }" />
                    <span class="name">{{ seg.categoryName }}</span>
                    <span class="value">{{ formatMinutes(seg.minutes) }}</span>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup lang="ts">
import { useCategoryStore } from '@/store/categories'
import { useSprintStore } from '@/store/sprints'
import { computed } from 'vue'
import TopPanel from '../TopPanel/TopPanelComp.vue'

const sprintStore = useSprintStore()
const categoryStore = useCategoryStore()

const todayKey = () => new Date().toISOString().split('T')[0]

type Segment = {
    categoryId: string
    categoryName: string
    categoryShort: string
    minutes: number
    color: string
}

const todaySprints = computed(() => {
    const key = todayKey()
    return sprintStore.sprints.filter(s => s.started_at.startsWith(key))
})

const segments = computed<Segment[]>(() => {
    const byCat: Record<string, number> = {}

    for (const s of todaySprints.value) {
        const ms = parseInt(s.duration)
        if (isNaN(ms)) continue
        const minutes = Math.round(ms / (1000 * 60))
        const categoryId = s.category_id
        if (!categoryId) continue
        byCat[categoryId] = (byCat[categoryId] || 0) + minutes
    }

    const result: Segment[] = Object.entries(byCat).map(([categoryId, minutes]) => {
        const idx = categoryStore.categories.findIndex(c => String(c.id) === String(categoryId))
        const name = idx >= 0 ? categoryStore.categories[idx].name : 'Unknown'
        const short = name.length > 10 ? name.slice(0, 9) + '…' : name
        const color = categoryStore.getColorByIndex(idx >= 0 ? idx : 0)
        return { categoryId, categoryName: name, categoryShort: short, minutes, color }
    })

    // Sort by size desc
    return result.sort((a, b) => b.minutes - a.minutes)
})

const totalMinutes = computed(() => segments.value.reduce((acc, s) => acc + s.minutes, 0))

const formatMinutes = (minutes: number) => {
    if (minutes === 0) return '0h'
    const hours = minutes / 60
    if (hours < 1) return `${minutes}m`
    if (hours === Math.floor(hours)) return `${hours}h`
    return `${hours.toFixed(1)}h`
}

</script>

<style scoped>
.daily-performance {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    min-width: 0;
}

.body {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;

    gap: 8px;
    padding: 10px;
    padding-top: 16px;
}

.loading {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
}

.loading-spinner {
    width: 18px;
    height: 18px;
    border: 2px solid var(--color-border);
    border-top: 2px solid var(--color-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg)
    }

    100% {
        transform: rotate(360deg)
    }
}

.empty {
    font-size: 12px;
    color: var(--color-text-mute);
    text-align: center;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.stacked-container {
    display: flex;
    width: 100%;

    height: 100%;
    border-radius: 6px;
    overflow: hidden;
    background: var(--color-background-soft);
    border: 1px solid var(--color-border);
    gap: 2px;
    box-sizing: border-box;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.stacked-container:hover {
    border-color: var(--color-border-hover);
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);
}

.segment {
    height: 100%;
    position: relative;
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    padding: 6px;
    box-sizing: border-box;
    color: var(--color-text);
    min-width: 0;
    overflow: hidden;
    /* soft overlay + hatch */
    background-image:
        linear-gradient(rgba(255, 255, 255, 0.24), rgba(255, 255, 255, 0.24)),
        repeating-linear-gradient(45deg,
            transparent,
            transparent 2px,
            rgba(255, 255, 255, 0.1) 2px,
            rgba(255, 255, 255, 0.1) 4px);
    filter: saturate(0.85) brightness(0.98);
    transition: transform 0.15s ease, filter 0.15s ease, opacity 0.2s ease;
}

.stacked-container:hover .segment {
    opacity: 0.88;
}

.segment:hover {
    opacity: 1;
    filter: brightness(1.03) saturate(1.05);
    transform: translateY(-1px);
}

/* gaps separate segments; avoid borders to prevent width overflow */

.segment-label {
    font-size: 10px;
    font-weight: 600;
    opacity: 0.9;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.segment:hover .segment-label {
    opacity: 1;
}

.legend {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 12px;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
}

.value {
    color: var(--color-text-mute);
}

.dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    border: 1px solid var(--color-border);
    opacity: 0.9;
}
</style>
