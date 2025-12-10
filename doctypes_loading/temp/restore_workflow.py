"""
Restore Supplier Inquiry Workflow
Fixed version with proper allow_edit handling
"""

import frappe

@frappe.whitelist()
def restore_workflow():
    """Create the workflow for Supplier Inquiry with proper field handling"""

    # Check if Workflow already exists
    if frappe.db.exists("Workflow", "Supplier Inquiry Workflow"):
        frappe.msgprint("⚠ Supplier Inquiry Workflow already exists. Deleting and recreating...")
        frappe.delete_doc("Workflow", "Supplier Inquiry Workflow", force=1)
        frappe.db.commit()

    # First, check that Supplier Inquiry DocType exists
    if not frappe.db.exists("DocType", "Supplier Inquiry"):
        frappe.throw("Supplier Inquiry DocType does not exist. Please create it first.")

    workflow = frappe.get_doc({
        'doctype': 'Workflow',
        'workflow_name': 'Supplier Inquiry Workflow',
        'document_type': 'Supplier Inquiry',
        'is_active': 1,
        'workflow_state_field': 'inquiry_status',
        'send_email_alert': 0,
    })

    # Add states with proper allow_edit handling
    states_config = [
        {
            'state': 'פנייה חדשה התקבלה',
            'doc_status': '0',
            'allow_edit': 'Service Provider User',
            'message': 'הפנייה התקבלה ממתינה למיון',
        },
        {
            'state': 'מיון וניתוב',
            'doc_status': '0',
            'allow_edit': 'Sorting Clerk',
            'message': 'הפנייה בתהליך מיון והקצאה לגורם מטפל',
        },
        {
            'state': 'בטיפול',
            'doc_status': '0',
            'allow_edit': 'Handling Clerk',
            'message': 'הפנייה בטיפול פעיל',
        },
        {
            'state': 'דורש השלמות / המתנה',
            'doc_status': '0',
            'allow_edit': 'Handling Clerk',
            'message': 'הפנייה ממתינה למידע נוסף או תגובה חיצונית',
        },
        {
            'state': 'נסגר – ניתן מענה',
            'doc_status': '0',
            'allow_edit': 'Handling Clerk',
            'message': 'הפנייה נסגרה ונמסר מענה לספק',
        },
        {
            'state': 'סגור',
            'doc_status': '1',
            'allow_edit': 'System Manager',  # Final state - only System Manager can edit
            'message': 'הפנייה בארכיון',
        },
    ]

    for state_data in states_config:
        workflow.append('states', state_data)

    # Add transitions
    transitions_config = [
        # From: פנייה חדשה התקבלה
        {
            'state': 'פנייה חדשה התקבלה',
            'action': 'העבר למיון',
            'next_state': 'מיון וניתוב',
            'allowed': 'Sorting Clerk',
            'allow_self_approval': 0,
        },
        # From: מיון וניתוב
        {
            'state': 'מיון וניתוב',
            'action': 'הקצה לטיפול',
            'next_state': 'בטיפול',
            'allowed': 'Sorting Clerk',
            'allow_self_approval': 0,
        },
        # From: בטיפול
        {
            'state': 'בטיפול',
            'action': 'דרוש השלמות',
            'next_state': 'דורש השלמות / המתנה',
            'allowed': 'Handling Clerk',
            'allow_self_approval': 1,
        },
        {
            'state': 'בטיפול',
            'action': 'סגור עם מענה',
            'next_state': 'נסגר – ניתן מענה',
            'allowed': 'Handling Clerk',
            'allow_self_approval': 1,
        },
        # From: דורש השלמות / המתנה
        {
            'state': 'דורש השלמות / המתנה',
            'action': 'חזור לטיפול',
            'next_state': 'בטיפול',
            'allowed': 'Handling Clerk',
            'allow_self_approval': 1,
        },
        {
            'state': 'דורש השלמות / המתנה',
            'action': 'סגור עם מענה',
            'next_state': 'נסגר – ניתן מענה',
            'allowed': 'Handling Clerk',
            'allow_self_approval': 1,
        },
        # From: נסגר – ניתן מענה
        {
            'state': 'נסגר – ניתן מענה',
            'action': 'העבר לארכיון',
            'next_state': 'סגור',
            'allowed': 'System Manager',
            'allow_self_approval': 1,
        },
        {
            'state': 'נסגר – ניתן מענה',
            'action': 'פתח מחדש',
            'next_state': 'בטיפול',
            'allowed': 'Handling Clerk',
            'allow_self_approval': 1,
        },
    ]

    for transition_data in transitions_config:
        workflow.append('transitions', transition_data)

    try:
        workflow.insert()
        frappe.db.commit()
        frappe.msgprint(f"✓ Successfully restored Supplier Inquiry Workflow")
        frappe.msgprint(f"  - States: {len(workflow.states)}")
        frappe.msgprint(f"  - Transitions: {len(workflow.transitions)}")
        return {"success": True, "workflow": "Supplier Inquiry Workflow"}
    except Exception as e:
        frappe.db.rollback()
        frappe.msgprint(f"✗ Error creating workflow: {str(e)}")
        import traceback
        frappe.log_error(traceback.format_exc(), "Workflow Creation Error")
        raise
