# DocType Creator

AI-powered DocType generator for Frappe Framework using YAML specifications.

**Version:** 1.0
**Status:** Production Ready (Sprint 6 Complete)
**Progress:** 100% (6 of 6 sprints completed)

---

## Overview

DocType Creator is a comprehensive system for generating Frappe Framework DocTypes from YAML specifications, with full support for LLM-based generation, validation, loading, and Python controller injection.

### Key Features

✅ **YAML-Based Specifications** - Human and AI-friendly DocType definitions
✅ **Three-Layer Validation** - Schema, business rules, and Frappe compatibility
✅ **Automated Loading** - One-command DocType creation in Frappe
✅ **Controller Injection** - Safe Python controller deployment with backups
✅ **AI Templates** - LLM prompts for natural language DocType generation
✅ **Docker Integration** - Seamless workflow with Frappe Docker environment
✅ **Comprehensive Testing** - 60 passing tests, 100% coverage of core features
✅ **Hebrew Support** - Full RTL interface support for Israeli context

---

## Quick Start

### Prerequisites

- Python 3.10+
- Frappe Docker environment (running)
- Access to Frappe bench directory

### Installation

```bash
cd doctype_creator
pip install -r requirements.txt
```

### Basic Usage

#### 1. Validate a YAML Specification

```bash
# Validate syntax and rules
python validate_yaml.py yaml_specs/service_provider.yaml

# Output:
# SUCCESS - YAML validation passed!
```

#### 2. Load DocType into Frappe

```bash
# From host machine
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/development/frappe-bench && \
  python /workspace/doctype_creator/load_doctype.py \
    /workspace/doctype_creator/yaml_specs/service_provider.yaml && \
  bench --site development.localhost clear-cache
"

# Or use convenience script
./scripts/load.sh yaml_specs/service_provider.yaml
```

#### 3. (Optional) Inject Python Controller

```bash
# After DocType is loaded
./scripts/inject.sh "Service Provider" controllers/service_provider.py

# Or manually
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/doctype_creator && \
  python -m src.controller_injector 'Service Provider' controllers/service_provider.py
"
```

#### 4. Access in Frappe UI

Navigate to: http://localhost:8000

---

## Complete Usage Examples

### Example 1: Create a Simple Master DocType

**Step 1:** Create YAML file `yaml_specs/equipment.yaml`

```yaml
doctype:
  name: "Medical Equipment"
  module: "Nursing Management"
  naming_rule: "autoname"
  autoname: "format:EQ-{#####}"
  track_changes: true
  description: "Medical equipment inventory"

  fields:
    - fieldname: "equipment_name"
      fieldtype: "Data"
      label: "שם ציוד"
      reqd: true
      in_list_view: true

    - fieldname: "equipment_code"
      fieldtype: "Data"
      label: "קוד ציוד"
      unique: true
      in_list_view: true

    - fieldname: "status"
      fieldtype: "Select"
      label: "סטטוס"
      options: "Available\nIn Use\nMaintenance\nRetired"
      default: "Available"
      in_list_view: true

  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
      delete: 1
```

**Step 2:** Validate

```bash
python validate_yaml.py yaml_specs/equipment.yaml
# SUCCESS - YAML validation passed!
```

**Step 3:** Load

```bash
./scripts/load.sh yaml_specs/equipment.yaml
# SUCCESS - DocType loaded successfully!
```

**Step 4:** Access UI

Visit http://localhost:8000/app/medical-equipment

---

### Example 2: Create DocType with Child Table

**Step 1:** Create parent YAML `yaml_specs/training_session.yaml`

```yaml
doctype:
  name: "Training Session"
  module: "Nursing Management"
  naming_rule: "autoname"
  autoname: "format:TRN-{#####}"
  track_changes: true

  fields:
    - fieldname: "session_title"
      fieldtype: "Data"
      label: "כותרת הדרכה"
      reqd: true
      in_list_view: true

    - fieldname: "session_date"
      fieldtype: "Date"
      label: "תאריך"
      reqd: true
      default: "Today"

    - fieldname: "participants_section"
      fieldtype: "Section Break"
      label: "משתתפים"

    - fieldname: "participants"
      fieldtype: "Table"
      label: "רשימת משתתפים"
      options: "Training Participant"

  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
```

**Step 2:** Create child table YAML `yaml_specs/training_participant.yaml`

```yaml
doctype:
  name: "Training Participant"
  module: "Nursing Management"
  naming_rule: "autoname"
  autoname: "format:TP-{#####}"
  is_child_table: true  # Important!

  fields:
    - fieldname: "participant_name"
      fieldtype: "Data"
      label: "שם משתתף"
      reqd: true
      in_list_view: true

    - fieldname: "attended"
      fieldtype: "Check"
      label: "השתתף"
      default: 0

  permissions:
    - role: "System Manager"
      read: 1
      write: 1
```

**Step 3:** Load both (child table first!)

```bash
# Load child table first
./scripts/load.sh yaml_specs/training_participant.yaml

# Then load parent
./scripts/load.sh yaml_specs/training_session.yaml
```

---

### Example 3: Use LLM to Generate YAML

**Step 1:** Copy the LLM prompt template

```bash
cat templates/doctype_generation_prompt.md
# Copy entire content
```

**Step 2:** Provide to LLM with requirement

```
[Paste prompt template]

Now generate a DocType for tracking nursing staff certifications.
It should include: staff member name, certification type,
issue date, expiry date, and certification status.
```

**Step 3:** Save LLM output and validate

```bash
# Save LLM output to yaml_specs/certification.yaml
python validate_yaml.py yaml_specs/certification.yaml
```

**Step 4:** Load if valid

```bash
./scripts/load.sh yaml_specs/certification.yaml
```

---

### Example 4: Add Python Controller with Validation

**Step 1:** Create controller file `controllers/equipment.py`

```python
import frappe
from frappe.model.document import Document

class MedicalEquipment(Document):
    def validate(self):
        """Runs before save"""
        self.validate_equipment_code()
        self.check_duplicate_code()

    def validate_equipment_code(self):
        """Ensure equipment code is uppercase"""
        if self.equipment_code:
            self.equipment_code = self.equipment_code.upper()

    def check_duplicate_code(self):
        """Check for duplicate equipment codes"""
        if self.equipment_code:
            existing = frappe.db.get_value(
                "Medical Equipment",
                {"equipment_code": self.equipment_code, "name": ["!=", self.name]},
                "name"
            )
            if existing:
                frappe.throw(f"Equipment code {self.equipment_code} already exists in {existing}")

    def before_insert(self):
        """Runs before first save"""
        print(f"Creating new equipment: {self.equipment_name}")

    def on_update(self):
        """Runs after any update"""
        if self.status == "Retired":
            self.log_retirement()

    def log_retirement(self):
        """Log equipment retirement"""
        frappe.log_error(
            f"Equipment {self.name} ({self.equipment_name}) retired",
            "Equipment Retirement"
        )
```

**Step 2:** Inject controller

```bash
./scripts/inject.sh "Medical Equipment" controllers/equipment.py

# Output:
# ✓ Controller injected successfully
# Next steps:
#   1. Restart Frappe: bench restart
#   2. Clear cache: bench --site development.localhost clear-cache
```

**Step 3:** Restart and test

```bash
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/development/frappe-bench && \
  bench restart && \
  bench --site development.localhost clear-cache
"
```

---

### Example 5: Iterative Development Workflow

**Scenario:** You need to modify an existing DocType repeatedly during development.

```bash
#!/bin/bash
# iterative_dev.sh - Development workflow script

YAML_FILE="yaml_specs/my_doctype.yaml"

echo "Starting iterative development for $YAML_FILE"

while true; do
  # Wait for user to edit YAML
  read -p "Edit YAML file, then press Enter to reload (or 'q' to quit): " answer

  if [ "$answer" = "q" ]; then
    echo "Exiting"
    break
  fi

  # Validate
  echo "Validating..."
  python validate_yaml.py "$YAML_FILE"
  if [ $? -ne 0 ]; then
    echo "Validation failed! Fix errors and try again."
    continue
  fi

  # Load with overwrite
  echo "Loading DocType..."
  ./scripts/load.sh "$YAML_FILE"

  # Clear cache
  echo "Clearing cache..."
  docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
    cd /workspace/development/frappe-bench && \
    bench --site development.localhost clear-cache
  "

  echo "✓ Reload complete! Refresh your browser."
done
```

**Usage:**

```bash
chmod +x iterative_dev.sh
./iterative_dev.sh
# Edit YAML → Press Enter → See changes in browser → Repeat
```

---

### Example 6: Batch Validation

**Validate all YAML files before loading:**

```bash
# Validate all files in yaml_specs/
./scripts/batch_validate.sh yaml_specs/*.yaml

# Or manually
for file in yaml_specs/*.yaml; do
  echo "Validating $file..."
  python validate_yaml.py "$file"
  if [ $? -ne 0 ]; then
    echo "Failed: $file"
    exit 1
  fi
done

echo "All YAML files valid!"
```

---

### Example 7: Restore Controller from Backup

**List available backups:**

```bash
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/doctype_creator && \
  python -m src.controller_injector 'Service Provider' --list-backups
"

# Output:
# Backup files for 'Service Provider':
#   - service_provider.20251205_143022.bak
#   - service_provider.20251204_095512.bak
```

**Restore from backup:**

```bash
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/doctype_creator && \
  python -m src.controller_injector 'Service Provider' \
    --restore /path/to/service_provider.20251205_143022.bak
"
```

---

## Directory Structure

```
doctype_creator/
├── yaml_specs/                # Your YAML DocType specifications
│   ├── service_provider.yaml
│   └── ...
├── controllers/               # Python controller files
│   ├── example_controller.py
│   └── ...
├── schemas/                   # Validation schemas
│   └── doctype_schema.json   # JSON Schema for validation
├── src/                       # Source code
│   ├── __init__.py
│   ├── validator.py          # YAML validator (3 layers)
│   ├── loader.py             # DocType loader
│   ├── controller_injector.py # Controller injector
│   └── utils.py
├── templates/                 # AI templates and examples
│   ├── doctype_generation_prompt.md  # LLM prompt template
│   ├── DESIGN_GUIDELINES.md          # Best practices
│   ├── LLM_TEST_SCENARIOS.md         # LLM testing guide
│   └── examples/
│       ├── simple_doctype.yaml
│       ├── with_child_table.yaml
│       ├── with_workflow.yaml
│       └── complex_relationships.yaml
├── tests/                     # Test files
│   ├── test_validator.py     # Validator tests (12 tests)
│   ├── test_loader.py        # Loader tests (15 tests)
│   ├── test_controller_injector.py  # Injector tests (18 tests)
│   ├── test_integration.py   # Integration tests (6 tests)
│   └── fixtures/             # Test YAML files
├── scripts/                   # Convenience shell scripts
│   ├── load.sh               # Load DocType from host
│   ├── validate.sh           # Validate from host
│   ├── batch_validate.sh     # Validate multiple files
│   └── inject.sh             # Inject controller from host
├── load_doctype.py            # Main CLI script
├── validate_yaml.py           # Standalone validator CLI
├── requirements.txt
├── README.md                  # This file
├── TROUBLESHOOTING.md         # Troubleshooting guide
├── DOCTYPE_CREATOR_PLAN.md    # Implementation plan
└── SPRINT{1-6}_COMPLETION.md  # Sprint completion reports
```

---

## CLI Reference

### validate_yaml.py

Validate YAML files against schema and business rules.

```bash
python validate_yaml.py <yaml_file> [--schema <schema_file>]

# Examples:
python validate_yaml.py yaml_specs/service_provider.yaml
python validate_yaml.py my_doctype.yaml --schema custom_schema.json
```

**Exit codes:**
- `0` - Validation passed
- `1` - Validation failed

---

### load_doctype.py

Load DocType from YAML into Frappe.

```bash
python load_doctype.py <yaml_file> [OPTIONS]

Options:
  --site SITE          Frappe site name (default: development.localhost)
  --overwrite          Overwrite existing DocType (DANGEROUS - deletes data!)
  --validate-only      Only validate, do not load
  --no-validate        Skip validation (not recommended)

# Examples:
python load_doctype.py yaml_specs/service_provider.yaml
python load_doctype.py yaml_specs/my_doctype.yaml --validate-only
python load_doctype.py yaml_specs/my_doctype.yaml --overwrite
python load_doctype.py yaml_specs/my_doctype.yaml --site production.localhost
```

**Workflow:**
1. Validates YAML (unless `--no-validate`)
2. Checks if DocType exists
3. Converts YAML to Frappe dict
4. Creates DocType in Frappe
5. Commits to database

---

### controller_injector (src/controller_injector.py)

Inject Python controllers into DocType directories.

```bash
python -m src.controller_injector <doctype_name> <controller_file> [OPTIONS]

Options:
  --app APP            App name (default: nursing_management)
  --bench-path PATH    Path to Frappe bench directory
  --no-backup          Skip backup of existing controller
  --no-validate        Skip controller syntax validation
  --list-backups       List all backup files for DocType
  --restore BACKUP     Restore from backup file

# Examples:
# Inject controller
python -m src.controller_injector "Service Provider" controllers/service_provider.py

# Inject without backup (risky!)
python -m src.controller_injector "Service Provider" my_controller.py --no-backup

# List backups
python -m src.controller_injector "Service Provider" --list-backups

# Restore from backup
python -m src.controller_injector "Service Provider" --restore service_provider.20251205.bak
```

**Features:**
- Automatic DocType directory discovery
- Python syntax validation
- Controller class verification
- Automatic backup with timestamps
- Backup restoration

---

## Shell Scripts (Convenience)

### load.sh

```bash
./scripts/load.sh <yaml_file> [site]

# Examples:
./scripts/load.sh yaml_specs/service_provider.yaml
./scripts/load.sh yaml_specs/my_doctype.yaml production.localhost
```

Runs validation, loading, and cache clearing in one command.

---

### validate.sh

```bash
./scripts/validate.sh <yaml_file>

# Example:
./scripts/validate.sh yaml_specs/service_provider.yaml
```

---

### batch_validate.sh

```bash
./scripts/batch_validate.sh <yaml_files...>

# Examples:
./scripts/batch_validate.sh yaml_specs/*.yaml
./scripts/batch_validate.sh file1.yaml file2.yaml file3.yaml
```

---

### inject.sh

```bash
./scripts/inject.sh <doctype_name> <controller_file>

# Example:
./scripts/inject.sh "Service Provider" controllers/service_provider.py
```

---

## YAML Specification Reference

### Minimal Example

```yaml
doctype:
  name: "My DocType"
  module: "Nursing Management"
  naming_rule: "autoname"
  autoname: "format:MDT-{####}"
  fields:
    - fieldname: "title"
      fieldtype: "Data"
      label: "Title"
      reqd: true
  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
```

### Complete Example

See `templates/examples/complex_relationships.yaml` for a full example with all features.

### Required Fields

- `doctype.name` - DocType name (CamelCase with spaces)
- `doctype.module` - Module name (must exist in Frappe)
- `doctype.naming_rule` - `"autoname"` or `"by_fieldname"`
- `doctype.fields` - Array of field definitions

### Supported Field Types

**Basic Text:**
- `Data` - Single line (max 140 chars)
- `Text` - Multi-line plain text
- `Small Text` - Smaller multi-line text
- `Text Editor` - Rich text with HTML

**Numbers:**
- `Int` - Integer
- `Float` - Decimal (use `precision` property)

**Selection:**
- `Select` - Dropdown (newline-separated options)
- `Link` - Reference to another DocType

**Dates:**
- `Date` - Date picker
- `Datetime` - Date and time picker

**Other:**
- `Check` - Boolean checkbox
- `Attach` - File attachment
- `Table` - Child table (one-to-many)

**UI Layout:**
- `Section Break` - New section with optional label
- `Column Break` - New column in section

### Naming Rules

**Auto-naming:**
```yaml
naming_rule: "autoname"
autoname: "format:PREFIX-{#####}"
# Generates: PREFIX-00001, PREFIX-00002, ...
```

**By field:**
```yaml
naming_rule: "by_fieldname"
autoname: "field:hp_number"
# Uses hp_number field value as document name
```

---

## Testing

### Run All Tests

```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_validator.py -v
python -m pytest tests/test_loader.py -v
python -m pytest tests/test_controller_injector.py -v
python -m pytest tests/test_integration.py -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Results

**Total:** 60 tests, 100% passing

- **Validator Tests:** 12 tests (schema, business rules, Frappe compatibility)
- **Loader Tests:** 15 tests (YAML to Frappe conversion, field mapping, permissions)
- **Controller Injector Tests:** 18 tests (injection, backup, validation, restore)
- **Integration Tests:** 6 tests (end-to-end workflows)
- **Manual Tests:** 9 scenarios (documented in test reports)

---

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for comprehensive troubleshooting guide covering:

- Installation & setup issues
- YAML validation errors
- DocType loading errors
- Controller injection issues
- Frappe-specific issues
- Docker & container issues
- Common patterns & solutions
- Debugging tips

**Quick error reference:**

| Error | Solution |
|-------|----------|
| Invalid YAML syntax | Check indentation (2 spaces) |
| fieldname must be snake_case | Use lowercase with underscores |
| options required | Add options for Select/Link/Table fields |
| DocType already exists | Use --overwrite flag |
| Module not found | Use existing Frappe module |
| Directory not found | Load DocType before injecting controller |
| Syntax error in controller | Check Python syntax |

---

## Design Guidelines

See [templates/DESIGN_GUIDELINES.md](templates/DESIGN_GUIDELINES.md) for comprehensive best practices covering:

- General principles (KISS, single responsibility, data integrity)
- Naming conventions
- Field organization
- Field selection guide
- Relationships and links
- Validation patterns
- UI/UX best practices
- Performance considerations
- Security and permissions
- Common patterns library
- Anti-patterns to avoid

---

## LLM Usage

### Generate DocType with LLM

**Step 1:** Use the prompt template

```bash
cat templates/doctype_generation_prompt.md
# Copy entire content to LLM
```

**Step 2:** Provide your requirement

Example prompt to LLM:
```
Generate a DocType for tracking patient medications with:
- Patient name (link to Patient)
- Medication name
- Dosage
- Frequency (select: Once daily, Twice daily, etc.)
- Start date
- End date
- Status (select: Active, Completed, Discontinued)
```

**Step 3:** Validate and load

```bash
# Save LLM output to yaml_specs/medication.yaml
python validate_yaml.py yaml_specs/medication.yaml
./scripts/load.sh yaml_specs/medication.yaml
```

### Test Scenarios

See [templates/LLM_TEST_SCENARIOS.md](templates/LLM_TEST_SCENARIOS.md) for 10 test scenarios covering:

- Simple master data
- DocTypes with relationships
- Workflow-based DocTypes
- DocTypes with child tables
- Complex relationships with auto-fetch
- Configuration DocTypes
- Minimum viable DocTypes
- Calculated fields
- Edge cases

---

## Project Status

### Completed Sprints

✅ **Sprint 1: Foundation** - YAML schema, validator, tests
✅ **Sprint 2: Loader** - YAML to Frappe conversion, loading logic
✅ **Sprint 3: CLI & Integration** - Shell scripts, Docker integration
✅ **Sprint 4: Controller Injection** - Safe controller deployment
✅ **Sprint 5: AI Templates** - LLM prompts, examples, guidelines
✅ **Sprint 6: Documentation & Polish** - Comprehensive docs, troubleshooting

### Statistics

- **Files Created:** 30 files
- **Lines of Code:** 4,711 lines
- **Test Coverage:** 60 tests, 100% passing
- **Documentation:** 3,500+ lines
- **Examples:** 4 YAML examples
- **Shell Scripts:** 4 convenience scripts

### Success Criteria Met

1. ✅ LLM can generate valid YAML from natural language
2. ✅ YAML validator catches all common errors
3. ✅ Loader creates working DocTypes in Frappe
4. ✅ Controller injection works for custom logic
5. ✅ Docker volume workflow is seamless
6. ✅ Error messages are clear and actionable
7. ✅ Documentation is comprehensive
8. ✅ All existing script patterns are supported

---

## Future Enhancements (Phase 2)

Planned features for future versions:

- Support for all Frappe field types
- Workflow YAML specifications
- Print format templates
- Report definitions
- Dashboard configurations
- Automated testing generation
- Web form generation
- API endpoint generation
- Migration script generation

---

## Dependencies

```
PyYAML >= 6.0
jsonschema >= 4.17.0
pytest >= 7.4.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## References

- **Implementation Plan:** [DOCTYPE_CREATOR_PLAN.md](DOCTYPE_CREATOR_PLAN.md)
- **Sprint Reports:** SPRINT{1-6}_COMPLETION.md
- **Design Guidelines:** [templates/DESIGN_GUIDELINES.md](templates/DESIGN_GUIDELINES.md)
- **LLM Prompt:** [templates/doctype_generation_prompt.md](templates/doctype_generation_prompt.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Project Context:** [../CLAUDE.md](../CLAUDE.md)
- **Frappe Docs:** https://frappeframework.com/docs

---

## Contributing

This is an internal tool for the Nursing Management System project. For changes:

1. Create feature branch
2. Update tests
3. Update documentation
4. Submit for review

---

## License

Internal use only - Nursing Management System project

---

**Last Updated:** 2025-12-05 (Sprint 6)
**Version:** 1.0
**Author:** BTL Development Team
