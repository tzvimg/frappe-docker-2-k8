<script setup lang="ts">
import { onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useInquiryStore, useReferenceStore } from '@/stores'
import { LoadingSpinner, StatusBadge } from '@/components/common'

const props = defineProps<{
  name: string
}>()

const router = useRouter()
const inquiryStore = useInquiryStore()
const referenceStore = useReferenceStore()

const inquiry = computed(() => inquiryStore.currentInquiry)

onMounted(async () => {
  await referenceStore.initialize()
  await inquiryStore.fetchInquiry(props.name)
})

onUnmounted(() => {
  inquiryStore.clearCurrentInquiry()
})

function formatDate(dateStr?: string): string {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('he-IL', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function goBack() {
  router.push({ name: 'InquiryList' })
}

// Check if status is a "closed" status
const isClosed = computed(() => {
  if (!inquiry.value?.inquiry_status) return false
  return referenceStore.closedStatuses.includes(inquiry.value.inquiry_status)
})

// Parse attachments - could be comma-separated URLs or JSON
function parseAttachments(attachments?: string): string[] {
  if (!attachments) return []
  try {
    // Try JSON parsing first
    const parsed = JSON.parse(attachments)
    return Array.isArray(parsed) ? parsed : [parsed]
  } catch {
    // Fall back to comma-separated
    return attachments.split(',').map(s => s.trim()).filter(Boolean)
  }
}

function getFileName(url: string): string {
  const parts = url.split('/')
  const fileName = parts[parts.length - 1]
  return fileName ? decodeURIComponent(fileName) : url
}
</script>

<template>
  <div>
    <!-- Back Button -->
    <button
      @click="goBack"
      class="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
    >
      <svg class="w-5 h-5 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      חזרה לרשימת הפניות
    </button>

    <!-- Loading State -->
    <div v-if="inquiryStore.detailLoading" class="bg-white rounded-lg border border-gray-200 p-12">
      <LoadingSpinner message="טוען פרטי פנייה..." />
    </div>

    <!-- Error State -->
    <div v-else-if="inquiryStore.detailError" class="bg-white rounded-lg border border-gray-200 p-12 text-center">
      <p class="text-red-600 mb-4">{{ inquiryStore.detailError }}</p>
      <button
        @click="inquiryStore.fetchInquiry(props.name)"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm font-medium"
      >
        נסה שוב
      </button>
    </div>

    <!-- Inquiry Details -->
    <template v-else-if="inquiry">
      <!-- Header Card -->
      <div class="bg-white rounded-lg border border-gray-200 p-6 mb-6">
        <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
          <div>
            <div class="flex items-center gap-3 mb-2">
              <h1 class="text-2xl font-bold text-gray-900">פנייה {{ inquiry.name }}</h1>
              <StatusBadge :status="inquiry.inquiry_status || 'פנייה חדשה התקבלה'" />
            </div>
            <p class="text-gray-600">נוצרה ב-{{ formatDate(inquiry.creation) }}</p>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column - Main Details -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Inquiry Info -->
          <div class="bg-white rounded-lg border border-gray-200 p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">פרטי הפנייה</h2>

            <dl class="space-y-4">
              <div>
                <dt class="text-sm font-medium text-gray-500">נושא</dt>
                <dd class="mt-1 text-gray-900">{{ inquiry.topic_category }}</dd>
              </div>

              <div>
                <dt class="text-sm font-medium text-gray-500">הקשר הפנייה</dt>
                <dd class="mt-1 text-gray-900">{{ inquiry.inquiry_context }}</dd>
              </div>

              <!-- Insured Details (if applicable) -->
              <template v-if="inquiry.inquiry_context === 'מבוטח'">
                <div v-if="inquiry.insured_id_number">
                  <dt class="text-sm font-medium text-gray-500">מספר זהות מבוטח</dt>
                  <dd class="mt-1 text-gray-900">{{ inquiry.insured_id_number }}</dd>
                </div>
                <div v-if="inquiry.insured_full_name">
                  <dt class="text-sm font-medium text-gray-500">שם מבוטח</dt>
                  <dd class="mt-1 text-gray-900">{{ inquiry.insured_full_name }}</dd>
                </div>
              </template>

              <div>
                <dt class="text-sm font-medium text-gray-500">תיאור הפנייה</dt>
                <dd
                  class="mt-1 text-gray-900 prose prose-sm max-w-none"
                  v-html="inquiry.inquiry_description"
                />
              </div>
            </dl>
          </div>

          <!-- Attachments -->
          <div
            v-if="parseAttachments(inquiry.attachments).length > 0"
            class="bg-white rounded-lg border border-gray-200 p-6"
          >
            <h2 class="text-lg font-semibold text-gray-900 mb-4">קבצים מצורפים</h2>
            <ul class="space-y-2">
              <li
                v-for="(attachment, index) in parseAttachments(inquiry.attachments)"
                :key="index"
                class="flex items-center gap-2"
              >
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                </svg>
                <a
                  :href="attachment"
                  target="_blank"
                  class="text-blue-600 hover:text-blue-700 hover:underline text-sm"
                >
                  {{ getFileName(attachment) }}
                </a>
              </li>
            </ul>
          </div>

          <!-- Response (if closed) -->
          <div
            v-if="isClosed && inquiry.response_text"
            class="bg-green-50 rounded-lg border border-green-200 p-6"
          >
            <h2 class="text-lg font-semibold text-green-800 mb-4">המענה שהתקבל</h2>
            <div
              class="text-green-900 prose prose-sm max-w-none"
              v-html="inquiry.response_text"
            />

            <!-- Response Attachments -->
            <div
              v-if="parseAttachments(inquiry.response_attachments).length > 0"
              class="mt-4 pt-4 border-t border-green-200"
            >
              <h3 class="text-sm font-medium text-green-700 mb-2">קבצים מצורפים למענה</h3>
              <ul class="space-y-1">
                <li
                  v-for="(attachment, index) in parseAttachments(inquiry.response_attachments)"
                  :key="index"
                  class="flex items-center gap-2"
                >
                  <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                  </svg>
                  <a
                    :href="attachment"
                    target="_blank"
                    class="text-green-700 hover:text-green-800 hover:underline text-sm"
                  >
                    {{ getFileName(attachment) }}
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Right Column - Meta Info -->
        <div class="space-y-6">
          <!-- Status Card -->
          <div class="bg-white rounded-lg border border-gray-200 p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">מידע נוסף</h2>

            <dl class="space-y-3">
              <div>
                <dt class="text-sm font-medium text-gray-500">סטטוס</dt>
                <dd class="mt-1">
                  <StatusBadge :status="inquiry.inquiry_status || 'פנייה חדשה התקבלה'" />
                </dd>
              </div>

              <div v-if="inquiry.assigned_role">
                <dt class="text-sm font-medium text-gray-500">מטפל</dt>
                <dd class="mt-1 text-gray-900">{{ inquiry.assigned_role }}</dd>
              </div>

              <div>
                <dt class="text-sm font-medium text-gray-500">תאריך יצירה</dt>
                <dd class="mt-1 text-gray-900">{{ formatDate(inquiry.creation) }}</dd>
              </div>

              <div v-if="inquiry.modified !== inquiry.creation">
                <dt class="text-sm font-medium text-gray-500">עדכון אחרון</dt>
                <dd class="mt-1 text-gray-900">{{ formatDate(inquiry.modified) }}</dd>
              </div>
            </dl>
          </div>

          <!-- Help Card -->
          <div class="bg-blue-50 rounded-lg border border-blue-200 p-6">
            <h3 class="text-sm font-semibold text-blue-800 mb-2">צריכים עזרה?</h3>
            <p class="text-sm text-blue-700">
              אם יש לכם שאלות נוספות בנוגע לפנייה זו, תוכלו ליצור פנייה חדשה ולציין את מספר הפנייה המקורית.
            </p>
            <router-link
              to="/inquiries/new"
              class="inline-block mt-3 text-sm font-medium text-blue-700 hover:text-blue-800"
            >
              יצירת פנייה חדשה &larr;
            </router-link>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
