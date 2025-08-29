<template>
    <div ref="buttonRef" class="icon-button" @click="$emit('clickEvent')" :class="[sizeClass, `variant-${variant}`]">
        <svg-icon type="mdi" :path="iconPath" />
    </div>
</template>

<script setup>
import SvgIcon from '@jamescoyle/vue-icon';
import tippy from 'tippy.js';
import 'tippy.js/dist/tippy.css';
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';

const props = defineProps({
    iconPath: { type: String, required: true },
    size: { type: String, default: 'md', validator: v => ['xs', 'sm', 'md', 'lg'].includes(v) },
    color: { type: String, default: 'basic' },
    variant: { type: String, default: 'default', validator: v => ['default', 'secondary'].includes(v) },
    tooltip: { type: String, default: '' }
})

const buttonRef = ref(null);
let tippyInstance = null;

const sizeClass = computed(() => {
    return {
        xs: 'icon-xs',
        sm: 'icon-small',
        md: 'icon-medium',
        lg: 'icon-large'
    }[props.size]
})

onMounted(() => {
    if (props.tooltip && buttonRef.value) {
        tippyInstance = tippy(buttonRef.value, {
            content: props.tooltip,
            placement: 'top',
            arrow: true,
            theme: 'custom',
            animation: 'scale',
            duration: [0, 0],
            zIndex: 9999
        });
    }
});

watch(() => props.tooltip, (newVal) => {
    if (tippyInstance) {
        tippyInstance.setContent(newVal)
    }
})

onBeforeUnmount(() => {
    if (tippyInstance) {
        tippyInstance.destroy();
    }
});
</script>

<style scoped>
.icon-button {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--border-radius-8);
    border: 1px solid var(--color-border);
    background-color: var(--color-background);
    width: 100%;
    height: 100%;
    transition: border 0.2s ease, background-color 0.2s ease;
}

.icon-button:hover {
    border: 1px solid var(--color-border-hover);
    cursor: pointer;
}

.icon-xs svg {
    width: 12px;
    height: 12px;
}

.icon-small svg {
    width: 16px;
    height: 16px;
}

.icon-medium svg {
    width: 24px;
    height: 24px;
}

.icon-large svg {
    width: 32px;
    height: 32px;
}

.variant-default svg {
    color: var(--color-text);
}

.variant-secondary svg {
    color: var(--color-text-mute);
}
</style>

<style>
/* Custom tippy theme */
.tippy-box[data-theme~='custom'] {
    background-color: #333;
    color: white;
    border-radius: 6px;
    font-size: 12px;
    padding: 6px 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.tippy-box[data-theme~='custom'] .tippy-arrow {
    color: #333;
}

.tippy-box[data-theme~='custom'] .tippy-content {
    padding: 0;
}
</style>
