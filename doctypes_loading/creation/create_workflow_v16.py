"""Create Supplier Inquiry Workflow - Fixed for Frappe v16"""
import frappe

@frappe.whitelist()
def create_workflow():
    """Create the workflow for Supplier Inquiry - Fixed for v16"""

    if frappe.db.exists("Workflow", "Supplier Inquiry Workflow"):
        frappe.msgprint("⚠ Supplier Inquiry Workflow already exists. Skipping.")
        return {"success": False, "message": "Already exists"}

    workflow = frappe.get_doc({
        'doctype': 'Workflow',
        'workflow_name': 'Supplier Inquiry Workflow',
        'document_type': 'Supplier Inquiry',
        'is_active': 1,
        'workflow_state_field': 'inquiry_status',
        'send_email_alert': 0,
        'states': [
            {
                'state': 'פנייה חדשה התקבלה',
                'doc_status': '0',
                'allow_edit': 'System Manager',
            },
            {
                'state': 'מיון וניתוב',
                'doc_status': '0',
                'allow_edit': 'Sorting Clerk',
            },
            {
                'state': 'בטיפול',
                'doc_status': '0',
                'allow_edit': 'Handling Clerk',
            },
            {
                'state': 'דורש השלמות / המתנה',
                'doc_status': '0',
                'allow_edit': 'Handling Clerk',
            },
            {
                'state': 'נסגר – ניתן מענה',
                'doc_status': '0',
                'allow_edit': 'Handling Clerk',
            },
            {
                'state': 'סגור',
                'doc_status': '0',
                'allow_edit': 'System Manager',
            },
        ],
        'transitions': [
            {
                'state': 'פנייה חדשה התקבלה',
                'action': 'העבר למיון',
                'next_state': 'מיון וניתוב',
                'allowed': 'Sorting Clerk',
                'allow_self_approval': 0,
            },
            {
                'state': 'מיון וניתוב',
                'action': 'הקצה לטיפול',
                'next_state': 'בטיפול',
                'allowed': 'Sorting Clerk',
                'allow_self_approval': 0,
            },
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
    })

    workflow.insert()
    frappe.db.commit()
    print(f"✓ Created Supplier Inquiry Workflow")
    return {"success": True}
