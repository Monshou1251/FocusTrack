<template>
  <nav class="navbar" :class="{ 'dark-mode': isDarkMode }">
    <div class="left-panel" v-if="isAuthenticated">
      <ProfileInfo />
    </div>


    <div class="right-block">

      <div class="toggle-container" @click="toggleColorMode">
        <div class="toggle">
          <div class="toggle-inner">
            <i class="icon" :class="isDarkMode ? 'fas fa-moon' : 'fas fa-sun'"></i>
          </div>
        </div>
        <span class="color_scheme">{{ isDarkMode ? 'Dark' : 'Light' }}</span>
      </div>

      <div class="exit-button" v-if="isAuthenticated">
        <svg-icon type="mdi" :path="mdiPowerStandby"></svg-icon>
      </div>
    </div>
  </nav>
</template>


<script setup>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiPowerStandby } from '@mdi/js';
import { onMounted, ref, watch } from 'vue';

import ProfileInfo from './ProfileInfo.vue';

const isDarkMode = ref(
  localStorage.getItem('isDarkMode') === 'true' || false
)

const isAuthenticated = ref(true)


const applyTheme = (dark) => {
  document.documentElement.classList.toggle('dark-mode', dark)
  document.documentElement.classList.toggle('light-mode', !dark)
}

const toggleColorMode = () => {
  isDarkMode.value = !isDarkMode.value
}

watch(isDarkMode, (newVal) => {
  localStorage.setItem('isDarkMode', String(newVal))
  applyTheme(newVal)
})

onMounted(() => {
  applyTheme(isDarkMode.value)
})

</script>

<style scoped>
.navbar {
  /* position: fixed; */
  top: 0;
  left: 0;
  height: 100px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  background-color: var(--color-background);
  transition: background-color 0.3s ease-in-out;
  font-family: 'Albert_Sans';
  font-weight: 400;
  font-size: 16px;
}

.left-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  min-width: 400px;
  background-color: var(--color-background-darkest);
  padding: 0 27px;
  border-bottom-right-radius: 8px;
  border-bottom: 1px solid var(--color-border);
  border-right: 1px solid var(--color-border);
}



.right-block {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding-right: 27px;
}

.toggle-container {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.exit-button {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-8);
  border: 1px solid var(--color-border);
  background-color: var(--color-background-mute);
  width: 40px;
  height: 40px;
  transition: border 0.2s ease, background-color 0.2s ease;
}

.exit-button:hover {
  border: 1px solid var(--color-border-hover);
  cursor: pointer;
}


.toggle {
  width: 40px;
  height: 22px;
  background-color: #646464;
  box-shadow: inset 0 0 2px rgba(0, 0, 0, 0.6);
  border-radius: 25px;
  position: relative;
  margin-right: 10px;
}

.dark-mode .toggle {
  background-color: var(--yellow);
}

.toggle-inner {
  width: 18px;
  height: 18px;
  background-color: #fff;
  border-radius: 50%;
  position: absolute;
  left: 2px;
  top: 50%;
  transform: translateY(-50%);
  transition: transform 0.3s ease-in-out;
}

.dark-mode .toggle-inner {
  background-color: var(--color-background);
  transform: translateX(100%) translateY(-50%);
}

.toggle-container span {
  transition: color 0.3s ease-in-out;

}

.icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 14px;
  margin-right: 10px;
}

.icon.fa-moon {
  color: #ffffff;
}

.icon.fa-sun {
  color: #ffcd4b;
  padding-right: 1px;
}
</style>
