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
        <el-header>Header</el-header>
        <el-main>
          <component :is="currentComponent" />
        </el-main>
        <el-footer>Footer</el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, markRaw } from 'vue'

import HomeView from './views/HomeView.vue'
import EncryptionView from './views/EncryptionView.vue'
import DecryptionView from './views/DecryptionView.vue'
import ToolsView from './views/ToolsView.vue'

const currentComponent = ref(markRaw(HomeView))

const showHome = () => {
  currentComponent.value = HomeView
}

const showEncryption = () => {
  currentComponent.value = EncryptionView
}

const showDecryption = () => {
  currentComponent.value = DecryptionView
}

const showTools = () => {
  currentComponent.value = ToolsView
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

.el-header {
  text-align: center;
  align-items: center;
  width: 100%;
  line-height: 100px;
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
  width: 95%;
  overflow: visible;
  justify-content: center;
  align-items: center;
}
</style>
