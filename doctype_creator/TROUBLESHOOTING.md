# DocType Creator - Troubleshooting Guide

This guide covers common issues, error messages, and solutions when using the DocType Creator system.

---

## Table of Contents

1. [Installation & Setup Issues](#installation--setup-issues)
2. [YAML Validation Errors](#yaml-validation-errors)
3. [DocType Loading Errors](#doctype-loading-errors)
4. [Controller Injection Issues](#controller-injection-issues)
5. [Frappe-Specific Issues](#frappe-specific-issues)
6. [Docker & Container Issues](#docker--container-issues)
7. [Common Patterns & Solutions](#common-patterns--solutions)
8. [Debugging Tips](#debugging-tips)

---

## Installation & Setup Issues

### Issue: Missing Dependencies

**Error:**
```
ModuleNotFoundError: No module named 'jsonschema'
```

**Solution:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install individually
pip install pyyaml jsonschema
```

---

### Issue: Cannot Find Schema File

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: '.../schemas/doctype_schema.json'
```

**Solution:**
1. Verify directory structure:
   ```bash
   ls -la doctype_creator/schemas/
   ```

2. Ensure `doctype_schema.json` exists:
   ```bash
   # Should see doctype_schema.json
   ```

3. If missing, regenerate from plan or restore from backup

---

## YAML Validation Errors

### Issue: Invalid YAML Syntax

**Error:**
```
Invalid YAML syntax: while parsing a block mapping
  in "<unicode string>", line 15, column 1
```

**Solution:**
1. **Check indentation** - YAML requires consistent 2-space indentation:
   ```yaml
   # WRONG - mixed tabs/spaces
   doctype:
	  name: "My DocType"   # Tab used
     module: "Module"      # Spaces used

   # CORRECT - consistent 2 spaces
   doctype:
     name: "My DocType"
     module: "Module"
   ```

2. **Check for special characters** in strings:
   ```yaml
   # WRONG - colon in unquoted string
   label: Status: Active

   # CORRECT - quote strings with special chars
   label: "Status: Active"
   ```

3. **Use a YAML validator** online or in editor

---

### Issue: Schema Validation Failed

**Error:**
```
Schema validation failed: 'name' is a required property
```

**Solution:**
Check that all required fields are present:
```yaml
doctype:
  name: "My DocType"           # REQUIRED
  module: "Module Name"         # REQUIRED
  naming_rule: "autoname"       # REQUIRED
  fields: []                    # REQUIRED (can be empty array)
```

**Required top-level fields:**
- `doctype.name`
- `doctype.module`
- `doctype.naming_rule`
- `doctype.fields` (array)

---

### Issue: Invalid Field Name Format

**Error:**
```
Field 3: fieldname 'providerName' must be snake_case
```

**Solution:**
Use snake_case (lowercase with underscores) for all field names:
```yaml
# WRONG
fieldname: "providerName"      # camelCase
fieldname: "ProviderName"      # PascalCase
fieldname: "provider-name"     # kebab-case

# CORRECT
fieldname: "provider_name"     # snake_case
```

---

### Issue: Reserved Field Name

**Error:**
```
Field 5: 'name' is a reserved field name
```

**Solution:**
Frappe reserves certain field names. Never use:
- `name`, `owner`, `creation`, `modified`, `modified_by`
- `docstatus`, `idx`, `parent`, `parentfield`, `parenttype`
- `_user_tags`, `_comments`, `_assign`, `_liked_by`

Choose different field names:
```yaml
# WRONG
fieldname: "name"

# CORRECT
fieldname: "provider_name"
fieldname: "full_name"
fieldname: "item_name"
```

---

### Issue: Missing Options for Select/Link

**Error:**
```
Field 7: options required for Select field
```

**Solution:**
Always provide `options` for Select, Link, and Table fields:
```yaml
# Select field - newline-separated values
- fieldname: "status"
  fieldtype: "Select"
  label: "Status"
  options: "Draft\nActive\nInactive"    # REQUIRED

# Link field - target DocType name
- fieldname: "provider"
  fieldtype: "Link"
  label: "Provider"
  options: "Service Provider"           # REQUIRED

# Table field - child DocType name
- fieldname: "items"
  fieldtype: "Table"
  label: "Items"
  options: "Item List"                  # REQUIRED
```

---

### Issue: Invalid Naming Rule

**Error:**
```
Invalid naming_rule: auto_name
```

**Solution:**
Use only supported naming rules:
```yaml
# Option 1: Auto-naming with format
naming_rule: "autoname"
autoname: "format:SP-{#####}"

# Option 2: Naming by field
naming_rule: "by_fieldname"
autoname: "field:hp_number"

# WRONG
naming_rule: "auto_name"      # Incorrect format
naming_rule: "by_series"      # Not supported in v1.0
```

---

### Issue: Autoname Field Not Found

**Error:**
```
autoname field 'hp_number' not found in fields
```

**Solution:**
When using `naming_rule: "by_fieldname"`, ensure the field exists:
```yaml
doctype:
  naming_rule: "by_fieldname"
  autoname: "field:hp_number"    # References hp_number field

  fields:
    - fieldname: "hp_number"      # MUST exist in fields
      fieldtype: "Data"
      label: "HP Number"
      unique: true                # Should be unique
```

---

## DocType Loading Errors

### Issue: DocType Already Exists

**Error:**
```
DocType 'Service Provider' already exists. Use --overwrite to replace.
```

**Solution:**
```bash
# Option 1: Use --overwrite flag
python load_doctype.py yaml_specs/service_provider.yaml --overwrite

# Option 2: Delete existing DocType first (from Frappe UI or console)
# Then reload without --overwrite
```

**Warning:** `--overwrite` will delete all data in existing DocType!

---

### Issue: Module Not Found

**Error:**
```
Module 'My Custom Module' not found in Frappe
```

**Solution:**
1. **Use existing module:**
   ```yaml
   module: "Nursing Management"  # Use existing module
   ```

2. **Create module first** (via Frappe UI):
   - Navigate to: Developer → Module Def → New
   - Create your module
   - Then reload DocType

3. **Check available modules:**
   ```bash
   # In Frappe console
   bench --site development.localhost console
   >>> import frappe
   >>> frappe.get_all("Module Def", fields=["name"])
   ```

---

### Issue: Frappe Not Initialized

**Error:**
```
frappe.exceptions.SiteNotSpecifiedError: Site not specified
```

**Solution:**
1. **Run from correct directory:**
   ```bash
   cd /workspace/development/frappe-bench
   python /workspace/doctype_creator/load_doctype.py ...
   ```

2. **Or specify site explicitly:**
   ```bash
   python load_doctype.py yaml_specs/my_doctype.yaml --site development.localhost
   ```

3. **Check if Frappe is running:**
   ```bash
   bench --site development.localhost console
   # Should connect without errors
   ```

---

### Issue: Permission Errors During Load

**Error:**
```
frappe.exceptions.PermissionError: Not permitted
```

**Solution:**
The loader uses `ignore_permissions=True`, but if still failing:

1. **Run as Administrator in Frappe:**
   ```bash
   # In console
   frappe.set_user("Administrator")
   ```

2. **Check database permissions:**
   ```bash
   # Ensure Docker user has DB access
   ```

---

## Controller Injection Issues

### Issue: DocType Directory Not Found

**Error:**
```
DocType directory not found for 'Service Provider' in app 'nursing_management'
Expected pattern: .../apps/nursing_management/*/doctype/service_provider/
```

**Solution:**
1. **Verify DocType was created first:**
   ```bash
   # Must load DocType before injecting controller
   python load_doctype.py yaml_specs/service_provider.yaml
   ```

2. **Check DocType exists in Frappe:**
   ```bash
   bench --site development.localhost console
   >>> frappe.db.exists("DocType", "Service Provider")
   ```

3. **Verify app name is correct:**
   ```bash
   ls /workspace/development/frappe-bench/apps/
   # Should see 'nursing_management'
   ```

4. **Manually check path:**
   ```bash
   find /workspace/development/frappe-bench/apps -name "service_provider" -type d
   ```

---

### Issue: Controller Syntax Errors

**Error:**
```
Controller validation failed:
Syntax error at line 15: invalid syntax
```

**Solution:**
1. **Check Python syntax in controller file:**
   ```python
   # Common mistakes
   def validate(self)      # WRONG - missing colon
   def validate(self):     # CORRECT

   if self.hp_number       # WRONG - missing colon
   if self.hp_number:      # CORRECT
   ```

2. **Test syntax locally:**
   ```bash
   python -m py_compile controllers/my_controller.py
   ```

3. **Use `--no-validate` to skip validation** (not recommended):
   ```bash
   python -m src.controller_injector "Service Provider" controller.py --no-validate
   ```

---

### Issue: Controller Class Not Found

**Warning:**
```
⚠ Warning: Controller file doesn't define expected class
```

**Explanation:**
This is a warning, not an error. The injection succeeded, but the controller should define a class matching the DocType name.

**Solution:**
Ensure controller has correct class:
```python
# For DocType "Service Provider"
class ServiceProvider(Document):    # CORRECT
    def validate(self):
        pass

# Not
class MyController(Document):       # WRONG - won't be loaded
```

**Class name rules:**
- Remove spaces: "Service Provider" → "ServiceProvider"
- Remove hyphens: "My-DocType" → "MyDocType"
- Keep camelCase: "ServiceProvider" not "serviceprovider"

---

### Issue: Backup File Conflicts

**Error:**
```
Multiple backup files with same timestamp
```

**Solution:**
Backups auto-increment if conflicts occur. To clean up old backups:
```bash
# List backups
python -m src.controller_injector "Service Provider" --list-backups

# Manually delete old backups
rm /path/to/doctype/dir/service_provider.20231201_*.bak
```

---

## Frappe-Specific Issues

### Issue: Cache Not Cleared After Changes

**Symptom:**
Changes to DocType don't appear in UI.

**Solution:**
Always clear cache after loading or modifying DocTypes:
```bash
bench --site development.localhost clear-cache

# Or clear specific cache types
bench --site development.localhost clear-cache --doctype "Service Provider"
```

---

### Issue: Database Schema Out of Sync

**Error:**
```
Table 'tabService Provider' doesn't exist
```

**Solution:**
Run migrations to create database tables:
```bash
bench --site development.localhost migrate

# Check if table was created
bench --site development.localhost console
>>> frappe.db.table_exists("Service Provider")
```

---

### Issue: Field Changes Not Reflected

**Symptom:**
Modified fields in JSON don't show in form.

**Solution:**
1. Clear cache (always first step)
2. Reload form in browser (hard refresh: Ctrl+Shift+R)
3. Check DocType in Customize Form
4. Rebuild if necessary:
   ```bash
   bench build --app nursing_management
   ```

---

### Issue: Hebrew Labels Not Displaying

**Symptom:**
Hebrew text shows as ??? or squares.

**Solution:**
1. **Ensure UTF-8 encoding in YAML:**
   ```bash
   file -i yaml_specs/my_doctype.yaml
   # Should show: charset=utf-8
   ```

2. **Set encoding in Python:**
   ```python
   # Already handled in validator/loader
   with open(yaml_path, encoding='utf-8') as f:
   ```

3. **Check browser encoding** (should be UTF-8)

4. **Verify database charset:**
   ```sql
   SHOW VARIABLES LIKE 'character_set_%';
   -- Should show utf8mb4
   ```

---

## Docker & Container Issues

### Issue: Cannot Access Container

**Error:**
```
Error: No such container: frappe_docker_devcontainer-frappe-1
```

**Solution:**
1. **List running containers:**
   ```bash
   docker ps
   ```

2. **Find correct container name:**
   ```bash
   docker ps | grep frappe
   ```

3. **Start container if stopped:**
   ```bash
   cd frappe_docker
   docker-compose up -d
   ```

4. **Use correct container name** in commands:
   ```bash
   docker exec -it <actual-container-name> bash
   ```

---

### Issue: Volume Mount Not Working

**Symptom:**
Files in `C:\dev\btl\frappe\doctype_creator` not visible in container.

**Solution:**
1. **Check volume mount in docker-compose.yml:**
   ```yaml
   volumes:
     - C:/dev/btl/frappe:/workspace:cached
   ```

2. **Restart container after volume changes:**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

3. **Verify mount inside container:**
   ```bash
   docker exec -it <container> bash
   ls /workspace/doctype_creator
   ```

---

### Issue: Permission Denied in Container

**Error:**
```
Permission denied: '/workspace/doctype_creator/...'
```

**Solution:**
1. **Check file permissions on host:**
   ```bash
   chmod -R 755 doctype_creator/
   ```

2. **Run as correct user in container:**
   ```bash
   # Check current user
   whoami

   # If necessary, change ownership
   chown -R frappe:frappe /workspace/doctype_creator
   ```

---

## Common Patterns & Solutions

### Pattern: Batch Validation

**Task:**
Validate multiple YAML files at once.

**Solution:**
Use the batch validation script:
```bash
./scripts/batch_validate.sh yaml_specs/*.yaml
```

Or manually:
```bash
for file in yaml_specs/*.yaml; do
  python validate_yaml.py "$file"
done
```

---

### Pattern: Testing Before Production

**Task:**
Test DocType creation without affecting production.

**Solution:**
1. **Use development site:**
   ```bash
   python load_doctype.py my_doctype.yaml --site development.localhost
   ```

2. **Validate only mode:**
   ```bash
   python load_doctype.py my_doctype.yaml --validate-only
   ```

3. **Test in disposable site:**
   ```bash
   # Create test site
   bench new-site test.localhost

   # Load to test site
   python load_doctype.py my_doctype.yaml --site test.localhost

   # Drop test site when done
   bench drop-site test.localhost
   ```

---

### Pattern: Iterative Development

**Task:**
Repeatedly modify and reload DocType during development.

**Solution:**
```bash
# 1. Validate after each YAML edit
python validate_yaml.py yaml_specs/my_doctype.yaml

# 2. Load with overwrite
python load_doctype.py yaml_specs/my_doctype.yaml --overwrite

# 3. Clear cache
docker exec -it <container> bash -c "cd /workspace/development/frappe-bench && bench --site development.localhost clear-cache"

# 4. Reload browser
```

**Convenience script:**
```bash
#!/bin/bash
# reload.sh
YAML_FILE=$1
python validate_yaml.py "$YAML_FILE" && \
python load_doctype.py "$YAML_FILE" --overwrite && \
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site development.localhost clear-cache"
```

---

### Pattern: Debugging Validation Errors

**Task:**
Understand why validation is failing.

**Solution:**
1. **Read error messages carefully** - they include line numbers and field names

2. **Validate incrementally:**
   ```yaml
   # Start minimal
   doctype:
     name: "Test"
     module: "Nursing Management"
     naming_rule: "autoname"
     autoname: "format:TEST-{####}"
     fields: []
     permissions: []
   ```

3. **Add fields one by one** and revalidate

4. **Check schema directly:**
   ```bash
   cat schemas/doctype_schema.json | jq '.definitions.field'
   ```

5. **Compare with working examples:**
   ```bash
   diff yaml_specs/my_doctype.yaml templates/examples/simple_doctype.yaml
   ```

---

## Debugging Tips

### Enable Verbose Logging

Add debug print statements:
```python
# In validator.py
print(f"DEBUG: Validating field {idx}: {field}")

# In loader.py
print(f"DEBUG: frappe_dict = {json.dumps(frappe_dict, indent=2)}")
```

---

### Inspect Intermediate Data

Use Python debugger:
```python
# Add to loader.py
import pdb; pdb.set_trace()

# Or use breakpoint() in Python 3.7+
breakpoint()
```

---

### Check Generated JSON

After successful load, inspect the generated JSON:
```bash
find /workspace/development/frappe-bench/apps -name "service_provider.json"
cat <path-to-json>
```

---

### Test in Frappe Console

Interactive testing:
```bash
bench --site development.localhost console
```

```python
>>> import frappe
>>> from doctype_creator.src.validator import DocTypeValidator
>>> from doctype_creator.src.loader import DocTypeLoader

# Test validator
>>> validator = DocTypeValidator()
>>> is_valid, errors, warnings = validator.validate_yaml_file(Path("yaml_specs/test.yaml"))
>>> print(errors)

# Test loader
>>> loader = DocTypeLoader()
>>> result = loader.load_from_yaml(Path("yaml_specs/test.yaml"))
```

---

### Use Validation in Stages

Break validation into layers:
```bash
# Layer 1: YAML syntax
python -c "import yaml; yaml.safe_load(open('my.yaml'))"

# Layer 2: JSON schema
python validate_yaml.py my.yaml --schema schemas/doctype_schema.json

# Layer 3: Business rules (full validation)
python validate_yaml.py my.yaml
```

---

## Getting Help

### Check Documentation

1. **Main README:** `doctype_creator/README.md`
2. **Design Guidelines:** `templates/DESIGN_GUIDELINES.md`
3. **Prompt Template:** `templates/doctype_generation_prompt.md`
4. **Implementation Plan:** `DOCTYPE_CREATOR_PLAN.md`
5. **Sprint Reports:** `SPRINT{1-5}_COMPLETION.md`

### Check Examples

Working examples in `templates/examples/`:
- `simple_doctype.yaml` - Minimal DocType
- `with_child_table.yaml` - Parent-child relationship
- `with_workflow.yaml` - Submittable with workflow
- `complex_relationships.yaml` - Multiple links and auto-fetch

### Common Error Reference

| Error | Quick Fix |
|-------|-----------|
| "Invalid YAML syntax" | Check indentation (2 spaces) |
| "fieldname must be snake_case" | Use lowercase with underscores |
| "options required" | Add options field for Select/Link/Table |
| "DocType already exists" | Use --overwrite flag |
| "Module not found" | Use existing module name |
| "Directory not found" | Load DocType before injecting controller |
| "Syntax error" | Check Python syntax in controller |
| "Cache not cleared" | Run bench clear-cache |

---

## Still Stuck?

1. **Check Sprint completion reports** for known limitations
2. **Review test files** in `tests/` for usage patterns
3. **Examine shell scripts** in `scripts/` for integration examples
4. **Test with minimal example** to isolate issue
5. **Check Frappe logs:** `/workspace/development/frappe-bench/sites/development.localhost/logs/`

---

**Last Updated:** 2025-12-05 (Sprint 6)
**Version:** 1.0
