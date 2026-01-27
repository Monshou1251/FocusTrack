import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'
import VueDevTools from 'vite-plugin-vue-devtools'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), VueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    // Убираем COOP заголовки - они могут блокировать popup окна
    // Для production через nginx COOP будет настроен там
    proxy: {
      '/api': {
        // Локальная разработка: использует localhost:8000 (по умолчанию)
        // Docker: установите VITE_BACKEND_URL=http://backend:8000 в .env или docker-compose
        target: process.env.VITE_BACKEND_URL || 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path,
        configure: (proxy, _options) => {
          proxy.on('error', (err, _req, _res) => {
            console.log('Proxy error:', err);
            console.log('Target URL:', process.env.VITE_BACKEND_URL || 'http://localhost:8000');
          });
          proxy.on('proxyReq', (proxyReq, req, _res) => {
            console.log('Proxying request:', req.method, req.url, '→', proxyReq.path);
          });
        },
      }
    }
  }
})
