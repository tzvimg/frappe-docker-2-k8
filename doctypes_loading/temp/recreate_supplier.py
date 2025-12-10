"""
Recreate Supplier DocType from scratch
"""
import frappe
import os
import shutil

def delete_supplier():
    """Delete existing Supplier DocType"""

    if not frappe.db.exists("DocType", "Supplier"):
        print("✓ Supplier doesn't exist, nothing to delete")
        return

    # Delete the DocType
    frappe.delete_doc("DocType", "Supplier", force=True)
    frappe.db.commit()
    print("✓ Deleted Supplier DocType")

    # Delete the directory
    doctype_dir = frappe.get_module_path("siud", "doctype", "supplier")
    if os.path.exists(doctype_dir):
        shutil.rmtree(doctype_dir)
        print("✓ Deleted Supplier directory")

def create_supplier():
    """Create fresh Supplier DocType"""

    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Supplier",
        "module": "Siud",
        "autoname": "field:supplier_id",
        "naming_rule": "By fieldname",
        "editable_grid": 1,
        "allow_rename": 1,
        "fields": [
            # Basic Information
            {
                "fieldname": "supplier_id",
                "fieldtype": "Data",
                "label": "מזהה ספק",
                "reqd": 1,
                "unique": 1,
                "in_list_view": 1,
                "read_only_depends_on": "eval:!doc.__islocal"
            },
            {
                "fieldname": "supplier_name",
                "fieldtype": "Data",
                "label": "שם ספק",
                "reqd": 1,
                "in_list_view": 1
            },

            # Activity Domains Section
            {
                "fieldname": "activity_domains_section",
                "fieldtype": "Section Break",
                "label": "תחומי פעילות"
            },
            {
                "fieldname": "activity_domains",
                "fieldtype": "Table",
                "label": "תחומי פעילות",
                "options": "Supplier Activity Domain"
            },

            # Contact Section
            {
                "fieldname": "contact_section",
                "fieldtype": "Section Break",
                "label": "פרטי קשר"
            },
            {
                "fieldname": "address",
                "fieldtype": "Text",
                "label": "כתובת"
            },
            {
                "fieldname": "column_break_1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "phone",
                "fieldtype": "Phone",
                "label": "טלפון"
            },
            {
                "fieldname": "email",
                "fieldtype": "Data",
                "label": "כתובת דוא\"ל",
                "options": "Email"
            }
        ],
        "permissions": [
            {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
                "submit": 0,
                "cancel": 0,
                "amend": 0,
                "report": 1,
                "export": 1,
                "import": 0,
                "share": 1,
                "print": 1,
                "email": 1
            }
        ]
    })

    doc.insert()
    frappe.db.commit()
    print("✓ Created fresh Supplier DocType")

def recreate_all():
    """Delete and recreate Supplier"""
    print("Recreating Supplier DocType...")
    delete_supplier()
    create_supplier()
    print("\n✓ Supplier DocType recreated!")
    print("  Run: bench --site development.localhost clear-cache")

if __name__ == "__main__":
    recreate_all()
