# Supplier Portal - Security Testing Checklist

**Created**: 2025-12-22
**Test Users**: Created via `/home/tzvi/frappe/doctypes_loading/test_data/create_portal_users.py`

---

## Test Credentials

### User 1
- **Email**: supplier1@test.com
- **Password**: Test@1234
- **Linked to**: SUP-TEST-001 (ספק בדיקה ראשון בע"מ)
- **Sample Inquiries**: SI-00026, SI-00027

### User 2
- **Email**: supplier2@test.com
- **Password**: Test@1234
- **Linked to**: SUP-TEST-002 (ספק בדיקה שני בע"מ)
- **Sample Inquiries**: SI-00028, SI-00029

---

## Security Testing Checklist

### 1. Portal Access & Landing Page ✓
**Expected**: Portal users see the supplier dashboard, not the desk interface

**Steps**:
1. [ ] Open http://localhost:8000 in browser
2. [ ] Log in as `supplier1@test.com` / `Test@1234`
3. [ ] **Verify**: You see the supplier dashboard at `/supplier-dashboard`
4. [ ] **Verify**: You do NOT see the desk interface at `/app`
5. [ ] **Verify**: Portal menu shows: דף הבית, הפניות שלי, פנייה חדשה, פרופיל הספק
6. [ ] **Verify**: Dashboard displays:
   - Welcome message with supplier name
   - Statistics cards (סה"כ פניות, פניות פתוחות, פניות סגורות)
   - Recent inquiries list
   - Quick action buttons

**Result**: ☐ Pass | ☐ Fail
**Notes**: _______________________________________

---

### 2. Data Isolation - Inquiry List ✓
**Expected**: User A can only see their own inquiries, not User B's inquiries

**Steps**:
1. [ ] Log in as `supplier1@test.com`
2. [ ] Click "הפניות שלי" in the menu
3. [ ] **Verify**: List shows only inquiries SI-00026 and SI-00027
4. [ ] **Verify**: Inquiries SI-00028 and SI-00029 are NOT visible
5. [ ] Try to access inquiry SI-00028 directly: `http://localhost:8000/supplier-inquiry-form/SI-00028`
6. [ ] **Verify**: You get a permission error or are redirected (cannot access other supplier's inquiry)
7. [ ] Log out
8. [ ] Log in as `supplier2@test.com`
9. [ ] Click "הפניות שלי"
10. [ ] **Verify**: List shows only inquiries SI-00028 and SI-00029
11. [ ] **Verify**: Inquiries SI-00026 and SI-00027 are NOT visible

**Result**: ☐ Pass | ☐ Fail
**Notes**: _______________________________________

---

### 3. Inquiry Submission - Auto-Link ✓
**Expected**: New inquiries are automatically linked to the logged-in supplier

**Steps**:
1. [ ] Log in as `supplier1@test.com`
2. [ ] Click "פנייה חדשה" in the menu
3. [ ] **Verify**: Form opens at `/supplier-inquiry-form/new`
4. [ ] **Verify**: Supplier link field is pre-populated and read-only
5. [ ] Fill in the form:
   - קטגורית נושא פנייה: Select any category
   - תיאור הפנייה: "בדיקת יצירת פנייה חדשה"
   - הקשר הפנייה: "ספק עצמו"
6. [ ] Click "Submit" or "שלח"
7. [ ] **Verify**: Inquiry is created successfully
8. [ ] Go to "הפניות שלי"
9. [ ] **Verify**: New inquiry appears in the list
10. [ ] **Verify**: Inquiry is linked to SUP-TEST-001
11. [ ] Try to manually edit the supplier_link in the browser console or by modifying the URL
12. [ ] **Verify**: You cannot change the supplier_link to another supplier

**Result**: ☐ Pass | ☐ Fail
**Notes**: _______________________________________

---

### 4. Profile Editing ✓
**Expected**: Can edit supplier profile, but cannot change supplier_id

**Steps**:
1. [ ] Log in as `supplier1@test.com`
2. [ ] Click "פרופיל הספק" in the menu
3. [ ] **Verify**: Profile page opens at `/supplier-profile`
4. [ ] **Verify**: Supplier ID field (SUP-TEST-001) is displayed but read-only/disabled
5. [ ] **Verify**: Name, Email, Address fields are editable
6. [ ] Edit the address field: "כתובת חדשה - רחוב הבדיקה 123, תל אביב"
7. [ ] Click "שמור שינויים" (Save Changes)
8. [ ] **Verify**: Success message appears
9. [ ] Refresh the page
10. [ ] **Verify**: Updated address is persisted
11. [ ] Try to use browser developer tools to change the supplier_id field
12. [ ] **Verify**: Server-side validation prevents changing supplier_id

**Result**: ☐ Pass | ☐ Fail
**Notes**: _______________________________________

---

### 5. Desk Access Restriction ✓
**Expected**: Portal users cannot access desk interface

**Steps**:
1. [ ] Log in as `supplier1@test.com`
2. [ ] Try to access desk directly: `http://localhost:8000/app`
3. [ ] **Verify**: You are redirected to portal dashboard OR get permission error
4. [ ] Try to access DocType list: `http://localhost:8000/app/supplier-inquiry`
5. [ ] **Verify**: You cannot access the desk view
6. [ ] Try to access desk API: `http://localhost:8000/api/resource/Supplier/SUP-TEST-002`
7. [ ] **Verify**: You get permission error (cannot access other supplier's data)
8. [ ] Try to access your own supplier via API: `http://localhost:8000/api/resource/Supplier/SUP-TEST-001`
9. [ ] **Verify**: You may be able to read your own data, but cannot access other suppliers

**Result**: ☐ Pass | ☐ Fail
**Notes**: _______________________________________

---

### 6. Cross-Supplier Data Access ✓
**Expected**: Cannot view or edit another supplier's profile

**Steps**:
1. [ ] Log in as `supplier1@test.com`
2. [ ] Note your supplier ID: SUP-TEST-001
3. [ ] Try to access other supplier's profile by modifying URL or API call
4. [ ] Try: `http://localhost:8000/api/resource/Supplier/SUP-TEST-002`
5. [ ] **Verify**: Permission error (403 or similar)
6. [ ] Log out
7. [ ] Log in as `supplier2@test.com`
8. [ ] Go to "פרופיל הספק"
9. [ ] **Verify**: Profile shows SUP-TEST-002 (not SUP-TEST-001)
10. [ ] Try to access SUP-TEST-001 profile
11. [ ] **Verify**: Cannot access other supplier's profile

**Result**: ☐ Pass | ☐ Fail
**Notes**: _______________________________________

---

### 7. Hebrew RTL Interface ✓
**Expected**: All portal pages display correctly in Hebrew RTL

**Steps**:
1. [ ] Log in as any portal user
2. [ ] Visit each portal page:
   - Dashboard: `/supplier-dashboard`
   - Inquiry list: `/supplier-inquiry-form/list`
   - New inquiry: `/supplier-inquiry-form/new`
   - Profile: `/supplier-profile`
3. [ ] **Verify** on each page:
   - Text is aligned to the right
   - Navigation menu is RTL
   - Forms and buttons are properly aligned
   - Hebrew text displays correctly
   - No layout issues or overlapping elements

**Result**: ☐ Pass | ☐ Fail
**Notes**: _______________________________________

---

## Summary

**Total Tests**: 7
**Passed**: _____
**Failed**: _____
**Date Tested**: _____
**Tester**: _____

---

## Known Issues / Notes

(Record any issues discovered during testing)

---

## Cleanup (Optional)

To delete all test data created by this script:

```bash
cd /home/tzvi/frappe
./run_doctype_script.sh test_data.create_portal_users.delete_test_portal_users
```

This will delete:
- Test users (supplier1@test.com, supplier2@test.com)
- Test suppliers (SUP-TEST-001, SUP-TEST-002)
- All test inquiries
