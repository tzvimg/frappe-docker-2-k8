#!/usr/bin/env python3
"""
Script to create Document Approval DocType
"""

import frappe
from frappe import _

def create_document_approval_doctype():
    """Create Document Approval DocType"""

    # Check if already exists
    if frappe.db.exists("DocType", "Document Approval"):
        print("Document Approval DocType already exists")
        return

    # Create DocType
    doc = frappe.new_doc("DocType")
    doc.update({
        "name": "Document Approval",
        "module": "Nursing Management",
        "custom": 0,
        "is_submittable": 0,
        "track_changes": 1,
        "is_tree": 0,
        "autoname": "field:document_number",
        "naming_rule": "By fieldname",
        "title_field": "document_number"
    })

    # Add fields
    fields = [
        {
            "fieldname": "document_number",
            "fieldtype": "Data",
            "label": "מס' מסמך",
            "reqd": 1,
            "unique": 1,
            "in_list_view": 1,
            "in_standard_filter": 1,
            "description": "מספר מסמך ייחודי"
        },
        {
            "fieldname": "contract",
            "fieldtype": "Link",
            "label": "הסכם",
            "options": "Contract",
            "reqd": 1,
            "in_list_view": 1,
            "in_standard_filter": 1
        },
        {
            "fieldname": "column_break_1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "document_type",
            "fieldtype": "Select",
            "label": "סוג מסמך",
            "options": "אישור ביטוח\nניהול תקין\nפרטי בנק\nהסכם בט\"ל",
            "reqd": 1,
            "in_list_view": 1,
            "in_standard_filter": 1
        },
        {
            "fieldname": "section_break_file",
            "fieldtype": "Section Break",
            "label": "קובץ מצורף"
        },
        {
            "fieldname": "attached_file",
            "fieldtype": "Attach",
            "label": "קובץ מצורף"
        },
        {
            "fieldname": "section_break_dates",
            "fieldtype": "Section Break",
            "label": "תאריכים"
        },
        {
            "fieldname": "submission_date",
            "fieldtype": "Date",
            "label": "תאריך הגשה",
            "default": "Today",
            "reqd": 1
        },
        {
            "fieldname": "column_break_2",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "expiry_date",
            "fieldtype": "Date",
            "label": "תאריך תוקף"
        },
        {
            "fieldname": "section_break_status",
            "fieldtype": "Section Break",
            "label": "סטטוס ובדיקה"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "סטטוס",
            "options": "חסר\nהוגש\nתקין\nלא תקין",
            "default": "חסר",
            "in_list_view": 1,
            "in_standard_filter": 1
        },
        {
            "fieldname": "column_break_3",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "reviewer",
            "fieldtype": "Link",
            "label": "בודק",
            "options": "User"
        },
        {
            "fieldname": "review_date",
            "fieldtype": "Date",
            "label": "תאריך בדיקה"
        },
        {
            "fieldname": "section_break_rejection",
            "fieldtype": "Section Break",
            "label": "סיבת דחייה",
            "depends_on": "eval:doc.status=='לא תקין'"
        },
        {
            "fieldname": "rejection_reason",
            "fieldtype": "Text",
            "label": "סיבת דחייה"
        }
    ]

    for field in fields:
        doc.append("fields", field)

    # Add permissions
    permissions = [
        {
            "role": "System Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 0,
            "cancel": 0,
            "amend": 0
        }
    ]

    for perm in permissions:
        doc.append("permissions", perm)

    # Insert
    doc.insert()
    print(f"✓ Document Approval DocType created: {doc.name}")

    return doc

if __name__ == "__main__":
    frappe.connect()
    frappe.init(site="development.localhost")
    frappe.connect()

    create_document_approval_doctype()

    frappe.db.commit()
    print("\n✓ Document Approval DocType creation complete!")
