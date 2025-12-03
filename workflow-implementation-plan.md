# Workflow Implementation Plan - Service Provider Application
## הקמת ספק חדש במערכת - Frappe Workflow

**Document Version:** 1.0
**Created:** 2025-12-03
**Status:** Planning Phase
**Based on:** workflow-spec.md, frappe-poc-plan.md

---

## Executive Summary

This document outlines the implementation plan for the "Service Provider Application" workflow in Frappe Framework. The workflow manages the end-to-end process of onboarding new service providers, from initial document submission through final approval and integration into the nursing management system.

**Key Components:**
- New DocType: `Service Provider Application`
- Frappe Workflow with 7 states and 8 transitions
- Email automation for provider communication
- Integration with existing `Service Provider` DocType
- Document checklist and file upload management

---

## 1. Current System Analysis

### 1.1 Existing DocTypes (from POC)
✅ **Already Implemented:**
- `Service Provider` - Core provider entity (HP number, name, contact info)
- `Service Provider Branch` - Branch locations linked to providers
- `Contract` - Service agreements with providers
- `Document Approval` - Document compliance tracking
- `Caregiver` - Individual caregiver records
- `Employment History` - Employment tracking (child table)

### 1.2 Gap Analysis
**What's Missing for Workflow:**
- ❌ Application/Request DocType for new providers
- ❌ Workflow states and transitions configuration
- ❌ Email alert templates for provider communication
- ❌ Document checklist management
- ❌ Integration logic to create Service Provider from approved application
- ❌ Role definitions for workflow participants

---

## 2. Implementation Architecture

### 2.1 New DocType: Service Provider Application

**Purpose:** Manage the application process for new service providers before they become active in the system.

**Relationship to Existing DocTypes:**
```
Service Provider Application (NEW)
  → [on approval] → Creates Service Provider (EXISTING)
    → Service Provider Branch (EXISTING)
      → Contract (EXISTING)
        → Document Approval (EXISTING)
```

**DocType Name:** `Service Provider Application`
**Module:** Nursing Management
**Naming:** Auto-name with format `SPA-.####` (e.g., SPA-0001, SPA-0002)

---

## 3. Detailed Implementation Specification

### 3.1 Service Provider Application - Fields

#### Section 1: Basic Information (פרטי ספק)
```json
{
  "provider_name": {
    "fieldtype": "Data",
    "label": "שם נותן השירות",
    "reqd": true,
    "description": "שם מלא של נותן השירות המבקש"
  },
  "hp_number": {
    "fieldtype": "Data",
    "label": "מספר ח\"פ",
    "reqd": true,
    "length": 9,
    "unique": false,
    "description": "מספר חברה/עוסק מורשה (9 ספרות)"
  },
  "service_type": {
    "fieldtype": "Select",
    "label": "סוג שירות",
    "options": "טיפול בבית\nמרכז יום\nקהילה תומכת\nמוצרי ספיגה",
    "reqd": true
  },
  "branch_type": {
    "fieldtype": "Data",
    "label": "סוג סניף",
    "description": "תיאור סוג הסניף העתידי"
  },
  "contact_person": {
    "fieldtype": "Data",
    "label": "איש קשר"
  },
  "phone": {
    "fieldtype": "Data",
    "label": "טלפון"
  },
  "email": {
    "fieldtype": "Data",
    "label": "אימייל",
    "options": "Email",
    "reqd": true
  },
  "address": {
    "fieldtype": "Small Text",
    "label": "כתובת"
  }
}
```

#### Section 2: Application Status (סטטוס בקשה)
```json
{
  "workflow_state": {
    "fieldtype": "Link",
    "label": "סטטוס",
    "options": "Workflow State",
    "read_only": true
  },
  "application_date": {
    "fieldtype": "Date",
    "label": "תאריך הגשה",
    "default": "Today",
    "read_only": true
  },
  "assigned_to": {
    "fieldtype": "Link",
    "label": "מטופל על ידי",
    "options": "User"
  }
}
```

#### Section 3: Document Checklist (רשימת מסמכים)
**Child Table:** `Application Document Checklist`
```json
{
  "document_type": {
    "fieldtype": "Select",
    "label": "סוג מסמך",
    "options": "אישור ניהול תקין\nתעודת עוסק מורשה\nאישור ביטוח\nהסכם בט\"ל\nפרטי בנק\nרשיון עסק",
    "reqd": true,
    "in_list_view": true
  },
  "status": {
    "fieldtype": "Select",
    "label": "סטטוס",
    "options": "חסר\nהוגש\nתקין\nלא תקין",
    "default": "חסר",
    "in_list_view": true
  },
  "attached_file": {
    "fieldtype": "Attach",
    "label": "קובץ מצורף",
    "in_list_view": true
  },
  "notes": {
    "fieldtype": "Small Text",
    "label": "הערות"
  }
}
```

#### Section 4: HQ Review (בדיקת מטה)
```json
{
  "hq_check_status": {
    "fieldtype": "Select",
    "label": "סטטוס בדיקת מטה",
    "options": "\nתקין\nלא תקין",
    "depends_on": "eval:doc.workflow_state=='HQ_Check'"
  },
  "hq_reviewer": {
    "fieldtype": "Link",
    "label": "בודק מטה",
    "options": "User",
    "depends_on": "eval:doc.workflow_state=='HQ_Check'"
  },
  "hq_review_date": {
    "fieldtype": "Date",
    "label": "תאריך בדיקת מטה"
  },
  "hq_notes": {
    "fieldtype": "Text Editor",
    "label": "הערות מטה"
  }
}
```

#### Section 5: Data Clarification (הבהרת נתונים)
```json
{
  "data_clarification_status": {
    "fieldtype": "Select",
    "label": "סטטוס הבהרת נתונים",
    "options": "\nתקין\nלא תקין",
    "depends_on": "eval:doc.workflow_state=='Data_Review'"
  },
  "bi_verification": {
    "fieldtype": "Check",
    "label": "אומת מול ביטוח לאומי",
    "depends_on": "eval:doc.workflow_state=='Data_Review'"
  },
  "data_reviewer": {
    "fieldtype": "Link",
    "label": "בודק נתונים",
    "options": "User"
  },
  "data_review_date": {
    "fieldtype": "Date",
    "label": "תאריך בדיקת נתונים"
  },
  "data_notes": {
    "fieldtype": "Text Editor",
    "label": "הערות בדיקת נתונים"
  }
}
```

#### Section 6: Rejection Handling (טיפול בדחייה)
```json
{
  "rejection_reason": {
    "fieldtype": "Text Editor",
    "label": "סיבת דחייה",
    "reqd": false,
    "depends_on": "eval:doc.workflow_state=='Rejected'"
  },
  "rejection_date": {
    "fieldtype": "Date",
    "label": "תאריך דחייה",
    "read_only": true
  }
}
```

#### Section 7: Final Processing (טיפול סופי)
```json
{
  "agreement_prepared": {
    "fieldtype": "Check",
    "label": "הסכם הוכן"
  },
  "agreement_file": {
    "fieldtype": "Attach",
    "label": "קובץ הסכם"
  },
  "nursing_system_synced": {
    "fieldtype": "Check",
    "label": "שוקף במערכת סיעוד"
  },
  "created_service_provider": {
    "fieldtype": "Link",
    "label": "נותן שירות שנוצר",
    "options": "Service Provider",
    "read_only": true
  },
  "approval_date": {
    "fieldtype": "Date",
    "label": "תאריך אישור סופי"
  }
}
```

#### Section 8: Communication Log (תיעוד תקשורת)
```json
{
  "communication_history": {
    "fieldtype": "Text Editor",
    "label": "היסטוריית תקשורת",
    "read_only": true
  }
}
```

---

### 3.2 Workflow Configuration

#### Workflow States (7 Total)

| State Code | State Name (Hebrew) | Description | Doc Status | Allow Edit |
|------------|---------------------|-------------|------------|------------|
| `Draft` | טיוטה/הגשה ראשונית | Initial submission by provider | Draft (0) | Service Provider User |
| `HQ_Check` | בדיקת מטה | HQ verification of documents | Submitted (0) | HQ Approver |
| `Data_Review` | בדיקת נתונים | Data verification and BI check | Submitted (0) | Internal Reviewer |
| `Agreement_Prep` | הכנת הסכם | Agreement preparation | Submitted (0) | Internal Reviewer |
| `Final_HQ_Processing` | טיפול מטה סופי | Final HQ processing and sync | Submitted (0) | HQ Approver |
| `Rejected` | נדחה | Application rejected | Cancelled (2) | None |
| `Approved` | הסכם התקבל | Application approved | Submitted (1) | None |

**State Configuration in Frappe:**
- **Draft State:** Starting point, allows provider to edit and submit
- **Intermediate States:** Submitted status, restricted editing based on role
- **Terminal States:** Approved (success) or Rejected (failure)

#### Workflow Transitions (8 Total)

| Action (Button) | From State | To State | Role | Conditions |
|-----------------|------------|----------|------|------------|
| **הגשת מסמכים** (Submit Documents) | Draft | HQ_Check | Service Provider User | All required fields filled |
| **תקין - מטה** (HQ Approved) | HQ_Check | Data_Review | HQ Approver | hq_check_status == "תקין" |
| **לא תקין - מטה** (HQ Rejected) | HQ_Check | Rejected | HQ Approver | hq_check_status == "לא תקין" |
| **תקין - נתונים** (Data Approved) | Data_Review | Agreement_Prep | Internal Reviewer | data_clarification_status == "תקין" |
| **לא תקין - נתונים** (Data Rejected) | Data_Review | Rejected | Internal Reviewer | data_clarification_status == "לא תקין" |
| **קליטה תקינה** (Documents Accepted) | Agreement_Prep | Final_HQ_Processing | Internal Reviewer | agreement_prepared == 1 |
| **קליטה לא תקינה** (Documents Not Accepted) | Agreement_Prep | Rejected | Internal Reviewer | agreement_prepared == 0 |
| **אישור סופי** (Final Approval) | Final_HQ_Processing | Approved | HQ Approver | nursing_system_synced == 1 |

**Transition Configuration:**
- Each transition requires specific field values as conditions
- Rejection transitions require `rejection_reason` to be filled
- Final approval triggers Service Provider creation

---

### 3.3 Role Definitions

#### Required Roles

**1. Service Provider User (נותן שירות - משתמש חיצוני)**
- **Purpose:** External provider submitting application
- **Permissions:**
  - Create: Service Provider Application (own only)
  - Read: Service Provider Application (own only)
  - Write: Service Provider Application (own only, Draft state only)
  - Transition: Draft → HQ_Check
- **Portal Access:** Yes (Web Portal)

**2. Internal Reviewer (בודק פנימי)**
- **Purpose:** Internal staff handling data review and preparation
- **Permissions:**
  - Read: All Service Provider Applications
  - Write: Service Provider Applications in Data_Review, Agreement_Prep states
  - Transitions:
    - Data_Review → Agreement_Prep
    - Data_Review → Rejected
    - Agreement_Prep → Final_HQ_Processing
    - Agreement_Prep → Rejected
- **Portal Access:** No (Desk access)

**3. HQ Approver (מאשר מטה)**
- **Purpose:** Headquarters staff for verification and final approval
- **Permissions:**
  - Read: All Service Provider Applications
  - Write: Service Provider Applications in HQ_Check, Final_HQ_Processing states
  - Transitions:
    - HQ_Check → Data_Review
    - HQ_Check → Rejected
    - Final_HQ_Processing → Approved
- **Portal Access:** No (Desk access)

**4. System Manager (מנהל מערכת)**
- **Purpose:** Full administrative access
- **Permissions:** All

---

### 3.4 Email Automation

#### Email Alert 1: New Application Received
**Trigger:** Transition from Draft → HQ_Check
**Recipients:** Users with role "HQ Approver"
**Subject:** `התקבלה בקשה חדשה להקמת נותן שירות - {{ doc.provider_name }}`

**Email Template (Hebrew):**
```html
<p>שלום,</p>

<p>התקבלה בקשה חדשה להקמת נותן שירות במערכת.</p>

<h3>פרטי הבקשה:</h3>
<ul>
  <li><strong>מספר בקשה:</strong> {{ doc.name }}</li>
  <li><strong>שם נותן השירות:</strong> {{ doc.provider_name }}</li>
  <li><strong>מספר ח"פ:</strong> {{ doc.hp_number }}</li>
  <li><strong>סוג שירות:</strong> {{ doc.service_type }}</li>
  <li><strong>תאריך הגשה:</strong> {{ doc.application_date }}</li>
</ul>

<p>אנא בדקו את המסמכים ועדכנו את סטטוס הבדיקה.</p>

<p><a href="{{ doc.get_url() }}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">צפייה בבקשה</a></p>

<p>בברכה,<br>מערכת ניהול סיעוד</p>
```

#### Email Alert 2: Application Rejected
**Trigger:** Transition to Rejected state
**Recipients:** `doc.email` (applicant)
**Subject:** `בקשתך להקמת נותן שירות נדחתה - {{ doc.provider_name }}`

**Email Template (Hebrew):**
```html
<p>שלום {{ doc.provider_name }},</p>

<p>לצערנו, בקשתך להקמת נותן שירות במערכת נדחתה.</p>

<h3>פרטי הדחייה:</h3>
<ul>
  <li><strong>מספר בקשה:</strong> {{ doc.name }}</li>
  <li><strong>תאריך דחייה:</strong> {{ doc.rejection_date }}</li>
</ul>

<h3>סיבת הדחייה:</h3>
<div style="background-color: #f8f9fa; padding: 15px; border-right: 4px solid #dc3545;">
  {{ doc.rejection_reason }}
</div>

<p>במידה ותרצו להגיש בקשה מתוקנת, אנא פנו אלינו.</p>

<p>בברכה,<br>אגף סיעוד</p>
```

#### Email Alert 3: Application Approved - Documents Verified
**Trigger:** Transition from Data_Review → Agreement_Prep
**Recipients:** `doc.email` (applicant)
**Subject:** `מסמכיך נבדקו ואושרו - {{ doc.provider_name }}`

**Email Template (Hebrew):**
```html
<p>שלום {{ doc.provider_name }},</p>

<p>שמחים לעדכן כי המסמכים שהגשת נבדקו ואושרו.</p>

<h3>פרטי הבקשה:</h3>
<ul>
  <li><strong>מספר בקשה:</strong> {{ doc.name }}</li>
  <li><strong>סטטוס נוכחי:</strong> הכנת הסכם</li>
</ul>

<p>הבקשה מועברת כעת לטיפול המשך במחלקות כספים, תקציבים והתקשרויות.</p>

<p>נעדכן אותך בהתקדמות.</p>

<p>בברכה,<br>אגף סיעוד</p>
```

#### Email Alert 4: Application Fully Approved
**Trigger:** Transition to Approved state
**Recipients:** `doc.email` (applicant)
**Subject:** `ההסכם התקבל ואושר - {{ doc.provider_name }}`

**Email Template (Hebrew):**
```html
<p>שלום {{ doc.provider_name }},</p>

<p>מזל טוב! בקשתך להקמת נותן שירות אושרה במלואה.</p>

<h3>פרטי האישור:</h3>
<ul>
  <li><strong>מספר בקשה:</strong> {{ doc.name }}</li>
  <li><strong>תאריך אישור:</strong> {{ doc.approval_date }}</li>
  <li><strong>מספר נותן שירות במערכת:</strong> {{ doc.created_service_provider }}</li>
</ul>

<p>ההסכם שוקף במערכת הסיעוד ותוכלו להתחיל בפעילות.</p>

<p>ניתן לגשת למערכת באמצעות הפורטל:</p>
<p><a href="{{ get_url() }}" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">כניסה לפורטל</a></p>

<p>בהצלחה,<br>אגף סיעוד</p>
```

#### Email Alert 5: Internal - Move to Final Processing
**Trigger:** Transition from Agreement_Prep → Final_HQ_Processing
**Recipients:** Users with role "HQ Approver"
**Subject:** `בקשה מוכנה לטיפול סופי - {{ doc.provider_name }}`

**Email Template (Hebrew):**
```html
<p>שלום,</p>

<p>בקשת נותן שירות מוכנה לטיפול מטה סופי.</p>

<h3>פרטי הבקשה:</h3>
<ul>
  <li><strong>מספר בקשה:</strong> {{ doc.name }}</li>
  <li><strong>שם נותן השירות:</strong> {{ doc.provider_name }}</li>
  <li><strong>מספר ח"פ:</strong> {{ doc.hp_number }}</li>
</ul>

<p><strong>נדרש:</strong></p>
<ul>
  <li>שיקוף ההסכם במערכת סיעוד</li>
  <li>יצירת רשומת נותן שירות במערכת</li>
  <li>אישור סופי</li>
</ul>

<p><a href="{{ doc.get_url() }}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">צפייה בבקשה</a></p>

<p>בברכה,<br>מערכת ניהול סיעוד</p>
```

---

### 3.5 Python Controller Logic

**File:** `service_provider_application.py`

#### Key Methods to Implement

**1. Validation Method**
```python
def validate(self):
    """Validate application data before saving"""
    self.validate_hp_number()
    self.validate_email()
    self.validate_required_documents()
    self.validate_workflow_state_changes()
```

**2. HP Number Validation**
```python
def validate_hp_number(self):
    """Validate HP number format (9 digits)"""
    if self.hp_number:
        hp_clean = self.hp_number.strip()
        if not hp_clean.isdigit():
            frappe.throw(_("מספר ח\"פ must contain only digits"))
        if len(hp_clean) != 9:
            frappe.throw(_("מספר ח\"פ must be exactly 9 digits"))
        self.hp_number = hp_clean

    # Check for duplicate HP in approved applications
    if self.workflow_state == "Approved":
        existing = frappe.db.exists("Service Provider", {"hp_number": self.hp_number})
        if existing:
            frappe.throw(_("Service Provider with HP number {0} already exists").format(self.hp_number))
```

**3. Required Documents Validation**
```python
def validate_required_documents(self):
    """Ensure all required documents are present before certain transitions"""
    if self.workflow_state in ["HQ_Check", "Data_Review", "Agreement_Prep"]:
        if not self.application_document_checklist:
            frappe.throw(_("אנא הוסף רשימת מסמכים נדרשים"))

        required_docs = ["אישור ניהול תקין", "תעודת עוסק מורשה", "אישור ביטוח"]
        for doc_type in required_docs:
            found = any(d.document_type == doc_type for d in self.application_document_checklist)
            if not found:
                frappe.msgprint(
                    _("מסמך חסר: {0}").format(doc_type),
                    title=_("אזהרה"),
                    indicator="orange"
                )
```

**4. Workflow State Change Handler**
```python
def validate_workflow_state_changes(self):
    """Validate state transitions and set required fields"""
    # On rejection, ensure rejection reason is provided
    if self.workflow_state == "Rejected" and not self.rejection_reason:
        frappe.throw(_("נדרשת סיבת דחייה"))

    # Set rejection date
    if self.workflow_state == "Rejected" and not self.rejection_date:
        self.rejection_date = frappe.utils.today()

    # Set approval date
    if self.workflow_state == "Approved" and not self.approval_date:
        self.approval_date = frappe.utils.today()
```

**5. Auto-Create Service Provider on Approval**
```python
def on_update_after_submit(self):
    """Trigger actions after document state changes"""
    if self.workflow_state == "Approved" and not self.created_service_provider:
        self.create_service_provider()
        self.log_communication("נותן שירות נוצר במערכת")
```

**6. Service Provider Creation Logic**
```python
def create_service_provider(self):
    """Create Service Provider record from approved application"""
    try:
        # Check if already exists
        existing = frappe.db.exists("Service Provider", {"hp_number": self.hp_number})
        if existing:
            frappe.msgprint(
                _("Service Provider {0} already exists").format(existing),
                title=_("הודעה"),
                indicator="blue"
            )
            self.created_service_provider = existing
            return

        # Create new Service Provider
        sp = frappe.get_doc({
            "doctype": "Service Provider",
            "hp_number": self.hp_number,
            "provider_name": self.provider_name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "service_types": self.service_type,
            "status": "פעיל"
        })
        sp.insert(ignore_permissions=True)

        # Link back to application
        self.created_service_provider = sp.name
        self.save(ignore_permissions=True)

        frappe.msgprint(
            _("Service Provider {0} created successfully").format(sp.name),
            title=_("הצלחה"),
            indicator="green"
        )

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Service Provider Creation Failed")
        frappe.throw(_("Failed to create Service Provider: {0}").format(str(e)))
```

**7. Communication Logging**
```python
def log_communication(self, message):
    """Add entry to communication history"""
    timestamp = frappe.utils.now_datetime().strftime("%Y-%m-%d %H:%M:%S")
    user = frappe.session.user

    new_entry = f"[{timestamp}] {user}: {message}\n"

    if self.communication_history:
        self.communication_history += new_entry
    else:
        self.communication_history = new_entry
```

**8. Document Status Check**
```python
def check_document_completeness(self):
    """Check if all documents are in 'תקין' status"""
    if not self.application_document_checklist:
        return False

    all_valid = all(doc.status == "תקין" for doc in self.application_document_checklist)
    return all_valid
```

---

### 3.6 Client-Side JavaScript (Optional Enhancements)

**File:** `service_provider_application.js`

```javascript
frappe.ui.form.on('Service Provider Application', {
    refresh: function(frm) {
        // Add custom buttons based on state
        add_custom_buttons(frm);

        // Set field properties based on workflow state
        set_field_properties(frm);

        // Show document completeness indicator
        show_document_status(frm);
    },

    workflow_state: function(frm) {
        // Update field visibility on state change
        set_field_properties(frm);
    },

    hp_number: function(frm) {
        // Auto-format HP number (remove spaces/dashes)
        if (frm.doc.hp_number) {
            frm.set_value('hp_number', frm.doc.hp_number.replace(/[^0-9]/g, ''));
        }
    }
});

function add_custom_buttons(frm) {
    // Check Document Completeness button
    if (frm.doc.workflow_state === 'Agreement_Prep') {
        frm.add_custom_button(__('בדוק שלמות מסמכים'), function() {
            frappe.call({
                method: 'check_document_completeness',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(__('כל המסמכים תקינים'));
                    } else {
                        frappe.msgprint(__('יש מסמכים חסרים או לא תקינים'));
                    }
                }
            });
        });
    }
}

function set_field_properties(frm) {
    // Make fields read-only based on workflow state
    const state = frm.doc.workflow_state;

    if (state !== 'Draft') {
        frm.set_df_property('provider_name', 'read_only', 1);
        frm.set_df_property('hp_number', 'read_only', 1);
        frm.set_df_property('service_type', 'read_only', 1);
    }
}

function show_document_status(frm) {
    // Show visual indicator of document status
    if (frm.doc.application_document_checklist) {
        const total = frm.doc.application_document_checklist.length;
        const valid = frm.doc.application_document_checklist.filter(d => d.status === 'תקין').length;
        const submitted = frm.doc.application_document_checklist.filter(d => d.status === 'הוגש').length;
        const missing = frm.doc.application_document_checklist.filter(d => d.status === 'חסר').length;

        const html = `
            <div style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                <strong>סטטוס מסמכים:</strong><br>
                <span style="color: green;">✓ תקין: ${valid}</span> |
                <span style="color: blue;">⏳ הוגש: ${submitted}</span> |
                <span style="color: red;">✗ חסר: ${missing}</span>
                <div style="margin-top: 5px;">
                    <progress value="${valid}" max="${total}" style="width: 100%;"></progress>
                    <small>${Math.round(valid/total*100)}% הושלם</small>
                </div>
            </div>
        `;

        frm.get_field('application_document_checklist').$wrapper.prepend(html);
    }
}

// Child table events
frappe.ui.form.on('Application Document Checklist', {
    attached_file: function(frm, cdt, cdn) {
        // Auto-change status to 'הוגש' when file is attached
        const row = locals[cdt][cdn];
        if (row.attached_file && row.status === 'חסר') {
            frappe.model.set_value(cdt, cdn, 'status', 'הוגש');
        }
    }
});
```

---

## 4. Implementation Tasks Breakdown

### Phase 1: DocType Creation (Day 1)
**Priority:** High
**Estimated Time:** 4-6 hours

- [ ] **Task 1.1:** Create `Service Provider Application` DocType via Frappe UI
  - Add all fields from Section 3.1
  - Configure field properties (required, read-only, depends_on)
  - Set auto-naming rule: `SPA-.####`
  - Enable track_changes

- [ ] **Task 1.2:** Create `Application Document Checklist` child table DocType
  - Add fields: document_type, status, attached_file, notes
  - Configure in_list_view properties

- [ ] **Task 1.3:** Add child table to `Service Provider Application`
  - Field name: `application_document_checklist`
  - Label: "רשימת מסמכים נדרשים"

- [ ] **Task 1.4:** Initial testing
  - Create test application record
  - Verify field validations
  - Test child table functionality

**Deliverable:** Functional DocType with all fields, ready for workflow configuration

---

### Phase 2: Workflow Configuration (Day 1-2)
**Priority:** High
**Estimated Time:** 4-6 hours

- [ ] **Task 2.1:** Create Workflow document
  - Navigate to: Setup → Workflow → New
  - Name: "Service Provider Application Workflow"
  - Document Type: "Service Provider Application"
  - Workflow State Field: "workflow_state"
  - Is Active: Yes

- [ ] **Task 2.2:** Define Workflow States (7 states)
  - Create states as per Section 3.2
  - Configure doc_status for each state
  - Set allow_edit roles

- [ ] **Task 2.3:** Define Workflow Transitions (8 transitions)
  - Configure actions and button labels (Hebrew)
  - Set allowed roles for each transition
  - Add conditions where applicable

- [ ] **Task 2.4:** Test workflow transitions
  - Test each transition path
  - Verify role-based access
  - Test rejection flows
  - Test approval flow

**Deliverable:** Fully configured and tested workflow

---

### Phase 3: Role & Permission Setup (Day 2)
**Priority:** High
**Estimated Time:** 2-3 hours

- [ ] **Task 3.1:** Create custom roles
  - Create role: "Service Provider User"
  - Create role: "Internal Reviewer"
  - Create role: "HQ Approver"

- [ ] **Task 3.2:** Configure DocType permissions
  - Set permissions for Service Provider Application
  - Configure state-based permissions
  - Set portal access for Service Provider User

- [ ] **Task 3.3:** Create test users
  - Create test user with "Service Provider User" role
  - Create test user with "Internal Reviewer" role
  - Create test user with "HQ Approver" role

- [ ] **Task 3.4:** Test permission enforcement
  - Test with each user role
  - Verify state-based edit restrictions
  - Test portal access

**Deliverable:** Proper role-based access control

---

### Phase 4: Python Controller Implementation (Day 2-3)
**Priority:** High
**Estimated Time:** 6-8 hours

- [ ] **Task 4.1:** Implement validation methods
  - `validate()` method
  - `validate_hp_number()`
  - `validate_email()`
  - `validate_required_documents()`
  - `validate_workflow_state_changes()`

- [ ] **Task 4.2:** Implement workflow handlers
  - `on_update_after_submit()` method
  - State change logging
  - Rejection date auto-set
  - Approval date auto-set

- [ ] **Task 4.3:** Implement Service Provider creation
  - `create_service_provider()` method
  - Duplicate check logic
  - Error handling
  - Success notification

- [ ] **Task 4.4:** Implement helper methods
  - `log_communication()` method
  - `check_document_completeness()` method

- [ ] **Task 4.5:** Testing
  - Test all validation rules
  - Test Service Provider creation
  - Test error scenarios
  - Test communication logging

**Deliverable:** Fully functional Python controller with all business logic

---

### Phase 5: Email Automation (Day 3)
**Priority:** Medium
**Estimated Time:** 4-5 hours

- [ ] **Task 5.1:** Create email alert templates
  - Create 5 email alert documents (Section 3.4)
  - Configure Hebrew email templates
  - Add inline CSS for better formatting

- [ ] **Task 5.2:** Configure email triggers
  - Alert 1: On transition to HQ_Check
  - Alert 2: On transition to Rejected
  - Alert 3: On transition to Agreement_Prep
  - Alert 4: On transition to Approved
  - Alert 5: On transition to Final_HQ_Processing

- [ ] **Task 5.3:** Setup email account (if needed)
  - Configure SMTP settings in Frappe
  - Test email delivery

- [ ] **Task 5.4:** Test email automation
  - Test each email trigger
  - Verify recipient configuration
  - Check email content and formatting
  - Verify Hebrew RTL rendering

**Deliverable:** Automated email notifications working for all workflow states

---

### Phase 6: Client-Side Enhancements (Day 3-4)
**Priority:** Low
**Estimated Time:** 3-4 hours

- [ ] **Task 6.1:** Implement JavaScript enhancements
  - Add custom buttons based on state
  - Implement field property management
  - Add document status indicator

- [ ] **Task 6.2:** Add child table enhancements
  - Auto-update status on file upload
  - Visual feedback for document completeness

- [ ] **Task 6.3:** Add form validations
  - HP number auto-formatting
  - Email validation
  - Phone number formatting

- [ ] **Task 6.4:** Testing
  - Test all custom buttons
  - Verify visual indicators
  - Test user experience flow

**Deliverable:** Enhanced user interface with better UX

---

### Phase 7: Integration Testing (Day 4)
**Priority:** High
**Estimated Time:** 4-6 hours

- [ ] **Task 7.1:** End-to-end workflow testing
  - Test complete application lifecycle
  - Test with different user roles
  - Test all rejection scenarios
  - Test approval and Service Provider creation

- [ ] **Task 7.2:** Integration with existing DocTypes
  - Verify Service Provider creation
  - Test link between Application and Service Provider
  - Verify data consistency

- [ ] **Task 7.3:** Portal testing
  - Test portal access for Service Provider User
  - Test document upload via portal
  - Test form submission via portal

- [ ] **Task 7.4:** Email flow testing
  - Test all email notifications
  - Verify email content
  - Check delivery timing

**Deliverable:** Fully tested and integrated workflow

---

### Phase 8: Documentation & Training (Day 4-5)
**Priority:** Medium
**Estimated Time:** 4-5 hours

- [ ] **Task 8.1:** Create user documentation
  - Service Provider user guide (portal)
  - Internal reviewer guide
  - HQ approver guide
  - Admin guide

- [ ] **Task 8.2:** Create technical documentation
  - Workflow diagram
  - State transition matrix
  - Email alert reference
  - API documentation (if needed)

- [ ] **Task 8.3:** Prepare demo scenarios
  - Create sample applications
  - Prepare demo script
  - Create screenshots/videos

- [ ] **Task 8.4:** Training materials
  - Create training presentation
  - Prepare FAQ document
  - Create troubleshooting guide

**Deliverable:** Complete documentation package

---

## 5. Testing Strategy

### 5.1 Unit Testing Scenarios

**Test Case 1: HP Number Validation**
- Input: Valid 9-digit number → Expected: Pass
- Input: 8-digit number → Expected: Error message
- Input: Alphanumeric string → Expected: Error message
- Input: Number with spaces → Expected: Auto-cleaned and pass

**Test Case 2: Workflow Transition - Draft to HQ_Check**
- User Role: Service Provider User
- Prerequisites: All required fields filled
- Action: Click "הגשת מסמכים"
- Expected: State changes to HQ_Check, email sent to HQ Approver

**Test Case 3: Workflow Transition - HQ_Check to Rejected**
- User Role: HQ Approver
- Prerequisites: hq_check_status = "לא תקין"
- Action: Click "לא תקין - מטה"
- Expected: State changes to Rejected, rejection_date set, email sent to applicant

**Test Case 4: Service Provider Auto-Creation**
- Prerequisites: Application approved, HP number unique
- Expected: New Service Provider created, link set in application

**Test Case 5: Duplicate HP Number Check**
- Prerequisites: Service Provider with HP 123456789 exists
- Action: Approve application with same HP number
- Expected: Error message, no duplicate created

### 5.2 Integration Testing Scenarios

**Scenario 1: Complete Approval Flow**
1. Provider submits application (Draft → HQ_Check)
2. HQ approves (HQ_Check → Data_Review)
3. Internal reviewer approves data (Data_Review → Agreement_Prep)
4. Documents accepted (Agreement_Prep → Final_HQ_Processing)
5. Final approval (Final_HQ_Processing → Approved)
6. Verify Service Provider created
7. Verify all emails sent

**Scenario 2: Early Rejection at HQ**
1. Provider submits application
2. HQ rejects (HQ_Check → Rejected)
3. Verify rejection email sent
4. Verify no Service Provider created

**Scenario 3: Rejection After Data Review**
1. Provider submits application
2. HQ approves
3. Data review fails (Data_Review → Rejected)
4. Verify rejection email sent
5. Verify reason captured

### 5.3 User Acceptance Testing

**UAT Scenario 1: Service Provider Submits Application**
- User: External service provider (portal user)
- Task: Fill application form, upload documents, submit
- Success Criteria: Application submitted successfully, confirmation received

**UAT Scenario 2: Internal Reviewer Processes Application**
- User: Internal reviewer
- Task: Review documents, update status, approve/reject
- Success Criteria: Can update status, transitions work, emails sent

**UAT Scenario 3: HQ Final Approval**
- User: HQ approver
- Task: Final review, sync with nursing system, approve
- Success Criteria: Can mark as synced, Service Provider created automatically

---

## 6. Risk Management

### 6.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Workflow state conflicts | High | Low | Implement proper locking, test concurrent access |
| Email delivery failures | Medium | Medium | Configure retry logic, log failed emails, use queue |
| Service Provider duplicate creation | High | Low | Add unique constraint check, transaction handling |
| Document upload size limits | Medium | Low | Configure max upload size, validate before upload |
| Portal access issues | Medium | Medium | Test thoroughly, document setup steps |
| Hebrew email rendering | Low | Medium | Test with multiple email clients, use UTF-8 |

### 6.2 Business Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| User adoption resistance | High | Medium | Provide training, create user guides, support channel |
| Incomplete requirements | High | Medium | Regular stakeholder reviews, iterative approach |
| Role confusion | Medium | Low | Clear role definitions, permission documentation |
| Process delays | Medium | Medium | SLA tracking, escalation workflow (future) |

---

## 7. Success Criteria

### 7.1 Functional Requirements
- ✅ Service Provider Application DocType created with all fields
- ✅ Child table for document checklist functioning
- ✅ Workflow with 7 states and 8 transitions configured
- ✅ Role-based access control working
- ✅ Portal access for external users enabled
- ✅ Email notifications sent at appropriate workflow stages
- ✅ Service Provider auto-created on final approval
- ✅ Duplicate prevention working
- ✅ Communication logging functional

### 7.2 Technical Requirements
- ✅ All validations working correctly
- ✅ No data integrity issues
- ✅ Hebrew RTL interface working
- ✅ File uploads working via portal and desk
- ✅ Performance acceptable (< 2 seconds for transitions)
- ✅ Error handling robust
- ✅ Logging adequate for troubleshooting

### 7.3 Business Requirements
- ✅ Process workflow matches specification
- ✅ Email templates professional and clear
- ✅ User experience smooth for all roles
- ✅ Audit trail complete
- ✅ Management can track applications
- ✅ Reporting possible (list views, filters)

---

## 8. Post-Implementation Enhancements (Future)

### 8.1 Phase 2 Features
- **SLA Tracking:** Automatic escalation if application stuck in state
- **Dashboard:** Visual overview of applications by state
- **Reports:** Custom reports for management (approval rates, avg time, etc.)
- **Batch Operations:** Bulk approve/reject applications
- **Advanced Portal:** Provider can track status, receive notifications

### 8.2 Integration Opportunities
- **BI Integration:** Auto-verify HP numbers against ביטוח לאומי API
- **Document OCR:** Auto-extract data from uploaded documents
- **E-Signature:** Electronic signature for agreements
- **SMS Notifications:** SMS alerts in addition to email
- **Mobile App:** Native mobile app for providers

### 8.3 AI/Automation Enhancements
- **Document Classification:** AI-based document type detection
- **Anomaly Detection:** Flag suspicious applications
- **Chatbot:** Automated responses to common questions
- **Predictive Analytics:** Predict approval likelihood
- **Smart Routing:** Auto-assign to best reviewer

---

## 9. Implementation Timeline

### Summary Timeline
| Phase | Duration | Dependencies | Deliverable |
|-------|----------|--------------|-------------|
| Phase 1: DocType Creation | 4-6 hours | None | DocType ready for workflow |
| Phase 2: Workflow Config | 4-6 hours | Phase 1 | Workflow operational |
| Phase 3: Roles & Permissions | 2-3 hours | Phase 2 | Access control configured |
| Phase 4: Python Controller | 6-8 hours | Phase 2 | Business logic complete |
| Phase 5: Email Automation | 4-5 hours | Phase 2, 4 | Email alerts working |
| Phase 6: Client JS | 3-4 hours | Phase 1, 2 | Enhanced UX |
| Phase 7: Integration Testing | 4-6 hours | All above | Fully tested system |
| Phase 8: Documentation | 4-5 hours | Phase 7 | Documentation complete |

**Total Estimated Time:** 31-43 hours (4-5 working days)

### Recommended Schedule
- **Day 1 (8 hours):** Phase 1 + Start Phase 2
- **Day 2 (8 hours):** Complete Phase 2 + Phase 3 + Start Phase 4
- **Day 3 (8 hours):** Complete Phase 4 + Phase 5
- **Day 4 (8 hours):** Phase 6 + Phase 7
- **Day 5 (4-8 hours):** Phase 8 + Buffer for issues

---

## 10. Resources & References

### 10.1 Frappe Documentation
- **Workflow:** https://frappeframework.com/docs/user/en/workflow
- **Email Alerts:** https://frappeframework.com/docs/user/en/email-alerts
- **Portal:** https://frappeframework.com/docs/user/en/portal
- **Permissions:** https://frappeframework.com/docs/user/en/permissions

### 10.2 Related Project Files
- `workflow-spec.md` - Original workflow specification (Hebrew)
- `frappe-poc-plan.md` - POC implementation plan with existing DocTypes
- `nursing_management/` - Custom Frappe app directory

### 10.3 Key File Locations
```
/workspace/development/frappe-bench/apps/nursing_management/
├── nursing_management/nursing_management/
│   ├── doctype/
│   │   ├── service_provider_application/
│   │   │   ├── service_provider_application.json
│   │   │   ├── service_provider_application.py
│   │   │   └── service_provider_application.js
│   │   └── application_document_checklist/
│   │       ├── application_document_checklist.json
│   │       └── application_document_checklist.py
│   └── email_templates/
│       ├── new_application_alert.html
│       ├── application_rejected.html
│       ├── documents_approved.html
│       ├── application_fully_approved.html
│       └── ready_for_final_processing.html
```

---

## 11. Appendices

### Appendix A: Workflow State Diagram

```
[Draft/טיוטה]
    |
    | הגשת מסמכים (Service Provider User)
    v
[HQ_Check/בדיקת מטה]
    |
    |----> תקין (HQ Approver) --------> [Data_Review/בדיקת נתונים]
    |                                       |
    |                                       |----> תקין (Internal Reviewer) --> [Agreement_Prep/הכנת הסכם]
    |                                       |                                        |
    |                                       |                                        |----> קליטה תקינה --> [Final_HQ_Processing/טיפול מטה סופי]
    |                                       |                                        |                          |
    |                                       |                                        |                          |----> אישור סופי --> [Approved/הסכם התקבל] ✓
    |                                       |                                        |
    |                                       |                                        |----> קליטה לא תקינה --> [Rejected/נדחה] ✗
    |                                       |
    |                                       |----> לא תקין (Internal Reviewer) ----> [Rejected/נדחה] ✗
    |
    |----> לא תקין (HQ Approver) --------> [Rejected/נדחה] ✗
```

### Appendix B: Field Dependencies Matrix

| Field | Visible When | Required When | Read-Only When |
|-------|--------------|---------------|----------------|
| provider_name | Always | Always | workflow_state != 'Draft' |
| hp_number | Always | Always | workflow_state != 'Draft' |
| service_type | Always | Always | workflow_state != 'Draft' |
| hq_check_status | workflow_state == 'HQ_Check' | On transition from HQ_Check | workflow_state != 'HQ_Check' |
| data_clarification_status | workflow_state == 'Data_Review' | On transition from Data_Review | workflow_state != 'Data_Review' |
| rejection_reason | workflow_state == 'Rejected' | workflow_state == 'Rejected' | workflow_state != 'Rejected' |
| created_service_provider | workflow_state == 'Approved' | No | Always |

### Appendix C: Email Template Variables

Available variables in Jinja2 templates:
- `{{ doc.name }}` - Application ID (e.g., SPA-0001)
- `{{ doc.provider_name }}` - Provider name
- `{{ doc.hp_number }}` - HP number
- `{{ doc.service_type }}` - Service type
- `{{ doc.application_date }}` - Application date
- `{{ doc.rejection_reason }}` - Rejection reason
- `{{ doc.rejection_date }}` - Rejection date
- `{{ doc.approval_date }}` - Approval date
- `{{ doc.created_service_provider }}` - Created Service Provider ID
- `{{ doc.get_url() }}` - Direct link to application
- `{{ frappe.utils.get_url() }}` - Base site URL

### Appendix D: Sample Data for Testing

**Test Application 1 - Should be Approved:**
- Provider Name: "מרכז סיעודי השרון"
- HP Number: "987654321"
- Service Type: "טיפול בבית"
- Email: "test@sharon-care.co.il"
- Documents: All uploaded, all valid
- Expected Result: Approved, Service Provider created

**Test Application 2 - Should be Rejected at HQ:**
- Provider Name: "טיפול ביתי דרום"
- HP Number: "111222333"
- Service Type: "מרכז יום"
- Email: "test@south-care.co.il"
- Documents: Missing "אישור ניהול תקין"
- Expected Result: Rejected at HQ_Check

**Test Application 3 - Should be Rejected at Data Review:**
- Provider Name: "סיעוד מקצועי צפון"
- HP Number: "444555666"
- Service Type: "קהילה תומכת"
- Email: "test@north-care.co.il"
- Documents: All uploaded, but BI verification fails
- Expected Result: Rejected at Data_Review

---

## 12. Quick Reference Commands

### Create DocType via Bench Console
```python
# Enter bench console
cd /workspace/development/frappe-bench
bench --site development.localhost console

# Create Service Provider Application DocType programmatically
# (Or use UI - recommended)
```

### Clear Cache After Changes
```bash
cd /workspace/development/frappe-bench
bench --site development.localhost clear-cache
```

### View Application List
```
URL: http://localhost:8000/app/service-provider-application
```

### Access Workflow Configuration
```
URL: http://localhost:8000/app/workflow/Service%20Provider%20Application%20Workflow
```

### Test Email Template
```python
# In bench console
frappe.sendmail(
    recipients=["test@example.com"],
    subject="Test Email",
    template="application_rejected",
    args={"doc": frappe.get_doc("Service Provider Application", "SPA-0001")}
)
```

---

## 13. Troubleshooting Guide

### Issue 1: Workflow transitions not appearing
**Symptoms:** Buttons for transitions don't show in form
**Possible Causes:**
- Workflow not active
- User doesn't have required role
- Document not in correct state

**Solution:**
1. Check workflow is set to "Is Active"
2. Verify user has required role for transition
3. Check current workflow_state field value
4. Clear cache: `bench --site development.localhost clear-cache`

### Issue 2: Email not sending
**Symptoms:** Email alert triggered but email not received
**Possible Causes:**
- Email account not configured
- Email alert not enabled
- Recipient email invalid
- Email queue stuck

**Solution:**
1. Check: Setup → Email → Email Account
2. Check: Setup → Email → Email Alert (ensure "Enabled" is checked)
3. Check email queue: Setup → Email → Email Queue
4. Test SMTP connection: Setup → Email → Email Account → Test

### Issue 3: Service Provider not auto-created
**Symptoms:** Application approved but Service Provider not created
**Possible Causes:**
- Python controller error
- Duplicate HP number
- Permission issue
- Method not called

**Solution:**
1. Check Error Log: Setup → Error Log
2. Verify HP number unique
3. Check method `on_update_after_submit` is implemented
4. Add debug logging in Python controller

### Issue 4: Portal access not working
**Symptoms:** Service Provider User can't access portal
**Possible Causes:**
- Portal settings not configured
- User doesn't have portal access enabled
- DocType not shared with portal users

**Solution:**
1. Check: Setup → Portal Settings
2. Check user has "Service Provider User" role
3. Check DocType permissions include portal role
4. Enable "Has Web View" in DocType settings if needed

---

## 14. Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-03 | Claude AI | Initial workflow implementation plan created |

---

**End of Document**

*Document Status: Ready for Implementation*
*Next Step: Begin Phase 1 - DocType Creation*
*Estimated Start Date: Upon approval*
*Estimated Completion: 4-5 working days*

---

## Notes for Implementation

1. **Use Frappe UI for DocType creation** - Faster and more reliable than programmatic creation
2. **Test incrementally** - Don't wait until everything is built to start testing
3. **Clear cache frequently** - After any DocType or workflow changes
4. **Use Git** - Commit after each phase completion
5. **Document issues** - Keep track of bugs and solutions for future reference
6. **Get stakeholder feedback early** - Show progress after Phase 2
7. **Portal testing** - Test portal access thoroughly with actual portal user
8. **Email testing** - Use test email addresses initially

**Good luck with implementation! 🚀**
