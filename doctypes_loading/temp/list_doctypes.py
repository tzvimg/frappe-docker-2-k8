"""
List all SIUD DocTypes and their record counts
"""

import frappe


@frappe.whitelist()
def list_all_doctypes():
    """List all custom DocTypes in the siud app"""

    frappe.msgprint("=" * 80)
    frappe.msgprint("SIUD DocTypes and Record Counts")
    frappe.msgprint("=" * 80)

    # Get all DocTypes for siud modules
    doctypes = frappe.get_all('DocType',
        filters={
            'custom': 0,
            'istable': 0,
            'module': ['in', ['Siud', 'Nursing Management', 'SIUD']]
        },
        fields=['name', 'module'],
        order_by='name'
    )

    if not doctypes:
        frappe.msgprint("\n⚠ No SIUD DocTypes found!")
        return {"success": False, "doctypes": []}

    results = []

    frappe.msgprint(f"\nFound {len(doctypes)} DocTypes:\n")

    for dt in doctypes:
        try:
            count = frappe.db.count(dt.name)
            frappe.msgprint(f"  • {dt.name:<40} ({dt.module:<20}): {count:>5} records")
            results.append({
                'name': dt.name,
                'module': dt.module,
                'count': count
            })
        except Exception as e:
            frappe.msgprint(f"  • {dt.name:<40} ({dt.module:<20}): ERROR - {str(e)}")

    frappe.msgprint("\n" + "=" * 80)

    return {"success": True, "doctypes": results}
