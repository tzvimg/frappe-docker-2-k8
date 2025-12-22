"""
Check which DocTypes exist in the Siud module
"""

import frappe


@frappe.whitelist()
def check():
    """Check which DocTypes currently exist"""

    print("\n" + "="*60)
    print("Checking Existing DocTypes in Siud Module")
    print("="*60 + "\n")

    # Get all DocTypes in Siud module
    doctypes = frappe.get_all(
        "DocType",
        filters={"module": "Siud"},
        fields=["name", "custom"],
        order_by="name"
    )

    if doctypes:
        print(f"Found {len(doctypes)} DocTypes:\n")
        for dt in doctypes:
            custom_marker = " (Custom)" if dt.custom else ""
            print(f"  ✓ {dt.name}{custom_marker}")
    else:
        print("No DocTypes found in Siud module")

    print("\n" + "="*60 + "\n")

    return {"success": True, "count": len(doctypes), "doctypes": [d.name for d in doctypes]}
