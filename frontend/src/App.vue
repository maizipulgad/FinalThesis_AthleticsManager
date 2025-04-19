<template>
  <div id="app">
    <div v-if="authStore.isAuthenticated">
      <HeaderComponent />
      <div class="main-layout">
        <SidebarComponent />
        <router-view />
      </div>
    </div>
    <div v-else>
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import HeaderComponent from '@/components/HeaderComponent.vue'
import SidebarComponent from '@/components/SidebarComponent.vue'

const authStore = useAuthStore()
</script>

<style scoped>
.main-layout {
  display: flex;
}

.main-layout > *:last-child {
  flex-grow: 2;
  width: 100%;
  padding: 10px;
}
</style>