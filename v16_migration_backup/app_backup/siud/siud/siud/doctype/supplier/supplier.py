# Copyright (c) 2025, Tzvi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Supplier(Document):
	pass


def has_website_permission(doc, ptype, user, verbose=False):
	"""
	Permission check for portal users accessing Supplier records.
	Portal users can only access their own linked supplier record.

	Args:
		doc: The Supplier document being accessed
		ptype: Permission type (read, write, etc.)
		user: Email of the user requesting access
		verbose: If True, print debug information

	Returns:
		bool: True if user has permission, False otherwise
	"""
	if not user:
		return False

	# Get the supplier_link from the User document
	user_doc = frappe.get_doc("User", user)
	user_supplier_link = user_doc.get("supplier_link")

	if verbose:
		frappe.msgprint(f"User: {user}, User Supplier Link: {user_supplier_link}, Doc Name: {doc.name}")

	# Portal users can only see their own linked supplier record
	if user_supplier_link:
		return doc.name == user_supplier_link

	# If no supplier_link is set on user, deny access
	return False
