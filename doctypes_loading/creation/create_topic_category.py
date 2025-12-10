"""
Create Inquiry Topic Category
"""

import frappe

@frappe.whitelist()
def create():
    """Create a topic category"""

    # Check what fields the Inquiry Topic Category DocType has
    try:
        meta = frappe.get_meta('Inquiry Topic Category')
        print("\n=== Inquiry Topic Category Fields ===")
        for field in meta.fields:
            if field.fieldtype not in ['Section Break', 'Column Break']:
                print(f"  • {field.fieldname} ({field.fieldtype}) - {field.label}")

        print(f"\nAuto-naming: {meta.autoname}")
    except Exception as e:
        print(f"Error inspecting DocType: {e}")
        return {"success": False, "error": str(e)}

    # Try to create topic categories
    categories = [
        {'code': 'PROF', 'name': 'נושאים מקצועיים'},
        {'code': 'COMP', 'name': 'תלונות'},
        {'code': 'ACCT', 'name': 'חשבונות שוטפים'},
        {'code': 'GEN', 'name': 'פניות כלליות'},
    ]

    created = []

    for cat in categories:
        if frappe.db.exists('Inquiry Topic Category', cat['code']):
            print(f"⚠ Topic category already exists: {cat['code']} - {cat['name']}")
            continue

        try:
            topic = frappe.get_doc({
                'doctype': 'Inquiry Topic Category',
                'category_code': cat['code'],
                'category_name': cat['name'],
                'is_group': 0,
            })
            topic.insert()
            created.append(f"{cat['code']} - {cat['name']}")
            print(f"✓ Created topic category: {cat['code']} - {cat['name']}")
        except Exception as e:
            print(f"✗ Error creating {cat['code']}: {str(e)}")

    frappe.db.commit()
    print(f"\n✅ Created {len(created)} topic categories")

    return {"success": True, "created": created}
