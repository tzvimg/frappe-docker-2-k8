"""
Create test portal users and suppliers for Supplier Portal testing

This script creates:
1. Two Supplier records (SUP-001, SUP-002)
2. Two portal users linked to those suppliers
3. Sample Supplier Inquiry records for each supplier

Usage:
    bench --site development.localhost execute siud.doctypes_loading.test_data.create_portal_users.create_test_portal_users

Or using the helper script:
    ./run_doctype_script.sh test_data.create_portal_users.create_test_portal_users
"""

import frappe
from frappe import _


@frappe.whitelist()
def create_test_portal_users():
    """Create test suppliers and portal users with sample data"""

    frappe.flags.ignore_permissions = True

    try:
        # Create two test suppliers
        suppliers = create_test_suppliers()

        # Create portal users linked to suppliers
        users = create_users_for_suppliers(suppliers)

        # Create sample inquiries for each supplier
        create_sample_inquiries(suppliers)

        frappe.db.commit()

        # Print summary
        print("\n" + "="*60)
        print("✓ Test Portal Users Created Successfully")
        print("="*60)
        print("\nSuppliers Created:")
        for supplier in suppliers:
            print(f"  - {supplier['name']}: {supplier['supplier_name']}")

        print("\nPortal Users Created:")
        for user in users:
            print(f"  - Email: {user['email']}")
            print(f"    Password: {user['password']}")
            print(f"    Linked to: {user['supplier_link']}")
            print()

        print("\nLogin URLs:")
        print("  - Portal: http://localhost:8000")
        print("\nNext Steps:")
        print("  1. Log in with one of the test users above")
        print("  2. Verify you see the supplier dashboard (not desk)")
        print("  3. Test creating new inquiries")
        print("  4. Test viewing inquiry list (only your inquiries)")
        print("  5. Test editing supplier profile")
        print("  6. Log in with second user and verify data isolation")
        print("="*60)

        return {
            "success": True,
            "suppliers": [s["name"] for s in suppliers],
            "users": [u["email"] for u in users]
        }

    except Exception as e:
        frappe.db.rollback()
        print(f"✗ Error creating test users: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Create Portal Users Error")
        raise


def create_test_suppliers():
    """Create two test supplier records"""

    suppliers_data = [
        {
            "supplier_id": "SUP-TEST-001",
            "supplier_name": "ספק בדיקה ראשון בע\"מ",
            "email": "supplier1@test.com",
            "address": "רחוב הבדיקה 1, תל אביב"
        },
        {
            "supplier_id": "SUP-TEST-002",
            "supplier_name": "ספק בדיקה שני בע\"מ",
            "email": "supplier2@test.com",
            "address": "שדרות הבדיקה 2, חיפה"
        }
    ]

    created_suppliers = []

    for data in suppliers_data:
        # Check if supplier already exists
        if frappe.db.exists("Supplier", {"supplier_id": data["supplier_id"]}):
            print(f"⚠ Supplier {data['supplier_id']} already exists, skipping...")
            supplier = frappe.get_doc("Supplier", {"supplier_id": data["supplier_id"]})
            created_suppliers.append({
                "name": supplier.name,
                "supplier_id": supplier.supplier_id,
                "supplier_name": supplier.supplier_name
            })
            continue

        supplier = frappe.get_doc({
            "doctype": "Supplier",
            "supplier_id": data["supplier_id"],
            "supplier_name": data["supplier_name"],
            "email": data["email"],
            "address": data["address"]
        })

        supplier.insert()
        print(f"✓ Created supplier: {supplier.name} ({data['supplier_name']})")

        created_suppliers.append({
            "name": supplier.name,
            "supplier_id": supplier.supplier_id,
            "supplier_name": supplier.supplier_name
        })

    return created_suppliers


def create_users_for_suppliers(suppliers):
    """Create portal users linked to suppliers"""

    users_data = [
        {
            "email": "supplier1@test.com",
            "first_name": "משתמש",
            "last_name": "ספק 1",
            "supplier_index": 0,
            "password": "Test@1234"
        },
        {
            "email": "supplier2@test.com",
            "first_name": "משתמש",
            "last_name": "ספק 2",
            "supplier_index": 1,
            "password": "Test@1234"
        }
    ]

    created_users = []

    for data in users_data:
        supplier = suppliers[data["supplier_index"]]

        # Check if user already exists
        if frappe.db.exists("User", data["email"]):
            print(f"⚠ User {data['email']} already exists, updating...")
            user = frappe.get_doc("User", data["email"])

            # Update supplier link if not set
            if not user.supplier_link:
                user.supplier_link = supplier["name"]
                user.save()
                print(f"  ✓ Updated supplier_link for {data['email']}")

            # Ensure role is assigned
            if not any(r.role == "Supplier Portal User" for r in user.roles):
                user.append("roles", {"role": "Supplier Portal User"})
                user.save()
                print(f"  ✓ Added Supplier Portal User role to {data['email']}")

            created_users.append({
                "email": user.email,
                "supplier_link": user.supplier_link,
                "password": "(existing password - not changed)"
            })
            continue

        # Create new user
        user = frappe.get_doc({
            "doctype": "User",
            "email": data["email"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "enabled": 1,
            "send_welcome_email": 0,
            "supplier_link": supplier["name"]
        })

        user.insert()

        # Set password
        user.new_password = data["password"]
        user.save()

        # Add Supplier Portal User role
        user.append("roles", {"role": "Supplier Portal User"})
        user.save()

        print(f"✓ Created user: {data['email']} (linked to {supplier['supplier_id']})")

        created_users.append({
            "email": user.email,
            "supplier_link": user.supplier_link,
            "password": data["password"]
        })

    return created_users


def create_sample_inquiries(suppliers):
    """Create sample inquiry records for each supplier"""

    # Get available topic categories
    available_categories = frappe.get_all("Inquiry Topic Category", pluck="name")

    if not available_categories:
        print("⚠ No Inquiry Topic Categories found, skipping sample inquiry creation")
        return

    # Use the first available category for all inquiries
    default_category = available_categories[0]

    inquiries_data = [
        {
            "supplier_index": 0,
            "topic_category": default_category,
            "inquiry_description": "שאלה לגבי תהליך התשלום - אני רוצה לדעת מתי מתבצעים התשלומים החודשיים",
            "inquiry_context": "ספק עצמו"
        },
        {
            "supplier_index": 0,
            "topic_category": default_category,
            "inquiry_description": "בעיה בכניסה למערכת - לא מצליח להתחבר למערכת מהטלפון הנייד",
            "inquiry_context": "ספק עצמו"
        },
        {
            "supplier_index": 1,
            "topic_category": default_category,
            "inquiry_description": "עדכון כתובת משרד - עברנו למשרד חדש ואני צריך לעדכן את הכתובת",
            "inquiry_context": "ספק עצמו"
        },
        {
            "supplier_index": 1,
            "topic_category": default_category,
            "inquiry_description": "שאלה לגבי מטופל מספר 123456789 - אני רוצה לדעת מה הסטטוס של הבקשה",
            "inquiry_context": "מבוטח",
            "insured_id_number": "123456789",
            "insured_full_name": "ישראל ישראלי"
        }
    ]

    for data in inquiries_data:
        supplier = suppliers[data["supplier_index"]]

        inquiry = frappe.get_doc({
            "doctype": "Supplier Inquiry",
            "supplier_link": supplier["name"],
            "topic_category": data["topic_category"],
            "inquiry_description": data["inquiry_description"],
            "inquiry_context": data["inquiry_context"],
            "inquiry_status": "פנייה חדשה התקבלה",
            "insured_id_number": data.get("insured_id_number", ""),
            "insured_full_name": data.get("insured_full_name", "")
        })

        inquiry.insert()
        print(f"✓ Created sample inquiry: {inquiry.name} for {supplier['supplier_id']}")


@frappe.whitelist()
def delete_test_portal_users():
    """Delete test users and suppliers (cleanup utility)"""

    frappe.flags.ignore_permissions = True

    try:
        # Delete test inquiries
        inquiries = frappe.get_all(
            "Supplier Inquiry",
            filters={"supplier_link": ["like", "SUP-TEST-%"]},
            pluck="name"
        )
        for inquiry in inquiries:
            frappe.delete_doc("Supplier Inquiry", inquiry, force=1)
            print(f"✓ Deleted inquiry: {inquiry}")

        # Delete test users
        test_emails = ["supplier1@test.com", "supplier2@test.com"]
        for email in test_emails:
            if frappe.db.exists("User", email):
                frappe.delete_doc("User", email, force=1)
                print(f"✓ Deleted user: {email}")

        # Delete test suppliers
        suppliers = frappe.get_all(
            "Supplier",
            filters={"supplier_id": ["like", "SUP-TEST-%"]},
            pluck="name"
        )
        for supplier in suppliers:
            frappe.delete_doc("Supplier", supplier, force=1)
            print(f"✓ Deleted supplier: {supplier}")

        frappe.db.commit()
        print("\n✓ All test data deleted successfully")

        return {"success": True}

    except Exception as e:
        frappe.db.rollback()
        print(f"✗ Error deleting test data: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Delete Portal Users Error")
        raise


if __name__ == "__main__":
    create_test_portal_users()
