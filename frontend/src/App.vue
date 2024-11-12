<template>
  <div class="common-layout">
    <el-container>
      <el-aside>
        <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
        <div class="wrapper">
          <el-button @click="showHome" type="primary" plain>Home</el-button>
          <el-button @click="showEncryption" type="primary" plain>Encryption</el-button>
          <el-button @click="showDecryption" type="primary" plain>Decryption</el-button>
          <el-button @click="showTools" type="primary" plain>Tools</el-button>
        </div>
      </el-aside>

      <el-container>
        <el-header>
          <Header :cusheader="headerTitle"> </Header>
        </el-header>
        <el-main>
          <component :is="currentComponent" />
        </el-main>
        <el-footer>
          <Footer></Footer>
        </el-footer>
      </el-container>
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
  height: 100%;
  width: 15%;
  min-width: 150px;
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

.el-container.el-container {
  align-items: center;
}

.el-main {
  width: 97%;
  overflow: visible;
  justify-content: center;
  align-items: center;
  border: 1px solid #e0e0e0;
  border-radius: 15px;
  margin-top: 2rem;
}

.el-footer {
  width: 100%;
}
</style>
