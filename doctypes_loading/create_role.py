import frappe

@frappe.whitelist()
def create_supplier_role_doctype():
    """Create Supplier Role (תפקיד ספק) DocType

    Note: Renamed from 'Role' to 'Supplier Role' to avoid conflict with Frappe's core Role DocType
    """
    if frappe.db.exists("DocType", "Supplier Role"):
        frappe.msgprint("Supplier Role DocType already exists")
        return

    dt = frappe.get_doc({
        "doctype": "DocType",
        "name": "Supplier Role",
        "module": "Siud",
        "autoname": "field:role_name",
        "naming_rule": "By fieldname",
        "fields": [
            {
                "fieldname": "role_name",
                "fieldtype": "Data",
                "label": "שם תפקיד",
                "reqd": 1,
                "unique": 1
            },
            {
                "fieldname": "role_title_he",
                "fieldtype": "Data",
                "label": "כותרת בעברית",
                "reqd": 1
            }
        ],
        "permissions": [
            {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1
            }
        ]
    })
    dt.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()
    frappe.msgprint("Supplier Role DocType created successfully")
