# Copyright (c) 2025, BTL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class ServiceProviderBranch(Document):
    def validate(self):
        """Validate Service Provider Branch data"""
        self.validate_branch_code()
        self.validate_unique_branch_per_provider()

    def validate_branch_code(self):
        """Validate that branch code is exactly 2 digits"""
        if self.branch_code:
            branch_clean = self.branch_code.strip()
            if not branch_clean.isdigit():
                frappe.throw(_("קוד סניף must contain only digits"))
            if len(branch_clean) != 2:
                frappe.throw(_("קוד סניף must be exactly 2 digits"))
            self.branch_code = branch_clean

    def validate_unique_branch_per_provider(self):
        """Ensure branch code is unique per service provider"""
        if not self.is_new():
            return

        existing = frappe.db.exists({
            "doctype": "Service Provider Branch",
            "service_provider": self.service_provider,
            "branch_code": self.branch_code,
            "name": ["!=", self.name]
        })

        if existing:
            frappe.throw(_("Branch code {0} already exists for this service provider").format(self.branch_code))

    def autoname(self):
        """Auto-generate name: {service_provider}-BR-{branch_code}"""
        if self.service_provider and self.branch_code:
            # Get the service provider's HP number
            sp_doc = frappe.get_doc("Service Provider", self.service_provider)
            self.name = f"{sp_doc.hp_number}-BR-{self.branch_code}"
