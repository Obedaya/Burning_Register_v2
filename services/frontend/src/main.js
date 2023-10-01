import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import axios from 'axios';
import { loadFonts } from './plugins/webfontloader'
import { createPinia } from 'pinia'

loadFonts()

const pinia = createPinia()

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:9090/';  // the FastAPI backend

axios.interceptors.response.use(undefined, function (error) {
  if (error) {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      return router.push('/login')
    }
  }
});

createApp(App)
  .use(router)
  .use(vuetify)
  .use(pinia)
  .mount('#app')
