import frappe

def create_portal_user():
    """Create a portal user for testing the supplier dashboard"""

    email = 'supplier@test.com'

    # Check if test portal user exists
    if not frappe.db.exists('User', email):
        # Create portal user
        user = frappe.get_doc({
            'doctype': 'User',
            'email': email,
            'first_name': 'Test',
            'last_name': 'Supplier',
            'user_type': 'Website User',
            'send_welcome_email': 0,
            'enabled': 1
        })
        user.insert(ignore_permissions=True)
        print(f'✓ Created user: {email}')
    else:
        user = frappe.get_doc('User', email)
        user.enabled = 1
        print(f'✓ User already exists: {email}')

    # Set password
    from frappe.utils.password import update_password
    update_password(user=email, pwd='TestSupplier@123', logout_all_sessions=False)

    # Link to first supplier
    suppliers = frappe.get_all('Supplier', limit=1)
    if suppliers:
        user.supplier_link = suppliers[0]['name']
        user.save(ignore_permissions=True)
        print(f'✓ Linked to supplier: {suppliers[0]["name"]}')

    frappe.db.commit()
    print(f'\n✓ Portal user ready!')
    print(f'  Email: {email}')
    print(f'  Password: test123')
    print(f'  Login at: http://localhost:8000/login')

    return {"status": "success"}
