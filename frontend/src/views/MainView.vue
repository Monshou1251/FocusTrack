<template>
  <div class="layout">
    <main class="main">
      <div class="cell navbar">
        <Navbar class="navbar" />
      </div>
      <div class="cell performance">Performance</div>
      <div class="cell main-content">main</div>
      <div class="cell spotify">spotify</div>
      <div class="cell categories">categories</div>
      <div class="cell calendar">calendar</div>
      <div class="cell smth">smth</div>
    </main>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue';
</script>

<style scoped>
.main {
  display: grid;
  grid-template-areas:
    "navbar navbar navbar"
    "performance main spotify"
    "categories calendar smth";
  grid-template-columns: 1fr 3fr 1fr;
  grid-template-rows: auto 2fr 1fr;
  gap: 1rem;
  height: 100vh;
}

.cell {
  background-color: rgba(255, 238, 216, 0.37);
}

.navbar {
  grid-area: navbar;
}

.performance {
  grid-area: performance;
  font-family: 'Albert_Sans';
}

.main-content {
  grid-area: main;
}

.spotify {
  grid-area: spotify;
}

.categories {
  grid-area: categories;
}

.calendar {
  grid-area: calendar;
}

.smth {
  grid-area: smth;
}
</style>
