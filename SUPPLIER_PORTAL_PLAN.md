# Supplier Portal Implementation Plan

**Status**: Planning Complete - Ready for Implementation
**Created**: 2025-12-22
**Last Updated**: 2025-12-22

---

## Overview
Create a WebForm-based portal for suppliers to submit inquiries, track their processing status, view/edit their profile, and upload documents.

## User Requirements (Confirmed)
- **Purpose**: Handle both new provider applications and existing supplier inquiries
- **Features**: Submit/track inquiries, view/edit supplier profile, upload documents
- **Approach**: Frappe WebForms (built-in, RTL-ready)
- **Access**: Admin-created accounts (self-registration deferred to future)

## Current State
- **Supplier Inquiry DocType**: Fully implemented with 6-state workflow
- **Supplier DocType**: Master data exists
- **Missing**: Portal role, WebForms, portal permissions, portal pages, User↔Supplier link

---

## Implementation Phases

### Phase 1: Foundation - Roles & Permissions (2-3 hours)

#### 1.1 Create Portal Role
- [x] Create `/home/tzvi/frappe/doctypes_loading/creation/create_portal_roles.py`
- [x] Function: `create_portal_roles()` - creates "Supplier Portal User" role with `desk_access=0`
- [x] Run: `./run_doctype_script.sh creation.create_portal_roles.create_portal_roles`

#### 1.2 Link Users to Suppliers
- [x] Create `/home/tzvi/frappe/doctypes_loading/creation/add_supplier_link_to_user.py`
- [x] Function: `add_supplier_link_custom_field()` - adds "supplier_link" custom field to User DocType
- [x] Run: `./run_doctype_script.sh creation.add_supplier_link_to_user.add_supplier_link_custom_field`
- [x] Run: `bench --site development.localhost clear-cache`

#### 1.3 Update DocType Permissions (Automated via Script)
- [x] Create `/home/tzvi/frappe/doctypes_loading/creation/add_portal_permissions.py`
- [x] Function: `add_portal_permissions()` - adds permissions programmatically
- [x] Run: `./run_doctype_script.sh creation.add_portal_permissions.add_portal_permissions`
- [x] **Supplier Inquiry**: Added "Supplier Portal User" role with Read, Write, Create, Email, Print permissions + "If Owner" flag
- [x] **Supplier**: Added "Supplier Portal User" role with Read, Write permissions + "If Owner" flag

### Phase 2: Data Access Control (2-3 hours)

#### 2.1 Implement Supplier Inquiry Permissions
- [ ] Modify: `/home/tzvi/frappe/frappe_docker/development/frappe-bench/apps/siud/siud/siud/doctype/supplier_inquiry/supplier_inquiry.py`
- [ ] Add `has_website_permission(doc, ptype, user, verbose=False)` function
- [ ] Logic: Portal users only see inquiries where `doc.supplier_link == User.supplier_link`

#### 2.2 Implement Supplier Permissions
- [ ] Modify: `/home/tzvi/frappe/frappe_docker/development/frappe-bench/apps/siud/siud/siud/doctype/supplier/supplier.py`
- [ ] Add `has_website_permission(doc, ptype, user, verbose=False)` function
- [ ] Logic: Portal users only see their linked supplier record

### Phase 3: WebForm for Inquiries (3-4 hours)

#### 3.1 Create Supplier Inquiry WebForm
- [ ] **Option A**: Manual UI creation (recommended)
  - Navigate to: `/app/web-form/new`
  - Title: "פניית ספק", Route: "supplier-inquiry-form"
  - Published: ✓, Login Required: ✓, Apply Document Permissions: ✓
  - Fields: supplier_link (read-only), topic_category, inquiry_description, inquiry_context, attachments
  - Hide internal fields: inquiry_status, assigned_role, response_text, internal_notes
  - Client script: Auto-populate supplier_link from `frappe.session.user`
  - List settings: Show list, title "הפניות שלי", columns: name, topic_category, inquiry_status, creation

- [ ] **Option B**: Programmatic creation
  - Create `/home/tzvi/frappe/doctypes_loading/creation/create_supplier_inquiry_webform.py`
  - Function: `create_supplier_inquiry_webform()`
  - Run: `./run_doctype_script.sh creation.create_supplier_inquiry_webform.create_supplier_inquiry_webform`

### Phase 4: Portal Navigation & Dashboard (4-5 hours)

#### 4.1 Configure Portal Menu
- [ ] Modify: `/home/tzvi/frappe/frappe_docker/development/frappe-bench/apps/siud/siud/hooks.py`
- [ ] Add `standard_portal_menu_items` with 4 menu items:
  - דף הבית → /supplier-dashboard
  - הפניות שלי → /supplier-inquiry-form/list
  - פנייה חדשה → /supplier-inquiry-form/new
  - פרופיל הספק → /supplier-profile
- [ ] Add `role_home_page = {"Supplier Portal User": "supplier-dashboard"}`
- [ ] Run: `bench --site development.localhost clear-cache && bench restart`
- [ ] Sync via UI: Portal Settings → Sync Menu → Enable items → Save

#### 4.2 Create Portal Pages
Create in `/home/tzvi/frappe/frappe_docker/development/frappe-bench/apps/siud/siud/www/`:

- [ ] **supplier-dashboard.html** + **.py**
  - Display: Welcome message, inquiry statistics (total/open/closed), recent inquiries list
  - Quick actions: New inquiry button, View all inquiries link

- [ ] **supplier-profile.html** + **.py**
  - Display: Supplier details (ID read-only, name/phone/email/address editable)
  - Form with save via `frappe.client.set_value` API

- [ ] Run: `bench --site development.localhost clear-cache && bench build --app siud`

### Phase 5: Testing & User Setup (2-3 hours)

#### 5.1 Create Test Users
- [ ] **Option A**: Manual UI
  - Create Supplier record (e.g., SUP-001)
  - Create User → Email, Roles: "Supplier Portal User", Supplier Link: SUP-001
  - Set password

- [ ] **Option B**: Script
  - Create `/home/tzvi/frappe/doctypes_loading/test_data/create_portal_users.py`
  - Function: `create_test_portal_users()` - creates SUP-001 and supplier1@test.com
  - Run: `./run_doctype_script.sh test_data.create_portal_users.create_test_portal_users`

#### 5.2 Security Testing
- [ ] **Data Isolation**: User A cannot see User B's inquiries
- [ ] **Portal-Only Access**: Cannot access /app/doctype (desk)
- [ ] **Profile Editing**: Can edit profile, cannot change supplier_id
- [ ] **Inquiry Submission**: supplier_link auto-populated and read-only
- [ ] **List Filtering**: Only own inquiries visible

---

## Critical Files

1. `supplier_inquiry.py` - has_website_permission() for inquiry access control
2. `supplier.py` - has_website_permission() for profile access control
3. `hooks.py` - Portal menu configuration
4. `www/supplier-dashboard.py` - Portal landing page
5. `www/supplier-profile.py` - Profile management page

## Security Model

**4 Permission Layers:**
1. Role-based: "Supplier Portal User" role (desk_access=0)
2. DocType permissions: "If Owner" flag
3. Code-level: `has_website_permission()` validates User.supplier_link
4. Application: WebForm auto-sets supplier_link (read-only)

**Critical Rules:**
- Never trust client-side supplier_link input
- Always validate via User.supplier_link server-side
- Portal sessions isolated from desk sessions
- Hide internal fields from WebForms

## Future Enhancements (Post-MVP)
- Self-registration workflow with admin approval
- Document upload for compliance (insurance, licenses)
- Email notifications on status changes
- Advanced dashboard with charts
- Multi-user per supplier support

## Success Criteria
- [ ] Supplier logs in → sees supplier-dashboard (not desk)
- [ ] Can submit new inquiry → auto-linked to their supplier
- [ ] Can view only their inquiries → filtered list
- [ ] Can edit profile → changes saved
- [ ] Cannot see other suppliers' data → permission denied
- [ ] Hebrew RTL interface works correctly

---

## Progress Tracking

### Session Log

**Session 1** - 2025-12-22
- [x] Requirements gathering
- [x] Codebase exploration
- [x] Plan creation
- [x] Implementation starts in next session

**Session 2** - 2025-12-22
- [x] Phase 1 implementation (COMPLETED)
  - [x] Created portal role "Supplier Portal User" with desk_access=0
  - [x] Added supplier_link custom field to User DocType
  - [x] Added portal permissions to Supplier Inquiry and Supplier DocTypes
- [ ] Phase 2 implementation (Next)

**Session 3** - [Date]
- [ ] Phase 3 implementation
- [ ] Phase 4 implementation

**Session 4** - [Date]
- [ ] Phase 5 implementation
- [ ] Final testing

---

## Notes & Decisions

### Decision Log
- **WebForms over Custom Pages**: Chosen for faster implementation and built-in RTL support
- **Admin-Created Accounts**: Self-registration deferred to v2 for security simplicity
- **4-Layer Security**: Comprehensive approach ensures data isolation
- **Automated Permission Setup**: Created `add_portal_permissions.py` script to automate permission configuration instead of manual UI updates (more repeatable and version-controlled)

### Known Issues
- None yet

### Questions / Blockers
- None yet

---

**Next Steps**: Start with Phase 1 - Create portal role and user-supplier link
