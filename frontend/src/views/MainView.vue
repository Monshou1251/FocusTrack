<template>
  <div class="layout">
    <div>
      <Navbar class="navbar" />
    </div>
    <div class="content">
      <div class="cell performance">Performance</div>
      <div class="cell main-content">
        <MainContent></MainContent>
      </div>
      <div class="cell spotify">spotify</div>
      <div class="cell categories">
        <CategoriesComp />
      </div>
      <div class="cell calendar">
        <CalendarComp />
      </div>
      <div class="cell smth">smth</div>
    </div>
  </div>
</template>


<script setup>
import CalendarComp from '@/components/Calendar/CalendarComp.vue';
import CategoriesComp from '@/components/Categories/CategoriesComp.vue';
import MainContent from '@/components/MainPage/MainContent.vue';
import Navbar from '@/components/Navbar/Navbar.vue';
</script>

<style scoped>
.layout {
  display: grid;
  grid-template-areas:
    "navbar"
    "content";
  grid-template-rows: auto 1fr;
  height: 100vh;
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
}

.performance {
  grid-area: performance;
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
