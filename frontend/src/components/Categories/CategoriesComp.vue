<template>
    <div class="main-categories">
        <div>
            <TopPanel title="categories" :showButton="true" @clickHelp="callHelpWindow" />

            <ul class="category-list">
                <li v-for="(category, index) in categoriesList" :key="index" class="category-item"
                    @mouseenter="hoveredIndex = index" @mouseleave="hoveredIndex = null">
                    <div class="color-box" :style="{ backgroundColor: pastelColors[index % pastelColors.length] }">
                    </div>

                    <div class="category-name">
                        <input v-if="editingIndex === index" v-model="editedText" @keyup.enter="saveCategory(index)"
                            @keyup.esc="cancelEditing" class="edit-input" v-focus />
                        <span v-else>{{ category }}</span>
                    </div>

                    <div class="actions" v-show="hoveredIndex === index || editingIndex === index">
                        <button class="action-btn" v-if="editingIndex === index"
                            @click="saveCategory(index)">✔️</button>

                        <button class="action-btn" v-else @click="editCategory(index)">✏️</button>

                        <button class="action-btn" @click="deleteCategory(index)">🗑️</button>
                    </div>
                </li>
            </ul>

        </div>
        <div class="bottom-panel" @click="addCategory">
            <svg-icon type="mdi" :path="mdiPlusBoxOutline" />
            <div class="add-text">Add new category</div>
        </div>
    </div>
</template>

<script setup>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiPlusBoxOutline } from '@mdi/js';
import { ref } from 'vue';
import TopPanel from '../TopPanel/TopPanelComp.vue';


const callHelpWindow = () => {
    console.log('kekCategories')
    // TODO: вызов окна подсказки
}

const vFocus = {
    mounted: (el) => {
        el.focus()
    }
}

const categoriesList = ref(['First', 'Second'])
const hoveredIndex = ref(null)
const editingIndex = ref(null)
const editedText = ref('')

const pastelColors = [
    '#ffcd4b', // тёплый жёлтый (заменил #FFB900 на твой цвет)
    '#FF6F61', // кораллово-красный
    '#F58EA8', // мягкий розовый
    '#6EC1E4', // голубой
    '#42B883', // мятно-зелёный
    '#A7D676', // светло-зелёный (замена жёлтому #FFE066)
    '#A78BFA', // мягкий фиолетовый
    '#80CBC4', // бирюзовый
    '#FBC02D', // янтарный
    '#F48FB1', // светло-розовый
]

const addCategory = () => {
    if (categoriesList.value.length < pastelColors.length) {
        categoriesList.value.push(`New category ${categoriesList.value.length + 1}`)
    } else {
        alert('Maximum 8 categories allowed.')
    }
}

const deleteCategory = (index) => {
    categoriesList.value.splice(index, 1)
}

const editCategory = (index) => {
    editingIndex.value = index
    editedText.value = categoriesList.value[index]
}

const saveCategory = (index) => {
    const trimmed = editedText.value.trim()

    if (editingIndex.value === null) return

    if (trimmed && trimmed !== categoriesList.value[index]) {
        categoriesList.value[index] = trimmed
    }

    editingIndex.value = null
    editedText.value = ''
}


const cancelEditing = () => {
    console.log('ESC pressed, canceling...')
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
    font-size: 15px;
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