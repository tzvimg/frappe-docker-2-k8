# DocTypes Loading Scripts

This directory contains scripts for creating DocTypes, workflows, and test data for the Siud application.

## Directory Structure

```
doctypes_loading/
├── creation/          # DocType and workflow creation scripts
├── test_data/         # Test data loading scripts
└── temp/              # Temporary/utility scripts for debugging
```

## 1. Creation Scripts (`creation/`)

These scripts create the core DocTypes, workflows, and dependencies for the application.

### Master Creation Script

**File:** `create_all_entities.py`
**Function:** `create_all_doctypes()`
**Usage:**
```bash
# From host
./run_doctype_script.sh creation.create_all_entities.create_all_doctypes

# From container
bench --site development.localhost execute siud.doctypes_loading.creation.create_all_entities.create_all_doctypes
```

### Supplier Inquiry Workflow

**File:** `create_supplier_inquiry_workflow.py`
**Functions:**
- `create_all()` - Creates roles, Supplier DocType, Supplier Inquiry DocType, and workflow
- `delete_all()` - Deletes all created components

**Usage:**
```bash
# Create everything
./run_doctype_script.sh creation.create_supplier_inquiry_workflow.create_all

# Delete everything (for fresh start)
./run_doctype_script.sh creation.create_supplier_inquiry_workflow.delete_all
```

### Individual Creation Scripts

| Script | Purpose |
|--------|---------|
| `create_supplier.py` | Create Supplier DocType |
| `create_supplier_inquiry.py` | Create Supplier Inquiry DocType |
| `create_contact_person.py` | Create Contact Person DocType |
| `create_role.py` | Create custom roles |
| `create_topic_category.py` | Create Topic Category DocType |
| `create_inquiry_topic_category.py` | Create Inquiry Topic Category DocType |
| `create_activity_domain_category.py` | Create Activity Domain Category DocType |

## 2. Test Data Scripts (`test_data/`)

Scripts for loading sample/test data into the system.

**File:** `create_test_data.py`
**Usage:**
```bash
./run_doctype_script.sh test_data.create_test_data.load_test_data
```

## 3. Temporary Scripts (`temp/`)

Utility scripts for debugging, inspection, and one-off operations.

| Script | Purpose |
|--------|---------|
| `check_role.py` | Check role configurations |
| `check_workflow.py` | Check workflow status |
| `inspect_supplier.py` | Inspect Supplier DocType |
| `inspect_supplier_inquiry.py` | Inspect Supplier Inquiry DocType |
| `inspect_workflow.py` | Inspect workflow details |
| `verify_workflow.py` | Verify workflow is properly configured |
| `restore_workflow.py` | Restore deleted workflow |
| `create_workflow_only.py` | Create only workflow (troubleshooting) |

**Example Usage:**
```bash
./run_doctype_script.sh temp.verify_workflow.verify
```

## Command Pattern

All scripts follow this pattern:

```bash
bench --site development.localhost execute siud.doctypes_loading.<subdirectory>.<module>.<function>
```

**Examples:**
- `siud.doctypes_loading.creation.create_all_entities.create_all_doctypes`
- `siud.doctypes_loading.test_data.create_test_data.load_test_data`
- `siud.doctypes_loading.temp.verify_workflow.verify`

## Typical Workflow

### Starting from Zero

1. **Delete all existing components** (optional, if rebuilding):
   ```bash
   ./run_doctype_script.sh creation.create_supplier_inquiry_workflow.delete_all
   ```

2. **Create all entities**:
   ```bash
   ./run_doctype_script.sh creation.create_supplier_inquiry_workflow.create_all
   ```

3. **Clear cache and migrate**:
   ```bash
   docker exec frappe_docker_devcontainer-frappe-1 bash -c \
     "cd /workspace/development/frappe-bench && \
      bench --site development.localhost clear-cache && \
      bench --site development.localhost migrate"
   ```

4. **Load test data** (optional):
   ```bash
   ./run_doctype_script.sh test_data.create_test_data.load_test_data
   ```

5. **Verify setup**:
   ```bash
   ./run_doctype_script.sh temp.verify_workflow.verify
   ```

## Notes

- Always run `bench clear-cache` after creating or modifying DocTypes
- Run `bench migrate` after cache clear to update database schema
- The `creation/` scripts are version-controlled and should be used for reproducible setups
- The `temp/` scripts are for debugging and can be modified as needed
- All files in this directory are mounted from host at `/home/tzvi/frappe/doctypes_loading/` to container at `/workspace/development/frappe-bench/apps/siud/siud/doctypes_loading/`
