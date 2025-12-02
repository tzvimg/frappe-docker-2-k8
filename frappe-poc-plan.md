# Frappe POC Implementation Plan - אגף סיעוד

## Executive Summary
This document outlines a comprehensive plan to implement a Proof of Concept (POC) for the Nursing Department (אגף סיעוד) management system using Frappe Framework. The POC will demonstrate core functionality including service provider management, contracts, complaints, invoices, and caregiver tracking.

---

## 1. Project Overview

### 1.1 Objectives
- Validate Frappe Framework's suitability for managing nursing department operations
- Implement core entities with essential relationships
- Demonstrate workflow automation capabilities
- Validate data model and business logic
- Create foundation for future AI/automation integration

### 1.2 Scope
The POC will implement 6 core DocTypes with their relationships:
1. **נותן שירות** (Service Provider)
2. **סניף נותן שירות** (Service Provider Branch)
3. **הסכם** (Contract)
4. **מסמך/אישור** (Document/Approval)
5. **תלונה** (Complaint)
6. **מטפלת** (Caregiver)

### 1.3 Out of Scope (Phase 2)
- חשבונית (Invoice) - Complex financial integration
- הכשרה/קורס (Training/Course) - Many-to-many relationships
- מבוטח (Insured) - External data source
- תיעוד תקשורת (Communication Log) - Can be added later
- איש קשר (Contact Person) - Can use Frappe's built-in Contact

---

## 2. Environment Setup

### 2.1 Prerequisites
- Docker Desktop installed (already have frappe_docker)
- Python 3.10+
- Node.js 16+
- Git
- Basic understanding of Frappe Framework
- VS Code with Dev Containers extension (recommended)

### 2.2 Current Environment Status ✅
**COMPLETED - Environment is ready!**

- **Container**: `frappe_docker_devcontainer-frappe-1` (Running)
- **Bench Location**: `/workspace/development/frappe-bench`
- **Site**: `development.localhost`
- **Installed Apps**:
  - frappe: 15.88.2 (version-15)
  - erpnext: 15.88.0 (version-15)
  - btl_firstone: 0.0.1 (test app - has Mana DocType removed)
  - **nursing_management: 0.0.1** ✨ (POC app)

### 2.3 Development Workflow Best Practices

#### 2.3.1 How to Access the Environment

**RECOMMENDED: Use VS Code Dev Container (Already Connected)**
```bash
# You have another VS Code instance connected to the dev container
# This is the BEST way to work with Frappe
# All commands run directly in the container context
```

**Alternative: Docker Exec (for automation/scripting)**
```bash
# Run commands from host (Windows) machine:
docker exec frappe_docker_devcontainer-frappe-1 bash -c "cd frappe-bench && <command>"

# Example:
docker exec frappe_docker_devcontainer-frappe-1 bash -c "cd frappe-bench && bench --site development.localhost list-apps"
```

#### 2.3.2 Frappe Command Structure

**Key Rules:**
1. Always run bench commands from `/workspace/development/frappe-bench` directory
2. Use `--site development.localhost` for site-specific commands
3. Bench must be run from within the bench directory

**Common Commands:**
```bash
# Inside container (via VS Code terminal or docker exec):
cd /workspace/development/frappe-bench

# List apps on site
bench --site development.localhost list-apps

# Create new DocType (via UI is recommended, but CLI option:)
bench --site development.localhost console
>>> # Python REPL opens

# Clear cache (important after changes)
bench --site development.localhost clear-cache

# Restart bench (if needed)
bench restart

# Migrate database (after DocType changes)
bench --site development.localhost migrate

# Build assets (after JS/CSS changes)
bench build --app nursing_management

# Run bench in development mode (auto-reload)
# NOT NEEDED - container already runs in dev mode
```

#### 2.3.3 Creating DocTypes - BEST METHODS

**Method 1: Frappe UI (RECOMMENDED for POC)**
1. Access web interface: http://localhost:8000
2. Login as Administrator
3. Navigate to: Desk → Developer → DocType
4. Click "New"
5. Fill in DocType details
6. Add fields
7. Save

**Advantages:**
- Visual, intuitive
- Real-time validation
- Automatic JSON generation
- Auto-updates database
- Generates Python controller files automatically

**Method 2: JSON File Creation (for version control)**
```bash
# Create DocType JSON file manually in:
# /workspace/development/frappe-bench/apps/nursing_management/nursing_management/nursing_management/doctype/<doctype_name>/<doctype_name>.json

# Then sync to database:
bench --site development.localhost migrate
```

**Method 3: bench console (for automation/testing)**
```python
# Inside bench console
doc = frappe.get_doc({
    "doctype": "DocType",
    "module": "Nursing Management",
    "name": "Service Provider",
    # ... field definitions
})
doc.insert()
```

#### 2.3.4 File Locations

**App Structure:**
```
/workspace/development/frappe-bench/apps/nursing_management/
├── nursing_management/                    # Main Python package
│   ├── nursing_management/                # Module directory
│   │   ├── doctype/                      # DocTypes go here
│   │   │   ├── service_provider/         # Example DocType
│   │   │   │   ├── service_provider.json # DocType definition
│   │   │   │   ├── service_provider.py   # Python controller
│   │   │   │   └── service_provider.js   # Client-side JS
│   │   └── __init__.py
│   ├── config/                            # App configuration
│   ├── hooks.py                           # App hooks (events, tasks)
│   ├── modules.txt                        # Module list
│   └── public/                            # Static files (CSS, JS, images)
├── license.txt
├── pyproject.toml                         # Python dependencies
└── README.md
```

#### 2.3.5 Key Frappe Concepts

**DocType = Data Model + Form + Controller**
- **JSON file**: Field definitions, permissions, naming rules
- **Python (.py) file**: Business logic, validations, calculations
- **JavaScript (.js) file**: Client-side behavior, UI customization

**Automatic Features:**
- REST API (auto-generated for every DocType)
- List View
- Form View
- Print Formats
- Permissions system
- Audit trail (track_changes)

#### 2.3.6 Windows-Specific Considerations

**Issue: TTY/Interactive Commands**
```bash
# ❌ This fails on Windows Git Bash:
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "command"

# ✅ Use without -it:
docker exec frappe_docker_devcontainer-frappe-1 bash -c "command"

# ✅ OR use VS Code integrated terminal (BEST option)
```

**Issue: Path Translation (Git Bash)**
```bash
# Git Bash auto-translates /workspace to C:/Program Files/Git/workspace
# Always use full docker exec command from Windows
# OR work inside VS Code Dev Container terminal
```

#### 2.3.7 Development Cycle

**Typical Workflow:**
1. **Create/Edit DocType** (via UI or JSON files)
2. **Clear Cache**: `bench --site development.localhost clear-cache`
3. **Test in Browser**: http://localhost:8000
4. **Add Business Logic**: Edit `.py` files in `doctype/` directory
5. **Add Client Scripts**: Edit `.js` files
6. **Migrate**: `bench --site development.localhost migrate` (if needed)
7. **Build**: `bench build --app nursing_management` (if JS/CSS changes)

**Hot Reload:**
- Python changes: Automatically reloaded (dev mode)
- JS/CSS changes: Need `bench build` or auto-build watcher
- DocType JSON changes: Need migrate or UI save

#### 2.3.8 Debugging

**View Logs:**
```bash
# Inside container or docker exec:
cd frappe-bench

# Real-time logs:
tail -f logs/bench.log

# Error logs:
tail -f logs/error.log

# Site-specific logs:
tail -f logs/development.localhost.error.log
```

**Python Debugging:**
```python
# Add to .py controller files:
frappe.log_error(message="Debug info", title="Debug")
# View in: Desk → Error Log

# Or use print (shows in bench.log):
print("Debug:", variable)
```

**Browser Console:**
```javascript
// In DocType .js file or browser console:
console.log("Debug:", cur_frm.doc);
frappe.msgprint("Debug message");
```

#### 2.3.9 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Cache not clearing | `bench --site development.localhost clear-cache` |
| DocType not appearing | Check module name matches, restart bench |
| Permission denied | Check DocType permissions, user roles |
| Changes not reflecting | Clear cache + hard refresh browser (Ctrl+Shift+R) |
| Bench command errors | Ensure you're in `/workspace/development/frappe-bench` |
| Database errors | Check migrations: `bench --site development.localhost migrate` |

---

### 2.4 Installation Steps (COMPLETED ✅)

#### Step 1: Setup Frappe Development Environment ✅
```bash
cd C:/dev/btl/frappe/frappe_docker/development
# Containers are running
```

#### Step 2: Create Custom App ✅
```bash
# nursing_management app created and installed
docker exec frappe_docker_devcontainer-frappe-1 bash -c "cd frappe-bench && bench --site development.localhost list-apps"
# Shows: nursing_management 0.0.1
```

#### Step 3: Verify Installation ✅
- App installed on development.localhost
- Module "Nursing Management" configured
- Ready for DocType implementation

---

## 3. DocType Implementation Plan

### 3.1 Implementation Order
DocTypes should be implemented in dependency order:

**Phase 1: Core Entities (Week 1)**
1. נותן שירות (Service Provider) - No dependencies
2. מטפלת (Caregiver) - Links to Service Provider

**Phase 2: Organizational Structure (Week 1-2)**
3. סניף נותן שירות (Branch) - Links to Service Provider
4. הסכם (Contract) - Links to Branch

**Phase 3: Documents & Compliance (Week 2)**
5. מסמך/אישור (Document) - Links to Contract

**Phase 4: Operations (Week 2-3)**
6. תלונה (Complaint) - Links to Service Provider, Caregiver

---

## 4. Detailed DocType Specifications

### 4.1 נותן שירות (Service Provider)

**DocType Name:** `Service Provider`

**Fields:**
```json
{
  "hp_number": {
    "fieldtype": "Data",
    "label": "ח\"פ מספר",
    "unique": true,
    "reqd": true,
    "length": 9
  },
  "provider_name": {
    "fieldtype": "Data",
    "label": "שם נותן השירות",
    "reqd": true
  },
  "address": {
    "fieldtype": "Small Text",
    "label": "כתובת"
  },
  "phone": {
    "fieldtype": "Data",
    "label": "טלפון"
  },
  "fax": {
    "fieldtype": "Data",
    "label": "פקס"
  },
  "email": {
    "fieldtype": "Data",
    "label": "אימייל",
    "options": "Email"
  },
  "service_types": {
    "fieldtype": "Select",
    "label": "סוגי שירותים",
    "options": "טיפול בבית\nמרכזי יום\nקהילות תומכות\nספקי מוצרי ספיגה",
    "reqd": true
  },
  "status": {
    "fieldtype": "Select",
    "label": "סטטוס",
    "options": "פעיל\nלא פעיל\nהוקפא",
    "default": "פעיל"
  }
}
```

**Permissions:**
- Service Provider can view/edit their own record via Portal
- Department staff: Full access

**Automation:**
- Auto-name: HP-{hp_number}
- Validation: HP number must be 9 digits

---

### 4.2 מטפלת (Caregiver)

**DocType Name:** `Caregiver`

**Fields:**
```json
{
  "id_number": {
    "fieldtype": "Data",
    "label": "תעודת זהות",
    "unique": true,
    "reqd": true,
    "length": 9
  },
  "first_name": {
    "fieldtype": "Data",
    "label": "שם פרטי",
    "reqd": true
  },
  "last_name": {
    "fieldtype": "Data",
    "label": "שם משפחה",
    "reqd": true
  },
  "phone": {
    "fieldtype": "Data",
    "label": "טלפון"
  },
  "address": {
    "fieldtype": "Small Text",
    "label": "כתובת"
  },
  "current_employer": {
    "fieldtype": "Link",
    "label": "מעסיק נוכחי",
    "options": "Service Provider"
  },
  "employment_start_date": {
    "fieldtype": "Date",
    "label": "תאריך תחילת העסקה"
  },
  "status": {
    "fieldtype": "Select",
    "label": "סטטוס",
    "options": "פעילה\nלא פעילה\nהוקפאה",
    "default": "פעילה"
  },
  "notes": {
    "fieldtype": "Text Editor",
    "label": "הערות"
  }
}
```

**Child Tables:**
- Employment History (היסטוריית העסקה)

**Automation:**
- Auto-name: CG-{id_number}

---

### 4.3 סניף נותן שירות (Service Provider Branch)

**DocType Name:** `Service Provider Branch`

**Fields:**
```json
{
  "branch_code": {
    "fieldtype": "Data",
    "label": "קוד סניף",
    "reqd": true,
    "length": 2
  },
  "service_provider": {
    "fieldtype": "Link",
    "label": "נותן שירות",
    "options": "Service Provider",
    "reqd": true
  },
  "branch_name": {
    "fieldtype": "Data",
    "label": "שם הסניף"
  },
  "address": {
    "fieldtype": "Small Text",
    "label": "כתובת סניף"
  },
  "phone": {
    "fieldtype": "Data",
    "label": "טלפון סניף"
  },
  "email": {
    "fieldtype": "Data",
    "label": "אימייל",
    "options": "Email"
  },
  "status": {
    "fieldtype": "Select",
    "label": "סטטוס",
    "options": "פעיל\nסגור",
    "default": "פעיל"
  }
}
```

**Automation:**
- Auto-name: {service_provider}-BR-{branch_code}
- Validation: Branch code must be exactly 2 digits
- Validation: Branch code unique per service provider

---

### 4.4 הסכם (Contract)

**DocType Name:** `Contract`

**Fields:**
```json
{
  "contract_number": {
    "fieldtype": "Data",
    "label": "מס' הסכם",
    "unique": true,
    "reqd": true
  },
  "branch": {
    "fieldtype": "Link",
    "label": "סניף",
    "options": "Service Provider Branch",
    "reqd": true
  },
  "service_provider": {
    "fieldtype": "Link",
    "label": "נותן שירות",
    "options": "Service Provider",
    "read_only": true
  },
  "start_date": {
    "fieldtype": "Date",
    "label": "תאריך תחילה",
    "reqd": true
  },
  "end_date": {
    "fieldtype": "Date",
    "label": "תאריך סיום",
    "reqd": true
  },
  "status": {
    "fieldtype": "Select",
    "label": "סטטוס",
    "options": "טיוטה\nפעיל\nפג תוקף\nבוטל",
    "default": "טיוטה"
  },
  "alert_days_before_expiry": {
    "fieldtype": "Int",
    "label": "התראה לפני פקיעה (ימים)",
    "default": 30
  },
  "notes": {
    "fieldtype": "Text Editor",
    "label": "הערות"
  }
}
```

**Automation:**
- Auto-name: CON-{contract_number}
- Auto-fetch: Service Provider from Branch
- Scheduled task: Daily check for expiring contracts
- Alert: Email notification before expiry

---

### 4.5 מסמך/אישור (Document/Approval)

**DocType Name:** `Document Approval`

**Fields:**
```json
{
  "document_number": {
    "fieldtype": "Data",
    "label": "מס' מסמך",
    "unique": true,
    "reqd": true
  },
  "contract": {
    "fieldtype": "Link",
    "label": "הסכם",
    "options": "Contract",
    "reqd": true
  },
  "document_type": {
    "fieldtype": "Select",
    "label": "סוג מסמך",
    "options": "אישור ביטוח\nניהול תקין\nפרטי בנק\nהסכם בט\"ל",
    "reqd": true
  },
  "attached_file": {
    "fieldtype": "Attach",
    "label": "קובץ מצורף"
  },
  "submission_date": {
    "fieldtype": "Date",
    "label": "תאריך הגשה",
    "default": "Today"
  },
  "expiry_date": {
    "fieldtype": "Date",
    "label": "תאריך תוקף"
  },
  "status": {
    "fieldtype": "Select",
    "label": "סטטוס",
    "options": "חסר\nהוגש\nתקין\nלא תקין",
    "default": "חסר"
  },
  "rejection_reason": {
    "fieldtype": "Text",
    "label": "סיבת דחייה",
    "depends_on": "eval:doc.status=='לא תקין'"
  },
  "reviewer": {
    "fieldtype": "Link",
    "label": "בודק",
    "options": "User"
  },
  "review_date": {
    "fieldtype": "Date",
    "label": "תאריך בדיקה"
  }
}
```

**Automation:**
- Auto-name: DOC-{document_number}
- Email notification on status change
- Portal access for service providers to upload
- Alert before document expiry

---

### 4.6 תלונה (Complaint)

**DocType Name:** `Complaint`

**Fields:**
```json
{
  "complaint_number": {
    "fieldtype": "Data",
    "label": "מס' תלונה",
    "unique": true,
    "read_only": true
  },
  "service_provider": {
    "fieldtype": "Link",
    "label": "נותן שירות",
    "options": "Service Provider"
  },
  "caregiver": {
    "fieldtype": "Link",
    "label": "מטפלת",
    "options": "Caregiver"
  },
  "complaint_source": {
    "fieldtype": "Select",
    "label": "מקור התלונה",
    "options": "מבוטח\nמטפלות\nצ\"מפ\nשיחה עם מבוטח\nיוזמת פקיד",
    "reqd": true
  },
  "complaint_date": {
    "fieldtype": "Date",
    "label": "תאריך התלונה",
    "default": "Today",
    "reqd": true
  },
  "description": {
    "fieldtype": "Text Editor",
    "label": "תיאור התלונה",
    "reqd": true
  },
  "status": {
    "fieldtype": "Select",
    "label": "סטטוס",
    "options": "חדשה\nבטיפול\nמוצדקת\nלא מוצדקת\nבמחלקה\nנסגרה",
    "default": "חדשה"
  },
  "severity": {
    "fieldtype": "Select",
    "label": "חומרה",
    "options": "נמוכה\nבינונית\nגבוהה",
    "default": "בינונית"
  },
  "assigned_to": {
    "fieldtype": "Link",
    "label": "מטופל על ידי",
    "options": "User"
  },
  "resolution": {
    "fieldtype": "Text Editor",
    "label": "פתרון/סיכום"
  },
  "closure_date": {
    "fieldtype": "Date",
    "label": "תאריך סגירה"
  }
}
```

**Child Tables:**
- Complaint Actions (פעולות טיפול)
- Attachments (מסמכים מצורפים)

**Automation:**
- Auto-name: COMP-.####
- Workflow: New → In Progress → Resolution → Closed
- Email notifications to assigned user
- SLA tracking

---

## 5. Implementation Tasks

### 5.1 Week 1: Setup & Core Entities

**Day 1-2: Environment Setup**
- [ ] Setup Frappe development environment using Docker
- [ ] Create custom app "nursing_management"
- [ ] Configure Git repository
- [ ] Setup development workspace

**Day 3-4: Service Provider Implementation**
- [ ] Create "Service Provider" DocType
- [ ] Define fields and validations
- [ ] Create List View and Form View
- [ ] Add permissions
- [ ] Test CRUD operations

**Day 5-7: Caregiver Implementation**
- [ ] Create "Caregiver" DocType
- [ ] Create Employment History child table
- [ ] Implement Link to Service Provider
- [ ] Create custom views
- [ ] Add validation logic
- [ ] Test relationships

### 5.2 Week 2: Organizational Structure

**Day 8-10: Branch & Contract**
- [ ] Create "Service Provider Branch" DocType
- [ ] Implement branch code validation
- [ ] Create "Contract" DocType
- [ ] Implement expiry alert logic
- [ ] Test 1:1 relationship between Branch and Contract

**Day 11-12: Document Management**
- [ ] Create "Document Approval" DocType
- [ ] Implement file upload functionality
- [ ] Create workflow for document approval
- [ ] Setup email notifications
- [ ] Test portal access for service providers

### 5.3 Week 3: Operations & Testing

**Day 13-15: Complaint System**
- [ ] Create "Complaint" DocType
- [ ] Implement complaint workflow
- [ ] Create child tables for actions
- [ ] Setup SLA and notifications
- [ ] Test complete complaint lifecycle

**Day 16-18: Integration & Testing**
- [ ] Test all entity relationships
- [ ] Create sample data for demo
- [ ] Test workflows end-to-end
- [ ] Performance testing
- [ ] Security testing

**Day 19-21: Documentation & Demo**
- [ ] Create user documentation
- [ ] Create technical documentation
- [ ] Prepare demo scenarios
- [ ] Record demo video
- [ ] Final POC presentation

---

## 6. Technical Considerations

### 6.1 Naming Conventions
- DocType names: English (for compatibility)
- Field labels: Hebrew (for users)
- Field names: English snake_case
- Auto-naming: Use prefixes (SP-, CG-, CON-, etc.)

### 6.2 Permissions Strategy
- **System Manager:** Full access to all DocTypes
- **Department Manager:** Full access, can assign tasks
- **Department Staff:** Read/Write access, limited delete
- **Service Provider (Portal User):** Limited access to their own records

### 6.3 Workflow Configuration
- Contract approval workflow
- Document approval workflow
- Complaint resolution workflow

### 6.4 Automation & Alerts
- Contract expiry alerts (30 days before)
- Document expiry alerts
- Complaint SLA alerts
- Automatic email notifications

### 6.5 API & Integration
- REST API for all DocTypes (auto-generated by Frappe)
- Webhook support for external integrations
- Custom API endpoints for complex operations

---

## 7. Data Migration Strategy

### 7.1 Data Preparation
- Identify existing data sources
- Clean and normalize data
- Map fields to DocTypes
- Prepare CSV templates

### 7.2 Migration Order
1. Service Providers (no dependencies)
2. Caregivers (depends on Service Providers)
3. Branches (depends on Service Providers)
4. Contracts (depends on Branches)
5. Documents (depends on Contracts)
6. Complaints (depends on Service Providers & Caregivers)

### 7.3 Migration Tools
- Frappe Data Import Tool
- Custom Python scripts for complex transformations
- Validation scripts

---

## 8. Testing Strategy

### 8.1 Unit Testing
- Field validation tests
- Business logic tests
- Permission tests

### 8.2 Integration Testing
- Test entity relationships
- Test workflows
- Test email notifications
- Test API endpoints

### 8.3 User Acceptance Testing
- Create test scenarios
- Prepare test data
- Document test results
- Gather feedback

---

## 9. Success Criteria

### 9.1 Functional Requirements
- ✅ All 6 core DocTypes implemented
- ✅ Relationships working correctly
- ✅ Workflows functioning
- ✅ Alerts and notifications working
- ✅ Portal access for service providers

### 9.2 Technical Requirements
- ✅ Response time < 2 seconds for common operations
- ✅ Support for Hebrew RTL interface
- ✅ Mobile responsive design
- ✅ Data validation working
- ✅ Permissions enforced

### 9.3 Business Requirements
- ✅ Can track service providers and contracts
- ✅ Can manage complaints end-to-end
- ✅ Can track document compliance
- ✅ Can generate basic reports
- ✅ Demonstrates automation capabilities

---

## 10. Risks & Mitigation

### 10.1 Technical Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Docker environment issues | High | Medium | Use stable Frappe version, document setup steps |
| RTL/Hebrew issues | Medium | Low | Test early, use Frappe's built-in RTL support |
| Performance with large datasets | Medium | Medium | Implement pagination, optimize queries |
| Complex workflow issues | High | Medium | Start simple, iterate |

### 10.2 Project Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Scope creep | High | High | Strict scope definition, phase approach |
| Unclear requirements | High | Medium | Regular stakeholder reviews |
| Timeline delays | Medium | Medium | Buffer time, prioritize core features |

---

## 11. Next Steps After POC

### 11.1 Phase 2 Entities
- חשבונית (Invoice)
- הכשרה/קורס (Training/Course)
- מבוטח (Insured)
- תיעוד תקשורת (Communication Log)
- איש קשר (Contact Person)

### 11.2 Advanced Features
- Advanced reporting and dashboards
- Integration with external systems
- Mobile app development
- AI-powered insights
- Automated document processing

### 11.3 Production Deployment
- Production environment setup
- Data migration
- User training
- Gradual rollout
- Monitoring and support

---

## 12. Resources & References

### 12.1 Frappe Documentation
- https://frappeframework.com/docs
- https://docs.erpnext.com (for reference)
- https://github.com/frappe/frappe

### 12.2 Development Tools
- VS Code with Frappe extensions
- Git for version control
- Docker for containerization
- Postman for API testing

### 12.3 Project Files
- `entities-doc.md` - Detailed entity specifications
- `erd.md` - Entity relationship diagram
- `erd.pdf` - Visual ERD

---

## 13. Appendices

### Appendix A: Frappe DocType JSON Template
```json
{
  "doctype": "DocType",
  "name": "Service Provider",
  "module": "Nursing Management",
  "custom": 0,
  "is_submittable": 0,
  "track_changes": 1,
  "fields": [
    {
      "fieldname": "hp_number",
      "fieldtype": "Data",
      "label": "ח\"פ מספר",
      "unique": 1,
      "reqd": 1
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    }
  ]
}
```

### Appendix B: Sample Data
See separate file: `sample-data.json`

### Appendix C: API Examples
```python
# Get all service providers
frappe.get_list("Service Provider", fields=["name", "hp_number", "provider_name"])

# Create new complaint
doc = frappe.get_doc({
    "doctype": "Complaint",
    "service_provider": "SP-123456789",
    "complaint_source": "מבוטח",
    "description": "תיאור התלונה"
})
doc.insert()
```

---

## 14. Timeline Summary

| Week | Focus | Deliverables |
|------|-------|--------------|
| Week 1 | Setup + Core Entities | Service Provider, Caregiver |
| Week 2 | Structure + Documents | Branch, Contract, Document Approval |
| Week 3 | Operations + Testing | Complaint, Testing, Documentation |

**Total Duration:** 3 weeks (15 working days)

---

## Document Version Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-02 | Claude AI | Initial POC plan creation |
| 1.1 | 2025-12-02 | Claude AI | Added comprehensive development workflow section with Windows-specific guidance, Frappe best practices, and troubleshooting |

---

## Quick Reference Card

### Essential Commands
```bash
# Access container (VS Code terminal - PREFERRED)
# Already connected if using Dev Container

# From Windows (automation):
docker exec frappe_docker_devcontainer-frappe-1 bash -c "cd frappe-bench && <command>"

# List apps
bench --site development.localhost list-apps

# Clear cache (IMPORTANT - run after changes)
bench --site development.localhost clear-cache

# Migrate database
bench --site development.localhost migrate

# Build assets
bench build --app nursing_management

# View logs
tail -f logs/bench.log
```

### Access Points
- **Web UI**: http://localhost:8000
- **Admin Credentials**: Check site config or use default Administrator
- **Container**: `frappe_docker_devcontainer-frappe-1`
- **Bench Path**: `/workspace/development/frappe-bench`
- **App Path**: `/workspace/development/frappe-bench/apps/nursing_management`

### Development Flow
1. Create/edit DocType (UI recommended)
2. `bench --site development.localhost clear-cache`
3. Test in browser
4. Add Python logic (.py files)
5. Add JS (.js files) if needed
6. Clear cache & test

### Important Notes
- ✅ **Use VS Code Dev Container terminal** for all commands (BEST)
- ✅ **Always clear cache** after DocType changes
- ✅ **Work inside `/workspace/development/frappe-bench`**
- ❌ **Don't use `-it` flag** with docker exec on Windows
- ❌ **Don't run bench commands** outside bench directory

---

**End of Document**
