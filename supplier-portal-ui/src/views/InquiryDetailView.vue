<script setup lang="ts">
defineProps<{
  name: string
}>()
// Inquiry detail implementation will be in Phase 3
</script>

<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-4">פרטי פנייה</h1>
    <p class="text-gray-600">מספר פנייה: {{ name }}</p>
    <div class="mt-4 text-sm text-gray-500">
      (יושלם בשלב 3)
    </div>
  </div>
</template>
