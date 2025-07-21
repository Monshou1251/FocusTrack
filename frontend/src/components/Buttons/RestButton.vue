<template>
    <div class="button-main" ref="dropdownRef">
        <div>
            <button class="app-button" :class="[withFilling ? 'filled' : 'ghost', { 'no-shadow': noShadow }]"
                @click="toggleDropdown">
                <span class="text">{{ selectedText || "Create category first" }}</span>
                <svg-icon type="mdi" :path="iconRight" class="icon right" />
            </button>

            <ul v-if="dropdownOpen" class="dropdown">
                <li v-for="(item, index) in restList" :key="index" class="dropdown-item" @click="selectItem(item)">
                    {{ item }}
                </li>
            </ul>
        </div>

        <span class="button-title" v-if="title">{{ title }}</span>
    </div>
</template>


<script setup lang="ts">
import { useTimerStore } from '@/store/timer'
import SvgIcon from '@jamescoyle/vue-icon'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

const props = defineProps({
    iconRight: { type: String, default: null },
    withFilling: { type: Boolean, default: true },
    noShadow: { type: Boolean, default: false },
    title: { type: String, default: '' },
})

const timerStore = useTimerStore()

const dropdownOpen = ref(false)
const selectedText = ref(
    timerStore.currentRest
)
const restList = computed(() => timerStore.restOptions)

const dropdownRef = ref<HTMLElement | null>(null)


// watch(() => props.text, (newVal) => {
//     selectedText.value = newVal
// })

const toggleDropdown = () => {
    dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
    dropdownOpen.value = false
}

const selectItem = (item: number) => {
    selectedText.value = item
    timerStore.currentRest = item
    timerStore.resetRestTimer()
    console.log("timerStore.currentRest: ", timerStore.currentRest)
    closeDropdown()
}

const handleClickOutside = (e: MouseEvent) => {
    if (dropdownRef.value && !dropdownRef.value.contains(e.target as Node)) {
        closeDropdown()
    }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
.button-main {
    position: relative;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 10px;
}

.app-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 6px 8px;
    padding-left: 12px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    height: 32px;
    font-size: 14px;
    color: var(--color-text);
    font-family: 'Albert_Sans';
    background: var(--color-background-soft);
    transition: all 0.2s ease;
    position: relative;
}

.dropdown {
    position: absolute;
    top: 35px;
    left: 0;
    background: var(--color-background);
    border: 1px solid var(--color-border);
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    z-index: 10;
    list-style: none;
    padding: 4px 0;
    min-width: 100%;
    max-width: 250px;
    white-space: nowrap;
}

.dropdown-item {
    padding: 3px 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.2s;

    overflow: hidden;
    text-overflow: ellipsis;
}

.dropdown-item:hover {
    cursor: pointer;
    color: var(--color-text-mute);
}


.text {
    color: var(--color-text);
}

.filled {
    background-color: var(--color-background-soft);
    border: 1px solid var(--color-border);
}

.ghost {
    background-color: var(--color-background-ghost);
    border: 1px solid var(--color-border);
}

.no-shadow {
    box-shadow: none !important;
}

.icon {
    width: 1.2em;
    height: 1.2em;
}

.button-title {
    font-size: 14px;
}

.button-wrapper {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.right {
    width: 18px;
    height: 18px;
}

.app-button:hover {
    border: 1px solid var(--color-border-hover);
    cursor: pointer;
    color: var(--color-text);
}
</style>
