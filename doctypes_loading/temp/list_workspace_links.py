"""
Check workspace links to debug empty sidebar
"""

import frappe
import json


@frappe.whitelist()
def check():
    """List workspace details"""

    print("\n" + "="*60)
    print("Workspace 'Siud' Details")
    print("="*60 + "\n")

    # Try to find the workspace by different names
    for name in ["Siud", "Supplier and Inquiry Management", "ניהול ספקים ופניות"]:
        if frappe.db.exists("Workspace", name):
            ws = frappe.get_doc("Workspace", name)
            print(f"Found workspace: {ws.name}")
            print(f"  Title: {ws.title}")
            print(f"  Label: {ws.label}")
            print(f"  Public: {ws.public}")
            print(f"  Hidden: {ws.is_hidden}")
            print(f"  Links count: {len(ws.links)}")
            print(f"  Shortcuts count: {len(ws.shortcuts)}")

            print(f"\n  Links:")
            for link in ws.links:
                if link.type == "Card Break":
                    print(f"    --- {link.label} ---")
                else:
                    print(f"    • {link.label} → {link.link_to}")

            print("\n" + "="*60 + "\n")
            return {"success": True}

    print("No Siud workspace found!")
    print("="*60 + "\n")
    return {"success": False}
