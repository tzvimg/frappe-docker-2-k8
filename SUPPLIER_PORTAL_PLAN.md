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

### Phase 2: Data Access Control (2-3 hours) ✅ COMPLETED

#### 2.1 Implement Supplier Inquiry Permissions
- [x] Modify: `/home/tzvi/frappe/frappe_docker/development/frappe-bench/apps/siud/siud/siud/doctype/supplier_inquiry/supplier_inquiry.py`
- [x] Add `has_website_permission(doc, ptype, user, verbose=False)` function
- [x] Logic: Portal users only see inquiries where `doc.supplier_link == User.supplier_link`

#### 2.2 Implement Supplier Permissions
- [x] Modify: `/home/tzvi/frappe/frappe_docker/development/frappe-bench/apps/siud/siud/siud/doctype/supplier/supplier.py`
- [x] Add `has_website_permission(doc, ptype, user, verbose=False)` function
- [x] Logic: Portal users only see their linked supplier record

### Phase 3: WebForm for Inquiries (3-4 hours) ✅ COMPLETED

#### 3.1 Create Supplier Inquiry WebForm
- [x] **Option B**: Programmatic creation (COMPLETED)
  - Created `/home/tzvi/frappe/doctypes_loading/creation/create_supplier_inquiry_webform.py`
  - Function: `create_supplier_inquiry_webform()`
  - Run: `./run_doctype_script.sh creation.create_supplier_inquiry_webform.create_supplier_inquiry_webform`
  - WebForm Details:
    - Title: "פניית ספק"
    - Route: `/supplier-inquiry-form`
    - Published: ✓, Login Required: ✓, Apply Document Permissions: ✓
    - Fields included: supplier_link (read-only), topic_category, inquiry_description, inquiry_context, insured_id_number, insured_full_name, attachments
    - Internal fields hidden: inquiry_status, assigned_role, assigned_employee_id, response_text, response_attachments
    - Client script added: Auto-populates supplier_link from User.supplier_link
    - List settings: Shows list with title "הפניות שלי", columns: name, topic_category, inquiry_status, creation
    - Success message and introduction text in Hebrew

### Phase 4: Portal Navigation & Dashboard (4-5 hours) ✅ COMPLETED

#### 4.1 Configure Portal Menu
- [x] Modify: `/home/tzvi/frappe/frappe_docker/development/frappe-bench/apps/siud/siud/hooks.py`
- [x] Add `standard_portal_menu_items` with 4 menu items:
  - דף הבית → /supplier-dashboard
  - הפניות שלי → /supplier-inquiry-form/list
  - פנייה חדשה → /supplier-inquiry-form/new
  - פרופיל הספק → /supplier-profile
- [x] Add `role_home_page = {"Supplier Portal User": "supplier-dashboard"}`
- [x] Run: `bench --site development.localhost clear-cache && bench build --app siud`
- [ ] Sync via UI: Portal Settings → Sync Menu → Enable items → Save (Manual step for user)

#### 4.2 Create Portal Pages
Create in `/home/tzvi/frappe/frappe_docker/development/frappe-bench/apps/siud/siud/www/`:

- [x] **supplier-dashboard.html** + **.py**
  - Display: Welcome message, inquiry statistics (total/open/closed), recent inquiries list
  - Quick actions: New inquiry button, View all inquiries link
  - Implementation: Python backend fetches supplier data and inquiry stats; HTML template displays dashboard with RTL Hebrew UI

- [x] **supplier-profile.html** + **.py**
  - Display: Supplier details (ID read-only, name/phone/email/address editable)
  - Form with save via AJAX call to server-side `update_supplier_profile()` function
  - Implementation: Includes form validation, loading spinner, success/error alerts, and security checks

- [x] Run: `bench --site development.localhost clear-cache && bench build --app siud`

### Phase 5: Testing & User Setup (2-3 hours) ✅ COMPLETED

#### 5.1 Create Test Users
- [x] **Option B**: Script (COMPLETED)
  - [x] Created `/home/tzvi/frappe/doctypes_loading/test_data/create_portal_users.py`
  - [x] Function: `create_test_portal_users()` - creates SUP-TEST-001, SUP-TEST-002 and portal users
  - [x] Run: `./run_doctype_script.sh test_data.create_portal_users.create_test_portal_users`
  - [x] Test users created:
    - supplier1@test.com (password: Test@1234) → SUP-TEST-001
    - supplier2@test.com (password: Test@1234) → SUP-TEST-002
  - [x] Sample inquiries created: SI-00026, SI-00027, SI-00028, SI-00029

#### 5.2 Security Testing
Testing documentation created at `/home/tzvi/frappe/SUPPLIER_PORTAL_TESTING.md`

Manual testing checklist (to be performed by user):
- [ ] **Portal Landing Page**: Supplier logs in → sees supplier-dashboard (not desk)
- [ ] **Data Isolation**: User A cannot see User B's inquiries
- [ ] **Portal-Only Access**: Cannot access /app/doctype (desk)
- [ ] **Profile Editing**: Can edit profile, cannot change supplier_id
- [ ] **Inquiry Submission**: supplier_link auto-populated and read-only
- [ ] **List Filtering**: Only own inquiries visible
- [ ] **Hebrew RTL**: Interface displays correctly in RTL Hebrew

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
**Implementation Complete - Manual testing required**

Test credentials and checklist available at `/home/tzvi/frappe/SUPPLIER_PORTAL_TESTING.md`

- [ ] Supplier logs in → sees supplier-dashboard (not desk)
- [ ] Can submit new inquiry → auto-linked to their supplier
- [ ] Can view only their inquiries → filtered list
- [ ] Can edit profile → changes saved
- [ ] Cannot see other suppliers' data → permission denied
- [ ] Hebrew RTL interface works correctly

**Status**: Ready for manual testing with test users (supplier1@test.com / supplier2@test.com)

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
- [x] Phase 2 implementation (COMPLETED)
  - [x] Implemented has_website_permission() in Supplier Inquiry controller
  - [x] Implemented has_website_permission() in Supplier controller
  - [x] Data access control ensures users only see their own supplier data

**Session 3** - 2025-12-22
- [x] Phase 3 implementation (COMPLETED)
  - [x] Created webform creation script at `/home/tzvi/frappe/doctypes_loading/creation/create_supplier_inquiry_webform.py`
  - [x] Executed script successfully: WebForm "פניית-ספק" created
  - [x] Auto-populate client script added for supplier_link field
  - [x] WebForm configured with Hebrew labels, introduction text, and success message
  - [x] Applied document permissions for data isolation
  - [x] List view configured to show inquiry history
- [x] Phase 4 implementation (COMPLETED)
  - [x] Modified hooks.py to add portal menu configuration
  - [x] Created role_home_page setting for "Supplier Portal User" → supplier-dashboard
  - [x] Created supplier-dashboard.py with inquiry statistics logic (total/open/closed counts, recent inquiries)
  - [x] Created supplier-dashboard.html with RTL Hebrew UI, statistics cards, and quick action buttons
  - [x] Created supplier-profile.py with profile data retrieval and update_supplier_profile() function
  - [x] Created supplier-profile.html with editable form, AJAX save, validation, and security checks
  - [x] Cleared cache and built app successfully

**Session 4** - 2025-12-22
- [x] Phase 5 implementation (COMPLETED)
  - [x] Created test user creation script at `/home/tzvi/frappe/doctypes_loading/test_data/create_portal_users.py`
  - [x] Executed script successfully: Created 2 test suppliers (SUP-TEST-001, SUP-TEST-002)
  - [x] Created 2 portal users (supplier1@test.com, supplier2@test.com) with password: Test@1234
  - [x] Created 4 sample inquiries (2 per supplier)
  - [x] Created comprehensive testing documentation at `/home/tzvi/frappe/SUPPLIER_PORTAL_TESTING.md`
  - [x] Testing checklist includes: Portal access, data isolation, profile editing, inquiry submission, desk restriction, cross-supplier access, RTL interface
- [ ] Manual testing (to be performed by user)

**Session 5** - 2025-12-24
- [x] Bug fix: Dashboard inquiry links not working
  - [x] Identified issue: WebForm had `allow_edit=0`, preventing viewing of individual inquiries
  - [x] Created `/home/tzvi/frappe/doctypes_loading/creation/enable_webform_edit.py` script
  - [x] Enabled `allow_edit=1` on "פניית-ספק" WebForm
  - [x] Cleared cache to apply changes
  - [x] Dashboard links to `/supplier-inquiry-form/{{ inquiry.name }}` now work correctly
  - [x] Suppliers can now view and edit their existing inquiries from the dashboard
- [x] Bug fix: "Not permitted" error when viewing inquiries
  - [x] Identified root cause: "If Owner" flag on permissions prevented access (inquiries owned by Administrator)
  - [x] Created diagnostic script `/home/tzvi/frappe/doctypes_loading/temp/check_inquiry_permissions.py`
  - [x] Verified that `has_website_permission()` function works correctly
  - [x] Created `/home/tzvi/frappe/doctypes_loading/creation/fix_portal_permissions.py` to fix Supplier Inquiry permissions
  - [x] Created `/home/tzvi/frappe/doctypes_loading/creation/fix_supplier_permissions.py` to fix Supplier permissions
  - [x] Removed "If Owner" flag from both DocTypes (replaced with `if_owner=0`)
  - [x] Security now properly handled by `has_website_permission()` checking supplier_link
  - [x] Cleared cache to apply permission changes
  - [x] Portal users can now view their inquiries regardless of who created them
- [x] Bug fix: WebForm list showing all inquiries instead of filtered by supplier
  - [x] Identified issue: WebForm list view wasn't applying supplier-based filtering
  - [x] Added `get_list_context()` function to `supplier_inquiry.py` controller
  - [x] Function filters list by current user's `supplier_link` field
  - [x] Cleared cache to apply changes
  - [x] WebForm list at `/supplier-inquiry-form/list` now shows only supplier's inquiries
- [x] Bug fix: Grid headers showing "undefined" in list view
  - [x] Identified issue: WebForm list columns had no labels set (all were `None`)
  - [x] Created `/home/tzvi/frappe/doctypes_loading/creation/fix_webform_list_columns.py` script
  - [x] Added Hebrew labels to all list columns:
    - name → "מספר פנייה"
    - topic_category → "קטגורית נושא"
    - inquiry_status → "סטטוס"
    - creation → "תאריך יצירה"
  - [x] Cleared cache to apply changes
  - [x] List view now displays proper Hebrew column headers
- [x] UI Enhancement: Removed sidebar and footer from portal
  - [x] Added CSS to hide sidebar (`.web-sidebar`, `.sidebar`, `.page-sidebar`)
  - [x] Added CSS to hide footer (`.web-footer`, `footer`)
  - [x] Made main content full width by removing left/right margins
  - [x] Applied changes to both `supplier_dashboard.html` and `supplier-profile.html`
  - [x] Portal now displays clean interface without Frappe branding
- [x] UI Enhancement: Added user menu to dashboard header
  - [x] Updated `supplier_dashboard.py` to add user info (`user_name`, `user_email`) to context
  - [x] Updated `supplier-profile.py` to add user info to context
  - [x] Created custom user dropdown menu in dashboard header with:
    - User avatar icon and name display
    - Dropdown showing user's full name and email
    - "הפרופיל שלי" (My Profile) link
    - "התנתק" (Logout) link
  - [x] Added matching user menu to supplier-profile page header with:
    - "חזרה לדף הבית" (Back to Dashboard) button
    - Same user dropdown menu
    - Active state indicator on current page
  - [x] Implemented dropdown toggle JavaScript functionality
  - [x] Styled dropdown with modern design matching header gradient
  - [x] Added click-outside-to-close behavior
  - [x] Cleared cache and rebuilt app
  - [x] User menu now accessible from header on all portal pages
- [x] UI Enhancement: Improved user menu button to avatar style
  - [x] Added initials generation logic in both Python files (`supplier_dashboard.py`, `supplier-profile.py`)
  - [x] Logic extracts first letter of first name and last name (or first 2 letters if single name)
  - [x] Replaced text button with circular avatar displaying user initials
  - [x] Styled avatar with:
    - 44px circular design
    - White gradient background
    - Purple text color matching theme
    - Border with semi-transparent white
    - Drop shadow and hover scale animation
  - [x] Updated dropdown to align right under avatar
  - [x] Applied changes to both dashboard and profile pages
  - [x] Cleared cache and rebuilt app
  - [x] Avatar now displays user initials in modern circular button
- [x] UI Enhancement: Minimalist clean interface - removed decorative headers
  - [x] Removed large purple gradient header from dashboard page
  - [x] Removed decorative header from profile page
  - [x] Created minimal white top bar with just user avatar menu
  - [x] Made top bar sticky for easy access to user menu while scrolling
  - [x] Updated avatar styling:
    - Changed from white gradient to purple gradient background
    - Changed text color from purple to white
    - Updated border and shadow for light background
  - [x] Profile page: Added "חזרה לדף הבית" button in top bar
  - [x] Profile page: Moved page title into main content area
  - [x] Dashboard: Content now starts immediately with statistics cards
  - [x] Clean, focused interface with maximum space for dashboard content
  - [x] Cleared cache and rebuilt app
  - [x] Portal now displays minimal UI with focus on content

---

## Notes & Decisions

### Decision Log
- **WebForms over Custom Pages**: Chosen for faster implementation and built-in RTL support
- **Admin-Created Accounts**: Self-registration deferred to v2 for security simplicity
- **4-Layer Security**: Comprehensive approach ensures data isolation
- **Automated Permission Setup**: Created `add_portal_permissions.py` script to automate permission configuration instead of manual UI updates (more repeatable and version-controlled)
- **Programmatic WebForm Creation**: Chose Option B (programmatic) over manual UI creation for consistency with Phase 1 & 2 approach, repeatability, and version control

### Known Issues
- None yet

### Questions / Blockers
- None yet

---

**Next Steps**: All phases (1-5) COMPLETED! 🎉

**Ready for Manual Testing**:
1. Review testing documentation at `/home/tzvi/frappe/SUPPLIER_PORTAL_TESTING.md`
2. Log in with test credentials:
   - supplier1@test.com / Test@1234
   - supplier2@test.com / Test@1234
3. Follow the 7-step security testing checklist
4. Report any issues or proceed with production deployment

**Optional**: To remove test data after testing:
```bash
./run_doctype_script.sh test_data.create_portal_users.delete_test_portal_users
```
