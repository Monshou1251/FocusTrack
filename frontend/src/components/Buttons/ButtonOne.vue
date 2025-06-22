<template>
    <div class="icon-button tooltip" data-tooltip="Click to save" @click="$emit('clickEvent')"
        :class="[sizeClass, `variant-${variant}`]">
        <svg-icon type="mdi" :path="iconPath" />
    </div>
</template>

<script setup>
import SvgIcon from '@jamescoyle/vue-icon';
import { computed } from 'vue';

const props = defineProps({
    iconPath: { type: String, required: true },
    size: { type: String, default: 'md', validator: v => ['xs', 'sm', 'md', 'lg'].includes(v) },
    color: { type: String, default: 'basic' },
    variant: { type: String, default: 'default', validator: v => ['default', 'secondary'].includes(v) }
})

const sizeClass = computed(() => {
    return {
        xs: 'icon-xs',
        sm: 'icon-small',
        md: 'icon-medium',
        lg: 'icon-large'
    }[props.size]
})

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
    border: 1px solid var(--color-text-mute);
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
