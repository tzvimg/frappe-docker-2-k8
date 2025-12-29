<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useInquiryStore, useReferenceStore } from '@/stores'
import { LoadingSpinner, EmptyState } from '@/components/common'
import { InquiryTable } from '@/components/inquiry'

const router = useRouter()
const inquiryStore = useInquiryStore()
const referenceStore = useReferenceStore()

// Filter state
const statusFilter = ref<string>('')
const dateFrom = ref<string>('')
const dateTo = ref<string>('')

onMounted(async () => {
  await referenceStore.initialize()
  await inquiryStore.fetchInquiries()
})

// Watch for filter changes and refetch
async function applyFilters() {
  inquiryStore.resetList()
  await inquiryStore.fetchInquiries({
    status: statusFilter.value || undefined,
    date_from: dateFrom.value || undefined,
    date_to: dateTo.value || undefined,
  })
}

function clearFilters() {
  statusFilter.value = ''
  dateFrom.value = ''
  dateTo.value = ''
  applyFilters()
}

function navigateToInquiry(name: string) {
  router.push({ name: 'InquiryDetail', params: { name } })
}

function goToPage(page: number) {
  inquiryStore.goToPage(page)
}

// Computed pagination info
const paginationPages = (): number[] => {
  const current = inquiryStore.pagination.page
  const total = inquiryStore.pagination.totalPages
  const pages: number[] = []

  // Show max 5 pages around current
  let start = Math.max(1, current - 2)
  let end = Math.min(total, current + 2)

  // Adjust if near start or end
  if (current <= 2) {
    end = Math.min(5, total)
  } else if (current >= total - 1) {
    start = Math.max(1, total - 4)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
}
</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">הפניות שלי</h1>
        <p class="text-gray-600 mt-1">
          {{ inquiryStore.pagination.total }} פניות בסה"כ
        </p>
      </div>
      <router-link
        to="/inquiries/new"
        class="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        פנייה חדשה
      </router-link>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg border border-gray-200 p-4 mb-6">
      <div class="flex flex-wrap items-end gap-4">
        <!-- Status Filter -->
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-medium text-gray-700 mb-1">סטטוס</label>
          <select
            v-model="statusFilter"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
          >
            <option value="">הכל</option>
            <option v-for="status in referenceStore.inquiryStatuses" :key="status.value" :value="status.value">
              {{ status.label }}
            </option>
          </select>
        </div>

        <!-- Date From -->
        <div class="flex-1 min-w-[150px]">
          <label class="block text-sm font-medium text-gray-700 mb-1">מתאריך</label>
          <input
            type="date"
            v-model="dateFrom"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
          />
        </div>

        <!-- Date To -->
        <div class="flex-1 min-w-[150px]">
          <label class="block text-sm font-medium text-gray-700 mb-1">עד תאריך</label>
          <input
            type="date"
            v-model="dateTo"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
          />
        </div>

        <!-- Filter Actions -->
        <div class="flex gap-2">
          <button
            @click="applyFilters"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm font-medium"
          >
            סנן
          </button>
          <button
            @click="clearFilters"
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 text-sm font-medium"
          >
            נקה
          </button>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="bg-white rounded-lg border border-gray-200">
      <!-- Loading State -->
      <div v-if="inquiryStore.listLoading" class="p-12">
        <LoadingSpinner message="טוען פניות..." />
      </div>

      <!-- Error State -->
      <div v-else-if="inquiryStore.listError" class="p-12 text-center">
        <p class="text-red-600 mb-4">{{ inquiryStore.listError }}</p>
        <button
          @click="applyFilters"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm font-medium"
        >
          נסה שוב
        </button>
      </div>

      <!-- Empty State -->
      <EmptyState
        v-else-if="!inquiryStore.hasInquiries"
        title="לא נמצאו פניות"
        :description="statusFilter || dateFrom || dateTo ? 'נסה לשנות את הסינון' : 'התחל ביצירת הפנייה הראשונה שלך'"
        icon="📋"
        @action="router.push('/inquiries/new')"
      >
        צור פנייה חדשה
      </EmptyState>

      <!-- Table -->
      <template v-else>
        <InquiryTable
          :inquiries="inquiryStore.inquiries"
          @select="navigateToInquiry"
        />

        <!-- Pagination -->
        <div
          v-if="inquiryStore.pagination.totalPages > 1"
          class="px-6 py-4 border-t border-gray-200 flex items-center justify-between"
        >
          <div class="text-sm text-gray-500">
            עמוד {{ inquiryStore.pagination.page }} מתוך {{ inquiryStore.pagination.totalPages }}
          </div>
          <div class="flex gap-1">
            <!-- Previous -->
            <button
              @click="goToPage(inquiryStore.pagination.page - 1)"
              :disabled="inquiryStore.pagination.page === 1"
              class="px-3 py-1 rounded border text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              הקודם
            </button>

            <!-- Page Numbers -->
            <button
              v-for="page in paginationPages()"
              :key="page"
              @click="goToPage(page)"
              class="px-3 py-1 rounded border text-sm"
              :class="page === inquiryStore.pagination.page
                ? 'bg-blue-600 text-white border-blue-600'
                : 'hover:bg-gray-50'"
            >
              {{ page }}
            </button>

            <!-- Next -->
            <button
              @click="goToPage(inquiryStore.pagination.page + 1)"
              :disabled="inquiryStore.pagination.page === inquiryStore.pagination.totalPages"
              class="px-3 py-1 rounded border text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              הבא
            </button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
