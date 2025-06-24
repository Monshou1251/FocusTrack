<template>
    <div class="top-panel">
        <div class="title">
            {{ title }}
        </div>
        <div class="exit-button" v-show="showButton">
            <ButtonOne :iconPath="mdiHelp" size="xs" variant="secondary" @clickEvent="$emit('clickHelp')" />
        </div>
    </div>
</template>

<script setup>
import { mdiHelp } from '@mdi/js';
import ButtonOne from '../Buttons/ButtonOne.vue';

defineProps({
    title: { type: String, default: 'Panel' },
    showButton: { type: Boolean, default: true },
})

defineEmits(['clickHelp'])

</script>

<style scoped>
.top-panel {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    height: 20px;
}

.title {
    display: flex;
    align-items: center;
    line-height: 1;
    padding-left: 5px;
    color: var(--color-text-mute);
}

.exit-button {
    width: 20px;
    height: 20px;
}
</style>