<template>
  <div class="common-layout">
    <el-container>
      <el-aside>
        <img alt="Guest Liang logo" class="logo" src="@/assets/GuestLianglogo.svg" width="130" height="130" />
        <div class="wrapper">
          <el-button @click="showHome" type="primary" :plain="selectedPage !== 'Home'">{{ t('Navigation.Home') }}</el-button>
          <el-button @click="showEncryption" type="primary" :plain="selectedPage !== 'Encryption'">{{ t('Navigation.Encryption') }}</el-button>
          <el-button @click="showDecryption" type="primary" :plain="selectedPage !== 'Decryption'">{{ t('Navigation.Decryption') }}</el-button>
          <el-button @click="showTools" type="primary" :plain="selectedPage !== 'Tools'">{{ t('Navigation.Tools') }}</el-button>
        </div>
      </el-aside>

      <el-container class="inner-el-container">
        <el-header>
          <Header :cusheader="t(`Navigation.${selectedPage}`)"> </Header>
        </el-header>
        <el-main>
          <component :is="currentComponent" />
        </el-main>
      </el-container>

      <el-footer>
        <Footer></Footer>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { useTranslation } from 'i18next-vue'
const { t, i18next } = useTranslation()

onMounted(() => {
  console.log('[Vue] onMounted, checking window.electron:', window.electron) // 检查 window.electron 是否存在

  if (window.electron?.changeLanguage) {
    console.log('[Vue] Listening for language change') // 确保监听
    window.electron.changeLanguage((lang) => {
      console.log('[Vue] Received language change:', lang) // 是否收到 IPC 事件
      i18next.changeLanguage(lang).then(() => {
        console.log('[Vue] Language changed to:', i18next.language) // Vue 端是否真的切换
      })
    })
  } else {
    console.error('[Vue] window.electron.changeLanguage is undefined') // Vue 未正确注入 Electron API
  }
})

import { ref, shallowRef, onMounted } from 'vue'

import HomeView from './views/HomeView.vue'
import EncryptionView from './views/EncryptionView.vue'
import DecryptionView from './views/DecryptionView.vue'
import ToolsView from './views/ToolsView.vue'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'

const currentComponent = shallowRef(HomeView)

const selectedPage = ref('Home')

const showHome = () => {
  currentComponent.value = HomeView
  selectedPage.value = 'Home'
}

const showEncryption = () => {
  currentComponent.value = EncryptionView
  selectedPage.value = 'Encryption'
}

const showDecryption = () => {
  currentComponent.value = DecryptionView
  selectedPage.value = 'Decryption'
}

const showTools = () => {
  currentComponent.value = ToolsView
  selectedPage.value = 'Tools'
}
</script>

<style scoped>
.common-layout {
  height: 100%;
  width: 100%;
  margin: 0;
}

.el-container {
  height: 100%;
  display: flex;
}

.el-aside {
  text-align: center;
  height: calc(100% - 90px);
  width: 15%;
  min-width: 150px;
  position: fixed;
  z-index: 5;
}

.wrapper {
  display: grid;
  flex-direction: column;
  margin-top: 0;
}

.el-button {
  margin-bottom: 1rem;
  font-size: 1rem;
}

.el-button + .el-button {
  margin-left: 0;
}

.inner-el-container {
  margin-left: max(calc(15% + 20px), calc(150px + 10px)); /* 和.el-aside的width\min-width保持一致*/
  flex-direction: column;
  height: calc(100vh - 90px);
}

.el-main {
  width: 100%;
  height: 100%;
  overflow: hidden;
  justify-content: center;
  align-items: center;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  margin-top: 1rem;
  overflow-y: auto;
}

.el-footer {
  background-color: white;
  z-index: 10;
  justify-content: center;
}
</style>
