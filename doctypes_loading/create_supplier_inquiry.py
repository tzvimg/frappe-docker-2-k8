import frappe

@frappe.whitelist()
def create_supplier_inquiry_doctype():
    """Create Supplier Inquiry (פניית ספק) DocType"""
    if frappe.db.exists("DocType", "Supplier Inquiry"):
        frappe.msgprint("Supplier Inquiry DocType already exists")
        return

    dt = frappe.get_doc({
        "doctype": "DocType",
        "name": "Supplier Inquiry",
        "module": "Siud",
        "autoname": "format:SI-{#####}",
        "track_changes": 1,
        "fields": [
            {
                "fieldname": "supplier_section",
                "fieldtype": "Section Break",
                "label": "פרטי ספק"
            },
            {
                "fieldname": "supplier_link",
                "fieldtype": "Link",
                "label": "מזהה ספק",
                "options": "Supplier",
                "reqd": 1
            },
            {
                "fieldname": "topic_category",
                "fieldtype": "Link",
                "label": "קטגורית נושא פנייה",
                "options": "Inquiry Topic Category",
                "reqd": 1
            },
            {
                "fieldname": "inquiry_section",
                "fieldtype": "Section Break",
                "label": "תוכן הפנייה"
            },
            {
                "fieldname": "inquiry_description",
                "fieldtype": "Text Editor",
                "label": "תיאור הפנייה",
                "reqd": 1
            },
            {
                "fieldname": "context_section",
                "fieldtype": "Section Break",
                "label": "הקשר הפנייה"
            },
            {
                "fieldname": "inquiry_context",
                "fieldtype": "Select",
                "label": "הקשר הפנייה",
                "options": "ספק עצמו\nמבוטח",
                "reqd": 1
            },
            {
                "fieldname": "column_break_1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "insured_id_number",
                "fieldtype": "Data",
                "label": "מספר זהות של המבוטח",
                "depends_on": "eval:doc.inquiry_context=='מבוטח'",
                "length": 9,
                "mandatory_depends_on": "eval:doc.inquiry_context=='מבוטח'"
            },
            {
                "fieldname": "insured_full_name",
                "fieldtype": "Data",
                "label": "שם מלא של המבוטח",
                "depends_on": "eval:doc.inquiry_context=='מבוטח'",
                "mandatory_depends_on": "eval:doc.inquiry_context=='מבוטח'"
            },
            {
                "fieldname": "attachments_section",
                "fieldtype": "Section Break",
                "label": "קבצים מצורפים"
            },
            {
                "fieldname": "attachments",
                "fieldtype": "Attach",
                "label": "קבצים מצורפים"
            },
            {
                "fieldname": "status_section",
                "fieldtype": "Section Break",
                "label": "סטטוס וטיפול"
            },
            {
                "fieldname": "inquiry_status",
                "fieldtype": "Select",
                "label": "סטטוס פנייה",
                "options": "חדש\nבטיפול\nממתין למידע\nנסגר\nנדחה",
                "default": "חדש"
            },
            {
                "fieldname": "column_break_2",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "assigned_role",
                "fieldtype": "Link",
                "label": "שיוך לתפקיד מטפל בפניה",
                "options": "Role"
            },
            {
                "fieldname": "assigned_employee_id",
                "fieldtype": "Link",
                "label": "מזהה הפקיד שמטפל בפנייה",
                "options": "User"
            },
            {
                "fieldname": "response_section",
                "fieldtype": "Section Break",
                "label": "מענה לפנייה"
            },
            {
                "fieldname": "response_text",
                "fieldtype": "Text Editor",
                "label": "המענה לפנייה - מלל"
            },
            {
                "fieldname": "response_attachments",
                "fieldtype": "Attach",
                "label": "המענה לפנייה - קבצים"
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
    frappe.msgprint("Supplier Inquiry DocType created successfully")
