<template>
  <div class="tools">
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

      <div
        class="button-container"
        style="display: flex; flex-direction: column; height: 100px; width: 150px"
      >
        <el-button
          type="primary"
          round
          @click="calculateHash"
          style="
            font-size: 1rem;
            height: 48%;
            line-height: 1.2rem;
            white-space: normal;
            word-wrap: break-word;
          "
        >
          Calculate Hash
        </el-button>
        <el-button
          type="danger"
          round
          @click="cleanUploadFiles"
          style="
            font-size: 1rem;
            height: 48%;
            margin-top: 4%;
            line-height: 1.2rem;
            white-space: normal;
            word-wrap: break-word;
          "
        >
          Clean up all files
        </el-button>
      </div>
    </div>

    <div class="hash-table-container" v-if="hashResults.length > 0">
      <el-table :data="hashResults" border stripe>
        <el-table-column prop="fileName" label="File Name" min-width="30%" />
        <el-table-column prop="hash" label="SHA-256 Hash" min-width="70%" />
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CryptoJS from 'crypto-js'
import { ElLoading, ElMessage } from 'element-plus'

const fileList = ref<File[]>([])
const hashResults = ref<{ fileName: string; hash: string; raw: File }[]>([])

const handleFileChange = (file: { raw: File }) => {
  hashResults.value.push({ fileName: file.raw.name, hash: '', raw: file.raw })
}

const cleanUploadFiles = () => {
  hashResults.value = []
  fileList.value = []
}

const calculateHash = async () => {
  const loading = ElLoading.service({
    target: '.tools',
    lock: true,
    text: 'Calculating hash...',
    background: 'rgba(0, 0, 0, 0.6)',
  })

  for (let i = 0; i < hashResults.value.length; i++) {
    const file = hashResults.value[i]
    const hash = await getFileHash(file.raw)
    hashResults.value[i].hash = hash
  }

  loading.close()
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
  align-items: center;
  overflow: hidden;
  border-radius: 10px;
  padding-bottom: 10px;
}

.el-upload-dragger {
  padding: 10px 10px 10px 10px;
}

.file-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  border-radius: 10px;
  overflow: hidden;
  padding: 0 0 10px 0;
}

.upload-component {
  margin: 0 10px;
  flex: 1;
}

.hash-table-container {
  max-height: 100%;
  height: calc(100vh - 310px);
  width: 100%;
  min-width: 200px;
  padding-top: 10px;
}

.el-table {
  margin-top: 10px;
  margin: 0;
  height: 100%;
  width: 100%;
}

.el-upload-dragger {
  height: 100px;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 2px dashed #409eff;
  border-radius: 10px;
}

.el-upload-dragger .el-upload__text {
  font-size: 1.4rem;
}

.el-upload__tip {
  font-size: 1rem;
}

.el-button + .el-button {
  margin-left: 0;
}

@media (min-width: 1024px) {
}

@media (max-width: 1024px) {
}
</style>
