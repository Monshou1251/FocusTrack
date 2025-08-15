<template>
    <div class="button-main" ref="dropdownRef">
        <div>
            <button class="app-button" :class="['filled', { 'no-shadow': noShadow }]" @click="toggleDropdown">
                <span class="category-color" :style="{ backgroundColor: currentColor }" />
                <span class="text">{{ selectedText || "Create category first" }}</span>
                <svg-icon type="mdi" :path="mdiMenuDown" class="icon right" />
            </button>

            <ul v-if="dropdownOpen" class="dropdown">
                <li v-for="category in categories" :key="category.id" class="dropdown-item"
                    @click="selectItem(category)">
                    <span class="color-dot" :style="{ backgroundColor: getColor(categories.indexOf(category)) }" />
                    {{ category.name }}
                </li>
            </ul>
        </div>

        <span class="button-title" v-if="title">{{ title }}</span>
    </div>
</template>


<script setup>
import { useCategoryStore } from '@/store/categories'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiMenuDown } from '@mdi/js'
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps({
    text: { type: String, required: true },
    categories: { type: Array, required: true },
    selectedCategory: { type: Object, default: null },
    noShadow: { type: Boolean, default: false },
    title: { type: String, default: '' },
})

const dropdownOpen = ref(false)
const selectedText = ref(props.text)
const dropdownRef = ref(null)

const categoryStore = useCategoryStore()
const getColor = categoryStore.getColorByIndex

const currentIndex = computed(() => {
    if (!props.selectedCategory || !props.categories) return -1
    return props.categories.findIndex(c => c.id === props.selectedCategory.id)
})

const currentColor = computed(() => {
    const index = currentIndex.value
    return index >= 0 ? getColor(index) : '#ccc'
})

watch(() => props.text, (newVal) => {
    selectedText.value = newVal
})

const toggleDropdown = () => {
    dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
    dropdownOpen.value = false
}

const selectItem = (category) => {
    categoryStore.selectedCategory = category
    closeDropdown()
}

const handleClickOutside = (e) => {
    if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
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

    overflow: hidden;
    text-overflow: ellipsis;
}

.dropdown-item:hover {
    cursor: pointer;
    color: var(--color-text-mute);
}

.color-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.text {
    color: var(--color-text);
}

.filled {
    background-color: var(--color-background-soft);
    border: 1px solid var(--color-border);
    /* box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12); */
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

.category-color {
    width: 18px;
    height: 18px;
    border-radius: 6px;
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
