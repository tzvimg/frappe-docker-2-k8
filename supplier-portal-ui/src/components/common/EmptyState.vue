<script setup lang="ts">
defineProps<{
  title: string
  description?: string
  icon?: string
}>()

defineEmits<{
  action: []
}>()
</script>

<template>
  <div class="flex flex-col items-center justify-center py-12 text-center">
    <div
      v-if="icon"
      class="mb-4 p-4 rounded-full bg-gray-100"
    >
      <span class="text-4xl">{{ icon }}</span>
    </div>
    <h3 class="text-lg font-medium text-gray-900 mb-2">{{ title }}</h3>
    <p v-if="description" class="text-sm text-gray-500 max-w-sm mb-6">
      {{ description }}
    </p>
    <slot name="action">
      <button
        v-if="$slots.default"
        @click="$emit('action')"
        class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        <slot />
      </button>
    </slot>
  </div>
</template>
