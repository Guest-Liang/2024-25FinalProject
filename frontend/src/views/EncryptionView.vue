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
              ? t('EncryptView.FileUploadText_nofile')
              : t('EncryptView.FileUploadText_hasfile')
          }}
        </div>
        <div class="el-upload__tip">
          {{ encryptFileName === null ? t('EncryptView.FileUploadTips_nofile') : t('EncryptView.FileUploadTips_hasfile') }}
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
        <div class="el-upload__text">{{ customImageName || t('EncryptView.CustomImageUploadText_nofile') }}</div>
        <div class="el-upload__tip">
          {{
            customImageName === null
              ? t('EncryptView.CustomImageUploadTips_nofile')
              : t('EncryptView.CustomImageUploadTips_hasfile')
          }}
        </div>
      </el-upload>
    </div>

    <div class="button-group">
      <el-button
        type="primary"
        round
        @click="uploadFiles"
      >
        {{ t('EncryptView.UploadFileButton') }}
      </el-button>
      <el-button
        type="danger"
        round
        @click="cleanUploadFiles"
        style="margin-left: 10px"
      >
        {{ t('EncryptView.CleanFileButton') }}
      </el-button>
      <el-divider direction="vertical" />
      <span>{{ t('EncryptView.GetbyEmail') }}</span>
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
        :placeholder="t('EncryptView.EmailPlaceholder')"
      />
    </div>

    <div v-if="downloadLinks.length > 0" class="DownloadLink">
      <h2>{{ t('EncryptView.DownloadLinks') }}</h2>
      <ul>
        <li v-for="(link, index) in downloadLinks" :key="index">
          <a :href="link.url" download>{{ link.name }}</a> —— {{ link.originalName }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, toRaw, watch } from 'vue'
import { ElLoading, ElMessage, ElMessageBox } from 'element-plus'
import type { EncryptResult, DownloadLink } from '@/types/interface'
import { BACKEND_API } from '@/types/config'

import { useTranslation } from 'i18next-vue'
const { t, i18next } = useTranslation()

let loading = null

watch(
  () => i18next.language,
  () => {
    if (loading) {
      loading.setText(t('DecryptView.LoadingText'))
    }
  }
)

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
      message: t('EncryptView.ExceedMaxSizeMsg'),
      type: 'error',
      duration: 5000,
    })
  }
  if (!isPNG) {
    ElMessage({
      showClose: true,
      message: t('EncryptView.NonePNGImageMsg'),
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
      message: t('EncryptView.NoFileUploadMsg'),
      type: 'warning',
      duration: 5000,
    })
    return
  }

  if (isSendingEmail.value && !isValidEmail(inputEmail.value)) {
    ElMessage({
      showClose: true,
      message: t('EncryptView.InvalidEmailMsg'),
      type: 'error',
      duration: 5000,
    })
    return
  }

  loading = ElLoading.service({
    target: '.upload-container',
    lock: true,
    text: t('EncryptView.LoadingText'),
    background: 'rgba(0, 0, 0, 0.6)',
  })

  const RawEncryptFileList = toRaw(encryptFileList.value)
  const RawCustomImageList = toRaw(customImageList.value)

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
    loading.setText(t('EncryptView.WaitingText'))
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
      ElMessageBox.alert(data.message, t('EncryptView.SuccessTitle'), {
        confirmButtonText: t('EncryptView.OKText'),
        type: 'success',
      })
    } else {
      ElMessageBox.alert(data.error, t('EncryptView.ErrorTitle'), {
        confirmButtonText: t('EncryptView.OKText'),
        type: 'error',
      })
      console.error('Upload failed:', data.error)
    }
  } catch (error) {
    console.error('Upload error:', error)
    ElMessageBox.alert(t('EncryptView.ErrorText'), t('EncryptView.ErrorTitle'), {
      confirmButtonText: t('EncryptView.OKText'),
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
