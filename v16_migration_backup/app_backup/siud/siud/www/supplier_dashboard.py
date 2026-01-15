import frappe
from frappe import _

def get_context(context):
	"""Portal page context for supplier dashboard"""

	# Ensure user is logged in - redirect to login if Guest
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login?redirect-to=/supplier_dashboard"
		raise frappe.Redirect()

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
		# Show error message instead of throwing exception
		context["show_error"] = True
		context["error_title"] = _("No Supplier Linked")
		context["error_message"] = _("No supplier linked to your account. Please contact the administrator.")
		context["title"] = "Error - Supplier Portal"
		return

	# Get supplier details
	try:
		supplier = frappe.get_doc("Supplier", supplier_link)
		context["supplier_name"] = supplier.supplier_name or supplier.name
		context["supplier_id"] = supplier.name
	except frappe.DoesNotExistError:
		# Show error message instead of throwing exception
		context["show_error"] = True
		context["error_title"] = _("Supplier Not Found")
		context["error_message"] = _("Supplier record not found. Please contact the administrator.")
		context["title"] = "Error - Supplier Portal"
		return

	# Get inquiry statistics
	total_inquiries = frappe.db.count("Supplier Inquiry", {"supplier_link": supplier_link})

	# Count by status
	open_statuses = ["פתוחה", "בטיפול", "ממתינה לתגובת ספק"]
	open_inquiries = frappe.db.count("Supplier Inquiry", {
		"supplier_link": supplier_link,
		"inquiry_status": ["in", open_statuses]
	})

	closed_statuses = ["טופלה", "נסגרה", "נדחתה"]
	closed_inquiries = frappe.db.count("Supplier Inquiry", {
		"supplier_link": supplier_link,
		"inquiry_status": ["in", closed_statuses]
	})

	context["total_inquiries"] = total_inquiries
	context["open_inquiries"] = open_inquiries
	context["closed_inquiries"] = closed_inquiries

	# Get recent inquiries (last 5)
	recent_inquiries = frappe.get_all(
		"Supplier Inquiry",
		filters={"supplier_link": supplier_link},
		fields=["name", "topic_category", "inquiry_status", "creation", "modified"],
		order_by="creation desc",
		limit=5
	)

	context["recent_inquiries"] = recent_inquiries

	# Page metadata
	context["title"] = "דף הבית - פורטל ספקים"
	context["show_sidebar"] = True
