#!/usr/bin/env python3
"""
Check what DocTypes exist
"""

import frappe

frappe.connect()
frappe.init(site="development.localhost")
frappe.connect()

# List all nursing_management DocTypes
nursing_doctypes = frappe.get_all("DocType",
    filters={"module": "Nursing Management"},
    fields=["name", "module", "modified"],
    order_by="modified desc"
)

print("\nNursing Management DocTypes:")
print("="*60)
for dt in nursing_doctypes:
    print(f"  {dt.name:<40} {dt.modified}")

# Check for Contract specifically
print("\n" + "="*60)
print("Checking Contract DocType:")
print("="*60)
contract_exists = frappe.db.exists("DocType", "Contract")
print(f"Contract exists in database: {contract_exists}")

if contract_exists:
    contract_doc = frappe.get_doc("DocType", "Contract")
    print(f"Module: {contract_doc.module}")
    print(f"Custom: {contract_doc.custom}")

# Check all DocTypes with 'contract' in name
all_contract_doctypes = frappe.get_all("DocType",
    filters=[["name", "like", "%contract%"]],
    fields=["name", "module"],
    order_by="name"
)

print("\nAll DocTypes with 'contract' in name:")
print("="*60)
for dt in all_contract_doctypes:
    print(f"  {dt.name:<40} {dt.module}")

frappe.db.commit()
