"""
Inspect DocType fields to understand structure
"""

import frappe
import json


@frappe.whitelist()
def inspect_doctype(doctype_name):
    """Inspect fields of a DocType"""

    frappe.msgprint("=" * 80)
    frappe.msgprint(f"Inspecting DocType: {doctype_name}")
    frappe.msgprint("=" * 80)

    try:
        meta = frappe.get_meta(doctype_name)

        frappe.msgprint(f"\n📋 DocType Info:")
        frappe.msgprint(f"   Module: {meta.module}")
        frappe.msgprint(f"   Autoname: {meta.autoname}")
        frappe.msgprint(f"   Is Table: {meta.istable}")
        frappe.msgprint(f"   Is Submittable: {meta.is_submittable}")

        frappe.msgprint(f"\n📊 Fields ({len(meta.fields)} total):")
        frappe.msgprint("-" * 80)

        for field in meta.fields:
            required = "✓ REQUIRED" if field.reqd else ""
            label = field.label or ""
            fieldname = field.fieldname or ""
            fieldtype = field.fieldtype or ""

            frappe.msgprint(f"{fieldname:<30} | {fieldtype:<15} | {label:<30} | {required}")

        frappe.msgprint("-" * 80)

        return {"success": True, "fields": [f.as_dict() for f in meta.fields]}

    except Exception as e:
        frappe.msgprint(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def inspect_all_siud_doctypes():
    """Inspect all SIUD DocTypes"""

    frappe.msgprint("=" * 80)
    frappe.msgprint("Inspecting All SIUD DocTypes")
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

    results = {}

    for dt in doctypes:
        frappe.msgprint(f"\n\n{'=' * 80}")
        result = inspect_doctype(dt.name)
        results[dt.name] = result

    return {"success": True, "results": results}
