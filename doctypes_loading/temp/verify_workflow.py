"""
Verify Supplier Inquiry Workflow exists and is properly configured
"""

import frappe

@frappe.whitelist()
def verify():
    """Check if workflow exists and show its details"""

    if not frappe.db.exists("Workflow", "Supplier Inquiry Workflow"):
        frappe.msgprint("❌ Workflow does NOT exist!")
        return {"success": False, "message": "Workflow not found"}

    workflow = frappe.get_doc("Workflow", "Supplier Inquiry Workflow")

    frappe.msgprint("=" * 60)
    frappe.msgprint("✅ Supplier Inquiry Workflow EXISTS and is ACTIVE!")
    frappe.msgprint("=" * 60)
    frappe.msgprint(f"Workflow Name: {workflow.workflow_name}")
    frappe.msgprint(f"Document Type: {workflow.document_type}")
    frappe.msgprint(f"Is Active: {workflow.is_active}")
    frappe.msgprint(f"State Field: {workflow.workflow_state_field}")
    frappe.msgprint(f"\nNumber of States: {len(workflow.states)}")
    frappe.msgprint(f"Number of Transitions: {len(workflow.transitions)}")

    frappe.msgprint("\n📋 Workflow States:")
    for i, state in enumerate(workflow.states, 1):
        frappe.msgprint(f"  {i}. {state.state} (Status: {state.doc_status}, Edit: {state.allow_edit or 'None'})")

    frappe.msgprint("\n🔄 Workflow Transitions:")
    for i, trans in enumerate(workflow.transitions, 1):
        frappe.msgprint(f"  {i}. {trans.state} → [{trans.action}] → {trans.next_state} (Role: {trans.allowed})")

    frappe.msgprint("\n" + "=" * 60)

    return {
        "success": True,
        "workflow": workflow.workflow_name,
        "states": len(workflow.states),
        "transitions": len(workflow.transitions)
    }
