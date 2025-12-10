"""
Inspect the Workflow DocType structure to understand the correct fields
"""

import frappe
import json

@frappe.whitelist()
def inspect():
    """Inspect Workflow DocType structure"""

    # Get the Workflow DocType
    workflow_doctype = frappe.get_doc("DocType", "Workflow")

    print("\n=== Workflow DocType Fields ===\n")

    # Get all fields
    for field in workflow_doctype.fields:
        if field.fieldtype in ['Table', 'Link', 'Select']:
            print(f"Field: {field.fieldname}")
            print(f"  Type: {field.fieldtype}")
            print(f"  Label: {field.label}")
            if field.options:
                print(f"  Options: {field.options}")
            print()

    # Get child tables
    print("\n=== Child Tables ===\n")

    for field in workflow_doctype.fields:
        if field.fieldtype == 'Table' and field.options:
            print(f"\nChild Table: {field.options}")
            print(f"Field Name: {field.fieldname}\n")

            # Get the child DocType structure
            try:
                child_doctype = frappe.get_doc("DocType", field.options)
                for child_field in child_doctype.fields:
                    print(f"  - {child_field.fieldname} ({child_field.fieldtype})", end="")
                    if child_field.options:
                        print(f" -> {child_field.options}", end="")
                    if child_field.reqd:
                        print(" [REQUIRED]", end="")
                    print()
            except Exception as e:
                print(f"  Error: {e}")

    return {"success": True}
