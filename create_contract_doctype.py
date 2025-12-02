#!/usr/bin/env python3
"""
Script to create Contract DocType
"""

import frappe
from frappe import _

def create_contract_doctype():
    """Create Contract DocType"""

    # Check if already exists
    if frappe.db.exists("DocType", "Contract"):
        print("Contract DocType already exists")
        return

    # Create DocType
    doc = frappe.new_doc("DocType")
    doc.update({
        "name": "Contract",
        "module": "Nursing Management",
        "custom": 0,
        "is_submittable": 0,
        "track_changes": 1,
        "is_tree": 0,
        "autoname": "field:contract_number",
        "naming_rule": "By fieldname",
        "title_field": "contract_number"
    })

    # Add fields
    fields = [
        {
            "fieldname": "contract_number",
            "fieldtype": "Data",
            "label": "מס' הסכם",
            "reqd": 1,
            "unique": 1,
            "in_list_view": 1,
            "in_standard_filter": 1,
            "description": "מספר הסכם ייחודי"
        },
        {
            "fieldname": "branch",
            "fieldtype": "Link",
            "label": "סניף",
            "options": "Service Provider Branch",
            "reqd": 1,
            "in_list_view": 1,
            "in_standard_filter": 1
        },
        {
            "fieldname": "column_break_1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "service_provider",
            "fieldtype": "Link",
            "label": "נותן שירות",
            "options": "Service Provider",
            "read_only": 1,
            "in_list_view": 1,
            "in_standard_filter": 1,
            "fetch_from": "branch.service_provider"
        },
        {
            "fieldname": "section_break_dates",
            "fieldtype": "Section Break",
            "label": "תאריכים"
        },
        {
            "fieldname": "start_date",
            "fieldtype": "Date",
            "label": "תאריך תחילה",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "column_break_2",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "end_date",
            "fieldtype": "Date",
            "label": "תאריך סיום",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "section_break_status",
            "fieldtype": "Section Break",
            "label": "סטטוס והתראות"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "סטטוס",
            "options": "טיוטה\nפעיל\nפג תוקף\nבוטל",
            "default": "טיוטה",
            "in_list_view": 1,
            "in_standard_filter": 1
        },
        {
            "fieldname": "column_break_3",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "alert_days_before_expiry",
            "fieldtype": "Int",
            "label": "התראה לפני פקיעה (ימים)",
            "default": 30
        },
        {
            "fieldname": "section_break_notes",
            "fieldtype": "Section Break",
            "label": "הערות"
        },
        {
            "fieldname": "notes",
            "fieldtype": "Text Editor",
            "label": "הערות"
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
    print(f"✓ Contract DocType created: {doc.name}")

    return doc

if __name__ == "__main__":
    frappe.connect()
    frappe.init(site="development.localhost")
    frappe.connect()

    create_contract_doctype()

    frappe.db.commit()
    print("\n✓ Contract DocType creation complete!")
