#!/usr/bin/env python3
"""
Update Document Approval to link to Nursing Contract
"""

import frappe

frappe.connect()
frappe.init(site="development.localhost")
frappe.connect()

# Get Document Approval DocType
doc_approval = frappe.get_doc("DocType", "Document Approval")

# Find the contract field and update it
for field in doc_approval.fields:
    if field.fieldname == "contract":
        print(f"Found contract field, current options: {field.options}")
        field.options = "Nursing Contract"
        print(f"Updated to: {field.options}")
        break

# Save the DocType
doc_approval.save()
frappe.db.commit()

print("✓ Document Approval updated to link to Nursing Contract")
