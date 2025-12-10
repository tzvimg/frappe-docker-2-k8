"""Check what workflow components were created"""

import frappe

@frappe.whitelist()
def check():
    """Check created components"""

    results = {}

    print("\n=== Checking created components ===\n")

    # Check DocTypes
    for dt in ['Supplier', 'Supplier Inquiry']:
        exists = frappe.db.exists('DocType', dt)
        results[f'DocType_{dt}'] = exists
        print(f"DocType '{dt}': {'✓ EXISTS' if exists else '✗ NOT FOUND'}")

    # Check Roles
    for role in ['Service Provider User', 'Sorting Clerk', 'Handling Clerk']:
        exists = frappe.db.exists('Role', role)
        results[f'Role_{role}'] = exists
        print(f"Role '{role}': {'✓ EXISTS' if exists else '✗ NOT FOUND'}")

    # Check Workflow
    exists = frappe.db.exists('Workflow', 'Supplier Inquiry Workflow')
    results['Workflow'] = exists
    print(f"Workflow 'Supplier Inquiry Workflow': {'✓ EXISTS' if exists else '✗ NOT FOUND'}")

    print("\n")

    return results
