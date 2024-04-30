<template>
  <Navbar />
  <div class="container">
    <div class="text-container">
      <h1 class="text">FocusTrack</h1>
    </div>
    <div class="input-main">
      <!-- <form> -->
      <div class="form-group">
        <svg-icon v-if="!username" type="mdi" :path="mdiAt"></svg-icon>
        <input
          type="text"
          name="username"
          v-model="username"
          class="form-control"
          placeholder="username"
        />
      </div>
      <div class="form-group">
        <svg-icon v-if="!password" type="mdi" :path="mdiKeyVariant"></svg-icon>
        <input
          type="password"
          name="password"
          v-model="password"
          class="form-control"
          placeholder="password"
        />
      </div>
      <div class="button-group">
        <button type="submit" class="button-signin">Sign in</button>
        <button type="submit" class="button-signup">Sign up</button>
      </div>
      <!-- </form> -->
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import SvgIcon from '@jamescoyle/vue-icon'
// import SpinnerLoad from '@/components/Helpers/SpinnerLoad.vue'
import { mdiAt, mdiKeyVariant } from '@mdi/js'
import { ref } from 'vue'

const username = ref()
const password = ref()

document.addEventListener('mousemove', function (e) {
  const gradientText = document.querySelector('.text')
  const xPos = e.clientX
  const yPos = e.clientY
  gradientText.style.backgroundPosition = `${0.2 * xPos}px ${0.2 * yPos}px`
})
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100vh;
  width: 100%;
}

.text-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 20%;
  cursor: default;
}

.text {
  font-size: 48px;
  font-weight: 800;
  opacity: 0;
  animation:
    fadeIn 4s ease forwards 1s,
    moveAndResize 1s ease forwards 5s;
  background-image: linear-gradient(
    to right,
    orange,
    rgb(0, 153, 255),
    rgb(174, 0, 255),
    rgb(255, 0, 170),
    rgb(174, 0, 255),
    #ffcd4b,
    orange
  );
  color: transparent;
  background-clip: text;
}

.input-main {
  position: relative;
  font-size: 18px;
  animation: fadeIn 4s ease forwards 6s;
  opacity: 0;
  margin-bottom: 20%;
  transform: translateY(-90px);
}

.form-group {
  margin-bottom: 20px;
}

.form-control {
  padding: 0;
  width: 260px;
  height: 40px;
  border-radius: var(--border-radius-8);
  border-width: 2px;
  font-size: 18px;
  box-shadow: none;
}

input {
  border-style: solid;
  display: inline-block;
  text-indent: 10px;
}

svg {
  position: absolute;
  display: inline-block;
  color: #2c3e5061;
  scale: 0.7;
  margin-top: 7px;
  margin-left: 7px;
}

input::placeholder {
  color: #2c3e5090;
  font-size: 18px;
  font-family: 'Jost';
  padding-left: 23px;
  transform: translateY(-1px);
}

input:-webkit-autofill {
  transition: background-color 5000s ease-in-out 0s;
}

.form-control:focus {
  outline: 1px solid #2b414149;
  /* border: 2px solid #BDC3C7; */
  /* box-shadow: 0 0 5px #2595be22; */
}

.form-group:focus-within svg {
  display: none;
  margin-left: -20px;
}

.form-group:focus-within input::placeholder {
  display: none;
  color: transparent;
}

.form-group:not(:placeholder-shown):focus + svg {
  display: none;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.button-signin {
  border: solid 4px var(--color-border);
  background-color: var(--color-background-mute);
}

.button-signup {
  background-color: var(--color-background);
  border: none;
}

button {
  font-size: 18px;
  font-family: 'Jost';
  width: 120px;
  height: 40px;
  color: var(--color-text);
  border-radius: var(--border-radius-8);
  cursor: pointer;
  font-weight: 400;
  display: inline-block;
  transition: background-color 0.5s ease;
}

button:hover {
  background-color: var(--color-button-hover);
  border: none;
  color: var(--vt-c-text-dark-1);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes moveAndResize {
  0% {
    /* transform: translate(0, 0); */
    transform: translateY(0);
    font-size: 48px;
    font-weight: 800;
  }
  100% {
    /* transform: translate(-50px, -100px); */
    transform: translateY(-100px);
    font-size: 32px;
    font-weight: 600;
  }
}
</style>
