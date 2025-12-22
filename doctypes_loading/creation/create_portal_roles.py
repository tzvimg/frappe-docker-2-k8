"""
Create Portal Roles for Supplier Portal

This script creates the "Supplier Portal User" role with desk_access disabled.
Portal users with this role will only access the web portal, not the desk interface.

Usage:
    From host: ./run_doctype_script.sh creation.create_portal_roles.create_portal_roles
    From container: bench --site development.localhost execute siud.doctypes_loading.creation.create_portal_roles.create_portal_roles
"""

import frappe


@frappe.whitelist()
def create_portal_roles():
    """
    Create the Supplier Portal User role with desk_access=0

    This role is intended for external supplier users who should only
    access the web portal interface, not the full Frappe desk.
    """
    frappe.init(site='development.localhost')
    frappe.connect()

    role_name = "Supplier Portal User"

    # Check if role already exists
    if frappe.db.exists("Role", role_name):
        print(f"ℹ️  Role '{role_name}' already exists. Updating...")
        role = frappe.get_doc("Role", role_name)
    else:
        print(f"✓ Creating role '{role_name}'...")
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": role_name
        })

    # Set portal-specific properties
    role.desk_access = 0  # Critical: disable desk access
    role.disabled = 0

    # Save the role
    if frappe.db.exists("Role", role_name):
        role.save()
        print(f"✓ Updated role '{role_name}' with desk_access=0")
    else:
        role.insert()
        print(f"✓ Created role '{role_name}' with desk_access=0")

    frappe.db.commit()

    print("\n" + "="*60)
    print("✓ Portal role creation completed successfully!")
    print("="*60)
    print(f"\nRole: {role_name}")
    print(f"Desk Access: {role.desk_access} (0 = portal only)")
    print("\nNext Steps:")
    print("1. Run: ./run_doctype_script.sh creation.add_supplier_link_to_user.add_supplier_link_custom_field")
    print("2. Then clear cache: bench --site development.localhost clear-cache")

    return {"success": True, "role": role_name}


if __name__ == "__main__":
    create_portal_roles()
