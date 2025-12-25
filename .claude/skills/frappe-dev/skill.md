# Frappe Framework Development Skill

**Trigger:** Use this skill whenever working with Frappe Framework, DocTypes, service providers, caregivers, contracts, or the Nursing Management System (Siud app).

**Project Type:** Frappe Framework v15 POC for Israel's Nursing Management System (אגף סיעוד)

## Quick Start

This skill includes all necessary helper scripts. To set up:

```bash
# From project root
.claude/skills/frappe-dev/setup.sh
```

This will make all scripts executable and optionally create symlinks in your project root.

### Available Helper Scripts

All scripts are located in `.claude/skills/frappe-dev/`:

| Script | Purpose | Usage |
|--------|---------|-------|
| `run_doctype_script.sh` | Execute DocType creation scripts | `./run_doctype_script.sh creation.module.function` |
| `clear_cache.sh` | Clear Frappe cache (run after DocType changes) | `./clear_cache.sh` |
| `migrate.sh` | Run database migrations (run after JSON changes) | `./migrate.sh` |
| `console.sh` | Open Python console for testing | `./console.sh` |
| `setup.sh` | Initial setup - make scripts executable | `./setup.sh` |

## Critical Context

- **Framework:** Frappe Framework v15 (metadata-driven, low-code platform)
- **Environment:** Docker-based with frappe_docker
- **Primary App:** `siud` (Supplier Inquiry & User Data / Nursing Management)
- **Language:** Python 3.10+, JavaScript (Node.js 16+)
- **UI Language:** Hebrew (RTL interface - all labels must be in Hebrew)
- **Database:** Metadata-driven schema via JSON files

## Container & Environment Setup

### Docker Container Access
```bash
# Primary development container
docker exec -it frappe_docker_devcontainer-frappe-1 bash

# Always work from bench directory inside container
cd /workspace/development/frappe-bench

# Site name (constant)
development.localhost
```

**CRITICAL:** All bench commands must run from `/workspace/development/frappe-bench` inside the container.

### Key Paths

| Location | Host Path | Container Path |
|----------|-----------|----------------|
| DocTypes Loading Scripts | `/home/tzvi/frappe/doctypes_loading/` | `/workspace/development/frappe-bench/apps/siud/siud/doctypes_loading/` |
| SIUD App | N/A | `/workspace/development/frappe-bench/apps/siud/` |
| Frappe Bench | N/A | `/workspace/development/frappe-bench/` |

## DocType Creation - Three Methods

### Method 1: Programmatic Creation via Scripts (RECOMMENDED for bulk operations)

**Use when:** Creating multiple related DocTypes, need version control, reproducible setup

**Command Pattern:**
```bash
# From project root (if you ran setup.sh with symlinks)
./run_doctype_script.sh <subdirectory>.<module>.<function>

# Or use full path from anywhere
.claude/skills/frappe-dev/run_doctype_script.sh <subdirectory>.<module>.<function>

# Examples:
./run_doctype_script.sh creation.create_supplier_inquiry_workflow.create_all
./run_doctype_script.sh creation.create_all_entities.create_all_doctypes
./run_doctype_script.sh test_data.create_test_data.load_test_data
./run_doctype_script.sh temp.verify_workflow.verify
```

**Direct Command (from container or host):**
```bash
# From inside container
bench --site development.localhost execute siud.doctypes_loading.<subdirectory>.<module>.<function>

# From host via docker exec
docker exec frappe_docker_devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && \
   bench --site development.localhost execute siud.doctypes_loading.<subdirectory>.<module>.<function>"
```

**Module Path Convention:**
- App: `siud` (constant)
- Module: `doctypes_loading` (constant)
- Subdirectories:
  - `creation/` - Production DocType and workflow creation
  - `test_data/` - Test data loading
  - `temp/` - Temporary/debugging utilities

**Script Structure Example:**
```python
# /home/tzvi/frappe/doctypes_loading/creation/create_my_doctype.py
import frappe

@frappe.whitelist()
def create_my_doctype():
    """Create a custom DocType programmatically"""

    doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'My DocType Name',
        'module': 'Siud',
        'autoname': 'format:PREFIX-{####}',
        'fields': [
            {
                'fieldname': 'field_name',
                'fieldtype': 'Data',
                'label': 'תווית בעברית',  # Hebrew label required
                'reqd': 1
            }
        ]
    })

    doc.insert()
    frappe.db.commit()
    frappe.msgprint(f"✓ Created {doc.name}")

    return {"success": True}
```

**After running scripts, ALWAYS:**
```bash
# Option 1: Use helper scripts (recommended)
./clear_cache.sh
./migrate.sh

# Option 2: Direct commands in container
bench --site development.localhost clear-cache
bench --site development.localhost migrate
```

### Method 2: Frappe UI

**Use when:** Creating single DocType, quick prototyping, visual design

1. Navigate to http://localhost:8000
2. Go to: Developer → DocType → New
3. Fill fields and save
4. System auto-generates JSON and Python files

### Method 3: Python Console

**Use when:** Quick testing, debugging, one-off operations

```bash
bench --site development.localhost console

# Inside Python console
import frappe
frappe.connect()

doc = frappe.get_doc({
    'doctype': 'DocType',
    'name': 'My DocType',
    'module': 'Siud',
    'fields': [
        {'fieldname': 'field1', 'fieldtype': 'Data', 'label': 'שדה 1'}
    ]
})
doc.insert()
frappe.db.commit()
```

## Core DocTypes in This System

### Implemented/Planned Entities

1. **Service Provider** (`service_provider`)
   - Primary Key: `hp_number` (מספר ח"פ - 9 digits)
   - Auto-naming: `SP-.####`
   - Validation: Exactly 9 digits, unique

2. **Service Provider Branch** (`service_provider_branch`)
   - Links to Service Provider
   - Branch code: 2-digit (e.g., "01", "15")
   - Auto-naming: `SPB-.####`

3. **Contract** (`contract`)
   - Links to Service Provider Branch
   - Date validations: end > start
   - Auto-naming: `CON-.####`

4. **Document Approval** (`document_approval`)
   - Links to Contract
   - Status: חסר, הוגש, תקין, לא תקין
   - Auto-naming: `DOC-.####`

5. **Caregiver** (`caregiver`)
   - Primary Key: `id_number` (Israeli ID)
   - Israeli ID validation algorithm required
   - Child table: Employment History
   - Auto-naming: `CG-.####`

6. **Service Provider Application** (`service_provider_application`)
   - Workflow-based onboarding
   - Auto-naming: `SPA-.#####`
   - 7 workflow states, 8 transitions

7. **Application Document Checklist** (`application_document_checklist`)
   - Child table for Service Provider Application

## Workflow System

### Service Provider Application Workflow

**States:**
1. Draft (טיוטה/הגשה ראשונית)
2. HQ_Check (בדיקת מטה)
3. Data_Review (בדיקת נתונים)
4. Agreement_Prep (הכנת הסכם)
5. Final_HQ_Processing (טיפול מטה סופי)
6. Rejected (נדחה)
7. Approved (הסכם התקבל)

**Key Transitions:**
- Draft → HQ_Check (Service Provider User)
- HQ_Check → Data_Review/Rejected (HQ Approver)
- Data_Review → Agreement_Prep/Rejected (Internal Reviewer)
- Agreement_Prep → Final_HQ_Processing/Rejected (Internal Reviewer)
- Final_HQ_Processing → Approved (HQ Approver)

**Roles:**
- Service Provider User (external portal)
- Internal Reviewer (staff)
- HQ Approver (management)

### Creating Workflows and Workspaces Programmatically

**CRITICAL:** Workflows and Workspaces have specific requirements for successful programmatic creation.

**📖 See `TESTED_PATTERNS.md` for production-tested working patterns**

**Quick Reference:**

**Workflows - Common Pitfalls:**
- ✗ Using `'doc_status': 0` (int) → ✓ Use `'doc_status': '0'` (string)
- ✗ Using `workflow.append('states', ...)` → ✓ Include all states/transitions in initial `frappe.get_doc()` dict
- ✗ State name mismatches → ✓ Ensure exact match between states and transitions

**Workspaces - Common Pitfalls:**
- ✗ Not setting `name` field → ✓ Set both `"name"` and `"label"` explicitly
- ✗ Missing metadata → ✓ Include `creation`, `modified`, `owner`, `modified_by`
- ✗ Not clearing cache → ✓ Run `frappe.clear_cache()` after creation

**Working Examples:**
- Workflow: `doctypes_loading/creation/create_supplier_inquiry_workflow.py`
- Workspace: `doctypes_loading/creation/create_siud_workspace_complete.py`

## Python Controllers

Controllers define business logic and validations:

```python
# Example: apps/siud/siud/doctype/service_provider/service_provider.py
import frappe
from frappe.model.document import Document

class ServiceProvider(Document):
    def validate(self):
        """Runs before save"""
        self.validate_hp_number()

    def validate_hp_number(self):
        """Validate 9-digit HP number"""
        if not self.hp_number or len(self.hp_number) != 9:
            frappe.throw('HP number must be 9 digits')

    def before_insert(self):
        """Before first save"""
        pass

    def after_insert(self):
        """After first save"""
        pass

    def on_update(self):
        """After any update"""
        pass
```

**Key Lifecycle Methods:**
- `validate()` - Before save validation
- `before_insert()` - Before first save
- `after_insert()` - After first save
- `on_update()` - After any update
- `on_submit()` - When submitted (if submittable)
- `on_cancel()` - When cancelled

## Hebrew (RTL) Requirements

**CRITICAL:** All user-facing text must be in Hebrew.

### Field Labels
```json
{
    "fieldname": "provider_name",
    "label": "שם נותן השירות",  // Hebrew required
    "fieldtype": "Data"
}
```

### Select Options
```json
{
    "fieldname": "service_type",
    "options": "טיפול בבית\nמרכז יום\nקהילה תומכת\nמוצרי ספיגה"
}
```

### Workflow State Labels
Use Hebrew for all state and transition labels.

## Common Development Commands

```bash
# Inside container at /workspace/development/frappe-bench

# List apps
bench --site development.localhost list-apps

# Clear cache (REQUIRED after DocType changes)
bench --site development.localhost clear-cache

# Run migrations (REQUIRED after JSON changes)
bench --site development.localhost migrate

# Build frontend
bench build --app siud

# Start dev server
bench start

# Python console
bench --site development.localhost console

# Execute script
bench --site development.localhost execute siud.doctypes_loading.creation.module.function
```

## Validation Patterns

### HP Number (9 digits)
```python
def validate_hp_number(self):
    if not self.hp_number or len(self.hp_number) != 9:
        frappe.throw('מספר ח"פ חייב להיות 9 ספרות')
    if not self.hp_number.isdigit():
        frappe.throw('מספר ח"פ חייב להכיל ספרות בלבד')
```

### Israeli ID Validation
```python
def validate_israeli_id(id_number):
    """Israeli ID check-digit algorithm"""
    if not id_number or len(id_number) != 9:
        return False

    total = 0
    for i, digit in enumerate(id_number):
        num = int(digit) * ((i % 2) + 1)
        total += num if num < 10 else num - 9

    return total % 10 == 0
```

### Date Validations
```python
def validate(self):
    if self.end_date and self.start_date:
        if self.end_date < self.start_date:
            frappe.throw('תאריך סיום חייב להיות אחרי תאריך התחלה')
```

## Auto-Naming Patterns

All DocTypes use Frappe's autoname field:
```json
{
    "autoname": "format:SP-{####}"
}
```

**Common Patterns:**
- `SP-.####` → SP-0001
- `SPA-.#####` → SPA-00001
- `CON-.####` → CON-0001

## Testing Approaches

### Console Testing
```bash
# Option 1: Use helper script (recommended)
./console.sh

# Option 2: Direct command
bench --site development.localhost console

# Inside Python console
import frappe
frappe.connect()

# Create test record
doc = frappe.get_doc({
    'doctype': 'Service Provider',
    'provider_name': 'מרכז סיעודי השרון',
    'hp_number': '123456789'
})
doc.insert()
frappe.db.commit()

# Query records
providers = frappe.get_all('Service Provider',
                          fields=['name', 'provider_name'])
print(providers)
```

### Test Data Scripts
```bash
# Load test data
./run_doctype_script.sh test_data.create_test_data.load_test_data
```

### Verification Scripts
```bash
# Run verification
./run_doctype_script.sh temp.verify_workflow.verify
```

## Common Pitfalls & Solutions

| Pitfall | Solution |
|---------|----------|
| DocType changes not visible | Run `bench clear-cache` |
| Bench commands fail | Ensure working directory is `/workspace/development/frappe-bench` |
| JSON changes not applied | Run `bench migrate` |
| HP/ID validation errors | Check exact digit count (9 for both) |
| Hebrew text not displaying | Ensure UTF-8 encoding, check RTL settings |
| Scripts not found | Verify mount path and module path format |
| Permission denied in container | Check docker exec command and working directory |

## Architecture Patterns

### Metadata-Driven Design
- DocType JSON defines: schema, UI, validation, permissions, API
- Changes to JSON → automatic schema updates
- No manual SQL/migrations needed

### Convention Over Configuration
- DocType names: CamelCase (e.g., ServiceProvider)
- Field names: snake_case (e.g., provider_name)
- Controller files: auto-discovered by name
- Module structure: follows Frappe conventions

### Built-in Features
Every DocType automatically includes:
- REST API endpoints (`/api/resource/{doctype}/{name}`)
- List view and form view
- Search and filters
- Permissions system
- Audit trail (created_by, modified_by, versions)
- File attachments
- Comments and timeline
- Email integration
- Print formats

## Child Tables

Used for one-to-many relationships within a document:

```python
# Define child DocType with istable=1
{
    'doctype': 'DocType',
    'name': 'Employment History',
    'istable': 1,  # Mark as child table
    'fields': [...]
}

# Link from parent DocType
{
    'fieldname': 'employment_history',
    'fieldtype': 'Table',
    'options': 'Employment History',
    'label': 'היסטוריית תעסוקה'
}
```

## API Access

Frappe auto-generates REST API:
- Endpoint: `/api/resource/{doctype}/{name}`
- Authentication: API keys or session-based
- Methods: GET, POST, PUT, DELETE
- Filter: `/api/resource/{doctype}?filters=[["field","=","value"]]`

## Best Practices

1. **Always use Hebrew labels** for all user-facing text
2. **Clear cache after DocType changes** - critical step
3. **Version control scripts** in `doctypes_loading/` directory
4. **Use helper script** `./run_doctype_script.sh` to minimize command variation
5. **Validate HP numbers** - exactly 9 digits
6. **Validate Israeli IDs** - use check-digit algorithm
7. **Test in console** before creating bulk data
8. **Use subdirectories** to organize scripts (creation/test_data/temp)
9. **Run migrations** after JSON modifications
10. **Check working directory** before bench commands

## Quick Reference Commands

All commands assume you're in the project root and have run `setup.sh` (or use full paths).

```bash
# === Setup (run once) ===
.claude/skills/frappe-dev/setup.sh

# === DocType Creation ===
./run_doctype_script.sh creation.create_all_entities.create_all_doctypes
./run_doctype_script.sh creation.create_supplier_inquiry_workflow.create_all

# === Test Data ===
./run_doctype_script.sh test_data.create_test_data.load_test_data

# === Verification ===
./run_doctype_script.sh temp.verify_workflow.verify

# === Maintenance (run after DocType changes) ===
./clear_cache.sh
./migrate.sh

# === Development ===
./console.sh  # Python console for testing

# === Alternative: Direct docker exec commands ===
docker exec frappe_docker_devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && bench --site development.localhost clear-cache"
```

## Resources

- Web Interface: http://localhost:8000
- Login: Administrator / (admin password)
- DocType Management: Desk → Developer → DocType
- Frappe Docs: https://frappeframework.com/docs
- Frappe Forum: https://discuss.frappe.io
- GitHub: https://github.com/frappe/frappe

## AI Agent Instructions

When working with this Frappe project:

1. **Always invoke this skill** when dealing with DocTypes, workflows, or Frappe-specific tasks
2. **Use helper scripts** - All scripts are in `.claude/skills/frappe-dev/`:
   - `run_doctype_script.sh` - Execute DocType scripts
   - `clear_cache.sh` - Clear cache after changes
   - `migrate.sh` - Run migrations after JSON changes
   - `console.sh` - Open Python console
3. **Remember Hebrew requirement** - all labels must be in Hebrew
4. **Don't forget cache clearing** - run `./clear_cache.sh` after DocType changes
5. **Check container paths** - bench commands must run from correct directory
6. **Follow naming conventions** - DocTypes in CamelCase, fields in snake_case
7. **Use programmatic creation** for bulk operations and version control
8. **Test in console first** - use `./console.sh` before bulk operations
9. **Validate business rules** - HP numbers (9 digits), Israeli IDs (check-digit)
10. **Organize scripts** - use creation/test_data/temp subdirectories appropriately

## Module Path Reference

**Constant Parts (never change):**
- App: `siud`
- Module: `doctypes_loading`
- Site: `development.localhost`

**Variable Parts:**
- Subdirectory: `creation`, `test_data`, or `temp`
- Module name: Python file name (without .py)
- Function name: Function to execute

**Full Pattern:**
```
siud.doctypes_loading.<subdirectory>.<module_name>.<function_name>
```

**Examples:**
- `siud.doctypes_loading.creation.create_supplier_inquiry_workflow.create_all`
- `siud.doctypes_loading.test_data.create_test_data.load_test_data`
- `siud.doctypes_loading.temp.verify_workflow.verify`
