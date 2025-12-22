"""
Check all workspaces in the system
"""

import frappe


@frappe.whitelist()
def check():
    """List all workspaces"""

    print("\n" + "="*60)
    print("All Workspaces in System")
    print("="*60 + "\n")

    workspaces = frappe.get_all(
        "Workspace",
        fields=["name", "title", "module", "public", "is_hidden"],
        order_by="name"
    )

    for ws in workspaces:
        print(f"Name: {ws.name}")
        print(f"  Title: {ws.title}")
        print(f"  Module: {ws.module}")
        print(f"  Public: {ws.public}")
        print(f"  Hidden: {ws.is_hidden}")
        print()

    print("="*60 + "\n")

    return {"success": True, "count": len(workspaces)}
