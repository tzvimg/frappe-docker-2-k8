<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// Form state (local)
const email = ref('')
const password = ref('')

// Computed from store
const loading = computed(() => authStore.loading)
const error = computed(() => authStore.error)

async function handleLogin() {
  authStore.clearError()

  const success = await authStore.login(email.value, password.value)

  if (success) {
    // Redirect to original destination or dashboard
    const redirect = route.query.redirect as string
    router.push(redirect || '/')
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
              autocomplete="email"
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
              autocomplete="current-password"
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
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">מתחבר...</span>
            <span v-else>התחברות</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
