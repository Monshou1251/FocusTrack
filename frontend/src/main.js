import './assets/main.css'

import '@fortawesome/fontawesome-free/css/all.css'
import axios from 'axios'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia) // 👈 добавляем pinia

app.use(router)

app.mount('#app')
