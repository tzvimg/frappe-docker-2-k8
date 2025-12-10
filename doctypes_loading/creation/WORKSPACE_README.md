# Siud Workspace Creation

This directory contains the complete, tested script for creating the Siud workspace.

## Quick Start

To create or recreate the Siud workspace, run:

```bash
# From the project root (/home/tzvi/frappe/)
./run_doctype_script.sh creation.create_siud_workspace_complete.create_workspace
```

That's it! The script will:
- Delete any existing workspace
- Create a new workspace with all links and shortcuts
- Set up the visual layout (content field)
- Clear the cache automatically

## What Gets Created

**Workspace Name:** Siud
**Title:** ניהול ספקים ופניות (Supplier and Inquiry Management)

### Sections

1. **ניהול ספקים** (Service Provider Management)
   - ספקים (Suppliers)
   - אנשי קשר (Contact Persons)
   - תפקידים (Roles)
   - תחומי פעילות (Activity Domains)

2. **ניהול פניות** (Inquiry Management)
   - פניות ספקים (Supplier Inquiries)
   - קטגוריות נושאי פנייה (Inquiry Topic Categories)

### Quick Shortcuts
- פניות ספקים (Supplier Inquiries)
- ספקים (Suppliers)
- אנשי קשר (Contact Persons)

## Access

After creation, access the workspace at:
- **Direct URL:** http://localhost:8000/app/siud
- **Or:** Look for "ניהול ספקים ופניות" in the workspace sidebar at http://localhost:8000

## Additional Commands

### Delete Workspace

```bash
./run_doctype_script.sh creation.create_siud_workspace_complete.delete_workspace
```

### Manual Execution (from inside container)

```bash
# Enter container
docker exec -it frappe_docker_devcontainer-frappe-1 bash
cd /workspace/development/frappe-bench

# Create workspace
bench --site development.localhost execute siud.doctypes_loading.creation.create_siud_workspace_complete.create_workspace

# Delete workspace
bench --site development.localhost execute siud.doctypes_loading.creation.create_siud_workspace_complete.delete_workspace
```

## Troubleshooting

If the workspace doesn't appear after creation:

1. **Hard refresh your browser:**
   - Windows/Linux: `Ctrl + F5` or `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`

2. **Manually clear cache:**
   ```bash
   docker exec frappe_docker_devcontainer-frappe-1 bash -c \
     "cd /workspace/development/frappe-bench && bench --site development.localhost clear-cache"
   ```

3. **Verify it was created:**
   ```bash
   docker exec frappe_docker_devcontainer-frappe-1 bash -c \
     "cd /workspace/development/frappe-bench && bench --site development.localhost console" << 'EOF'
   import frappe
   if frappe.db.exists('Workspace', 'Siud'):
       print('✓ Workspace exists')
   else:
       print('✗ Workspace not found')
   EOF
   ```

## Script Details

**File:** `creation/create_siud_workspace_complete.py`

The script uses the complete JSON-like data structure approach to create the workspace, including:
- All metadata fields (creation, modified, owner, etc.)
- The critical `label` field required for Workspace auto-naming
- Complete links structure with Card Breaks and Links
- Shortcuts for quick access
- Content field for visual layout (shortcuts + cards)

The script automatically handles:
- Deleting existing workspace if it exists
- Creating all sections and links
- Setting up the visual layout
- Clearing cache after creation

## Notes

- The workspace is **non-standard** (can be customized)
- It's **public** (visible to all users with appropriate permissions)
- The workspace DocTypes must exist before creation (Supplier, Contact Person, etc.)
- The script has been tested and works reliably
