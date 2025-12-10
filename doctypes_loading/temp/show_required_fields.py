"""
Show only required fields for each DocType
"""

import frappe


@frappe.whitelist()
def show_required_fields():
    """Show required fields for all SIUD DocTypes"""

    frappe.msgprint("=" * 80)
    frappe.msgprint("Required Fields for All SIUD DocTypes")
    frappe.msgprint("=" * 80)

    doctypes = frappe.get_all('DocType',
        filters={
            'custom': 0,
            'istable': 0,
            'module': ['in', ['Siud', 'Nursing Management', 'SIUD']]
        },
        fields=['name'],
        order_by='name'
    )

    for dt in doctypes:
        meta = frappe.get_meta(dt.name)

        frappe.msgprint(f"\n📋 {dt.name}")
        frappe.msgprint(f"   Autoname: {meta.autoname}")
        frappe.msgprint("   Required Fields:")

        required_fields = [f for f in meta.fields if f.reqd and f.fieldtype not in ['Section Break', 'Column Break', 'Tab Break']]

        if required_fields:
            for field in required_fields:
                frappe.msgprint(f"      • {field.fieldname:<30} ({field.fieldtype:<15}) - {field.label}")
        else:
            frappe.msgprint("      (no required fields)")

        frappe.msgprint("")

    return {"success": True}
