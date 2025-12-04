# Service Provider Application - UI Creation Guide

## Quick Reference for Creating via Frappe UI

**Access:** http://localhost:8000
**Path:** Desk → Developer → DocType → New

---

## Basic Settings

| Field | Value |
|-------|-------|
| **Name** | Service Provider Application |
| **Module** | Nursing Management |
| **Is Submittable** | ✓ Yes |
| **Track Changes** | ✓ Yes |
| **Naming** | Select "By fieldname" → Create field `naming_series` OR use "Expression" → `format:SPA-{#####}` |

---

## Fields to Add (45 total across 8 sections)

### Section 1: פרטי ספק (Basic Information)
1. **Section Break** - `basic_info_section` - "פרטי ספק"
2. **Data** - `provider_name` - "שם נותן השירות" - ✓ Mandatory
3. **Data** - `hp_number` - "מספר ח\"פ" - ✓ Mandatory - Length: 9
4. **Column Break** - `column_break_1`
5. **Select** - `service_type` - "סוג שירות" - ✓ Mandatory
   - Options: `טיפול בבית\nמרכז יום\nקהילה תומכת\nמוצרי ספיגה`
6. **Data** - `branch_type` - "סוג סניף"
7. **Column Break** - `column_break_2`
8. **Data** - `contact_person` - "איש קשר"
9. **Data** - `phone` - "טלפון"
10. **Data** - `email` - "אימייל" - ✓ Mandatory - Options: "Email"
11. **Small Text** - `address` - "כתובת"

### Section 2: סטטוס בקשה (Application Status)
12. **Section Break** - `status_section` - "סטטוס בקשה"
13. **Link** - `workflow_state` - "סטטוס" - Options: "Workflow State" - ✓ Read Only
14. **Date** - `application_date` - "תאריך הגשה" - Default: "Today" - ✓ Read Only
15. **Column Break** - `column_break_3`
16. **Link** - `assigned_to` - "מטופל על ידי" - Options: "User"

### Section 3: רשימת מסמכים (Document Checklist)
17. **Section Break** - `documents_section` - "רשימת מסמכים"
18. **Table** - `application_document_checklist` - "רשימת מסמכים נדרשים" - Options: "Application Document Checklist"

### Section 4: בדיקת מטה (HQ Review)
19. **Section Break** - `hq_section` - "בדיקת מטה"
20. **Select** - `hq_check_status` - "סטטוס בדיקת מטה"
    - Options: `\nתקין\nלא תקין`
21. **Link** - `hq_reviewer` - "בודק מטה" - Options: "User"
22. **Column Break** - `column_break_4`
23. **Date** - `hq_review_date` - "תאריך בדיקת מטה"
24. **Text Editor** - `hq_notes` - "הערות מטה"

### Section 5: הבהרת נתונים (Data Clarification)
25. **Section Break** - `data_section` - "הבהרת נתונים"
26. **Select** - `data_clarification_status` - "סטטוס הבהרת נתונים"
    - Options: `\nתקין\nלא תקין`
27. **Check** - `bi_verification` - "אומת מול ביטוח לאומי"
28. **Column Break** - `column_break_5`
29. **Link** - `data_reviewer` - "בודק נתונים" - Options: "User"
30. **Date** - `data_review_date` - "תאריך בדיקת נתונים"
31. **Text Editor** - `data_notes` - "הערות בדיקת נתונים"

### Section 6: טיפול בדחייה (Rejection Handling)
32. **Section Break** - `rejection_section` - "טיפול בדחייה"
33. **Text Editor** - `rejection_reason` - "סיבת דחייה"
34. **Column Break** - `column_break_6`
35. **Date** - `rejection_date` - "תאריך דחייה" - ✓ Read Only

### Section 7: טיפול סופי (Final Processing)
36. **Section Break** - `final_section` - "טיפול סופי"
37. **Check** - `agreement_prepared` - "הסכם הוכן"
38. **Attach** - `agreement_file` - "קובץ הסכם"
39. **Column Break** - `column_break_7`
40. **Check** - `nursing_system_synced` - "שוקף במערכת סיעוד"
41. **Link** - `created_service_provider` - "נותן שירות שנוצר" - Options: "Service Provider" - ✓ Read Only
42. **Date** - `approval_date` - "תאריך אישור סופי"

### Section 8: תיעוד תקשורת (Communication Log)
43. **Section Break** - `communication_section` - "תיעוד תקשורת"
44. **Text Editor** - `communication_history` - "היסטוריית תקשורת" - ✓ Read Only

---

## Permissions

Add permission for **System Manager** role:
- ✓ Read
- ✓ Write
- ✓ Create
- ✓ Delete
- ✓ Submit
- ✓ Cancel
- ✓ Amend

---

## After Creation

1. Click **Save**
2. The system will create:
   - JSON file: `service_provider_application.json`
   - Python controller: `service_provider_application.py`
   - JS file: `service_provider_application.js`

3. Location: `/workspace/development/frappe-bench/apps/nursing_management/nursing_management/nursing_management/doctype/service_provider_application/`

4. Then run from command line:
   ```bash
   bench --site development.localhost clear-cache
   bench --site development.localhost migrate
   ```

---

## Verification

After creation, verify via command line:
```bash
docker exec frappe_docker_devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site development.localhost console" <<'EOF'
import frappe
doc = frappe.get_doc('DocType', 'Service Provider Application')
print(f"Fields: {len(doc.fields)}")
print(f"Submittable: {doc.is_submittable}")
exit
EOF
```

Expected output:
- Fields: 44+
- Submittable: 1 (True)

---

## Next Steps

After DocType is created:
1. Add Python validations to `service_provider_application.py`
2. Configure Workflow (Phase 2)
3. Test with sample data
