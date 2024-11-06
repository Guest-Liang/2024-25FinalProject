<template>
  <div class="encryption">
    <h1>This is EncryptionView page</h1>
    <div class="upload-container">
      <el-upload
        action=""
        class="upload-demo"
        drag
        multiple
        :on-change="handleEncryptFileChange"
        :file-list="encryptFileList"
        :before-upload="beforeUpload"
        :show-file-list="true"
        :auto-upload="false"
        accept="*"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">{{ (encryptFileName === null) ? 'Choose files that needs to be encrypted' : 'List of chosen files'}}</div>
        <div v-if="encryptFileName === null" class="el-upload__tip">Support all file type</div>
      </el-upload>

      <el-upload
        action=""
        class="upload-demo"
        drag
        multiple
        :on-change="handleCustomImageChange"
        :file-list="customImageList"
        :before-upload="beforeUpload"
        :show-file-list="true"
        :auto-upload="false"
        :limit="1"
        accept="image/png"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">{{ customImageName || 'Select a custom image' }}</div>
        <div class="el-upload__tip">{{ (customImageName === null) ? 'Only PNG images are supported' : 'Already selected 1 image!'}}</div>
      </el-upload>
    </div>

    <el-button type="primary" round @click="uploadFiles">Upload to Server</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, toRaw } from 'vue'

const encryptFileList = ref<File[]>([])
const customImageList = ref<File[]>([])
const encryptFileName = ref<string | null>(null)
const customImageName = ref<string | null>(null)
const message = ref('')

const handleCustomImageChange = (fileList: { raw: File }) => {
  customImageList.value.push(fileList.raw)
  customImageName.value = fileList.raw.name
}

const handleEncryptFileChange = (fileList: { raw: File }) => {
  encryptFileList.value.push(fileList.raw) 
  encryptFileName.value = fileList.raw.name
}



const beforeUpload = (file: File) => {
  const isValidSize = file.size / 1024 / 1024 < 10 // Limit to 10MB
  if (!isValidSize) {
    alert('Custom image size cannot exceed 10MB')
  }
  return isValidSize
}


const uploadFiles = async () => {
  let RawEncryptFileList = toRaw(encryptFileList.value)
  let RawCustomImageList = toRaw(customImageList.value)
  if (encryptFileList.value.length === 0) {
    message.value = 'Please choose at least one file to encrypt!'
    alert('Please choose at least one file to encrypt!')
    return
  }

  const formData = new FormData()
  RawEncryptFileList.forEach(file => {
    formData.append('file', file)
  })

  if (customImageList.value.length > 0) {
    formData.append('isUseCustomImg', RawCustomImageList[0])
  }

  try {
    const response = await fetch('http://localhost:8000/api/encrypt/', {
      method: 'POST',
      body: formData,
    })

    if (response.ok) {
      const data = await response.json()
      console.log(data)
    } else {
      message.value = 'File upload failed!'
      console.error('Upload failed:', response)
    }
  } catch (error) {
    console.error('Upload error:', error)
    message.value = 'Error uploading file!'
  }
}
</script>

<style>
.encryption {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.upload-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 800px;
}

.upload-demo {
  margin: 0 10px;
  flex: 1;
}

@media (min-width: 1024px) {
  .encryption {
    min-height: 100vh;
    align-items: flex-start;
  }
}

@media (max-width: 1024px) {
  .encryption {
    align-items: center;
  }
}
</style>
