<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useInquiryStore, useReferenceStore } from '@/stores'
import { LoadingSpinner } from '@/components/common'

const router = useRouter()
const inquiryStore = useInquiryStore()
const referenceStore = useReferenceStore()

// Form state
const formData = ref({
  topic_category: '',
  description: '',
  inquiry_context: 'ספק עצמו' as 'ספק עצמו' | 'מבוטח',
  insured_id: '',
  insured_name: '',
})

const files = ref<File[]>([])
const fileInputRef = ref<HTMLInputElement | null>(null)
const isSubmitting = ref(false)
const submitSuccess = ref(false)
const createdInquiryName = ref<string | null>(null)

// Validation errors
const errors = ref<Record<string, string>>({})

onMounted(async () => {
  await referenceStore.initialize()
  inquiryStore.clearFormState()
})

// Show insured fields when context is 'מבוטח'
const showInsuredFields = computed(() => formData.value.inquiry_context === 'מבוטח')

// Validate form
function validateForm(): boolean {
  errors.value = {}

  if (!formData.value.topic_category) {
    errors.value.topic_category = 'נא לבחור נושא פנייה'
  }

  if (!formData.value.description || formData.value.description.trim().length < 10) {
    errors.value.description = 'נא להזין תיאור פנייה (לפחות 10 תווים)'
  }

  if (!formData.value.inquiry_context) {
    errors.value.inquiry_context = 'נא לבחור הקשר פנייה'
  }

  // Validate insured fields if context is 'מבוטח'
  if (formData.value.inquiry_context === 'מבוטח') {
    if (!formData.value.insured_id || formData.value.insured_id.trim().length < 5) {
      errors.value.insured_id = 'נא להזין מספר זהות מבוטח תקין'
    }
    if (!formData.value.insured_name || formData.value.insured_name.trim().length < 2) {
      errors.value.insured_name = 'נא להזין שם מבוטח'
    }
  }

  return Object.keys(errors.value).length === 0
}

// Handle file selection
function handleFileSelect(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files) {
    const newFiles = Array.from(input.files)
    // Validate file size (max 10MB each)
    const validFiles = newFiles.filter(file => {
      if (file.size > 10 * 1024 * 1024) {
        alert(`הקובץ ${file.name} גדול מ-10MB ולא יתווסף`)
        return false
      }
      return true
    })
    files.value = [...files.value, ...validFiles]
  }
  // Reset input
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
}

// Remove file
function removeFile(index: number) {
  files.value.splice(index, 1)
}

// Format file size
function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

// Submit form
async function handleSubmit() {
  if (!validateForm()) return

  isSubmitting.value = true
  errors.value = {}

  try {
    // Create inquiry
    const inquiryName = await inquiryStore.submitInquiry({
      topic_category: formData.value.topic_category,
      description: formData.value.description,
      inquiry_context: formData.value.inquiry_context,
      insured_id: showInsuredFields.value ? formData.value.insured_id : undefined,
      insured_name: showInsuredFields.value ? formData.value.insured_name : undefined,
    })

    if (!inquiryName) {
      // Error is set in store
      return
    }

    // Upload files if any
    for (const file of files.value) {
      try {
        await inquiryStore.attachFile(inquiryName, file)
      } catch (e) {
        console.error('Failed to attach file:', file.name, e)
      }
    }

    // Success!
    submitSuccess.value = true
    createdInquiryName.value = inquiryName

    // Redirect after short delay
    setTimeout(() => {
      router.push({ name: 'InquiryDetail', params: { name: inquiryName } })
    }, 2000)
  } finally {
    isSubmitting.value = false
  }
}

function goBack() {
  router.push({ name: 'InquiryList' })
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
      חזרה
    </button>

    <!-- Success Message -->
    <div
      v-if="submitSuccess"
      class="bg-green-50 border border-green-200 rounded-lg p-6 mb-6"
    >
      <div class="flex items-center gap-3">
        <div class="flex-shrink-0">
          <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-green-800">הפנייה נשלחה בהצלחה!</h3>
          <p class="text-green-700">מספר פנייה: {{ createdInquiryName }}</p>
          <p class="text-sm text-green-600 mt-1">מעביר לדף הפנייה...</p>
        </div>
      </div>
    </div>

    <!-- Form -->
    <div v-else class="bg-white rounded-lg border border-gray-200 p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">פנייה חדשה</h1>

      <!-- Loading Reference Data -->
      <div v-if="referenceStore.loading" class="py-12">
        <LoadingSpinner message="טוען נתונים..." />
      </div>

      <form v-else @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Topic Category -->
        <div>
          <label for="topic" class="block text-sm font-medium text-gray-700 mb-1">
            נושא הפנייה <span class="text-red-500">*</span>
          </label>
          <select
            id="topic"
            v-model="formData.topic_category"
            class="block w-full rounded-md shadow-sm text-sm"
            :class="errors.topic_category
              ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
              : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'"
          >
            <option value="">בחר נושא...</option>
            <option
              v-for="topic in referenceStore.inquiryTopics"
              :key="topic.name"
              :value="topic.name"
            >
              {{ topic.category_name }}
            </option>
          </select>
          <p v-if="errors.topic_category" class="mt-1 text-sm text-red-600">
            {{ errors.topic_category }}
          </p>
        </div>

        <!-- Inquiry Context -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            הקשר הפנייה <span class="text-red-500">*</span>
          </label>
          <div class="flex gap-4">
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                v-model="formData.inquiry_context"
                value="ספק עצמו"
                class="text-blue-600 focus:ring-blue-500"
              />
              <span class="text-gray-700">ספק עצמו</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                v-model="formData.inquiry_context"
                value="מבוטח"
                class="text-blue-600 focus:ring-blue-500"
              />
              <span class="text-gray-700">מבוטח</span>
            </label>
          </div>
          <p v-if="errors.inquiry_context" class="mt-1 text-sm text-red-600">
            {{ errors.inquiry_context }}
          </p>
        </div>

        <!-- Insured Fields (conditional) -->
        <div v-if="showInsuredFields" class="bg-gray-50 rounded-lg p-4 space-y-4">
          <h3 class="text-sm font-medium text-gray-700">פרטי המבוטח</h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Insured ID -->
            <div>
              <label for="insuredId" class="block text-sm font-medium text-gray-700 mb-1">
                מספר זהות מבוטח <span class="text-red-500">*</span>
              </label>
              <input
                id="insuredId"
                type="text"
                v-model="formData.insured_id"
                class="block w-full rounded-md shadow-sm text-sm"
                :class="errors.insured_id
                  ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
                  : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'"
                placeholder="הזן מספר זהות"
              />
              <p v-if="errors.insured_id" class="mt-1 text-sm text-red-600">
                {{ errors.insured_id }}
              </p>
            </div>

            <!-- Insured Name -->
            <div>
              <label for="insuredName" class="block text-sm font-medium text-gray-700 mb-1">
                שם מלא של המבוטח <span class="text-red-500">*</span>
              </label>
              <input
                id="insuredName"
                type="text"
                v-model="formData.insured_name"
                class="block w-full rounded-md shadow-sm text-sm"
                :class="errors.insured_name
                  ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
                  : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'"
                placeholder="הזן שם מלא"
              />
              <p v-if="errors.insured_name" class="mt-1 text-sm text-red-600">
                {{ errors.insured_name }}
              </p>
            </div>
          </div>
        </div>

        <!-- Description -->
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
            תיאור הפנייה <span class="text-red-500">*</span>
          </label>
          <textarea
            id="description"
            v-model="formData.description"
            rows="6"
            class="block w-full rounded-md shadow-sm text-sm"
            :class="errors.description
              ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
              : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'"
            placeholder="תאר את הפנייה בפירוט..."
          />
          <p v-if="errors.description" class="mt-1 text-sm text-red-600">
            {{ errors.description }}
          </p>
        </div>

        <!-- File Upload -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            קבצים מצורפים
          </label>

          <!-- File List -->
          <div v-if="files.length > 0" class="mb-3 space-y-2">
            <div
              v-for="(file, index) in files"
              :key="index"
              class="flex items-center justify-between bg-gray-50 rounded-lg px-4 py-2"
            >
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                </svg>
                <span class="text-sm text-gray-700">{{ file.name }}</span>
                <span class="text-xs text-gray-500">({{ formatFileSize(file.size) }})</span>
              </div>
              <button
                type="button"
                @click="removeFile(index)"
                class="text-red-500 hover:text-red-700"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Upload Button -->
          <input
            ref="fileInputRef"
            type="file"
            multiple
            @change="handleFileSelect"
            class="hidden"
            accept=".pdf,.doc,.docx,.xls,.xlsx,.png,.jpg,.jpeg"
          />
          <button
            type="button"
            @click="fileInputRef?.click()"
            class="inline-flex items-center gap-2 px-4 py-2 border-2 border-dashed border-gray-300 rounded-lg text-sm text-gray-600 hover:border-gray-400 hover:text-gray-700"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            הוסף קבצים
          </button>
          <p class="mt-1 text-xs text-gray-500">
            PDF, Word, Excel או תמונות. גודל מקסימלי 10MB לקובץ.
          </p>
        </div>

        <!-- Form Error -->
        <div v-if="inquiryStore.formError" class="bg-red-50 border border-red-200 rounded-lg p-4">
          <p class="text-sm text-red-600">{{ inquiryStore.formError }}</p>
        </div>

        <!-- Submit Button -->
        <div class="flex items-center justify-end gap-4 pt-4 border-t border-gray-200">
          <button
            type="button"
            @click="goBack"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            ביטול
          </button>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="inline-flex items-center gap-2 px-6 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <LoadingSpinner v-if="isSubmitting" size="sm" class="text-white" />
            <span>{{ isSubmitting ? 'שולח...' : 'שלח פנייה' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
