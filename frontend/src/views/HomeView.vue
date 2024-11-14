<script setup lang="ts">
import Intro from '../components/Intro.vue'
import { onMounted } from 'vue'
import { ElMessageBox } from 'element-plus'

onMounted(() => {
  console.log('HomeView Mounted')
  window.electron.listenDjangoStatus((data: any) => {
    console.log('Django Status:', data.message)
    ElMessageBox.alert(data.message, 'Django Restful API Status', {
      confirmButtonText: 'OK',
      type: 'info',
    }).then(() => {
      setTimeout(() => {
        window.close()
      }, 10000)
    })
  })
})
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
