"""Create Workflow States and Actions for Supplier Inquiry Workflow"""
import frappe

@frappe.whitelist()
def create_workflow_states():
    """Create all workflow states needed for Supplier Inquiry workflow"""
    
    states = [
        'פנייה חדשה התקבלה',
        'מיון וניתוב', 
        'בטיפול',
        'דורש השלמות / המתנה',
        'נסגר – ניתן מענה',
        'סגור'
    ]
    
    for state in states:
        if not frappe.db.exists('Workflow State', state):
            doc = frappe.get_doc({'doctype': 'Workflow State', 'workflow_state_name': state})
            doc.insert()
            print(f'✓ Created state: {state}')
        else:
            print(f'⚠ State exists: {state}')
    
    frappe.db.commit()
    return {"success": True}

@frappe.whitelist()
def create_workflow_actions():
    """Create all workflow actions needed for Supplier Inquiry workflow"""
    
    actions = [
        'העבר למיון',
        'הקצה לטיפול',
        'דרוש השלמות',
        'סגור עם מענה',
        'חזור לטיפול',
        'העבר לארכיון',
        'פתח מחדש'
    ]
    
    for action in actions:
        if not frappe.db.exists('Workflow Action Master', action):
            doc = frappe.get_doc({'doctype': 'Workflow Action Master', 'workflow_action_name': action})
            doc.insert()
            print(f'✓ Created action: {action}')
        else:
            print(f'⚠ Action exists: {action}')
    
    frappe.db.commit()
    return {"success": True}

@frappe.whitelist()
def create_all():
    """Create all workflow states and actions"""
    create_workflow_states()
    create_workflow_actions()
    print('✓ All workflow states and actions created')
    return {"success": True}
