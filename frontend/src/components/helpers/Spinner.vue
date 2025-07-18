<template>
  <div class="loading-overlay">
    <div class="loader">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
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
  /* background-color: rgba(0, 0, 0, 0.3); */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* From Uiverse.io by mrhyddenn */
.loader {
  position: relative;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(var(--color-coral-red), var(--color-sky-blue), var(--color-mint-green));
  animation: animate7712 1.2s linear infinite;
}

@keyframes animate7712 {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.loader span {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(var(--color-coral-red), var(--color-sky-blue), var(--color-mint-green));
}

.loader:after {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  /* background: #333; */
  /* border: solid #333 10px; */
  border-radius: 50%;
}

.loader span:nth-child(1) {
  filter: blur(5px);
}

.loader span:nth-child(2) {
  filter: blur(10px);
}

.loader span:nth-child(3) {
  filter: blur(25px);
}

.loader span:nth-child(4) {
  filter: blur(50px);
}
</style>
