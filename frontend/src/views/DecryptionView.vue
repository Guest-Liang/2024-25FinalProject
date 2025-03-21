<template>
  <div class="decryption">
    <div class="upload-container">
      <el-upload
        action=""
        :key="Keys.FileUpload"
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
              ? $t('DecryptView.UploadText_nofile')
              : $t('DecryptView.UploadText_hasfile')
          }}
        </div>
        <div v-if="customImageList.length === 0" class="el-upload__tip">
          {{ $t('DecryptView.UploadTips') }}
        </div>
      </el-upload>
      <div
        class="button-container"
        style="display: flex; flex-direction: column; height: 100px; width: 150px"
      >
        <el-button
          type="primary"
          :key="Keys.UploadButton"
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
          {{ $t('DecryptView.UploadFileButton') }}
        </el-button>
        <el-button
          type="danger"
          :key="Keys.CleanButton"
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
          {{ $t('DecryptView.CleanFileButton') }}
        </el-button>
      </div>
    </div>

    <div v-if="downloadLinks.length > 0" class="DownloadLink">
      <h2>{{ $t('DecryptView.DownloadLinks') }}</h2>
      <ul>
        <li v-for="(link, index) in downloadLinks" :key="index">
          <a :href="link.url" download>{{ link.name }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, toRaw, watch, reactive } from 'vue'
import { ElLoading, ElMessage, ElMessageBox } from 'element-plus'
import type { DecryptResult, DownloadLink } from '@/types/interface'
import { BACKEND_API } from '@/types/config'

import i18next from 'i18next'

let loading = null

const Keys = reactive({
  FileUpload: 0,
  UploadButton: 0,
  CleanButton: 0,
  ExceedMaxSizeMsg: i18next.t('DecryptView.ExceedMaxSizeMsg'),
  NonePNGImageMsg: i18next.t('DecryptView.NonePNGImageMsg'),
  LoadingText: i18next.t('DecryptView.LoadingText'),
  NoFileUploadMsg: i18next.t('DecryptView.NoFileUploadMsg'),
  WaitingText: i18next.t('DecryptView.WaitingText'),
  SuccessTitle: i18next.t('DecryptView.SuccessTitle'),
  OKText: i18next.t('DecryptView.OKText'),
  ErrorText: i18next.t('DecryptView.ErrorText'),
  ErrorTitle: i18next.t('DecryptView.ErrorTitle'),
})

watch(() => i18next.language, () => {
  Object.keys(Keys).forEach((key) => {
    Keys[key]++
  })
  Keys.ExceedMaxSizeMsg = i18next.t('DecryptView.ExceedMaxSizeMsg')
  Keys.NonePNGImageMsg = i18next.t('DecryptView.NonePNGImageMsg')
  Keys.LoadingText = i18next.t('DecryptView.LoadingText')
  if (loading) {
    loading.setText(i18next.t('DecryptView.LoadingText'))
  }
  Keys.NoFileUploadMsg = i18next.t('DecryptView.NoFileUploadMsg')
  Keys.WaitingText = i18next.t('DecryptView.WaitingText')
  Keys.SuccessTitle = i18next.t('DecryptView.SuccessTitle')
  Keys.OKText = i18next.t('DecryptView.OKText')
  Keys.ErrorText = i18next.t('DecryptView.ErrorText')
  Keys.ErrorTitle = i18next.t('DecryptView.ErrorTitle')
})

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
      message: Keys.ExceedMaxSizeMsg,
      type: 'error',
      duration: 5000,
    })
  }
  if (!isPNG) {
    ElMessage({
      showClose: true,
      message: Keys.NonePNGImageMsg,
      type: 'error',
      duration: 5000,
    })
  }
  return isValidSize && isPNG
}

const uploadFiles = async () => {
  loading = ElLoading.service({
    target: '.upload-container',
    lock: true,
    text: Keys.LoadingText,
    background: 'rgba(0, 0, 0, 0.6)',
  })

  const RawCustomImageList = toRaw(customImageList.value)
  if (customImageList.value.length === 0) {
    ElMessage({
      showClose: true,
      message: Keys.NoFileUploadMsg,
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
    loading.setText(Keys.WaitingText)
    const response = await fetch(`http://${BACKEND_API}/api/decrypt/`, {
      method: 'POST',
      body: formData,
    })

    if (response.ok) {
      const data = await response.json()
      downloadLinks.value = data.results.map((item: DecryptResult) => {
        const fileName = item.DecryptedFilePath.split(/[/\\]/).pop()
        return {
          name: fileName,
          url: `http://${BACKEND_API}/api/download/${fileName}`,
        }
      })
      ElMessageBox.alert(data.message, Keys.SuccessTitle, {
        confirmButtonText: Keys.OKText,
        type: 'success',
      })
    } else {
      ElMessageBox.alert(Keys.ErrorText, Keys.ErrorTitle, {
        confirmButtonText: Keys.OKText,
        type: 'error',
      })
      console.error('Upload failed:', response)
    }
  } catch (error) {
    console.error('Upload error:', error)
    ElMessageBox.alert(Keys.ErrorText, Keys.ErrorTitle, {
      confirmButtonText: Keys.OKText,
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
  transition: border 0.3s ease;
}

:deep(.el-upload-dragger:hover) {
  border: 2px solid #409eff;
  background-color: #e2eaf7;
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
