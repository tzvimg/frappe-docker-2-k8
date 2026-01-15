import frappe
from frappe import _

def get_context(context):
	"""Portal page context for supplier profile"""

	# Ensure user is logged in
	if frappe.session.user == "Guest":
		frappe.throw(_("Please log in to access this page"), frappe.PermissionError)

	# Get current user's supplier link
	user = frappe.get_doc("User", frappe.session.user)
	supplier_link = user.get("supplier_link")

	# Add user info for header menu
	context["user_name"] = user.full_name or user.first_name or frappe.session.user
	context["user_email"] = frappe.session.user

	# Generate user initials for avatar
	name_parts = (user.full_name or user.first_name or frappe.session.user).split()
	if len(name_parts) >= 2:
		context["user_initials"] = name_parts[0][0] + name_parts[-1][0]
	elif len(name_parts) == 1:
		context["user_initials"] = name_parts[0][0:2] if len(name_parts[0]) >= 2 else name_parts[0][0]
	else:
		context["user_initials"] = frappe.session.user[0:2]
	context["user_initials"] = context["user_initials"].upper()

	if not supplier_link:
		frappe.throw(_("No supplier linked to your account. Please contact the administrator."), frappe.PermissionError)

	# Get supplier details
	try:
		supplier = frappe.get_doc("Supplier", supplier_link)

		# Pass supplier data to template
		context.supplier = {
			"name": supplier.name,
			"supplier_id": supplier.supplier_id,
			"supplier_name": supplier.supplier_name or "",
			"phone": supplier.phone or "",
			"email": supplier.email or "",
			"address": supplier.address or "",
		}

	except frappe.DoesNotExistError:
		frappe.throw(_("Supplier record not found. Please contact the administrator."), frappe.PermissionError)

	# Page metadata
	context.title = "פרופיל הספק"
	context.show_sidebar = True

	return context


@frappe.whitelist()
def update_supplier_profile(supplier_name, name, phone, email, address):
	"""Update supplier profile fields via AJAX"""

	# Ensure user is logged in
	if frappe.session.user == "Guest":
		frappe.throw(_("Please log in to perform this action"), frappe.PermissionError)

	# Get current user's supplier link
	user = frappe.get_doc("User", frappe.session.user)
	supplier_link = user.get("supplier_link")

	if not supplier_link:
		frappe.throw(_("No supplier linked to your account"), frappe.PermissionError)

	# Security check: ensure the supplier being updated matches the user's supplier_link
	if name != supplier_link:
		frappe.throw(_("You are not authorized to update this supplier profile"), frappe.PermissionError)

	# Get and update supplier
	try:
		supplier = frappe.get_doc("Supplier", name)

		# Update allowed fields only
		supplier.supplier_name = supplier_name
		supplier.phone = phone
		supplier.email = email
		supplier.address = address

		# Save with permissions check
		supplier.save(ignore_permissions=False)
		frappe.db.commit()

		return {
			"success": True,
			"message": _("Profile updated successfully")
		}

	except frappe.PermissionError:
		frappe.throw(_("You do not have permission to update this profile"), frappe.PermissionError)
	except Exception as e:
		frappe.log_error(f"Error updating supplier profile: {str(e)}")
		frappe.throw(_("An error occurred while updating the profile. Please try again."))
