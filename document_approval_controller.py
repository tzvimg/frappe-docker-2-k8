# Copyright (c) 2025, BTL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from datetime import datetime, timedelta


class DocumentApproval(Document):
    def validate(self):
        """Validate Document Approval data"""
        self.validate_expiry_date()
        self.check_document_status()

    def validate_expiry_date(self):
        """Validate that expiry_date is after submission_date"""
        if self.submission_date and self.expiry_date:
            if self.expiry_date < self.submission_date:
                frappe.throw(_("תאריך תוקף must be after תאריך הגשה"))

    def check_document_status(self):
        """Check document expiry and update status"""
        if self.expiry_date and self.status == "תקין":
            today = datetime.now().date()
            expiry_date = datetime.strptime(str(self.expiry_date), "%Y-%m-%d").date()

            # If document has expired, change status
            if expiry_date < today:
                frappe.msgprint(
                    _("Document {0} has expired on {1}").format(self.document_number, self.expiry_date),
                    title=_("Document Expired"),
                    indicator="red"
                )

            # Alert if expiring within 30 days
            alert_date = expiry_date - timedelta(days=30)
            if today >= alert_date and today <= expiry_date:
                frappe.msgprint(
                    _("Document {0} is expiring on {1}").format(self.document_number, self.expiry_date),
                    title=_("Document Expiry Alert"),
                    indicator="orange"
                )

    def on_update(self):
        """Trigger notifications when status changes"""
        if self.has_value_changed("status"):
            self.send_status_notification()

    def send_status_notification(self):
        """Send email notification when document status changes"""
        if self.status in ["תקין", "לא תקין"]:
            # Get contract details
            contract = frappe.get_doc("Contract", self.contract)

            subject = _("Document {0} Status Changed: {1}").format(self.document_number, self.status)
            message = _("""
                <p>Document approval status has been updated:</p>
                <ul>
                    <li><strong>Document Number:</strong> {0}</li>
                    <li><strong>Document Type:</strong> {1}</li>
                    <li><strong>Status:</strong> {2}</li>
                    <li><strong>Contract:</strong> {3}</li>
                    <li><strong>Reviewer:</strong> {4}</li>
                    <li><strong>Review Date:</strong> {5}</li>
                </ul>
            """).format(
                self.document_number,
                self.document_type,
                self.status,
                contract.contract_number,
                self.reviewer or "N/A",
                self.review_date or "N/A"
            )

            if self.status == "לא תקין" and self.rejection_reason:
                message += _("<p><strong>Rejection Reason:</strong> {0}</p>").format(self.rejection_reason)

            frappe.log_error(message=message, title=subject)

    def autoname(self):
        """Auto-generate name: DOC-{document_number}"""
        if self.document_number:
            self.name = f"DOC-{self.document_number}"
