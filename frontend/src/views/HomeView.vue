<template>
  <div class="landing-page" :class="{ 'fade-out': isTransitioning }">
    <div class="landing-content">
      <!-- Left side: App name and description -->
      <div class="left-section">
        <h1 class="app-title">FocusTrack</h1>
        <p class="app-description">
          <span v-for="(char, index) in 'Your personal focus timer for maximum productivity'" :key="index" class="char"
            :style="{ animationDelay: `${1.5 + index * 0.05}s` }">
            {{ char === ' ' ? '\u00A0' : char }}
          </span>
        </p>
        <p class="app-tagline">
          <span v-for="(char, index) in 'Stay focused'" :key="index" class="char highlight"
            :style="{ animationDelay: `${2 + index * 0.05}s` }">
            {{ char === ' ' ? '\u00A0' : char }}
          </span>
        </p>
      </div>

      <!-- Right side: Big arrow -->
      <div class="right-section">
        <div class="arrow-container" @click="goToLogin">
          <div class="arrow-circle">
            <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="arrowGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" style="stop-color:var(--color-warm-yellow)" />
                  <stop offset="20%" style="stop-color:var(--color-coral-red)" />
                  <stop offset="40%" style="stop-color:var(--color-sky-blue)" />
                  <stop offset="60%" style="stop-color:var(--color-mint-green)" />
                  <stop offset="80%" style="stop-color:var(--color-soft-purple)" />
                  <stop offset="100%" style="stop-color:var(--color-light-pink)" />
                </linearGradient>
              </defs>
              <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="url(#arrowGradient)" stroke-width="3"
                stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isTransitioning = ref(false)

const goToLogin = async () => {
  isTransitioning.value = true

  // Ждем завершения анимации исчезновения
  // await new Promise(resolve => setTimeout(resolve, 500))
  await new Promise(resolve => setTimeout(resolve, 500))

  // Переходим на страницу логина
  router.push('/login')
}
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-background) -50%, var(--color-background-mute) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Albert_Sans', sans-serif;
}

.landing-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  padding: 0 5%;
  gap: 100px;
}

.left-section {
  flex: 1;
  max-width: 600px;
}

.app-title {
  font-family: 'Bruno_Ace', sans-serif;
  font-size: 6rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
  line-height: 1;
  margin-bottom: 30px;
  animation: titleGlow 5s ease-in-out infinite, slideInFromTop 1.5s ease-out forwards;
  opacity: 0;
  transform: translateY(-100px);
}

@keyframes titleGlow {

  0%,
  100% {
    text-shadow: 0 0 20px rgba(255, 205, 75, 0.3);
  }

  50% {
    text-shadow: 0 0 40px rgba(255, 205, 75, 0.6);
  }
}

/* Entrance animations */
@keyframes slideInFromTop {
  0% {
    opacity: 0;
    transform: translateY(-100px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scaleIn {
  0% {
    opacity: 0;
    transform: scale(0.5);
  }

  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Typewriter effect */
.char {
  display: inline-block;
  opacity: 0;
  animation: typeIn 0.1s ease-out forwards;
}

/* Page transition */
.landing-page {
  transition: all 0.5s ease-out;
}

.landing-page.fade-out {
  opacity: 0;
  transform: translateY(-50px);
}

@keyframes typeIn {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.app-description {
  font-family: 'Jost', sans-serif;
  font-size: 1.5rem;
  color: var(--color-text-mute);
  margin: 0;
  line-height: 1.4;
  margin-bottom: 20px;
}

.app-tagline {
  font-family: 'Jost', sans-serif;
  font-size: 1.1rem;
  color: var(--color-text-mute);
  margin: 0;
  line-height: 1.4;
}

.highlight {
  color: var(--color-warm-yellow);
  font-weight: 600;
}

.right-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.arrow-container {
  cursor: pointer;
  transition: transform 0.3s ease;
  border-radius: 100%;
}

/* Hover эффекты для стрелки */
.arrow-container:hover .arrow-circle {
  border-color: var(--color-primary);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  transform: scale(1.02);
}

.arrow-container:hover .arrow-icon {
  transform: translateX(3px);
}



.arrow-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: transparent;
  border: 8px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  animation: scaleIn 1s ease-out 2.5s forwards;
  opacity: 0;
  transform: scale(0.5);
}



.arrow-icon {
  width: 48px;
  height: 48px;
  transition: all 0.3s ease;
  animation: gradientShift 2s linear infinite;
}



/* Анимация для градиента */
@keyframes gradientShift {
  0% {
    filter: hue-rotate(0deg);
  }

  100% {
    filter: hue-rotate(360deg);
  }
}



/* Responsive design */
@media (max-width: 768px) {
  .landing-content {
    flex-direction: column;
    text-align: center;
    gap: 60px;
  }

  .app-title {
    font-size: 4rem;
  }

  .app-description {
    font-size: 1.2rem;
  }

  .arrow-circle {
    width: 100px;
    height: 100px;

  }

  .arrow-icon {
    width: 40px;
    height: 40px;
  }
}

@media (max-width: 480px) {
  .app-title {
    font-size: 3rem;
  }

  .app-description {
    font-size: 1.1rem;
  }

  .arrow-circle {
    width: 80px;
    height: 80px;
  }

  .arrow-icon {
    width: 32px;
    height: 32px;
  }
}
</style>
