<script setup lang="ts">
import type { SupplierInquiry } from '@/types'
import { StatusBadge } from '@/components/common'

defineProps<{
  inquiries: SupplierInquiry[]
}>()

const emit = defineEmits<{
  select: [name: string]
}>()

function formatDate(dateStr?: string): string {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('he-IL', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function truncateText(text: string, maxLength: number = 50): string {
  if (!text) return '-'
  // Strip HTML tags for display
  const plainText = text.replace(/<[^>]*>/g, '')
  if (plainText.length <= maxLength) return plainText
  return plainText.substring(0, maxLength) + '...'
}
</script>

<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
            מספר פנייה
          </th>
          <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
            נושא
          </th>
          <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell">
            תיאור
          </th>
          <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
            הקשר
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
          v-for="inquiry in inquiries"
          :key="inquiry.name"
          class="hover:bg-gray-50 cursor-pointer transition-colors"
          @click="emit('select', inquiry.name)"
        >
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
            {{ inquiry.name }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {{ inquiry.topic_category }}
          </td>
          <td class="px-6 py-4 text-sm text-gray-500 hidden md:table-cell max-w-xs">
            {{ truncateText(inquiry.inquiry_description) }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {{ inquiry.inquiry_context }}
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
</template>
