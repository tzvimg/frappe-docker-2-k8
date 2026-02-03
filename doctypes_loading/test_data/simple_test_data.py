"""Simple test data for Siud app"""
import frappe

@frappe.whitelist()
def load_all():
    """Load all test data"""
    results = []
    
    # 1. Create roles
    for role_name in ['Service Provider User', 'Sorting Clerk', 'Handling Clerk']:
        if not frappe.db.exists('Role', role_name):
            frappe.get_doc({'doctype': 'Role', 'role_name': role_name, 'desk_access': 1}).insert()
            results.append(f"✓ Role: {role_name}")
    
    # 2. Create Activity Domain Categories
    domains = [{'category_name': 'טיפול בבית', 'category_code': 'HOME'}, {'category_name': 'מרכז יום', 'category_code': 'DAY'}, {'category_name': 'קהילה תומכת', 'category_code': 'COMM'}]
    for d in domains:
        if not frappe.db.exists('Activity Domain Category', {'category_code': d['category_code']}):
            frappe.get_doc({'doctype': 'Activity Domain Category', **d}).insert()
            results.append(f"✓ Domain: {d['category_name']}")
    
    # 3. Create Inquiry Topic Categories
    for topic in [{'category_name': 'נושאים מקצועיים', 'category_code': 'PROF'}, {'category_name': 'תלונות', 'category_code': 'COMP'}]:
        if not frappe.db.exists('Inquiry Topic Category', {'category_code': topic['category_code']}):
            frappe.get_doc({'doctype': 'Inquiry Topic Category', **topic}).insert()
            results.append(f"✓ Topic: {topic['category_name']}")
    
    # 4. Create Supplier Roles
    for sr in ['מנהל', 'רכז', 'מטפל']:
        if not frappe.db.exists('Supplier Role', {'role_name': sr}):
            frappe.get_doc({'doctype': 'Supplier Role', 'role_name': sr}).insert()
            results.append(f"✓ Supplier Role: {sr}")
    
    # 5. Create test Supplier
    if not frappe.db.exists('Supplier', {'supplier_name': 'מרכז סיעודי השרון'}):
        supplier = frappe.get_doc({'doctype': 'Supplier', 'supplier_name': 'מרכז סיעודי השרון', 'hp_number': '123456789'})
        supplier.insert()
        results.append(f"✓ Supplier: {supplier.name}")
    
    frappe.db.commit()
    for r in results:
        print(r)
    print(f"\n✓ Loaded {len(results)} test records")
    return {"success": True, "count": len(results)}
