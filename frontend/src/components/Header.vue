<script setup lang="ts">
defineProps<{
  cusheader: string
}>()
</script>

<template>
  <div class="headers">
    <h1>{{ cusheader }}</h1>
  </div>
</template>

<style scoped>
.headers h1 {
  text-align: center;
  align-items: center;
  justify-content: center;
  width: 100%;
  font-size: 2.5rem;
  font-family: '思源黑体 Medium', sans-serif;
  color: #333;
}
</style>
