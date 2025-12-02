#!/usr/bin/env python3
"""
Script to create Service Provider Branch DocType
"""

import frappe
from frappe import _

def create_service_provider_branch_doctype():
    """Create Service Provider Branch DocType"""

    # Check if already exists
    if frappe.db.exists("DocType", "Service Provider Branch"):
        print("Service Provider Branch DocType already exists")
        return

    # Create DocType
    doc = frappe.new_doc("DocType")
    doc.update({
        "name": "Service Provider Branch",
        "module": "Nursing Management",
        "custom": 0,
        "is_submittable": 0,
        "track_changes": 1,
        "is_tree": 0,
        "autoname": "field:branch_code",
        "naming_rule": "By fieldname",
        "title_field": "branch_name"
    })

    # Add fields
    fields = [
        {
            "fieldname": "branch_code",
            "fieldtype": "Data",
            "label": "קוד סניף",
            "reqd": 1,
            "unique": 1,
            "length": 10,
            "in_list_view": 1,
            "in_standard_filter": 1,
            "description": "קוד ייחודי לסניף (2 תווים)"
        },
        {
            "fieldname": "service_provider",
            "fieldtype": "Link",
            "label": "נותן שירות",
            "options": "Service Provider",
            "reqd": 1,
            "in_list_view": 1,
            "in_standard_filter": 1
        },
        {
            "fieldname": "column_break_1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "branch_name",
            "fieldtype": "Data",
            "label": "שם הסניף",
            "in_list_view": 1
        },
        {
            "fieldname": "section_break_1",
            "fieldtype": "Section Break",
            "label": "פרטי קשר"
        },
        {
            "fieldname": "address",
            "fieldtype": "Small Text",
            "label": "כתובת סניף"
        },
        {
            "fieldname": "column_break_2",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "phone",
            "fieldtype": "Data",
            "label": "טלפון סניף",
            "options": "Phone"
        },
        {
            "fieldname": "email",
            "fieldtype": "Data",
            "label": "אימייל",
            "options": "Email"
        },
        {
            "fieldname": "section_break_2",
            "fieldtype": "Section Break",
            "label": "סטטוס"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "סטטוס",
            "options": "פעיל\nסגור",
            "default": "פעיל",
            "in_list_view": 1,
            "in_standard_filter": 1
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
    print(f"✓ Service Provider Branch DocType created: {doc.name}")

    return doc

if __name__ == "__main__":
    frappe.connect()
    frappe.init(site="development.localhost")
    frappe.connect()

    create_service_provider_branch_doctype()

    frappe.db.commit()
    print("\n✓ Service Provider Branch DocType creation complete!")
