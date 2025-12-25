#!/usr/bin/env python3
"""
Check WebForm list configuration
"""

import frappe

def check_webform_list():
    """Check how WebForm list filtering works"""

    # Get the WebForm
    webform = frappe.get_doc("Web Form", "פניית-ספק")

    print("\n=== WebForm Configuration ===")
    print(f"Name: {webform.name}")
    print(f"Route: {webform.route}")
    print(f"Show List: {webform.show_list}")
    print(f"List Title: {webform.list_title}")
    print(f"Apply Document Permissions: {webform.apply_document_permissions}")
    print(f"Login Required: {webform.login_required}")

    print("\n=== List Columns ===")
    for col in webform.list_columns:
        print(f"  - {col.fieldname} ({col.fieldtype})")

if __name__ == "__main__":
    check_webform_list()
