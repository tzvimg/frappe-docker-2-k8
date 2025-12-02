# Copyright (c) 2025, BTL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from datetime import datetime, timedelta


class Contract(Document):
    def validate(self):
        """Validate Contract data"""
        self.validate_dates()
        self.fetch_service_provider()
        self.check_expiry_status()

    def validate_dates(self):
        """Validate that end_date is after start_date"""
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                frappe.throw(_("תאריך סיום must be after תאריך תחילה"))

    def fetch_service_provider(self):
        """Auto-fetch service provider from branch"""
        if self.branch and not self.service_provider:
            branch_doc = frappe.get_doc("Service Provider Branch", self.branch)
            self.service_provider = branch_doc.service_provider

    def check_expiry_status(self):
        """Check if contract is expiring and update status"""
        if self.end_date and self.status == "פעיל":
            today = datetime.now().date()
            end_date = datetime.strptime(str(self.end_date), "%Y-%m-%d").date()

            # If contract has expired, update status
            if end_date < today:
                self.status = "פג תוקף"

            # Check if approaching expiry (within alert_days_before_expiry)
            if self.alert_days_before_expiry:
                alert_date = end_date - timedelta(days=self.alert_days_before_expiry)
                if today >= alert_date and today <= end_date:
                    frappe.msgprint(
                        _("Contract {0} is expiring on {1}").format(self.contract_number, self.end_date),
                        title=_("Contract Expiry Alert"),
                        indicator="orange"
                    )

    def autoname(self):
        """Auto-generate name: CON-{contract_number}"""
        if self.contract_number:
            self.name = f"CON-{self.contract_number}"
