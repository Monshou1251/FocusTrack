<template>
    <div class="main">

        <div class="panels">
            <div class="panels-left">
                <div>
                    <AppButton text="Category" :iconLeft="mdiLogout" :withFilling="false" :noShadow="false" />

                </div>
                <div>
                    <AppButton text="45" :iconRight="mdiMenuDown" :withFilling="false" :noShadow="false" />
                </div>
                <div>Rest</div>
            </div>
            <div class="panels-right">
                <div class="exit-button">
                    <svg-icon type="mdi" :path="mdiArrowExpand"></svg-icon>
                </div>
            </div>
        </div>
        <div class="timer">
            <span class="time-main">12:45</span>
            <span class="time-ms">31</span>
        </div>

        <div>
            buttons
        </div>
    </div>
</template>

<script setup>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiArrowExpand, mdiLogout, mdiMenuDown } from '@mdi/js';
import AppButton from './AppButton.vue';


</script>

<style scoped>
.main {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    height: 100%;
}

.panels {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 8px;
}

.panels-left {
    display: flex;
    flex-direction: row;
}

.timer {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    font-family: 'Bruno_Ace', sans-serif;
}

.time-main {
    font-size: 64px;
    font-weight: 400;
}

.time-ms {
    font-size: 36px;
    font-weight: 400;
    color: #999;
}

.exit-button {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--border-radius-8);
    border: 1px solid var(--color-border);
    background-color: var(--color-background);
    width: 32px;
    height: 32px;
}

.exit-button:hover {
    border: 1px solid var(--color-border-hover);
    cursor: pointer;
}
</style>