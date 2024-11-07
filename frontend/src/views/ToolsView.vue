<template>
  <div class="tools">
    <h1>This is ToolsView page</h1>
    <div class="file-container">
      <el-upload
        action=""
        class="upload-component"
        :drag="true"
        multiple
        :on-change="handleFileChange"
        :file-list="fileList"
        :before-upload="beforeUpload"
        :show-file-list="false"
        :auto-upload="false"
        accept="*"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">Choose files that need to be hashed</div>
        <div class="el-upload__tip">Support all file types</div>
      </el-upload>
    </div>
    <el-button type="primary" round @click="calculateHash">Calculate Hash</el-button>
    
    <div class="hash-table-container" v-if="hashResults.length > 0">
      <el-table :data="hashResults" border stripe height="72vh" style="width: 100%">
        <el-table-column
          prop="fileName"
          label="File Name"
          min-width="17%"
        />
        <el-table-column
          prop="hash"
          label="SHA-256 Hash"
          min-width="83%"
        />
      </el-table>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref } from 'vue'
import CryptoJS from 'crypto-js'
import { ElMessage } from 'element-plus'

const fileList = ref<File[]>([])
const hashResults = ref<{ fileName: string; hash: string, raw: File }[]>([])


const handleFileChange = (file: { raw: File }) => {
  hashResults.value.push({ fileName: file.raw.name, hash: '', raw: file.raw })
}


const calculateHash = async () => {
  for (let i = 0; i < hashResults.value.length; i++) {
    const file = hashResults.value[i]
    const hash = await getFileHash(file.raw)
    hashResults.value[i].hash = hash
  }
}

const getFileHash = (file: File): Promise<string> => {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const fileContent = e.target?.result
      const hash = CryptoJS.SHA256(CryptoJS.lib.WordArray.create(fileContent as ArrayBuffer))
        .toString(CryptoJS.enc.Hex)
        .toUpperCase()
      resolve(hash)
    }
    reader.readAsArrayBuffer(file) 
  })
}

const beforeUpload = (file: File) => {
  const isValidSize = file.size / 1024 < 10 // Limit to 10GB
  if (!isValidSize) {
    ElMessage.error('Custom image size cannot exceed 10MB')
  }
  return isValidSize
}
</script>

<style>
.tools {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.el-upload-dragger {
  padding: 10px 10px 10px 10px; 
}

.file-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 800px;
  border-radius: 10px;
  overflow: hidden;
  padding: 0 0 10px 0;
}

.upload-component {
  margin: 0 10px;
  flex: 1;
}

el-button {
  margin-bottom: 10px;
}

.hash-table-container {
  max-height: 80vh;
  overflow-y: auto;
  width: 45vw;
  padding-top: 10px;
}

.el-table {
  margin-top: 10px;
  margin: 0;
}

@media (min-width: 1024px) {
  .tools {
    min-height: 100vh;
  }
}
</style>
