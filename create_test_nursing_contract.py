#!/usr/bin/env python3
"""
Create test Nursing Contract
"""

import frappe
from datetime import datetime, timedelta

frappe.connect()
frappe.init(site="development.localhost")
frappe.connect()

# Get existing branch
branches = frappe.get_all("Service Provider Branch", limit=1)
if not branches:
    print("No branches found!")
    exit()

branch_name = branches[0].name
print(f"Using branch: {branch_name}")

# Calculate dates
start_date = datetime.now().date()
end_date = start_date + timedelta(days=365)

# Check if contract already exists
existing = frappe.db.exists("Nursing Contract", {"contract_number": "2025-001"})

if existing:
    print(f"✓ Nursing Contract already exists: {existing}")
    contract = frappe.get_doc("Nursing Contract", existing)
else:
    # Create nursing contract
    contract = frappe.get_doc({
        "doctype": "Nursing Contract",
        "contract_number": "2025-001",
        "branch": branch_name,
        "start_date": start_date,
        "end_date": end_date,
        "status": "פעיל",
        "alert_days_before_expiry": 30,
        "notes": "חוזה ראשי לשנת 2025"
    })
    contract.insert()
    frappe.db.commit()
    print(f"✓ Created Nursing Contract: {contract.name}")

print(f"  Contract Number: {contract.contract_number}")
print(f"  Branch: {contract.branch}")
print(f"  Service Provider: {contract.service_provider}")
print(f"  Start Date: {contract.start_date}")
print(f"  End Date: {contract.end_date}")
print(f"  Status: {contract.status}")
print("\n✓ Nursing Contract test complete!")
