<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { login as apiLogin, getCurrentUser } from '@/api/auth'

const router = useRouter()
const route = useRoute()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''

  try {
    await apiLogin(email.value, password.value)

    // Verify login was successful by getting current user
    const currentUser = await getCurrentUser()
    if (currentUser.user) {
      localStorage.setItem('user_authenticated', 'true')

      // Redirect to original destination or dashboard
      const redirect = route.query.redirect as string
      router.push(redirect || '/')
    }
  } catch (e: unknown) {
    error.value = 'שם משתמש או סיסמה שגויים'
    console.error('Login error:', e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">
          פורטל ספקים
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          התחברות לחשבון
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email" class="sr-only">כתובת דוא"ל</label>
            <input
              id="email"
              v-model="email"
              name="email"
              type="email"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="כתובת דוא״ל"
            />
          </div>
          <div>
            <label for="password" class="sr-only">סיסמה</label>
            <input
              id="password"
              v-model="password"
              name="password"
              type="password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="סיסמה"
            />
          </div>
        </div>

        <div v-if="error" class="rounded-md bg-red-50 p-4">
          <div class="flex">
            <div class="text-sm text-red-700">
              {{ error }}
            </div>
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            <span v-if="loading">מתחבר...</span>
            <span v-else>התחברות</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
