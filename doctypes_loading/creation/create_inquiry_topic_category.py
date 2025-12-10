import frappe

@frappe.whitelist()
def create_inquiry_topic_category_doctype():
    """Create Inquiry Topic Category (קטגוריות של נושאי פנייה) DocType

    Supports up to two levels of hierarchy via parent_category self-link.
    """
    if frappe.db.exists("DocType", "Inquiry Topic Category"):
        frappe.msgprint("Inquiry Topic Category DocType already exists")
        return

    dt = frappe.get_doc({
        "doctype": "DocType",
        "name": "Inquiry Topic Category",
        "module": "Siud",
        "autoname": "field:category_code",
        "naming_rule": "By fieldname",
        "is_tree": 1,
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
            },
            {
                "fieldname": "parent_category",
                "fieldtype": "Link",
                "label": "קטגוריית אב",
                "options": "Inquiry Topic Category"
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
    frappe.msgprint("Inquiry Topic Category DocType created successfully")
