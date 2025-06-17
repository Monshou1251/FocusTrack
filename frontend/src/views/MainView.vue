<template>
  <div class="layout">
    <div>
      <Navbar class="navbar" />
    </div>
    <div class="content">
      <div class="cell performance">Performance</div>
      <div class="cell main-content">
        <div>
          <div>panels</div>
        </div>
        <div class="timer">
          <span class="time-main">12:45</span>
          <span class="time-ms">31</span>
        </div>

        <div>buttons</div>
      </div>
      <div class="cell spotify">spotify</div>
      <div class="cell categories">categories</div>
      <div class="cell calendar">calendar</div>
      <div class="cell smth">smth</div>
    </div>
  </div>
</template>


<script setup>
import Navbar from '@/components/Navbar.vue';
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
  grid-template-rows: 1fr 1fr;
  gap: 10px;
  padding: 1rem;
  padding-top: 0;
  box-sizing: border-box;
}

.cell {
  padding: 1rem;
  border-radius: 8px;
}

.main-content {
  background-color: var(--color-background-mute);
  border: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

.timer {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  font-family: 'Bruno_Ace', sans-serif;
}

.time-main {
  font-size: 64px;
  font-weight: 400;
}

.time-ms {
  font-size: 36px;
  /* Меньше основного времени */
  font-weight: 500;
  color: #999;
  /* Можно сделать серым */
}


.calendar {
  border: 1px solid var(--color-border);
}

.categories {
  border: 1px dashed var(--color-border);
}
</style>
