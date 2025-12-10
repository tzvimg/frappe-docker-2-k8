"""
Add Contact Person link to Supplier DocType
"""
import frappe

def add_contact_link():
    """Add link from Supplier to Contact Person"""

    # Get the Supplier DocType
    supplier_doctype = frappe.get_doc("DocType", "Supplier")

    # Check if link already exists
    existing_link = None
    for link in supplier_doctype.links:
        if link.link_doctype == "Contact Person":
            existing_link = link
            break

    if existing_link:
        print("✓ Link to Contact Person already exists")
        return

    # Add the link
    supplier_doctype.append("links", {
        "link_doctype": "Contact Person",
        "link_fieldname": "supplier_link",
        "group": "אנשי קשר"  # "Contacts" in Hebrew
    })

    # Save the DocType
    supplier_doctype.save()
    frappe.db.commit()

    print("✓ Successfully added Contact Person link to Supplier DocType")
    print("  Contact Persons will now appear on the Supplier form")
    print("\nNext steps:")
    print("  1. Clear cache: bench --site development.localhost clear-cache")
    print("  2. Reload the Supplier form in your browser")
    print("  3. You should see a 'אנשי קשר' (Contacts) section with Contact Persons")

if __name__ == "__main__":
    add_contact_link()
