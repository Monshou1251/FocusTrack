<template>
  <div class="loader"></div>
</template>

<script></script>

<style scoped>
.loader {
  width: 70px;
  display: flex;
  justify-content: center;
  align-items: center;
  aspect-ratio: 1.154;
  --_g: no-repeat radial-gradient(farthest-side, rgba(189, 194, 199, 1) 90%, #0000);
  --_g2: no-repeat radial-gradient(farthest-side, rgba(185, 46, 30, 1) 90%, #0000);
  --_g3: no-repeat radial-gradient(farthest-side, rgba(43, 65, 65, 1) 90%, #0000);
  background:
    var(--_g) 50% 0,
    var(--_g2) 0 100%,
    var(--_g3) 100% 100%;
  background-size: 35% calc(35% * 1.154);
  animation: l16 1s infinite cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Using cubic-bezier for bouncy effect */
}

@keyframes l16 {
  50%,
  100% {
    background-position:
      calc(100% - 5px) calc(100% - 5px),
      /* Adjusted position */ 50% calc(0% + 5px),
      calc(0% + 5px) calc(100% - 5px); /* Adjusted position */
  }
}
</style>
