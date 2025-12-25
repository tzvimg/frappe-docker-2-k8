#!/usr/bin/env python3
"""
Enable editing for Supplier Inquiry WebForm
This allows suppliers to view and edit their existing inquiries via the portal
"""

import frappe

def enable_webform_edit():
    """Enable allow_edit on Supplier Inquiry WebForm"""

    try:
        # Get the WebForm
        webform = frappe.get_doc("Web Form", "פניית-ספק")

        # Enable editing
        webform.allow_edit = 1

        # Save the changes
        webform.save()
        frappe.db.commit()

        print("✅ Successfully enabled editing for Supplier Inquiry WebForm")
        print(f"   - WebForm: {webform.name}")
        print(f"   - Route: /{webform.route}")
        print(f"   - Allow Edit: {webform.allow_edit}")
        print("\nSuppliers can now view and edit their existing inquiries!")

        return {"success": True, "message": "WebForm updated successfully"}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        frappe.db.rollback()
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    enable_webform_edit()
