"""
Complete Siud Workspace Creation Script

This script creates a fully functional workspace for the Supplier Inquiry Management System.
Run this script anytime to recreate the workspace from scratch.

Usage:
    From host: ./run_doctype_script.sh creation.create_siud_workspace_complete.create_workspace
    From container: bench --site development.localhost execute siud.doctypes_loading.creation.create_siud_workspace_complete.create_workspace
"""

import frappe
import json
from datetime import datetime
from frappe import _


@frappe.whitelist()
def create_workspace():
    """Create the complete Siud workspace with all links, shortcuts, and content"""

    workspace_name = "Siud"

    print(f"\n{'='*60}")
    print(f"Creating Siud Workspace for Supplier Inquiry Management")
    print(f"{'='*60}\n")

    # Step 1: Delete existing workspace if it exists
    if frappe.db.exists("Workspace", workspace_name):
        print(f"⚠️  Workspace '{workspace_name}' already exists. Deleting...")
        frappe.delete_doc("Workspace", workspace_name, force=True)
        frappe.db.commit()
        print(f"✓ Deleted existing workspace\n")

    # Step 2: Create complete workspace data structure (like a JSON export)
    print(f"Creating workspace data structure...")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    workspace_data = {
        "doctype": "Workspace",
        "name": workspace_name,
        "label": workspace_name,  # This is required for autoname!
        "creation": now,
        "modified": now,
        "modified_by": "Administrator",
        "owner": "Administrator",
        "docstatus": 0,
        "idx": 0,
        "title": "ניהול ספקים ופניות",
        "module": "Siud",
        "icon": "healthcare",
        "public": 1,
        "is_hidden": 0,
        "for_user": "",
        "parent_page": "",
        "content": None,  # Will be set later
        "charts": [],
        "custom_blocks": [],
        "number_cards": [],
        "quick_lists": [],
        "roles": [],
        "links": [
            # Section 1: Service Provider Management
            {
                "type": "Card Break",
                "label": "ניהול ספקים",
                "hidden": 0,
                "is_query_report": 0,
                "link_count": 0,
                "onboard": 0,
            },
            {
                "type": "Link",
                "link_type": "DocType",
                "link_to": "Supplier",
                "label": "ספקים",
                "hidden": 0,
                "is_query_report": 0,
                "link_count": 0,
                "onboard": 0,
                "dependencies": "",
            },
            {
                "type": "Link",
                "link_type": "DocType",
                "link_to": "Contact Person",
                "label": "אנשי קשר",
                "hidden": 0,
                "is_query_report": 0,
                "link_count": 0,
                "onboard": 0,
                "dependencies": "",
            },
            {
                "type": "Link",
                "link_type": "DocType",
                "link_to": "Supplier Role",
                "label": "תפקידים",
                "hidden": 0,
                "is_query_report": 0,
                "link_count": 0,
                "onboard": 0,
                "dependencies": "",
            },
            {
                "type": "Link",
                "link_type": "DocType",
                "link_to": "Activity Domain Category",
                "label": "תחומי פעילות",
                "hidden": 0,
                "is_query_report": 0,
                "link_count": 0,
                "onboard": 0,
                "dependencies": "",
            },
            # Section 2: Inquiry Management
            {
                "type": "Card Break",
                "label": "ניהול פניות",
                "hidden": 0,
                "is_query_report": 0,
                "link_count": 0,
                "onboard": 0,
            },
            {
                "type": "Link",
                "link_type": "DocType",
                "link_to": "Supplier Inquiry",
                "label": "פניות ספקים",
                "hidden": 0,
                "is_query_report": 0,
                "link_count": 0,
                "onboard": 0,
                "dependencies": "",
            },
            {
                "type": "Link",
                "link_type": "DocType",
                "link_to": "Inquiry Topic Category",
                "label": "קטגוריות נושאי פנייה",
                "hidden": 0,
                "is_query_report": 0,
                "link_count": 0,
                "onboard": 0,
                "dependencies": "",
            }
        ],
        "shortcuts": [
            {
                "type": "DocType",
                "link_to": "Supplier Inquiry",
                "label": "פניות ספקים",
                "doc_view": "List",
                "stats_filter": "[]",
            },
            {
                "type": "DocType",
                "link_to": "Supplier",
                "label": "ספקים",
                "doc_view": "List",
                "stats_filter": "[]",
            },
            {
                "type": "DocType",
                "link_to": "Contact Person",
                "label": "אנשי קשר",
                "doc_view": "List",
                "stats_filter": "[]",
            }
        ]
    }

    # Step 3: Create content field (visual layout)
    print(f"Setting workspace content layout...")

    content = [
        {"id": "shortcut_supplier_inquiry", "type": "shortcut", "data": {"shortcut_name": "פניות ספקים", "col": 4}},
        {"id": "shortcut_supplier", "type": "shortcut", "data": {"shortcut_name": "ספקים", "col": 4}},
        {"id": "shortcut_contact", "type": "shortcut", "data": {"shortcut_name": "אנשי קשר", "col": 4}},
        {"id": "spacer_main", "type": "spacer", "data": {"col": 12}},
        {"id": "card_suppliers", "type": "card", "data": {"card_name": "ניהול ספקים", "col": 6}},
        {"id": "card_inquiries", "type": "card", "data": {"card_name": "ניהול פניות", "col": 6}},
    ]

    workspace_data["content"] = json.dumps(content)

    # Step 4: Create workspace from data structure
    print(f"Creating workspace document...")
    try:
        workspace = frappe.get_doc(workspace_data)
        workspace.insert(ignore_permissions=True, ignore_if_duplicate=True)
        frappe.db.commit()

        print(f"\n{'='*60}")
        print(f"✓ SUCCESS! Workspace created successfully")
        print(f"{'='*60}\n")

        print(f"Workspace Details:")
        print(f"  - Name: {workspace.name}")
        print(f"  - Title: {workspace.title}")
        print(f"  - Module: {workspace.module}")
        print(f"  - Links: {len(workspace.links)} items in 2 sections")
        print(f"  - Shortcuts: {len(workspace.shortcuts)} quick access buttons")

        print(f"\nAccess URLs:")
        print(f"  - Direct: http://localhost:8000/app/siud")
        print(f"  - Main: http://localhost:8000")

        print(f"\n💡 Next Steps:")
        print(f"   1. Refresh your browser (Ctrl+F5 or Cmd+Shift+R)")
        print(f"   2. Look for 'ניהול ספקים ופניות' in the sidebar")

        print(f"\n📝 To recreate this workspace in the future:")
        print(f"   ./run_doctype_script.sh creation.create_siud_workspace_complete.create_workspace")
        print(f"\n{'='*60}\n")

        # Clear cache automatically
        frappe.clear_cache()
        print(f"✓ Cache cleared automatically\n")

        return {"success": True, "workspace": workspace_name}

    except Exception as e:
        frappe.db.rollback()
        print(f"\n{'='*60}")
        print(f"✗ ERROR: Failed to create workspace")
        print(f"{'='*60}\n")
        print(f"Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        raise


@frappe.whitelist()
def delete_workspace():
    """Delete the Siud workspace (utility function)"""

    workspace_name = "Siud"

    if frappe.db.exists("Workspace", workspace_name):
        frappe.delete_doc("Workspace", workspace_name, force=True)
        frappe.db.commit()
        print(f"✓ Deleted workspace '{workspace_name}'")
        return {"success": True}
    else:
        print(f"⚠️  Workspace '{workspace_name}' does not exist")
        return {"success": False, "message": "Workspace not found"}


if __name__ == "__main__":
    create_workspace()
