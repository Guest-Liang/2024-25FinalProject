<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import ChoiceItem from './ChoiceItem.vue'
import EncryptionIcon from './icons/IconEncryption.vue'
import DecryptionIcon from './icons/IconDecryption.vue'
import ToolingIcon from './icons/IconTooling.vue'
import CommunityIcon from './icons/IconCommunity.vue'

import { useTranslation } from 'i18next-vue'
const { t, i18next } = useTranslation()
</script>

<template>
  <ChoiceItem>
    <template #icon><EncryptionIcon /></template>
    <template #heading>{{ t('Intro.Heading1') }}</template>
    {{ t('Intro.Paragraph1_1') }}
    <br />
    {{ t('Intro.Paragraph1_2') }}
  </ChoiceItem>

  <ChoiceItem>
    <template #icon><DecryptionIcon /></template>
    <template #heading>{{ t('Intro.Heading2') }}</template>
    {{ t('Intro.Paragraph2') }}
  </ChoiceItem>

  <ChoiceItem>
    <template #icon><ToolingIcon /></template>
    <template #heading>{{ t('Intro.Heading3') }}</template>
    {{ t('Intro.Paragraph3_1') }}
    <br />
    {{ t('Intro.Paragraph3_2') }}
  </ChoiceItem>

  <ChoiceItem>
    <template #icon><CommunityIcon /></template>
    <template #heading>{{ t('Intro.Heading4') }}</template>
    {{ t('Intro.Paragraph4') }}
    <el-text class="mx-1" type="success">https://github.com/Guest-Liang</el-text>.
  </ChoiceItem>
</template>
