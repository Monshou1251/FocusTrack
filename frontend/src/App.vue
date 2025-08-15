<template>
  <router-view />
</template>

<script setup>
import { RouterView } from 'vue-router';
</script>

<style>
/* Hide scrollbars in fullscreen mode */
body.fullscreen {
  overflow: hidden !important;
}

html.fullscreen {
  overflow: hidden !important;
}

/* Ensure no scrollbars appear */
.fullscreen * {
  overflow: hidden !important;
}
</style>
