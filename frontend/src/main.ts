import 'vue-heatmap-table/dist/vue-heatmap-table.css'
import './assets/main.css'

import '@fortawesome/fontawesome-free/css/all.css'
import axios from 'axios'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

axios.defaults.baseURL = 'http://localhost:8000'
axios.defaults.withCredentials = true

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

app.use(router)

app.mount('#app')
