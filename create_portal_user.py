#!/usr/bin/env python3
"""Create a portal user for testing the supplier dashboard"""

import subprocess
import sys

# Script to run inside the container
script = """
import frappe

frappe.connect()
frappe.set_user('Administrator')

# Check if test portal user exists
email = 'supplier@test.com'
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

    # Set password
    user.new_password = 'test123'
    user.save(ignore_permissions=True)

    print(f'✓ Created user: {email}')
else:
    user = frappe.get_doc('User', email)
    user.enabled = 1
    user.new_password = 'test123'
    user.save(ignore_permissions=True)
    print(f'✓ User already exists: {email}')

# Link to first supplier
suppliers = frappe.get_all('Supplier', limit=1)
if suppliers:
    user.supplier_link = suppliers[0]['name']
    user.save(ignore_permissions=True)
    print(f'✓ Linked to supplier: {suppliers[0]["name"]}')

frappe.db.commit()
print(f'\\n✓ Portal user ready: {email} / test123')
"""

# Run the script
cmd = f'docker exec frappe_docker_devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site development.localhost console" <<< "{script}"'
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

print(result.stdout)
if result.returncode != 0:
    print("Error:", result.stderr, file=sys.stderr)
    sys.exit(1)
