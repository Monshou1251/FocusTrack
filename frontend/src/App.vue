<template>
  <router-view />
  <ToastContainer />
</template>

<script setup>
import ToastContainer from '@/components/helpers/ToastContainer.vue';
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
