<template>
  <Navbar />
  <div class="text-container">
    <h1 class="text">FocusTrack</h1>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<style scoped>
.text-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.text {
  font-size: 48px;
  font-weight: 800;
  opacity: 0;
  animation:
    fadeIn 4s ease forwards 1s,
    moveAndResize 1s ease forwards 5s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes moveAndResize {
  from {
    transform: translateY(0);
    font-size: 48px; /* Initial font size */
    font-weight: 800; /* Initial font weight */
  }
  to {
    transform: translateY(-300px); /* Move up by 300px */
    font-size: 24px; /* Decrease font size */
    font-weight: 400; /* Decrease font weight */
  }
}
</style>
