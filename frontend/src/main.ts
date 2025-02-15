import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'

import i18next from 'i18next'
import I18NextVue from 'i18next-vue'

import en from './locales/en-US.json'
import zh from './locales/zh-CN.json'
import type { I18nSchema } from './locales/types'

 // TypeScript 校验 JSON 结构
const enTyped: I18nSchema = en
const zhTyped: I18nSchema = zh

i18next.init({
  lng: 'en-US',
  fallbackLng: 'en-US',
  resources: {
    'en-US': { translation: enTyped },
    'zh-CN': { translation: zhTyped }
  }
})

const app = createApp(App)

app.use(I18NextVue, { i18next })

app.use(ElementPlus)
app.use(createPinia())
app.use(router)

app.mount('#app')
