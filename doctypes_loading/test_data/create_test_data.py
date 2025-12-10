"""
Create test users, supplier, and inquiry to demonstrate the workflow
"""

import frappe
from frappe.utils import now_datetime


@frappe.whitelist()
def create_test_users():
    """Create test users with appropriate roles"""

    users = [
        {
            'email': 'supplier.user@example.com',
            'first_name': 'דוד',
            'last_name': 'כהן',
            'roles': ['Service Provider User'],
            'send_welcome_email': 0,
        },
        {
            'email': 'sorting.clerk@example.com',
            'first_name': 'שרה',
            'last_name': 'לוי',
            'roles': ['Sorting Clerk', 'Desk User'],
            'send_welcome_email': 0,
        },
        {
            'email': 'handling.clerk@example.com',
            'first_name': 'משה',
            'last_name': 'ישראלי',
            'roles': ['Handling Clerk', 'Desk User'],
            'send_welcome_email': 0,
        },
    ]

    created_users = []

    for user_data in users:
        email = user_data['email']

        if frappe.db.exists("User", email):
            frappe.msgprint(f"⚠ User already exists: {email}")
            # Update roles for existing user
            user = frappe.get_doc("User", email)
            for role in user_data['roles']:
                if not any(r.role == role for r in user.roles):
                    user.append('roles', {'role': role})
            user.save()
            frappe.msgprint(f"✓ Updated roles for user: {email}")
        else:
            # Create new user
            user = frappe.get_doc({
                'doctype': 'User',
                'email': email,
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'send_welcome_email': user_data['send_welcome_email'],
                'roles': [{'role': role} for role in user_data['roles']]
            })
            user.insert(ignore_permissions=True)
            created_users.append(email)
            frappe.msgprint(f"✓ Created user: {email} ({user_data['first_name']} {user_data['last_name']})")

            # Set a default password for testing
            user.new_password = 'Test@1234'
            user.save()
            frappe.msgprint(f"  Password set to: Test@1234")

    frappe.db.commit()

    return {"success": True, "created": created_users}


@frappe.whitelist()
def create_test_supplier():
    """Create a test supplier"""

    supplier_id = 'SUP-001'
    supplier_name = 'מרכז סיעודי השרון'

    # Check if supplier already exists
    existing = frappe.db.exists('Supplier', supplier_id)

    if existing:
        frappe.msgprint(f"⚠ Supplier already exists: {existing}")
        return {"success": False, "supplier": existing, "message": "Already exists"}

    supplier_data = {
        'supplier_id': supplier_id,
        'supplier_name': supplier_name,
        'email': 'supplier.user@example.com',
        'phone': '+972-3-1234567',
    }

    supplier = frappe.get_doc({
        'doctype': 'Supplier',
        **supplier_data
    })

    supplier.insert()
    frappe.db.commit()

    frappe.msgprint(f"✓ Created supplier: {supplier.name} - {supplier.supplier_name}")

    return {"success": True, "supplier": supplier.name}


@frappe.whitelist()
def create_test_inquiry():
    """Create a test supplier inquiry"""

    # Get the first supplier
    supplier = frappe.db.get_value('Supplier', {}, 'name')

    if not supplier:
        frappe.throw("No supplier found. Please create a supplier first.")

    # Use existing topic category
    topic_category = 'PROF'  # נושאים מקצועיים

    inquiry_data = {
        'supplier_link': supplier,
        'topic_category': topic_category,
        'inquiry_description': '''
            <p><strong>שאלה לגבי הכשרה חדשה לעובדים</strong></p>
            <p>שלום רב,</p>
            <p>אנו מעוניינים לברר האם יש דרישה חדשה להכשרת עובדים בנושא טיפול בחולי אלצהיימר.</p>
            <p>נודה לתגובה בהקדם.</p>
            <p>בברכה,<br>דוד כהן</p>
        ''',
        'inquiry_context': 'ספק עצמו',
        'inquiry_status': 'פנייה חדשה התקבלה',
    }

    inquiry = frappe.get_doc({
        'doctype': 'Supplier Inquiry',
        **inquiry_data
    })

    inquiry.insert()
    frappe.db.commit()

    frappe.msgprint(f"✓ Created inquiry: {inquiry.name}")
    frappe.msgprint(f"  Supplier: {supplier}")
    frappe.msgprint(f"  Status: {inquiry.inquiry_status}")

    return {"success": True, "inquiry": inquiry.name}


@frappe.whitelist()
def test_workflow_transitions():
    """Test workflow transitions with the created inquiry"""

    # Get the first inquiry
    inquiry_name = frappe.db.get_value('Supplier Inquiry', {}, 'name')

    if not inquiry_name:
        frappe.throw("No inquiry found. Please create an inquiry first.")

    inquiry = frappe.get_doc('Supplier Inquiry', inquiry_name)

    frappe.msgprint("=" * 60)
    frappe.msgprint(f"Testing Workflow Transitions for: {inquiry_name}")
    frappe.msgprint("=" * 60)

    # Show current state
    frappe.msgprint(f"\n📍 Current State: {inquiry.inquiry_status}")

    # Get available transitions
    from frappe.model.workflow import get_transitions

    try:
        transitions = get_transitions(inquiry)

        if transitions:
            frappe.msgprint(f"\n✅ Available Transitions:")
            for i, transition in enumerate(transitions, 1):
                frappe.msgprint(f"  {i}. {transition.get('action')} → {transition.get('next_state')}")
                frappe.msgprint(f"     Allowed: {transition.get('allowed')}")
        else:
            frappe.msgprint("\n⚠ No transitions available for current state")
    except Exception as e:
        frappe.msgprint(f"\n❌ Error getting transitions: {str(e)}")

    frappe.msgprint("\n" + "=" * 60)

    return {
        "success": True,
        "inquiry": inquiry_name,
        "current_state": inquiry.inquiry_status,
        "transitions": transitions if 'transitions' in locals() else []
    }


@frappe.whitelist()
def apply_transition(inquiry_name, action):
    """Apply a workflow transition to an inquiry"""

    inquiry = frappe.get_doc('Supplier Inquiry', inquiry_name)

    frappe.msgprint(f"Applying transition: {action}")
    frappe.msgprint(f"Current state: {inquiry.inquiry_status}")

    from frappe.model.workflow import apply_workflow

    try:
        # Apply the workflow action
        inquiry = apply_workflow(inquiry, action)
        frappe.db.commit()

        frappe.msgprint(f"✓ Transition successful!")
        frappe.msgprint(f"New state: {inquiry.inquiry_status}")

        return {"success": True, "new_state": inquiry.inquiry_status}
    except Exception as e:
        frappe.db.rollback()
        frappe.msgprint(f"✗ Transition failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def demonstrate_workflow():
    """Demonstrate the complete workflow with transitions"""

    # Get inquiry
    inquiry_name = frappe.db.get_value('Supplier Inquiry', {}, 'name')

    if not inquiry_name:
        frappe.throw("No inquiry found. Please create an inquiry first.")

    inquiry = frappe.get_doc('Supplier Inquiry', inquiry_name)

    frappe.msgprint("\n" + "=" * 60)
    frappe.msgprint("🔄 WORKFLOW DEMONSTRATION")
    frappe.msgprint("=" * 60)

    steps = [
        {
            'state': 'פנייה חדשה התקבלה',
            'action': 'העבר למיון',
            'user': 'sorting.clerk@example.com',
            'description': 'Sorting Clerk moves inquiry to sorting',
        },
        {
            'state': 'מיון וניתוב',
            'action': 'הקצה לטיפול',
            'user': 'sorting.clerk@example.com',
            'description': 'Sorting Clerk assigns to handling clerk',
            'set_field': {'assigned_employee_id': 'handling.clerk@example.com'}
        },
        {
            'state': 'בטיפול',
            'action': 'דרוש השלמות',
            'user': 'handling.clerk@example.com',
            'description': 'Handling Clerk requests additional information',
            'set_field': {'internal_notes': 'נדרש לברר פרטים נוספים עם המשרד'}
        },
        {
            'state': 'דורש השלמות / המתנה',
            'action': 'חזור לטיפול',
            'user': 'handling.clerk@example.com',
            'description': 'Handling Clerk returns to processing after receiving info',
        },
        {
            'state': 'בטיפול',
            'action': 'סגור עם מענה',
            'user': 'handling.clerk@example.com',
            'description': 'Handling Clerk closes with response',
            'set_field': {
                'response_text': '''<p>שלום רב,</p>
<p>בתגובה לפנייתך - אין דרישה חדשה להכשרה בנושא זה.</p>
<p>ההכשרות הנדרשות נשארות כפי שהיו.</p>
<p>בברכה,<br>משה ישראלי<br>פקיד מטפל</p>'''
            }
        },
    ]

    for i, step in enumerate(steps, 1):
        frappe.msgprint(f"\n📍 Step {i}: {step['description']}")
        frappe.msgprint(f"   Current State: {inquiry.inquiry_status}")
        frappe.msgprint(f"   Expected State: {step['state']}")

        # Verify we're in the expected state
        if inquiry.inquiry_status != step['state']:
            frappe.msgprint(f"   ⚠ WARNING: Not in expected state!")
            frappe.msgprint(f"   Skipping to next step...")
            continue

        # Set any required fields
        if 'set_field' in step:
            for field, value in step['set_field'].items():
                setattr(inquiry, field, value)
                frappe.msgprint(f"   ✓ Set {field}")
            inquiry.save()

        # Apply the action
        frappe.msgprint(f"   Action: {step['action']}")
        frappe.msgprint(f"   User: {step['user']}")

        try:
            from frappe.model.workflow import apply_workflow
            inquiry = apply_workflow(inquiry, step['action'])
            frappe.db.commit()
            frappe.msgprint(f"   ✅ Success! New state: {inquiry.inquiry_status}")
        except Exception as e:
            frappe.msgprint(f"   ❌ Failed: {str(e)}")
            import traceback
            traceback.print_exc()
            break

        # Reload the inquiry
        inquiry.reload()

    frappe.msgprint("\n" + "=" * 60)
    frappe.msgprint(f"🏁 Final State: {inquiry.inquiry_status}")
    frappe.msgprint("=" * 60 + "\n")

    return {"success": True, "final_state": inquiry.inquiry_status}


@frappe.whitelist()
def create_all_test_data():
    """Master function - create all test data and demonstrate workflow"""

    frappe.msgprint("=" * 60)
    frappe.msgprint("Creating Test Data for Supplier Inquiry Workflow")
    frappe.msgprint("=" * 60)

    results = {}

    # Step 1: Create test users
    frappe.msgprint("\n1️⃣ Creating test users...")
    results['users'] = create_test_users()

    # Step 2: Create test supplier
    frappe.msgprint("\n2️⃣ Creating test supplier...")
    results['supplier'] = create_test_supplier()

    # Step 3: Create test inquiry
    frappe.msgprint("\n3️⃣ Creating test inquiry...")
    results['inquiry'] = create_test_inquiry()

    # Step 4: Test workflow
    frappe.msgprint("\n4️⃣ Testing workflow transitions...")
    results['workflow_test'] = test_workflow_transitions()

    # Step 5: Demonstrate workflow
    frappe.msgprint("\n5️⃣ Demonstrating complete workflow...")
    results['workflow_demo'] = demonstrate_workflow()

    frappe.msgprint("\n" + "=" * 60)
    frappe.msgprint("✅ Test Data Creation Complete!")
    frappe.msgprint("=" * 60)
    frappe.msgprint("\n📋 Summary:")
    frappe.msgprint(f"   • Created 3 test users")
    frappe.msgprint(f"   • Created test supplier: {results['supplier'].get('supplier', 'N/A')}")
    frappe.msgprint(f"   • Created test inquiry: {results['inquiry'].get('inquiry', 'N/A')}")
    frappe.msgprint(f"   • Final workflow state: {results['workflow_demo'].get('final_state', 'N/A')}")
    frappe.msgprint("\n📧 Test User Credentials:")
    frappe.msgprint("   • supplier.user@example.com / Test@1234 (Service Provider)")
    frappe.msgprint("   • sorting.clerk@example.com / Test@1234 (Sorting Clerk)")
    frappe.msgprint("   • handling.clerk@example.com / Test@1234 (Handling Clerk)")
    frappe.msgprint("\n🌐 Access at: http://localhost:8000")
    frappe.msgprint("\n")

    return results


@frappe.whitelist()
def delete_test_data():
    """Delete all test data"""

    frappe.msgprint("🗑️ Deleting test data...\n")

    # Delete inquiries
    inquiries = frappe.get_all('Supplier Inquiry')
    for inquiry in inquiries:
        frappe.delete_doc('Supplier Inquiry', inquiry.name, force=1)
        frappe.msgprint(f"✓ Deleted inquiry: {inquiry.name}")

    # Delete suppliers
    suppliers = frappe.get_all('Supplier')
    for supplier in suppliers:
        frappe.delete_doc('Supplier', supplier.name, force=1)
        frappe.msgprint(f"✓ Deleted supplier: {supplier.name}")

    # Delete test users (but not Administrator)
    test_users = [
        'supplier.user@example.com',
        'sorting.clerk@example.com',
        'handling.clerk@example.com',
    ]

    for email in test_users:
        if frappe.db.exists('User', email):
            frappe.delete_doc('User', email, force=1)
            frappe.msgprint(f"✓ Deleted user: {email}")

    frappe.db.commit()
    frappe.msgprint("\n✅ Test data deletion complete!")

    return {"success": True}
