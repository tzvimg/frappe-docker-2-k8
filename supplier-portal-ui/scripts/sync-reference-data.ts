/**
 * Reference Data Sync Script
 * Fetches reference data from Frappe at build time and saves as JSON
 *
 * Run with: npm run generate:reference
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const OUTPUT_PATH = path.resolve(__dirname, '../public/data')
const API_URL = process.env.VITE_FRAPPE_API_URL || 'http://localhost:8000'

interface ReferenceData {
  activity_domains: unknown[]
  inquiry_topics: unknown[]
  supplier_roles: unknown[]
  contact_person_roles: unknown[]
  inquiry_statuses: unknown[]
  inquiry_contexts: unknown[]
}

async function fetchReferenceData(): Promise<ReferenceData | null> {
  try {
    const response = await fetch(
      `${API_URL}/api/method/siud.api.supplier_portal.get_reference_data`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    )

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data.message as ReferenceData
  } catch (error) {
    console.warn('Warning: Could not fetch reference data from Frappe:', error)
    console.log('Using empty reference data. Run this script when Frappe is available.')
    return null
  }
}

function getDefaultReferenceData(): ReferenceData {
  return {
    activity_domains: [],
    inquiry_topics: [],
    supplier_roles: [],
    contact_person_roles: [],
    inquiry_statuses: [
      { value: 'פנייה חדשה התקבלה', label: 'פנייה חדשה התקבלה', type: 'open' },
      { value: 'בטיפול', label: 'בטיפול', type: 'open' },
      { value: 'מיון וניתוב', label: 'מיון וניתוב', type: 'open' },
      { value: 'דורש השלמות / המתנה', label: 'דורש השלמות / המתנה', type: 'open' },
      { value: 'סגור', label: 'סגור', type: 'closed' },
      { value: 'נסגר – ניתן מענה', label: 'נסגר – ניתן מענה', type: 'closed' },
    ],
    inquiry_contexts: [
      { value: 'ספק עצמו', label: 'ספק עצמו' },
      { value: 'מבוטח', label: 'מבוטח' },
    ],
  }
}

async function main() {
  // Ensure output directory exists
  if (!fs.existsSync(OUTPUT_PATH)) {
    fs.mkdirSync(OUTPUT_PATH, { recursive: true })
  }

  console.log('Fetching reference data from Frappe...\n')
  console.log(`API URL: ${API_URL}`)

  let referenceData = await fetchReferenceData()

  if (!referenceData) {
    console.log('\nUsing default reference data...')
    referenceData = getDefaultReferenceData()
  }

  // Save each data type as separate JSON file
  const dataFiles = [
    { name: 'activity-domains', data: referenceData.activity_domains },
    { name: 'inquiry-topics', data: referenceData.inquiry_topics },
    { name: 'supplier-roles', data: referenceData.supplier_roles },
    { name: 'contact-person-roles', data: referenceData.contact_person_roles },
    { name: 'inquiry-statuses', data: referenceData.inquiry_statuses },
    { name: 'inquiry-contexts', data: referenceData.inquiry_contexts },
  ]

  for (const { name, data } of dataFiles) {
    const filePath = path.join(OUTPUT_PATH, `${name}.json`)
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2))
    console.log(`  → Created: ${filePath}`)
  }

  // Also save combined reference data
  const combinedPath = path.join(OUTPUT_PATH, 'reference-data.json')
  fs.writeFileSync(combinedPath, JSON.stringify(referenceData, null, 2))
  console.log(`  → Created: ${combinedPath}`)

  console.log('\nReference data sync complete!')
}

main()
