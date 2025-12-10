"""
Create only the Supplier Inquiry Workflow
Separate script to troubleshoot workflow creation
"""

import frappe

@frappe.whitelist()
def create_workflow():
    """Create the workflow for Supplier Inquiry - using correct child table structure"""

    # Check if Workflow already exists
    if frappe.db.exists("Workflow", "Supplier Inquiry Workflow"):
        frappe.msgprint("⚠ Supplier Inquiry Workflow already exists. Deleting and recreating...")
        frappe.delete_doc("Workflow", "Supplier Inquiry Workflow", force=1)
        frappe.db.commit()

    # First, let's check that Supplier Inquiry DocType exists
    if not frappe.db.exists("DocType", "Supplier Inquiry"):
        frappe.throw("Supplier Inquiry DocType does not exist. Please create it first.")

    workflow = frappe.get_doc({
        'doctype': 'Workflow',
        'workflow_name': 'Supplier Inquiry Workflow',
        'document_type': 'Supplier Inquiry',
        'is_active': 1,
        'workflow_state_field': 'inquiry_status',
        'send_email_alert': 0,  # Disable email for now
    })

    # Add states (must be added as child table entries)
    workflow.append('states', {
        'state': 'פנייה חדשה התקבלה',
        'doc_status': '0',
        'allow_edit': 'Service Provider User',
        'message': 'הפנייה התקבלה ממתינה למיון',
    })

    workflow.append('states', {
        'state': 'מיון וניתוב',
        'doc_status': '0',
        'allow_edit': 'Sorting Clerk',
        'message': 'הפנייה בתהליך מיון והקצאה לגורם מטפל',
    })

    workflow.append('states', {
        'state': 'בטיפול',
        'doc_status': '0',
        'allow_edit': 'Handling Clerk',
        'message': 'הפנייה בטיפול פעיל',
    })

    workflow.append('states', {
        'state': 'דורש השלמות / המתנה',
        'doc_status': '0',
        'allow_edit': 'Handling Clerk',
        'message': 'הפנייה ממתינה למידע נוסף או תגובה חיצונית',
    })

    workflow.append('states', {
        'state': 'נסגר – ניתן מענה',
        'doc_status': '0',
        'allow_edit': 'Handling Clerk',
        'message': 'הפנייה נסגרה ונמסר מענה לספק',
    })

    workflow.append('states', {
        'state': 'סגור',
        'doc_status': '1',
        'allow_edit': '',
        'message': 'הפנייה בארכיון',
    })

    # Add transitions
    # From: פנייה חדשה התקבלה
    workflow.append('transitions', {
        'state': 'פנייה חדשה התקבלה',
        'action': 'העבר למיון',
        'next_state': 'מיון וניתוב',
        'allowed': 'Sorting Clerk',
        'allow_self_approval': 0,
    })

    # From: מיון וניתוב
    workflow.append('transitions', {
        'state': 'מיון וניתוב',
        'action': 'הקצה לטיפול',
        'next_state': 'בטיפול',
        'allowed': 'Sorting Clerk',
        'allow_self_approval': 0,
    })

    # From: בטיפול
    workflow.append('transitions', {
        'state': 'בטיפול',
        'action': 'דרוש השלמות',
        'next_state': 'דורש השלמות / המתנה',
        'allowed': 'Handling Clerk',
        'allow_self_approval': 1,
    })

    workflow.append('transitions', {
        'state': 'בטיפול',
        'action': 'סגור עם מענה',
        'next_state': 'נסגר – ניתן מענה',
        'allowed': 'Handling Clerk',
        'allow_self_approval': 1,
    })

    # From: דורש השלמות / המתנה
    workflow.append('transitions', {
        'state': 'דורש השלמות / המתנה',
        'action': 'חזור לטיפול',
        'next_state': 'בטיפול',
        'allowed': 'Handling Clerk',
        'allow_self_approval': 1,
    })

    workflow.append('transitions', {
        'state': 'דורש השלמות / המתנה',
        'action': 'סגור עם מענה',
        'next_state': 'נסגר – ניתן מענה',
        'allowed': 'Handling Clerk',
        'allow_self_approval': 1,
    })

    # From: נסגר – ניתן מענה
    workflow.append('transitions', {
        'state': 'נסגר – ניתן מענה',
        'action': 'העבר לארכיון',
        'next_state': 'סגור',
        'allowed': 'System Manager',
        'allow_self_approval': 1,
    })

    workflow.append('transitions', {
        'state': 'נסגר – ניתן מענה',
        'action': 'פתח מחדש',
        'next_state': 'בטיפול',
        'allowed': 'Handling Clerk',
        'allow_self_approval': 1,
    })

    try:
        workflow.insert()
        frappe.db.commit()
        frappe.msgprint(f"✓ Created Supplier Inquiry Workflow with {len(workflow.states)} states and {len(workflow.transitions)} transitions")
        return {"success": True, "workflow": "Supplier Inquiry Workflow"}
    except Exception as e:
        frappe.db.rollback()
        frappe.msgprint(f"✗ Error creating workflow: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}
