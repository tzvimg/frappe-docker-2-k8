"""
Inspect the Supplier Inquiry DocType to see what fields it has
"""

import frappe

@frappe.whitelist()
def inspect():
    """Inspect Supplier Inquiry DocType"""

    meta = frappe.get_meta('Supplier Inquiry')

    print("\n" + "=" * 60)
    print("Supplier Inquiry DocType Information")
    print("=" * 60)

    print(f"\nAuto-naming: {meta.autoname}")
    print(f"Naming Rule: {meta.naming_rule}")
    print(f"Workflow State Field: {meta.get('workflow_state_field', 'N/A')}")

    print("\n📋 Fields:")
    for field in meta.fields:
        if field.fieldtype not in ['Section Break', 'Column Break', 'HTML']:
            required = " [REQUIRED]" if field.reqd else ""
            options = f" → {field.options}" if field.options else ""
            print(f"  • {field.fieldname} ({field.fieldtype}){options} - {field.label}{required}")

    return {"success": True}
