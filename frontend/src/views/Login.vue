<script setup lang="ts">
import AccountService from '@/services/AccountService'
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

let loginName = ref('')
let loginPassword = ref('')
let loginIsOngoing = ref(false)
let errors = ref<string[]>([])

const doLogin = async () => {
  loginIsOngoing.value = true
  try {
    const res = await AccountService.loginAsync(loginName.value, loginPassword.value)

    if (res.data) {
      authStore.setTokens(res.data.access, res.data.refresh, res.data.roles);
      errors.value = []
      await router.push('/home')
    } else {
      errors.value = res.errors!
    }
  } catch (err) {
    errors.value = ['An error occurred. Please try again.']
  }

    loginIsOngoing.value = false
}
</script>
<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="text-center mb-4">Log in</h1>
      <form id="account" method="post">
        <div v-if="errors.length" class="alert alert-danger">
          {{ errors.join(',') }}
        </div>

        <div class="form-floating mb-3">
          <input
            v-model="loginName"
            class="form-control"
            autocomplete="username"
            aria-required="true"
            placeholder="name@example.com"
            type="email"
            id="Input_Email"
            name="Input.Email"
          />
          <label for="Input_Email">Email</label>
        </div>

        <div class="form-floating mb-3">
          <input
            v-model="loginPassword"
            class="form-control"
            autocomplete="current-password"
            aria-required="true"
            placeholder="password"
            type="password"
            id="Input_Password"
            name="Input.Password"
          />
          <label for="Input_Password">Password</label>
        </div>

        <button
          @click.prevent="doLogin"
          id="login-submit"
          type="submit"
          class="w-100 btn btn-primary btn-lg"
        >
          {{ loginIsOngoing ? 'Wait...' : 'Do login' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh; /* Full screen height */
  background-color: #f8f9fa;
  padding: 20px;
  box-sizing: border-box;
  margin: 0;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>