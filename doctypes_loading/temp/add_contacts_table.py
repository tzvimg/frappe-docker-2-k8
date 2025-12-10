"""
Add inline contacts table to Supplier DocType
"""
import frappe

def create_supplier_contact_table():
    """Create a child table for supplier contacts"""

    # Check if it already exists
    if frappe.db.exists("DocType", "Supplier Contact"):
        print("✓ Supplier Contact child table already exists")
        return

    # Create child table DocType
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Supplier Contact",
        "module": "Siud",
        "istable": 1,  # This makes it a child table
        "editable_grid": 1,
        "fields": [
            {
                "fieldname": "contact_name",
                "fieldtype": "Data",
                "label": "שם איש קשר",
                "in_list_view": 1,
                "reqd": 1
            },
            {
                "fieldname": "role",
                "fieldtype": "Data",
                "label": "תפקיד",
                "in_list_view": 1
            },
            {
                "fieldname": "mobile_phone",
                "fieldtype": "Phone",
                "label": "טלפון נייד",
                "in_list_view": 1
            },
            {
                "fieldname": "email",
                "fieldtype": "Data",
                "label": "כתובת דוא\"ל",
                "options": "Email",
                "in_list_view": 1
            },
            {
                "fieldname": "is_primary",
                "fieldtype": "Check",
                "label": "איש קשר ראשי",
                "in_list_view": 1
            }
        ]
    })

    doc.insert()
    frappe.db.commit()
    print("✓ Created Supplier Contact child table")

def add_contacts_table_to_supplier():
    """Add the contacts table field to Supplier DocType"""

    # Reload to get latest version
    supplier_doc = frappe.get_doc("DocType", "Supplier")
    supplier_doc.reload()

    # Check if contacts field already exists
    for field in supplier_doc.fields:
        if field.fieldname == "contacts":
            print("✓ Contacts table field already exists on Supplier")
            return

    # Remove or hide the old single contact fields
    for field in supplier_doc.fields:
        if field.fieldname in ["address", "phone", "email", "column_break_1"]:
            field.hidden = 1

    # Add the contacts table field
    supplier_doc.append("fields", {
        "fieldname": "contacts",
        "fieldtype": "Table",
        "label": "אנשי קשר",
        "options": "Supplier Contact",
        "insert_after": "contact_section"
    })

    supplier_doc.save()
    frappe.db.commit()
    print("✓ Added contacts table to Supplier DocType")

def run_all():
    """Create child table and add it to Supplier"""
    print("Creating inline contacts table for Supplier...")
    create_supplier_contact_table()
    add_contacts_table_to_supplier()
    print("\n✓ Done! Clear cache and reload the Supplier form.")
    print("  You'll see an inline editable table for contacts.")

if __name__ == "__main__":
    run_all()
