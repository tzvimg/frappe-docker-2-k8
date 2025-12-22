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


def doctype_exists(doctype_name):
    """Check if a DocType exists"""
    return frappe.db.exists("DocType", doctype_name)


@frappe.whitelist()
def create_workspace():
    """Create the complete Siud workspace with all links, shortcuts, and content"""

    workspace_name = "Siud"  # English name for clean URLs
    workspace_title = "Supplier and Inquiry Management"  # English title for display

    print(f"\n{'='*60}")
    print(f"Creating Siud Workspace for Supplier Inquiry Management")
    print(f"{'='*60}\n")

    # Step 1: Delete existing workspaces if they exist (both possible names)
    existing_workspaces = ["Siud", "ניהול ספקים ופניות"]
    for ws_name in existing_workspaces:
        if frappe.db.exists("Workspace", ws_name):
            print(f"⚠️  Workspace '{ws_name}' already exists. Deleting...")
            frappe.delete_doc("Workspace", ws_name, force=True)
            frappe.db.commit()
            print(f"✓ Deleted existing workspace '{ws_name}'\n")

    # Step 2: Define all possible links (will filter to only existing DocTypes)
    print(f"Checking which DocTypes exist...")

    all_possible_links = [
        # Section 1: Service Provider Management
        ("section", "ניהול נותני שירות"),
        ("link", "Service Provider", "נותני שירות"),
        ("link", "Service Provider Branch", "סניפי נותני שירות"),
        ("link", "Service Provider Application", "בקשות נותני שירות"),

        # Section 2: Contract & Document Management
        ("section", "חוזים ומסמכים"),
        ("link", "Contract", "חוזים"),
        ("link", "Document Approval", "אישורי מסמכים"),

        # Section 3: Caregiver Management
        ("section", "ניהול מטפלים"),
        ("link", "Caregiver", "מטפלים"),

        # Section 4: Suppliers (Legacy/Reference)
        ("section", "ניהול ספקים"),
        ("link", "Supplier", "ספקים"),
        ("link", "Contact Person", "אנשי קשר"),
        ("link", "Supplier Role", "תפקידים"),
        ("link", "Activity Domain Category", "תחומי פעילות"),

        # Section 5: Inquiry Management
        ("section", "ניהול פניות"),
        ("link", "Supplier Inquiry", "פניות ספקים"),
        ("link", "Inquiry Topic Category", "קטגוריות נושאי פנייה"),
    ]

    # Filter links to only include existing DocTypes
    links = []
    section_has_links = {}
    current_section = None

    for item in all_possible_links:
        if item[0] == "section":
            current_section = item[1]
            section_has_links[current_section] = False
        elif item[0] == "link":
            doctype_name = item[1]
            if doctype_exists(doctype_name):
                # Add section if this is the first link in it
                if current_section and not section_has_links[current_section]:
                    links.append({
                        "type": "Card Break",
                        "label": current_section,
                        "hidden": 0,
                        "is_query_report": 0,
                        "link_count": 0,
                        "onboard": 0,
                    })
                    section_has_links[current_section] = True

                # Add the link
                links.append({
                    "type": "Link",
                    "link_type": "DocType",
                    "link_to": doctype_name,
                    "label": item[2],
                    "hidden": 0,
                    "is_query_report": 0,
                    "link_count": 0,
                    "onboard": 0,
                    "dependencies": "",
                })
                print(f"  ✓ Including: {item[2]} ({doctype_name})")
            else:
                print(f"  ⊗ Skipping: {item[2]} ({doctype_name}) - not found")

    # Define all possible shortcuts (will filter to only existing DocTypes)
    all_possible_shortcuts = [
        ("Service Provider", "נותני שירות"),
        ("Service Provider Application", "בקשות נותני שירות"),
        ("Contract", "חוזים"),
        ("Caregiver", "מטפלים"),
        ("Supplier Inquiry", "פניות ספקים"),
        ("Supplier", "ספקים"),
    ]

    shortcuts = []
    for doctype_name, label in all_possible_shortcuts:
        if doctype_exists(doctype_name):
            shortcuts.append({
                "type": "DocType",
                "link_to": doctype_name,
                "label": label,
                "doc_view": "List",
                "stats_filter": "[]",
            })

    print(f"\n✓ Workspace will have {len(links)} links and {len(shortcuts)} shortcuts\n")

    # Step 3: Create complete workspace data structure
    print(f"Creating workspace data structure...")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    workspace_data = {
        "doctype": "Workspace",
        "name": workspace_name,
        "label": workspace_name,  # English name for clean URLs
        "creation": now,
        "modified": now,
        "modified_by": "Administrator",
        "owner": "Administrator",
        "docstatus": 0,
        "idx": 0,
        "title": workspace_title,  # Hebrew title for display
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
        "links": links,  # Use dynamically filtered links
        "shortcuts": shortcuts  # Use dynamically filtered shortcuts
    }

    # Step 4: Create content field (visual layout)
    print(f"Setting workspace content layout...")

    # Create shortcuts for content
    content = []
    col_width = 12 // min(len(shortcuts), 4) if shortcuts else 12  # Max 4 per row

    for idx, shortcut in enumerate(shortcuts):
        shortcut_id = f"shortcut_{idx}"
        content.append({
            "id": shortcut_id,
            "type": "shortcut",
            "data": {"shortcut_name": shortcut["label"], "col": col_width}
        })

    # Add spacer
    content.append({"id": "spacer_main", "type": "spacer", "data": {"col": 12}})

    # Create cards for each section that has links
    sections_with_content = []
    for link in links:
        if link["type"] == "Card Break" and link["label"] not in sections_with_content:
            sections_with_content.append(link["label"])

    card_col = 12 // len(sections_with_content) if sections_with_content else 12

    for idx, section_label in enumerate(sections_with_content):
        card_id = f"card_{idx}"
        content.append({
            "id": card_id,
            "type": "card",
            "data": {"card_name": section_label, "col": card_col}
        })

    workspace_data["content"] = json.dumps(content)

    # Step 5: Create workspace from data structure
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
        print(f"  - Links: {len(workspace.links)} items in {len(sections_with_content)} sections")
        print(f"  - Shortcuts: {len(workspace.shortcuts)} quick access buttons")

        if sections_with_content:
            print(f"\nSidebar Sections:")
            for idx, section in enumerate(sections_with_content, 1):
                print(f"  {idx}. {section}")

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

    workspace_names = ["Siud", "ניהול ספקים ופניות"]
    deleted = False

    for workspace_name in workspace_names:
        if frappe.db.exists("Workspace", workspace_name):
            frappe.delete_doc("Workspace", workspace_name, force=True)
            frappe.db.commit()
            print(f"✓ Deleted workspace '{workspace_name}'")
            deleted = True

    if deleted:
        return {"success": True}
    else:
        print(f"⚠️  No Siud workspaces found")
        return {"success": False, "message": "Workspace not found"}


if __name__ == "__main__":
    create_workspace()
