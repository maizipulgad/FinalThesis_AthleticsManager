<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

authStore.clear()

router.push('/')
</script>

<template>
  <h1>Logged out</h1>
</template>

<style scoped></style>
