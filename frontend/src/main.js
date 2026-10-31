import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import './style.css'
import App from './App.vue'
import { useThemeStore } from './stores/theme'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Iniciar configuración del tema (Claro/Oscuro/Sistema)
const themeStore = useThemeStore()
themeStore.iniciarEscuchaSistema()

app.mount('#app')
