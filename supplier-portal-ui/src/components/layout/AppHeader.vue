<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const showUserMenu = ref(false)

const navItems = [
  { name: 'Dashboard', path: '/', label: 'ראשי' },
  { name: 'InquiryList', path: '/inquiries', label: 'פניות' },
  { name: 'Profile', path: '/profile', label: 'פרופיל' },
]

function isActiveRoute(path: string): boolean {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <header class="bg-white border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo / Title -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-lg">ס</span>
            </div>
            <span class="text-lg font-semibold text-gray-900">פורטל ספקים</span>
          </router-link>
        </div>

        <!-- Navigation -->
        <nav class="hidden md:flex items-center gap-1">
          <router-link
            v-for="item in navItems"
            :key="item.name"
            :to="item.path"
            class="px-4 py-2 rounded-md text-sm font-medium transition-colors"
            :class="isActiveRoute(item.path)
              ? 'bg-blue-50 text-blue-700'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
          >
            {{ item.label }}
          </router-link>
        </nav>

        <!-- User Menu -->
        <div class="relative">
          <button
            @click="showUserMenu = !showUserMenu"
            class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
          >
            <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
              <span class="text-gray-600 text-sm">{{ authStore.userName?.charAt(0) || 'U' }}</span>
            </div>
            <span class="hidden sm:block">{{ authStore.supplierName || authStore.userName }}</span>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <!-- Dropdown Menu -->
          <div
            v-if="showUserMenu"
            class="absolute left-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1"
            @click="showUserMenu = false"
          >
            <div class="px-4 py-2 border-b border-gray-100">
              <p class="text-sm font-medium text-gray-900">{{ authStore.supplierName }}</p>
              <p class="text-xs text-gray-500">{{ authStore.user?.email }}</p>
            </div>
            <router-link
              to="/profile"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
            >
              פרופיל
            </router-link>
            <button
              @click="handleLogout"
              class="block w-full text-right px-4 py-2 text-sm text-red-600 hover:bg-red-50"
            >
              התנתקות
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <nav class="md:hidden border-t border-gray-200 px-4 py-2 flex gap-1 overflow-x-auto">
      <router-link
        v-for="item in navItems"
        :key="item.name"
        :to="item.path"
        class="px-3 py-1.5 rounded-md text-sm font-medium whitespace-nowrap transition-colors"
        :class="isActiveRoute(item.path)
          ? 'bg-blue-50 text-blue-700'
          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
      >
        {{ item.label }}
      </router-link>
    </nav>
  </header>

  <!-- Click outside to close menu -->
  <div
    v-if="showUserMenu"
    class="fixed inset-0 z-40"
    @click="showUserMenu = false"
  />
</template>
