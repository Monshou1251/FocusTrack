<template>
  <Navbar />
  <Spinner v-if="isLoading" />
  <div class="container">
    <div class="container-wrapper">
      <div class="text-container">
        <h1 class="text">FocusTrack</h1>
      </div>
      <div class="input-main">
        <form @submit.prevent="signIn">
          <div>
            <div class="form-group">
              <svg-icon class="input-icons" v-if="!email" type="mdi" :path="mdiAt"></svg-icon>
              <input type="email" name="email" v-model="email" class="form-control" placeholder="email" />
            </div>
            <div class="form-group">
              <svg-icon class="input-icons" v-if="!password" type="mdi" :path="mdiKeyVariant"></svg-icon>
              <input type="password" name="password" v-model="password" class="form-control" placeholder="password" />
            </div>
          </div>
          <div class="button-group">
            <button type="submit" class="button-signin">Sign in</button>
            <button type="submit" class="button-signup" @click="signUp">Sign up</button>
          </div>
          <div class="google-git-icons">
            <div class="google-git-icons-item" title="Login with Google">
              <svg-icon type="mdi" :path="mdiGoogle" @click="handleGoogleLogin"></svg-icon>
            </div>
            <div class="google-git-icons-item" title="Login with Github">
              <svg-icon type="mdi" :path="mdiGithub"></svg-icon>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar/Navbar.vue'
import SvgIcon from '@jamescoyle/vue-icon'
// import SpinnerLoad from '@/components/Helpers/SpinnerLoad.vue'
import Spinner from '@/components/helpers/Spinner.vue'
import { useAuthStore } from '@/store/auth'
import { mdiAt, mdiGithub, mdiGoogle, mdiKeyVariant } from '@mdi/js'
import axios from 'axios'
import { GoogleOAuthProvider } from 'google-oauth-gsi'
import { ref } from 'vue'
import { useRouter } from 'vue-router'


const authStore = useAuthStore()

const router = useRouter();

const email = ref("")
const password = ref("")

const isLoading = ref(false)

const signIn = async () => {
  isLoading.value = true
  try {
    const form = new FormData()
    form.append('email', email.value)
    form.append('password', password.value)

    const response = await axios.post('/api/auth/login', form)
    const data = response.data

    if (data.success) {
      try {
        await authStore.fetchCurrentUser()
        router.push('/main')
      } catch (e) {
        console.error("❌ fetchCurrentUser failed:", e)
        alert("❌ Ошибка при получении данных пользователя")
      }
    } else {
      alert("❌ Error: " + (data.error ?? data.message ?? "Login failed"))
    }

  } catch (error) {
    const errData = error.response?.data
    const errMsg = errData?.message ?? "Login failed11"
    alert("❌ " + errMsg)
  } finally {
    isLoading.value = false
  }
}


const signUp = async () => {
  isLoading.value = true
  if (!email.value.trim() || !password.value.trim()) {
    alert("❌ Please enter both email and password.")
    return
  }
  try {
    const form = new FormData()
    form.append('email', email.value)
    form.append('password', password.value)

    const response = await axios.post('/api/auth/register', form)
    const data = response.data

    if (data.success) {
      alert("✅ Successfully registered!")
    } else {
      alert("❌ Error: " + (data.error ?? "Registration failed"))
    }

  } catch (error) {
    console.log(error)
    const errData = error?.response?.data
    const errMsg = errData?.message ?? "Registration failed2"
    alert("❌ " + errMsg)
    console.error("Registration error:", error)
  } finally {
    isLoading.value = false
  }
}


const googleProvider = new GoogleOAuthProvider({
  clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID,
  onScriptLoadError: () => console.log('onScriptLoadError'),
  onScriptLoadSuccess: () => console.log('onScriptLoadSuccess'),
});

const handleGoogleLogin = googleProvider.useGoogleLogin({
  flow: 'auth-code',
  onSuccess: async (res) => {
    console.log('Logged in with Google', res);
    try {
      isLoading.value = true
      const response = await axios.post('/api/auth/google_auth', res);
      const data = response.data

      if (data.success) {
        await authStore.fetchCurrentUser()
        router.push('/main')
      } else {
        alert("❌ Error: " + (data.error ?? data.message ?? "Login failed"))
      }
      console.log('✅ Auth success:', response.data);
    } catch (e) {
      console.error('❌ Auth error:', e);
      alert('❌ Ошибка при входе через Google.');
    } finally {
      isLoading.value = false
    }
  },
  onError: (err) => {
    console.error('❌ Failed to login with Google:', err);
    alert('❌ Ошибка: не удалось авторизоваться через Google.');
  },
});


document.addEventListener('mousemove', function (e) {
  const gradientText = document.querySelector('.text')
  const xPos = e.clientX
  const yPos = e.clientY
  gradientText.style.backgroundPosition = `${0.2 * xPos}px ${0.2 * yPos}px`
})
</script>

<style scoped>
.container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding-bottom: 80px;
}

.container-wrapper {
  padding: 30px;
  border-radius: 10px;
  border-color: transparent;
}

.text-container {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: default;
  padding-bottom: 15px;
}

.text {
  /* font-size: 48px; */
  font-size: 36px;
  font-weight: 800;
  font-family: 'Bruno_Ace';

  background-image: linear-gradient(to right,
      var(--color-warm-yellow),
      var(--color-coral-red),
      var(--color-sky-blue),
      var(--color-mint-green),
      var(--color-soft-purple),
      var(--color-light-pink));
  color: transparent;
  background-clip: text;
}

.input-main {
  position: relative;
  font-size: 18px;
  /* animation: fadeIn 4s ease forwards 6s; */
  /* opacity: 0; */
  /* margin-bottom: 20%; */
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

.input-icons {
  position: absolute;
  display: inline-block;
  color: #2c3e5061;
  scale: 0.7;
  margin-top: 7px;
  margin-left: 7px;
}

.email-input {
  background-color: var(--color-background-mute);
  color: var(--color-text);
}

.email-icon {
  color: var(--color-text);
  opacity: 0.4;
}

input::placeholder {
  /* color: #2c3e5090; */
  font-size: 18px;
  font-family: 'Albert_Sans';
  padding-left: 23px;
  transform: translateY(-1px);
}

input:-webkit-autofill {
  transition: background-color 5000s ease-in-out 0s;
}

.form-control:focus {
  outline: 1px solid #2b414149;
}

.form-group:focus-within svg {
  display: none;
  margin-left: -20px;
}

.form-group:focus-within input::placeholder {
  display: none;
  color: transparent;
}

.form-group:not(:placeholder-shown):focus+svg {
  display: none;
}

.button-group {
  display: flex;
  justify-content: space-between;
  padding-top: 10px;
}

.button-signin {
  border: solid 2px var(--color-border);
  background-color: var(--color-background-mute);
}

.button-signup {
  background-color: var(--color-background);
  border: none;
}

button {
  font-size: 18px;
  font-family: 'Albert_Sans';
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

.google-git-icons {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin-top: 26px;
  gap: 25px;
  scale: 1.4;
}

.google-git-icons-item {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  opacity: 0.4;

}

.google-git-icons-item:hover {
  background-color: var(--color-background-mute);
  cursor: pointer;
  transition: background-color 0.2s ease-in-out, opacity 0.2s ease-in-out;
  opacity: 1;
}

.google-git-icons-item[title]:hover::after {
  /* content: attr(title +); */
  border-radius: 10%;
}


@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes borderFadeIn {
  from {
    border-color: transparent;
  }

  to {
    border-color: var(--color-border);
  }
}

@keyframes moveAndResize {
  0% {
    transform: translateY(0);
    font-size: 48px;
    font-weight: 800;
  }

  100% {
    font-size: 32px;
    font-weight: 600;
  }
}
</style>
