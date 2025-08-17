<template>
  <div class="layout" :class="{ 'fullscreen': isFullscreen }">
    <!-- Navbar - hidden in fullscreen mode -->
    <div v-show="!isFullscreen">
      <Navbar class="navbar" />
    </div>

    <div class="content" :class="{ 'fullscreen': isFullscreen }">
      <!-- All other components hidden in fullscreen mode -->
      <div v-show="!isFullscreen" class="cell performance">
        <WeeklyPerformance />
      </div>
      <div class="cell main-content" :class="{ 'fullscreen': isFullscreen }">
        <MainContent></MainContent>
      </div>
      <div v-show="!isFullscreen" class="cell spotify">smth</div>
      <div v-show="!isFullscreen" class="cell categories">
        <CategoriesComp />
      </div>
      <div v-show="!isFullscreen" class="cell calendar">
        <CalendarComp />
      </div>
      <div v-show="!isFullscreen" class="cell smth">spotify</div>
    </div>
  </div>
</template>


<script setup>
import CalendarComp from '@/components/Calendar/CalendarComp.vue';
import CategoriesComp from '@/components/Categories/CategoriesComp.vue';
import MainContent from '@/components/MainPage/MainContent.vue';
import Navbar from '@/components/Navbar/Navbar.vue';
import WeeklyPerformance from '@/components/Performance/WeeklyPerformance.vue';
import { useTimerStore } from '@/store/timer';
import { storeToRefs } from 'pinia';

const timerStore = useTimerStore();
const { isFullscreen } = storeToRefs(timerStore);
</script>

<style scoped>
.layout {
  display: grid;
  grid-template-areas:
    "navbar"
    "content";
  grid-template-rows: auto 1fr;
  height: 100vh;
  transition: all 0.3s ease;
}

.layout.fullscreen {
  grid-template-areas: "content";
  grid-template-rows: 1fr;
  overflow: hidden;
}

.navbar {
  grid-area: navbar;
}

.content {
  grid-area: content;
  display: grid;
  grid-template-areas:
    "performance main spotify"
    "categories main smth"
    "categories calendar smth";
  grid-template-columns: 1fr 3fr 1fr;
  grid-template-rows: 3fr 2fr auto;
  gap: 10px;
  padding: 1rem;
  padding-top: 0;
  margin-top: 10px;
  box-sizing: border-box;
  transition: all 0.3s ease;
}

.content.fullscreen {
  grid-template-areas: "main";
  grid-template-columns: 1fr;
  grid-template-rows: 1fr;
  gap: 0;
  padding: 0;
  margin-top: 0;
  overflow: hidden;
}

.performance {
  grid-area: performance;
  border: 1.4px dashed var(--color-border);
  padding: 0;
}

.spotify {
  grid-area: spotify;
}

.smth {
  grid-area: smth;
}

.main-content {
  grid-area: main;
  background-color: var(--color-background-mute);
  border: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  transition: opacity 0.3s ease, background-color 0.3s ease, border 0.3s ease;
}

.main-content.fullscreen {
  background: var(--color-background-mute);
  border: none;
  border-radius: 0;
  justify-content: center;
  overflow: visible;
  padding: 20px;
  height: auto;
  min-height: 100vh;
}

.categories {
  grid-area: categories;
  border: 1.4px dashed var(--color-border);
  padding: 0;
}

.cell {
  padding: 10px;
  border-radius: 8px;
}

.calendar {
  grid-area: calendar;
  /* padding: 0; */
}
</style>
