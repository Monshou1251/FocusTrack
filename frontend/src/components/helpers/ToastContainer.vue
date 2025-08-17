<template>
    <div class="toast-container">
        <TransitionGroup name="toast" tag="div">
            <Toast v-for="toast in toasts" :key="toast.id" :message="toast.message" :type="toast.type"
                :duration="toast.duration" @close="removeToast(toast.id)" />
        </TransitionGroup>
    </div>
</template>

<script setup>
import { useToast } from '@/composables/useToast';
import Toast from './Toast.vue';

const { toasts, removeToast } = useToast()
</script>

<style scoped>
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    pointer-events: none;
}

.toast-container>div {
    pointer-events: auto;
}

/* Toast group animations */
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

.toast-move {
    transition: transform 0.3s ease;
}
</style>
