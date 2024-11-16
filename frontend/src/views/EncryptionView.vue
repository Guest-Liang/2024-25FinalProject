<template>
  <div class="encryption">
    <div class="upload-container">
      <el-upload
        action=""
        class="upload-component"
        :drag="true"
        multiple
        :on-change="handleEncryptFileChange"
        :file-list="encryptFileList"
        :before-upload="beforeUpload"
        :show-file-list="true"
        :auto-upload="false"
        accept="*"
        :on-remove="handleEncryptFileRemove"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          {{
            encryptFileName === null
              ? 'Choose files that needs to be encrypted'
              : 'List of chosen files'
          }}
        </div>
        <div class="el-upload__tip">
          {{ encryptFileName === null ? 'Support all file type' : 'Files are ready' }}
        </div>
      </el-upload>

      <el-upload
        action=""
        class="upload-component"
        :drag="true"
        multiple
        :on-change="handleCustomImageChange"
        :file-list="customImageList"
        :before-upload="beforeUpload"
        :show-file-list="true"
        :auto-upload="false"
        :limit="1"
        accept="image/png"
        :on-remove="handleCustomFileRemove"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">{{ customImageName || 'Select a custom image' }}</div>
        <div class="el-upload__tip">
          {{
            customImageName === null ? 'Only PNG images are supported' : 'Already selected 1 image!'
          }}
        </div>
      </el-upload>
    </div>

    <div class="button-group">
      <el-button type="primary" round @click="uploadFiles">Upload to Server</el-button>
      <el-button type="danger" round @click="cleanUploadFiles" style="margin-left: 10px"
        >Clean up all files</el-button
      >
      <el-divider direction="vertical" />
      <span>Get results throught email? </span>
      <el-switch
        v-model="isSendingEmail"
        class="ml-2"
        inline-prompt
        size="large"
        style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
        active-text="Y"
        inactive-text="N"
      />
      <el-input
        v-if="isSendingEmail"
        v-model="inputEmail"
        style="width: 240px; margin-left: 10px"
        clearable
        placeholder="Please input Email Address"
      />
    </div>

    <div v-if="downloadLinks.length > 0" class="DownloadLink">
      <h2>Download Links</h2>
      <ul>
        <li v-for="(link, index) in downloadLinks" :key="index">
          <a :href="link.url" download>{{ link.name }}</a> —— {{ link.originalName }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, toRaw } from 'vue'
import { ElLoading, ElMessage, ElMessageBox } from 'element-plus'
import type { EncryptResult, DownloadLink } from '@/types/interface'
import { BACKEND_API } from '@/types/config'

const isSendingEmail = ref(false)
const inputEmail = ref('')

const downloadLinks = ref<DownloadLink[]>([])

const encryptFileList = ref<File[]>([])
const customImageList = ref<File[]>([])
const encryptFileName = ref<string | null>(null)
const customImageName = ref<string | null>(null)

const isValidEmail = (email: string) => {
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  return emailPattern.test(email)
}

const handleEncryptFileRemove = (file: File) => {
  const index = encryptFileList.value.indexOf(file)
  if (index > -1) {
    encryptFileList.value.splice(index, 1)
  }
  console.log(`Removed file: ${file.name}`)
}

const handleCustomFileRemove = (file: File) => {
  const index = customImageList.value.indexOf(file)
  if (index > -1) {
    customImageList.value.splice(index, 1)
  }
  console.log(`Removed custom image: ${file.name}`)
}

const cleanUploadFiles = () => {
  encryptFileList.value = []
  customImageList.value = []
  encryptFileName.value = null
  customImageName.value = null
  downloadLinks.value = []
}

const handleCustomImageChange = (fileList: { raw: File }) => {
  customImageList.value.push(fileList.raw)
  customImageName.value = fileList.raw.name
}

const handleEncryptFileChange = (fileList: { raw: File }) => {
  encryptFileList.value.push(fileList.raw)
  encryptFileName.value = fileList.raw.name
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
  if (encryptFileList.value.length === 0) {
    ElMessage({
      showClose: true,
      message: 'Please choose at least one file to encrypt!',
      type: 'warning',
      duration: 5000,
    })
    return
  }

  if (isSendingEmail.value && !isValidEmail(inputEmail.value)) {
    ElMessage({
      showClose: true,
      message: 'Please input a valid email address!',
      type: 'error',
      duration: 5000,
    })
    return
  }

  const loading = ElLoading.service({
    target: '.upload-container',
    lock: true,
    text: 'Fetching Data',
    background: 'rgba(0, 0, 0, 0.6)',
  })

  let RawEncryptFileList = toRaw(encryptFileList.value)
  let RawCustomImageList = toRaw(customImageList.value)

  const formData = new FormData()
  RawEncryptFileList.forEach((file) => {
    formData.append('file', file)
  })

  if (customImageList.value.length > 0) {
    formData.append('isUseCustomImg', RawCustomImageList[0])
  }

  if (isSendingEmail.value) {
    formData.append('EmailAddress', inputEmail.value)
  }

  try {
    loading.setText('Waiting for processing...')
    const response = await fetch(`http://${BACKEND_API}/api/encrypt/`, {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()

    if (response.ok) {
      downloadLinks.value = data.results.map((item: EncryptResult, index: number) => {
        const fileName = item.EncodedImagePath.split(/[/\\]/).pop()
        const originalFile = encryptFileList.value[index]
        return {
          name: fileName,
          url: `http://${BACKEND_API}/api/download/${fileName}`,
          originalName: originalFile.name,
        }
      })
      ElMessageBox.alert(data.message, 'Success', {
        confirmButtonText: 'OK',
        type: 'success',
      })
    } else {
      ElMessageBox.alert(data.error, 'Error', {
        confirmButtonText: 'OK',
        type: 'error',
      })
      console.error('Upload failed:', data.error)
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
.encryption {
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
  transition: height 0.2s;
  margin: 0 10px;
  flex: 1;
  width: 30%;
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

.encryption .el-button {
  margin-top: 0.25rem;
  font-size: 1rem;
  padding: 20px 20px;
}

@media (min-width: 1024px) {
}

@media (max-width: 1024px) {
}
</style>
