# DocType Creator

AI-powered DocType generator for Frappe Framework using YAML specifications.

## Sprint 1 - Foundation (COMPLETED)

Sprint 1 has been successfully completed with the following deliverables:

- ✅ Directory structure created
- ✅ JSON Schema for YAML validation
- ✅ Validator module with 3 validation layers
- ✅ Example YAML files (simple and with child table)
- ✅ Test fixtures (valid and invalid cases)
- ✅ Comprehensive unit tests (12 tests, all passing)
- ✅ Requirements file with dependencies

## Quick Start

### 1. Install Dependencies

```bash
cd doctype_creator
pip install -r requirements.txt
```

### 2. Validate a YAML File

```bash
python src/validator.py templates/examples/simple_doctype.yaml
```

### 3. Run Tests

```bash
python -m pytest tests/test_validator.py -v
```

## Directory Structure

```
doctype_creator/
├── yaml_specs/              # Your YAML files (empty for now)
├── controllers/             # Python controllers (optional)
├── schemas/                 # Validation schemas
│   └── doctype_schema.json # JSON Schema for YAML validation
├── src/                     # Source code
│   ├── __init__.py
│   └── validator.py        # Validation module
├── templates/               # AI prompts and examples
│   └── examples/
│       ├── simple_doctype.yaml
│       └── with_child_table.yaml
├── tests/                   # Tests
│   ├── __init__.py
│   ├── test_validator.py
│   └── fixtures/           # Test YAML files
│       ├── valid_simple.yaml
│       ├── invalid_missing_name.yaml
│       ├── invalid_reserved_field.yaml
│       ├── invalid_bad_fieldname.yaml
│       └── invalid_select_no_options.yaml
├── scripts/                 # Convenience scripts (for future)
├── requirements.txt
└── README.md
```

## Validator Features

### Three-Layer Validation

1. **Schema Validation (JSON Schema)**
   - Validates YAML structure
   - Checks required fields
   - Type checking
   - Enum validation

2. **Business Rules**
   - fieldname must be snake_case
   - fieldname must be unique within DocType
   - label required for all non-break fields
   - options required for Select/Link/Table fields
   - Naming rule validation

3. **Frappe Compatibility**
   - Reserved field names (name, owner, creation, etc.)
   - Field type compatibility
   - Permission role validation

### Supported Field Types (Phase 1)

Data, Text, Text Editor, Small Text, Select, Link, Date, Datetime, Int, Float, Check, Attach, Section Break, Column Break, Table

## Example YAML Structure

```yaml
doctype:
  name: "Service Provider"
  module: "Nursing Management"
  naming_rule: "autoname"
  autoname: "format:SP-{#####}"
  track_changes: true
  description: "Service provider master data"

  fields:
    - fieldname: "provider_name"
      fieldtype: "Data"
      label: "שם נותן השירות"
      reqd: true
      in_list_view: true

  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
```

## Test Results

All 12 unit tests passing:

- ✅ Valid YAML validation
- ✅ Missing required field detection
- ✅ Reserved field name detection
- ✅ Invalid fieldname (non-snake_case) detection
- ✅ Select field without options detection
- ✅ Nonexistent file handling
- ✅ Reserved fields list verification
- ✅ Valid field types verification
- ✅ Valid naming rules verification
- ✅ Schema validation layer
- ✅ Business rules validation layer
- ✅ Frappe compatibility validation layer

## Next Steps (Sprint 2)

- [ ] Implement YAML to Frappe dict converter
- [ ] Write loader module
- [ ] Handle naming rules
- [ ] Add error handling and rollback
- [ ] Test with simple DocTypes

## Dependencies

- PyYAML >= 6.0
- jsonschema >= 4.17.0
- pytest >= 7.4.0 (for testing)

## References

- See `DOCTYPE_CREATOR_PLAN.md` for complete implementation plan
- Frappe DocType Documentation: https://frappeframework.com/docs/user/en/basics/doctypes
