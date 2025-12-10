import frappe

@frappe.whitelist()
def check_role_doctype():
    """Check if Role DocType exists and what module it belongs to"""

    if not frappe.db.exists("DocType", "Role"):
        return {"exists": False, "message": "Role DocType does not exist!"}

    role_meta = frappe.get_meta("Role")

    # Get field names
    field_names = [f.fieldname for f in role_meta.fields]

    info = {
        "exists": True,
        "module": role_meta.module,
        "total_fields": len(field_names),
        "has_disabled": "disabled" in field_names,
        "has_desk_access": "desk_access" in field_names,
        "has_role_name": "role_name" in field_names,
        "has_role_title_he": "role_title_he" in field_names,
        "field_names": field_names
    }

    # Determine if it's core or custom
    if info["module"] == "Core" or (info["has_disabled"] and info["has_desk_access"]):
        info["type"] = "FRAPPE CORE - DO NOT DELETE!"
    elif info["module"] == "Siud" and info["has_role_title_he"]:
        info["type"] = "Custom Supplier Role (CONFLICT!)"
    else:
        info["type"] = "Unknown"

    frappe.msgprint(f"""
    <b>Role DocType Status:</b><br>
    Type: {info['type']}<br>
    Module: {info['module']}<br>
    Total Fields: {info['total_fields']}<br>
    Has 'disabled' (core): {info['has_disabled']}<br>
    Has 'desk_access' (core): {info['has_desk_access']}<br>
    Has 'role_title_he' (custom): {info['has_role_title_he']}<br>
    """)

    return info
