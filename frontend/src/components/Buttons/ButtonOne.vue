<template>
    <div class="icon-button" @click="$emit('clickEvent')">
        <svg-icon type="mdi" :path="iconPath" />
    </div>
</template>

<script setup>
import SvgIcon from '@jamescoyle/vue-icon';

defineProps({
    iconPath: { type: String, required: true }
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
    border: 1px solid var(--color-border-hover);
    cursor: pointer;
}
</style>
