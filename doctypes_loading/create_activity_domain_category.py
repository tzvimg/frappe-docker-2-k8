import frappe

@frappe.whitelist()
def create_activity_domain_category_doctype():
    """Create Activity Domain Category (קטגוריות תחומי פעילות) DocType"""
    if frappe.db.exists("DocType", "Activity Domain Category"):
        frappe.msgprint("Activity Domain Category DocType already exists")
        return

    dt = frappe.get_doc({
        "doctype": "DocType",
        "name": "Activity Domain Category",
        "module": "Siud",
        "autoname": "field:category_code",
        "naming_rule": "By fieldname",
        "fields": [
            {
                "fieldname": "category_code",
                "fieldtype": "Data",
                "label": "קוד קטגוריה",
                "reqd": 1,
                "unique": 1
            },
            {
                "fieldname": "category_name",
                "fieldtype": "Data",
                "label": "שם קטגוריה",
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
    frappe.msgprint("Activity Domain Category DocType created successfully")
