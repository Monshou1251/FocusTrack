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
      <div class="cell calendar">calendar</div>
      <div class="cell smth">smth</div>
    </div>
  </div>
</template>


<script setup>
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
    "categories calendar smth";
  grid-template-columns: 1fr 3fr 1fr;
  grid-template-rows: 3fr 2fr;
  gap: 10px;
  padding: 1rem;
  padding-top: 0;
  margin-top: 10px;
  box-sizing: border-box;
}

.cell {
  padding: 10px;
  border-radius: 8px;
}

.main-content {
  background-color: var(--color-background-mute);
  border: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.calendar {
  border: 1px solid var(--color-border);

}

.categories {
  border: 1.4px dashed var(--color-border);
  padding: 0;
}
</style>
