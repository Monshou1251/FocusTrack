<template>
    <div class="button-main">

        <button class="app-button" :class="[
            withFilling ? 'filled' : 'ghost',
            { 'no-shadow': noShadow }
        ]">
            <span v-if="iconLeft" class="category-color"></span>
            <span class="text">{{ text }}</span>
            <svg-icon type="mdi" v-if="iconRight" :path="iconRight" class="icon right" />
        </button>
        <span class="button-title" v-if="title">{{ title }}</span>
    </div>
</template>

<script setup>
import SvgIcon from '@jamescoyle/vue-icon';

defineProps({
    text: { type: String, required: true },
    iconLeft: { type: String, default: null },
    iconRight: { type: String, default: null },
    withFilling: { type: Boolean, default: true },
    noShadow: { type: Boolean, default: false },
    title: { type: String, default: '' }
});
</script>

<style scoped>
.button-main {
    display: flex;
    align-items: center;
    gap: 10px;
}

.app-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 6px 8px;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    height: 32px;
    font-size: 14px;
    color: var(--color-text);
}

.filled {
    background-color: var(--color-background-soft);
    border: 1px solid var(--color-border);
    /* box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12); */
}

.ghost {
    background-color: transparent;

    /* box-shadow:
        0px 1px 2px rgba(0, 0, 0, 0.3),
        inset 0px 1px 2px rgba(0, 0, 0, 0.3); */
    border: 1px solid var(--color-border);
}

.no-shadow {
    box-shadow: none !important;
}

.icon {
    width: 1.2em;
    height: 1.2em;
}

.category-color {
    background-color: var(--yellow);
    width: 18px;
    height: 18px;
    border-radius: 6px;
}

.button-title {
    font-size: 14px;
}

.button-wrapper {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.app-button:hover {
    border: 1px solid var(--color-border-hover);
    cursor: pointer;
}
</style>
