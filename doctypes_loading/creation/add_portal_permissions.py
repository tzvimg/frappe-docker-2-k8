"""
Add Portal Permissions to DocTypes

This script adds "Supplier Portal User" role permissions to:
1. Supplier Inquiry DocType - Read, Write, Create, Email, Print + "If Owner"
2. Supplier DocType - Read, Write + "If Owner"

Usage:
    From host: ./run_doctype_script.sh creation.add_portal_permissions.add_portal_permissions
    From container: bench --site development.localhost execute siud.doctypes_loading.creation.add_portal_permissions.add_portal_permissions
"""

import frappe


def add_permission(doctype, role, permlevel=0, if_owner=0, read=0, write=0, create=0,
                   delete=0, submit=0, cancel=0, amend=0, report=0, export=0,
                   import_data=0, share=0, print_access=0, email=0, set_user_permissions=0):
    """
    Add or update a permission rule for a DocType and role
    """
    # Check if permission already exists
    existing = frappe.db.get_value(
        "Custom DocPerm",
        {
            "parent": doctype,
            "role": role,
            "permlevel": permlevel
        },
        "name"
    )

    if existing:
        print(f"  ℹ️  Permission already exists for {role} on {doctype}. Updating...")
        perm = frappe.get_doc("Custom DocPerm", existing)
    else:
        print(f"  ✓ Creating permission for {role} on {doctype}...")
        perm = frappe.get_doc({
            "doctype": "Custom DocPerm",
            "parent": doctype,
            "parenttype": "DocType",
            "parentfield": "permissions",
            "role": role,
            "permlevel": permlevel
        })

    # Set permissions
    perm.if_owner = if_owner
    perm.read = read
    perm.write = write
    perm.create = create
    perm.delete = delete
    perm.submit = submit
    perm.cancel = cancel
    perm.amend = amend
    perm.report = report
    perm.export = export
    perm.import_data = import_data  # Changed from 'import' to 'import_data'
    perm.share = share
    perm.print = print_access  # Changed from 'print' to 'print_access'
    perm.email = email
    perm.set_user_permissions = set_user_permissions

    # Save
    if existing:
        perm.save()
        print(f"  ✓ Updated permission for {role} on {doctype}")
    else:
        perm.insert()
        print(f"  ✓ Created permission for {role} on {doctype}")

    return perm


@frappe.whitelist()
def add_portal_permissions():
    """
    Add Supplier Portal User permissions to Supplier Inquiry and Supplier DocTypes
    """
    frappe.init(site='development.localhost')
    frappe.connect()

    role = "Supplier Portal User"

    print("\n" + "="*60)
    print("Adding Portal Permissions")
    print("="*60 + "\n")

    # 1. Supplier Inquiry permissions
    print(f"1. Adding permissions to Supplier Inquiry DocType...")
    add_permission(
        doctype="Supplier Inquiry",
        role=role,
        permlevel=0,
        if_owner=1,  # Critical: Users only see their own records
        read=1,
        write=1,
        create=1,
        email=1,
        print_access=1,
        delete=0,  # Don't allow deletion
        submit=0,
        cancel=0,
        amend=0,
        report=0,
        export=0,
        import_data=0,
        share=0,
        set_user_permissions=0
    )

    # 2. Supplier permissions
    print(f"\n2. Adding permissions to Supplier DocType...")
    add_permission(
        doctype="Supplier",
        role=role,
        permlevel=0,
        if_owner=1,  # Critical: Users only see their own supplier record
        read=1,
        write=1,
        create=0,  # Suppliers don't create new supplier records
        email=0,
        print_access=0,
        delete=0,
        submit=0,
        cancel=0,
        amend=0,
        report=0,
        export=0,
        import_data=0,
        share=0,
        set_user_permissions=0
    )

    frappe.db.commit()

    # Clear cache to ensure permissions are applied
    frappe.clear_cache(doctype="Supplier Inquiry")
    frappe.clear_cache(doctype="Supplier")

    print("\n" + "="*60)
    print("✓ Portal permissions added successfully!")
    print("="*60)
    print(f"\nRole: {role}")
    print("\nSupplier Inquiry Permissions:")
    print("  - Read: ✓")
    print("  - Write: ✓")
    print("  - Create: ✓")
    print("  - Email: ✓")
    print("  - Print: ✓")
    print("  - If Owner: ✓ (users only see their own inquiries)")
    print("\nSupplier Permissions:")
    print("  - Read: ✓")
    print("  - Write: ✓")
    print("  - If Owner: ✓ (users only see their linked supplier)")
    print("\nNext Steps:")
    print("1. Verify permissions in UI: DocType → Permissions")
    print("2. Proceed to Phase 2: Implement has_website_permission() functions")

    return {"success": True}


if __name__ == "__main__":
    add_portal_permissions()
