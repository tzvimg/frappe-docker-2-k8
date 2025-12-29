<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore, useReferenceStore } from '@/stores'
import { getSupplierProfile, updateSupplierProfile, type SupplierProfile } from '@/api/supplier'
import { LoadingSpinner } from '@/components/common'

const authStore = useAuthStore()
const referenceStore = useReferenceStore()

// State
const profile = ref<SupplierProfile | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

// Edit mode
const isEditing = ref(false)
const isSaving = ref(false)
const saveError = ref<string | null>(null)
const saveSuccess = ref(false)

// Edit form data
const editForm = ref({
  supplier_name: '',
  phone: '',
  email: '',
  address: '',
})

onMounted(async () => {
  await referenceStore.initialize()
  await loadProfile()
})

async function loadProfile() {
  loading.value = true
  error.value = null

  try {
    profile.value = await getSupplierProfile()
  } catch (e) {
    console.error('Failed to load profile:', e)
    error.value = 'שגיאה בטעינת פרטי הספק'
  } finally {
    loading.value = false
  }
}

function startEditing() {
  if (!profile.value) return

  editForm.value = {
    supplier_name: profile.value.supplier_name || '',
    phone: profile.value.phone || '',
    email: profile.value.email || '',
    address: profile.value.address || '',
  }
  isEditing.value = true
  saveError.value = null
  saveSuccess.value = false
}

function cancelEditing() {
  isEditing.value = false
  saveError.value = null
}

async function saveProfile() {
  isSaving.value = true
  saveError.value = null
  saveSuccess.value = false

  try {
    const result = await updateSupplierProfile({
      supplier_name: editForm.value.supplier_name,
      phone: editForm.value.phone,
      email: editForm.value.email,
      address: editForm.value.address,
    })

    if (result.success) {
      // Reload profile to get updated data
      await loadProfile()
      isEditing.value = false
      saveSuccess.value = true

      // Hide success message after 3 seconds
      setTimeout(() => {
        saveSuccess.value = false
      }, 3000)
    } else {
      saveError.value = result.message || 'שגיאה בשמירת הנתונים'
    }
  } catch (e) {
    console.error('Failed to save profile:', e)
    saveError.value = 'שגיאה בשמירת הנתונים'
  } finally {
    isSaving.value = false
  }
}

// Get activity domain names
const activityDomainNames = computed(() => {
  if (!profile.value?.activity_domains) return []
  return profile.value.activity_domains.map(d => {
    const domain = referenceStore.getActivityDomain(d.activity_domain_category)
    return domain?.category_name || d.activity_domain_category
  })
})
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">פרופיל ספק</h1>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-lg border border-gray-200 p-12">
      <LoadingSpinner message="טוען פרטי ספק..." />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-white rounded-lg border border-gray-200 p-12 text-center">
      <p class="text-red-600 mb-4">{{ error }}</p>
      <button
        @click="loadProfile"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm font-medium"
      >
        נסה שוב
      </button>
    </div>

    <!-- Profile Content -->
    <template v-else-if="profile">
      <!-- Success Message -->
      <div
        v-if="saveSuccess"
        class="bg-green-50 border border-green-200 rounded-lg p-4 mb-6 flex items-center gap-3"
      >
        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="text-green-700">הפרטים נשמרו בהצלחה</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Main Profile Card -->
        <div class="lg:col-span-2 bg-white rounded-lg border border-gray-200 p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-semibold text-gray-900">פרטי הספק</h2>
            <button
              v-if="!isEditing"
              @click="startEditing"
              class="inline-flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-md transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
              עריכה
            </button>
          </div>

          <!-- View Mode -->
          <dl v-if="!isEditing" class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <dt class="text-sm font-medium text-gray-500">מזהה ספק</dt>
                <dd class="mt-1 text-gray-900">{{ profile.supplier_id }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">שם הספק</dt>
                <dd class="mt-1 text-gray-900">{{ profile.supplier_name }}</dd>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <dt class="text-sm font-medium text-gray-500">טלפון</dt>
                <dd class="mt-1 text-gray-900">{{ profile.phone || '-' }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">דוא"ל</dt>
                <dd class="mt-1 text-gray-900">{{ profile.email || '-' }}</dd>
              </div>
            </div>

            <div>
              <dt class="text-sm font-medium text-gray-500">כתובת</dt>
              <dd class="mt-1 text-gray-900">{{ profile.address || '-' }}</dd>
            </div>

            <div v-if="activityDomainNames.length > 0">
              <dt class="text-sm font-medium text-gray-500 mb-2">תחומי פעילות</dt>
              <dd class="flex flex-wrap gap-2">
                <span
                  v-for="domain in activityDomainNames"
                  :key="domain"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                >
                  {{ domain }}
                </span>
              </dd>
            </div>
          </dl>

          <!-- Edit Mode -->
          <form v-else @submit.prevent="saveProfile" class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-500 mb-1">מזהה ספק</label>
                <input
                  type="text"
                  :value="profile.supplier_id"
                  disabled
                  class="block w-full rounded-md border-gray-200 bg-gray-50 text-gray-500 text-sm"
                />
              </div>
              <div>
                <label for="supplierName" class="block text-sm font-medium text-gray-700 mb-1">
                  שם הספק
                </label>
                <input
                  id="supplierName"
                  type="text"
                  v-model="editForm.supplier_name"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
                />
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">
                  טלפון
                </label>
                <input
                  id="phone"
                  type="tel"
                  v-model="editForm.phone"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
                  dir="ltr"
                />
              </div>
              <div>
                <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
                  דוא"ל
                </label>
                <input
                  id="email"
                  type="email"
                  v-model="editForm.email"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
                  dir="ltr"
                />
              </div>
            </div>

            <div>
              <label for="address" class="block text-sm font-medium text-gray-700 mb-1">
                כתובת
              </label>
              <textarea
                id="address"
                v-model="editForm.address"
                rows="2"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
              />
            </div>

            <!-- Save Error -->
            <div v-if="saveError" class="bg-red-50 border border-red-200 rounded-lg p-3">
              <p class="text-sm text-red-600">{{ saveError }}</p>
            </div>

            <!-- Form Actions -->
            <div class="flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
              <button
                type="button"
                @click="cancelEditing"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                ביטול
              </button>
              <button
                type="submit"
                :disabled="isSaving"
                class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <LoadingSpinner v-if="isSaving" size="sm" />
                <span>{{ isSaving ? 'שומר...' : 'שמור' }}</span>
              </button>
            </div>
          </form>
        </div>

        <!-- Side Cards -->
        <div class="space-y-6">
          <!-- User Info Card -->
          <div class="bg-white rounded-lg border border-gray-200 p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">פרטי המשתמש</h2>
            <dl class="space-y-3">
              <div>
                <dt class="text-sm font-medium text-gray-500">שם מלא</dt>
                <dd class="mt-1 text-gray-900">{{ authStore.user?.full_name || '-' }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">דוא"ל</dt>
                <dd class="mt-1 text-gray-900">{{ authStore.user?.email || '-' }}</dd>
              </div>
            </dl>
          </div>

          <!-- Contact Persons Card -->
          <div
            v-if="profile.contact_persons && profile.contact_persons.length > 0"
            class="bg-white rounded-lg border border-gray-200 p-6"
          >
            <h2 class="text-lg font-semibold text-gray-900 mb-4">אנשי קשר</h2>
            <ul class="space-y-3">
              <li
                v-for="contact in profile.contact_persons"
                :key="contact.name"
                class="border-b border-gray-100 pb-3 last:border-0 last:pb-0"
              >
                <p class="font-medium text-gray-900">{{ contact.contact_name }}</p>
                <p v-if="contact.primary_role_type" class="text-sm text-gray-500">{{ contact.primary_role_type }}</p>
                <p v-if="contact.mobile_phone" class="text-sm text-gray-600" dir="ltr">{{ contact.mobile_phone }}</p>
                <p v-if="contact.email" class="text-sm text-gray-600" dir="ltr">{{ contact.email }}</p>
              </li>
            </ul>
          </div>

          <!-- Help Card -->
          <div class="bg-blue-50 rounded-lg border border-blue-200 p-6">
            <h3 class="text-sm font-semibold text-blue-800 mb-2">עדכון פרטים נוספים</h3>
            <p class="text-sm text-blue-700">
              לעדכון תחומי פעילות, אנשי קשר או פרטים נוספים, אנא פנו אלינו דרך מערכת הפניות.
            </p>
            <router-link
              to="/inquiries/new"
              class="inline-block mt-3 text-sm font-medium text-blue-700 hover:text-blue-800"
            >
              יצירת פנייה &larr;
            </router-link>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
