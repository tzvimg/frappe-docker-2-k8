"""
Create Test Clinic DocTypes
This script creates Patient, Doctor, and Appointment DocTypes for the test_clinic app
"""
import frappe

@frappe.whitelist()
def create_all_clinic_doctypes():
    """Create all clinic DocTypes"""

    create_patient()
    create_doctor()
    create_appointment()

    frappe.db.commit()
    frappe.msgprint("✓ All Test Clinic DocTypes created successfully!")

    return {"success": True, "message": "Created Patient, Doctor, and Appointment DocTypes"}


def create_patient():
    """Create Patient DocType"""

    # Check if already exists
    if frappe.db.exists('DocType', 'Patient'):
        frappe.msgprint("Patient DocType already exists")
        return

    doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Patient',
        'module': 'Test Clinic',
        'autoname': 'format:PAT-{#####}',
        'naming_rule': 'By fieldname',
        'track_changes': 1,
        'fields': [
            {
                'fieldname': 'patient_details_section',
                'fieldtype': 'Section Break',
                'label': 'Patient Details'
            },
            {
                'fieldname': 'first_name',
                'fieldtype': 'Data',
                'label': 'First Name',
                'reqd': 1,
                'in_list_view': 1
            },
            {
                'fieldname': 'last_name',
                'fieldtype': 'Data',
                'label': 'Last Name',
                'reqd': 1,
                'in_list_view': 1
            },
            {
                'fieldname': 'column_break_1',
                'fieldtype': 'Column Break'
            },
            {
                'fieldname': 'date_of_birth',
                'fieldtype': 'Date',
                'label': 'Date of Birth',
                'reqd': 1
            },
            {
                'fieldname': 'gender',
                'fieldtype': 'Select',
                'label': 'Gender',
                'options': 'Male\nFemale\nOther',
                'reqd': 1
            },
            {
                'fieldname': 'contact_section',
                'fieldtype': 'Section Break',
                'label': 'Contact Information'
            },
            {
                'fieldname': 'phone',
                'fieldtype': 'Data',
                'label': 'Phone Number',
                'options': 'Phone'
            },
            {
                'fieldname': 'email',
                'fieldtype': 'Data',
                'label': 'Email',
                'options': 'Email'
            },
            {
                'fieldname': 'column_break_2',
                'fieldtype': 'Column Break'
            },
            {
                'fieldname': 'address',
                'fieldtype': 'Small Text',
                'label': 'Address'
            },
            {
                'fieldname': 'medical_section',
                'fieldtype': 'Section Break',
                'label': 'Medical Information'
            },
            {
                'fieldname': 'blood_group',
                'fieldtype': 'Select',
                'label': 'Blood Group',
                'options': '\nA+\nA-\nB+\nB-\nAB+\nAB-\nO+\nO-'
            },
            {
                'fieldname': 'allergies',
                'fieldtype': 'Small Text',
                'label': 'Allergies'
            }
        ],
        'permissions': [
            {
                'role': 'System Manager',
                'read': 1,
                'write': 1,
                'create': 1,
                'delete': 1
            }
        ]
    })

    doc.insert()
    frappe.msgprint(f"✓ Created {doc.name}")


def create_doctor():
    """Create Doctor DocType"""

    # Check if already exists
    if frappe.db.exists('DocType', 'Doctor'):
        frappe.msgprint("Doctor DocType already exists")
        return

    doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Doctor',
        'module': 'Test Clinic',
        'autoname': 'format:DOC-{####}',
        'naming_rule': 'By fieldname',
        'track_changes': 1,
        'fields': [
            {
                'fieldname': 'doctor_details_section',
                'fieldtype': 'Section Break',
                'label': 'Doctor Details'
            },
            {
                'fieldname': 'full_name',
                'fieldtype': 'Data',
                'label': 'Full Name',
                'reqd': 1,
                'in_list_view': 1
            },
            {
                'fieldname': 'specialization',
                'fieldtype': 'Select',
                'label': 'Specialization',
                'options': '\nGeneral Practice\nCardiology\nPediatrics\nOrthopedics\nDermatology\nNeurology',
                'reqd': 1,
                'in_list_view': 1
            },
            {
                'fieldname': 'column_break_1',
                'fieldtype': 'Column Break'
            },
            {
                'fieldname': 'license_number',
                'fieldtype': 'Data',
                'label': 'Medical License Number',
                'reqd': 1,
                'unique': 1
            },
            {
                'fieldname': 'years_of_experience',
                'fieldtype': 'Int',
                'label': 'Years of Experience'
            },
            {
                'fieldname': 'contact_section',
                'fieldtype': 'Section Break',
                'label': 'Contact Information'
            },
            {
                'fieldname': 'phone',
                'fieldtype': 'Data',
                'label': 'Phone Number',
                'options': 'Phone'
            },
            {
                'fieldname': 'email',
                'fieldtype': 'Data',
                'label': 'Email',
                'options': 'Email',
                'reqd': 1
            },
            {
                'fieldname': 'availability_section',
                'fieldtype': 'Section Break',
                'label': 'Availability'
            },
            {
                'fieldname': 'is_available',
                'fieldtype': 'Check',
                'label': 'Currently Available',
                'default': 1
            }
        ],
        'permissions': [
            {
                'role': 'System Manager',
                'read': 1,
                'write': 1,
                'create': 1,
                'delete': 1
            }
        ]
    })

    doc.insert()
    frappe.msgprint(f"✓ Created {doc.name}")


def create_appointment():
    """Create Appointment DocType with workflow support"""

    # Check if already exists
    if frappe.db.exists('DocType', 'Appointment'):
        frappe.msgprint("Appointment DocType already exists")
        return

    doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Appointment',
        'module': 'Test Clinic',
        'autoname': 'format:APT-{#####}',
        'naming_rule': 'By fieldname',
        'is_submittable': 1,  # Enable submit/cancel
        'track_changes': 1,
        'fields': [
            {
                'fieldname': 'appointment_details_section',
                'fieldtype': 'Section Break',
                'label': 'Appointment Details'
            },
            {
                'fieldname': 'patient',
                'fieldtype': 'Link',
                'label': 'Patient',
                'options': 'Patient',
                'reqd': 1,
                'in_list_view': 1
            },
            {
                'fieldname': 'doctor',
                'fieldtype': 'Link',
                'label': 'Doctor',
                'options': 'Doctor',
                'reqd': 1,
                'in_list_view': 1
            },
            {
                'fieldname': 'column_break_1',
                'fieldtype': 'Column Break'
            },
            {
                'fieldname': 'appointment_date',
                'fieldtype': 'Date',
                'label': 'Appointment Date',
                'reqd': 1,
                'in_list_view': 1
            },
            {
                'fieldname': 'appointment_time',
                'fieldtype': 'Time',
                'label': 'Appointment Time',
                'reqd': 1
            },
            {
                'fieldname': 'status_section',
                'fieldtype': 'Section Break',
                'label': 'Status'
            },
            {
                'fieldname': 'status',
                'fieldtype': 'Select',
                'label': 'Status',
                'options': 'Scheduled\nConfirmed\nIn Progress\nCompleted\nCancelled',
                'default': 'Scheduled',
                'in_list_view': 1,
                'reqd': 1
            },
            {
                'fieldname': 'column_break_2',
                'fieldtype': 'Column Break'
            },
            {
                'fieldname': 'duration',
                'fieldtype': 'Int',
                'label': 'Duration (minutes)',
                'default': 30
            },
            {
                'fieldname': 'notes_section',
                'fieldtype': 'Section Break',
                'label': 'Notes'
            },
            {
                'fieldname': 'reason',
                'fieldtype': 'Small Text',
                'label': 'Reason for Visit'
            },
            {
                'fieldname': 'notes',
                'fieldtype': 'Text',
                'label': 'Doctor Notes'
            }
        ],
        'permissions': [
            {
                'role': 'System Manager',
                'read': 1,
                'write': 1,
                'create': 1,
                'delete': 1,
                'submit': 1,
                'cancel': 1
            }
        ]
    })

    doc.insert()
    frappe.msgprint(f"✓ Created {doc.name}")
