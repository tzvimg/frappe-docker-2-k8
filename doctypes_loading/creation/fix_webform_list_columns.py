#!/usr/bin/env python3
"""
Fix WebForm list columns by adding proper Hebrew labels
"""

import frappe

def fix_webform_list_columns():
    """Update WebForm list columns with Hebrew labels"""

    try:
        # Get the WebForm
        webform = frappe.get_doc("Web Form", "פניית-ספק")

        # Clear existing list columns
        webform.list_columns = []

        # Add columns with proper labels
        columns = [
            {
                "fieldname": "name",
                "fieldtype": "Link",
                "label": "מספר פנייה"
            },
            {
                "fieldname": "topic_category",
                "fieldtype": "Link",
                "label": "קטגורית נושא"
            },
            {
                "fieldname": "inquiry_status",
                "fieldtype": "Data",
                "label": "סטטוס"
            },
            {
                "fieldname": "creation",
                "fieldtype": "Datetime",
                "label": "תאריך יצירה"
            }
        ]

        for idx, col in enumerate(columns, start=1):
            webform.append("list_columns", {
                "fieldname": col["fieldname"],
                "fieldtype": col["fieldtype"],
                "label": col["label"]
            })

        # Save the WebForm
        webform.save()
        frappe.db.commit()

        print("✅ Successfully updated WebForm list columns")
        print("\nList Columns:")
        for col in webform.list_columns:
            print(f"  - {col.fieldname}: {col.label}")

        return {"success": True, "message": "List columns updated successfully"}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        frappe.db.rollback()
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    fix_webform_list_columns()
