#!/usr/bin/env python3
"""Check for Client Scripts attached to Supplier Inquiry DocType"""
import frappe

def check_scripts():
    """Find and display Client Scripts for Supplier Inquiry"""

    # Check Client Scripts
    print("=" * 60)
    print("CLIENT SCRIPTS for Supplier Inquiry")
    print("=" * 60)

    client_scripts = frappe.get_all(
        'Client Script',
        filters={'dt': 'Supplier Inquiry'},
        fields=['name', 'enabled']
    )

    if client_scripts:
        for script in client_scripts:
            doc = frappe.get_doc('Client Script', script.name)
            print(f"\nName: {doc.name}")
            print(f"Enabled: {doc.enabled}")
            print(f"Script Type: {doc.script_type if hasattr(doc, 'script_type') else 'N/A'}")
            print(f"\nScript Content:")
            print("-" * 60)
            print(doc.script)
            print("-" * 60)
    else:
        print("No Client Scripts found")

    # Check for Custom Script in Customize Form
    print("\n" + "=" * 60)
    print("CUSTOM SCRIPT in Property Setter")
    print("=" * 60)

    custom_scripts = frappe.get_all(
        'Property Setter',
        filters={
            'doc_type': 'Supplier Inquiry',
            'property': 'custom_script'
        },
        fields=['name', 'value']
    )

    if custom_scripts:
        for ps in custom_scripts:
            print(f"\nProperty Setter: {ps.name}")
            print(f"Custom Script:")
            print("-" * 60)
            print(ps.value)
            print("-" * 60)
    else:
        print("No custom scripts in Property Setter")

    frappe.db.commit()
    return {"success": True, "message": "Check complete"}

if __name__ == "__main__":
    check_scripts()
