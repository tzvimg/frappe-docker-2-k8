import frappe

@frappe.whitelist()
def create_contact_person_doctype():
    """Create Contact Person (איש קשר) DocType"""
    if frappe.db.exists("DocType", "Contact Person"):
        frappe.msgprint("Contact Person DocType already exists")
        return

    dt = frappe.get_doc({
        "doctype": "DocType",
        "name": "Contact Person",
        "module": "Siud",
        "autoname": "format:CP-{#####}",
        "fields": [
            {
                "fieldname": "contact_name",
                "fieldtype": "Data",
                "label": "שם איש קשר",
                "reqd": 1
            },
            {
                "fieldname": "supplier_link",
                "fieldtype": "Link",
                "label": "שיוך לספק",
                "options": "Supplier",
                "reqd": 1
            },
            {
                "fieldname": "contact_section",
                "fieldtype": "Section Break",
                "label": "פרטי קשר"
            },
            {
                "fieldname": "email",
                "fieldtype": "Data",
                "label": "כתובת דוא\"ל",
                "options": "Email"
            },
            {
                "fieldname": "column_break_1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "mobile_phone",
                "fieldtype": "Phone",
                "label": "טלפון נייד"
            },
            {
                "fieldname": "branch_section",
                "fieldtype": "Section Break",
                "label": "סניף ותפקיד"
            },
            {
                "fieldname": "branch",
                "fieldtype": "Data",
                "label": "סניף"
            },
            {
                "fieldname": "column_break_2",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "primary_role_type",
                "fieldtype": "Select",
                "label": "תפקיד ראשי",
                "options": "ספק\nאיש קשר של ספק"
            },
            {
                "fieldname": "roles_section",
                "fieldtype": "Section Break",
                "label": "תפקידים משויכים"
            },
            {
                "fieldname": "assigned_roles",
                "fieldtype": "Table",
                "label": "רשימת תפקידים משויכים",
                "options": "Contact Person Role"
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
    frappe.msgprint("Contact Person DocType created successfully")


@frappe.whitelist()
def create_contact_person_role_child():
    """Create child table for Contact Person Roles"""
    if frappe.db.exists("DocType", "Contact Person Role"):
        frappe.msgprint("Contact Person Role DocType already exists")
        return

    dt = frappe.get_doc({
        "doctype": "DocType",
        "name": "Contact Person Role",
        "module": "Siud",
        "istable": 1,
        "editable_grid": 1,
        "fields": [
            {
                "fieldname": "role",
                "fieldtype": "Link",
                "label": "תפקיד",
                "options": "Role",
                "in_list_view": 1,
                "reqd": 1
            }
        ]
    })
    dt.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()
    frappe.msgprint("Contact Person Role child table created successfully")
