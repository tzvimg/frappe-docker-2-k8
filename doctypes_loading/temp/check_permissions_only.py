#!/usr/bin/env python3
"""
Check DocType permissions
"""

import frappe

def check_permissions():
    """Check Supplier Inquiry DocType permissions"""

    # Get permissions for Supplier Inquiry
    perms = frappe.get_all(
        "Custom DocPerm",
        filters={"parent": "Supplier Inquiry"},
        fields=["role", "read", "write", "create", "delete", "submit", "email", "print", "if_owner", "permlevel"]
    )

    print("\n=== Custom DocPerm for Supplier Inquiry ===")
    for perm in perms:
        print(f"\nRole: {perm.role}")
        print(f"  Read: {perm.read}, Write: {perm.write}, Create: {perm.create}")
        print(f"  If Owner: {perm.if_owner}, Permlevel: {perm.permlevel}")

    # Get default permissions from DocType
    doc = frappe.get_doc("DocType", "Supplier Inquiry")
    print("\n\n=== Standard Permissions from DocType ===")
    for perm in doc.permissions:
        print(f"\nRole: {perm.role}")
        print(f"  Read: {perm.read}, Write: {perm.write}, Create: {perm.create}")
        print(f"  If Owner: {perm.if_owner}, Permlevel: {perm.permlevel}")

if __name__ == "__main__":
    check_permissions()
