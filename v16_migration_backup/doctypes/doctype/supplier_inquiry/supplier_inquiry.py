# Copyright (c) 2025, Tzvi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SupplierInquiry(Document):
	pass


def has_website_permission(doc, ptype, user, verbose=False):
	"""
	Permission check for portal users accessing Supplier Inquiry records.
	Portal users can only access inquiries linked to their supplier.

	Args:
		doc: The Supplier Inquiry document being accessed
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
		frappe.msgprint(f"User: {user}, User Supplier Link: {user_supplier_link}, Doc Supplier Link: {doc.supplier_link}")

	# Portal users can only see inquiries linked to their supplier
	if user_supplier_link and doc.supplier_link:
		return doc.supplier_link == user_supplier_link

	# If no supplier_link is set on user or document, deny access
	return False


def get_list_context(context=None):
	"""
	Filter the list view for WebForm to only show inquiries for the current user's supplier.
	This function is called by Frappe when rendering list views on the web.

	Args:
		context: Optional context dict

	Returns:
		dict: Context with filters applied
	"""
	if context is None:
		context = {}

	# Get current user's supplier link
	user = frappe.session.user
	if user and user != "Guest":
		user_doc = frappe.get_doc("User", user)
		supplier_link = user_doc.get("supplier_link")

		if supplier_link:
			# Add filter to only show inquiries for this supplier
			context["filters"] = {"supplier_link": supplier_link}
			context["title"] = "הפניות שלי"
		else:
			# If no supplier link, show empty list
			context["filters"] = {"supplier_link": ""}
			context["title"] = "הפניות שלי"
	else:
		# Guest users see nothing
		context["filters"] = {"supplier_link": ""}

	return context
