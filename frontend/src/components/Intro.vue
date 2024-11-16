<script setup lang="ts">
import ChoiceItem from './ChoiceItem.vue'
import EncryptionIcon from './icons/IconEncryption.vue'
import DecryptionIcon from './icons/IconDecryption.vue'
import ToolingIcon from './icons/IconTooling.vue'
import CommunityIcon from './icons/IconCommunity.vue'
</script>

<template>
  <ChoiceItem>
    <template #icon><EncryptionIcon /></template>
    <template #heading>Encryption</template>

    😆Just upload your file and get the encoded image as your key.
    <br />
    😍😍You can also upload a picture you like as your key to the file.
  </ChoiceItem>

  <ChoiceItem>
    <template #icon><DecryptionIcon /></template>
    <template #heading>Decryption</template>

    😉You can get your file by uploading your key image.
  </ChoiceItem>

  <ChoiceItem>
    <template #icon><ToolingIcon /></template>
    <template #heading>Tools</template>

    🧐Check file hash value. Even compare two files at the same time
    <br />

    ...More tools are coming soon.
  </ChoiceItem>

  <ChoiceItem>
    <template #icon><CommunityIcon /></template>
    <template #heading>Contact</template>

    🤔Got stuck? Ask question on
    <el-text class="mx-1" type="success">https://github.com/Guest-Liang</el-text>.
  </ChoiceItem>
</template>
