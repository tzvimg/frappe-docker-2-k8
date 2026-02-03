"""Verify all created entities"""
import frappe

@frappe.whitelist()
def verify():
    """Verify all DocTypes, Workflows, and Workspaces"""
    
    print("\n=== DocTypes in Siud Module ===")
    doctypes = frappe.get_all('DocType', filters={'module': 'Siud'}, pluck='name')
    for dt in doctypes:
        print(f"  ✓ {dt}")
    
    print(f"\nTotal DocTypes: {len(doctypes)}")
    
    print("\n=== Workflows ===")
    workflows = frappe.get_all('Workflow', filters={'document_type': ['in', doctypes]}, pluck='name')
    for wf in workflows:
        print(f"  ✓ {wf}")
    
    print(f"\nTotal Workflows: {len(workflows)}")
    
    print("\n=== Workspaces ===")
    workspaces = frappe.get_all('Workspace', filters={'module': 'Siud'}, pluck='name')
    for ws in workspaces:
        print(f"  ✓ {ws}")
    
    print(f"\nTotal Workspaces: {len(workspaces)}")
    
    return {
        "doctypes": doctypes,
        "workflows": workflows,
        "workspaces": workspaces
    }
