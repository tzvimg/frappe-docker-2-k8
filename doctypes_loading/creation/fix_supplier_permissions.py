#!/usr/bin/env python3
"""
Fix Supplier DocType permissions by removing 'if_owner' flag
"""

import frappe

def fix_supplier_permissions():
    """Remove if_owner flag from Supplier Portal User permissions for Supplier DocType"""

    try:
        # Remove the Custom DocPerm with if_owner=1
        custom_perms = frappe.get_all(
            "Custom DocPerm",
            filters={
                "parent": "Supplier",
                "role": "Supplier Portal User"
            },
            pluck="name"
        )

        for perm_name in custom_perms:
            frappe.delete_doc("Custom DocPerm", perm_name)
            print(f"✅ Deleted old Custom DocPerm: {perm_name}")

        frappe.db.commit()

        # Add new permission without if_owner flag
        perm = frappe.get_doc({
            "doctype": "Custom DocPerm",
            "parent": "Supplier",
            "parenttype": "DocType",
            "parentfield": "permissions",
            "role": "Supplier Portal User",
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 0,
            "delete": 0,
            "submit": 0,
            "cancel": 0,
            "amend": 0,
            "email": 0,
            "print": 0,
            "if_owner": 0,  # Remove the if_owner restriction
        })

        perm.insert()
        frappe.db.commit()

        print(f"\n✅ Created new Custom DocPerm for Supplier without if_owner flag")
        print(f"   Role: Supplier Portal User")
        print(f"   Permissions: Read, Write")
        print(f"   If Owner: 0 (disabled)")
        print(f"\nSecurity is now handled by has_website_permission() function")
        print(f"which checks the supplier_link field.")

        return {"success": True, "message": "Supplier permissions fixed successfully"}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        frappe.db.rollback()
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    fix_supplier_permissions()
