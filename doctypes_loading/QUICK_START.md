# Quick Start Guide - Running from Zero

This guide shows how to rebuild the entire Supplier Inquiry system from scratch.

## Prerequisites

- Docker containers running
- Frappe bench accessible at `/workspace/development/frappe-bench` in container
- Helper script: `/home/tzvi/frappe/run_doctype_script.sh`

## Step-by-Step: Build from Zero

### 1. Delete Existing Components (Optional)

If you want to start completely fresh:

```bash
./run_doctype_script.sh creation.create_supplier_inquiry_workflow.delete_all
```

### 2. Create All Components

This will create:
- Required roles (Service Provider User, Sorting Clerk, Handling Clerk)
- Supplier DocType
- Supplier Inquiry DocType
- Supplier Inquiry Workflow (6 states, 8 transitions)

```bash
./run_doctype_script.sh creation.create_supplier_inquiry_workflow.create_all
```

### 3. Clear Cache and Migrate

**IMPORTANT:** Always run after creating DocTypes!

```bash
docker exec frappe_docker_devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && \
   bench --site development.localhost clear-cache && \
   bench --site development.localhost migrate"
```

### 4. Verify Setup

```bash
./run_doctype_script.sh temp.verify_workflow.verify
```

Expected output:
```
✅ Supplier Inquiry Workflow EXISTS and is ACTIVE!
States: 6
Transitions: 8
```

### 5. Load Test Data (Optional)

```bash
./run_doctype_script.sh test_data.create_test_data.load_test_data
```

### 6. Access the System

Open browser: http://localhost:8000

Navigate to: **Desk → Supplier Inquiry**

## Available Creation Scripts

All scripts are in `doctypes_loading/creation/`:

### Master Scripts

| Script | Function | Purpose |
|--------|----------|---------|
| `create_supplier_inquiry_workflow.py` | `create_all()` | Creates entire Supplier Inquiry system |
| `create_supplier_inquiry_workflow.py` | `delete_all()` | Deletes entire Supplier Inquiry system |
| `create_all_entities.py` | `create_all_doctypes()` | Creates all core DocTypes |

### Individual Scripts

| Script | Purpose |
|--------|---------|
| `create_supplier.py` | Supplier DocType |
| `create_supplier_inquiry.py` | Supplier Inquiry DocType |
| `create_contact_person.py` | Contact Person DocType |
| `create_role.py` | Custom roles |
| `create_topic_category.py` | Topic Category DocType |
| `create_inquiry_topic_category.py` | Inquiry Topic Category |
| `create_activity_domain_category.py` | Activity Domain Category |

## Common Commands

### Using Helper Script (Recommended)

```bash
# Show help
./run_doctype_script.sh --help

# Run creation script
./run_doctype_script.sh creation.create_supplier_inquiry_workflow.create_all

# Run test data script
./run_doctype_script.sh test_data.create_test_data.load_test_data

# Run temp/utility script
./run_doctype_script.sh temp.verify_workflow.verify
```

### Direct Docker Commands

```bash
# General pattern
docker exec frappe_docker_devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && \
   bench --site development.localhost execute siud.doctypes_loading.<subdirectory>.<module>.<function>"

# Example
docker exec frappe_docker_devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && \
   bench --site development.localhost execute siud.doctypes_loading.creation.create_supplier_inquiry_workflow.create_all"
```

## Troubleshooting

### Workflow Already Exists Error

```bash
# Delete the workflow first
./run_doctype_script.sh creation.create_supplier_inquiry_workflow.delete_all

# Then recreate
./run_doctype_script.sh creation.create_supplier_inquiry_workflow.create_all
```

### Permission Errors

```bash
# Fix file permissions
chmod -R 777 /home/tzvi/frappe/doctypes_loading/
```

### Cache Issues

```bash
# Clear cache
docker exec frappe_docker_devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && \
   bench --site development.localhost clear-cache"
```

### Module Not Found

Make sure `__init__.py` files exist in all subdirectories:
```bash
ls /home/tzvi/frappe/doctypes_loading/creation/__init__.py
ls /home/tzvi/frappe/doctypes_loading/test_data/__init__.py
ls /home/tzvi/frappe/doctypes_loading/temp/__init__.py
```

## Directory Structure

```
/home/tzvi/frappe/doctypes_loading/
├── creation/                          # Production-ready creation scripts
│   ├── __init__.py
│   ├── create_all_entities.py         # Master: Create all core DocTypes
│   ├── create_supplier_inquiry_workflow.py  # Master: Supplier Inquiry system
│   ├── create_supplier.py
│   ├── create_supplier_inquiry.py
│   ├── create_contact_person.py
│   ├── create_role.py
│   ├── create_topic_category.py
│   ├── create_inquiry_topic_category.py
│   └── create_activity_domain_category.py
│
├── test_data/                         # Test data loading
│   ├── __init__.py
│   └── create_test_data.py
│
├── temp/                              # Temporary/debug scripts
│   ├── __init__.py
│   ├── verify_workflow.py
│   ├── restore_workflow.py
│   ├── inspect_supplier.py
│   ├── inspect_supplier_inquiry.py
│   ├── inspect_workflow.py
│   ├── check_role.py
│   ├── check_workflow.py
│   └── create_workflow_only.py
│
├── README.md                          # Full documentation
└── QUICK_START.md                     # This file
```

## Workflow States (Reference)

The Supplier Inquiry Workflow has 6 states:

1. **פנייה חדשה התקבלה** (New Inquiry Received) - Initial state
2. **מיון וניתוב** (Sorting and Routing) - Triage by Sorting Clerk
3. **בטיפול** (In Progress) - Active handling by Handling Clerk
4. **דורש השלמות / המתנה** (Requires Completion / Waiting) - Waiting for info
5. **נסגר – ניתן מענה** (Closed - Response Given) - Completed with response
6. **סגור** (Archived) - Final archived state

## Next Steps

After successful setup:

1. Create test Supplier records
2. Create test Supplier Inquiry records
3. Test workflow transitions
4. Configure email notifications (optional)
5. Set up portal access for Service Provider Users

## Support

For detailed documentation, see `README.md` in this directory.
