import frappe

def test_dashboard():
    """Test the supplier dashboard get_context function"""
    print("=== Testing Supplier Dashboard ===")

    # Set user to Administrator
    frappe.set_user('Administrator')
    print(f"Current user: {frappe.session.user}")

    # Check if Administrator has supplier_link
    user = frappe.get_doc('User', 'Administrator')
    supplier_link = user.get('supplier_link')
    print(f"Administrator supplier_link: {supplier_link}")

    # Import the dashboard module
    from siud.www.supplier_dashboard import get_context

    context = {}
    try:
        result = get_context(context)
        print("\n✓ SUCCESS - Context generated")
        print(f"  Supplier Name: {context.get('supplier_name')}")
        print(f"  Supplier ID: {context.get('supplier_id')}")
        print(f"  Total Inquiries: {context.get('total_inquiries')}")
        print(f"  Open Inquiries: {context.get('open_inquiries')}")
        print(f"  Closed Inquiries: {context.get('closed_inquiries')}")
        print(f"  Recent Inquiries: {len(context.get('recent_inquiries', []))}")
        return {"status": "success"}
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}
