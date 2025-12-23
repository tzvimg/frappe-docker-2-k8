import frappe

def check_data():
    """Check supplier data and user links"""

    # Check if there are any suppliers
    suppliers = frappe.get_all('Supplier', fields=['name', 'supplier_id', 'supplier_name'], limit=5)
    print(f"\nFound {len(suppliers)} suppliers:")
    for s in suppliers:
        print(f"  - {s.get('name')} ({s.get('supplier_id')}): {s.get('supplier_name')}")

    # Check Administrator's supplier_link
    user = frappe.get_doc('User', 'Administrator')
    supplier_link = user.get('supplier_link')
    print(f"\nAdministrator supplier_link: {supplier_link}")

    # If no link but suppliers exist, link the first one
    if not supplier_link and suppliers:
        first_supplier = suppliers[0]['name']
        print(f"\nLinking Administrator to {first_supplier}...")
        user.supplier_link = first_supplier
        user.save(ignore_permissions=True)
        frappe.db.commit()
        print("✓ Linked successfully!")
    elif not suppliers:
        print("\n⚠ No suppliers found. Please create a supplier first.")

    return {"status": "success"}
