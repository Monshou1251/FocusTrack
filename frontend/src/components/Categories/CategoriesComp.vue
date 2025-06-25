<template>
    <div class="main-categories">
        <div>

            <TopPanel title="categories" :showButton="true" @clickHelp="callHelpWindow" />

            <ul class="category-list">
                <li v-for="(category, index) in categoryStore.categories" :key="index" class="category-item"
                    @mouseenter="hoveredIndex = index" @mouseleave="hoveredIndex = null">
                    <div class="color-box" :style="{ backgroundColor: categoryStore.getColorByIndex(index) }" />

                    <div class="category-name">
                        <input v-if="editingIndex === index" v-model="editedText" @keyup.enter="saveCategory(index)"
                            @keyup.esc="cancelEditing" class="edit-input" v-focus />
                        <span v-else>{{ category }}</span>
                    </div>

                    <div class="actions" v-show="hoveredIndex === index || editingIndex === index">
                        <button class="action-btn" v-if="editingIndex === index" @click="saveCategory(index)">
                            ✔️
                        </button>
                        <button class="action-btn" v-else @click="editCategory(index)">
                            ✏️
                        </button>
                        <button class="action-btn" @click="categoryStore.deleteCategory(index)">
                            🗑️
                        </button>
                    </div>
                </li>
            </ul>
        </div>

        <div class="bottom-panel" @click="categoryStore.addCategory()">
            <svg-icon type="mdi" :path="mdiPlusBoxOutline" />
            <div class="add-text">Add new category</div>
        </div>
    </div>
</template>


<script setup>
import { useCategoryStore } from '@/store/categories'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiPlusBoxOutline } from '@mdi/js'
import { ref } from 'vue'
import TopPanel from '../TopPanel/TopPanelComp.vue'

const categoryStore = useCategoryStore()

const callHelpWindow = () => {
    console.log('kekCategories')
}

const vFocus = {
    mounted: (el) => el.focus(),
}

const hoveredIndex = ref(null)
const editingIndex = ref(null)
const editedText = ref('')

const editCategory = (index) => {
    editingIndex.value = index
    editedText.value = categoryStore.categories[index]
}

const saveCategory = (index) => {
    if (editingIndex.value === null) return
    const trimmed = editedText.value.trim()
    if (trimmed && trimmed !== categoryStore.categories[index]) {
        categoryStore.updateCategory(index, trimmed)
    }
    editingIndex.value = null
    editedText.value = ''
}

const cancelEditing = () => {
    editingIndex.value = null
    editedText.value = ''
}
</script>

<style scoped>
.main-categories {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    /* padding: 10px; */
    padding-bottom: 0;
}

/* Category List */

.category-list {
    list-style: none;
    padding: 0;
    padding-top: 10px;
    margin: 0;
}

.category-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0px 10px;
    border-radius: 6px;
    transition: background-color 0.3s;
    height: 35px;
    gap: 5px;
    /* font-size: 14px; */
}

.category-item:hover {
    background-color: var(--color-background-soft);
    cursor: pointer;
}

.category-name {
    flex: 1;
    margin-left: 10px;
    min-width: 0;
    overflow: hidden;
}

.category-name input,
.category-name span {
    display: block;
    width: 100%;
    box-sizing: border-box;
}

.color-box {
    width: 20px;
    height: 20px;
    border-radius: 6px;
}

.actions {
    display: flex;
    gap: 4px;
}

.edit-input {
    font-size: 16px;
    padding: 0;
    margin: 0;
    border: none;
    background: transparent;
    color: inherit;
    font-family: inherit;
    width: 100%;
    outline: none;
    border-bottom: 1px solid var(--color-border);
    /* можно убрать */
    transition: border-color 0.2s ease;
}

.edit-input:focus {
    border-color: var(--color-border-hover);
}


.action-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 14px;
    color: var(--color-text);
    padding: 4px;
    border-radius: 4px;
    transition: background-color 0.2s ease;

}

.action-btn:hover {
    background-color: var(--color-border-hover);
}


.bottom-panel {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    height: 50px;
    width: 100%;
    border-top: 1px solid var(--color-border);
    gap: 10px;
    color: var(--color-text-mute);
    transition: color 0.3s ease, transform 0.2s ease;
}

.bottom-panel svg {
    width: 20px;
    height: 20px;
}

.bottom-panel:hover {
    color: var(--color-text);
    cursor: pointer;
    /* background-color: var(--color-background-soft); */
}

.add-text {
    padding-top: 2px;
}
</style>