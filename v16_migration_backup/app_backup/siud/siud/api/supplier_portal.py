# Copyright (c) 2025, Tzvi and contributors
# For license information, please see license.txt

"""
Supplier Portal API

Whitelisted methods for the standalone Supplier Portal UI.
All methods require authentication and validate supplier_link access.
"""

import frappe
from frappe import _


# =============================================================================
# Helper Functions
# =============================================================================

def get_user_supplier_link():
	"""
	Get the supplier_link for the current logged-in user.

	Returns:
		str: The supplier document name linked to the user

	Raises:
		frappe.AuthenticationError: If user is not logged in
		frappe.PermissionError: If user has no supplier_link
	"""
	if frappe.session.user == "Guest":
		frappe.throw(_("Please log in to access this resource"), frappe.AuthenticationError)

	user = frappe.get_doc("User", frappe.session.user)
	supplier_link = user.get("supplier_link")

	if not supplier_link:
		frappe.throw(_("No supplier linked to your account. Please contact the administrator."), frappe.PermissionError)

	return supplier_link


def validate_supplier_access(supplier_name):
	"""
	Validate that the current user has access to the specified supplier.

	Args:
		supplier_name: The supplier document name to validate access for

	Raises:
		frappe.PermissionError: If user doesn't have access to this supplier
	"""
	user_supplier_link = get_user_supplier_link()

	if supplier_name != user_supplier_link:
		frappe.throw(_("You are not authorized to access this supplier"), frappe.PermissionError)


# =============================================================================
# Authentication & User Info
# =============================================================================

@frappe.whitelist()
def get_current_user():
	"""
	Get the current logged-in user's information and linked supplier.

	Returns:
		dict: {
			"user": {
				"email": str,
				"full_name": str,
				"first_name": str,
				"initials": str
			},
			"supplier": {
				"name": str,  # Document ID
				"supplier_id": str,
				"supplier_name": str
			}
		}
	"""
	supplier_link = get_user_supplier_link()
	user = frappe.get_doc("User", frappe.session.user)

	# Generate user initials
	name_parts = (user.full_name or user.first_name or frappe.session.user).split()
	if len(name_parts) >= 2:
		initials = name_parts[0][0] + name_parts[-1][0]
	elif len(name_parts) == 1:
		initials = name_parts[0][0:2] if len(name_parts[0]) >= 2 else name_parts[0][0]
	else:
		initials = frappe.session.user[0:2]

	# Get supplier details
	supplier = frappe.get_doc("Supplier", supplier_link)

	return {
		"user": {
			"email": frappe.session.user,
			"full_name": user.full_name or "",
			"first_name": user.first_name or "",
			"initials": initials.upper()
		},
		"supplier": {
			"name": supplier.name,
			"supplier_id": supplier.supplier_id,
			"supplier_name": supplier.supplier_name or supplier.name
		}
	}


# =============================================================================
# Supplier Profile
# =============================================================================

@frappe.whitelist()
def get_supplier_profile():
	"""
	Get the current user's supplier profile details.

	Returns:
		dict: {
			"name": str,  # Document ID
			"supplier_id": str,
			"supplier_name": str,
			"phone": str,
			"email": str,
			"address": str,
			"activity_domains": list,  # List of activity domain categories
			"contact_persons": list    # List of contact persons
		}
	"""
	supplier_link = get_user_supplier_link()
	supplier = frappe.get_doc("Supplier", supplier_link)

	# Get activity domains
	activity_domains = []
	if hasattr(supplier, 'activity_domains') and supplier.activity_domains:
		for ad in supplier.activity_domains:
			activity_domains.append({
				"activity_domain_category": ad.activity_domain_category
			})

	# Get contact persons
	contact_persons = []
	if hasattr(supplier, 'contact_persons') and supplier.contact_persons:
		for cp in supplier.contact_persons:
			contact_persons.append({
				"full_name": cp.full_name,
				"role": cp.role,
				"phone": cp.phone,
				"email": cp.email,
				"is_primary": cp.is_primary
			})

	return {
		"name": supplier.name,
		"supplier_id": supplier.supplier_id,
		"supplier_name": supplier.supplier_name or "",
		"phone": supplier.phone or "",
		"email": supplier.email or "",
		"address": supplier.address or "",
		"activity_domains": activity_domains,
		"contact_persons": contact_persons
	}


@frappe.whitelist()
def update_supplier_profile(supplier_name, phone, email, address):
	"""
	Update the current user's supplier profile.

	Args:
		supplier_name: Updated supplier name
		phone: Updated phone number
		email: Updated email address
		address: Updated address

	Returns:
		dict: {"success": True, "message": str}
	"""
	supplier_link = get_user_supplier_link()

	try:
		supplier = frappe.get_doc("Supplier", supplier_link)

		# Update allowed fields only
		supplier.supplier_name = supplier_name
		supplier.phone = phone
		supplier.email = email
		supplier.address = address

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


# =============================================================================
# Inquiry Statistics
# =============================================================================

@frappe.whitelist()
def get_inquiry_stats():
	"""
	Get inquiry statistics for the current user's supplier.

	Returns:
		dict: {
			"total": int,
			"open": int,
			"closed": int,
			"by_status": dict  # Count per status
		}
	"""
	supplier_link = get_user_supplier_link()

	# Total count
	total = frappe.db.count("Supplier Inquiry", {"supplier_link": supplier_link})

	# Open statuses (Hebrew)
	open_statuses = ["פנייה חדשה התקבלה", "מיון וניתוב", "בטיפול", "דורש השלמות / המתנה"]
	open_count = frappe.db.count("Supplier Inquiry", {
		"supplier_link": supplier_link,
		"inquiry_status": ["in", open_statuses]
	})

	# Closed statuses (Hebrew)
	closed_statuses = ["נסגר – ניתן מענה", "סגור"]
	closed_count = frappe.db.count("Supplier Inquiry", {
		"supplier_link": supplier_link,
		"inquiry_status": ["in", closed_statuses]
	})

	# Count by individual status
	all_statuses = open_statuses + closed_statuses
	by_status = {}
	for status in all_statuses:
		count = frappe.db.count("Supplier Inquiry", {
			"supplier_link": supplier_link,
			"inquiry_status": status
		})
		by_status[status] = count

	return {
		"total": total,
		"open": open_count,
		"closed": closed_count,
		"by_status": by_status
	}


# =============================================================================
# Inquiry CRUD
# =============================================================================

@frappe.whitelist()
def get_inquiries(
	page=1,
	page_size=20,
	status=None,
	date_from=None,
	date_to=None,
	order_by="creation desc"
):
	"""
	Get paginated list of inquiries for the current user's supplier.

	Args:
		page: Page number (1-indexed)
		page_size: Number of items per page (max 100)
		status: Filter by inquiry_status (optional)
		date_from: Filter by creation date >= (optional, YYYY-MM-DD)
		date_to: Filter by creation date <= (optional, YYYY-MM-DD)
		order_by: Sort order (default: "creation desc")

	Returns:
		dict: {
			"data": list,  # List of inquiry objects
			"total": int,  # Total count (for pagination)
			"page": int,
			"page_size": int,
			"total_pages": int
		}
	"""
	supplier_link = get_user_supplier_link()

	# Validate and sanitize inputs
	page = max(1, int(page))
	page_size = min(100, max(1, int(page_size)))

	# Build filters
	filters = {"supplier_link": supplier_link}

	if status:
		filters["inquiry_status"] = status

	if date_from:
		filters["creation"] = [">=", date_from]

	if date_to:
		if "creation" in filters:
			# Already have date_from, need to use AND
			filters["creation"] = ["between", [date_from, date_to + " 23:59:59"]]
		else:
			filters["creation"] = ["<=", date_to + " 23:59:59"]

	# Validate order_by to prevent SQL injection
	allowed_order_fields = ["creation", "modified", "inquiry_status", "topic_category"]
	order_parts = order_by.lower().split()
	if len(order_parts) >= 1 and order_parts[0] not in allowed_order_fields:
		order_by = "creation desc"

	# Get total count
	total = frappe.db.count("Supplier Inquiry", filters)

	# Calculate pagination
	total_pages = (total + page_size - 1) // page_size
	start = (page - 1) * page_size

	# Get inquiries
	inquiries = frappe.get_all(
		"Supplier Inquiry",
		filters=filters,
		fields=[
			"name",
			"topic_category",
			"inquiry_status",
			"inquiry_context",
			"inquiry_description",
			"creation",
			"modified"
		],
		order_by=order_by,
		start=start,
		limit=page_size
	)

	return {
		"data": inquiries,
		"total": total,
		"page": page,
		"page_size": page_size,
		"total_pages": total_pages
	}


@frappe.whitelist()
def get_inquiry(name):
	"""
	Get a single inquiry by name/ID.

	Args:
		name: The inquiry document name

	Returns:
		dict: Full inquiry details including attachments
	"""
	supplier_link = get_user_supplier_link()

	# Get the inquiry
	inquiry = frappe.get_doc("Supplier Inquiry", name)

	# Validate access
	if inquiry.supplier_link != supplier_link:
		frappe.throw(_("You are not authorized to access this inquiry"), frappe.PermissionError)

	# Get attachments
	attachments = frappe.get_all(
		"File",
		filters={
			"attached_to_doctype": "Supplier Inquiry",
			"attached_to_name": name
		},
		fields=["name", "file_name", "file_url", "file_size", "creation"]
	)

	return {
		"name": inquiry.name,
		"topic_category": inquiry.topic_category,
		"inquiry_status": inquiry.inquiry_status,
		"inquiry_context": inquiry.inquiry_context,
		"inquiry_description": inquiry.inquiry_description,
		"insured_id_number": inquiry.insured_id_number if hasattr(inquiry, 'insured_id_number') else None,
		"insured_full_name": inquiry.insured_full_name if hasattr(inquiry, 'insured_full_name') else None,
		"admin_response": inquiry.admin_response if hasattr(inquiry, 'admin_response') else None,
		"creation": inquiry.creation,
		"modified": inquiry.modified,
		"attachments": attachments
	}


@frappe.whitelist()
def create_inquiry(topic_category, description, inquiry_context, insured_id=None, insured_name=None):
	"""
	Create a new inquiry for the current user's supplier.

	Args:
		topic_category: The inquiry topic category (required)
		description: Description of the inquiry (required)
		inquiry_context: Context type - "ספק עצמו" or "מבוטח" (required)
		insured_id: Insured person ID (required if inquiry_context == "מבוטח")
		insured_name: Insured person name (required if inquiry_context == "מבוטח")

	Returns:
		dict: {"success": True, "name": str, "message": str}
	"""
	supplier_link = get_user_supplier_link()

	# Validate required fields
	if not topic_category:
		frappe.throw(_("Topic category is required"))

	if not description:
		frappe.throw(_("Description is required"))

	if not inquiry_context:
		frappe.throw(_("Inquiry context is required"))

	# Validate conditional fields
	if inquiry_context == "מבוטח":
		if not insured_id:
			frappe.throw(_("Insured ID is required when inquiry is about an insured person"))
		if not insured_name:
			frappe.throw(_("Insured name is required when inquiry is about an insured person"))

	try:
		# Create the inquiry
		inquiry = frappe.get_doc({
			"doctype": "Supplier Inquiry",
			"supplier_link": supplier_link,
			"topic_category": topic_category,
			"inquiry_description": description,
			"inquiry_context": inquiry_context,
			"inquiry_status": "פנייה חדשה התקבלה",  # Default status
			"insured_id_number": insured_id if inquiry_context == "מבוטח" else None,
			"insured_full_name": insured_name if inquiry_context == "מבוטח" else None
		})

		inquiry.insert(ignore_permissions=False)
		frappe.db.commit()

		return {
			"success": True,
			"name": inquiry.name,
			"message": _("Inquiry created successfully")
		}

	except Exception as e:
		frappe.log_error(f"Error creating inquiry: {str(e)}")
		frappe.throw(_("An error occurred while creating the inquiry. Please try again."))


# =============================================================================
# Reference Data
# =============================================================================

@frappe.whitelist(allow_guest=True)
def get_reference_data():
	"""
	Get all reference data needed for the portal.
	This method allows guest access for build-time data sync.

	Returns:
		dict: {
			"activity_domains": list,
			"inquiry_topics": list,
			"supplier_roles": list,
			"contact_person_roles": list,
			"inquiry_statuses": list,
			"inquiry_contexts": list
		}
	"""
	# Activity Domain Categories
	activity_domains = frappe.get_all(
		"Activity Domain Category",
		fields=["name", "category_code", "category_name"],
		order_by="category_name"
	)

	# Inquiry Topic Categories (hierarchical)
	inquiry_topics = frappe.get_all(
		"Inquiry Topic Category",
		fields=["name", "category_code", "category_name", "parent_inquiry_topic_category"],
		order_by="lft"  # NestedSet order
	)

	# Supplier Roles
	supplier_roles = frappe.get_all(
		"Supplier Role",
		fields=["name", "role_name", "role_title_he"],
		order_by="role_name"
	)

	# Contact Person Roles
	contact_person_roles = frappe.get_all(
		"Contact Person Role",
		fields=["name", "role"],
		order_by="role"
	)

	# Static reference data
	inquiry_statuses = [
		{"value": "פנייה חדשה התקבלה", "label": "פנייה חדשה התקבלה", "type": "open"},
		{"value": "מיון וניתוב", "label": "מיון וניתוב", "type": "open"},
		{"value": "בטיפול", "label": "בטיפול", "type": "open"},
		{"value": "דורש השלמות / המתנה", "label": "דורש השלמות / המתנה", "type": "open"},
		{"value": "נסגר – ניתן מענה", "label": "נסגר – ניתן מענה", "type": "closed"},
		{"value": "סגור", "label": "סגור", "type": "closed"}
	]

	inquiry_contexts = [
		{"value": "ספק עצמו", "label": "ספק עצמו"},
		{"value": "מבוטח", "label": "מבוטח"}
	]

	return {
		"activity_domains": activity_domains,
		"inquiry_topics": inquiry_topics,
		"supplier_roles": supplier_roles,
		"contact_person_roles": contact_person_roles,
		"inquiry_statuses": inquiry_statuses,
		"inquiry_contexts": inquiry_contexts
	}


# =============================================================================
# File Upload
# =============================================================================

@frappe.whitelist()
def attach_file_to_inquiry(inquiry_name, file_url):
	"""
	Attach an uploaded file to an inquiry.
	Use Frappe's /api/method/upload_file first, then call this to link it.

	Args:
		inquiry_name: The inquiry document name
		file_url: The file URL returned from upload_file

	Returns:
		dict: {"success": True, "message": str}
	"""
	supplier_link = get_user_supplier_link()

	# Validate access to the inquiry
	inquiry = frappe.get_doc("Supplier Inquiry", inquiry_name)
	if inquiry.supplier_link != supplier_link:
		frappe.throw(_("You are not authorized to modify this inquiry"), frappe.PermissionError)

	# Find the file by URL and update its attachment
	file_doc = frappe.get_all(
		"File",
		filters={"file_url": file_url},
		fields=["name"],
		limit=1
	)

	if not file_doc:
		frappe.throw(_("File not found"))

	# Update file attachment
	frappe.db.set_value("File", file_doc[0].name, {
		"attached_to_doctype": "Supplier Inquiry",
		"attached_to_name": inquiry_name
	})
	frappe.db.commit()

	return {
		"success": True,
		"message": _("File attached successfully")
	}
