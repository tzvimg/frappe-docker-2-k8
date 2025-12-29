/**
 * Base Frappe REST API client
 * Handles all communication with the Frappe backend
 */

import axios, { type AxiosInstance, type AxiosError } from 'axios'
import type { FrappeResponse, FrappeError } from '@/types'

// Get API URL from environment
const API_URL = import.meta.env.VITE_FRAPPE_API_URL || ''
const AUTH_MODE = import.meta.env.VITE_AUTH_MODE || 'session'

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  withCredentials: true, // Required for session-based auth
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
})

// Request interceptor - add auth token for JWT mode
api.interceptors.request.use(
  (config) => {
    if (AUTH_MODE === 'jwt') {
      const token = localStorage.getItem('frappe_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<FrappeError>) => {
    if (error.response?.status === 401) {
      // Clear auth state and redirect to login
      localStorage.removeItem('frappe_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

/**
 * Call a whitelisted Frappe API method
 */
export async function call<T>(
  method: string,
  args: object = {}
): Promise<T> {
  const response = await api.post<FrappeResponse<T>>(
    `/api/method/${method}`,
    args
  )
  return response.data.message
}

/**
 * Call a supplier portal API method
 */
export async function callSupplierPortal<T>(
  method: string,
  args: object = {}
): Promise<T> {
  return call<T>(`siud.api.supplier_portal.${method}`, args)
}

/**
 * Get a list of documents
 */
export async function getList<T>(
  doctype: string,
  options: {
    fields?: string[]
    filters?: Record<string, unknown>
    orderBy?: string
    limit?: number
    start?: number
  } = {}
): Promise<T[]> {
  const params = new URLSearchParams()
  params.append('doctype', doctype)

  if (options.fields) {
    params.append('fields', JSON.stringify(options.fields))
  }
  if (options.filters) {
    params.append('filters', JSON.stringify(options.filters))
  }
  if (options.orderBy) {
    params.append('order_by', options.orderBy)
  }
  if (options.limit) {
    params.append('limit_page_length', options.limit.toString())
  }
  if (options.start) {
    params.append('limit_start', options.start.toString())
  }

  const response = await api.get<{ data: T[] }>(
    `/api/resource/${doctype}?${params.toString()}`
  )
  return response.data.data
}

/**
 * Get a single document by name
 */
export async function getDoc<T>(
  doctype: string,
  name: string
): Promise<T> {
  const response = await api.get<{ data: T }>(
    `/api/resource/${doctype}/${encodeURIComponent(name)}`
  )
  return response.data.data
}

/**
 * Create a new document
 */
export async function createDoc<T>(
  doctype: string,
  doc: Partial<T>
): Promise<T> {
  const response = await api.post<{ data: T }>(
    `/api/resource/${doctype}`,
    doc
  )
  return response.data.data
}

/**
 * Update an existing document
 */
export async function updateDoc<T>(
  doctype: string,
  name: string,
  doc: Partial<T>
): Promise<T> {
  const response = await api.put<{ data: T }>(
    `/api/resource/${doctype}/${encodeURIComponent(name)}`,
    doc
  )
  return response.data.data
}

/**
 * Delete a document
 */
export async function deleteDoc(
  doctype: string,
  name: string
): Promise<void> {
  await api.delete(`/api/resource/${doctype}/${encodeURIComponent(name)}`)
}

/**
 * Upload a file
 */
export async function uploadFile(
  file: File,
  options: {
    doctype?: string
    docname?: string
    isPrivate?: boolean
  } = {}
): Promise<{ file_url: string; name: string }> {
  const formData = new FormData()
  formData.append('file', file)

  if (options.doctype) {
    formData.append('doctype', options.doctype)
  }
  if (options.docname) {
    formData.append('docname', options.docname)
  }
  if (options.isPrivate !== undefined) {
    formData.append('is_private', options.isPrivate ? '1' : '0')
  }

  const response = await api.post<{ message: { file_url: string; name: string } }>(
    '/api/method/upload_file',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  )
  return response.data.message
}

/**
 * Login with username and password (session-based auth)
 */
export async function login(
  usr: string,
  pwd: string
): Promise<{ message: string; full_name?: string }> {
  const response = await api.post<{ message: string; full_name?: string }>(
    '/api/method/login',
    { usr, pwd }
  )
  return response.data
}

/**
 * Logout current session
 */
export async function logout(): Promise<void> {
  await api.post('/api/method/logout')
  localStorage.removeItem('frappe_token')
}

/**
 * Get logged in user info
 */
export async function getLoggedUser(): Promise<string> {
  const response = await api.get<{ message: string }>('/api/method/frappe.auth.get_logged_user')
  return response.data.message
}

export default api
