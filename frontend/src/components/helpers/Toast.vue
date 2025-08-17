<template>
    <Transition name="toast">
        <div v-if="isVisible" class="toast" :class="type">
            <div class="toast-content">
                <div class="toast-icon">
                    <svg-icon v-if="type === 'error'" type="mdi" :path="mdiAlertCircle" />
                    <svg-icon v-else-if="type === 'success'" type="mdi" :path="mdiCheckCircle" />
                    <svg-icon v-else type="mdi" :path="mdiInformation" />
                </div>
                <div class="toast-message">{{ message }}</div>
                <button class="toast-close" @click="close">
                    <svg-icon type="mdi" :path="mdiClose" />
                </button>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiAlertCircle, mdiCheckCircle, mdiClose, mdiInformation } from '@mdi/js'
import { onMounted, ref } from 'vue'

const props = defineProps({
    message: {
        type: String,
        required: true
    },
    type: {
        type: String,
        default: 'info',
        validator: (value) => ['success', 'error', 'info', 'warning'].includes(value)
    },
    duration: {
        type: Number,
        default: 5000
    }
})

const emit = defineEmits(['close'])

const isVisible = ref(false)

const close = () => {
    isVisible.value = false
    emit('close')
}

onMounted(() => {
    isVisible.value = true
    if (props.duration > 0) {
        setTimeout(close, props.duration)
    }
})
</script>

<style scoped>
.toast {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    min-width: 300px;
    max-width: 400px;
    background: var(--color-background);
    border: 2px solid var(--color-border);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    backdrop-filter: blur(10px);
}

.toast.error {
    border-color: #dc2626;
    background: #fef2f2;
    box-shadow: 0 4px 16px rgba(220, 38, 38, 0.15);
}

.toast.success {
    border-color: #059669;
    background: #f0fdf4;
    box-shadow: 0 4px 16px rgba(5, 150, 105, 0.15);
}

.toast.info {
    border-color: #2563eb;
    background: #eff6ff;
    box-shadow: 0 4px 16px rgba(37, 99, 235, 0.15);
}

.toast.warning {
    border-color: #d97706;
    background: #fffbeb;
    box-shadow: 0 4px 16px rgba(217, 119, 6, 0.15);
}

.toast-content {
    display: flex;
    align-items: center;
    padding: 16px;
    gap: 12px;
}

.toast-icon {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.toast.error .toast-icon {
    color: #7f1d1d;
}

.toast.success .toast-icon {
    color: #064e3b;
}

.toast.info .toast-icon {
    color: #1e3a8a;
}

.toast.warning .toast-icon {
    color: #78350f;
}

.toast-message {
    flex: 1;
    font-size: 14px;
    font-weight: 600;
    line-height: 1.4;
}

.toast.error .toast-message {
    color: #991b1b;
}

.toast.success .toast-message {
    color: #065f46;
}

.toast.info .toast-message {
    color: #1e40af;
}

.toast.warning .toast-message {
    color: #92400e;
}

.toast-close {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    background: none;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.7;
    transition: all 0.2s ease;
}

.toast.error .toast-close {
    color: #7f1d1d;
}

.toast.success .toast-close {
    color: #064e3b;
}

.toast.info .toast-close {
    color: #1e3a8a;
}

.toast.warning .toast-close {
    color: #78350f;
}

.toast-close:hover {
    opacity: 1;
    background: rgba(0, 0, 0, 0.08);
}

/* Toast animations */
.toast-enter-active,
.toast-leave-active {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-enter-from {
    opacity: 0;
    transform: translateX(100%) scale(0.9);
}

.toast-leave-to {
    opacity: 0;
    transform: translateX(100%) scale(0.9);
}

.toast-enter-to,
.toast-leave-from {
    opacity: 1;
    transform: translateX(0) scale(1);
}
</style>
