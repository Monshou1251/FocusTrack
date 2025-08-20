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
      <div v-show="!isFullscreen" class="cell daily">
        <DailyPerformance />
      </div>
      <div v-show="!isFullscreen" class="cell categories">
        <CategoriesComp />
      </div>
      <div v-show="!isFullscreen" class="cell calendar">
        <CalendarComp />
      </div>
      <div v-show="!isFullscreen" class="cell ai-chat">
        <AIChatComp />
      </div>
    </div>
  </div>
</template>


<script setup>
import AIChatComp from '@/components/AI/AIChatComp.vue';
import CalendarComp from '@/components/Calendar/CalendarComp.vue';
import CategoriesComp from '@/components/Categories/CategoriesComp.vue';
import MainContent from '@/components/MainPage/MainContent.vue';
import Navbar from '@/components/Navbar/Navbar.vue';
import DailyPerformance from '@/components/Performance/DailyPerformance.vue';
import WeeklyPerformance from '@/components/Performance/WeeklyPerformance.vue';
import { useCategoryStore } from '@/store/categories';
import { useSprintStore } from '@/store/sprints';
import { useTimerStore } from '@/store/timer';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';

const timerStore = useTimerStore();
const { isFullscreen } = storeToRefs(timerStore);

// One-time bootstrap of shared data
const sprintStore = useSprintStore();
const categoryStore = useCategoryStore();

onMounted(async () => {
  await Promise.all([
    sprintStore.fetchSprints(),
    categoryStore.fetchCategories()
  ]);
});
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
    "performance main daily"
    "categories main ai-chat"
    "categories calendar ai-chat";
  grid-template-columns: 1fr 3fr 1fr;
  grid-template-rows: 3fr 2fr auto;
  gap: 10px;
  padding: 1rem;
  padding-top: 0;
  margin-top: 10px;
  box-sizing: border-box;
  transition: all 0.3s ease;
  min-height: 0;
  /* NEW */
  min-width: 0;
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



.daily {
  grid-area: daily;
  min-width: 0;
  overflow: hidden;
  border: 1.4px dashed var(--color-border);
}

.cell.ai-chat {
  grid-area: ai-chat;
  border: 1px solid var(--color-border);
  overflow: hidden;

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
  overflow: hidden;
  height: 100%;
}


.calendar {
  grid-area: calendar;
  /* padding: 0; */
}
</style>
