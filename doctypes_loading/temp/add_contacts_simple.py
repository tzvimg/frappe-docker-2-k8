"""
Simple approach: Add contacts table to Supplier
"""
import frappe
import json

def add_contacts_field():
    """Add contacts table field to Supplier JSON directly"""

    # Get the JSON file path
    doctype_path = frappe.get_module_path(
        "siud", "doctype", "supplier", "supplier.json"
    )

    # Read the JSON
    with open(doctype_path, 'r', encoding='utf-8') as f:
        supplier_json = json.load(f)

    # Check if contacts field already exists
    for field in supplier_json.get("fields", []):
        if field.get("fieldname") == "contacts":
            print("✓ Contacts field already exists")
            return

    # Find contact_section index
    contact_section_idx = None
    for idx, field in enumerate(supplier_json["field_order"]):
        if field == "contact_section":
            contact_section_idx = idx
            break

    if contact_section_idx is None:
        print("✗ Could not find contact_section")
        return

    # Hide old fields
    for field in supplier_json["fields"]:
        if field["fieldname"] in ["address", "phone", "email", "column_break_1"]:
            field["hidden"] = 1

    # Add contacts to field_order
    supplier_json["field_order"].insert(contact_section_idx + 1, "contacts")

    # Add contacts field definition
    supplier_json["fields"].append({
        "fieldname": "contacts",
        "fieldtype": "Table",
        "label": "אנשי קשר",
        "options": "Supplier Contact"
    })

    # Update modified timestamp
    supplier_json["modified"] = frappe.utils.now()

    # Write back
    with open(doctype_path, 'w', encoding='utf-8') as f:
        json.dump(supplier_json, f, indent=1, ensure_ascii=False)

    print("✓ Added contacts field to Supplier JSON")
    print("  Run: bench --site development.localhost reload-doctype Supplier")

if __name__ == "__main__":
    add_contacts_field()
