import frappe

@frappe.whitelist()
def create_delegated_supplier_scope_child():
    """Create child table for Delegated Supplier Scope (היקף האצלה)"""
    if frappe.db.exists("DocType", "Delegated Supplier Scope"):
        frappe.msgprint("Delegated Supplier Scope DocType already exists")
        return

    dt = frappe.get_doc({
        "doctype": "DocType",
        "name": "Delegated Supplier Scope",
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
    frappe.msgprint("Delegated Supplier Scope child table created successfully")


@frappe.whitelist()
def create_delegated_supplier_doctype():
    """Create Delegated Supplier (ספק מואצל) DocType"""
    if frappe.db.exists("DocType", "Delegated Supplier"):
        frappe.msgprint("Delegated Supplier DocType already exists")
        return

    dt = frappe.get_doc({
        "doctype": "DocType",
        "name": "Delegated Supplier",
        "module": "Siud",
        "autoname": "format:DS-{#####}",
        "fields": [
            {
                "fieldname": "delegating_supplier",
                "fieldtype": "Link",
                "label": "ספק מאציל",
                "options": "Supplier",
                "reqd": 1,
                "in_list_view": 1,
                "in_standard_filter": 1
            },
            {
                "fieldname": "delegated_supplier",
                "fieldtype": "Link",
                "label": "ספק מואצל",
                "options": "Supplier",
                "reqd": 1,
                "in_list_view": 1,
                "in_standard_filter": 1
            },
            {
                "fieldname": "delegation_status",
                "fieldtype": "Select",
                "label": "סטטוס האצלה",
                "options": "פעיל\nמושהה\nבוטל",
                "default": "פעיל",
                "in_list_view": 1,
                "in_standard_filter": 1
            },
            {
                "fieldname": "dates_section",
                "fieldtype": "Section Break",
                "label": "תקופת תוקף"
            },
            {
                "fieldname": "valid_from",
                "fieldtype": "Date",
                "label": "תקף מתאריך",
                "reqd": 1
            },
            {
                "fieldname": "column_break_dates",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "valid_until",
                "fieldtype": "Date",
                "label": "תקף עד תאריך",
                "description": "השאר ריק להאצלה ללא הגבלת זמן"
            },
            {
                "fieldname": "scope_section",
                "fieldtype": "Section Break",
                "label": "היקף האצלה"
            },
            {
                "fieldname": "delegation_scope",
                "fieldtype": "Table",
                "label": "היקף האצלה",
                "options": "Delegated Supplier Scope",
                "description": "תחומי הפעילות שהספק המואצל מורשה לבצע"
            },
            {
                "fieldname": "notes_section",
                "fieldtype": "Section Break",
                "label": "הערות"
            },
            {
                "fieldname": "notes",
                "fieldtype": "Text",
                "label": "הערות",
                "description": "הערות או תנאים נוספים להאצלה"
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
    frappe.msgprint("Delegated Supplier DocType created successfully")


@frappe.whitelist()
def create_delegated_supplier_all():
    """Create all Delegated Supplier related DocTypes"""
    results = []

    try:
        # First create the child table
        create_delegated_supplier_scope_child()
        results.append("✓ Delegated Supplier Scope child table created")

        # Then create the main DocType
        create_delegated_supplier_doctype()
        results.append("✓ Delegated Supplier DocType created")

        frappe.msgprint("<br>".join(results) + "<br><br><b>Delegated Supplier DocTypes created successfully!</b>")

        return {
            "success": True,
            "message": "Delegated Supplier DocTypes created successfully",
            "details": results
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Delegated Supplier DocType Creation Error")
        frappe.throw(f"Error creating Delegated Supplier DocTypes: {str(e)}")


@frappe.whitelist()
def delete_delegated_supplier_doctypes():
    """Delete Delegated Supplier related DocTypes (in reverse order)"""
    doctypes_to_delete = [
        "Delegated Supplier",
        "Delegated Supplier Scope"
    ]

    results = []

    for dt_name in doctypes_to_delete:
        try:
            if frappe.db.exists("DocType", dt_name):
                frappe.delete_doc("DocType", dt_name, force=True)
                results.append(f"✓ Deleted {dt_name}")
                frappe.msgprint(f"Deleted {dt_name}")
            else:
                results.append(f"- {dt_name} does not exist")
        except Exception as e:
            results.append(f"✗ Error deleting {dt_name}: {str(e)}")
            frappe.msgprint(f"Error deleting {dt_name}: {str(e)}")

    frappe.db.commit()
    frappe.clear_cache()

    frappe.msgprint("<br>".join(results) + "<br><br><b>Deletion complete</b>")

    return {
        "success": True,
        "message": "Deletion process completed",
        "details": results
    }
