<template>
  <div class="common-layout">
    <el-container>
      <el-aside>
        <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="75" height="75" />
        <div class="wrapper">
          <el-button @click="showHome" type="primary" plain>Home</el-button>
          <el-button @click="showEncryption" type="primary" plain>Encryption</el-button>
          <el-button @click="showDecryption" type="primary" plain>Decryption</el-button>
          <el-button @click="showTools" type="primary" plain>Tools</el-button>
        </div>
      </el-aside>

      <el-container class="inner-el-container">
        <el-header>
          <Header :cusheader="headerTitle"> </Header>
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
import { ref, shallowRef } from 'vue'

import HomeView from './views/HomeView.vue'
import EncryptionView from './views/EncryptionView.vue'
import DecryptionView from './views/DecryptionView.vue'
import ToolsView from './views/ToolsView.vue'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'

const currentComponent = shallowRef(HomeView)

const headerTitle = ref('Home')

const showHome = () => {
  currentComponent.value = HomeView
  headerTitle.value = 'Home'
}

const showEncryption = () => {
  currentComponent.value = EncryptionView
  headerTitle.value = 'Encryption'
}

const showDecryption = () => {
  currentComponent.value = DecryptionView
  headerTitle.value = 'Decryption'
}

const showTools = () => {
  currentComponent.value = ToolsView
  headerTitle.value = 'Tools'
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
  width: 12%;
  min-width: 130px;
  position: fixed;
  z-index: 5;
}

.wrapper {
  display: grid;
  flex-direction: column;
  margin-top: 2rem;
}

.el-button {
  margin-bottom: 1rem;
  font-size: 1rem;
}

.el-button + .el-button {
  margin-left: 0;
}

.inner-el-container {
  margin-left: max(calc(12% + 20px), calc(130px + 10px));
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
  margin-top: 2rem;
}

.el-footer {
  background-color: white;
  z-index: 10;
  justify-content: center;
}
</style>
