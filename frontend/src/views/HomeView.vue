<script setup lang="ts">
import Intro from '../components/Intro.vue'
</script>

<template>
  <main>
    <Intro />
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: calc(35vw - 230px);
  height: 100%;
}
</style>
