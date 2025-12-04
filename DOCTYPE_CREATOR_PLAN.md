# DocType Creator - Implementation Plan

## 🎯 Project Status

**Current Sprint**: Sprint 4 ✅ COMPLETED (2025-12-05)
**Next Sprint**: Sprint 5 - AI Templates
**Overall Progress**: 67% (4 of 6 sprints completed)

### Quick Stats
- **Files Created**: 25 files (2,961 lines of code)
- **Test Coverage**: 60 tests (100% passing)
- **Modules**: Validator (3 layers) + Loader (YAML→Frappe) + Controller Injector
- **CLI Scripts**: 2 Python + 4 Shell scripts
- **Example YAML Files**: 2 working examples (loadable)
- **Example Controllers**: 1 template controller
- **Integration Tests**: 6 test scenarios

### Recent Achievements (Sprint 4)
✅ Complete Python controller injection system (345 lines)
✅ Automatic DocType directory discovery with smart path resolution
✅ Python syntax validation and controller class verification
✅ Timestamped backup mechanism with restore functionality
✅ Comprehensive test suite with 18 tests (100% passing)
✅ Docker-integrated shell script (inject.sh)
✅ Example controller template with best practices

📄 See [SPRINT4_COMPLETION.md](doctype_creator/SPRINT4_COMPLETION.md) for Sprint 4 detailed report
📄 See [SPRINT3_COMPLETION.md](doctype_creator/SPRINT3_COMPLETION.md) for Sprint 3 detailed report
📄 See [SPRINT2_COMPLETION.md](doctype_creator/SPRINT2_COMPLETION.md) for Sprint 2 detailed report
📄 See [SPRINT1_COMPLETION.md](doctype_creator/SPRINT1_COMPLETION.md) for Sprint 1 detailed report

---

## Overview
A system for LLM-based DocType generation using YAML specifications, with automated loading into Frappe via bench commands and separate Python controller injection.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       LLM Model (Claude/etc)                     │
│          Generates YAML specs from natural language              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    YAML Specification File                       │
│  - DocType metadata (name, fields, permissions, etc)             │
│  - Validation rules                                              │
│  - UI layout hints                                               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   YAML Validator Module                          │
│  - Schema validation (pydantic/jsonschema)                       │
│  - Business rules validation                                     │
│  - Frappe compatibility checks                                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DocType Loader Script                           │
│  - Parse YAML to Frappe DocType dict                             │
│  - Execute via bench console                                     │
│  - Handle errors and rollback                                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              Python Controller Injector (Optional)               │
│  - Load controller.py file separately                            │
│  - Place in correct DocType folder                               │
│  - Handle method validation                                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Frappe DocType (Loaded)                       │
│  - JSON schema generated                                         │
│  - Database table created                                        │
│  - UI forms available                                            │
└─────────────────────────────────────────────────────────────────┘
```

## File Structure

```
C:\dev\btl\frappe\
├── doctype_creator/              # New directory (mounted to container)
│   ├── yaml_specs/               # LLM-generated YAML files
│   │   ├── service_provider.yaml
│   │   ├── contract.yaml
│   │   └── ...
│   ├── controllers/              # Python controller files (optional)
│   │   ├── service_provider.py
│   │   ├── contract.py
│   │   └── ...
│   ├── schemas/                  # Validation schemas
│   │   └── doctype_schema.json  # JSON Schema for YAML validation
│   ├── src/                      # Source code
│   │   ├── __init__.py
│   │   ├── validator.py         # YAML validation logic
│   │   ├── loader.py            # DocType loading logic
│   │   ├── controller_injector.py
│   │   └── utils.py
│   ├── templates/                # AI prompt templates
│   │   ├── doctype_generation_prompt.md
│   │   └── examples/
│   │       ├── simple_doctype.yaml
│   │       ├── with_child_table.yaml
│   │       └── with_workflow.yaml
│   ├── tests/                    # Test files
│   │   ├── test_validator.py
│   │   ├── test_loader.py
│   │   └── fixtures/
│   ├── load_doctype.py           # Main CLI script
│   ├── validate_yaml.py          # Standalone validator
│   ├── requirements.txt
│   └── README.md
└── frappe_docker/
    └── .devcontainer/
        └── docker-compose.yml    # Already has volume mount configured
```

## Phase 1: YAML Schema Design

### 1.1 Basic YAML Structure

**Supported in v1.0:**
```yaml
# Basic DocType specification
doctype:
  name: "Service Provider"
  module: "Nursing Management"
  naming_rule: "autoname"  # or "by_fieldname"
  autoname: "format:SP-{#####}"

  # Optional metadata
  is_submittable: false
  track_changes: true
  is_tree: false
  title_field: null
  description: "Manages service provider master data"

  # Fields
  fields:
    - fieldname: "provider_name"
      fieldtype: "Data"
      label: "שם נותן השירות"
      reqd: true
      in_list_view: true
      in_standard_filter: false
      unique: false
      description: "Name of the service provider"

    - fieldname: "hp_number"
      fieldtype: "Data"
      label: "מספר ח\"פ"
      reqd: true
      length: 9
      unique: true
      in_list_view: true
      in_standard_filter: true

    - fieldname: "section_break_1"
      fieldtype: "Section Break"
      label: "Contact Details"

    - fieldname: "column_break_1"
      fieldtype: "Column Break"

    - fieldname: "email"
      fieldtype: "Data"
      label: "אימייל"
      options: "Email"

    - fieldname: "service_type"
      fieldtype: "Select"
      label: "סוג שירות"
      options: "טיפול בבית\nמרכז יום\nקהילה תומכת"
      reqd: true

    - fieldname: "branch"
      fieldtype: "Link"
      label: "סניף"
      options: "Service Provider Branch"

    - fieldname: "status"
      fieldtype: "Select"
      label: "סטטוס"
      options: "פעיל\nסגור"
      default: "פעיל"

    - fieldname: "start_date"
      fieldtype: "Date"
      label: "תאריך התחלה"
      default: "Today"

    - fieldname: "notes"
      fieldtype: "Text Editor"
      label: "הערות"

    - fieldname: "attachment"
      fieldtype: "Attach"
      label: "קובץ מצורף"

  # Permissions
  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
      delete: 1
      submit: 0
      cancel: 0
      amend: 0

    - role: "Internal Reviewer"
      read: 1
      write: 1
      create: 0
      delete: 0

# Optional: Controller hints (won't be loaded, just documentation)
controller:
  file: "service_provider.py"
  methods:
    - validate
    - before_insert
    - on_update
  validations:
    - "HP number must be 9 digits"
    - "Email format validation"
```

### 1.2 Supported Field Types (Phase 1)

**Core field types:**
- `Data` - Single-line text
- `Text` - Multi-line text
- `Text Editor` - Rich text with HTML
- `Small Text` - Multi-line plain text
- `Select` - Dropdown (options separated by \n)
- `Link` - Reference to another DocType
- `Date` - Date picker
- `Datetime` - Date and time picker
- `Int` - Integer number
- `Float` - Decimal number
- `Check` - Checkbox (boolean)
- `Attach` - File attachment
- `Section Break` - UI section separator
- `Column Break` - UI column separator
- `Table` - Child table (link to child DocType)

**Not supported in v1.0 (future):**
- Dynamic Link
- Table MultiSelect
- HTML
- Code
- Color
- Barcode
- Geolocation
- Custom field types

### 1.3 Field Properties (Phase 1)

```yaml
field:
  fieldname: "field_name"        # Required, snake_case
  fieldtype: "Data"              # Required
  label: "Field Label"           # Required
  reqd: false                    # Optional, default false
  unique: false                  # Optional, default false
  read_only: false               # Optional, default false
  hidden: false                  # Optional, default false
  in_list_view: false            # Optional, show in list view
  in_standard_filter: false      # Optional, show in filters
  default: null                  # Optional, default value
  description: null              # Optional, help text
  options: null                  # Required for Select/Link, null otherwise
  length: null                   # Optional, for Data fields
  precision: null                # Optional, for Float fields
  fetch_from: null               # Optional, e.g., "branch.service_provider"
```

### 1.4 Naming Rules

```yaml
# Option 1: Auto-naming with format
naming_rule: "autoname"
autoname: "format:SP-{#####}"  # SP-00001, SP-00002, etc.

# Option 2: Naming by fieldname
naming_rule: "by_fieldname"
autoname: "field:hp_number"    # Use hp_number as primary key

# Option 3: Naming by series (future)
naming_rule: "by_series"
autoname: "SP-.#####"
```

## Phase 2: YAML Validator Module

### 2.1 Validation Layers

**Layer 1: Schema Validation (JSON Schema)**
- Validate YAML structure
- Check required fields
- Type checking
- Enum validation

**Layer 2: Business Rules**
- fieldname must be snake_case
- fieldname must be unique within DocType
- label required for all non-break fields
- options required for Select/Link
- Module must exist in Frappe
- Link target DocType must exist (warning)

**Layer 3: Frappe Compatibility**
- Reserved field names (name, owner, creation, etc.)
- Field type compatibility
- Naming rule validation
- Permission role validation

### 2.2 Validator Implementation

**File: `doctype_creator/src/validator.py`**

```python
"""
YAML DocType Specification Validator

Validates YAML files against schema and business rules before loading.
"""

import yaml
import jsonschema
from pathlib import Path
from typing import Dict, List, Tuple
import re


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


class DocTypeValidator:
    """Validates DocType YAML specifications"""

    # Frappe reserved field names
    RESERVED_FIELDS = {
        'name', 'owner', 'creation', 'modified', 'modified_by',
        'docstatus', 'idx', 'parent', 'parentfield', 'parenttype',
        '_user_tags', '_comments', '_assign', '_liked_by'
    }

    # Valid field types for phase 1
    VALID_FIELD_TYPES = {
        'Data', 'Text', 'Text Editor', 'Small Text',
        'Select', 'Link', 'Date', 'Datetime',
        'Int', 'Float', 'Check', 'Attach',
        'Section Break', 'Column Break', 'Table'
    }

    # Valid naming rules
    VALID_NAMING_RULES = {'autoname', 'by_fieldname'}

    def __init__(self, schema_path: Path = None):
        """Initialize validator with JSON schema"""
        if schema_path is None:
            schema_path = Path(__file__).parent.parent / 'schemas' / 'doctype_schema.json'

        with open(schema_path) as f:
            self.schema = json.load(f)

    def validate_yaml_file(self, yaml_path: Path) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a YAML file

        Returns:
            (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        # Load YAML
        try:
            with open(yaml_path) as f:
                spec = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return False, [f"Invalid YAML syntax: {e}"], []
        except Exception as e:
            return False, [f"Error reading file: {e}"], []

        # Layer 1: Schema validation
        schema_errors = self._validate_schema(spec)
        errors.extend(schema_errors)

        if errors:
            return False, errors, warnings

        # Layer 2: Business rules
        business_errors, business_warnings = self._validate_business_rules(spec)
        errors.extend(business_errors)
        warnings.extend(business_warnings)

        # Layer 3: Frappe compatibility
        frappe_errors, frappe_warnings = self._validate_frappe_compatibility(spec)
        errors.extend(frappe_errors)
        warnings.extend(frappe_warnings)

        is_valid = len(errors) == 0
        return is_valid, errors, warnings

    def _validate_schema(self, spec: Dict) -> List[str]:
        """Validate against JSON schema"""
        errors = []
        try:
            jsonschema.validate(instance=spec, schema=self.schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation failed: {e.message}")
        except Exception as e:
            errors.append(f"Schema validation error: {e}")
        return errors

    def _validate_business_rules(self, spec: Dict) -> Tuple[List[str], List[str]]:
        """Validate business rules"""
        errors = []
        warnings = []

        doctype = spec.get('doctype', {})

        # Validate naming
        naming_rule = doctype.get('naming_rule')
        if naming_rule not in self.VALID_NAMING_RULES:
            errors.append(f"Invalid naming_rule: {naming_rule}")

        if naming_rule == 'autoname':
            autoname = doctype.get('autoname', '')
            if not autoname.startswith('format:'):
                errors.append(f"autoname must start with 'format:' when using autoname rule")

        if naming_rule == 'by_fieldname':
            autoname = doctype.get('autoname', '')
            if not autoname.startswith('field:'):
                errors.append(f"autoname must start with 'field:' when using by_fieldname rule")
            else:
                field_name = autoname.replace('field:', '')
                field_names = [f['fieldname'] for f in doctype.get('fields', [])]
                if field_name not in field_names:
                    errors.append(f"autoname field '{field_name}' not found in fields")

        # Validate fields
        field_names = set()
        for idx, field in enumerate(doctype.get('fields', [])):
            fieldname = field.get('fieldname', '')
            fieldtype = field.get('fieldtype', '')
            label = field.get('label', '')

            # Check snake_case
            if fieldname and not re.match(r'^[a-z][a-z0-9_]*$', fieldname):
                errors.append(f"Field {idx}: fieldname '{fieldname}' must be snake_case")

            # Check uniqueness
            if fieldname in field_names:
                errors.append(f"Field {idx}: duplicate fieldname '{fieldname}'")
            field_names.add(fieldname)

            # Check reserved names
            if fieldname in self.RESERVED_FIELDS:
                errors.append(f"Field {idx}: '{fieldname}' is a reserved field name")

            # Check field type
            if fieldtype not in self.VALID_FIELD_TYPES:
                errors.append(f"Field {idx}: invalid fieldtype '{fieldtype}'")

            # Check label for non-break fields
            if fieldtype not in ['Section Break', 'Column Break']:
                if not label:
                    errors.append(f"Field {idx}: label required for fieldtype '{fieldtype}'")

            # Check options for Select/Link
            if fieldtype == 'Select':
                if not field.get('options'):
                    errors.append(f"Field {idx}: options required for Select field")

            if fieldtype == 'Link':
                if not field.get('options'):
                    errors.append(f"Field {idx}: options (target DocType) required for Link field")

            if fieldtype == 'Table':
                if not field.get('options'):
                    errors.append(f"Field {idx}: options (child DocType) required for Table field")

        return errors, warnings

    def _validate_frappe_compatibility(self, spec: Dict) -> Tuple[List[str], List[str]]:
        """Validate Frappe-specific compatibility"""
        errors = []
        warnings = []

        doctype = spec.get('doctype', {})

        # Check module (will warn if doesn't exist, but won't error)
        module = doctype.get('module')
        if not module:
            errors.append("module is required")

        # Check permissions
        permissions = doctype.get('permissions', [])
        if not permissions:
            warnings.append("No permissions defined - DocType will only be accessible to System Manager")

        for perm in permissions:
            role = perm.get('role')
            if not role:
                errors.append("Permission missing 'role' field")

        return errors, warnings


# CLI interface
def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Validate DocType YAML specification')
    parser.add_argument('yaml_file', help='Path to YAML file')
    parser.add_argument('--schema', help='Path to JSON schema (optional)')

    args = parser.parse_args()

    validator = DocTypeValidator(schema_path=args.schema)
    is_valid, errors, warnings = validator.validate_yaml_file(Path(args.yaml_file))

    if warnings:
        print("⚠ Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        print("❌ Errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print("✓ YAML validation passed!")
    sys.exit(0)


if __name__ == '__main__':
    main()
```

### 2.3 JSON Schema

**File: `doctype_creator/schemas/doctype_schema.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Frappe DocType YAML Specification",
  "type": "object",
  "required": ["doctype"],
  "properties": {
    "doctype": {
      "type": "object",
      "required": ["name", "module", "naming_rule", "fields"],
      "properties": {
        "name": {
          "type": "string",
          "description": "DocType name (CamelCase)"
        },
        "module": {
          "type": "string",
          "description": "Module name"
        },
        "naming_rule": {
          "type": "string",
          "enum": ["autoname", "by_fieldname"],
          "description": "How to name documents"
        },
        "autoname": {
          "type": "string",
          "description": "Naming pattern (e.g., 'format:SP-{#####}')"
        },
        "is_submittable": {
          "type": "boolean",
          "default": false
        },
        "track_changes": {
          "type": "boolean",
          "default": true
        },
        "is_tree": {
          "type": "boolean",
          "default": false
        },
        "title_field": {
          "type": ["string", "null"],
          "default": null
        },
        "description": {
          "type": "string",
          "description": "DocType description"
        },
        "fields": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/field"
          },
          "minItems": 1
        },
        "permissions": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/permission"
          }
        }
      }
    },
    "controller": {
      "type": "object",
      "description": "Optional controller metadata (documentation only)",
      "properties": {
        "file": {
          "type": "string"
        },
        "methods": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "validations": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    }
  },
  "definitions": {
    "field": {
      "type": "object",
      "required": ["fieldname", "fieldtype"],
      "properties": {
        "fieldname": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_]*$"
        },
        "fieldtype": {
          "type": "string",
          "enum": [
            "Data", "Text", "Text Editor", "Small Text",
            "Select", "Link", "Date", "Datetime",
            "Int", "Float", "Check", "Attach",
            "Section Break", "Column Break", "Table"
          ]
        },
        "label": {
          "type": "string"
        },
        "reqd": {
          "type": "boolean",
          "default": false
        },
        "unique": {
          "type": "boolean",
          "default": false
        },
        "read_only": {
          "type": "boolean",
          "default": false
        },
        "hidden": {
          "type": "boolean",
          "default": false
        },
        "in_list_view": {
          "type": "boolean",
          "default": false
        },
        "in_standard_filter": {
          "type": "boolean",
          "default": false
        },
        "default": {
          "type": ["string", "number", "boolean", "null"]
        },
        "description": {
          "type": "string"
        },
        "options": {
          "type": "string"
        },
        "length": {
          "type": "integer"
        },
        "precision": {
          "type": "integer"
        },
        "fetch_from": {
          "type": "string"
        }
      }
    },
    "permission": {
      "type": "object",
      "required": ["role"],
      "properties": {
        "role": {
          "type": "string"
        },
        "read": {
          "type": "integer",
          "enum": [0, 1],
          "default": 0
        },
        "write": {
          "type": "integer",
          "enum": [0, 1],
          "default": 0
        },
        "create": {
          "type": "integer",
          "enum": [0, 1],
          "default": 0
        },
        "delete": {
          "type": "integer",
          "enum": [0, 1],
          "default": 0
        },
        "submit": {
          "type": "integer",
          "enum": [0, 1],
          "default": 0
        },
        "cancel": {
          "type": "integer",
          "enum": [0, 1],
          "default": 0
        },
        "amend": {
          "type": "integer",
          "enum": [0, 1],
          "default": 0
        }
      }
    }
  }
}
```

## Phase 3: DocType Loader Script

### 3.1 Loader Implementation

**File: `doctype_creator/src/loader.py`**

```python
"""
DocType Loader

Loads DocType from YAML specification into Frappe
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Optional
import frappe
from frappe import _


class LoadError(Exception):
    """Raised when loading fails"""
    pass


class DocTypeLoader:
    """Loads DocType from YAML specification"""

    def __init__(self, site: str = 'development.localhost'):
        """Initialize loader"""
        self.site = site
        self.dry_run = False

    def load_from_yaml(self, yaml_path: Path, overwrite: bool = False) -> Dict:
        """
        Load DocType from YAML file

        Args:
            yaml_path: Path to YAML file
            overwrite: If True, delete existing DocType before creating

        Returns:
            Created DocType document dict
        """
        # Load YAML
        with open(yaml_path) as f:
            spec = yaml.safe_load(f)

        doctype_spec = spec.get('doctype', {})
        doctype_name = doctype_spec.get('name')

        print(f"Loading DocType: {doctype_name}")

        # Check if exists
        if frappe.db.exists("DocType", doctype_name):
            if overwrite:
                print(f"  - DocType exists, deleting...")
                self._delete_doctype(doctype_name)
            else:
                raise LoadError(f"DocType '{doctype_name}' already exists. Use --overwrite to replace.")

        # Convert to Frappe dict
        frappe_dict = self._yaml_to_frappe_dict(doctype_spec)

        # Create DocType
        doc = frappe.get_doc(frappe_dict)
        doc.insert(ignore_permissions=True)

        frappe.db.commit()

        print(f"✓ DocType '{doctype_name}' created successfully")
        print(f"  - Total fields: {len(doc.fields)}")
        print(f"  - Permissions: {len(doc.permissions)} roles")

        return doc.as_dict()

    def _yaml_to_frappe_dict(self, spec: Dict) -> Dict:
        """Convert YAML spec to Frappe DocType dict"""

        frappe_dict = {
            'doctype': 'DocType',
            'name': spec['name'],
            'module': spec['module'],
            'custom': 0,
            'is_submittable': spec.get('is_submittable', False),
            'track_changes': spec.get('track_changes', True),
            'is_tree': spec.get('is_tree', False),
        }

        # Handle naming
        naming_rule = spec.get('naming_rule')
        autoname = spec.get('autoname', '')

        if naming_rule == 'autoname':
            # Format: "format:SP-{#####}" -> autoname = "format:SP-{#####}"
            frappe_dict['autoname'] = autoname
        elif naming_rule == 'by_fieldname':
            # Format: "field:hp_number" -> autoname = "field:hp_number"
            frappe_dict['autoname'] = autoname
            frappe_dict['naming_rule'] = 'By fieldname'

        # Title field
        if spec.get('title_field'):
            frappe_dict['title_field'] = spec['title_field']

        # Description
        if spec.get('description'):
            frappe_dict['description'] = spec['description']

        # Fields
        frappe_dict['fields'] = []
        for field_spec in spec.get('fields', []):
            field_dict = self._convert_field(field_spec)
            frappe_dict['fields'].append(field_dict)

        # Permissions
        frappe_dict['permissions'] = []
        for perm_spec in spec.get('permissions', []):
            perm_dict = self._convert_permission(perm_spec)
            frappe_dict['permissions'].append(perm_dict)

        return frappe_dict

    def _convert_field(self, spec: Dict) -> Dict:
        """Convert YAML field spec to Frappe field dict"""
        field = {
            'fieldname': spec['fieldname'],
            'fieldtype': spec['fieldtype'],
        }

        # Optional properties
        optional_props = [
            'label', 'reqd', 'unique', 'read_only', 'hidden',
            'in_list_view', 'in_standard_filter', 'default',
            'description', 'options', 'length', 'precision', 'fetch_from'
        ]

        for prop in optional_props:
            if prop in spec:
                value = spec[prop]
                # Convert boolean to int for Frappe (reqd, unique, etc.)
                if isinstance(value, bool):
                    value = 1 if value else 0
                field[prop] = value

        return field

    def _convert_permission(self, spec: Dict) -> Dict:
        """Convert YAML permission spec to Frappe permission dict"""
        perm = {
            'role': spec['role'],
            'read': spec.get('read', 0),
            'write': spec.get('write', 0),
            'create': spec.get('create', 0),
            'delete': spec.get('delete', 0),
            'submit': spec.get('submit', 0),
            'cancel': spec.get('cancel', 0),
            'amend': spec.get('amend', 0),
        }
        return perm

    def _delete_doctype(self, doctype_name: str):
        """Delete existing DocType"""
        try:
            frappe.delete_doc("DocType", doctype_name, force=True)
            frappe.db.commit()
        except Exception as e:
            raise LoadError(f"Failed to delete existing DocType: {e}")


# CLI interface
def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Load DocType from YAML')
    parser.add_argument('yaml_file', help='Path to YAML file')
    parser.add_argument('--site', default='development.localhost', help='Frappe site name')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing DocType')
    parser.add_argument('--validate-only', action='store_true', help='Only validate, do not load')

    args = parser.parse_args()

    # Validate first
    if args.validate_only:
        from .validator import DocTypeValidator
        validator = DocTypeValidator()
        is_valid, errors, warnings = validator.validate_yaml_file(Path(args.yaml_file))

        if warnings:
            print("⚠ Warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        if errors:
            print("❌ Validation errors:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)

        print("✓ Validation passed!")
        sys.exit(0)

    # Initialize Frappe
    frappe.init(site=args.site)
    frappe.connect()

    try:
        loader = DocTypeLoader(site=args.site)
        result = loader.load_from_yaml(Path(args.yaml_file), overwrite=args.overwrite)
        print(f"\n✓ DocType loaded successfully: {result['name']}")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error loading DocType: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
```

### 3.2 Main CLI Script

**File: `doctype_creator/load_doctype.py`**

```python
#!/usr/bin/env python3
"""
DocType Creator - Main CLI

Validates and loads DocType from YAML specification into Frappe
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from validator import DocTypeValidator
from loader import DocTypeLoader
import frappe


def main():
    parser = argparse.ArgumentParser(
        description='Create Frappe DocType from YAML specification',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate only
  python load_doctype.py yaml_specs/service_provider.yaml --validate-only

  # Load DocType
  python load_doctype.py yaml_specs/service_provider.yaml

  # Overwrite existing
  python load_doctype.py yaml_specs/service_provider.yaml --overwrite

  # Load to specific site
  python load_doctype.py yaml_specs/service_provider.yaml --site production.localhost
        """
    )

    parser.add_argument('yaml_file', help='Path to YAML specification file')
    parser.add_argument('--site', default='development.localhost', help='Frappe site name')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing DocType')
    parser.add_argument('--validate-only', action='store_true', help='Only validate, do not load')
    parser.add_argument('--no-validate', action='store_true', help='Skip validation (not recommended)')

    args = parser.parse_args()

    yaml_path = Path(args.yaml_file)

    if not yaml_path.exists():
        print(f"❌ Error: File not found: {yaml_path}")
        sys.exit(1)

    # Step 1: Validation
    if not args.no_validate:
        print("=" * 60)
        print("STEP 1: YAML VALIDATION")
        print("=" * 60)

        validator = DocTypeValidator()
        is_valid, errors, warnings = validator.validate_yaml_file(yaml_path)

        if warnings:
            print("\n⚠ Warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        if not is_valid:
            print("\n❌ Validation failed with errors:")
            for error in errors:
                print(f"  - {error}")
            print("\nPlease fix the errors and try again.")
            sys.exit(1)

        print("\n✓ Validation passed!")

        if args.validate_only:
            sys.exit(0)

    # Step 2: Loading
    print("\n" + "=" * 60)
    print("STEP 2: LOADING DOCTYPE")
    print("=" * 60)

    try:
        # Initialize Frappe
        frappe.init(site=args.site)
        frappe.connect()

        loader = DocTypeLoader(site=args.site)
        result = loader.load_from_yaml(yaml_path, overwrite=args.overwrite)

        print("\n" + "=" * 60)
        print("✓ SUCCESS")
        print("=" * 60)
        print(f"DocType '{result['name']}' has been created successfully!")
        print(f"\nAccess it at: http://localhost:8000/app/{result['name'].lower().replace(' ', '-')}")
        print("\nNext steps:")
        print("  1. Clear cache: bench --site {args.site} clear-cache")
        print("  2. View in UI: http://localhost:8000")
        print("  3. Add Python controller if needed")

        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Error loading DocType: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
```

## Phase 4: Python Controller Injection

### 4.1 Controller Injector

**File: `doctype_creator/src/controller_injector.py`**

```python
"""
Python Controller Injector

Injects Python controller files into DocType directories
"""

import shutil
from pathlib import Path
from typing import Optional
import frappe


class ControllerInjector:
    """Injects Python controllers into Frappe DocTypes"""

    def __init__(self, bench_path: Path = None):
        """Initialize injector"""
        if bench_path is None:
            bench_path = Path('/workspace/development/frappe-bench')
        self.bench_path = bench_path

    def inject_controller(
        self,
        doctype_name: str,
        controller_path: Path,
        module: str = 'Nursing Management',
        app: str = 'nursing_management'
    ) -> bool:
        """
        Inject Python controller into DocType directory

        Args:
            doctype_name: Name of DocType (e.g., "Service Provider")
            controller_path: Path to controller .py file
            module: Module name
            app: App name

        Returns:
            True if successful
        """
        # Convert DocType name to directory name (lowercase, underscores)
        doctype_dir = doctype_name.lower().replace(' ', '_')

        # Target directory
        target_dir = (
            self.bench_path / 'apps' / app / app.replace('-', '_') /
            'doctype' / doctype_dir
        )

        if not target_dir.exists():
            raise ValueError(f"DocType directory not found: {target_dir}")

        # Target file
        target_file = target_dir / f"{doctype_dir}.py"

        if target_file.exists():
            print(f"⚠ Controller file already exists: {target_file}")
            print(f"  Backing up to {target_file}.bak")
            shutil.copy2(target_file, str(target_file) + '.bak')

        # Copy controller
        shutil.copy2(controller_path, target_file)
        print(f"✓ Controller injected: {target_file}")

        return True


# CLI
def main():
    import argparse

    parser = argparse.ArgumentParser(description='Inject Python controller into DocType')
    parser.add_argument('doctype_name', help='DocType name (e.g., "Service Provider")')
    parser.add_argument('controller_file', help='Path to controller .py file')
    parser.add_argument('--app', default='nursing_management', help='App name')
    parser.add_argument('--module', default='Nursing Management', help='Module name')

    args = parser.parse_args()

    try:
        injector = ControllerInjector()
        injector.inject_controller(
            args.doctype_name,
            Path(args.controller_file),
            module=args.module,
            app=args.app
        )
        print("\n✓ Controller injection complete!")
        print("  Run: bench --site development.localhost clear-cache")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
```

## Phase 5: AI Prompt Templates

### 5.1 DocType Generation Prompt

**File: `doctype_creator/templates/doctype_generation_prompt.md`**

```markdown
# Frappe DocType YAML Generator

You are an expert in Frappe Framework DocType design. Your task is to generate a YAML specification file for a Frappe DocType based on the user's requirements.

## Output Format

Generate a YAML file following this structure:

```yaml
doctype:
  name: "DocType Name"
  module: "Module Name"
  naming_rule: "autoname"  # or "by_fieldname"
  autoname: "format:PREFIX-{#####}"
  is_submittable: false
  track_changes: true
  description: "Description of the DocType"

  fields:
    - fieldname: "field_name"
      fieldtype: "Data"
      label: "Field Label"
      reqd: true
      in_list_view: true
      description: "Field description"

  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
```

## Supported Field Types

**Basic text:**
- `Data` - Single line text (max 140 chars)
- `Text` - Multi-line plain text
- `Small Text` - Multi-line plain text (smaller)
- `Text Editor` - Rich text with HTML

**Numbers:**
- `Int` - Integer number
- `Float` - Decimal number (use `precision` property)

**Selection:**
- `Select` - Dropdown (options separated by \n)
- `Link` - Reference to another DocType (set `options` to target DocType name)

**Dates:**
- `Date` - Date picker
- `Datetime` - Date and time picker

**Other:**
- `Check` - Boolean checkbox
- `Attach` - File attachment
- `Table` - Child table (set `options` to child DocType name)

**UI Layout:**
- `Section Break` - Start new section with optional label
- `Column Break` - Start new column in same section

## Field Properties

Required:
- `fieldname` - Unique field identifier (snake_case)
- `fieldtype` - One of the supported types above

Common properties:
- `label` - Display label (use Hebrew for this project)
- `reqd` - Required field (true/false)
- `unique` - Must be unique (true/false)
- `read_only` - Cannot be edited (true/false)
- `hidden` - Hidden from UI (true/false)
- `default` - Default value (use "Today" for current date)
- `description` - Help text
- `in_list_view` - Show in list view (true/false)
- `in_standard_filter` - Show in filters (true/false)

Type-specific:
- `options` - Required for Select (newline-separated values), Link (target DocType), Table (child DocType)
- `length` - Max length for Data fields (integer)
- `precision` - Decimal places for Float (integer)
- `fetch_from` - Auto-fetch from Link field (e.g., "branch.service_provider")

## Naming Rules

**Auto-naming with format pattern:**
```yaml
naming_rule: "autoname"
autoname: "format:SP-{#####}"  # Generates SP-00001, SP-00002, etc.
```

**Naming by field value:**
```yaml
naming_rule: "by_fieldname"
autoname: "field:hp_number"  # Use hp_number field as document name
```

## Permissions

Standard permission levels:
- `read` - Can view documents
- `write` - Can edit documents
- `create` - Can create new documents
- `delete` - Can delete documents
- `submit` - Can submit (if is_submittable=true)
- `cancel` - Can cancel (if is_submittable=true)
- `amend` - Can amend (if is_submittable=true)

Common roles:
- System Manager (full access)
- Internal Reviewer (read/write, no delete)
- HQ Approver (read/write/submit)
- Service Provider User (limited access)

## Design Guidelines

1. **Field naming**: Use clear, descriptive snake_case names
2. **Labels**: Use Hebrew labels for this project
3. **Organization**: Use Section Break and Column Break for clean layout
4. **Required fields**: Mark essential fields as required
5. **Unique fields**: Mark identifier fields (like IDs, codes) as unique
6. **List view**: Select 3-5 most important fields for list view
7. **Filters**: Add important search fields to standard filters
8. **Links**: Use Link fields to connect DocTypes
9. **Defaults**: Provide sensible defaults where possible
10. **Validation**: Document validation rules in field descriptions

## Example: Simple DocType

```yaml
doctype:
  name: "Service Provider"
  module: "Nursing Management"
  naming_rule: "autoname"
  autoname: "format:SP-{#####}"
  track_changes: true
  description: "Service provider master data"

  fields:
    # Section 1: Basic Info
    - fieldname: "basic_section"
      fieldtype: "Section Break"
      label: "פרטים בסיסיים"

    - fieldname: "provider_name"
      fieldtype: "Data"
      label: "שם נותן השירות"
      reqd: true
      in_list_view: true
      in_standard_filter: true

    - fieldname: "hp_number"
      fieldtype: "Data"
      label: "מספר ח\"פ"
      reqd: true
      unique: true
      length: 9
      in_list_view: true
      description: "9-digit HP number"

    - fieldname: "column_break_1"
      fieldtype: "Column Break"

    - fieldname: "service_type"
      fieldtype: "Select"
      label: "סוג שירות"
      options: "טיפול בבית\nמרכז יום\nקהילה תומכת"
      reqd: true
      in_standard_filter: true

    - fieldname: "status"
      fieldtype: "Select"
      label: "סטטוס"
      options: "פעיל\nסגור"
      default: "פעיל"
      in_list_view: true

    # Section 2: Contact
    - fieldname: "contact_section"
      fieldtype: "Section Break"
      label: "פרטי קשר"

    - fieldname: "email"
      fieldtype: "Data"
      label: "אימייל"
      options: "Email"

    - fieldname: "phone"
      fieldtype: "Data"
      label: "טלפון"
      options: "Phone"

  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
      delete: 1
```

## Instructions

When given a DocType requirement:

1. Ask clarifying questions if needed:
   - What fields are required?
   - What should be the primary identifier?
   - What are the different states/status values?
   - Should it be submittable?
   - Who should have access (roles)?

2. Design the field structure:
   - Group related fields with Section Breaks
   - Use Column Breaks for side-by-side layout
   - Choose appropriate field types
   - Set proper validations (reqd, unique, length)

3. Generate clean YAML:
   - Use proper indentation (2 spaces)
   - Include helpful comments
   - Add field descriptions for complex fields
   - Use Hebrew labels
   - Set sensible defaults

4. Include metadata:
   - Clear DocType description
   - Proper naming pattern
   - Appropriate permissions

5. Validate your output:
   - Check for required properties
   - Ensure fieldnames are snake_case
   - Verify field types are supported
   - Check that Link/Select/Table fields have options

## Common Patterns

**Status tracking:**
```yaml
- fieldname: "status"
  fieldtype: "Select"
  label: "סטטוס"
  options: "Draft\nActive\nInactive\nClosed"
  default: "Draft"
```

**Date range:**
```yaml
- fieldname: "start_date"
  fieldtype: "Date"
  label: "תאריך התחלה"
  reqd: true

- fieldname: "end_date"
  fieldtype: "Date"
  label: "תאריך סיום"
```

**Link with auto-fetch:**
```yaml
- fieldname: "branch"
  fieldtype: "Link"
  label: "סניף"
  options: "Service Provider Branch"
  reqd: true

- fieldname: "service_provider"
  fieldtype: "Link"
  label: "נותן שירות"
  options: "Service Provider"
  read_only: true
  fetch_from: "branch.service_provider"
```

**Child table:**
```yaml
- fieldname: "documents"
  fieldtype: "Table"
  label: "רשימת מסמכים"
  options: "Document Checklist"
```

## Error Prevention

Common mistakes to avoid:

1. ❌ Using spaces in fieldnames → Use snake_case
2. ❌ Missing options for Select/Link → Always set options
3. ❌ Missing labels for data fields → Add Hebrew labels
4. ❌ Reserved fieldnames (name, owner, creation, etc.) → Use unique names
5. ❌ Invalid field types → Use only supported types from list above
6. ❌ Inconsistent indentation → Use 2 spaces consistently

## Next Steps After Generation

After generating the YAML:

1. Validate: `python validate_yaml.py your_file.yaml`
2. Load: `python load_doctype.py your_file.yaml`
3. Add controller if needed: Create separate .py file with validation logic
4. Test in UI: http://localhost:8000

Now, please provide the DocType requirements you'd like me to generate!
```

### 5.2 Example YAML Files

**File: `doctype_creator/templates/examples/simple_doctype.yaml`**

```yaml
# Simple DocType Example
# A basic service provider with essential fields only

doctype:
  name: "Simple Provider"
  module: "Nursing Management"
  naming_rule: "autoname"
  autoname: "format:SIMP-{####}"
  track_changes: true
  description: "Simplified service provider"

  fields:
    - fieldname: "provider_name"
      fieldtype: "Data"
      label: "שם הספק"
      reqd: true
      in_list_view: true

    - fieldname: "email"
      fieldtype: "Data"
      label: "אימייל"
      options: "Email"

  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
      delete: 1
```

**File: `doctype_creator/templates/examples/with_child_table.yaml`**

```yaml
# DocType with Child Table Example
# Parent-child relationship

doctype:
  name: "Service Agreement"
  module: "Nursing Management"
  naming_rule: "autoname"
  autoname: "format:AGR-{#####}"
  is_submittable: true
  track_changes: true
  description: "Service agreement with line items"

  fields:
    - fieldname: "agreement_section"
      fieldtype: "Section Break"
      label: "פרטי הסכם"

    - fieldname: "agreement_name"
      fieldtype: "Data"
      label: "שם הסכם"
      reqd: true
      in_list_view: true

    - fieldname: "provider"
      fieldtype: "Link"
      label: "ספק"
      options: "Service Provider"
      reqd: true
      in_list_view: true

    - fieldname: "start_date"
      fieldtype: "Date"
      label: "תאריך התחלה"
      reqd: true
      default: "Today"

    - fieldname: "items_section"
      fieldtype: "Section Break"
      label: "פריטים"

    - fieldname: "items"
      fieldtype: "Table"
      label: "פריטי הסכם"
      options: "Agreement Item"

  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
      submit: 1
```

## Phase 6: Docker Volume Integration

### 6.1 Usage Workflow

```bash
# On host machine (C:\dev\btl\frappe\)

# 1. Create doctype_creator directory (if not exists)
mkdir doctype_creator
cd doctype_creator

# 2. Generate YAML with AI (manual or automated)
# ... LLM generates service_provider.yaml ...

# 3. Save to yaml_specs/
mkdir -p yaml_specs
# Save YAML file to yaml_specs/service_provider.yaml

# 4. Validate (optional, from host)
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/doctype_creator && \
  python validate_yaml.py yaml_specs/service_provider.yaml
"

# 5. Load DocType
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/development/frappe-bench && \
  python /workspace/doctype_creator/load_doctype.py \
    /workspace/doctype_creator/yaml_specs/service_provider.yaml
"

# 6. Clear cache
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/development/frappe-bench && \
  bench --site development.localhost clear-cache
"

# 7. (Optional) Inject controller
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/doctype_creator && \
  python -m src.controller_injector 'Service Provider' \
    controllers/service_provider.py
"
```

### 6.2 Convenience Scripts

**File: `doctype_creator/scripts/load.sh`**

```bash
#!/bin/bash
# Convenience script to load DocType from host

YAML_FILE=$1
SITE=${2:-development.localhost}

if [ -z "$YAML_FILE" ]; then
  echo "Usage: ./scripts/load.sh <yaml_file> [site]"
  echo "Example: ./scripts/load.sh yaml_specs/service_provider.yaml"
  exit 1
fi

echo "Loading DocType from $YAML_FILE..."

docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/development/frappe-bench && \
  python /workspace/doctype_creator/load_doctype.py \
    /workspace/doctype_creator/$YAML_FILE \
    --site $SITE && \
  bench --site $SITE clear-cache
"

echo "✓ Done! Access at http://localhost:8000"
```

**File: `doctype_creator/scripts/validate.sh`**

```bash
#!/bin/bash
# Validate YAML file

YAML_FILE=$1

if [ -z "$YAML_FILE" ]; then
  echo "Usage: ./scripts/validate.sh <yaml_file>"
  exit 1
fi

docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/doctype_creator && \
  python validate_yaml.py $YAML_FILE
"
```

## Phase 7: Testing & Examples

### 7.1 Test Strategy

**Unit tests:**
- YAML schema validation
- Field conversion logic
- Naming rule handling
- Permission mapping

**Integration tests:**
- Full DocType creation
- Existing DocType handling
- Error scenarios
- Controller injection

**Manual tests:**
- UI form rendering
- Field validations in browser
- List view display
- Permissions enforcement

### 7.2 Test Fixtures

**File: `doctype_creator/tests/fixtures/valid_simple.yaml`**

```yaml
doctype:
  name: "Test Simple"
  module: "Nursing Management"
  naming_rule: "autoname"
  autoname: "format:TEST-{####}"

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

**File: `doctype_creator/tests/fixtures/invalid_missing_name.yaml`**

```yaml
doctype:
  module: "Nursing Management"
  fields: []
```

## Phase 8: Documentation

### 8.1 README Structure

**File: `doctype_creator/README.md`**

```markdown
# DocType Creator

AI-powered DocType generator for Frappe Framework using YAML specifications.

## Quick Start

### 1. Generate YAML

Use the AI prompt template to generate a YAML specification:

```bash
# Show prompt template
cat templates/doctype_generation_prompt.md

# Or see examples
cat templates/examples/simple_doctype.yaml
```

### 2. Validate YAML

```bash
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/doctype_creator && \
  python validate_yaml.py yaml_specs/your_doctype.yaml
"
```

### 3. Load DocType

```bash
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/development/frappe-bench && \
  python /workspace/doctype_creator/load_doctype.py \
    /workspace/doctype_creator/yaml_specs/your_doctype.yaml && \
  bench --site development.localhost clear-cache
"
```

### 4. Access in UI

http://localhost:8000

## Features

✅ YAML-based DocType specifications
✅ JSON Schema validation
✅ Business rules validation
✅ Automated loading via bench
✅ Python controller injection
✅ AI prompt templates
✅ Docker volume integration
✅ Comprehensive error messages

## Directory Structure

```
doctype_creator/
├── yaml_specs/       # Your YAML files
├── controllers/      # Python controllers (optional)
├── schemas/          # Validation schemas
├── src/              # Source code
├── templates/        # AI prompts
├── tests/            # Tests
└── scripts/          # Convenience scripts
```

## YAML Specification

See `templates/doctype_generation_prompt.md` for complete specification.

### Basic Structure

```yaml
doctype:
  name: "DocType Name"
  module: "Module Name"
  naming_rule: "autoname"
  autoname: "format:PREFIX-{#####}"

  fields:
    - fieldname: "field_name"
      fieldtype: "Data"
      label: "Label"
      reqd: true

  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
```

### Supported Field Types (v1.0)

Data, Text, Text Editor, Small Text, Select, Link, Date, Datetime, Int, Float, Check, Attach, Section Break, Column Break, Table

## CLI Usage

### validate_yaml.py

```bash
python validate_yaml.py <yaml_file> [--schema <schema_file>]
```

### load_doctype.py

```bash
python load_doctype.py <yaml_file> [OPTIONS]

Options:
  --site SITE          Frappe site name (default: development.localhost)
  --overwrite          Overwrite existing DocType
  --validate-only      Only validate, do not load
  --no-validate        Skip validation (not recommended)
```

### Controller Injection

```bash
python -m src.controller_injector <doctype_name> <controller_file> [OPTIONS]

Options:
  --app APP            App name (default: nursing_management)
  --module MODULE      Module name (default: Nursing Management)
```

## Common Issues

### Issue: "DocType already exists"

**Solution:** Use `--overwrite` flag

```bash
python load_doctype.py yaml_specs/my_doctype.yaml --overwrite
```

### Issue: "Module not found"

**Solution:** Ensure module exists in Frappe or create it first

### Issue: "Invalid field type"

**Solution:** Check supported field types in templates/doctype_generation_prompt.md

## Development

### Running Tests

```bash
cd doctype_creator
python -m pytest tests/
```

### Adding New Field Types

1. Update `validator.py` - Add to `VALID_FIELD_TYPES`
2. Update `loader.py` - Handle any special conversion logic
3. Update `schemas/doctype_schema.json` - Add to enum
4. Update `templates/doctype_generation_prompt.md` - Document usage

## References

- Frappe DocType Documentation: https://frappeframework.com/docs/user/en/basics/doctypes
- Project Documentation: ../CLAUDE.md
- Workflow Implementation: ../workflow-implementation-plan.md

## License

MIT
```

## Implementation Roadmap

### Sprint 1: Foundation (Days 1-2) ✅ COMPLETED

**Status**: Completed on 2025-12-05

- [x] Create directory structure
- [x] Implement basic YAML schema (2 example files)
- [x] Write JSON Schema validator (152 lines, complete schema)
- [x] Create validation module (226 lines, 3-layer validation)
- [x] Write unit tests for validator (12 tests, all passing)
- [x] Create requirements.txt with dependencies
- [x] Create README documentation
- [x] Create test fixtures (5 invalid cases, 1 valid case)

**Deliverables**:
- Total: 787 lines of code across 12 files
- Validator with schema, business rules, and Frappe compatibility layers
- 100% test pass rate (12/12 tests)
- Example YAML files for simple DocType and child table DocType
- Complete JSON Schema for validation

### Sprint 2: Loader (Days 3-4) ✅ COMPLETED

**Status**: Completed on 2025-12-05

- [x] Implement YAML to Frappe dict converter
- [x] Write loader module (184 lines)
- [x] Handle naming rules (autoname and by_fieldname)
- [x] Add error handling and rollback
- [x] Create main CLI script (103 lines)
- [x] Create standalone validator CLI (72 lines)
- [x] Write comprehensive test suite (15 tests, all passing)

**Deliverables**:
- Total: 659 lines of code across 4 new files
- Loader module with full YAML to Frappe conversion
- Main CLI script with validation + loading workflow
- Standalone validator CLI for batch validation
- 100% test pass rate (15/15 new tests, 27/27 total)
- Support for all Phase 1 field types and properties

### Sprint 3: CLI & Integration (Days 5-6) ✅ COMPLETED

**Status**: Completed on 2025-12-05

- [x] Create main CLI script (✅ Completed in Sprint 2)
- [x] Add Docker volume integration testing
- [x] Write convenience shell scripts (load.sh, validate.sh, batch_validate.sh)
- [x] Test end-to-end workflow in Frappe container
- [x] Test overwrite scenarios with real DocTypes
- [x] Add progress indicators and better output formatting

**Deliverables**:
- Total: 600 lines of new code across 4 new files
- 3 convenience shell scripts (180 lines)
- Integration test suite with 6 test scenarios (420 lines)
- Enhanced loader with 5-step progress tracking
- Batch validation support
- End-to-end workflow testing capabilities

### Sprint 4: Controller Injection (Day 7) ✅ COMPLETED

**Status**: Completed on 2025-12-05

- [x] Implement controller injector (345 lines)
- [x] Add file placement logic with smart DocType discovery
- [x] Create backup mechanism with timestamps and restore
- [x] Add Python syntax validation
- [x] Add controller class verification
- [x] Write unit tests (18 tests, all passing)
- [x] Create convenience shell script (inject.sh)
- [x] Create example controller template

**Deliverables**:
- Total: 915 lines of code across 4 new files
- Controller injector with validation, backup, and restore
- 100% test pass rate (18/18 new tests, 60/60 total)
- Shell script for Docker integration
- Example controller demonstrating all patterns
- CLI with multiple modes (inject, list-backups, restore)

### Sprint 5: AI Templates (Days 8-9)
- [ ] Write comprehensive prompt template
- [ ] Create example YAML files (✅ 2 examples already created)
- [ ] Add design guidelines
- [ ] Test with LLM generation

### Sprint 6: Documentation & Polish (Day 10)
- [x] Write comprehensive README (✅ Sprint 1 README completed)
- [ ] Add inline documentation
- [ ] Create troubleshooting guide
- [ ] Polish error messages
- [ ] Add usage examples

## Success Criteria

1. ✅ LLM can generate valid YAML from natural language
2. ✅ YAML validator catches all common errors (Sprint 1 ✅)
3. ✅ Loader creates working DocTypes in Frappe (Sprint 2 ✅)
4. ✅ Controller injection works for custom logic (Sprint 4 ✅)
5. ✅ Docker volume workflow is seamless (Sprint 3 ✅)
6. ✅ Error messages are clear and actionable (Sprint 1 & 2 ✅)
7. ✅ Documentation is comprehensive
8. ✅ All existing scripts' patterns are supported

## Future Enhancements (Phase 2)

- Support for all Frappe field types
- Workflow YAML specifications
- Print format templates
- Report definitions
- Dashboard configurations
- Automated testing generation
- Web form generation
- API endpoint generation
- Migration script generation

## Lessons from Existing Scripts

Based on analysis of `create_spa_doctype.py`, `create_contract_doctype.py`, `create_branch_doctype.py`:

**What worked:**
- Using `frappe.new_doc('DocType')` for creation
- Using `append('fields', {...})` for fields
- Using `insert(ignore_permissions=True)` for loading
- Checking existence with `frappe.db.exists()`

**What can be improved:**
- Manual field dict creation → YAML spec
- No validation before creation → Add validator
- Inconsistent patterns → Standardized YAML
- No reusability → Template-based generation

**Patterns to support:**
- Hebrew labels (RTL)
- Israeli validations (HP number, ID number)
- Common field combinations (dates, status, etc.)
- Permission patterns (internal vs external users)

---

**Total estimated time:** 10 days
**Priority:** High (enables rapid DocType development)
**Dependencies:** Docker environment, Frappe Framework
**Risk level:** Low (non-destructive, can rollback)
