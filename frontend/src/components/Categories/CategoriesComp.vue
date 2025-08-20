<template>
    <div class="main-categories">
        <div>

            <TopPanel title="categories" :showButton="true" @clickHelp="callHelpWindow" />

            <ul class="category-list">

                <template v-if="categoryStore.isLoading">

                    <li v-for="n in 5" :key="n" class="category-item skeleton">
                        <div class="color-box shimmer" />
                        <div class="category-name shimmer" style="width: 120px; height: 20px;"></div>
                    </li>
                </template>
                <template v-else>

                    <li v-for="(category, index) in categoryStore.categories" :key="category.id" class="category-item"
                        @mouseenter="hoveredIndex = index" @mouseleave="hoveredIndex = null">
                        <div class="color-box" :style="{ backgroundColor: categoryStore.getColorByIndex(index) }" />

                        <div class="category-name">
                            <span>{{ category.name }}</span>
                        </div>

                        <div class="actions" v-show="hoveredIndex === index">
                            <button class="action-btn" @click="editCategory(index)">
                                ✏️
                            </button>
                            <button class="action-btn" @click="deleteCategory(index)">
                                🗑️
                            </button>
                        </div>
                    </li>
                </template>
            </ul>
        </div>

        <div class="bottom-panel" @click="showAddModal = true">
            <svg-icon type="mdi" :path="mdiPlusBoxOutline" />
            <div class="add-text">Add new category</div>
        </div>

        <!-- Add Category Modal -->
        <div v-if="showAddModal" class="modal-overlay">
            <div class="modal-content" @click.stop>
                <h3>Add New Category</h3>
                <input v-model="newCategoryName" @keyup.enter="createCategory" @keyup.esc="closeAddModal"
                    placeholder="Enter category name" class="modal-input" ref="categoryInput" v-focus
                    :disabled="isCreating" />
                <div class="modal-actions">
                    <button @click="closeAddModal" class="modal-btn cancel" :disabled="isCreating">
                        Cancel
                    </button>
                    <button @click="createCategory" class="modal-btn confirm"
                        :disabled="!newCategoryName.trim() || isCreating">
                        <span v-if="isCreating" class="spinner-container">
                            <div class="mini-spinner"></div>
                        </span>
                        <span v-else>Create</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="modal-overlay">
            <div class="modal-content delete-modal" @click.stop>
                <h3>Delete Category</h3>
                <p class="delete-message">
                    Are you sure you want to delete "<strong>{{ categoryToDelete?.name }}</strong>"?
                </p>
                <p class="delete-warning">This action cannot be undone.</p>
                <div class="modal-actions">
                    <button @click="closeDeleteModal" class="modal-btn cancel" :disabled="isDeleting">
                        Cancel
                    </button>
                    <button @click="confirmDelete" class="modal-btn delete" :disabled="isDeleting">
                        <span v-if="isDeleting" class="spinner-container">
                            <div class="mini-spinner"></div>
                        </span>
                        <span v-else>Delete</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- Edit Category Modal -->
        <div v-if="showEditModal" class="modal-overlay">
            <div class="modal-content" @click.stop>
                <h3>Edit Category</h3>
                <input v-model="editCategoryName" @keyup.enter="saveCategory" @keyup.esc="closeEditModal"
                    placeholder="Enter category name" class="modal-input" ref="editInput" v-focus
                    :disabled="isUpdating" />
                <div class="modal-actions">
                    <button @click="closeEditModal" class="modal-btn cancel" :disabled="isUpdating">
                        Cancel
                    </button>
                    <button @click="saveCategory" class="modal-btn save"
                        :disabled="!editCategoryName.trim() || isUpdating">
                        <span v-if="isUpdating" class="spinner-container">
                            <div class="mini-spinner"></div>
                        </span>
                        <span v-else>Save</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { useCategoryStore } from '@/store/categories'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiPlusBoxOutline } from '@mdi/js'
import { onBeforeUnmount, onMounted, ref } from 'vue'
import TopPanel from '../TopPanel/TopPanelComp.vue'

const categoryStore = useCategoryStore()

const callHelpWindow = () => {
    console.log('kekCategories')
}

const vFocus = {
    mounted: (el) => el.focus(),
}

const hoveredIndex = ref(null)
const showAddModal = ref(false)
const newCategoryName = ref('')
const categoryInput = ref(null)
const isCreating = ref(false)
const showDeleteModal = ref(false)
const categoryToDelete = ref(null)
const isDeleting = ref(false)
const showEditModal = ref(false)
const editCategoryName = ref('')
const editInput = ref(null)
const isUpdating = ref(false)

const editingIndex = ref(null)

const editCategory = (index) => {
    editingIndex.value = index
    editCategoryName.value = categoryStore.categories[index].name
    showEditModal.value = true
}

const saveCategory = async () => {
    if (editingIndex.value === null) return
    const trimmed = editCategoryName.value.trim()
    if (trimmed && trimmed !== categoryStore.categories[editingIndex.value].name) {
        isUpdating.value = true
        try {
            await categoryStore.updateCategory(editingIndex.value, trimmed)
            closeEditModal()
        } catch (error) {
            alert('Failed to update category. Please try again.')
        } finally {
            isUpdating.value = false
        }
    } else {
        closeEditModal()
    }
}

const deleteCategory = async (index) => {
    categoryToDelete.value = categoryStore.categories[index]
    showDeleteModal.value = true
}

const confirmDelete = async () => {
    if (!categoryToDelete.value) return

    isDeleting.value = true
    try {
        const index = categoryStore.categories.findIndex(c => c.id === categoryToDelete.value.id)
        if (index !== -1) {
            await categoryStore.deleteCategory(index)
            closeDeleteModal()
        }
    } catch (error) {
        alert('Failed to delete category. Please try again.')
    } finally {
        isDeleting.value = false
    }
}

const closeDeleteModal = () => {
    showDeleteModal.value = false
    categoryToDelete.value = null
}

const createCategory = async () => {
    const trimmed = newCategoryName.value.trim()
    if (!trimmed) return

    isCreating.value = true
    try {
        await categoryStore.addCategory(trimmed)
        closeAddModal()
    } catch (error) {
        if (error.message === 'Maximum categories reached.') {
            alert('Maximum categories reached.')
        } else {
            alert('Failed to create category. Please try again.')
        }
    } finally {
        isCreating.value = false
    }
}

const closeAddModal = () => {
    showAddModal.value = false
    newCategoryName.value = ''
}

const closeEditModal = () => {
    showEditModal.value = false
    editCategoryName.value = ''
    editingIndex.value = null
}

const handleKeydown = (e) => {
    if (e.key === 'Escape') {
        if (showAddModal.value && !isCreating.value) closeAddModal()
        if (showEditModal.value && !isUpdating.value) closeEditModal()
        if (showDeleteModal.value && !isDeleting.value) closeDeleteModal()
    }
}

onMounted(async () => {
    document.addEventListener('keydown', handleKeydown)
    await categoryStore.fetchCategories()
})

onBeforeUnmount(() => {
    document.removeEventListener('keydown', handleKeydown)
})
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
    transition: background-color 0.3s, filter 0.2s ease, opacity 0.2s ease;
    height: 35px;
    gap: 5px;
    /* font-size: 14px; */
    opacity: 0.92;
    filter: saturate(0.9) brightness(0.98);
}

.category-item:hover {
    background-color: var(--color-background-soft);
    cursor: pointer;
    opacity: 1;
    filter: none;
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
    opacity: 0.92;
    transition: opacity 0.2s ease;
}

.category-item:hover .color-box {
    opacity: 1;
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


.skeleton {
    display: flex;
    align-items: center;
    gap: 10px;
}

.shimmer {
    background: linear-gradient(90deg,
            var(--vt-c-black-mute-raw) 25%,
            var(--vt-c-black) 50%,
            var(--vt-c-black-mute-raw) 75%);
    background-size: 200% 100%;
    animation: shimmer 4s infinite;
    border-radius: 4px;
}



@keyframes shimmer {
    0% {
        background-position: 200% 0;
    }

    100% {
        background-position: -200% 0;
    }
}

/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: var(--color-background);
    border: 1px solid var(--color-border);
    border-radius: 8px;
    padding: 24px;
    min-width: 300px;
    max-width: 400px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.modal-content h3 {
    margin: 0 0 16px 0;
    color: var(--color-text);
    font-size: 18px;
    font-weight: 600;
}

.modal-input {
    width: 100%;
    padding: 12px;
    border: 1px solid var(--color-border);
    border-radius: 6px;
    background: var(--color-background-soft);
    color: var(--color-text);
    font-size: 14px;
    margin-bottom: 20px;
    box-sizing: border-box;
}

.modal-input:focus {
    outline: none;
    border-color: var(--color-border-hover);
}

.modal-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
}

.modal-btn {
    padding: 8px 16px;
    border: 1px solid var(--color-border);
    border-radius: 6px;
    background: var(--color-background-soft);
    color: var(--color-text);
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
}

.modal-btn:hover {
    background: var(--color-background);
    border-color: var(--color-border-hover);
}

.modal-btn.confirm {
    background: var(--color-primary);
    color: white;
    border-color: var(--color-primary);
}

.modal-btn.confirm:hover {
    background: var(--color-primary-hover);
}

.modal-btn.confirm:disabled {
    background: var(--color-text-mute);
    border-color: var(--color-text-mute);
    cursor: not-allowed;
}

.modal-btn.save {
    background: var(--color-primary);
    color: white;
    border-color: var(--color-primary);
}

.modal-btn.save:hover {
    background: var(--color-primary-hover);
    border-color: var(--color-primary-hover);
}

.modal-btn.save:disabled {
    background: var(--color-text-mute);
    border-color: var(--color-text-mute);
    cursor: not-allowed;
}

/* Delete Modal Styles */
.delete-modal {
    max-width: 450px;
}

.delete-message {
    margin: 0 0 12px 0;
    color: var(--color-text);
    font-size: 14px;
    line-height: 1.4;
}

.delete-warning {
    margin: 0 0 20px 0;
    color: var(--color-text-mute);
    font-size: 12px;
    font-style: italic;
}

.modal-btn.delete {
    background: var(--color-danger, #dc3545);
    color: white;
    border-color: var(--color-danger, #dc3545);
}

.modal-btn.delete:hover {
    background: var(--color-danger-hover, #c82333);
    border-color: var(--color-danger-hover, #c82333);
}

.modal-btn.delete:disabled {
    background: var(--color-text-mute);
    border-color: var(--color-text-mute);
    cursor: not-allowed;
}

/* Mini Spinner Styles */
.spinner-container {
    display: flex;
    align-items: center;
    justify-content: center;
}

.mini-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
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

/* Disabled state styles */
.modal-input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.modal-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
</style>