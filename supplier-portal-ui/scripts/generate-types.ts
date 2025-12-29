/**
 * Type Generation Script
 * Parses Frappe DocType JSON files and generates TypeScript interfaces
 *
 * Run with: npm run generate:types
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Path to DocType JSON files
const DOCTYPE_BASE_PATH = path.resolve(__dirname, '../../frappe_docker/development/frappe-bench/apps/siud/siud/siud/doctype')
const OUTPUT_PATH = path.resolve(__dirname, '../src/types')

// DocTypes to generate types for
const DOCTYPES = [
  'supplier',
  'supplier_inquiry',
  'activity_domain_category',
  'inquiry_topic_category',
  'contact_person',
  'supplier_role',
  'supplier_activity_domain',
  'contact_person_role',
]

// Mapping of child table DocTypes to their file names
const CHILD_TABLE_MAP: Record<string, string> = {
  'Supplier Activity Domain': 'supplier-activity-domain',
  'Contact Person Role': 'contact-person-role',
}

// Frappe field type to TypeScript type mapping
const FIELD_TYPE_MAP: Record<string, string> = {
  'Data': 'string',
  'Text': 'string',
  'Text Editor': 'string',
  'Small Text': 'string',
  'Long Text': 'string',
  'Int': 'number',
  'Float': 'number',
  'Currency': 'number',
  'Check': 'boolean',
  'Select': 'string',
  'Link': 'string',
  'Dynamic Link': 'string',
  'Table': 'any[]',
  'Date': 'string',
  'Datetime': 'string',
  'Time': 'string',
  'Attach': 'string',
  'Attach Image': 'string',
  'Phone': 'string',
  'Email': 'string',
  'Password': 'string',
  'Read Only': 'string',
  'HTML': 'string',
  'Color': 'string',
  'Rating': 'number',
  'Duration': 'number',
  'Autocomplete': 'string',
  'Geolocation': 'string',
  'JSON': 'Record<string, any>',
}

// UI-only field types that should be excluded
const UI_ONLY_FIELDS = [
  'Section Break',
  'Column Break',
  'Tab Break',
  'HTML',
  'Button',
  'Fold',
  'Heading',
]

interface DocTypeField {
  fieldname: string
  fieldtype: string
  label?: string
  options?: string
  reqd?: number | boolean
  default?: string
}

interface DocTypeDefinition {
  name: string
  fields: DocTypeField[]
}

function toPascalCase(str: string): string {
  return str
    .split(/[-_\s]+/)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join('')
}

function toCamelCase(str: string): string {
  const pascal = toPascalCase(str)
  return pascal.charAt(0).toLowerCase() + pascal.slice(1)
}

function toKebabCase(str: string): string {
  return str
    .split(/[-_\s]+/)
    .map(word => word.toLowerCase())
    .join('-')
}

function getTypeScriptType(field: DocTypeField): string {
  const baseType = FIELD_TYPE_MAP[field.fieldtype] || 'unknown'

  // Handle Select fields with specific options
  if (field.fieldtype === 'Select' && field.options) {
    const options = field.options.split('\n').filter(Boolean)
    if (options.length > 0) {
      return options.map(opt => `'${opt.trim()}'`).join(' | ')
    }
  }

  // Handle Table fields with specific child DocType
  if (field.fieldtype === 'Table' && field.options) {
    const childType = toPascalCase(field.options)
    return `${childType}[]`
  }

  return baseType
}

interface GeneratedInterface {
  code: string
  imports: string[]
}

function generateInterface(doctype: DocTypeDefinition): GeneratedInterface {
  const interfaceName = toPascalCase(doctype.name)
  const fields = doctype.fields
    .filter(f => !UI_ONLY_FIELDS.includes(f.fieldtype))
    .filter(f => f.fieldname && f.fieldtype)

  const imports: string[] = []
  const lines: string[] = []
  lines.push(`/**`)
  lines.push(` * ${doctype.name} DocType`)
  lines.push(` * Auto-generated from Frappe DocType definition`)
  lines.push(` */`)
  lines.push(`export interface ${interfaceName} {`)
  lines.push(`  /** Document name (primary key) */`)
  lines.push(`  name: string`)
  lines.push(`  /** Creation timestamp */`)
  lines.push(`  creation?: string`)
  lines.push(`  /** Last modified timestamp */`)
  lines.push(`  modified?: string`)
  lines.push(`  /** Modified by user */`)
  lines.push(`  modified_by?: string`)
  lines.push(`  /** Owner user */`)
  lines.push(`  owner?: string`)
  lines.push(`  /** Document status (0=Draft, 1=Submitted, 2=Cancelled) */`)
  lines.push(`  docstatus?: 0 | 1 | 2`)

  for (const field of fields) {
    const tsType = getTypeScriptType(field)
    const isRequired = field.reqd === 1 || field.reqd === true
    const optional = isRequired ? '' : '?'
    const label = field.label || field.fieldname

    // Track imports for child table types
    if (field.fieldtype === 'Table' && field.options && CHILD_TABLE_MAP[field.options]) {
      const childType = toPascalCase(field.options)
      const childFile = CHILD_TABLE_MAP[field.options]
      imports.push(`import type { ${childType} } from './${childFile}'`)
    }

    lines.push(`  /** ${label} */`)
    lines.push(`  ${field.fieldname}${optional}: ${tsType}`)
  }

  lines.push(`}`)

  return {
    code: lines.join('\n'),
    imports: [...new Set(imports)], // Remove duplicates
  }
}

function generateFieldMetadata(doctype: DocTypeDefinition): string {
  const metaName = `${toCamelCase(doctype.name)}Fields`
  const fields = doctype.fields
    .filter(f => !UI_ONLY_FIELDS.includes(f.fieldtype))
    .filter(f => f.fieldname && f.fieldtype)

  const lines: string[] = []
  lines.push(`/**`)
  lines.push(` * Field metadata for ${doctype.name}`)
  lines.push(` */`)
  lines.push(`export const ${metaName} = {`)

  for (const field of fields) {
    const isRequired = field.reqd === 1 || field.reqd === true
    lines.push(`  ${field.fieldname}: {`)
    lines.push(`    fieldtype: '${field.fieldtype}',`)
    lines.push(`    label: '${field.label || field.fieldname}',`)
    lines.push(`    required: ${isRequired},`)
    if (field.options) {
      if (field.fieldtype === 'Select') {
        const options = field.options.split('\n').filter(Boolean)
        lines.push(`    options: [${options.map(o => `'${o.trim()}'`).join(', ')}],`)
      } else {
        lines.push(`    options: '${field.options}',`)
      }
    }
    if (field.default) {
      lines.push(`    default: '${field.default}',`)
    }
    lines.push(`  },`)
  }

  lines.push(`} as const`)

  return lines.join('\n')
}

function loadDocType(doctypeName: string): DocTypeDefinition | null {
  const doctypePath = path.join(DOCTYPE_BASE_PATH, doctypeName, `${doctypeName}.json`)

  if (!fs.existsSync(doctypePath)) {
    console.warn(`Warning: DocType file not found: ${doctypePath}`)
    return null
  }

  try {
    const content = fs.readFileSync(doctypePath, 'utf-8')
    const json = JSON.parse(content)
    return {
      name: json.name,
      fields: json.fields || [],
    }
  } catch (error) {
    console.error(`Error loading DocType ${doctypeName}:`, error)
    return null
  }
}

function main() {
  // Ensure output directory exists
  if (!fs.existsSync(OUTPUT_PATH)) {
    fs.mkdirSync(OUTPUT_PATH, { recursive: true })
  }

  const indexExports: string[] = []

  console.log('Generating TypeScript types from Frappe DocTypes...\n')

  for (const doctypeName of DOCTYPES) {
    console.log(`Processing: ${doctypeName}`)

    const doctype = loadDocType(doctypeName)
    if (!doctype) {
      continue
    }

    const { code: interfaceCode, imports } = generateInterface(doctype)
    const metadataCode = generateFieldMetadata(doctype)

    const fileContentParts = [
      '// Auto-generated file - do not edit manually',
      `// Generated from: ${doctypeName}.json`,
      '',
    ]

    // Add imports if any
    if (imports.length > 0) {
      fileContentParts.push(...imports, '')
    }

    fileContentParts.push(
      interfaceCode,
      '',
      metadataCode,
      ''
    )

    const fileContent = fileContentParts.join('\n')

    const outputFile = path.join(OUTPUT_PATH, `${toKebabCase(doctype.name)}.ts`)
    fs.writeFileSync(outputFile, fileContent)
    console.log(`  → Created: ${outputFile}`)

    // Add to index exports (using export type for interfaces with verbatimModuleSyntax)
    const exportName = toPascalCase(doctype.name)
    const metaExportName = `${toCamelCase(doctype.name)}Fields`
    const fileName = toKebabCase(doctype.name)
    indexExports.push(`export type { ${exportName} } from './${fileName}'`)
    indexExports.push(`export { ${metaExportName} } from './${fileName}'`)
  }

  // Generate index.ts
  const indexContent = [
    '// Auto-generated index file',
    '// Re-exports all generated types',
    '',
    ...indexExports,
    '',
    '// Common Frappe types',
    'export interface FrappeDoc {',
    '  name: string',
    '  creation?: string',
    '  modified?: string',
    '  modified_by?: string',
    '  owner?: string',
    '  docstatus?: 0 | 1 | 2',
    '}',
    '',
    'export interface FrappeListResponse<T> {',
    '  data: T[]',
    '  total: number',
    '  page: number',
    '  page_size: number',
    '  total_pages: number',
    '}',
    '',
    'export interface FrappeResponse<T> {',
    '  message: T',
    '}',
    '',
    'export interface FrappeError {',
    '  exc_type: string',
    '  exception: string',
    '  _server_messages?: string',
    '}',
    '',
  ].join('\n')

  fs.writeFileSync(path.join(OUTPUT_PATH, 'index.ts'), indexContent)
  console.log(`\n✓ Generated index.ts`)
  console.log(`\nType generation complete! Generated ${DOCTYPES.length} types.`)
}

main()
