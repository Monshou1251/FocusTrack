import { ref } from 'vue'

export interface Toast {
  id: number
  message: string
  type: 'success' | 'error' | 'info' | 'warning'
  duration?: number
}

const toasts = ref<Toast[]>([])
let nextId = 1

export function useToast() {
  const showToast = (message: string, type: Toast['type'] = 'info', duration: number = 5000) => {
    const toast: Toast = {
      id: nextId++,
      message,
      type,
      duration
    }

    toasts.value.push(toast)

    // Auto remove after duration
    if (duration > 0) {
      setTimeout(() => {
        removeToast(toast.id)
      }, duration)
    }

    return toast.id
  }

  const removeToast = (id: number) => {
    const index = toasts.value.findIndex((toast) => toast.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  const clearAll = () => {
    toasts.value = []
  }

  // Convenience methods
  const showSuccess = (message: string, duration?: number) =>
    showToast(message, 'success', duration)
  const showError = (message: string, duration?: number) => showToast(message, 'error', duration)
  const showInfo = (message: string, duration?: number) => showToast(message, 'info', duration)
  const showWarning = (message: string, duration?: number) =>
    showToast(message, 'warning', duration)

  return {
    toasts: toasts.value,
    showToast,
    showSuccess,
    showError,
    showInfo,
    showWarning,
    removeToast,
    clearAll
  }
}
