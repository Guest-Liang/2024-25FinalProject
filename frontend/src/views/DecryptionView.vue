<template>
  <div class="decryption">
    <h1>This is DecryptionView page</h1>
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
        <div class="el-upload__text">{{ (customImageList.length === 0) ? 'Select the images you want to decrypt' : 'List of chosen files' }}</div>
        <div v-if="customImageList.length === 0" class="el-upload__tip">Only PNG images are supported</div>
      </el-upload>
    </div>
    <el-button type="primary" round @click="uploadFiles">Upload to Server</el-button>

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
import { ElLoading, ElMessage } from 'element-plus'
import type { DecryptResult, DownloadLink} from '@/types/interface';
import { BACKEND_API } from '@/types/config';

const downloadLinks = ref<DownloadLink[]>([]);
const customImageList = ref<File[]>([])

const handleImageChange = (fileList: { raw: File }) => {
  customImageList.value.push(fileList.raw)
}

const handleImageRemove = (file: File) => {
  const index = customImageList.value.findIndex(item => item.name === file.name)
  if (index !== -1) {
    customImageList.value.splice(index, 1)
  }
}


const beforeUpload = (file: File) => {
  const isPNG = file.type === 'image/png';
  const isValidSize = file.size / 1024 / 1024 < 10 && file.size / 1024 > 200 // Limit to 200KB-10MB
  if (!isValidSize) {
    ElMessage.error('Custom image size cannot exceed 10MB')
  }
  if (!isPNG) {
    ElMessage.error('Only PNG images are supported')
  }
  return isValidSize && isPNG;
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
    ElMessage.warning('Please choose at least one file to decrypt!')
    loading.close()
    return
  }

  const formData = new FormData()
  RawCustomImageList.forEach(file => {
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
          url: `http://${BACKEND_API}/api/download/${fileName}`
        }
      })
      ElMessage.success('Files uploaded successfully!')
    } else {
      ElMessage.error('File upload failed!')
      console.error('Upload failed:', response)
    }
  } catch (error) {
    console.error('Upload error:', error)
    ElMessage.error('Error uploading file!')
  } finally {
    loading.close()
  }
}
</script>

<style scoped>
.decryption {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.upload-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 800px;
  border-radius: 10px;
  overflow: hidden;
}

.upload-component {
  margin: 0 10px;
  flex: 1;
}

@media (min-width: 1024px) {
  .decryption {
    min-height: 100vh;
  }
}

@media (max-width: 1024px) {

}
</style>
