import frappe

@frappe.whitelist()
def create_supplier_doctype():
    """Create Supplier (ספק) DocType"""
    if frappe.db.exists("DocType", "Supplier"):
        frappe.msgprint("Supplier DocType already exists")
        return

    dt = frappe.get_doc({
        "doctype": "DocType",
        "name": "Supplier",
        "module": "Siud",
        "autoname": "field:supplier_id",
        "naming_rule": "By fieldname",
        "fields": [
            {
                "fieldname": "supplier_id",
                "fieldtype": "Data",
                "label": "מזהה ספק",
                "reqd": 1,
                "unique": 1,
                "read_only_depends_on": "eval:!doc.__islocal"
            },
            {
                "fieldname": "supplier_name",
                "fieldtype": "Data",
                "label": "שם ספק",
                "reqd": 1
            },
            {
                "fieldname": "activity_domains_section",
                "fieldtype": "Section Break",
                "label": "תחומי פעילות"
            },
            # {
            #     "fieldname": "activity_domains",
            #     "fieldtype": "Table",
            #     "label": "תחומי פעילות",
            #     "options": "Supplier Activity Domain"
            # },
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
                "delete": 1
            }
        ]
    })
    dt.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()
    frappe.msgprint("Supplier DocType created successfully")


@frappe.whitelist()
def create_supplier_activity_domain_child():
    """Create child table for Supplier Activity Domains"""
    if frappe.db.exists("DocType", "Supplier Activity Domain"):
        frappe.msgprint("Supplier Activity Domain DocType already exists")
        return

    dt = frappe.get_doc({
        "doctype": "DocType",
        "name": "Supplier Activity Domain",
        "module": "Siud",
        "istable": 1,
        "editable_grid": 1,
        "fields": [
            {
                "fieldname": "activity_domain_category",
                "fieldtype": "Link",
                "label": "קטגורית תחום פעילות",
                "options": "Activity Domain Category",
                "in_list_view": 1,
                "reqd": 1
            }
        ]
    })
    dt.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()
    frappe.msgprint("Supplier Activity Domain child table created successfully")
