"""
Create Supplier Inquiry WebForm for Portal Users

This script creates a WebForm that allows portal users to:
- Submit new supplier inquiries
- View their submitted inquiries
- Track inquiry status

The webform auto-populates supplier_link from the logged-in user's profile.
"""

import frappe
from frappe import _


def create_supplier_inquiry_webform():
    """Create the Supplier Inquiry WebForm for portal access"""

    print("\n" + "="*80)
    print("Creating Supplier Inquiry WebForm")
    print("="*80 + "\n")

    # Check if WebForm already exists
    if frappe.db.exists("Web Form", "supplier-inquiry-form"):
        print("⚠️  WebForm 'supplier-inquiry-form' already exists. Deleting...")
        frappe.delete_doc("Web Form", "supplier-inquiry-form", force=True)
        frappe.db.commit()

    # Create WebForm
    webform = frappe.get_doc({
        "doctype": "Web Form",
        "title": "פניית ספק",
        "route": "supplier-inquiry-form",
        "doc_type": "Supplier Inquiry",
        "is_standard": 0,
        "published": 1,
        "login_required": 1,
        "allow_edit": 0,
        "allow_delete": 0,
        "allow_multiple": 1,
        "show_sidebar": 1,
        "allow_print": 1,
        "allow_comments": 0,
        "show_list": 1,
        "show_attachments": 1,
        "max_attachment_size": 5,  # 5 MB
        "apply_document_permissions": 1,

        # Success message
        "success_url": "/supplier-inquiry-form",
        "success_message": "הפנייה נשלחה בהצלחה! תוכל לעקוב אחר הסטטוס שלה ברשימת הפניות.",

        # Introduction text
        "introduction_text": """
        <div style="padding: 15px; background-color: #f8f9fa; border-right: 4px solid #007bff; margin-bottom: 20px;">
            <h4>ברוכים הבאים למערכת הפניות</h4>
            <p>דרך טופס זה תוכלו לפנות אלינו בנושאים שונים הקשורים לפעילותכם כספק.</p>
            <p>אנא מלאו את כל השדות הנדרשים, ונחזור אליכם בהקדם האפשרי.</p>
        </div>
        """,

        # List settings
        "list_title": "הפניות שלי",
        "list_columns": [
            {
                "fieldname": "name",
                "fieldtype": "Link"
            },
            {
                "fieldname": "topic_category",
                "fieldtype": "Link"
            },
            {
                "fieldname": "inquiry_status",
                "fieldtype": "Data"
            },
            {
                "fieldname": "creation",
                "fieldtype": "Datetime"
            }
        ],

        # Web Form Fields
        "web_form_fields": [
            # Supplier Section
            {
                "fieldname": "supplier_section",
                "fieldtype": "Section Break",
                "label": "פרטי ספק",
                "hidden": 0
            },
            {
                "fieldname": "supplier_link",
                "fieldtype": "Link",
                "label": "מזהה ספק",
                "options": "Supplier",
                "reqd": 1,
                "read_only": 1,
                "hidden": 0,
                "description": "מזהה הספק שלך (מוקצה אוטומטית)"
            },

            # Topic Section
            {
                "fieldname": "topic_section",
                "fieldtype": "Section Break",
                "label": "נושא הפנייה",
                "hidden": 0
            },
            {
                "fieldname": "topic_category",
                "fieldtype": "Link",
                "label": "קטגוריית נושא פנייה",
                "options": "Inquiry Topic Category",
                "reqd": 1,
                "hidden": 0,
                "description": "אנא בחר את קטגוריית הנושא המתאימה ביותר לפנייתך"
            },

            # Inquiry Content Section
            {
                "fieldname": "inquiry_section",
                "fieldtype": "Section Break",
                "label": "תוכן הפנייה",
                "hidden": 0
            },
            {
                "fieldname": "inquiry_description",
                "fieldtype": "Text Editor",
                "label": "תיאור הפנייה",
                "reqd": 1,
                "hidden": 0,
                "description": "אנא פרט את פנייתך בצורה ברורה ומפורטת"
            },

            # Context Section
            {
                "fieldname": "context_section",
                "fieldtype": "Section Break",
                "label": "הקשר הפנייה",
                "hidden": 0
            },
            {
                "fieldname": "inquiry_context",
                "fieldtype": "Select",
                "label": "הקשר הפנייה",
                "options": "ספק עצמו\nמבוטח",
                "reqd": 1,
                "hidden": 0,
                "description": "האם הפנייה היא בנוגע לספק עצמו או מבוטח?"
            },
            {
                "fieldname": "column_break_context",
                "fieldtype": "Column Break",
                "hidden": 0
            },
            {
                "fieldname": "insured_id_number",
                "fieldtype": "Data",
                "label": "מספר זהות של המבוטח",
                "hidden": 0,
                "depends_on": "eval:doc.inquiry_context=='מבוטח'",
                "mandatory_depends_on": "eval:doc.inquiry_context=='מבוטח'",
                "description": "מספר זהות של המבוטח (9 ספרות)"
            },
            {
                "fieldname": "insured_full_name",
                "fieldtype": "Data",
                "label": "שם מלא של המבוטח",
                "hidden": 0,
                "depends_on": "eval:doc.inquiry_context=='מבוטח'",
                "mandatory_depends_on": "eval:doc.inquiry_context=='מבוטח'",
                "description": "שם מלא של המבוטח"
            },

            # Attachments Section
            {
                "fieldname": "attachments_section",
                "fieldtype": "Section Break",
                "label": "קבצים מצורפים",
                "hidden": 0
            },
            {
                "fieldname": "attachments",
                "fieldtype": "Attach",
                "label": "קבצים מצורפים",
                "hidden": 0,
                "description": "ניתן לצרף מסמכים רלוונטיים לפנייה (עד 5MB)"
            }
        ]
    })

    try:
        webform.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Successfully created WebForm: {webform.name}")
        print(f"   Route: /{webform.route}")
        print(f"   DocType: {webform.doc_type}")
        print(f"   Published: {webform.published}")
        print(f"   Login Required: {webform.login_required}")
        print(f"   Apply Document Permissions: {webform.apply_document_permissions}")

    except Exception as e:
        print(f"❌ Error creating WebForm: {str(e)}")
        frappe.db.rollback()
        raise

    # Add client script to auto-populate supplier_link
    create_webform_client_script(webform.name)

    print("\n" + "="*80)
    print("WebForm Creation Complete!")
    print("="*80)
    print("\n📝 Next Steps:")
    print("1. Clear cache: bench --site development.localhost clear-cache")
    print("2. Visit: http://localhost:8000/supplier-inquiry-form")
    print("3. Test with a portal user account")
    print("\n")

    return {"success": True, "webform": webform.name}


def create_webform_client_script(webform_name):
    """Add client-side script to auto-populate supplier_link from user"""

    print("\n📜 Adding client script to auto-populate supplier_link...")

    client_script_code = """
// Auto-populate supplier_link from logged-in user
frappe.ready(function() {
    // Get the current user's supplier link
    frappe.call({
        method: 'frappe.client.get_value',
        args: {
            doctype: 'User',
            filters: {'name': frappe.session.user},
            fieldname: 'supplier_link'
        },
        callback: function(r) {
            if (r.message && r.message.supplier_link) {
                // Set the supplier_link field value
                frappe.web_form.set_value('supplier_link', r.message.supplier_link);

                // Make the field read-only
                frappe.web_form.fields_dict.supplier_link.df.read_only = 1;
                frappe.web_form.fields_dict.supplier_link.$wrapper.find('input').prop('disabled', true);

                console.log('Auto-populated supplier_link:', r.message.supplier_link);
            } else {
                // If no supplier link found, show error
                frappe.msgprint({
                    title: 'שגיאה',
                    indicator: 'red',
                    message: 'לא נמצא קישור לספק עבור המשתמש הנוכחי. אנא פנה למנהל המערכת.'
                });
            }
        }
    });
});

// Prevent manual modification of supplier_link
frappe.web_form.on('supplier_link', function() {
    // Re-fetch and set the correct value if someone tries to change it
    frappe.call({
        method: 'frappe.client.get_value',
        args: {
            doctype: 'User',
            filters: {'name': frappe.session.user},
            fieldname: 'supplier_link'
        },
        callback: function(r) {
            if (r.message && r.message.supplier_link) {
                frappe.web_form.set_value('supplier_link', r.message.supplier_link);
            }
        }
    });
});
"""

    # Check if client script already exists
    script_name = webform_name + "-auto-populate"
    if frappe.db.exists("Client Script", script_name):
        print(f"⚠️  Client Script '{script_name}' already exists. Updating...")
        script = frappe.get_doc("Client Script", script_name)
    else:
        script = frappe.new_doc("Client Script")
        script.name = script_name

    script.dt = "Supplier Inquiry"
    script.view = "Form"
    script.enabled = 1
    script.script = client_script_code

    try:
        if frappe.db.exists("Client Script", script_name):
            script.save(ignore_permissions=True)
        else:
            script.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Successfully created/updated Client Script: {script.name}")
    except Exception as e:
        print(f"❌ Error creating Client Script: {str(e)}")
        frappe.db.rollback()


def delete_supplier_inquiry_webform():
    """Delete the Supplier Inquiry WebForm (cleanup utility)"""

    print("\n🗑️  Deleting Supplier Inquiry WebForm...")

    if frappe.db.exists("Web Form", "supplier-inquiry-form"):
        frappe.delete_doc("Web Form", "supplier-inquiry-form", force=True)
        print("✅ Deleted WebForm: supplier-inquiry-form")
    else:
        print("ℹ️  WebForm 'supplier-inquiry-form' does not exist")

    # Delete client script
    script_name = "supplier-inquiry-form-auto-populate"
    if frappe.db.exists("Client Script", script_name):
        frappe.delete_doc("Client Script", script_name, force=True)
        print(f"✅ Deleted Client Script: {script_name}")

    frappe.db.commit()
    print("✅ Cleanup complete")


if __name__ == "__main__":
    create_supplier_inquiry_webform()
