<script setup lang="ts">
defineProps<{
  title: string
  value: number | string
  icon?: string
  color?: 'blue' | 'green' | 'orange' | 'gray'
  loading?: boolean
}>()

const colorClasses = {
  blue: 'bg-blue-50 text-blue-600 border-blue-100',
  green: 'bg-green-50 text-green-600 border-green-100',
  orange: 'bg-orange-50 text-orange-600 border-orange-100',
  gray: 'bg-gray-50 text-gray-600 border-gray-100',
}
</script>

<template>
  <div
    class="rounded-lg border p-6 bg-white"
    :class="color ? colorClasses[color] : 'bg-white border-gray-200'"
  >
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm font-medium text-gray-500 mb-1">{{ title }}</p>
        <div v-if="loading" class="h-8 w-16 bg-gray-200 animate-pulse rounded"></div>
        <p v-else class="text-3xl font-bold" :class="color ? `text-${color}-600` : 'text-gray-900'">
          {{ value }}
        </p>
      </div>
      <div
        v-if="icon"
        class="p-3 rounded-full"
        :class="color ? `bg-${color}-100` : 'bg-gray-100'"
      >
        <span class="text-2xl">{{ icon }}</span>
      </div>
    </div>
  </div>
</template>
