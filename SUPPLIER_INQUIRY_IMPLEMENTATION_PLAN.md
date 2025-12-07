# Supplier Inquiry Management POC - Implementation Plan

**Project:** Supplier Inquiry Management System
**Framework:** Frappe Framework v15
**Environment:** Docker-based development
**Date Created:** 2025-12-07
**Status:** Planning Phase

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture Summary](#architecture-summary)
3. [Implementation Phases](#implementation-phases)
4. [DocType Specifications](#doctype-specifications)
5. [Implementation Tasks](#implementation-tasks)
6. [Validation & Business Rules](#validation--business-rules)
7. [Permissions & Security](#permissions--security)
8. [Testing Plan](#testing-plan)
9. [Success Criteria](#success-criteria)

---

## Overview

### Project Goal
Implement a Supplier Inquiry Management POC system in Frappe that allows:
- Suppliers to register and manage their profile
- Contact persons to submit and track inquiries
- Staff to process inquiries with role-based assignment
- Communication tracking and document management

### Key Features
- **Supplier Management:** Profile, activity domains, contact information
- **Contact Management:** Multiple contacts per supplier with role assignments
- **Inquiry System:** Categorized inquiries with rich text, attachments, and tracking
- **Role-Based Assignment:** Automatic routing based on inquiry topic and roles
- **Status Tracking:** Complete inquiry lifecycle management
- **Hebrew Interface:** Full RTL support with Hebrew labels

### Technical Approach
- Use `doctype_creator` tool for DocType generation from YAML specifications
- Container-based development workflow
- Iterative development with validation at each step

---

## Architecture Summary

### DocType Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                     MASTER DATA                              │
├─────────────────────────────────────────────────────────────┤
│ Role (תפקיד)                                                │
│ Activity Domain Category (קטגוריות תחומי פעילות)           │
│ Inquiry Topic Category (קטגוריות נושאי פנייה)              │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │
┌─────────────────────────────────────────────────────────────┐
│                    SUPPLIER ENTITIES                         │
├─────────────────────────────────────────────────────────────┤
│ Supplier (ספק)                                              │
│   ├─ Links to: Activity Domain Category (child table)      │
│   └─ Has many: Contact Person                              │
│                                                             │
│ Contact Person (איש קשר)                                    │
│   ├─ Links to: Supplier                                    │
│   ├─ Links to: Role (child table)                          │
│   └─ Has many: Supplier Inquiry                            │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │
┌─────────────────────────────────────────────────────────────┐
│                   TRANSACTION ENTITIES                       │
├─────────────────────────────────────────────────────────────┤
│ Supplier Inquiry (פניית ספק)                               │
│   ├─ Links to: Supplier                                    │
│   ├─ Links to: Inquiry Topic Category                      │
│   ├─ Links to: Role (assigned)                             │
│   └─ Links to: User (assigned employee)                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    CHILD TABLES                              │
├─────────────────────────────────────────────────────────────┤
│ Supplier Activity Domain (child of Supplier)                │
│ Contact Person Role (child of Contact Person)               │
└─────────────────────────────────────────────────────────────┘
```

### Relationships
- **Supplier** → many **Contact Persons** (1:N)
- **Supplier** → many **Activity Domains** via child table (1:N)
- **Contact Person** → one **Supplier** (N:1)
- **Contact Person** → many **Roles** via child table (N:N)
- **Supplier Inquiry** → one **Supplier** (N:1)
- **Supplier Inquiry** → one **Inquiry Topic Category** (N:1)
- **Supplier Inquiry** → one **Role** (assigned role) (N:1)
- **Supplier Inquiry** → one **User** (assigned employee) (N:1)

---

## Implementation Phases

### Phase 1: Master Data DocTypes (Foundation)
**Duration:** Day 1
**Goal:** Create lookup tables and reference data

**DocTypes:**
1. Role (תפקיד)
2. Activity Domain Category (קטגוריות תחומי פעילות)
3. Inquiry Topic Category (קטגוריות נושאי פנייה)

**Deliverables:**
- 3 YAML specifications
- 3 loaded DocTypes in Frappe
- Sample data for each

---

### Phase 2: Child Tables
**Duration:** Day 1-2
**Goal:** Create reusable child tables for multi-select relationships

**DocTypes:**
1. Supplier Activity Domain (child table)
2. Contact Person Role (child table)

**Deliverables:**
- 2 YAML specifications
- 2 loaded child table DocTypes

---

### Phase 3: Supplier Management
**Duration:** Day 2-3
**Goal:** Implement supplier registration and profile management

**DocTypes:**
1. Supplier (ספק)

**Deliverables:**
- YAML specification with child table integration
- Python controller with validations
- Sample supplier records
- Permission configuration

---

### Phase 4: Contact Person Management
**Duration:** Day 3-4
**Goal:** Implement contact person management with role assignments

**DocTypes:**
1. Contact Person (איש קשר)

**Deliverables:**
- YAML specification
- Python controller with supplier linking
- User creation workflow (if needed)
- Permission configuration

---

### Phase 5: Inquiry Management
**Duration:** Day 4-5
**Goal:** Implement core inquiry submission and tracking

**DocTypes:**
1. Supplier Inquiry (פניית ספק)

**Deliverables:**
- YAML specification with all fields
- Python controller with business logic
- Status workflow (Draft → Submitted → In Progress → Resolved/Closed)
- Auto-assignment logic
- Email notifications (basic)

---

### Phase 6: Business Logic & Validations
**Duration:** Day 5-6
**Goal:** Implement all business rules and validations

**Tasks:**
- Add validation rules to controllers
- Implement auto-assignment logic
- Add field dependencies (show/hide based on inquiry_context)
- Implement communication logging

---

### Phase 7: Testing & Refinement
**Duration:** Day 6-7
**Goal:** End-to-end testing and UI/UX improvements

**Tasks:**
- Create test scenarios
- Manual testing of all workflows
- UI improvements (list views, filters, search)
- Hebrew translation verification
- Performance testing

---

## DocType Specifications

### 1. Role (תפקיד)

**Purpose:** Define roles for handling different inquiry types

**YAML Location:** `doctype_creator/yaml_specs/role.yaml`

**Fields:**
| Field | Type | Label | Properties |
|-------|------|-------|------------|
| role_name | Data | שם תפקיד | Required, Unique, In List View |
| role_title_he | Data | כותרת בעברית | Required, In List View |
| description | Small Text | תיאור | Optional |

**Naming Rule:** By field (role_name)

**Sample Data:**
- `service` → שירות (נושאים מקצועיים)
- `complaints` → טיפול בתלונות
- `accounts` → טיפול חשבונות שוטפים
- `audit` → טיפול בקרות רו"ח

---

### 2. Activity Domain Category (קטגוריות תחומי פעילות)

**Purpose:** Categorize supplier activity domains

**YAML Location:** `doctype_creator/yaml_specs/activity_domain_category.yaml`

**Fields:**
| Field | Type | Label | Properties |
|-------|------|-------|------------|
| category_code | Data | קוד קטגוריה | Required, Unique, In List View |
| category_name | Data | שם קטגוריה | Required, In List View |
| description | Small Text | תיאור | Optional |

**Naming Rule:** By field (category_code)

**Sample Data:**
- `nursing_home` → טיפול סיעודי בבית
- `day_center` → מרכז יום
- `community` → קהילה תומכת
- `supplies` → מוצרי ספיגה

---

### 3. Inquiry Topic Category (קטגוריות נושאי פנייה)

**Purpose:** Hierarchical categorization of inquiry topics

**YAML Location:** `doctype_creator/yaml_specs/inquiry_topic_category.yaml`

**Fields:**
| Field | Type | Label | Properties |
|-------|------|-------|------------|
| category_code | Data | קוד קטגוריה | Required, Unique, In List View |
| category_name | Data | שם קטגוריה | Required, In List View |
| parent_category | Link → Inquiry Topic Category | קטגוריית אב | Optional |
| description | Small Text | תיאור | Optional |

**Naming Rule:** By field (category_code)

**Hierarchy:** Max 2 levels

**Sample Data:**
```
billing (חיובים)
  ├── billing_error (שגיאה בחיוב)
  └── payment_delay (עיכוב בתשלום)

service (שירות)
  ├── service_quality (איכות שירות)
  └── service_complaint (תלונה על שירות)
```

---

### 4. Supplier Activity Domain (Child Table)

**Purpose:** Link suppliers to their activity domains

**YAML Location:** `doctype_creator/yaml_specs/supplier_activity_domain.yaml`

**Fields:**
| Field | Type | Label | Properties |
|-------|------|-------|------------|
| activity_domain | Link → Activity Domain Category | תחום פעילות | Required, In List View |

**Naming Rule:** Auto (SUP-ACT-{#####})

**Is Child Table:** Yes

---

### 5. Contact Person Role (Child Table)

**Purpose:** Link contact persons to their roles

**YAML Location:** `doctype_creator/yaml_specs/contact_person_role.yaml`

**Fields:**
| Field | Type | Label | Properties |
|-------|------|-------|------------|
| role | Link → Role | תפקיד | Required, In List View |

**Naming Rule:** Auto (CNT-ROLE-{#####})

**Is Child Table:** Yes

---

### 6. Supplier (ספק)

**Purpose:** Main supplier entity with profile information

**YAML Location:** `doctype_creator/yaml_specs/supplier.yaml`

**Fields:**

| Field | Type | Label | Properties |
|-------|------|-------|------------|
| **Basic Information Section** ||||
| supplier_id | Data | מזהה ספק | Required, Unique, Read Only After Create |
| supplier_name | Data | שם ספק | Required, In List View |
| address | Text | כתובת | Optional |
| phone | Data (Phone) | טלפון | Required |
| email | Data (Email) | כתובת דוא"ל | Required |
| **Activity Domains Section** ||||
| activity_domains | Table → Supplier Activity Domain | תחומי פעילות | Optional |
| **Metadata Section** ||||
| creation_date | Date | תאריך רישום | Read Only, Default: Today |

**Naming Rule:** Auto (SUP-{#####})

**Track Changes:** Yes

**Controller Logic:**
- Validate phone format
- Validate email format
- Ensure supplier_id is unique
- Auto-set creation_date on insert

---

### 7. Contact Person (איש קשר)

**Purpose:** Contact persons associated with suppliers

**YAML Location:** `doctype_creator/yaml_specs/contact_person.yaml`

**Fields:**

| Field | Type | Label | Properties |
|-------|------|-------|------------|
| **Basic Information Section** ||||
| contact_name | Data | שם איש קשר | Required, In List View |
| email | Data (Email) | כתובת דוא"ל | Required |
| mobile_phone | Data (Phone) | טלפון נייד | Required |
| **Supplier Association Section** ||||
| supplier_link | Link → Supplier | שיוך לספק | Required, In List View |
| branch | Data | סניף | Optional |
| **Role Assignment Section** ||||
| primary_role_type | Select | תפקיד ראשי | Required, Options: "ספק\nאיש קשר של ספק" |
| assigned_roles | Table → Contact Person Role | רשימת תפקידים משויכים | Optional |
| **User Account Section** ||||
| user | Link → User | משתמש מערכת | Optional (for portal access) |

**Naming Rule:** Auto (CNT-{#####})

**Track Changes:** Yes

**Controller Logic:**
- Validate supplier exists
- Auto-create User if needed (for portal access)
- Validate at least one role assigned
- Email uniqueness check

---

### 8. Supplier Inquiry (פניית ספק)

**Purpose:** Inquiry/ticket management for supplier communications

**YAML Location:** `doctype_creator/yaml_specs/supplier_inquiry.yaml`

**Fields:**

| Field | Type | Label | Properties |
|-------|------|-------|------------|
| **Inquiry Information Section** ||||
| supplier_link | Link → Supplier | מזהה ספק | Required, In List View |
| topic_category | Link → Inquiry Topic Category | קטגורית נושא פנייה | Required, In List View |
| inquiry_description | Text Editor | תיאור הפנייה | Required |
| **Context Section** ||||
| inquiry_context | Select | הקשר הפנייה | Required, Options: "ספק עצמו\nמבוטח", Default: "ספק עצמו" |
| insured_id_number | Data | מספר זהות של המבוטח | Depends on: inquiry_context = "מבוטח", Length: 9 |
| insured_full_name | Data | שם מלא של המבוטח | Depends on: inquiry_context = "מבוטח" |
| **Attachments Section** ||||
| attachments | Attach | קבצים מצורפים | Optional, Multiple files allowed |
| **Status & Assignment Section** ||||
| inquiry_status | Select | סטטוס פנייה | Required, Options: "טיוטה\nהוגשה\nבטיפול\nממתין למידע\nנפתרה\nנסגרה", Default: "טיוטה", In List View |
| assigned_role | Link → Role | שיוך לתפקיד מטפל בפניה | Optional, In List View |
| assigned_employee_id | Link → User | מזהה הפקיד שמטפל בפנייה | Optional |
| **Response Section** ||||
| response_text | Text Editor | המענה לפנייה - מלל | Optional |
| response_attachments | Attach | המענה לפנייה - קבצים | Optional |
| **Metadata Section** ||||
| submission_date | Datetime | תאריך הגשה | Read Only, Auto-set on status = "הוגשה" |
| resolution_date | Datetime | תאריך פתרון | Read Only, Auto-set on status = "נפתרה" |

**Naming Rule:** Auto (INQ-{#####})

**Is Submittable:** Yes (Draft → Submitted)

**Track Changes:** Yes

**Controller Logic:**
- Validate insured_id_number when inquiry_context = "מבוטח" (9 digits)
- Auto-assign role based on topic_category (if mapping exists)
- Auto-set submission_date when status changes to "הוגשה"
- Auto-set resolution_date when status changes to "נפתרה"
- Prevent editing certain fields after submission
- Email notification to assigned_employee_id on assignment
- Status transition validation

---

## Implementation Tasks

### Task Checklist

#### Phase 1: Master Data (Day 1)

- [ ] **Task 1.1:** Create Role DocType
  - [ ] Write YAML specification (`yaml_specs/role.yaml`)
  - [ ] Validate YAML: `python validate_yaml.py yaml_specs/role.yaml`
  - [ ] Load DocType: `./scripts/load.sh yaml_specs/role.yaml`
  - [ ] Create sample data (5-10 roles)
  - [ ] Test in UI

- [ ] **Task 1.2:** Create Activity Domain Category DocType
  - [ ] Write YAML specification (`yaml_specs/activity_domain_category.yaml`)
  - [ ] Validate YAML
  - [ ] Load DocType
  - [ ] Create sample data (5-10 categories)
  - [ ] Test in UI

- [ ] **Task 1.3:** Create Inquiry Topic Category DocType
  - [ ] Write YAML specification (`yaml_specs/inquiry_topic_category.yaml`)
  - [ ] Validate YAML
  - [ ] Load DocType
  - [ ] Create sample hierarchical data (2 levels)
  - [ ] Test parent-child relationships in UI

#### Phase 2: Child Tables (Day 1-2)

- [ ] **Task 2.1:** Create Supplier Activity Domain Child Table
  - [ ] Write YAML specification (`yaml_specs/supplier_activity_domain.yaml`)
  - [ ] Set `is_child_table: true`
  - [ ] Validate YAML
  - [ ] Load DocType

- [ ] **Task 2.2:** Create Contact Person Role Child Table
  - [ ] Write YAML specification (`yaml_specs/contact_person_role.yaml`)
  - [ ] Set `is_child_table: true`
  - [ ] Validate YAML
  - [ ] Load DocType

#### Phase 3: Supplier Management (Day 2-3)

- [ ] **Task 3.1:** Create Supplier DocType
  - [ ] Write YAML specification (`yaml_specs/supplier.yaml`)
  - [ ] Include child table reference for activity_domains
  - [ ] Validate YAML
  - [ ] Load DocType

- [ ] **Task 3.2:** Create Supplier Python Controller
  - [ ] Create `controllers/supplier.py`
  - [ ] Implement field validations (phone, email, supplier_id)
  - [ ] Implement auto-set creation_date
  - [ ] Inject controller: `./scripts/inject.sh "Supplier" controllers/supplier.py`
  - [ ] Test validations

- [ ] **Task 3.3:** Configure Supplier Permissions
  - [ ] System Manager: full access
  - [ ] Supplier User: read own records only
  - [ ] Test permission rules

- [ ] **Task 3.4:** Create Sample Suppliers
  - [ ] Create 3-5 test suppliers with various activity domains
  - [ ] Test child table functionality

#### Phase 4: Contact Person Management (Day 3-4)

- [ ] **Task 4.1:** Create Contact Person DocType
  - [ ] Write YAML specification (`yaml_specs/contact_person.yaml`)
  - [ ] Include link to Supplier
  - [ ] Include child table for roles
  - [ ] Validate YAML
  - [ ] Load DocType

- [ ] **Task 4.2:** Create Contact Person Python Controller
  - [ ] Create `controllers/contact_person.py`
  - [ ] Implement supplier validation
  - [ ] Implement email uniqueness check
  - [ ] Optional: Auto-create User for portal access
  - [ ] Inject controller
  - [ ] Test validations

- [ ] **Task 4.3:** Configure Contact Person Permissions
  - [ ] System Manager: full access
  - [ ] Supplier User: read/write own supplier's contacts
  - [ ] Contact User: read/write own record

- [ ] **Task 4.4:** Create Sample Contact Persons
  - [ ] Create 2-3 contacts per sample supplier
  - [ ] Assign various roles
  - [ ] Test role assignment functionality

#### Phase 5: Inquiry Management (Day 4-5)

- [ ] **Task 5.1:** Create Supplier Inquiry DocType
  - [ ] Write YAML specification (`yaml_specs/supplier_inquiry.yaml`)
  - [ ] Include all fields with proper dependencies
  - [ ] Set is_submittable: true
  - [ ] Validate YAML
  - [ ] Load DocType

- [ ] **Task 5.2:** Create Supplier Inquiry Python Controller
  - [ ] Create `controllers/supplier_inquiry.py`
  - [ ] Implement insured_id_number validation (9 digits, only when context = "מבוטח")
  - [ ] Implement auto-assignment logic based on topic_category
  - [ ] Implement auto-set dates (submission_date, resolution_date)
  - [ ] Implement status transition validations
  - [ ] Inject controller
  - [ ] Test all validations

- [ ] **Task 5.3:** Configure Inquiry Status Workflow
  - [ ] Define allowed status transitions:
    - טיוטה → הוגשה
    - הוגשה → בטיפול
    - בטיפול → ממתין למידע
    - בטיפול → נפתרה
    - ממתין למידע → בטיפול
    - נפתרה → נסגרה
  - [ ] Implement in controller
  - [ ] Test all transitions

- [ ] **Task 5.4:** Configure Inquiry Permissions
  - [ ] Supplier User: create, read own inquiries
  - [ ] Staff User: read all, write assigned inquiries
  - [ ] Manager: full access

- [ ] **Task 5.5:** Create Sample Inquiries
  - [ ] Create inquiries with different contexts
  - [ ] Test supplier context inquiries
  - [ ] Test insured context inquiries
  - [ ] Test file attachments
  - [ ] Test status transitions

#### Phase 6: Business Logic & Notifications (Day 5-6)

- [ ] **Task 6.1:** Implement Auto-Assignment Logic
  - [ ] Create mapping: Inquiry Topic Category → Role
  - [ ] Update Supplier Inquiry controller to auto-assign role
  - [ ] Optional: Auto-assign to specific employee based on workload
  - [ ] Test auto-assignment

- [ ] **Task 6.2:** Configure Email Notifications
  - [ ] Email on inquiry submission (to assigned role/employee)
  - [ ] Email on status change (to supplier contact)
  - [ ] Email on inquiry resolution (to supplier contact)
  - [ ] Test email sending

- [ ] **Task 6.3:** Field Dependencies & Show/Hide Logic
  - [ ] Hide insured fields when inquiry_context = "ספק עצמו"
  - [ ] Show insured fields when inquiry_context = "מבוטח"
  - [ ] Test in UI

- [ ] **Task 6.4:** Communication Logging (Optional)
  - [ ] Use Frappe's built-in Communication/Activity Feed
  - [ ] Or create Communication Log child table in Supplier
  - [ ] Test communication tracking

#### Phase 7: Testing & Refinement (Day 6-7)

- [ ] **Task 7.1:** End-to-End Testing
  - [ ] Test complete supplier registration flow
  - [ ] Test contact person creation and role assignment
  - [ ] Test inquiry submission from portal user perspective
  - [ ] Test inquiry assignment and processing from staff perspective
  - [ ] Test all status transitions
  - [ ] Test file attachments (upload/download)
  - [ ] Test email notifications

- [ ] **Task 7.2:** UI/UX Improvements
  - [ ] Configure list views (fields, filters, sorting)
  - [ ] Add standard filters (by status, by supplier, by date)
  - [ ] Configure search fields
  - [ ] Test Hebrew RTL rendering
  - [ ] Add helpful descriptions to fields

- [ ] **Task 7.3:** Performance Testing
  - [ ] Create 50+ suppliers
  - [ ] Create 100+ inquiries
  - [ ] Test list view performance
  - [ ] Test search performance
  - [ ] Add database indexes if needed

- [ ] **Task 7.4:** Documentation
  - [ ] Document all DocTypes
  - [ ] Create user guide for supplier portal
  - [ ] Create user guide for staff
  - [ ] Document business rules and validations

---

## Validation & Business Rules

### Supplier (ספק)

**Validations:**
1. `supplier_id` must be unique
2. `phone` must be valid phone format
3. `email` must be valid email format
4. `supplier_name` is required

**Business Rules:**
1. `supplier_id` becomes read-only after creation
2. `creation_date` auto-set on insert
3. At least one activity domain recommended (warning if none)

### Contact Person (איש קשר)

**Validations:**
1. `supplier_link` must exist
2. `email` must be unique across all contact persons
3. At least one role must be assigned

**Business Rules:**
1. Email and mobile_phone can be updated by contact themselves
2. Auto-create User record for portal access if email provided

### Supplier Inquiry (פניית ספק)

**Validations:**
1. `insured_id_number` must be exactly 9 digits (only when inquiry_context = "מבוטח")
2. `insured_full_name` required when inquiry_context = "מבוטח"
3. Status transitions must follow allowed workflow

**Business Rules:**
1. `submission_date` auto-set when status changes to "הוגשה"
2. `resolution_date` auto-set when status changes to "נפתרה"
3. Auto-assign `assigned_role` based on `topic_category`
4. Send email notification on assignment
5. Prevent editing `supplier_link` and `topic_category` after submission
6. Allow response only when status is "בטיפול" or "ממתין למידע"

**Status Workflow:**
```
טיוטה (Draft)
  ↓
הוגשה (Submitted)
  ↓
בטיפול (In Progress) ←→ ממתין למידע (Waiting for Info)
  ↓
נפתרה (Resolved)
  ↓
נסגרה (Closed)
```

---

## Permissions & Security

### Role Definitions

**System Manager:**
- Full access to all DocTypes
- Can create, read, update, delete all records

**Supplier User (Portal User):**
- Can create and edit own Supplier record
- Can create and edit Contact Persons for own supplier
- Can create and read own Supplier Inquiries
- Cannot delete records

**Contact Person User (Portal User):**
- Can edit own Contact Person record (email, phone only)
- Can create Supplier Inquiries
- Can read own submitted inquiries
- Cannot access other suppliers' data

**Staff User (Internal):**
- Can read all Supplier records
- Can read all Contact Person records
- Can read all Supplier Inquiries
- Can write/update inquiries assigned to them
- Cannot delete inquiries

**Manager (Internal):**
- Full read access to all records
- Can reassign inquiries
- Can override status changes
- Can delete records if needed

### Permission Matrix

| DocType | System Manager | Supplier User | Contact Person User | Staff User | Manager |
|---------|----------------|---------------|---------------------|------------|---------|
| **Role** | CRUD | R | R | R | R |
| **Activity Domain Category** | CRUD | R | R | R | R |
| **Inquiry Topic Category** | CRUD | R | R | R | R |
| **Supplier** | CRUD | RU (own) | R (own supplier) | R | RU |
| **Contact Person** | CRUD | CRU (own supplier) | RU (self only) | R | RU |
| **Supplier Inquiry** | CRUD | CR (own) | CR (own) | RU (assigned) | CRUD |

**Legend:** C=Create, R=Read, U=Update, D=Delete

### Data Access Rules

1. **Supplier User** sees only their own supplier data
2. **Contact Person User** sees only their own contact data and supplier data
3. **Staff User** sees all data but can only modify assigned inquiries
4. **Manager** sees and modifies all data

---

## Testing Plan

### Unit Testing (Per DocType)

#### Role
- [ ] Create role with valid data
- [ ] Validate unique role_name
- [ ] Update role_title_he
- [ ] Cannot create duplicate role_name

#### Activity Domain Category
- [ ] Create category with valid data
- [ ] Validate unique category_code
- [ ] Cannot create duplicate category_code

#### Inquiry Topic Category
- [ ] Create top-level category (no parent)
- [ ] Create child category (with parent)
- [ ] Validate max 2-level hierarchy
- [ ] Cannot create 3rd level
- [ ] Parent-child relationship works correctly

#### Supplier
- [ ] Create supplier with all required fields
- [ ] Validate phone format
- [ ] Validate email format
- [ ] Add activity domains (child table)
- [ ] Update supplier details
- [ ] supplier_id is read-only after creation
- [ ] creation_date auto-set

#### Contact Person
- [ ] Create contact linked to supplier
- [ ] Validate email uniqueness
- [ ] Add multiple roles (child table)
- [ ] Cannot link to non-existent supplier
- [ ] Update contact email and phone

#### Supplier Inquiry
- [ ] Create inquiry with context = "ספק עצמו"
- [ ] Create inquiry with context = "מבוטח"
- [ ] Validate insured_id_number (9 digits) when context = "מבוטח"
- [ ] insured fields required when context = "מבוטח"
- [ ] Upload attachments
- [ ] Status transitions work correctly
- [ ] submission_date auto-set on status = "הוגשה"
- [ ] resolution_date auto-set on status = "נפתרה"
- [ ] Auto-assignment of role works
- [ ] Cannot edit after submission (certain fields)

### Integration Testing

#### Workflow 1: Supplier Registration
1. System Admin creates Supplier record
2. Add activity domains
3. Create Contact Person for supplier
4. Assign roles to contact
5. Verify contact can login (if portal enabled)

#### Workflow 2: Inquiry Submission (Supplier Context)
1. Contact Person logs in
2. Creates new Supplier Inquiry
3. Sets context = "ספק עצמו"
4. Fills description, uploads attachment
5. Submits inquiry (status → "הוגשה")
6. Verify submission_date set
7. Verify assigned_role set (if auto-assignment enabled)

#### Workflow 3: Inquiry Submission (Insured Context)
1. Contact Person creates inquiry
2. Sets context = "מבוטח"
3. Fills insured_id_number (9 digits)
4. Fills insured_full_name
5. Submits inquiry
6. Verify all insured fields saved correctly

#### Workflow 4: Inquiry Processing
1. Staff User views assigned inquiries
2. Opens inquiry, changes status to "בטיפול"
3. Adds response_text
4. Uploads response_attachments
5. Changes status to "נפתרה"
6. Verify resolution_date set
7. Verify email sent to contact

#### Workflow 5: Inquiry Lifecycle
1. Create inquiry (טיוטה)
2. Submit inquiry (הוגשה)
3. Start processing (בטיפול)
4. Request info (ממתין למידע)
5. Resume processing (בטיפול)
6. Resolve (נפתרה)
7. Close (נסגרה)
8. Verify all status transitions work
9. Verify dates recorded correctly

### Performance Testing

- [ ] Create 100 suppliers
- [ ] Create 500 contact persons
- [ ] Create 1000 inquiries
- [ ] Test list view load time (<2 seconds)
- [ ] Test search performance (<1 second)
- [ ] Test filter performance (<1 second)

### UI/UX Testing

- [ ] All Hebrew labels display correctly
- [ ] RTL layout works properly
- [ ] Field dependencies work (show/hide)
- [ ] Required field validations work
- [ ] Error messages in Hebrew
- [ ] List views show relevant columns
- [ ] Filters work correctly
- [ ] Search finds records correctly

---

## Success Criteria

### Functional Requirements

✅ **Supplier Management**
- [ ] Suppliers can be created with profile information
- [ ] Activity domains can be assigned to suppliers
- [ ] Supplier records can be updated

✅ **Contact Management**
- [ ] Contact persons can be linked to suppliers
- [ ] Multiple roles can be assigned to contacts
- [ ] Contact persons can update their own info

✅ **Inquiry Management**
- [ ] Inquiries can be created with both contexts (supplier/insured)
- [ ] Rich text editor works for descriptions
- [ ] File attachments can be uploaded and downloaded
- [ ] Status workflow functions correctly
- [ ] Inquiries can be assigned to roles/employees
- [ ] Responses can be added by staff

### Technical Requirements

✅ **Data Integrity**
- [ ] All relationships (links) work correctly
- [ ] Child tables function properly
- [ ] Data validations prevent invalid data
- [ ] Unique constraints enforced

✅ **Security**
- [ ] Role-based permissions work correctly
- [ ] Supplier users see only their own data
- [ ] Staff users can only modify assigned inquiries
- [ ] Data access rules enforced

✅ **Usability**
- [ ] Hebrew interface works correctly (RTL)
- [ ] All labels translated to Hebrew
- [ ] Error messages are clear and in Hebrew
- [ ] UI is intuitive and easy to use

✅ **Performance**
- [ ] List views load in <2 seconds
- [ ] Search responds in <1 second
- [ ] System handles 1000+ inquiries without issues

### Process Requirements

✅ **Inquiry Lifecycle**
- [ ] Complete inquiry lifecycle can be tracked
- [ ] Status transitions are logical and enforced
- [ ] Dates are automatically recorded
- [ ] Email notifications sent at appropriate times

✅ **Reporting & Communication**
- [ ] Communication history is tracked
- [ ] Activity feed shows inquiry updates
- [ ] Notifications work correctly

---

## Development Workflow

### Daily Workflow

1. **Morning:** Review tasks for the day
2. **Create YAML:** Write DocType specification
3. **Validate:** `python validate_yaml.py yaml_specs/<file>.yaml`
4. **Load:** `./scripts/load.sh yaml_specs/<file>.yaml`
5. **Test in UI:** Create sample records, verify fields
6. **Create Controller (if needed):** Write Python controller
7. **Inject Controller:** `./scripts/inject.sh "<DocType>" controllers/<file>.py`
8. **Clear Cache:** Inside container: `bench --site development.localhost clear-cache`
9. **Test Validations:** Create records that should pass/fail
10. **Document:** Update this plan with progress

### Container Commands Reference

**Enter container:**
```bash
docker exec -it frappe_docker_devcontainer-frappe-1 bash
```

**Inside container:**
```bash
cd /workspace/development/frappe-bench

# Clear cache
bench --site development.localhost clear-cache

# Migrate (after schema changes)
bench --site development.localhost migrate

# Console (Python shell)
bench --site development.localhost console

# Restart bench
bench restart
```

**From host:**
```bash
# Validate YAML
python validate_yaml.py yaml_specs/<file>.yaml

# Load DocType
./scripts/load.sh yaml_specs/<file>.yaml

# Inject controller
./scripts/inject.sh "<DocType Name>" controllers/<file>.py
```

---

## Progress Tracking

### Phase Completion

- [ ] **Phase 1:** Master Data DocTypes (3/3 DocTypes)
- [ ] **Phase 2:** Child Tables (2/2 DocTypes)
- [ ] **Phase 3:** Supplier Management (1/1 DocType + Controller)
- [ ] **Phase 4:** Contact Person Management (1/1 DocType + Controller)
- [ ] **Phase 5:** Inquiry Management (1/1 DocType + Controller)
- [ ] **Phase 6:** Business Logic & Validations
- [ ] **Phase 7:** Testing & Refinement

### Overall Progress: 0% Complete

---

## Notes & Decisions

### Design Decisions

1. **Use child tables for multi-select relationships** (activity domains, roles) rather than separate link DocTypes
2. **Use auto-naming** (SUP-{#####}, INQ-{#####}) for cleaner URLs and references
3. **Make Supplier Inquiry submittable** to enforce draft/submitted workflow
4. **Use Hebrew labels** everywhere for authentic user experience
5. **Use Frappe's built-in Communication** for activity tracking (rather than custom child table)

### Open Questions

1. **User creation:** Auto-create User records for contact persons, or manual process?
   - **Decision:** Manual for POC, can automate later

2. **Email notifications:** Use Frappe Email Alerts or custom Python?
   - **Decision:** Start with Frappe Email Alerts (UI-based), add custom logic if needed

3. **Role-topic mapping:** How to map Inquiry Topic Categories to Roles?
   - **Decision:** Add custom field in Inquiry Topic Category for default_role

4. **Document management:** Add Document DocType or use Attach fields?
   - **Decision:** Use Attach fields for POC, separate Document DocType for Phase 2

### Future Enhancements (Out of Scope for POC)

- [ ] Document expiry tracking and alerts
- [ ] Advanced communication logging with call records
- [ ] Supplier rating/evaluation system
- [ ] SLA tracking for inquiry resolution
- [ ] Dashboard with inquiry metrics
- [ ] Mobile app for suppliers
- [ ] WhatsApp integration for notifications
- [ ] Advanced search with full-text indexing

---

## Appendix

### YAML File Naming Convention

- Use snake_case for file names
- Match DocType name (with underscores)
- Examples:
  - `role.yaml`
  - `activity_domain_category.yaml`
  - `supplier_inquiry.yaml`

### Controller File Naming Convention

- Use snake_case for file names
- Match DocType name (with underscores)
- Class name should be PascalCase (from DocType name)
- Examples:
  - File: `supplier.py` → Class: `Supplier`
  - File: `contact_person.py` → Class: `ContactPerson`
  - File: `supplier_inquiry.py` → Class: `SupplierInquiry`

### Reference Links

- Frappe DocType Guide: https://frappeframework.com/docs/user/en/basics/doctypes
- Frappe Field Types: https://frappeframework.com/docs/user/en/basics/doctypes/field-types
- Frappe Controller Hooks: https://frappeframework.com/docs/user/en/api/document

---

**End of Implementation Plan**

**Next Steps:**
1. Review this plan
2. Start Phase 1: Create master data DocTypes
3. Update progress as tasks are completed
4. Document any issues or deviations in "Notes & Decisions" section
