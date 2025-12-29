/**
 * Reference Data Store
 * Manages static reference data (activity domains, inquiry topics, etc.)
 * Loads from build-time JSON or fetches from API as fallback
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getReferenceData, type ReferenceData, type InquiryStatus, type InquiryContext } from '@/api/reference'
import type { ActivityDomainCategory, InquiryTopicCategory, SupplierRole, ContactPersonRole } from '@/types'

// Time-to-live for cached data (1 hour)
const CACHE_TTL = 60 * 60 * 1000

export const useReferenceStore = defineStore('reference', () => {
  // State
  const activityDomains = ref<ActivityDomainCategory[]>([])
  const inquiryTopics = ref<InquiryTopicCategory[]>([])
  const supplierRoles = ref<SupplierRole[]>([])
  const contactPersonRoles = ref<ContactPersonRole[]>([])
  const inquiryStatuses = ref<InquiryStatus[]>([])
  const inquiryContexts = ref<InquiryContext[]>([])

  const loading = ref(false)
  const error = ref<string | null>(null)
  const lastFetched = ref<number | null>(null)
  const initialized = ref(false)

  // Getters
  const isLoaded = computed(() => initialized.value && activityDomains.value.length > 0)
  const isCacheValid = computed(() => {
    if (!lastFetched.value) return false
    return Date.now() - lastFetched.value < CACHE_TTL
  })

  const openStatuses = computed(() =>
    inquiryStatuses.value.filter(s => s.type === 'open').map(s => s.value)
  )

  const closedStatuses = computed(() =>
    inquiryStatuses.value.filter(s => s.type === 'closed').map(s => s.value)
  )

  /**
   * Initialize reference data
   * First tries to load from build-time JSON, then falls back to API
   */
  async function initialize(): Promise<void> {
    if (initialized.value && isCacheValid.value) return

    loading.value = true
    error.value = null

    try {
      // Try loading from build-time JSON files first
      const loaded = await loadFromStaticFiles()
      if (loaded) {
        initialized.value = true
        lastFetched.value = Date.now()
        return
      }

      // Fallback to API
      await fetchFromApi()
    } catch (e) {
      console.error('Failed to initialize reference data:', e)
      error.value = 'שגיאה בטעינת נתוני הפניה'
    } finally {
      loading.value = false
    }
  }

  /**
   * Load reference data from static JSON files (build-time generated)
   */
  async function loadFromStaticFiles(): Promise<boolean> {
    try {
      const response = await fetch('/data/reference-data.json')
      if (!response.ok) return false

      const data: ReferenceData = await response.json()
      setReferenceData(data)
      return true
    } catch {
      console.warn('Could not load static reference data, falling back to API')
      return false
    }
  }

  /**
   * Fetch reference data from API
   */
  async function fetchFromApi(): Promise<void> {
    const data = await getReferenceData()
    setReferenceData(data)
    initialized.value = true
    lastFetched.value = Date.now()
  }

  /**
   * Set reference data from response
   */
  function setReferenceData(data: ReferenceData): void {
    activityDomains.value = data.activity_domains || []
    inquiryTopics.value = data.inquiry_topics || []
    supplierRoles.value = data.supplier_roles || []
    contactPersonRoles.value = data.contact_person_roles || []
    inquiryStatuses.value = data.inquiry_statuses || []
    inquiryContexts.value = data.inquiry_contexts || []
  }

  /**
   * Force refresh from API (ignores cache)
   */
  async function refresh(): Promise<void> {
    loading.value = true
    error.value = null

    try {
      await fetchFromApi()
    } catch (e) {
      console.error('Failed to refresh reference data:', e)
      error.value = 'שגיאה בעדכון נתוני הפניה'
    } finally {
      loading.value = false
    }
  }

  /**
   * Get activity domain by name
   */
  function getActivityDomain(name: string): ActivityDomainCategory | undefined {
    return activityDomains.value.find(d => d.name === name)
  }

  /**
   * Get inquiry topic by name
   */
  function getInquiryTopic(name: string): InquiryTopicCategory | undefined {
    return inquiryTopics.value.find(t => t.name === name)
  }

  /**
   * Get supplier role by name
   */
  function getSupplierRole(name: string): SupplierRole | undefined {
    return supplierRoles.value.find(r => r.name === name)
  }

  /**
   * Get inquiry status label
   */
  function getStatusLabel(value: string): string {
    const status = inquiryStatuses.value.find(s => s.value === value)
    return status?.label || value
  }

  /**
   * Get inquiry context label
   */
  function getContextLabel(value: string): string {
    const context = inquiryContexts.value.find(c => c.value === value)
    return context?.label || value
  }

  /**
   * Check if status is an "open" status
   */
  function isOpenStatus(value: string): boolean {
    return openStatuses.value.includes(value)
  }

  return {
    // State
    activityDomains,
    inquiryTopics,
    supplierRoles,
    contactPersonRoles,
    inquiryStatuses,
    inquiryContexts,
    loading,
    error,
    initialized,

    // Getters
    isLoaded,
    isCacheValid,
    openStatuses,
    closedStatuses,

    // Actions
    initialize,
    refresh,
    getActivityDomain,
    getInquiryTopic,
    getSupplierRole,
    getStatusLabel,
    getContextLabel,
    isOpenStatus,
  }
})
