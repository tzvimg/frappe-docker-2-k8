import frappe

# Import all creation functions
from .create_role import create_supplier_role_doctype
from .create_activity_domain_category import create_activity_domain_category_doctype
from .create_inquiry_topic_category import create_inquiry_topic_category_doctype
from .create_supplier import create_supplier_doctype, create_supplier_activity_domain_child
from .create_contact_person import create_contact_person_doctype, create_contact_person_role_child
from .create_supplier_inquiry import create_supplier_inquiry_doctype
from .create_delegated_supplier import create_delegated_supplier_scope_child, create_delegated_supplier_doctype

@frappe.whitelist()
def create_all_doctypes():
    """
    Master script to create all DocTypes for Supplier Inquiry Management POC

    Order is important:
    1. First create independent master DocTypes (Role, Activity Domain Category, Inquiry Topic Category)
    2. Then create child tables that depend on masters
    3. Finally create parent DocTypes that depend on everything else
    """

    results = []

    try:
        # Step 1: Create independent master DocTypes
        frappe.msgprint("Creating independent master DocTypes...")

        # Supplier Role - independent
        create_supplier_role_doctype()
        results.append("✓ Supplier Role DocType created")

        # Activity Domain Category - independent
        create_activity_domain_category_doctype()
        results.append("✓ Activity Domain Category DocType created")

        # Inquiry Topic Category - independent (self-referencing is ok)
        create_inquiry_topic_category_doctype()
        results.append("✓ Inquiry Topic Category DocType created")

        # Step 2: Create child tables
        frappe.msgprint("Creating child table DocTypes...")

        # Supplier Activity Domain child (depends on Activity Domain Category)
        create_supplier_activity_domain_child()
        results.append("✓ Supplier Activity Domain child table created")

        # Contact Person Role child (depends on Supplier Role)
        create_contact_person_role_child()
        results.append("✓ Contact Person Role child table created")

        # Step 3: Create parent DocTypes
        frappe.msgprint("Creating parent DocTypes...")

        # Supplier (depends on Supplier Activity Domain child table)
        create_supplier_doctype()
        results.append("✓ Supplier DocType created")

        # Contact Person (depends on Supplier, Supplier Role, Contact Person Role child)
        create_contact_person_doctype()
        results.append("✓ Contact Person DocType created")

        # Supplier Inquiry (depends on Supplier, Inquiry Topic Category, Supplier Role, User)
        create_supplier_inquiry_doctype()
        results.append("✓ Supplier Inquiry DocType created")

        # Delegated Supplier Scope child (depends on Activity Domain Category)
        create_delegated_supplier_scope_child()
        results.append("✓ Delegated Supplier Scope child table created")

        # Delegated Supplier (depends on Supplier, Delegated Supplier Scope)
        create_delegated_supplier_doctype()
        results.append("✓ Delegated Supplier DocType created")

        # Final message
        frappe.msgprint("<br>".join(results) + "<br><br><b>All DocTypes created successfully!</b>")

        return {
            "success": True,
            "message": "All DocTypes created successfully",
            "details": results
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "DocType Creation Error")
        frappe.throw(f"Error creating DocTypes: {str(e)}")


@frappe.whitelist()
def delete_all_doctypes():
    """
    Utility function to delete all created DocTypes (in reverse order)
    WARNING: This will delete all data!
    """

    doctypes_to_delete = [
        "Delegated Supplier",
        "Delegated Supplier Scope",
        "Supplier Inquiry",
        "Contact Person",
        "Supplier",
        "Contact Person Role",
        "Supplier Activity Domain",
        "Inquiry Topic Category",
        "Activity Domain Category",
        "Supplier Role"
    ]

    results = []

    for dt_name in doctypes_to_delete:
        try:
            if frappe.db.exists("DocType", dt_name):
                frappe.delete_doc("DocType", dt_name, force=True)
                results.append(f"✓ Deleted {dt_name}")
                frappe.msgprint(f"Deleted {dt_name}")
        except Exception as e:
            results.append(f"✗ Error deleting {dt_name}: {str(e)}")
            frappe.msgprint(f"Error deleting {dt_name}: {str(e)}")

    frappe.db.commit()
    frappe.clear_cache()

    frappe.msgprint("<br>".join(results) + "<br><br><b>Deletion complete</b>")

    return {
        "success": True,
        "message": "Deletion process completed",
        "details": results
    }
