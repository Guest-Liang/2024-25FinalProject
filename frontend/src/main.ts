import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'

import i18next from 'i18next'
import I18NextVue from 'i18next-vue'

i18next.init({
  lng: 'en-US',
  resources: {
    'zh-CN': {
      translation: {
        greeting: '你好，世界！',
      },
    },
    'en-US': {
      translation: {
        greeting: 'Hello, World!',
      },
    },
  },
})

const app = createApp(App)

app.use(I18NextVue, { i18next })

app.use(ElementPlus)
app.use(createPinia())
app.use(router)

app.mount('#app')
