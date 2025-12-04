# DocType Design Guidelines and Best Practices

This document provides comprehensive guidelines for designing DocTypes using the YAML specification system.

## Table of Contents

1. [General Principles](#general-principles)
2. [Naming Conventions](#naming-conventions)
3. [Field Organization](#field-organization)
4. [Field Selection Guide](#field-selection-guide)
5. [Relationships and Links](#relationships-and-links)
6. [Validation Patterns](#validation-patterns)
7. [UI/UX Best Practices](#uiux-best-practices)
8. [Performance Considerations](#performance-considerations)
9. [Security and Permissions](#security-and-permissions)
10. [Common Patterns Library](#common-patterns-library)
11. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

## General Principles

### KISS (Keep It Simple, Stupid)

- Start with minimal fields - you can always add more later
- Don't add fields "just in case" - add them when needed
- Each field should have a clear purpose
- If you can't explain why a field exists, remove it

### Single Responsibility

- Each DocType should represent one clear entity or concept
- Don't try to make one DocType serve multiple purposes
- Use child tables for one-to-many relationships within a document
- Use Link fields for many-to-many or independent relationships

### Data Integrity

- Always mark required fields as `reqd: true`
- Use `unique: true` for identifier fields
- Set appropriate field types to enforce data formats
- Use Select fields instead of free text when options are limited

## Naming Conventions

### DocType Names

- Use **Title Case** with spaces (e.g., "Service Provider")
- Should be singular nouns (e.g., "Caregiver", not "Caregivers")
- Should be descriptive and self-explanatory
- Avoid abbreviations unless universally understood

**Good examples:**
- Service Provider
- Service Provider Application
- Document Approval
- Caregiver

**Bad examples:**
- SP (too abbreviated)
- ServiceProvider (no spaces)
- Service Providers (plural)
- Doc Approval (unclear abbreviation)

### Field Names (fieldname)

- Use **snake_case** (all lowercase with underscores)
- Should be descriptive and clear
- Avoid abbreviations except for very common ones
- Should be unique within the DocType

**Good examples:**
- `provider_name`
- `hp_number`
- `start_date`
- `email_address`

**Bad examples:**
- `prov_nm` (too abbreviated)
- `providerName` (camelCase not allowed)
- `provider name` (spaces not allowed)
- `name` (too generic, may conflict with system field)

### Label Names

- Use **Hebrew** for this project (right-to-left)
- Should be user-friendly and clear
- Can be more verbose than fieldnames
- Should match business terminology

**Examples:**
- fieldname: `provider_name` → label: `שם נותן השירות`
- fieldname: `hp_number` → label: `מספר ח"פ`
- fieldname: `start_date` → label: `תאריך התחלה`

## Field Organization

### Section Breaks

Use Section Breaks to group related fields visually:

```yaml
# Basic Information
- fieldname: "basic_section"
  fieldtype: "Section Break"
  label: "פרטים בסיסיים"

- fieldname: "provider_name"
  fieldtype: "Data"
  label: "שם נותן השירות"

# Contact Information
- fieldname: "contact_section"
  fieldtype: "Section Break"
  label: "פרטי קשר"

- fieldname: "email"
  fieldtype: "Data"
  label: "אימייל"
```

**Best practices:**
- Use 3-6 sections per DocType (not too many, not too few)
- Group logically related fields together
- Put most important information first
- Use descriptive section labels in Hebrew

### Column Breaks

Use Column Breaks for side-by-side layout:

```yaml
- fieldname: "provider_name"
  fieldtype: "Data"
  label: "שם נותן השירות"

- fieldname: "column_break_1"
  fieldtype: "Column Break"

- fieldname: "hp_number"
  fieldtype: "Data"
  label: "מספר ח\"פ"
```

**Best practices:**
- Use 2 columns maximum in most cases
- Put related but independent fields side-by-side
- Balance the number of fields in each column
- Consider mobile view (columns stack on small screens)

### Field Ordering Strategy

1. **Identification fields** - Name, ID, code (top)
2. **Core business fields** - Essential data
3. **Relationships** - Links to other DocTypes
4. **Dates and timeline** - Start, end, validity
5. **Status and workflow** - Current state
6. **Additional details** - Optional information
7. **Notes and attachments** - Bottom

## Field Selection Guide

### When to Use Each Field Type

#### Data
- Single-line text up to 140 characters
- Names, codes, short identifiers
- Email (with `options: "Email"`)
- Phone (with `options: "Phone"`)

```yaml
- fieldname: "provider_name"
  fieldtype: "Data"
  label: "שם נותן השירות"
  length: 100
```

#### Text / Small Text
- Multi-line plain text
- Descriptions, comments, notes
- Use Small Text for shorter content

```yaml
- fieldname: "notes"
  fieldtype: "Small Text"
  label: "הערות"
```

#### Text Editor
- Rich formatted text with HTML
- Long descriptions needing formatting
- User-facing content

```yaml
- fieldname: "description"
  fieldtype: "Text Editor"
  label: "תיאור מפורט"
```

#### Select
- Fixed set of options (< 20 options)
- Status fields
- Categories or types
- Options separated by `\n`

```yaml
- fieldname: "status"
  fieldtype: "Select"
  label: "סטטוס"
  options: "פעיל\nסגור\nמושהה"
  default: "פעיל"
```

#### Link
- Reference to another DocType
- Many-to-one relationships
- Can fetch values from linked document

```yaml
- fieldname: "service_provider"
  fieldtype: "Link"
  label: "נותן שירות"
  options: "Service Provider"
```

#### Int / Float
- Numeric values
- Use Int for whole numbers
- Use Float with precision for decimals

```yaml
- fieldname: "weekly_hours"
  fieldtype: "Float"
  label: "שעות שבועיות"
  precision: 1

- fieldname: "employee_count"
  fieldtype: "Int"
  label: "מספר עובדים"
```

#### Date / Datetime
- Date for day-level precision
- Datetime for time-level precision

```yaml
- fieldname: "start_date"
  fieldtype: "Date"
  label: "תאריך התחלה"
  default: "Today"

- fieldname: "submission_time"
  fieldtype: "Datetime"
  label: "זמן הגשה"
```

#### Check
- Boolean yes/no values
- Flags and toggles

```yaml
- fieldname: "is_active"
  fieldtype: "Check"
  label: "פעיל"
  default: true
```

#### Table
- One-to-many relationships
- Child records within parent
- Must reference a child DocType

```yaml
- fieldname: "documents"
  fieldtype: "Table"
  label: "רשימת מסמכים"
  options: "Document Checklist"
```

#### Attach
- File uploads
- Documents, images, PDFs

```yaml
- fieldname: "attachment"
  fieldtype: "Attach"
  label: "קובץ מצורף"
```

## Relationships and Links

### Link Fields

Use Link fields to create relationships between DocTypes:

```yaml
- fieldname: "service_provider"
  fieldtype: "Link"
  label: "נותן שירות"
  options: "Service Provider"
  reqd: true
  in_standard_filter: true
```

### Auto-Fetch from Links

Automatically pull values from linked documents:

```yaml
- fieldname: "service_provider"
  fieldtype: "Link"
  label: "נותן שירות"
  options: "Service Provider"

- fieldname: "provider_name"
  fieldtype: "Data"
  label: "שם נותן השירות"
  read_only: true
  fetch_from: "service_provider.provider_name"
```

**Best practices:**
- Mark fetched fields as `read_only: true`
- Fetch display values for better UX
- Don't fetch too many fields (performance)
- Fetch fields shown in list view

### Child Tables

For one-to-many relationships within a document:

**Parent DocType:**
```yaml
- fieldname: "items"
  fieldtype: "Table"
  label: "פריטים"
  options: "Purchase Request Item"
```

**Child DocType:**
- Create separately as `istable: 1`
- Only contains data fields, no workflow
- Automatically linked to parent

**Best practices:**
- Use child tables for dependent data
- Keep child tables simple (< 10 fields)
- Don't nest child tables (not supported)
- Use read-only fields in child tables for calculated values

## Validation Patterns

### Required Fields

Mark essential fields as required:

```yaml
- fieldname: "provider_name"
  fieldtype: "Data"
  label: "שם נותן השירות"
  reqd: true
```

### Unique Fields

Ensure uniqueness for identifiers:

```yaml
- fieldname: "hp_number"
  fieldtype: "Data"
  label: "מספר ח\"פ"
  unique: true
  length: 9
```

### Length Constraints

Set maximum length for Data fields:

```yaml
- fieldname: "branch_code"
  fieldtype: "Data"
  label: "קוד סניף"
  length: 2
```

### Default Values

Provide sensible defaults:

```yaml
- fieldname: "status"
  fieldtype: "Select"
  options: "פעיל\nסגור"
  default: "פעיל"

- fieldname: "submission_date"
  fieldtype: "Date"
  default: "Today"
```

### Complex Validations

Document validation rules that require Python controller:

```yaml
- fieldname: "end_date"
  fieldtype: "Date"
  label: "תאריך סיום"
  description: "חייב להיות אחרי תאריך התחלה"
```

Then implement in controller:
```python
def validate(self):
    if self.end_date and self.start_date:
        if self.end_date < self.start_date:
            frappe.throw("תאריך סיום חייב להיות אחרי תאריך התחלה")
```

## UI/UX Best Practices

### List View Fields

Select 3-5 most important fields for list view:

```yaml
- fieldname: "provider_name"
  in_list_view: true

- fieldname: "hp_number"
  in_list_view: true

- fieldname: "status"
  in_list_view: true
```

**What to include:**
- Primary identifier (name, code)
- Key status field
- Important dates
- Critical relationships

**What to exclude:**
- Long text fields
- Internal IDs
- Too many fields (clutters view)

### Standard Filters

Add frequently searched fields to filters:

```yaml
- fieldname: "service_type"
  in_standard_filter: true

- fieldname: "status"
  in_standard_filter: true
```

**Good filter candidates:**
- Status/state fields
- Categories and types
- Date fields
- Key relationships

### Read-Only Fields

Mark calculated or auto-fetched fields as read-only:

```yaml
- fieldname: "monthly_cost"
  fieldtype: "Float"
  label: "עלות חודשית"
  read_only: true
  description: "מחושב אוטומטית"
```

### Hidden Fields

Hide technical fields from users:

```yaml
- fieldname: "internal_id"
  fieldtype: "Data"
  hidden: true
```

Use sparingly - prefer not adding the field if truly never needed.

### Field Descriptions

Add helpful descriptions for complex fields:

```yaml
- fieldname: "hp_number"
  fieldtype: "Data"
  label: "מספר ח\"פ"
  description: "מספר ח\"פ בן 9 ספרות"
```

## Performance Considerations

### Indexing

Fields marked with certain properties get database indexes:
- `unique: true` - Unique index
- `in_standard_filter: true` - Regular index

### Fetch Performance

- Limit number of `fetch_from` fields (each is a query)
- Don't fetch large text fields
- Consider caching fetched values in controller

### Child Table Size

- Keep child tables reasonable (< 100 rows typically)
- For large datasets, use separate linked DocType
- Consider pagination for very large child tables

## Security and Permissions

### Permission Levels

Standard permission types:
- `read` - View documents
- `write` - Edit documents
- `create` - Create new documents
- `delete` - Delete documents
- `submit` - Submit (workflow)
- `cancel` - Cancel submitted documents
- `amend` - Amend cancelled documents

### Role-Based Permissions

```yaml
permissions:
  - role: "System Manager"
    read: 1
    write: 1
    create: 1
    delete: 1

  - role: "Internal Reviewer"
    read: 1
    write: 1
    create: 1
    delete: 0

  - role: "Service Provider User"
    read: 1
    write: 0
    create: 0
```

**Best practices:**
- System Manager always gets full access
- Give minimum necessary permissions
- External users (portal) get limited access
- Use workflow for approval processes

### Sensitive Data

For sensitive fields:
- Don't include in list view
- Consider field-level permissions (in controller)
- Hide from export if needed
- Audit access in controller

## Common Patterns Library

### Master Data Pattern

For entities like Service Provider, Customer, Item:

```yaml
doctype:
  name: "Entity Name"
  naming_rule: "autoname"
  autoname: "format:PREFIX-{#####}"
  track_changes: true

  fields:
    # Basic info
    # Contact info
    # Status
    # Dates
    # Notes
```

### Transaction Pattern

For documents like Orders, Invoices, Applications:

```yaml
doctype:
  name: "Transaction Name"
  naming_rule: "autoname"
  autoname: "format:PREFIX-{#####}"
  is_submittable: true
  track_changes: true

  fields:
    # Header info (date, reference)
    # Party info (customer, supplier)
    # Items (child table)
    # Totals (calculated)
    # Terms and conditions
    # Status and workflow
```

### Configuration Pattern

For settings and configuration:

```yaml
doctype:
  name: "Settings Name"
  is_single: true  # Only one document

  fields:
    # Configuration options
    # Feature toggles
    # Default values
```

### Status Tracking Pattern

```yaml
- fieldname: "status"
  fieldtype: "Select"
  label: "סטטוס"
  options: "Draft\nActive\nInactive\nClosed"
  default: "Draft"
  in_list_view: true
  in_standard_filter: true
```

### Date Range Pattern

```yaml
- fieldname: "start_date"
  fieldtype: "Date"
  label: "תאריך התחלה"
  reqd: true

- fieldname: "end_date"
  fieldtype: "Date"
  label: "תאריך סיום"

- fieldname: "is_active"
  fieldtype: "Check"
  label: "פעיל"
  read_only: true
  description: "מחושב אוטומטית לפי טווח תאריכים"
```

### Approval Workflow Pattern

```yaml
- fieldname: "workflow_state"
  fieldtype: "Select"
  label: "מצב"
  options: "Draft\nPending Approval\nApproved\nRejected"
  default: "Draft"
  read_only: true

- fieldname: "approved_by"
  fieldtype: "Link"
  label: "אושר על ידי"
  options: "User"
  read_only: true

- fieldname: "approval_date"
  fieldtype: "Datetime"
  label: "תאריך אישור"
  read_only: true

- fieldname: "rejection_reason"
  fieldtype: "Small Text"
  label: "סיבת דחייה"
```

## Anti-Patterns to Avoid

### ❌ Don't: Use Data for Long Text

```yaml
# BAD
- fieldname: "description"
  fieldtype: "Data"  # Limited to 140 chars
```

```yaml
# GOOD
- fieldname: "description"
  fieldtype: "Text Editor"
```

### ❌ Don't: Duplicate Linked Data

```yaml
# BAD - Manually copying data
- fieldname: "service_provider"
  fieldtype: "Link"
  options: "Service Provider"

- fieldname: "provider_name"
  fieldtype: "Data"
  # User has to type this manually!
```

```yaml
# GOOD - Auto-fetch
- fieldname: "service_provider"
  fieldtype: "Link"
  options: "Service Provider"

- fieldname: "provider_name"
  fieldtype: "Data"
  read_only: true
  fetch_from: "service_provider.provider_name"
```

### ❌ Don't: Use Generic Field Names

```yaml
# BAD
- fieldname: "name"  # Conflicts with system
- fieldname: "data"  # Too generic
- fieldname: "field1"  # Meaningless
```

```yaml
# GOOD
- fieldname: "provider_name"
- fieldname: "service_type"
- fieldname: "contact_email"
```

### ❌ Don't: Create Flat Structures

```yaml
# BAD - No sections
fields:
  - fieldname: "provider_name"
  - fieldname: "hp_number"
  - fieldname: "email"
  - fieldname: "phone"
  - fieldname: "status"
  # ... 20 more fields in one long list
```

```yaml
# GOOD - Organized sections
fields:
  - fieldname: "basic_section"
    fieldtype: "Section Break"
  - fieldname: "provider_name"
  - fieldname: "hp_number"

  - fieldname: "contact_section"
    fieldtype: "Section Break"
  - fieldname: "email"
  - fieldname: "phone"
```

### ❌ Don't: Over-Normalize

```yaml
# BAD - Too complex for simple case
- fieldname: "country"
  fieldtype: "Link"
  options: "Country"  # Overkill if only Israel
```

```yaml
# GOOD - Simple for limited options
- fieldname: "country"
  fieldtype: "Select"
  options: "Israel\nUSA\nUK"
  default: "Israel"
```

### ❌ Don't: Forget Permissions

```yaml
# BAD - No permissions defined
doctype:
  name: "My DocType"
  fields: [...]
  # Missing permissions!
```

```yaml
# GOOD
doctype:
  name: "My DocType"
  fields: [...]
  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
```

## Checklist for New DocTypes

Before finalizing a DocType design, verify:

- [ ] DocType name is clear and singular
- [ ] All fieldnames are snake_case
- [ ] All labels are in Hebrew
- [ ] Required fields are marked `reqd: true`
- [ ] Identifier fields are marked `unique: true`
- [ ] Fields are organized into logical sections
- [ ] 3-5 fields selected for list view
- [ ] Important fields added to standard filters
- [ ] Link fields have correct `options`
- [ ] Select fields have Hebrew options
- [ ] Date fields have sensible defaults
- [ ] Fetched fields are read_only
- [ ] Permissions defined for all relevant roles
- [ ] Naming rule is appropriate
- [ ] Track changes enabled if needed
- [ ] Description added to DocType

## Additional Resources

- See example YAML files in `templates/examples/`
- Frappe documentation: https://frappeframework.com/docs
- Project-specific patterns in CLAUDE.md
- Workflow implementation guide in workflow-implementation-plan.md

## Questions?

When in doubt:
1. Look at existing DocTypes in the system
2. Check example YAML files
3. Start simple and iterate
4. Test with real data early
5. Get user feedback

Remember: **Perfect is the enemy of good. Ship a working v1, then improve.**
