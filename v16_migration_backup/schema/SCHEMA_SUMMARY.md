# Database Schema Summary - Siud App (v15)

## Exported: 2026-01-15

## DocType Tables

| Table Name | Type | Key Fields |
|------------|------|------------|
| `tabSupplier` | Core Entity | supplier_id (UNI), supplier_name, address, phone, email |
| `tabSupplier Activity Domain` | Child Table | activity_domain_category, parent (MUL) |
| `tabSupplier Inquiry` | Business | supplier_link, topic_category, inquiry_description, inquiry_status |
| `tabSupplier Role` | Reference | role_name (UNI), role_title_he |
| `tabActivity Domain Category` | Reference | category_code (UNI), category_name |
| `tabContact Person` | Related | contact_name, supplier_link, email, mobile_phone, primary_role_type |
| `tabContact Person Role` | Child Table | role, parent (MUL) |
| `tabDelegated Supplier` | Related | delegating_supplier, delegated_supplier, delegation_status, valid_from, valid_until |
| `tabDelegated Supplier Scope` | Child Table | activity_domain_category, parent (MUL) |
| `tabInquiry Topic Category` | Hierarchical Ref | category_code (UNI), category_name, parent_category, lft/rgt (Nested Set) |

## Common Fields (All Tables)

All Frappe DocTypes include these standard fields:
- `name` (varchar 140) - Primary key
- `creation` (datetime) - Record creation timestamp
- `modified` (datetime) - Last modification timestamp
- `modified_by` (varchar 140) - Last modifier
- `owner` (varchar 140) - Record creator
- `docstatus` (int) - Document status (0=Draft, 1=Submitted, 2=Cancelled)
- `idx` (int) - Row index for ordering
- `_user_tags`, `_comments`, `_assign`, `_liked_by` - Frappe system fields

## Child Table Fields

Child tables also include:
- `parent` (varchar 140) - Link to parent document
- `parentfield` (varchar 140) - Parent field name
- `parenttype` (varchar 140) - Parent DocType name

## Hierarchical Tables (Nested Set)

`tabInquiry Topic Category` uses Frappe's Nested Set for hierarchy:
- `lft` (int) - Left boundary
- `rgt` (int) - Right boundary
- `is_group` (int) - Whether node can have children
- `old_parent` (varchar 140) - Previous parent (for reorganization)

## Detailed Schemas

See `table_schemas.txt` for complete DESCRIBE output of all tables.
