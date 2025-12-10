"""
Load comprehensive test data for all SIUD DocTypes
"""

import frappe
from frappe.utils import now_datetime, add_days, add_months


@frappe.whitelist()
def load_activity_domain_categories():
    """Load test data for Activity Domain Category"""

    frappe.msgprint("\n📦 Loading Activity Domain Categories...")

    categories = [
        {
            'category_name': 'בית אבות',
            'category_code': 'BA',
        },
        {
            'category_name': 'מרכזי יום',
            'category_code': 'MY',
        },
        {
            'category_name': 'סיעוד ביתי',
            'category_code': 'SB',
        },
        {
            'category_name': 'קהילה תומכת',
            'category_code': 'KT',
        },
        {
            'category_name': 'שיקום',
            'category_code': 'SH',
        },
    ]

    created = 0
    for cat in categories:
        if not frappe.db.exists('Activity Domain Category', cat['category_code']):
            doc = frappe.get_doc({
                'doctype': 'Activity Domain Category',
                **cat
            })
            doc.insert()
            created += 1
            frappe.msgprint(f"  ✓ Created: {cat['category_name']} ({cat['category_code']})")
        else:
            frappe.msgprint(f"  ⚠ Already exists: {cat['category_name']}")

    frappe.db.commit()
    frappe.msgprint(f"✅ Created {created} Activity Domain Categories")
    return created


@frappe.whitelist()
def load_supplier_roles():
    """Load test data for Supplier Role"""

    frappe.msgprint("\n👤 Loading Supplier Roles...")

    roles = [
        {
            'role_name': 'מנהל כללי',
            'role_title_he': 'מנהל כללי',
        },
        {
            'role_name': 'מנהל סיעודי',
            'role_title_he': 'מנהל סיעודי',
        },
        {
            'role_name': 'רכז טיפול',
            'role_title_he': 'רכז טיפול',
        },
        {
            'role_name': 'אחות מוסמכת',
            'role_title_he': 'אחות מוסמכת',
        },
        {
            'role_name': 'מנהל משאבי אנוש',
            'role_title_he': 'מנהל משאבי אנוש',
        },
    ]

    created = 0
    for role in roles:
        if not frappe.db.exists('Supplier Role', {'role_name': role['role_name']}):
            doc = frappe.get_doc({
                'doctype': 'Supplier Role',
                **role
            })
            doc.insert()
            created += 1
            frappe.msgprint(f"  ✓ Created: {role['role_name']}")
        else:
            frappe.msgprint(f"  ⚠ Already exists: {role['role_name']}")

    frappe.db.commit()
    frappe.msgprint(f"✅ Created {created} Supplier Roles")
    return created


@frappe.whitelist()
def load_contact_persons():
    """Load test data for Contact Person"""

    frappe.msgprint("\n📧 Loading Contact Persons...")

    # Get all suppliers
    suppliers = frappe.get_all('Supplier', fields=['name', 'supplier_name'])

    if not suppliers:
        frappe.msgprint("  ⚠ No suppliers found. Please create suppliers first.")
        return 0

    # Get roles for assignment
    roles = frappe.get_all('Supplier Role', fields=['name', 'role_name'])

    contact_persons = []

    # Create multiple contacts for each supplier
    for supplier in suppliers:
        contacts = [
            {
                'supplier_link': supplier.name,
                'contact_name': 'דוד כהן',
                'email': f'david.cohen@{supplier.name.lower().replace(" ", "")}.co.il',
                'mobile_phone': '+972-3-5551234',
            },
            {
                'supplier_link': supplier.name,
                'contact_name': 'שרה לוי',
                'email': f'sarah.levi@{supplier.name.lower().replace(" ", "")}.co.il',
                'mobile_phone': '+972-3-5551235',
            },
            {
                'supplier_link': supplier.name,
                'contact_name': 'משה ישראלי',
                'email': f'moshe.israeli@{supplier.name.lower().replace(" ", "")}.co.il',
                'mobile_phone': '+972-3-5551236',
            },
        ]
        contact_persons.extend(contacts)

    created = 0
    for contact in contact_persons:
        # Check if contact already exists by email
        if not frappe.db.exists('Contact Person', {'email': contact['email']}):
            doc = frappe.get_doc({
                'doctype': 'Contact Person',
                **contact
            })
            doc.insert()
            created += 1
            frappe.msgprint(f"  ✓ Created: {contact['contact_name']} ({contact['email']})")
        else:
            frappe.msgprint(f"  ⚠ Already exists: {contact['email']}")

    frappe.db.commit()
    frappe.msgprint(f"✅ Created {created} Contact Persons")
    return created


@frappe.whitelist()
def load_additional_suppliers():
    """Load more test suppliers"""

    frappe.msgprint("\n🏢 Loading Additional Suppliers...")

    suppliers = [
        {
            'supplier_id': 'SUP-002',
            'supplier_name': 'בית אבות הגליל',
            'email': 'info@galil-nursing.co.il',
            'phone': '+972-4-6667777',
        },
        {
            'supplier_id': 'SUP-003',
            'supplier_name': 'מרכז יום נגב',
            'email': 'contact@negev-daycare.co.il',
            'phone': '+972-8-9998888',
        },
        {
            'supplier_id': 'SUP-004',
            'supplier_name': 'סיעוד ביתי ירושלים',
            'email': 'office@jlm-homecare.co.il',
            'phone': '+972-2-5554444',
        },
        {
            'supplier_id': 'SUP-005',
            'supplier_name': 'קהילה תומכת הר חרמון',
            'email': 'admin@hermon-community.co.il',
            'phone': '+972-4-1112222',
        },
        {
            'supplier_id': 'SUP-006',
            'supplier_name': 'מרכז שיקום תל אביב',
            'email': 'info@tlv-rehab.co.il',
            'phone': '+972-3-7778888',
        },
    ]

    created = 0
    for supplier in suppliers:
        if not frappe.db.exists('Supplier', {'supplier_id': supplier['supplier_id']}):
            doc = frappe.get_doc({
                'doctype': 'Supplier',
                **supplier
            })
            doc.insert()
            created += 1
            frappe.msgprint(f"  ✓ Created: {supplier['supplier_name']} ({supplier['supplier_id']})")
        else:
            frappe.msgprint(f"  ⚠ Already exists: {supplier['supplier_id']}")

    frappe.db.commit()
    frappe.msgprint(f"✅ Created {created} Suppliers")
    return created


@frappe.whitelist()
def load_additional_inquiries():
    """Load more test supplier inquiries"""

    frappe.msgprint("\n📝 Loading Additional Supplier Inquiries...")

    # Get all suppliers
    suppliers = frappe.get_all('Supplier', fields=['name', 'supplier_name'])

    if not suppliers:
        frappe.msgprint("  ⚠ No suppliers found. Please create suppliers first.")
        return 0

    # Get topic categories
    topics = frappe.get_all('Inquiry Topic Category', fields=['name', 'category_name'])

    if not topics:
        frappe.msgprint("  ⚠ No topic categories found.")
        return 0

    inquiries = [
        {
            'supplier_link': suppliers[0].name if len(suppliers) > 0 else None,
            'topic_category': topics[0].name if len(topics) > 0 else None,
            'inquiry_description': '''
                <p><strong>שאלה לגבי רישוי מוסד חדש</strong></p>
                <p>שלום רב,</p>
                <p>אנו מעוניינים לפתוח מוסד חדש באזור הצפון.</p>
                <p>מה התהליך הנדרש לקבלת רישיון?</p>
                <p>בברכה</p>
            ''',
            'inquiry_context': 'ספק עצמו',
            'inquiry_status': 'פנייה חדשה התקבלה',
        },
        {
            'supplier_link': suppliers[1].name if len(suppliers) > 1 else suppliers[0].name,
            'topic_category': topics[1].name if len(topics) > 1 else topics[0].name,
            'inquiry_description': '''
                <p><strong>בירור לגבי תקנות חדשות</strong></p>
                <p>שלום,</p>
                <p>האם יש תקנות חדשות לגבי יחס מטפלים למטופלים?</p>
                <p>תודה</p>
            ''',
            'inquiry_context': 'ספק עצמו',
            'inquiry_status': 'פנייה חדשה התקבלה',
        },
        {
            'supplier_link': suppliers[2].name if len(suppliers) > 2 else suppliers[0].name,
            'topic_category': topics[2].name if len(topics) > 2 else topics[0].name,
            'inquiry_description': '''
                <p><strong>שאלה לגבי הכשרות נדרשות</strong></p>
                <p>היי,</p>
                <p>מה ההכשרות הנדרשות למטפלים חדשים?</p>
                <p>האם יש קורסים מומלצים?</p>
                <p>בברכה</p>
            ''',
            'inquiry_context': 'ספק עצמו',
            'inquiry_status': 'פנייה חדשה התקבלה',
        },
        {
            'supplier_link': suppliers[3].name if len(suppliers) > 3 else suppliers[0].name,
            'topic_category': topics[3].name if len(topics) > 3 else topics[0].name,
            'inquiry_description': '''
                <p><strong>בקשה לעדכון פרטי נותן שירות</strong></p>
                <p>שלום רב,</p>
                <p>אנו רוצים לעדכן את פרטי איש הקשר במערכת.</p>
                <p>מה התהליך?</p>
                <p>תודה רבה</p>
            ''',
            'inquiry_context': 'ספק עצמו',
            'inquiry_status': 'פנייה חדשה התקבלה',
        },
        {
            'supplier_link': suppliers[0].name if len(suppliers) > 0 else None,
            'topic_category': topics[0].name if len(topics) > 0 else None,
            'inquiry_description': '''
                <p><strong>פנייה דחופה - בעיית כוח אדם</strong></p>
                <p>שלום,</p>
                <p>יש לנו מחסור חמור במטפלים.</p>
                <p>האם יש אפשרות לסיוע?</p>
                <p>דחוף!</p>
            ''',
            'inquiry_context': 'ספק עצמו',
            'inquiry_status': 'פנייה חדשה התקבלה',
        },
    ]

    created = 0
    for inquiry in inquiries:
        if inquiry['supplier_link']:
            doc = frappe.get_doc({
                'doctype': 'Supplier Inquiry',
                **inquiry
            })
            doc.insert()
            created += 1
            frappe.msgprint(f"  ✓ Created inquiry for: {inquiry['supplier_link']}")

    frappe.db.commit()
    frappe.msgprint(f"✅ Created {created} Supplier Inquiries")
    return created


@frappe.whitelist()
def load_all_test_data():
    """Master function - load comprehensive test data for all DocTypes"""

    frappe.msgprint("=" * 80)
    frappe.msgprint("🚀 Loading Comprehensive Test Data for All SIUD DocTypes")
    frappe.msgprint("=" * 80)

    results = {
        'activity_domains': 0,
        'supplier_roles': 0,
        'suppliers': 0,
        'contact_persons': 0,
        'inquiries': 0,
    }

    try:
        # Step 1: Load Activity Domain Categories
        frappe.msgprint("\n" + "=" * 80)
        frappe.msgprint("STEP 1: Activity Domain Categories")
        frappe.msgprint("=" * 80)
        results['activity_domains'] = load_activity_domain_categories()

        # Step 2: Load Supplier Roles
        frappe.msgprint("\n" + "=" * 80)
        frappe.msgprint("STEP 2: Supplier Roles")
        frappe.msgprint("=" * 80)
        results['supplier_roles'] = load_supplier_roles()

        # Step 3: Load Additional Suppliers
        frappe.msgprint("\n" + "=" * 80)
        frappe.msgprint("STEP 3: Additional Suppliers")
        frappe.msgprint("=" * 80)
        results['suppliers'] = load_additional_suppliers()

        # Step 4: Load Contact Persons
        frappe.msgprint("\n" + "=" * 80)
        frappe.msgprint("STEP 4: Contact Persons")
        frappe.msgprint("=" * 80)
        results['contact_persons'] = load_contact_persons()

        # Step 5: Load Additional Inquiries
        frappe.msgprint("\n" + "=" * 80)
        frappe.msgprint("STEP 5: Additional Supplier Inquiries")
        frappe.msgprint("=" * 80)
        results['inquiries'] = load_additional_inquiries()

        # Summary
        frappe.msgprint("\n" + "=" * 80)
        frappe.msgprint("✅ TEST DATA LOADING COMPLETE!")
        frappe.msgprint("=" * 80)
        frappe.msgprint("\n📊 Summary of Created Records:")
        frappe.msgprint(f"   • Activity Domain Categories: {results['activity_domains']}")
        frappe.msgprint(f"   • Supplier Roles: {results['supplier_roles']}")
        frappe.msgprint(f"   • Additional Suppliers: {results['suppliers']}")
        frappe.msgprint(f"   • Contact Persons: {results['contact_persons']}")
        frappe.msgprint(f"   • Additional Inquiries: {results['inquiries']}")

        # Get total counts
        frappe.msgprint("\n📈 Total Records in System:")
        frappe.msgprint(f"   • Activity Domain Categories: {frappe.db.count('Activity Domain Category')}")
        frappe.msgprint(f"   • Supplier Roles: {frappe.db.count('Supplier Role')}")
        frappe.msgprint(f"   • Suppliers: {frappe.db.count('Supplier')}")
        frappe.msgprint(f"   • Contact Persons: {frappe.db.count('Contact Person')}")
        frappe.msgprint(f"   • Inquiry Topic Categories: {frappe.db.count('Inquiry Topic Category')}")
        frappe.msgprint(f"   • Supplier Inquiries: {frappe.db.count('Supplier Inquiry')}")

        frappe.msgprint("\n🌐 Access the system at: http://localhost:8000")
        frappe.msgprint("\n")

    except Exception as e:
        frappe.msgprint(f"\n❌ Error loading test data: {str(e)}")
        import traceback
        traceback.print_exc()
        frappe.db.rollback()
        return {"success": False, "error": str(e)}

    return {"success": True, "results": results}


@frappe.whitelist()
def delete_all_test_data():
    """Delete all test data from all DocTypes"""

    frappe.msgprint("=" * 80)
    frappe.msgprint("🗑️  Deleting All Test Data")
    frappe.msgprint("=" * 80)

    deleted = {}

    # Delete in reverse dependency order

    # 1. Delete Contact Persons
    frappe.msgprint("\n1️⃣ Deleting Contact Persons...")
    contacts = frappe.get_all('Contact Person')
    for contact in contacts:
        frappe.delete_doc('Contact Person', contact.name, force=1)
    deleted['contact_persons'] = len(contacts)
    frappe.msgprint(f"   ✓ Deleted {len(contacts)} Contact Persons")

    # 2. Delete Supplier Inquiries
    frappe.msgprint("\n2️⃣ Deleting Supplier Inquiries...")
    inquiries = frappe.get_all('Supplier Inquiry')
    for inquiry in inquiries:
        frappe.delete_doc('Supplier Inquiry', inquiry.name, force=1)
    deleted['inquiries'] = len(inquiries)
    frappe.msgprint(f"   ✓ Deleted {len(inquiries)} Supplier Inquiries")

    # 3. Delete Suppliers
    frappe.msgprint("\n3️⃣ Deleting Suppliers...")
    suppliers = frappe.get_all('Supplier')
    for supplier in suppliers:
        frappe.delete_doc('Supplier', supplier.name, force=1)
    deleted['suppliers'] = len(suppliers)
    frappe.msgprint(f"   ✓ Deleted {len(suppliers)} Suppliers")

    # 4. Delete Supplier Roles
    frappe.msgprint("\n4️⃣ Deleting Supplier Roles...")
    roles = frappe.get_all('Supplier Role')
    for role in roles:
        frappe.delete_doc('Supplier Role', role.name, force=1)
    deleted['roles'] = len(roles)
    frappe.msgprint(f"   ✓ Deleted {len(roles)} Supplier Roles")

    # 5. Delete Activity Domain Categories
    frappe.msgprint("\n5️⃣ Deleting Activity Domain Categories...")
    categories = frappe.get_all('Activity Domain Category')
    for cat in categories:
        frappe.delete_doc('Activity Domain Category', cat.name, force=1)
    deleted['categories'] = len(categories)
    frappe.msgprint(f"   ✓ Deleted {len(categories)} Activity Domain Categories")

    frappe.db.commit()

    frappe.msgprint("\n" + "=" * 80)
    frappe.msgprint("✅ Test Data Deletion Complete!")
    frappe.msgprint("=" * 80)
    frappe.msgprint(f"\n📊 Deleted {sum(deleted.values())} records total")
    frappe.msgprint("\n")

    return {"success": True, "deleted": deleted}
