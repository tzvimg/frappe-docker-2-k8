"""
Add Supplier Link Custom Field to User DocType

This script adds a "supplier_link" custom field to the User DocType.
This field links portal users to their corresponding Supplier records,
enabling data access control (users can only see their own supplier's data).

Usage:
    From host: ./run_doctype_script.sh creation.add_supplier_link_to_user.add_supplier_link_custom_field
    From container: bench --site development.localhost execute siud.doctypes_loading.creation.add_supplier_link_to_user.add_supplier_link_custom_field
"""

import frappe


@frappe.whitelist()
def add_supplier_link_custom_field():
    """
    Add supplier_link custom field to User DocType

    This field creates a Link to the Supplier DocType, allowing each
    portal user to be associated with a specific supplier record.
    This relationship is critical for permission filtering.
    """
    frappe.init(site='development.localhost')
    frappe.connect()

    field_name = "supplier_link"
    doctype = "User"

    # Check if custom field already exists
    if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}):
        print(f"ℹ️  Custom field '{field_name}' already exists in {doctype}. Updating...")
        custom_field = frappe.get_doc("Custom Field", {"dt": doctype, "fieldname": field_name})
    else:
        print(f"✓ Creating custom field '{field_name}' in {doctype}...")
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": doctype,
            "fieldname": field_name
        })

    # Set field properties
    custom_field.label = "Supplier Link"
    custom_field.fieldtype = "Link"
    custom_field.options = "Supplier"
    custom_field.insert_after = "username"  # Place after username field
    custom_field.allow_in_quick_entry = 0
    custom_field.bold = 0
    custom_field.collapsible = 0
    custom_field.columns = 0
    custom_field.default = None
    custom_field.depends_on = None
    custom_field.description = "Link to Supplier record for portal access control"
    custom_field.fetch_from = None
    custom_field.fetch_if_empty = 0
    custom_field.hidden = 0
    custom_field.hide_border = 0
    custom_field.hide_days = 0
    custom_field.hide_seconds = 0
    custom_field.ignore_user_permissions = 0
    custom_field.ignore_xss_filter = 0
    custom_field.in_global_search = 0
    custom_field.in_list_view = 0
    custom_field.in_preview = 0
    custom_field.in_standard_filter = 1  # Enable filtering by this field
    custom_field.length = 0
    custom_field.mandatory_depends_on = None
    custom_field.no_copy = 0
    custom_field.non_negative = 0
    custom_field.permlevel = 0
    custom_field.precision = ""
    custom_field.print_hide = 1  # Hide from print
    custom_field.print_hide_if_no_value = 0
    custom_field.print_width = None
    custom_field.read_only = 0
    custom_field.read_only_depends_on = None
    custom_field.report_hide = 0
    custom_field.reqd = 0  # Not required for all users, only portal users
    custom_field.search_index = 0
    custom_field.show_dashboard = 0
    custom_field.translatable = 0
    custom_field.unique = 0
    custom_field.width = None

    # Save the custom field
    if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}):
        custom_field.save()
        print(f"✓ Updated custom field '{field_name}' in {doctype}")
    else:
        custom_field.insert()
        print(f"✓ Created custom field '{field_name}' in {doctype}")

    frappe.db.commit()

    # Clear cache to ensure the field is immediately visible
    frappe.clear_cache(doctype=doctype)

    print("\n" + "="*60)
    print("✓ Supplier link custom field creation completed!")
    print("="*60)
    print(f"\nDocType: {doctype}")
    print(f"Field: {field_name}")
    print(f"Type: Link → Supplier")
    print(f"Purpose: Links portal users to their supplier records")
    print("\nNext Steps:")
    print("1. Run: bench --site development.localhost clear-cache")
    print("2. Update permissions for Supplier Inquiry and Supplier DocTypes")
    print("3. Test by creating a test user and linking to a supplier")

    return {"success": True, "field": field_name, "doctype": doctype}


if __name__ == "__main__":
    add_supplier_link_custom_field()
