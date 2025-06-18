<template>
    <div class="main">

        <div class="panels">
            <div class="panels-left">
                <div>
                    <AppButton text="Category" :iconRight="mdiMenuDown" :iconLeft="mdiLogout" :withFilling="true"
                        :noShadow="false" />
                </div>
                <div>
                    <AppButton text="45" :iconRight="mdiMenuDown" :withFilling="false" :noShadow="false" title="Pace" />
                </div>
                <div>
                    <AppButton text="45" :iconLeft="false" :iconRight="mdiMenuDown" :withFilling="false"
                        :noShadow="false" title="Rest" />
                </div>
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

        <div class="buttons">
            <svg-icon class="button-icons" type="mdi" :path="mdiPlay"></svg-icon>
            <svg-icon class="button-icons" type="mdi" :path="mdiStop"></svg-icon>
            <svg-icon class="button-icons" type="mdi" :path="mdiAutorenew"></svg-icon>
        </div>
    </div>
</template>

<script setup>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiArrowExpand, mdiAutorenew, mdiLogout, mdiMenuDown, mdiPlay, mdiStop } from '@mdi/js';
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
    gap: 17px;
}



.timer {
    padding-left: 45px;
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

.buttons {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    background-color: var(--color-background-soft);
    min-width: 200px;
    height: 60px;
    border-radius: var(--border-radius-8);
    transform: translateY(-10px);

}

.button-icons {
    height: 32px;
    width: auto;
    border-radius: 4px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.button-icons:hover {
    background-color: var(--color-background-soft);
    transform: scale(1.05);
    /* чуть увеличиваем */
    cursor: pointer;
}
</style>