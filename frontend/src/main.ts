import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import {useAuthStore} from "@/stores/auth";
import Toast from 'vue-toastification';
import "vue-toastification/dist/index.css";


const app = createApp(App)

app.use(createPinia())
app.use(router)

app.use(Toast, {
  position: "top-right",
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: "button",
  icon: true,
});

const authStore = useAuthStore();
authStore.loadTokens();

app.mount('#app')

