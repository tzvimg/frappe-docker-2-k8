/**
 * Inquiry Store
 * Manages inquiry state including list, details, stats, and form state
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getInquiryStats,
  getInquiries,
  getInquiry,
  createInquiry,
  uploadAndAttachFile,
  type InquiryStats,
  type GetInquiriesParams,
  type CreateInquiryParams,
} from '@/api/inquiry'
import type { SupplierInquiry, FrappeListResponse } from '@/types'

// Time-to-live for cached stats (5 minutes)
const STATS_CACHE_TTL = 5 * 60 * 1000

export const useInquiryStore = defineStore('inquiry', () => {
  // State - Stats
  const stats = ref<InquiryStats | null>(null)
  const statsLoading = ref(false)
  const statsLastFetched = ref<number | null>(null)

  // State - List
  const inquiries = ref<SupplierInquiry[]>([])
  const listLoading = ref(false)
  const listError = ref<string | null>(null)
  const pagination = ref({
    page: 1,
    pageSize: 20,
    total: 0,
    totalPages: 0,
  })
  const filters = ref<GetInquiriesParams>({})

  // State - Current inquiry (detail view)
  const currentInquiry = ref<SupplierInquiry | null>(null)
  const detailLoading = ref(false)
  const detailError = ref<string | null>(null)

  // State - Form (create/edit)
  const formLoading = ref(false)
  const formError = ref<string | null>(null)

  // Getters
  const hasInquiries = computed(() => inquiries.value.length > 0)
  const isStatsStale = computed(() => {
    if (!statsLastFetched.value) return true
    return Date.now() - statsLastFetched.value > STATS_CACHE_TTL
  })
  const recentInquiries = computed(() => inquiries.value.slice(0, 5))

  /**
   * Fetch inquiry statistics
   */
  async function fetchStats(force = false): Promise<void> {
    if (!force && stats.value && !isStatsStale.value) return

    statsLoading.value = true

    try {
      stats.value = await getInquiryStats()
      statsLastFetched.value = Date.now()
    } catch (e) {
      console.error('Failed to fetch inquiry stats:', e)
    } finally {
      statsLoading.value = false
    }
  }

  /**
   * Fetch inquiry list with optional filters
   */
  async function fetchInquiries(params: GetInquiriesParams = {}): Promise<void> {
    listLoading.value = true
    listError.value = null
    filters.value = params

    try {
      const response: FrappeListResponse<SupplierInquiry> = await getInquiries({
        page: pagination.value.page,
        page_size: pagination.value.pageSize,
        ...params,
      })

      inquiries.value = response.data
      pagination.value = {
        page: response.page,
        pageSize: response.page_size,
        total: response.total,
        totalPages: response.total_pages,
      }
    } catch (e) {
      console.error('Failed to fetch inquiries:', e)
      listError.value = 'שגיאה בטעינת רשימת הפניות'
      inquiries.value = []
    } finally {
      listLoading.value = false
    }
  }

  /**
   * Load more inquiries (next page)
   */
  async function loadNextPage(): Promise<void> {
    if (pagination.value.page >= pagination.value.totalPages) return

    pagination.value.page++
    await fetchInquiries(filters.value)
  }

  /**
   * Go to specific page
   */
  async function goToPage(page: number): Promise<void> {
    if (page < 1 || page > pagination.value.totalPages) return

    pagination.value.page = page
    await fetchInquiries(filters.value)
  }

  /**
   * Fetch single inquiry details
   */
  async function fetchInquiry(name: string): Promise<SupplierInquiry | null> {
    detailLoading.value = true
    detailError.value = null

    try {
      currentInquiry.value = await getInquiry(name)
      return currentInquiry.value
    } catch (e) {
      console.error('Failed to fetch inquiry:', e)
      detailError.value = 'שגיאה בטעינת פרטי הפנייה'
      currentInquiry.value = null
      return null
    } finally {
      detailLoading.value = false
    }
  }

  /**
   * Create a new inquiry
   */
  async function submitInquiry(params: CreateInquiryParams): Promise<string | null> {
    formLoading.value = true
    formError.value = null

    try {
      const result = await createInquiry(params)
      if (result.success) {
        // Refresh stats after creating
        await fetchStats(true)
        return result.name
      }
      formError.value = result.message || 'שגיאה ביצירת הפנייה'
      return null
    } catch (e) {
      console.error('Failed to create inquiry:', e)
      formError.value = 'שגיאה ביצירת הפנייה'
      return null
    } finally {
      formLoading.value = false
    }
  }

  /**
   * Upload and attach a file to an inquiry
   */
  async function attachFile(inquiryName: string, file: File): Promise<string | null> {
    try {
      const result = await uploadAndAttachFile(inquiryName, file)
      return result.file_url
    } catch (e) {
      console.error('Failed to attach file:', e)
      return null
    }
  }

  /**
   * Clear current inquiry (when leaving detail view)
   */
  function clearCurrentInquiry(): void {
    currentInquiry.value = null
    detailError.value = null
  }

  /**
   * Clear form state
   */
  function clearFormState(): void {
    formError.value = null
    formLoading.value = false
  }

  /**
   * Reset list to first page with no filters
   */
  function resetList(): void {
    pagination.value.page = 1
    filters.value = {}
    inquiries.value = []
    listError.value = null
  }

  return {
    // State - Stats
    stats,
    statsLoading,

    // State - List
    inquiries,
    listLoading,
    listError,
    pagination,
    filters,

    // State - Detail
    currentInquiry,
    detailLoading,
    detailError,

    // State - Form
    formLoading,
    formError,

    // Getters
    hasInquiries,
    isStatsStale,
    recentInquiries,

    // Actions - Stats
    fetchStats,

    // Actions - List
    fetchInquiries,
    loadNextPage,
    goToPage,
    resetList,

    // Actions - Detail
    fetchInquiry,
    clearCurrentInquiry,

    // Actions - Form
    submitInquiry,
    attachFile,
    clearFormState,
  }
})
