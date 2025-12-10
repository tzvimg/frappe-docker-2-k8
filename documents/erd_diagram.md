# ERD Diagram - Supplier Inquiry Management System

Entity Relationship Diagram based on the DocType specification for the Nursing Management System POC.

```mermaid
erDiagram
    SUPPLIER ||--o{ SUPPLIER_ACTIVITY_DOMAINS : "has"
    SUPPLIER ||--o{ CONTACT_PERSON : "employs"
    SUPPLIER ||--o{ SUPPLIER_INQUIRY : "submits"

    ACTIVITY_DOMAIN_CATEGORY ||--o{ SUPPLIER_ACTIVITY_DOMAINS : "categorizes"

    CONTACT_PERSON ||--o{ CONTACT_PERSON_ROLES : "has"
    ROLE ||--o{ CONTACT_PERSON_ROLES : "assigned to"
    ROLE ||--o{ SUPPLIER_INQUIRY : "handles"

    INQUIRY_TOPIC_CATEGORY ||--o| INQUIRY_TOPIC_CATEGORY : "parent of"
    INQUIRY_TOPIC_CATEGORY ||--o{ SUPPLIER_INQUIRY : "classifies"

    USER ||--o{ SUPPLIER_INQUIRY : "assigned to"

    SUPPLIER {
        string supplier_id PK "מזהה ספק"
        string supplier_name "שם ספק"
        text address "כתובת"
        phone phone "טלפון"
        email email "דוא״ל"
    }

    ACTIVITY_DOMAIN_CATEGORY {
        string category_code PK "קוד קטגוריה"
        string category_name "שם קטגוריה"
    }

    SUPPLIER_ACTIVITY_DOMAINS {
        string supplier_id FK
        string category_code FK
    }

    CONTACT_PERSON {
        string contact_id PK
        string contact_name "שם איש קשר"
        email email "דוא״ל"
        phone mobile_phone "טלפון נייד"
        string supplier_link FK "שיוך לספק"
        string branch "סניף"
        string primary_role_type "תפקיד ראשי"
    }

    ROLE {
        string role_name PK "שם תפקיד"
        string role_title_he "כותרת בעברית"
    }

    CONTACT_PERSON_ROLES {
        string contact_id FK
        string role_name FK
    }

    INQUIRY_TOPIC_CATEGORY {
        string category_code PK "קוד קטגוריה"
        string category_name "שם קטגוריה"
        string parent_category FK "קטגורית אב"
    }

    SUPPLIER_INQUIRY {
        string inquiry_id PK
        string supplier_link FK "מזהה ספק"
        string topic_category FK "קטגורית נושא"
        text inquiry_description "תיאור הפנייה"
        string inquiry_context "הקשר הפנייה"
        string insured_id_number "מס׳ זהות מבוטח"
        string insured_full_name "שם מבוטח"
        string attachments "קבצים מצורפים"
        string inquiry_status "סטטוס פנייה"
        string assigned_role FK "שיוך לתפקיד"
        string assigned_employee_id FK "מזהה פקיד"
        text response_text "מלל מענה"
        string response_attachments "קבצי מענה"
    }

    USER {
        string user_id PK
        string full_name "שם מלא"
        email email "דוא״ל"
    }
```

## Entity Descriptions

### Core Entities

1. **Supplier (ספק)**
   - Primary entity representing service providers
   - Has multiple activity domains and contact persons
   - Submits inquiries to the system

2. **Contact Person (איש קשר)**
   - Portal users associated with suppliers
   - Can have multiple roles
   - Links to specific supplier and branch

3. **Role (תפקיד)**
   - Functional roles for inquiry handling
   - Examples: שירות, טיפול בתלונות, טיפול חשבונות שוטפים

4. **Activity Domain Category (קטגוריות תחומי פעילות)**
   - Categories defining supplier's areas of operation
   - Many-to-many relationship with suppliers

5. **Inquiry Topic Category (קטגוריות נושאי פנייה)**
   - Hierarchical classification (2 levels)
   - Self-referential for parent-child relationship

6. **Supplier Inquiry (פניית ספק)**
   - Main transactional entity
   - Tracks inquiry lifecycle, assignment, and responses
   - Links to supplier, topic category, role, and employee

7. **User (משתמש מערכת)**
   - Frappe built-in entity
   - Represents internal employees handling inquiries

## Relationship Summary

- **One-to-Many**: Supplier→Contact Person, Supplier→Inquiry, Role→Inquiry, User→Inquiry
- **Many-to-Many**: Supplier↔Activity Domain (via child table), Contact Person↔Role (via child table)
- **Self-Referential**: Inquiry Topic Category (parent-child hierarchy)
- **Lookup**: Inquiry→Topic Category, Inquiry→Supplier, Inquiry→Role, Inquiry→User

## Notes

- Child tables (SUPPLIER_ACTIVITY_DOMAINS, CONTACT_PERSON_ROLES) represent many-to-many relationships
- All field labels shown in Hebrew as per system requirements
- PK = Primary Key, FK = Foreign Key
- Inquiry context can be "ספק עצמו" or "מבוטח"
