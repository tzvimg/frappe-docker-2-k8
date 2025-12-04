"""
Example Controller for DocType

This is a sample controller file that demonstrates common patterns
used in Frappe DocType controllers.
"""

import frappe
from frappe import _
from frappe.model.document import Document


class ExampleDocType(Document):
    """Controller class for Example DocType"""

    def validate(self):
        """
        Runs before save (both insert and update)
        Use this for validation logic
        """
        self.validate_required_fields()
        self.validate_dates()
        self.calculate_totals()

    def before_insert(self):
        """
        Runs before first save only
        Use this for initialization logic
        """
        if not self.status:
            self.status = "Draft"

    def after_insert(self):
        """
        Runs after first save only
        Use this for post-creation logic
        """
        self.create_related_records()

    def on_update(self):
        """
        Runs after any update
        Use this for sync logic
        """
        self.update_related_records()

    def on_submit(self):
        """
        Runs when document is submitted (if is_submittable=True)
        Use this for workflow transitions
        """
        self.validate_submission()
        self.update_status("Submitted")

    def on_cancel(self):
        """
        Runs when document is cancelled (if is_submittable=True)
        Use this for rollback logic
        """
        self.update_status("Cancelled")

    def before_save(self):
        """
        Runs before save (similar to validate but after validate)
        Use this for final adjustments before save
        """
        self.updated_by = frappe.session.user

    # Custom validation methods

    def validate_required_fields(self):
        """Validate that required fields are filled"""
        if not self.title:
            frappe.throw(_("Title is required"))

        if not self.start_date:
            frappe.throw(_("Start date is required"))

    def validate_dates(self):
        """Validate date logic"""
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                frappe.throw(_("End date cannot be before start date"))

    def calculate_totals(self):
        """Calculate totals from child table"""
        if hasattr(self, 'items'):
            self.total = sum(item.amount for item in self.items)

    # Custom action methods

    def create_related_records(self):
        """Create related records after insert"""
        # Example: Create a related document
        # related_doc = frappe.get_doc({
        #     'doctype': 'Related DocType',
        #     'reference': self.name,
        #     'status': 'Active'
        # })
        # related_doc.insert()
        pass

    def update_related_records(self):
        """Update related records after update"""
        # Example: Update related documents
        # related_docs = frappe.get_all('Related DocType',
        #     filters={'reference': self.name})
        # for doc in related_docs:
        #     frappe.db.set_value('Related DocType', doc.name, 'status', self.status)
        pass

    def validate_submission(self):
        """Validate before submission"""
        if self.status != "Approved":
            frappe.throw(_("Document must be approved before submission"))

    def update_status(self, status):
        """Update status and commit"""
        frappe.db.set_value(self.doctype, self.name, 'status', status)
        frappe.db.commit()


# Utility functions (can be called from outside the class)

def get_active_records():
    """Get all active records"""
    return frappe.get_all('Example DocType',
        filters={'status': 'Active'},
        fields=['name', 'title', 'start_date'])


def validate_unique_field(doc, field_name):
    """Validate that a field value is unique"""
    field_value = doc.get(field_name)
    if field_value:
        existing = frappe.db.exists(doc.doctype, {
            field_name: field_value,
            'name': ['!=', doc.name]
        })
        if existing:
            frappe.throw(_(f"{field_name} must be unique"))


# Whitelisted methods (can be called via API)

@frappe.whitelist()
def get_summary(docname):
    """
    Get summary information for a document
    Can be called from JavaScript or API
    """
    doc = frappe.get_doc('Example DocType', docname)
    return {
        'name': doc.name,
        'title': doc.title,
        'status': doc.status,
        'total': doc.total if hasattr(doc, 'total') else 0
    }


@frappe.whitelist()
def bulk_update_status(docnames, new_status):
    """
    Update status for multiple documents
    Can be called from JavaScript or API
    """
    if isinstance(docnames, str):
        import json
        docnames = json.loads(docnames)

    for docname in docnames:
        doc = frappe.get_doc('Example DocType', docname)
        doc.status = new_status
        doc.save()

    frappe.db.commit()
    return {'success': True, 'count': len(docnames)}


# Event hooks (can be registered in hooks.py)

def on_trash(doc, method):
    """
    Called when document is deleted
    Register in hooks.py:
        doc_events = {
            "Example DocType": {
                "on_trash": "path.to.controller.on_trash"
            }
        }
    """
    # Clean up related records
    frappe.db.delete('Related DocType', {'reference': doc.name})
