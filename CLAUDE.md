# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a **Frappe Framework** implementation for a Nursing Management System (אגף סיעוד) for Israel's nursing care administration. This is a fresh POC (Proof of Concept) starting point for implementing service provider management, caregiver tracking, contracts, document approvals, and workflow automation.

**Framework:** Frappe Framework v15 (Low-code, metadata-driven platform)
**Environment:** Docker-based development with frappe_docker
**Primary App:** `siud` (custom Frappe app for Supplier Inquiry and User management/Nursing Management)
**Language:** Python 3.10+, JavaScript (Node.js 16+)
**UI Language:** Hebrew (RTL interface)

**Current Status:** Fresh POC start - core DocTypes and workflows are to be implemented

## Quick Reference

### Running DocType Creation Scripts

**From Host Machine (Recommended):**
```bash
./run_doctype_script.sh <subdirectory.module.function>

# Examples:
./run_doctype_script.sh creation.create_supplier_inquiry_workflow.create_all
./run_doctype_script.sh creation.create_all_entities.create_all_doctypes
./run_doctype_script.sh test_data.create_test_data.load_test_data
./run_doctype_script.sh temp.verify_workflow.verify
```

**Direct Command (from host or inside container):**
```bash
# Inside container
bench --site development.localhost execute siud.doctypes_loading.<subdirectory>.<module>.<function>

# From host
docker exec frappe_docker_devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && \
   bench --site development.localhost execute siud.doctypes_loading.<subdirectory>.<module>.<function>"
```

**Command Pattern:**
- **App:** `siud` (constant)
- **Module Path:** `doctypes_loading` (constant)
- **Subdirectory:** `creation`, `test_data`, or `temp`
- **Variable:** `<subdirectory>.<module>.<function>` (e.g., `creation.create_supplier_inquiry_workflow.create_all`)

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

### DocTypes Loading Directory Mount

The `doctypes_loading/` directory from the host is mounted into the container for programmatic DocType creation:

- **Host path:** `/home/tzvi/frappe/doctypes_loading/`
- **Container path:** `/workspace/development/frappe-bench/apps/siud/siud/doctypes_loading/`
- **Purpose:** Version-controlled DocType creation scripts that can be executed via `bench execute`

**Directory Structure:**
```
doctypes_loading/
├── creation/          # Production DocType and workflow creation scripts
├── test_data/         # Test data loading scripts
├── temp/              # Temporary/debugging utility scripts
├── README.md          # Complete documentation
└── QUICK_START.md     # Step-by-step setup guide
```

This mounting enables:
1. Edit scripts on host with any IDE
2. Execute scripts inside container with Frappe context
3. Version control DocType schemas as code
4. Reproducible environment setup
5. Organized separation of creation, test data, and utility scripts

### Common Development Commands

```bash
# Inside container at /workspace/development/frappe-bench

# Environment constants (for reference)
SITE="development.localhost"
APP="siud"

# List installed apps
bench --site development.localhost list-apps

# Clear cache (run after DocType changes)
bench --site development.localhost clear-cache

# Run database migrations
bench --site development.localhost migrate

# Build frontend assets
bench build --app siud

# Access Python console (for testing/debugging)
bench --site development.localhost console

# Start development server (auto-reload)
bench start

# Execute Python scripts from doctypes_loading/
# Pattern: bench --site <SITE> execute <APP>.doctypes_loading.<subdirectory>.<script>.<function>
bench --site development.localhost execute siud.doctypes_loading.creation.create_supplier_inquiry_workflow.create_all
```

### Command Shortcuts and Aliases

To minimize variation between commands and make them more abstract, you can create shell aliases or helper scripts:

**Option 1: Shell Aliases (inside container)**
```bash
# Add to ~/.bashrc or run directly in container shell
alias bench-exec='bench --site development.localhost execute siud.doctypes_loading'

# Usage becomes much simpler:
bench-exec creation.create_supplier_inquiry_workflow.create_all
bench-exec creation.create_all_entities.create_all_doctypes
bench-exec test_data.create_test_data.load_test_data
bench-exec temp.verify_workflow.verify
```

**Option 2: Helper Script (Included)**
A helper script is provided at `/home/tzvi/frappe/run_doctype_script.sh` that abstracts away the container and path details:
```bash
#!/bin/bash
# Usage: ./run_doctype_script.sh <subdirectory.module.function>
# Example: ./run_doctype_script.sh creation.create_supplier_inquiry_workflow.create_all

SITE="development.localhost"
APP="siud"
MODULE_PATH="doctypes_loading"

if [ -z "$1" ]; then
    echo "Usage: $0 <subdirectory.module.function>"
    echo "Example: $0 creation.create_supplier_inquiry_workflow.create_all"
    exit 1
fi

bench --site "$SITE" execute "$APP.$MODULE_PATH.$1"
```

Usage from host machine:
```bash
# From /home/tzvi/frappe/
./run_doctype_script.sh creation.create_supplier_inquiry_workflow.create_all
./run_doctype_script.sh creation.create_all_entities.create_all_doctypes
./run_doctype_script.sh test_data.create_test_data.load_test_data
./run_doctype_script.sh temp.verify_workflow.verify

# Get help
./run_doctype_script.sh --help
```

The script automatically handles:
- Docker container execution
- Correct working directory
- Full module path construction (including subdirectory)
- Success/failure feedback
- Reminder to clear cache

**Option 3: Python Wrapper**
Create `doctypes_loading/run.py` with a CLI:
```python
import frappe
import click

@click.command()
@click.argument('action')
def run(action):
    """Run DocType creation scripts"""
    # Maps simple names to full module paths
    actions = {
        'create-all': 'siud.doctypes_loading.creation.create_supplier_inquiry_workflow.create_all',
        'delete-all': 'siud.doctypes_loading.creation.create_supplier_inquiry_workflow.delete_all',
        'load-test-data': 'siud.doctypes_loading.test_data.create_test_data.load_test_data',
        'verify': 'siud.doctypes_loading.temp.verify_workflow.verify',
        # Add more mappings as needed
    }

    if action in actions:
        frappe.init(site='development.localhost')
        frappe.connect()
        frappe.execute_cmd(actions[action])
    else:
        print(f"Unknown action: {action}")
        print(f"Available actions: {', '.join(actions.keys())}")

if __name__ == '__main__':
    run()
```

### Accessing the Application

- **Web Interface:** http://localhost:8000
- **Login:** Administrator / (admin password)
- **DocType Management:** Desk → Developer → DocType

## Project Architecture

### Repository Structure

```
/home/tzvi/frappe/
├── frappe_docker/              # Frappe Docker infrastructure (upstream)
│   ├── development/            # Development workspace
│   │   └── frappe-bench/      # Frappe bench installation
│   │       ├── apps/
│   │       │   ├── frappe/    # Core framework
│   │       │   ├── erpnext/   # ERPNext (if installed)
│   │       │   └── siud/      # Custom POC app (Supplier Inquiry & User Data/Nursing)
│   │       └── sites/
│   │           └── development.localhost/
│   └── docs/                  # Docker setup documentation
├── doctype_creator/           # Legacy utility tools for DocType creation
├── doctypes_loading/          # DocType creation scripts (mounted into container)
│   ├── creation/              # Production creation scripts
│   ├── test_data/             # Test data loading scripts
│   ├── temp/                  # Temporary/debugging utilities
│   ├── README.md              # Complete documentation
│   └── QUICK_START.md         # Step-by-step setup guide
├── run_doctype_script.sh      # Helper script to run DocType scripts with minimal variation
├── .claude/                   # Claude Code configuration
└── CLAUDE.md                  # This file - project documentation
```

### SIUD App Structure

```
/workspace/development/frappe-bench/apps/siud/
├── siud/
│   ├── siud/                        # Main module
│   │   ├── doctype/                # DocTypes directory
│   │   │   └── (DocTypes are created here programmatically or via UI)
│   │   ├── doctypes_loading/       # Mounted from host - DocType creation scripts
│   │   │   ├── creation/           # Production creation scripts
│   │   │   ├── test_data/          # Test data loading scripts
│   │   │   ├── temp/               # Temporary/debugging utilities
│   │   │   ├── README.md           # Complete documentation
│   │   │   └── QUICK_START.md      # Step-by-step setup guide
│   │   └── config/
│   ├── hooks.py               # App lifecycle hooks
│   ├── modules.txt
│   └── public/               # Static assets
├── setup.py
└── requirements.txt
```

**Note:** DocTypes are created during development either via Frappe UI or programmatically. Each DocType will have its own subdirectory containing:
- `<doctype_name>.json` - Schema definition
- `<doctype_name>.py` - Python controller (business logic)
- `<doctype_name>.js` - Client-side JavaScript (optional)

## Core DocTypes (Entities)

The following DocTypes are planned for implementation as part of the Nursing Management System POC:

### Planned Core Entities

1. **Service Provider** (`service_provider`)
   - Primary Key: `hp_number` (מספר ח"פ - 9 digits)
   - Manages service provider master data
   - Auto-naming: `SP-.####`
   - Status: To be implemented

2. **Service Provider Branch** (`service_provider_branch`)
   - Links to Service Provider
   - Branch code: 2-digit code
   - Auto-naming: `SPB-.####`
   - Status: To be implemented

3. **Contract** (`contract`)
   - Links to Service Provider Branch
   - Tracks contract validity and expiry
   - Auto-naming: `CON-.####`
   - Status: To be implemented

4. **Document Approval** (`document_approval`)
   - Links to Contract
   - Manages required documents (insurance, permits, etc.)
   - Status tracking: חסר, הוגש, תקין, לא תקין
   - Auto-naming: `DOC-.####`
   - Status: To be implemented

5. **Caregiver** (`caregiver`)
   - Primary Key: `id_number` (תעודת זהות)
   - Includes Employment History child table
   - Auto-naming: `CG-.####`
   - Status: To be implemented

6. **Service Provider Application** (`service_provider_application`)
   - Workflow-based DocType for onboarding new providers
   - Auto-naming: `SPA-.#####`
   - 7 workflow states, 8 transitions
   - Status: To be implemented

7. **Application Document Checklist** (`application_document_checklist`)
   - Child table for Service Provider Application
   - Tracks document submission status
   - Status: To be implemented

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

**Method 2: Python Code (in bench console or custom scripts)**
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

**Method 3: Programmatic Creation via bench execute (Recommended for bulk operations)**

For creating multiple related DocTypes, use Python scripts in the `doctypes_loading/` directory. This approach is ideal for:
- Creating entire entity sets at once
- Version-controlled DocType definitions
- Reproducible development environments
- Automated setup scripts

**Directory Organization:**

Scripts are organized into subdirectories:
- **`creation/`** - Production DocType and workflow creation scripts
- **`test_data/`** - Test data loading scripts
- **`temp/`** - Temporary/debugging utility scripts

**Setup:**

1. Create Python scripts in `/home/tzvi/frappe/doctypes_loading/<subdirectory>/` directory on the host machine
2. This directory is mounted into the container at `/workspace/development/frappe-bench/apps/siud/siud/doctypes_loading/`
3. Scripts can be executed from the container using `bench execute`

**Command Pattern:**
```bash
# General pattern
bench --site development.localhost execute siud.doctypes_loading.<subdirectory>.<module_name>.<function_name>

# Examples:
# Create Supplier Inquiry workflow system
bench --site development.localhost execute siud.doctypes_loading.creation.create_supplier_inquiry_workflow.create_all

# Create all entities
bench --site development.localhost execute siud.doctypes_loading.creation.create_all_entities.create_all_doctypes

# Load test data
bench --site development.localhost execute siud.doctypes_loading.test_data.create_test_data.load_test_data
```

**Module Path Convention:**
- App name: `siud` (constant across all commands)
- Module path: `doctypes_loading` (constant across all commands)
- Subdirectory: `creation`, `test_data`, or `temp`
- Variable parts: `<subdirectory>.<module_name>.<function_name>`

**Example Script Structure:**
```python
# /home/tzvi/frappe/doctypes_loading/creation/create_my_doctype.py
import frappe

@frappe.whitelist()
def create_my_doctype():
    """Create a custom DocType programmatically"""

    doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'My Custom DocType',
        'module': 'Siud',
        'autoname': 'format:MYDT-{####}',
        'fields': [
            {
                'fieldname': 'title',
                'fieldtype': 'Data',
                'label': 'כותרת',
                'reqd': 1
            }
        ]
    })

    doc.insert()
    frappe.db.commit()
    frappe.msgprint(f"✓ Created {doc.name}")

    return {"success": True}

# Run with:
# bench --site development.localhost execute siud.doctypes_loading.creation.create_my_doctype.create_my_doctype
```

**Master Script Pattern:**

For complex systems with multiple dependent DocTypes, create a master script that:
1. Imports individual creation functions
2. Executes them in dependency order
3. Provides status feedback

**Primary Master Scripts:**
- `doctypes_loading/creation/create_supplier_inquiry_workflow.py` - Complete Supplier Inquiry system
- `doctypes_loading/creation/create_all_entities.py` - All core DocTypes

**Quick Start from Zero:**
See `doctypes_loading/QUICK_START.md` for step-by-step guide to rebuild the entire system.

**Advantages:**
- Version control for DocType schemas
- Repeatable setup across environments
- Easy to reset and rebuild during POC phase
- Can include data validation and relationships
- Single command to create entire entity sets

**After Running:**
```bash
# Always clear cache and migrate after creating DocTypes
bench --site development.localhost clear-cache
bench --site development.localhost migrate
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

### Service Provider Application Workflow (Planned)

**Workflow States:**
1. Draft (טיוטה/הגשה ראשונית)
2. HQ_Check (בדיקת מטה)
3. Data_Review (בדיקת נתונים)
4. Agreement_Prep (הכנת הסכם)
5. Final_HQ_Processing (טיפול מטה סופי)
6. Rejected (נדחה)
7. Approved (הסכם התקבל)

**Workflow Transitions:**
- Draft → HQ_Check (Service Provider User)
- HQ_Check → Data_Review (HQ Approver, if valid)
- HQ_Check → Rejected (HQ Approver, if invalid)
- Data_Review → Agreement_Prep (Internal Reviewer, if valid)
- Data_Review → Rejected (Internal Reviewer, if invalid)
- Agreement_Prep → Final_HQ_Processing (Internal Reviewer, if documents accepted)
- Agreement_Prep → Rejected (Internal Reviewer, if documents not accepted)
- Final_HQ_Processing → Approved (HQ Approver, final approval)

**Planned Email Automation:**
- New application notification to HQ
- Rejection notification to applicant
- Documents approved notification
- Final approval notification

**Roles:**
- Service Provider User (external portal user)
- Internal Reviewer (internal staff)
- HQ Approver (management level)

Status: To be implemented

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
Email templates will use Hebrew with HTML formatting when workflows are implemented.

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

### Automated Testing
Custom test scripts can be created in Python using Frappe's test framework or as standalone scripts in the `doctypes_loading/test_data/` or `doctypes_loading/temp/` directories. These scripts can be executed using the `bench execute` command pattern described above.

**Example test/verification scripts:**
- `doctypes_loading/temp/verify_workflow.py` - Verify workflow configuration
- `doctypes_loading/temp/inspect_supplier_inquiry.py` - Inspect Supplier Inquiry DocType
- `doctypes_loading/test_data/create_test_data.py` - Load sample test data

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

External documentation resources:
- `frappe_docker/docs/development.md` - Docker development setup guide
- `frappe_docker/docs/getting-started.md` - Comprehensive Frappe Docker guide
- Official Frappe Framework documentation: https://frappeframework.com/docs

**Note:** Previous implementation documentation has been archived. This is a fresh POC start.

## POC Development Roadmap

### Phase 1: Core Entity Setup
- [ ] Create Service Provider DocType
- [ ] Create Service Provider Branch DocType
- [ ] Implement HP number validation
- [ ] Set up basic relationships

### Phase 2: Contract Management
- [ ] Create Contract DocType
- [ ] Create Document Approval DocType
- [ ] Implement date validations
- [ ] Set up document tracking

### Phase 3: Caregiver Management
- [ ] Create Caregiver DocType
- [ ] Create Employment History child table
- [ ] Implement Israeli ID validation

### Phase 4: Workflow Implementation
- [ ] Create Service Provider Application DocType
- [ ] Set up workflow states and transitions
- [ ] Configure role-based permissions
- [ ] Implement email notifications

### Phase 5: Testing and Refinement
- [ ] End-to-end testing
- [ ] UI/UX improvements
- [ ] Hebrew translation verification
- [ ] Performance optimization

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
