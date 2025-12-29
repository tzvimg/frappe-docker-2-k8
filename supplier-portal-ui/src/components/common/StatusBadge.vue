<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: string
}>()

// Status color mapping for Hebrew inquiry statuses
const statusColors = computed(() => {
  const statusMap: Record<string, { bg: string; text: string }> = {
    'פנייה חדשה התקבלה': { bg: 'bg-blue-100', text: 'text-blue-800' },
    'מיון וניתוב': { bg: 'bg-yellow-100', text: 'text-yellow-800' },
    'בטיפול': { bg: 'bg-purple-100', text: 'text-purple-800' },
    'דורש השלמות / המתנה': { bg: 'bg-orange-100', text: 'text-orange-800' },
    'נסגר – ניתן מענה': { bg: 'bg-green-100', text: 'text-green-800' },
    'סגור': { bg: 'bg-gray-100', text: 'text-gray-800' },
  }
  return statusMap[props.status] || { bg: 'bg-gray-100', text: 'text-gray-800' }
})
</script>

<template>
  <span
    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
    :class="[statusColors.bg, statusColors.text]"
  >
    {{ status }}
  </span>
</template>
