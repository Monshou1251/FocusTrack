<template>
  <div class="journal">
    <div class="header">
      <div>

        <!-- <button @click="toogleJournalFullscreen">test</button> -->
        <div class="panels">
          <h3>Journal</h3>
          <div class="fs-button">

            <ButtonOne :iconPath="mdiArrowExpand" @click="toogleJournalFullscreen" size="sm"
              :tooltip="isJournalFullscreen ? 'Exit fullscreen' : 'Enter fullscreen'" />
          </div>
        </div>
      </div>
      <form class="create" @submit.prevent="onCreate">
        <input v-model="title" type="text" placeholder="Title" required />
        <textarea v-model="content" placeholder="What's on your mind?" rows="3" class="content-textarea" required />
      </form>
    </div>
    <button class="primary-btn" :disabled="!canSubmit" @click="tryCreate">
      <svg-icon type="mdi" :path="mdiPlusBoxOutline" />
      <span>Add entry</span>
    </button>
    <div class="list" v-if="!isLoading && entries.length">
      <div class="item" v-for="e in entries" :key="e.id">
        <div class="meta">
          <div class="date">{{ formatDate(e.created_at) }}</div>
          <button class="icon-btn" title="Delete" @click="onDelete(e.id)">✕</button>
        </div>
        <div class="title" v-if="e.title">{{ e.title }}</div>
        <div class="content">{{ e.content }}</div>
      </div>
    </div>
    <div class="empty" v-else-if="!isLoading">No entries yet</div>
    <div class="loading" v-else>Loading…</div>

  </div>
  <!-- Delete Confirmation Modal -->
  <div v-if="showDeleteModal" class="modal-overlay">
    <div class="modal-content delete-modal" @click.stop>
      <h3>Delete Entry</h3>
      <p class="delete-message">
        Are you sure you want to delete
        <strong v-if="entryToDelete?.title">"{{ entryToDelete?.title }}"</strong>
        <span v-else>this entry</span>?
      </p>
      <p class="delete-warning">This action cannot be undone.</p>
      <div class="modal-actions">
        <button @click="closeDeleteModal" class="modal-btn cancel" :disabled="isDeleting">Cancel</button>
        <button @click="confirmDelete" class="modal-btn delete" :disabled="isDeleting">
          <span v-if="isDeleting" class="spinner-container">
            <div class="mini-spinner"></div>
          </span>
          <span v-else>Delete</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useJournalStore } from '@/store/journal'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiArrowExpand, mdiPlusBoxOutline } from '@mdi/js'
import { storeToRefs } from 'pinia'
import { computed, onMounted, ref } from 'vue'
import ButtonOne from '../Buttons/ButtonOne.vue'

const journal = useJournalStore()
const { toogleJournalFullscreen } = journal


const { entries, isLoading, isJournalFullscreen } = storeToRefs(journal)


const title = ref('')
const content = ref('')
const canSubmit = computed(() => title.value.trim().length > 0 && content.value.trim().length > 0)

// Delete modal state
const showDeleteModal = ref(false)
const entryToDelete = ref<{ id: number; title?: string } | null>(null)
const isDeleting = ref(false)

onMounted(() => {
  if (!entries.value.length) journal.fetchEntries()
})

function formatDate(iso: string) {
  const d = new Date(iso)
  return d.toLocaleString()
}

async function onCreate() {
  if (!title.value.trim() || !content.value.trim()) return
  await journal.addEntry({ title: title.value.trim(), content: content.value.trim() })
  title.value = ''
  content.value = ''
}

async function onDelete(id: number) {
  const e = entries.value.find(x => x.id === id)
  entryToDelete.value = e ? { id: e.id, title: e.title } : { id }
  showDeleteModal.value = true
}

function tryCreate() {
  if (!canSubmit.value) return
  onCreate()
}

async function confirmDelete() {
  if (!entryToDelete.value) return
  isDeleting.value = true
  try {
    await journal.removeEntry(entryToDelete.value.id)
    closeDeleteModal()
  } finally {
    isDeleting.value = false
  }
}

function closeDeleteModal() {
  showDeleteModal.value = false
  entryToDelete.value = null
}
</script>

<style scoped>
.journal {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-width: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Noto Sans", "Ubuntu", "Cantarell", "Helvetica Neue", Arial, sans-serif;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 8px;
  /* padding-bottom: 8px; */
  /* border-bottom: 1px solid var(--color-border); */
}

h3 {
  margin: 0;
  font-size: 1rem;
  opacity: 0.9;
}

.create {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-wrap: wrap;
}

.panels {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 17px;
}

.create input {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 6px 8px;
  color: var(--color-text);
  /* flex: 1 1 140px; */
  min-width: 0;
  font-family: inherit;
  font-size: 0.8rem;
  line-height: 1.4;
  /* max-width: 40vw; */
}

.fs-button {
  width: 22px;
  height: 22px;
}

.content-textarea {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 6px 8px;
  color: var(--color-text);
  /* flex: 1 1 100%; */
  min-width: 0;
  resize: vertical;
  font-family: inherit;
  font-size: 0.8rem;
  line-height: 1.5;
  overflow: auto;
  /* max-width: 40vw; */
}

/* bottom action bar like categories */
.primary-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
  padding: 8px 12px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  color: var(--color-text-mute);
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.3s ease, background-color 0.3s ease, color 0.3s ease;
  margin-bottom: 8px;
  /* max-width: 40vw; */
}

.primary-btn:hover:enabled {
  color: var(--color-text);
  border-color: var(--color-border-hover);
  background: var(--color-background-soft);
}

.primary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.primary-btn svg {
  width: 18px;
  height: 18px;
}

.list {
  overflow-y: auto;
  min-height: 0;
  padding-top: 8px;
  display: flex;
  flex-direction: column;
  border-top: 1px solid var(--color-border);
  gap: 6px;
}

/* Custom scrollbar for journal list */
.list::-webkit-scrollbar {
  width: 10px;
}

.list::-webkit-scrollbar-track {
  background: var(--color-background);
}

.list::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 8px;
  border: 2px solid var(--color-background);
}

.list::-webkit-scrollbar-thumb:hover {
  background: var(--color-border-hover);
}

/* Firefox */
.list {
  scrollbar-width: thin;
  scrollbar-color: var(--color-border) var(--color-background);
}

/* Match scrollbar styling for textarea */
.content-textarea::-webkit-scrollbar {
  width: 10px;
}

.content-textarea::-webkit-scrollbar-track {
  background: var(--color-background);
}

.content-textarea::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 8px;
  border: 2px solid var(--color-background);
}

.content-textarea::-webkit-scrollbar-thumb:hover {
  background: var(--color-border-hover);
}

.content-textarea {
  scrollbar-width: thin;
  scrollbar-color: var(--color-border) var(--color-background);
}

.item {
  border-bottom: 1px dashed var(--color-border);

  border-radius: 2px;
  padding: 8px;
  /* background: var(--color-background-mute); */
  margin-right: 4px;
}

.meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.date {
  font-size: 0.7rem;
  opacity: 0.7;
  /* border-bottom: 1px solid var(--color-text-mute); */
  border-bottom: 1px solid var(--color-border);
}

.title {
  font-weight: 400;
  font-size: 0.8rem;
  margin-top: 4px;
  word-break: break-word;

}

.content {
  opacity: 0.9;
  word-break: break-word;
  font-size: 0.8rem;
  color: var(--color-text-mute-2);
}

.icon-btn {
  border: 1px solid var(--color-border);
  background: transparent;
  color: var(--color-text);
  border-radius: 4px;
  padding: 0 4px;

  width: 20px;
  height: 20px;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-btn:hover {
  border-color: var(--color-border-hover);
}

.empty,
.loading {
  opacity: 0.7;
  padding: 12px;
}

/* Modal Styles aligned with project */
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
  max-width: 420px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.modal-content h3 {
  margin: 0 0 16px 0;
  color: var(--color-text);
  font-size: 18px;
  font-weight: 600;
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

.modal-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.modal-btn.delete {
  background: var(--color-danger, #dc3545);
  color: #fff;
  border-color: var(--color-danger, #dc3545);
}

.modal-btn.delete:hover {
  background: var(--color-danger-hover, #c82333);
  border-color: var(--color-danger-hover, #c82333);
}

.spinner-container {
  display: inline-flex;
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
</style>
