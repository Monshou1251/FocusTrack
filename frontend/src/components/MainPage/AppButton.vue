<template>
    <button class="app-button" :class="[
        withFilling ? 'filled' : 'ghost',
        { 'no-shadow': noShadow }
    ]">
        <svg-icon type="mdi" v-if="iconLeft" :path="iconLeft" class="icon left" />
        <span class="text">{{ text }}</span>
        <svg-icon type="mdi" v-if="iconRight" :path="iconRight" class="icon right" />
    </button>
    text
</template>

<script setup>
import SvgIcon from '@jamescoyle/vue-icon';

defineProps({
    text: { type: String, required: true },
    iconLeft: { type: String, default: null },
    iconRight: { type: String, default: null },
    withFilling: { type: Boolean, default: true },
    noShadow: { type: Boolean, default: false }
});
</script>

<style scoped>
.app-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem 1.25rem;
    border: none;
    border-radius: 8px;
    /* font-size: 1rem; */
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    height: 32px;
}

/* Залитая кнопка */
.filled {
    background-color: var(--color-background-soft);
    color: var(--color-text);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12);
}

/* Прозрачная кнопка с тенью и inset эффектом */
.ghost {
    background-color: transparent;
    color: var(--color-text);
    box-shadow:
        0px 1px 2px rgba(0, 0, 0, 0.3),
        inset 0px 1px 2px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--color-border);
}

/* Без тени */
.no-shadow {
    box-shadow: none !important;
}

.icon {
    width: 1.2em;
    height: 1.2em;
}

.icon.left {
    margin-right: 0.4rem;
}

.icon.right {
    margin-left: 0.4rem;
}
</style>
