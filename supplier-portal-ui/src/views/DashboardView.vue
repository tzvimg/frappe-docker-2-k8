<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore, useInquiryStore, useReferenceStore } from '@/stores'
import { StatCard, LoadingSpinner, EmptyState, StatusBadge } from '@/components/common'

const router = useRouter()
const authStore = useAuthStore()
const inquiryStore = useInquiryStore()
const referenceStore = useReferenceStore()

onMounted(async () => {
  // Initialize reference data and fetch stats/inquiries in parallel
  await Promise.all([
    referenceStore.initialize(),
    inquiryStore.fetchStats(),
    inquiryStore.fetchInquiries({ page_size: 5 }),
  ])
})

function formatDate(dateStr?: string): string {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('he-IL', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function navigateToInquiry(name: string) {
  router.push({ name: 'InquiryDetail', params: { name } })
}
</script>

<template>
  <div>
    <!-- Welcome Section -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">
        שלום, {{ authStore.supplierName || authStore.userName }}
      </h1>
      <p class="text-gray-600 mt-1">ברוכים הבאים לפורטל הספקים</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <StatCard
        title="סה״כ פניות"
        :value="inquiryStore.stats?.total || 0"
        color="blue"
        :loading="inquiryStore.statsLoading"
      />
      <StatCard
        title="פניות פתוחות"
        :value="inquiryStore.stats?.open || 0"
        color="orange"
        :loading="inquiryStore.statsLoading"
      />
      <StatCard
        title="פניות סגורות"
        :value="inquiryStore.stats?.closed || 0"
        color="green"
        :loading="inquiryStore.statsLoading"
      />
    </div>

    <!-- Quick Actions -->
    <div class="bg-white rounded-lg border border-gray-200 p-6 mb-8">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">פעולות מהירות</h2>
      <div class="flex flex-wrap gap-3">
        <router-link
          to="/inquiries/new"
          class="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          פנייה חדשה
        </router-link>
        <router-link
          to="/inquiries"
          class="inline-flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          כל הפניות
        </router-link>
        <router-link
          to="/profile"
          class="inline-flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          פרופיל
        </router-link>
      </div>
    </div>

    <!-- Recent Inquiries -->
    <div class="bg-white rounded-lg border border-gray-200">
      <div class="p-6 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">פניות אחרונות</h2>
          <router-link
            to="/inquiries"
            class="text-sm text-blue-600 hover:text-blue-700 font-medium"
          >
            צפה בכולן
          </router-link>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="inquiryStore.listLoading" class="p-12">
        <LoadingSpinner message="טוען פניות..." />
      </div>

      <!-- Empty State -->
      <EmptyState
        v-else-if="!inquiryStore.hasInquiries"
        title="אין פניות עדיין"
        description="התחל ביצירת הפנייה הראשונה שלך"
        icon="📋"
        @action="router.push('/inquiries/new')"
      >
        צור פנייה חדשה
      </EmptyState>

      <!-- Inquiries Table -->
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                מספר פנייה
              </th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                נושא
              </th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                סטטוס
              </th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                תאריך יצירה
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="inquiry in inquiryStore.recentInquiries"
              :key="inquiry.name"
              class="hover:bg-gray-50 cursor-pointer transition-colors"
              @click="navigateToInquiry(inquiry.name)"
            >
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
                {{ inquiry.name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ inquiry.topic_category }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <StatusBadge :status="inquiry.inquiry_status || 'פנייה חדשה התקבלה'" />
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(inquiry.creation) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
