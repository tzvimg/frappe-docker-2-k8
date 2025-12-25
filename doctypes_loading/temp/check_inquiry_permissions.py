#!/usr/bin/env python3
"""
Check Supplier Inquiry permissions and data
"""

import frappe

def check_inquiry_permissions():
    """Check inquiry data and permissions"""

    # Get all inquiries
    inquiries = frappe.get_all(
        "Supplier Inquiry",
        fields=["name", "supplier_link", "topic_category", "inquiry_status", "owner"],
        limit=10
    )

    print("\n=== Supplier Inquiries ===")
    for inq in inquiries:
        print(f"\nInquiry: {inq.name}")
        print(f"  Supplier Link: {inq.supplier_link}")
        print(f"  Topic: {inq.topic_category}")
        print(f"  Status: {inq.inquiry_status}")
        print(f"  Owner: {inq.owner}")

    # Check test users
    print("\n\n=== Test Users ===")
    test_users = ["supplier1@test.com", "supplier2@test.com"]
    for user_email in test_users:
        try:
            user = frappe.get_doc("User", user_email)
            print(f"\nUser: {user_email}")
            print(f"  Supplier Link: {user.get('supplier_link')}")
            print(f"  Roles: {[r.role for r in user.roles]}")
        except Exception as e:
            print(f"  Error: {e}")

    # Test permission check
    print("\n\n=== Testing Permissions ===")
    if inquiries:
        test_inquiry = frappe.get_doc("Supplier Inquiry", inquiries[0].name)

        for user_email in test_users:
            from siud.siud.doctype.supplier_inquiry.supplier_inquiry import has_website_permission

            has_perm = has_website_permission(test_inquiry, "read", user_email, verbose=False)
            user = frappe.get_doc("User", user_email)

            print(f"\nUser: {user_email}")
            print(f"  User Supplier Link: {user.get('supplier_link')}")
            print(f"  Inquiry: {test_inquiry.name}")
            print(f"  Inquiry Supplier Link: {test_inquiry.supplier_link}")
            print(f"  Has Permission: {has_perm}")

if __name__ == "__main__":
    check_inquiry_permissions()
