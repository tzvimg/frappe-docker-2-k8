/**
 * Inquiry API
 */

import { callSupplierPortal, uploadFile } from './client'
import type { SupplierInquiry, FrappeListResponse } from '@/types'

export interface InquiryStats {
  total: number
  open: number
  closed: number
  by_status: Record<string, number>
}

export interface GetInquiriesParams {
  page?: number
  page_size?: number
  status?: string
  date_from?: string
  date_to?: string
  order_by?: string
}

export interface CreateInquiryParams {
  topic_category: string
  description: string
  inquiry_context: string
  insured_id?: string
  insured_name?: string
}

export interface CreateInquiryResult {
  success: boolean
  name: string
  message: string
}

export interface AttachFileResult {
  success: boolean
  message: string
}

/**
 * Get inquiry statistics for current supplier
 */
export async function getInquiryStats(): Promise<InquiryStats> {
  return callSupplierPortal<InquiryStats>('get_inquiry_stats')
}

/**
 * Get paginated list of inquiries for current supplier
 */
export async function getInquiries(params: GetInquiriesParams = {}): Promise<FrappeListResponse<SupplierInquiry>> {
  return callSupplierPortal<FrappeListResponse<SupplierInquiry>>('get_inquiries', params)
}

/**
 * Get single inquiry by name
 */
export async function getInquiry(name: string): Promise<SupplierInquiry> {
  return callSupplierPortal<SupplierInquiry>('get_inquiry', { name })
}

/**
 * Create a new inquiry
 */
export async function createInquiry(params: CreateInquiryParams): Promise<CreateInquiryResult> {
  return callSupplierPortal<CreateInquiryResult>('create_inquiry', params)
}

/**
 * Attach an uploaded file to an inquiry
 */
export async function attachFileToInquiry(inquiryName: string, fileUrl: string): Promise<AttachFileResult> {
  return callSupplierPortal<AttachFileResult>('attach_file_to_inquiry', {
    inquiry_name: inquiryName,
    file_url: fileUrl,
  })
}

/**
 * Upload a file and attach it to an inquiry
 */
export async function uploadAndAttachFile(inquiryName: string, file: File): Promise<{ file_url: string }> {
  // First upload the file
  const uploadResult = await uploadFile(file, {
    doctype: 'Supplier Inquiry',
    docname: inquiryName,
  })

  // Then attach it to the inquiry
  await attachFileToInquiry(inquiryName, uploadResult.file_url)

  return { file_url: uploadResult.file_url }
}
