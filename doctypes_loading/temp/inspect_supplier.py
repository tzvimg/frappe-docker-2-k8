"""
Inspect the Supplier DocType to see what fields it has
"""

import frappe
import json

@frappe.whitelist()
def inspect():
    """Inspect Supplier DocType"""

    meta = frappe.get_meta('Supplier')

    print("\n" + "=" * 60)
    print("Supplier DocType Information")
    print("=" * 60)

    print(f"\nAuto-naming: {meta.autoname}")
    print(f"Naming Rule: {meta.naming_rule}")

    print("\n📋 Fields:")
    for field in meta.fields:
        if field.fieldtype not in ['Section Break', 'Column Break']:
            required = " [REQUIRED]" if field.reqd else ""
            print(f"  • {field.fieldname} ({field.fieldtype}) - {field.label}{required}")

    return {"success": True}
