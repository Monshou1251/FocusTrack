<template>
  <Navbar />
  <div class="container">
    <div class="container-wrapper">
      <div class="text-container">
        <h1 class="text">FocusTrack</h1>
      </div>
      <div class="input-main">
        <div>
          <div class="form-group">
            <svg-icon class="input-icons" v-if="!email" type="mdi" :path="mdiAt"></svg-icon>
            <input
              type="email"
              name="email"
              v-model="email"
              class="form-control"
              placeholder="email"
            />
          </div>
          <div class="form-group">
            <svg-icon class="input-icons" v-if="!password" type="mdi" :path="mdiKeyVariant"></svg-icon>
            <input
              type="password"
              name="password"
              v-model="password"
              class="form-control"
              placeholder="password"
            />
          </div>
        </div>
        <div class="button-group">
          <button type="submit" class="button-signin" @click="signIn">Sign in</button>
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
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import SvgIcon from '@jamescoyle/vue-icon'
// import SpinnerLoad from '@/components/Helpers/SpinnerLoad.vue'
import { mdiAt, mdiKeyVariant, mdiGoogle, mdiGithub} from '@mdi/js'
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router';
import { GoogleOAuthProvider } from 'google-oauth-gsi';

const router = useRouter();

const email = ref("")
const password = ref("")

const signIn = async () => {
  try {
    const form = new FormData()
    form.append('username', email.value)
    form.append('password', password.value)

    const response = await axios.post('/api/auth/login', form)

    if (response.status == 200) {
      alert("✅ Успешный вход!");
      // router.push({ name: 'home' })
    } else {
      console.log('Unexpected code:', response.status)
    }

  } catch (error) {
    console.log('Error occurred:', error.response?.data?.detail ?? error)
  }
}


const signUp = async () => {
  try {
    const form = new FormData();
    form.append('username', email.value);
    form.append('password', password.value);

    const response = await axios.post('/api/auth/register', form);
    const data = response.data;

    if (data.success) {
      alert("✅ Успешная регистрация!");
    } else {
      alert("❌ Ошибка: " + (data.error || "Неизвестная ошибка"));
    }

  } catch(error) {
    // Ошибка HTTP или сети
    if (error.response && error.response.data && error.response.data.detail) {
      alert("❌ Ошибка: " + error.response.data.detail);
    } else {
      alert("❌ Ошибка: " + error.message);
    }
    console.error('Error occured:', error);
  }
}


const googleProvider = new GoogleOAuthProvider({
    clientId: "107837184301-fascjn9elhupdsdasvjd87iqjangdrt4.apps.googleusercontent.com",
    onScriptLoadError: () => console.log('onScriptLoadError'),
    onScriptLoadSuccess: () => console.log('onScriptLoadSuccess'),
});

const handleGoogleLogin = googleProvider.useGoogleLogin({
  flow: 'auth-code',
  onSuccess: async (res) => {
    console.log('Logged in with Google', res);
    try {
      const response = await axios.post('/api/auth/google_auth', res);
      console.log('✅ Auth success:', response.data);
      alert('✅ Успешный вход через Google!');
    } catch (e) {
      console.error('❌ Auth error:', e);
      alert('❌ Ошибка при входе через Google.');
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
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100vh;
  width: 100%;
}

.container-wrapper {
  padding: 30px;
  margin-bottom: 20%;
  /* border: solid 1px var(--color-border); */
  border-radius: 10px;
  border-color: transparent; /* Start with transparent border */
  /* animation: borderFadeIn 4s ease forwards 6s; */
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
  font-size: 38px;
  font-weight: 800;
  /* opacity: 0; */
  /* animation:
    fadeIn 4s ease forwards 1s,
    moveAndResize 1s ease forwards 5s; */
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
  font-family: 'Jost';
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

.form-group:not(:placeholder-shown):focus + svg {
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
  transition: background-color  0.2s ease-in-out, opacity  0.2s ease-in-out;
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
