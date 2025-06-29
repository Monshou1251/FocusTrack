<template>
  <div class="loading-overlay">
    <div class="pulse-wrapper">
      <div class="pulse-ring ring1"></div>
      <div class="pulse-ring ring2"></div>
      <div class="pulse-ring ring3"></div>
    </div>
  </div>
</template>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  backdrop-filter: blur(3px);
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.pulse-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
}

.pulse-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  border: 6px solid;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 1.5s ease-out infinite;
  opacity: 0;
}

.ring1 {
  border-color: var(--color-coral-red);
  animation-delay: 0s;
}

.ring2 {
  border-color: var(--color-soft-purple);
  animation-delay: 0.4s;
}

.ring3 {
  border-color: var(--color-sky-blue);
  animation-delay: 0.8s;
}

@keyframes pulse {
  0% {
    width: 0;
    height: 0;
    opacity: 1;
  }

  100% {
    width: 100px;
    height: 100px;
    opacity: 0;
  }
}
</style>
