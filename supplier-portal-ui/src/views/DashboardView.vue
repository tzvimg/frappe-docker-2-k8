<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores'

const router = useRouter()
const authStore = useAuthStore()

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="p-8">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">
          שלום, {{ authStore.supplierName || authStore.userName }}
        </h1>
        <p class="text-gray-600 mt-1">ברוכים הבאים לפורטל הספקים</p>
      </div>
      <button
        @click="handleLogout"
        class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        התנתקות
      </button>
    </div>

    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">פרטי המשתמש</h2>
      <dl class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <dt class="text-sm font-medium text-gray-500">שם מלא</dt>
          <dd class="mt-1 text-sm text-gray-900">{{ authStore.user?.full_name || '-' }}</dd>
        </div>
        <div>
          <dt class="text-sm font-medium text-gray-500">דוא"ל</dt>
          <dd class="mt-1 text-sm text-gray-900">{{ authStore.user?.email || '-' }}</dd>
        </div>
        <div v-if="authStore.supplier">
          <dt class="text-sm font-medium text-gray-500">שם ספק</dt>
          <dd class="mt-1 text-sm text-gray-900">{{ authStore.supplier.supplier_name }}</dd>
        </div>
        <div v-if="authStore.supplier">
          <dt class="text-sm font-medium text-gray-500">מזהה ספק</dt>
          <dd class="mt-1 text-sm text-gray-900">{{ authStore.supplier.supplier_id }}</dd>
        </div>
      </dl>
    </div>

    <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <p class="text-sm text-blue-700">
        סטטיסטיקות פניות ותכונות נוספות יושלמו בשלב 3
      </p>
    </div>
  </div>
</template>
