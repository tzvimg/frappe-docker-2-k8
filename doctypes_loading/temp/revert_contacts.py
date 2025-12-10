"""
Revert contacts table changes - restore original Supplier form
"""
import frappe
import json
import os
import shutil

def revert_supplier_changes():
    """Remove contacts table and restore original fields"""

    # Get the JSON file path
    doctype_path = frappe.get_module_path(
        "siud", "doctype", "supplier", "supplier.json"
    )

    # Read the JSON
    with open(doctype_path, 'r', encoding='utf-8') as f:
        supplier_json = json.load(f)

    # Remove contacts from field_order
    if "contacts" in supplier_json["field_order"]:
        supplier_json["field_order"].remove("contacts")
        print("✓ Removed contacts from field_order")

    # Remove contacts field definition
    supplier_json["fields"] = [
        field for field in supplier_json["fields"]
        if field.get("fieldname") != "contacts"
    ]
    print("✓ Removed contacts field definition")

    # Unhide old fields
    for field in supplier_json["fields"]:
        if field["fieldname"] in ["address", "phone", "email", "column_break_1"]:
            if "hidden" in field:
                del field["hidden"]
    print("✓ Restored original contact fields")

    # Update modified timestamp
    supplier_json["modified"] = frappe.utils.now()

    # Write back
    with open(doctype_path, 'w', encoding='utf-8') as f:
        json.dump(supplier_json, f, indent=1, ensure_ascii=False)

    print("✓ Reverted Supplier DocType")

def delete_supplier_contact_doctype():
    """Delete the Supplier Contact child table"""

    if not frappe.db.exists("DocType", "Supplier Contact"):
        print("✓ Supplier Contact already deleted")
        return

    # Delete the DocType
    frappe.delete_doc("DocType", "Supplier Contact", force=True)
    frappe.db.commit()
    print("✓ Deleted Supplier Contact DocType")

    # Delete the directory
    doctype_dir = frappe.get_module_path(
        "siud", "doctype", "supplier_contact"
    )
    if os.path.exists(doctype_dir):
        shutil.rmtree(doctype_dir)
        print("✓ Deleted Supplier Contact directory")

def revert_all():
    """Revert all changes"""
    print("Reverting contacts table changes...")
    revert_supplier_changes()
    delete_supplier_contact_doctype()
    print("\n✓ All changes reverted!")
    print("  Run: bench --site development.localhost reload-doctype Supplier")
    print("  Then: bench --site development.localhost clear-cache")

if __name__ == "__main__":
    revert_all()
