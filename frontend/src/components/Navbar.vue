<template>
  <nav class="navbar" :class="{ 'dark-mode': isDarkMode }">
    <div class="toggle-container" @click="toggleColorMode">
      <div class="toggle">
        <div class="toggle-inner">
          <i class="icon" :class="isDarkMode ? 'fas fa-moon' : 'fas fa-sun'"></i>
        </div>
      </div>
      <span>{{ isDarkMode ? 'Dark' : 'Light' }}</span>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const isDarkMode = ref(true)

const toggleColorMode = () => {
  // Toggle dark mode
  isDarkMode.value = !isDarkMode.value
  // Update CSS variables
  updateCSSVariables(isDarkMode.value)
}

const updateCSSVariables = (isDarkMode) => {
  const root = document.documentElement

  if (isDarkMode) {
    // Dark mode CSS variables
    root.style.setProperty('--color-background', 'var(--vt-c-black)')
    root.style.setProperty('--color-background-soft', 'var(--vt-c-black-soft)')
    root.style.setProperty('--color-background-mute', 'var(--vt-c-black-mute)')
    root.style.setProperty('--color-border', 'var(--vt-c-divider-dark-2)')
    root.style.setProperty('--color-border-hover', 'var(--vt-c-divider-dark-1)')
    root.style.setProperty('--color-heading', 'var(--vt-c-text-dark-1)')
    root.style.setProperty('--color-text', 'var(--vt-c-text-dark-1)')
    root.style.setProperty('--color-button-hover', 'var(--hover-blue-dark)')
  } else {
    // Light mode CSS variables
    root.style.setProperty('--color-background', 'var(--vt-c-white)')
    root.style.setProperty('--color-background-soft', 'var(--vt-c-white-soft)')
    root.style.setProperty('--color-background-mute', 'var(--vt-c-white-mute)')
    root.style.setProperty('--color-border', 'var(--vt-c-divider-light-2)')
    root.style.setProperty('--color-border-hover', 'var(--vt-c-divider-light-1)')
    root.style.setProperty('--color-heading', 'var(--vt-c-text-light-1)')
    root.style.setProperty('--color-text', 'var(--vt-c-text-light-1)')
    root.style.setProperty('--color-button-hover', 'var(--hover-blue-light)')
  }
}

// Initialize CSS variables based on initial mode
updateCSSVariables(isDarkMode.value)
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding: 20px;
  background-color: var(--color-background);
  transition: background-color 0.3s ease-in-out;
  font-family: 'Jost-Regular';
  font-weight: 400;
}

.toggle-container {
  display: flex;
  align-items: center;
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
  background-color: #ffcd4b;
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
  /* color: var(--color-text); */
  /* font-weight: bold; */
  transition: color 0.3s ease-in-out;
  font-family: 'Jost-SemiBold';
  font-size: 16px;
}

.icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 14px; /* Adjust icon size */
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
