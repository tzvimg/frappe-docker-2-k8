## DocType Specification for Supplier Inquiry Management POC

### 1. DocType: Supplier (ספק)

| Field Name (English) | Field Type (Frappe) | Length / Format | Description | Label (Hebrew) | Link / Details | Source |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`supplier_id`** | Data | | Unique identifier of the supplier. | **מזהה ספק** | Primary Key, Read Only after creation. | |
| **`supplier_name`** | Data | | Full name of the service provider. | **שם ספק** | | |
| **`activity_domains`** | Table | | Domains of activity of the supplier. | **תחומי פעילות** | Child table linked to `Activity Domain Category` (Allows multi-selection). | |
| **`address`** | Text | | Supplier address. | **כתובת** | |, |
| **`phone`** | Phone | | Phone number. | **טלפון** | Set by System Administrator during registration. | |
| **`email`** | Email | | Email address. | **כתובת דוא"ל** | Set by System Administrator during registration. Used for communication. | |

---

### 2. DocType: Contact Person (איש קשר)

ישות זו מייצגת משתמשי פורטל ווב (Users) בעלי גישה, המשויכים לספק,.

| Field Name (English) | Field Type (Frappe) | Length / Format | Description | Label (Hebrew) | Link / Details | Source |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`contact_name`** | Data | | Full name of the contact person. | **שם איש קשר** | | |
| **`email`** | Email | | Email address. | **כתובת דוא"ל** | Updatable by the contact person himself, as it is not used for identification. | |
| **`mobile_phone`** | Phone | | Mobile phone number. | **טלפון נייד** | Updatable by the contact person himself, as it is not used for identification. | |
| **`supplier_link`** | Link | | Association to the specific supplier. | **שיוך לספק** | Links to `Supplier` DocType. | |
| **`branch`** | Data | | The supplier branch the contact is associated with. | **סניף** | Relevant for managing contacts at the branch level,. | |
| **`assigned_roles`** | Table | | List of roles associated with this contact for handling various issues. | **רשימת תפקידים משויכים** | Child table linked to `Role` DocType. Managed independently by the supplier. | |
| **`primary_role_type`** | Select | | Classification of the contact's primary role. | **תפקיד ראשי** | Options: "ספק" (Supplier) or "איש קשר של ספק" (Supplier Contact Person). | |

---

### 3. DocType: Role (תפקיד)

| Field Name (English) | Field Type (Frappe) | Length / Format | Description | Label (Hebrew) | Link / Details | Source |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`role_name`** | Data | | Internal unique identifier for the role. | **שם תפקיד** | | |
| **`role_title_he`** | Data | | Display name in Hebrew. | **כותרת בעברית** | Examples include: שירות (נושאים מקצועיים), טיפול בתלונות, טיפול חשבונות שוטפים, טיפול בקרות רו"ח, ועוד,,. | |

---

### 4. DocType: Activity Domain Category (קטגוריות תחומי פעילות)

| Field Name (English) | Field Type (Frappe) | Length / Format | Description | Label (Hebrew) | Link / Details | Source |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`category_code`** | Data | | Unique category code. | **קוד קטגוריה** | | |
| **`category_name`** | Data | | Category name. | **שם קטגוריה** | | |

---

### 5. DocType: Inquiry Topic Category (קטגוריות של נושאי פנייה)

| Field Name (English) | Field Type (Frappe) | Length / Format | Description | Label (Hebrew) | Link / Details | Source |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`category_code`** | Data | | Unique category code. | **קוד קטגוריה** | | |
| **`category_name`** | Data | | Category name. | **שם קטגוריה** | | |
| **`parent_category`** | Link | | Link to the category above it in the hierarchy. | **קטגוריית אב** | Self-link to `Inquiry Topic Category`. Supports up to two levels of hierarchy. | |

---

### 6. DocType: Supplier Inquiry (פניית ספק)

| Field Name (English) | Field Type (Frappe) | Length / Format | Description | Label (Hebrew) | Link / Details | Source |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`supplier_link`** | Link | | The supplier submitting the inquiry. | **מזהה ספק** | Links to `Supplier` DocType. | |
| **`topic_category`** | Link | | Classification of the inquiry topic. | **קטגורית נושא פנייה** | Links to `Inquiry Topic Category`. | |
| **`inquiry_description`** | Text Editor | | Detailed content of the inquiry. | **תיאור הפנייה** | Rich Text field, allowing detailed textual input. | |
| **`inquiry_context`** | Select | | Whether the inquiry is for the supplier itself or for an insured party. | **הקשר הפנייה** | Options: "ספק עצמו" / "מבוטח". | |
| **`insured_id_number`** | Data | 9 digits | Insured party's ID number (if context is 'Insured'). | **מספר זהות של המבוטח** | | |
| **`insured_full_name`** | Data | | Insured party's full name (if context is 'Insured'). | **שם מלא של המבוטח** | | |
| **`attachments`** | Attach | | Files attached by the supplier. | **קבצים מצורפים** | Optional field. | |
| **`inquiry_status`** | Select | | Current status of the inquiry handling. | **סטטוס פנייה** | Status values to be defined later. | |
| **`assigned_role`** | Link | | The defined role responsible for handling this inquiry. | **שיוך לתפקיד מטפל בפניה** | Links to `Role` DocType. | |
| **`assigned_employee_id`** | Link | | The specific employee (system user) handling the inquiry. | **מזהה הפקיד שמטפל בפנייה** | Links to Frappe `User` DocType. | |
| **`response_text`** | Text Editor | | Content of the response provided by the handling employee. | **המענה לפנייה - מלל** | Rich Text field. Updated by the staff treating the inquiry. | |
| **`response_attachments`** | Attach | | Optional files sent in response. | **המענה לפנייה - קבצים** | Optional field. | |

### הערות נוספות על מודולים ותהליכים (יישום Frappe)

הספציפיקציה לעיל מכסה את גבולות ה-POC כפי שהוגדרו,. ה-Frappe Framework מאפשר ליישם את תהליכי הניהול הנלווים כדלקמן:

1.  **עדכון פרטי ספק/איש קשר:** נותן השירות יכול להיכנס לאתר ולעדכן באופן עצמאי את פרטי הקשר של עצמו ואת פרטי אנשי הקשר הרלוונטיים שלו. ב-Frappe, ניתן להגדיר הרשאות משתמש (Permissions) כך שמשתמשים בעלי תפקיד "ספק" יוכלו לערוך ישויות `Supplier` ו-`Contact Person` המשויכות אליהם.
2.  **ניהול מסמכים נלווים:** למרות שישות `Document` נפרדת אינה מוגדרת בגבולות ה-POC, האפיון מציין צורך בניהול מסמכים כגון הסכמים ואישורים, ובמעקב אחר תוקף המסמכים עם התראות מתאימות. נדרש שהמערכת תאפשר לנותני שירותים להעלות קבצים חתומים.
3.  **תיעוד תקשורת ("תיק לקוח"):** האפיון מציין צורך ב-"תיק לקוח" או "תיק ספק" לתיעוד שיחות ופניות של הספק מול עובדי האגף. ב-Frappe, ניתן להשתמש בפיצ'ר ה-**Communication/Activity Feed** הקיים בכל DocType, או להוסיף DocType ילד (`Child Table`) בתוך ישות `Supplier` בשם `Communication Log` שיכיל שדות כגון: `Date`, `Type` (שיחה/פנייה), ו-`Details`.
4.  **התראות (Alerts):** נדרשת יכולת יצירת התראה על קבלת מסמך חדש או פנייה חדשה שתגיע לעובדים הרלוונטיים. Frappe מספקת מנגנון התראות מובנה (Alerts/Notifications) ו-Email Alerts, המאפשר לשלוח הודעות אוטומטיות (כאשר מסמכים נבדקו תקין/חסר/לא תקין).