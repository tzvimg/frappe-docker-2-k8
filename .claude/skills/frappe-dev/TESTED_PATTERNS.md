# Tested Workflow and Workspace Creation Patterns

This document contains **production-tested** patterns extracted from working scripts in the siud app.

## ✓ Workflow Creation Pattern (TESTED & WORKING)

Based on: `doctypes_loading/creation/create_supplier_inquiry_workflow.py`

### Critical Success Factors:

1. **Create Workflow State documents FIRST** ⚠️ **CRITICAL**
   - Before creating a Workflow, you must create Workflow State documents
   - Each state name must exist as a separate Workflow State document
   - See "Step 0" in the template below

2. **`doc_status` MUST be a STRING, not int**
   - ✓ Correct: `'doc_status': '0'`
   - ✗ Wrong: `'doc_status': 0`

3. **NEVER use `doc_status: '2'` in workflows** ⚠️ **CRITICAL**
   - ✓ Use '0' for draft/editable states
   - ✓ Use '1' for final states (completed, cancelled, closed)
   - ✗ **DON'T** use '2' - causes "Illegal Document Status" error
   - This pattern is confirmed from working Supplier Inquiry workflow

4. **`allow_edit` cannot be empty string**
   - ✓ Use 'All' for states that anyone can edit
   - ✓ Use specific role like 'System Manager' for restricted states
   - ✗ Empty string '' causes "Mandatory Error"

5. **Use `frappe.flags.ignore_links = True`**
   - Prevents link validation errors during insert
   - Must be set before insert and reset after

6. **Add states and transitions in the initial `frappe.get_doc()` call**
   - Don't use `workflow.append()` after creation
   - Include all child tables in the initial dictionary

### Working Template:

```python
import frappe

@frappe.whitelist()
def create_workflow():
    """Create workflow - tested pattern"""

    # STEP 0: Create Workflow State documents FIRST (CRITICAL!)
    state_names = ['Draft', 'Pending', 'Approved', 'Rejected']
    for state_name in state_names:
        if not frappe.db.exists('Workflow State', state_name):
            state = frappe.get_doc({
                'doctype': 'Workflow State',
                'workflow_state_name': state_name
            })
            state.insert(ignore_permissions=True)
    frappe.db.commit()

    # Check if workflow exists
    if frappe.db.exists("Workflow", "My Workflow"):
        frappe.msgprint("Workflow already exists")
        return {"success": False, "message": "Already exists"}

    # Create workflow with all data at once
    workflow = frappe.get_doc({
        'doctype': 'Workflow',
        'workflow_name': 'My Workflow',
        'document_type': 'My DocType',  # Must exist first
        'is_active': 1,
        'workflow_state_field': 'status',  # Field in your DocType
        'send_email_alert': 0,  # Optional

        # Define all states
        'states': [
            {
                'state': 'Draft',  # Must match status field options
                'doc_status': '0',  # STRING! 0=draft, 1=submitted, 2=cancelled
                'allow_edit': 'System Manager',  # Role name
                'message': 'Document is in draft state',  # Optional
            },
            {
                'state': 'Pending',
                'doc_status': '0',
                'allow_edit': 'Approver',
            },
            {
                'state': 'Approved',
                'doc_status': '1',  # Submitted/Final
                'allow_edit': 'System Manager',  # Can't be empty
            },
            {
                'state': 'Rejected',
                'doc_status': '1',  # Use '1', NOT '2'!
                'allow_edit': 'System Manager',  # Can't be empty
            },
        ],

        # Define all transitions
        'transitions': [
            {
                'state': 'Draft',  # From state (must exist in states above)
                'action': 'Submit for Approval',  # Button text
                'next_state': 'Pending',  # To state (must exist in states above)
                'allowed': 'System Manager',  # Who can do this transition
                'allow_self_approval': 0,  # 0 or 1
                'condition': '',  # Optional: Python expression like 'doc.field_name'
            },
            {
                'state': 'Pending',
                'action': 'Approve',
                'next_state': 'Approved',
                'allowed': 'Approver',
                'allow_self_approval': 0,
            },
            {
                'state': 'Pending',
                'action': 'Reject',
                'next_state': 'Rejected',
                'allowed': 'Approver',
                'allow_self_approval': 0,
            },
        ]
    })

    # Insert and commit
    workflow.insert()
    frappe.db.commit()
    frappe.msgprint(f"✓ Created workflow with {len(workflow.states)} states and {len(workflow.transitions)} transitions")

    return {"success": True, "workflow": "My Workflow"}
```

### Common Workflow Errors and Fixes:

| Error | Cause | Fix |
|-------|-------|-----|
| "Workflow State [Name] not found" | Workflow State documents don't exist | Create Workflow State documents BEFORE creating workflow |
| "Illegal Document Status for Cancelled" | Using `doc_status: '2'` in workflow | Use `doc_status: '1'` for all final states (cancelled, rejected, closed) |
| "allow_edit, allow_edit" (Mandatory) | Empty string for `allow_edit` | Use 'All' or specific role like 'System Manager' |
| "Could not find Row #1: State..." | Link validation or missing states | Use `frappe.flags.ignore_links = True` before insert |
| `doc_status` type error | `doc_status` is int instead of string | Change `0` to `'0'` (string) |
| State not found in transitions | Typo in state name | Ensure exact match between states and transitions |
| Workflow doesn't appear | `workflow_state_field` doesn't match DocType field | Check field name in DocType |

---

## ✓ Workspace Creation Pattern (TESTED & WORKING)

Based on: `doctypes_loading/creation/create_siud_workspace_complete.py`

### Critical Success Factors:

1. **Set `name` explicitly** - Workspace doesn't auto-name like DocTypes
2. **Set `label` to same value as `name`**
3. **Include metadata fields**: `creation`, `modified`, `owner`, `modified_by`
4. **Add all child tables in initial dict**: `links`, `shortcuts`
5. **Set `content` as JSON string** for visual layout
6. **Use `ignore_permissions=True, ignore_if_duplicate=True`** when inserting

### Working Template:

```python
import frappe
import json
from datetime import datetime

@frappe.whitelist()
def create_workspace():
    """Create workspace - tested pattern"""

    workspace_name = "My Workspace"  # English name for clean URLs
    workspace_title = "My Workspace Title"  # Display title (can be Hebrew)

    # Delete if exists
    if frappe.db.exists("Workspace", workspace_name):
        frappe.delete_doc("Workspace", workspace_name, force=True)
        frappe.db.commit()
        print(f"Deleted existing workspace: {workspace_name}")

    # Get current timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # Define links (sidebar items)
    links = [
        # Section header
        {
            "type": "Card Break",
            "label": "My Section",  # Section title
            "hidden": 0,
            "is_query_report": 0,
            "link_count": 0,
            "onboard": 0,
        },
        # Links under the section
        {
            "type": "Link",
            "link_type": "DocType",
            "link_to": "Patient",  # DocType name (must exist)
            "label": "Patients",  # Display name
            "hidden": 0,
            "is_query_report": 0,
            "link_count": 0,
            "onboard": 0,
            "dependencies": "",
        },
        {
            "type": "Link",
            "link_type": "DocType",
            "link_to": "Doctor",
            "label": "Doctors",
            "hidden": 0,
            "is_query_report": 0,
            "link_count": 0,
            "onboard": 0,
            "dependencies": "",
        },
    ]

    # Define shortcuts (quick access buttons at top)
    shortcuts = [
        {
            "type": "DocType",
            "link_to": "Patient",  # DocType name
            "label": "Patients",  # Display name
            "doc_view": "List",  # List or Form
            "stats_filter": "[]",
        },
        {
            "type": "DocType",
            "link_to": "Appointment",
            "label": "Appointments",
            "doc_view": "List",
            "stats_filter": "[]",
        },
    ]

    # Create content layout (visual arrangement)
    content = []

    # Add shortcuts in a row (max 4 per row)
    col_width = 12 // min(len(shortcuts), 4) if shortcuts else 12
    for idx, shortcut in enumerate(shortcuts):
        content.append({
            "id": f"shortcut_{idx}",
            "type": "shortcut",
            "data": {"shortcut_name": shortcut["label"], "col": col_width}
        })

    # Add spacer
    content.append({
        "id": "spacer_main",
        "type": "spacer",
        "data": {"col": 12}
    })

    # Add card for the section
    content.append({
        "id": "card_0",
        "type": "card",
        "data": {"card_name": "My Section", "col": 12}
    })

    # Create complete workspace data
    workspace_data = {
        "doctype": "Workspace",
        "name": workspace_name,  # CRITICAL: Set explicitly
        "label": workspace_name,  # CRITICAL: Set to same value
        "creation": now,
        "modified": now,
        "modified_by": "Administrator",
        "owner": "Administrator",
        "docstatus": 0,
        "idx": 0,
        "title": workspace_title,
        "module": "Test Clinic",  # Your module name
        "icon": "healthcare",  # Icon name
        "public": 1,  # 1=visible to all, 0=private
        "is_hidden": 0,
        "for_user": "",
        "parent_page": "",
        "content": json.dumps(content),  # JSON string
        "charts": [],
        "custom_blocks": [],
        "number_cards": [],
        "quick_lists": [],
        "roles": [],
        "links": links,
        "shortcuts": shortcuts
    }

    # Create and insert
    try:
        workspace = frappe.get_doc(workspace_data)
        workspace.insert(ignore_permissions=True, ignore_if_duplicate=True)
        frappe.db.commit()

        print(f"✓ Created workspace: {workspace.name}")
        print(f"  - Title: {workspace.title}")
        print(f"  - Links: {len(workspace.links)}")
        print(f"  - Shortcuts: {len(workspace.shortcuts)}")
        print(f"  - Access: http://localhost:8000/app/{workspace_name.lower().replace(' ', '-')}")

        # Clear cache
        frappe.clear_cache()

        return {"success": True, "workspace": workspace_name}

    except Exception as e:
        frappe.db.rollback()
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
```

### Common Workspace Errors and Fixes:

| Error | Cause | Fix |
|-------|-------|-----|
| "Name is required" | `name` field not set | Add `"name": workspace_name` to dict |
| Workspace not appearing | Cache not cleared | Run `frappe.clear_cache()` after creation |
| Links not showing | DocType doesn't exist | Check if linked DocTypes exist first |
| Layout broken | Invalid `content` JSON | Use tested pattern above for content structure |

---

## Best Practices from Production Code

### 1. **Check Existence Before Creating**
```python
if frappe.db.exists("Workflow", "My Workflow"):
    frappe.msgprint("Already exists")
    return {"success": False, "message": "Already exists"}
```

### 2. **Delete Before Recreating (for development)**
```python
if frappe.db.exists("Workspace", workspace_name):
    frappe.delete_doc("Workspace", workspace_name, force=True)
    frappe.db.commit()
```

### 3. **Verify Dependencies First**
```python
# For workflows - check DocType exists
if not frappe.db.exists("DocType", "My DocType"):
    frappe.throw("DocType 'My DocType' must be created first")

# For workspaces - filter to existing DocTypes
if doctype_exists(doctype_name):
    # Add to workspace
    pass
```

### 4. **Always Commit After Insert**
```python
doc.insert()
frappe.db.commit()  # Don't forget this!
```

### 5. **Clear Cache After Creating Workspaces**
```python
frappe.clear_cache()
# Or from command line: bench --site development.localhost clear-cache
```

---

## Integration with frappe-dev Skill

### Add to skill.md:

```markdown
## Creating Workflows and Workspaces

**IMPORTANT:** See `TESTED_PATTERNS.md` for production-tested patterns.

### Quick Reference:

**Workflows:**
- ✓ Use `'doc_status': '0'` (string, not int)
- ✓ Add states and transitions in initial `frappe.get_doc()` call
- ✓ Ensure state names match exactly between states and transitions

**Workspaces:**
- ✓ Set `name` and `label` explicitly in the dict
- ✓ Include metadata: `creation`, `modified`, `owner`, `modified_by`
- ✓ Add `links` and `shortcuts` as child tables
- ✓ Use `ignore_permissions=True, ignore_if_duplicate=True` when inserting
- ✓ Clear cache after creation

See `TESTED_PATTERNS.md` for complete working examples.
```

---

## Summary

These patterns are extracted from production code that is actively running in the siud app. The key differences from failed attempts:

**Workflows:**
- String `doc_status` instead of int
- Single-pass creation instead of multi-step

**Workspaces:**
- Explicit `name` and `label` fields
- Complete metadata population
- Proper JSON content structure

Both patterns emphasize creating the complete object in one `frappe.get_doc()` call rather than incremental building, which avoids validation issues during the insert phase.
