#!/usr/bin/env python3
"""
Check WebForm list columns configuration
"""

import frappe

def check_list_columns():
    """Check WebForm list columns"""

    webform = frappe.get_doc("Web Form", "פניית-ספק")

    print("\n=== WebForm List Columns ===")
    for col in webform.list_columns:
        print(f"\nColumn {col.idx}:")
        print(f"  Fieldname: {col.fieldname}")
        print(f"  Fieldtype: {col.fieldtype}")
        print(f"  Label: {col.label}")
        print(f"  Options: {col.options}")

    # Get the actual DocType field labels
    doctype = frappe.get_doc("DocType", "Supplier Inquiry")
    print("\n\n=== Supplier Inquiry Field Labels ===")
    for field in doctype.fields:
        if field.fieldname in ["name", "topic_category", "inquiry_status", "creation"]:
            print(f"{field.fieldname}: {field.label}")

if __name__ == "__main__":
    check_list_columns()
