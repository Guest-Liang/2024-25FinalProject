<template>
  <div class="decryption">
    <div class="upload-container">
      <el-upload
        action=""
        class="upload-component"
        :drag="true"
        multiple
        :on-change="handleImageChange"
        :file-list="customImageList"
        :before-upload="beforeUpload"
        :on-remove="handleImageRemove"
        :show-file-list="true"
        :auto-upload="false"
        accept="image/png"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          {{
            customImageList.length === 0
              ? 'Select the images you want to decrypt'
              : 'List of chosen files'
          }}
        </div>
        <div v-if="customImageList.length === 0" class="el-upload__tip">
          Only PNG images are supported
        </div>
      </el-upload>
      <div
        class="button-container"
        style="display: flex; flex-direction: column; height: 100px; width: 150px"
      >
        <el-button
          type="primary"
          round
          @click="uploadFiles"
          style="
            font-size: 1rem;
            height: 48%;
            line-height: 1.2rem;
            white-space: normal;
            word-wrap: break-word;
          "
        >
          Upload to Server
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

    <div v-if="downloadLinks.length > 0" class="DownloadLink">
      <h2>Download Links</h2>
      <ul>
        <li v-for="(link, index) in downloadLinks" :key="index">
          <a :href="link.url" download>{{ link.name }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, toRaw } from 'vue'
import { ElLoading, ElMessage, ElMessageBox } from 'element-plus'
import type { DecryptResult, DownloadLink } from '@/types/interface'
import { BACKEND_API } from '@/types/config'

const downloadLinks = ref<DownloadLink[]>([])
const customImageList = ref<File[]>([])

const handleImageChange = (fileList: { raw: File }) => {
  customImageList.value.push(fileList.raw)
}

const handleImageRemove = (file: File) => {
  const index = customImageList.value.indexOf(file)
  if (index > -1) {
    customImageList.value.splice(index, 1)
  }
  console.log(`Removed custom image: ${file.name}`)
}

const cleanUploadFiles = () => {
  customImageList.value = []
  downloadLinks.value = []
}

const beforeUpload = (file: File) => {
  const isPNG = file.type === 'image/png'
  const isValidSize = file.size / 1024 / 1024 < 10 && file.size / 1024 > 200 // Limit to 200KB-10MB
  if (!isValidSize) {
    ElMessage({
      showClose: true,
      message: 'Custom image size cannot exceed 10MB',
      type: 'error',
      duration: 5000,
    })
  }
  if (!isPNG) {
    ElMessage({
      showClose: true,
      message: 'Only PNG images are supported',
      type: 'error',
      duration: 5000,
    })
  }
  return isValidSize && isPNG
}

const uploadFiles = async () => {
  const loading = ElLoading.service({
    target: '.upload-container',
    lock: true,
    text: 'Fetching Data',
    background: 'rgba(0, 0, 0, 0.6)',
  })

  let RawCustomImageList = toRaw(customImageList.value)
  if (customImageList.value.length === 0) {
    ElMessage({
      showClose: true,
      message: 'Please choose at least one file to encrypt!',
      type: 'warning',
      duration: 5000,
    })
    loading.close()
    return
  }

  const formData = new FormData()
  RawCustomImageList.forEach((file) => {
    formData.append('file', file)
  })

  try {
    loading.setText('Waiting for process...')
    const response = await fetch(`http://${BACKEND_API}/api/decrypt/`, {
      method: 'POST',
      body: formData,
    })

    if (response.ok) {
      const data = await response.json()
      downloadLinks.value = data.results.map((item: DecryptResult) => {
        const fileName = item.DecryptedFilePath.split('\\').pop()
        return {
          name: fileName,
          url: `http://${BACKEND_API}/api/download/${fileName}`,
        }
      })
      ElMessageBox.alert(data.message, 'Success', {
        confirmButtonText: 'OK',
        type: 'success',
      })
    } else {
      ElMessageBox.alert('File upload failed!', 'Error', {
        confirmButtonText: 'OK',
        type: 'error',
      })
      console.error('Upload failed:', response)
    }
  } catch (error) {
    console.error('Upload error:', error)
    ElMessageBox.alert('Error uploading file!', 'Error', {
      confirmButtonText: 'OK',
      type: 'error',
    })
  } finally {
    loading.close()
  }
}
</script>

<style scoped>
.decryption {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  border-radius: 10px;
  overflow: hidden;
}

.upload-component {
  margin: 0 10px;
  flex: 1;
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

.el-button + .el-button {
  margin-left: 0;
}

@media (min-width: 1024px) {
}

@media (max-width: 1024px) {
}
</style>
