# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a **Frappe Framework** implementation for a Nursing Management System (אגף סיעוד) for Israel's nursing care administration. The project implements service provider management, caregiver tracking, contracts, document approvals, and workflow automation.

**Framework:** Frappe Framework v15 (Low-code, metadata-driven platform)
**Environment:** Docker-based development with frappe_docker
**Primary App:** `nursing_management` (custom Frappe app)
**Language:** Python 3.10+, JavaScript (Node.js 16+)
**UI Language:** Hebrew (RTL interface)

## Development Environment

### Container Access

The development environment runs in Docker containers:

```bash
# Primary development container
docker exec -it frappe_docker_devcontainer-frappe-1 bash

# Bench location inside container
cd /workspace/development/frappe-bench

# Site name
development.localhost
```

**IMPORTANT:** Always run bench commands from `/workspace/development/frappe-bench` directory inside the container.

### Common Development Commands

```bash
# Inside container at /workspace/development/frappe-bench

# List installed apps
bench --site development.localhost list-apps

# Clear cache (run after DocType changes)
bench --site development.localhost clear-cache

# Run database migrations
bench --site development.localhost migrate

# Build frontend assets
bench build --app nursing_management

# Access Python console (for testing/debugging)
bench --site development.localhost console

# Start development server (auto-reload)
bench start
```

### Accessing the Application

- **Web Interface:** http://localhost:8000
- **Login:** Administrator / (admin password)
- **DocType Management:** Desk → Developer → DocType

## Project Architecture

### Repository Structure

```
C:\dev\btl\frappe\
├── frappe_docker/              # Frappe Docker infrastructure (upstream)
│   ├── development/            # Development workspace
│   │   └── frappe-bench/      # Frappe bench installation
│   │       ├── apps/
│   │       │   ├── frappe/    # Core framework
│   │       │   ├── erpnext/   # ERPNext (if needed)
│   │       │   └── nursing_management/  # POC app
│   │       └── sites/
│   │           └── development.localhost/
│   └── docs/                  # Docker setup docs
├── *.py                       # Helper scripts for DocType creation
├── *_controller.py            # Python controller implementations
├── *.md                       # Project documentation
└── workflow-implementation-plan.md  # Detailed workflow specs
```

### Nursing Management App Structure

```
/workspace/development/frappe-bench/apps/nursing_management/
├── nursing_management/
│   ├── nursing_management/          # Main module
│   │   ├── doctype/                # DocTypes directory
│   │   │   ├── service_provider/
│   │   │   │   ├── service_provider.json    # Schema definition
│   │   │   │   ├── service_provider.py      # Business logic
│   │   │   │   └── service_provider.js      # Client-side logic
│   │   │   ├── service_provider_branch/
│   │   │   ├── contract/
│   │   │   ├── document_approval/
│   │   │   ├── caregiver/
│   │   │   └── service_provider_application/  # NEW - Workflow DocType
│   │   └── config/
│   ├── hooks.py               # App lifecycle hooks
│   ├── modules.txt
│   └── public/               # Static assets
├── setup.py
└── requirements.txt
```

## Core DocTypes (Entities)

### Implemented DocTypes

1. **Service Provider** (`service_provider`)
   - Primary Key: `hp_number` (מספר ח"פ - 9 digits)
   - Manages service provider master data
   - Auto-naming: `SP-.####`

2. **Service Provider Branch** (`service_provider_branch`)
   - Links to Service Provider
   - Branch code: 2-digit code
   - Auto-naming: `SPB-.####`

3. **Contract** (`contract`)
   - Links to Service Provider Branch
   - Tracks contract validity and expiry
   - Auto-naming: `CON-.####`

4. **Document Approval** (`document_approval`)
   - Links to Contract
   - Manages required documents (insurance, permits, etc.)
   - Status tracking: חסר, הוגש, תקין, לא תקין
   - Auto-naming: `DOC-.####`

5. **Caregiver** (`caregiver`)
   - Primary Key: `id_number` (תעודת זהות)
   - Includes Employment History child table
   - Auto-naming: `CG-.####`

6. **Application Document Checklist** (`application_document_checklist`)
   - Child table for Service Provider Application
   - Tracks document submission status

### Planned/In Progress

7. **Service Provider Application** (`service_provider_application`)
   - NEW workflow-based DocType for onboarding new providers
   - Auto-naming: `SPA-.#####`
   - 7 workflow states, 8 transitions
   - See: `workflow-implementation-plan.md` for full specs

## Key Business Rules

### HP Number Validation
- Must be exactly 9 digits
- Unique within Service Provider DocType
- Python validation in controller files

### ID Number Validation (Israeli ID)
- Must pass Israeli ID check-digit algorithm
- Used for Caregiver DocType

### Branch Code Format
- Exactly 2 digits (e.g., "01", "15")
- Enforced in Service Provider Branch

### Date Validations
- Contract end date must be after start date
- Document expiry tracking with alerts

### Auto-Naming Patterns
All DocTypes use Frappe's auto-naming feature:
- Format: `PREFIX-.####` or `PREFIX-.#####`
- Examples: `SP-0001`, `SPA-00001`

## Working with DocTypes

### Creating DocTypes

**Method 1: Frappe UI (Recommended)**
1. Navigate to: http://localhost:8000
2. Go to: Developer → DocType → New
3. Fill in fields and save
4. System auto-generates JSON and Python files

**Method 2: Helper Scripts (Available in repo root)**
```bash
# Example scripts in C:\dev\btl\frappe\
./create_spa_doctype.py
./create_contract_doctype.py
./create_branch_doctype.py
```

**Method 3: Python Code**
```python
# Inside bench console
import frappe

doc = frappe.get_doc({
    'doctype': 'DocType',
    'name': 'My DocType',
    'module': 'Nursing Management',
    'fields': [
        {'fieldname': 'field1', 'fieldtype': 'Data', 'label': 'Field 1'}
    ]
})
doc.insert()
frappe.db.commit()
```

### Modifying DocTypes

1. Edit via UI or modify `.json` file directly
2. Run migration: `bench --site development.localhost migrate`
3. Clear cache: `bench --site development.localhost clear-cache`

### Python Controllers

Controllers contain business logic and validations:

```python
# Example: service_provider.py
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
```

**Key Controller Methods:**
- `validate()` - Before save validation
- `before_insert()` - Before first save
- `after_insert()` - After first save
- `on_update()` - After any update
- `on_submit()` - When document is submitted (if submittable)
- `on_cancel()` - When document is cancelled

## Workflows

### Service Provider Application Workflow

**States:**
1. Draft (טיוטה/הגשה ראשונית)
2. HQ_Check (בדיקת מטה)
3. Data_Review (בדיקת נתונים)
4. Agreement_Prep (הכנת הסכם)
5. Final_HQ_Processing (טיפול מטה סופי)
6. Rejected (נדחה)
7. Approved (הסכם התקבל)

**Transitions:**
- Draft → HQ_Check (Service Provider User)
- HQ_Check → Data_Review (HQ Approver, if valid)
- HQ_Check → Rejected (HQ Approver, if invalid)
- Data_Review → Agreement_Prep (Internal Reviewer, if valid)
- Data_Review → Rejected (Internal Reviewer, if invalid)
- Agreement_Prep → Final_HQ_Processing (Internal Reviewer, if documents accepted)
- Agreement_Prep → Rejected (Internal Reviewer, if documents not accepted)
- Final_HQ_Processing → Approved (HQ Approver, final approval)

**Email Automation:**
- New application notification to HQ
- Rejection notification to applicant
- Documents approved notification
- Final approval notification

See `workflow-implementation-plan.md` for complete implementation details including:
- Field specifications (45+ fields across 8 sections)
- Role definitions (Service Provider User, Internal Reviewer, HQ Approver)
- Email templates (Hebrew)
- Python controller logic
- JavaScript enhancements

## Hebrew (RTL) Interface

The system is designed for Hebrew users with RTL interface:

### Field Labels
Always use Hebrew labels in DocType definitions:
```json
{
    "fieldname": "provider_name",
    "label": "שם נותן השירות",
    "fieldtype": "Data"
}
```

### Select Options
Use Hebrew for dropdown options:
```json
{
    "fieldname": "service_type",
    "options": "טיפול בבית\nמרכז יום\nקהילה תומכת\nמוצרי ספיגה"
}
```

### Email Templates
Email templates use Hebrew with HTML formatting. See `workflow-implementation-plan.md` sections 3.4 for examples.

## Testing

### Manual Testing via UI
1. Access web interface: http://localhost:8000
2. Navigate to DocType list view
3. Create test records
4. Verify validations and relationships

### Console Testing
```bash
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
providers = frappe.get_all('Service Provider', fields=['name', 'provider_name'])
print(providers)
```

### Automated Test Scripts
Test scripts are available in repo root (e.g., `test_phase2.py`)

## Important Notes

### Database Schema
- Frappe auto-manages database schema from JSON definitions
- Column names follow snake_case convention
- Primary key is always 'name' field (auto or custom)

### Permissions
- Frappe has built-in role-based permission system
- Configure in DocType permissions section
- Portal users (external) have limited access via web portal

### API Access
- Frappe auto-generates REST API for all DocTypes
- Endpoint: `/api/resource/{doctype}/{name}`
- Authentication: API keys or session-based

### Child Tables
- Used for one-to-many relationships within a document
- Example: Employment History is child table of Caregiver
- Defined as separate DocType with `istable = 1`

### Common Pitfalls
1. **Not clearing cache** after DocType changes → Always run `bench clear-cache`
2. **Running bench commands from wrong directory** → Must be in `/workspace/development/frappe-bench`
3. **Forgetting to migrate** after JSON changes → Run `bench migrate`
4. **HP/ID validation errors** → Check exact digit count and format
5. **Hebrew encoding issues** → Ensure UTF-8 encoding in all files

## Additional Documentation

- `workflow-implementation-plan.md` - Complete workflow implementation guide (1400+ lines)
- `workflow-spec.md` - Original Hebrew workflow specification
- `entities-doc.md` - Hebrew entity documentation with semantic metadata
- `frappe-poc-plan.md` - POC implementation plan with phase tracking
- `SERVICE_PROVIDER_APPLICATION_UI_GUIDE.md` - UI creation guide for new DocType
- `frappe_docker/docs/development.md` - Docker development setup guide
- `frappe_docker/docs/getting-started.md` - Comprehensive Frappe Docker guide

## Architecture Patterns

### Metadata-Driven Design
Frappe Framework uses metadata-driven architecture where DocType JSON files define:
- Database schema
- UI form layout
- Validation rules
- Permissions
- API endpoints

This makes it ideal for AI/automation as the semantic meaning is explicitly defined.

### Convention Over Configuration
- DocType names use CamelCase (e.g., ServiceProvider)
- Field names use snake_case (e.g., provider_name)
- Controller files auto-discovered based on DocType name
- Module structure follows standard Frappe conventions

### Built-in Features
Every DocType automatically includes:
- REST API endpoints
- List view and form view
- Search and filters
- Permissions system
- Audit trail (created_by, modified_by, versions)
- File attachments
- Comments and timeline
- Email integration
- Print formats

## Contact and Support

For Frappe Framework documentation:
- Frappe Docs: https://frappeframework.com/docs
- Frappe Forum: https://discuss.frappe.io
- GitHub: https://github.com/frappe/frappe
