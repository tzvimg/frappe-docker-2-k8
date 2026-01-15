# Frappe v15 to v16 Migration Plan - Fresh Instance Approach

## Overview

**Project**: Siud (אגף סיעוד) - Nursing Management System
**Current Version**: Frappe v15
**Target Version**: Frappe v16
**Approach**: Fresh v16 installation with object recreation
**Estimated Downtime**: 4-8 hours (during cutover)

---

## Current App Inventory

### DocTypes (11 Total)
| # | DocType | Type | Priority |
|---|---------|------|----------|
| 1 | Supplier | Core Entity | Critical |
| 2 | Supplier Inquiry | Main Business | Critical |
| 3 | Activity Domain Category | Reference | High |
| 4 | Contact Person | Child/Related | High |
| 5 | Contact Person Role | Reference | Medium |
| 6 | Delegated Supplier | Related Entity | High |
| 7 | Delegated Supplier Scope | Reference | Medium |
| 8 | Supplier Activity Domain | Child Table | High |
| 9 | Supplier Role | Reference | Medium |
| 10 | Inquiry Topic Category | Hierarchical Ref | High |

### Custom Code
- **API Module**: `siud/api/supplier_portal.py` (581 lines)
- **Portal Pages**: 2 (supplier_dashboard, supplier-profile)
- **Workspace**: 1 (supplier_and_inquiry_management)
- **Translations**: 17 languages (Hebrew primary)

---

## Phase 1: Preparation & Backup ✅ COMPLETED

**Completed**: 2026-01-15

### 1.1 Document Current State
- [x] Export all DocType JSON definitions (10 DocTypes exported)
- [x] Document current database schema (see `v16_migration_backup/schema/`)
- [x] List all custom fields and configurations (none found - all in DocType JSONs)
- [x] Document workspace layout (exported to backup)
- [x] Document user roles and permissions (Supplier Portal User role documented)

### 1.2 Backup Everything
- [x] Full database backup (MariaDB dump with files)
- [x] Full file system backup of siud app (115 files, 620KB)
- [x] Backup site configuration files
- [x] Export fixtures (no fixtures configured; tables empty in dev environment)

### 1.3 Backup Location
All backups stored in: `v16_migration_backup/`

```
v16_migration_backup/
├── doctypes/           # All 10 DocType JSON definitions
│   └── doctype/        # Full doctype directory with .py, .js, .json files
├── schema/             # Database schema documentation
│   ├── SCHEMA_SUMMARY.md
│   ├── table_schemas.txt
│   └── siud_tables.txt
├── config/             # Configuration files
│   ├── CONFIGURATION_SUMMARY.md
│   ├── ROLES_AND_PERMISSIONS.md
│   ├── hooks.py
│   ├── site_config.json
│   ├── common_site_config.json
│   ├── workspace/
│   └── www/            # Portal pages
├── db_backup/          # Database backup (2026-01-15)
│   ├── *-database.sql.gz
│   ├── *-files.tar
│   ├── *-private-files.tar
│   └── *-site_config_backup.json
├── app_backup/         # Complete siud app copy
│   └── siud/
└── fixtures/           # Reference data (empty in dev)
    └── README.md
```

### 1.4 Backup Commands Used
```bash
# Inside container (site: siud.local)
cd /home/frappe/frappe-bench

# Database backup with files
bench --site siud.local backup --with-files

# App copied via docker cp
docker cp frappe-frappe-backend-1:/home/frappe/frappe-bench/apps/siud ./backup/
```

---

## Phase 2: Setup Fresh Frappe v16 Environment

### 2.1 System Requirements for v16
- Python: 3.11+ (3.12 recommended)
- Node.js: 20.x LTS
- MariaDB: 10.6+ or 11.x
- Redis: 7.x
- wkhtmltopdf: 0.12.6+

### 2.2 Docker Setup Options

**Option A: Update existing frappe_docker**
```bash
# Update frappe_docker to v16 branch
cd frappe_docker
git fetch origin
git checkout version-16
```

**Option B: Fresh frappe_docker clone (Recommended)**
```bash
# Clone fresh v16 frappe_docker
cd /home/tzvi/frappe
git clone --branch version-16 https://github.com/frappe/frappe_docker.git frappe_docker_v16
```

### 2.3 Create New Development Environment
```bash
cd frappe_docker_v16

# Copy development compose if needed
cp devcontainer-example/.devcontainer .

# Update docker-compose for v16
# Edit .devcontainer/docker-compose.yml to use v16 images
```

### 2.4 Initialize v16 Bench
```bash
# Inside new container
bench init frappe-bench --frappe-branch version-16
cd frappe-bench
bench new-site development.localhost
bench use development.localhost
```

---

## Phase 3: Recreate Siud App Structure

### 3.1 Create New App
```bash
bench new-app siud
# Answer prompts:
# App Title: Siud
# Description: Nursing Management System (אגף סיעוד)
# Publisher: Tzvi
# Email: tzvimg@gmail.com
# License: MIT
```

### 3.2 Install App on Site
```bash
bench --site development.localhost install-app siud
```

### 3.3 Copy Configuration Files
Files to copy from v15 backup:
- `pyproject.toml` (update Python version if needed)
- `.pre-commit-config.yaml`
- `.eslintrc`
- `.editorconfig`
- `license.txt`

### 3.4 Update pyproject.toml for v16
```toml
[project]
requires-python = ">=3.11"  # Updated for v16

[dependencies]
# "frappe~=16.0.0"  # Managed by bench
```

---

## Phase 4: Migrate DocTypes to v16

### 4.1 DocType Migration Order (Dependencies First)

**Round 1: Reference Tables (No Dependencies)**
1. Activity Domain Category
2. Contact Person Role
3. Delegated Supplier Scope
4. Supplier Role
5. Inquiry Topic Category

**Round 2: Child Tables**
6. Supplier Activity Domain

**Round 3: Main Entities**
7. Supplier
8. Contact Person
9. Delegated Supplier

**Round 4: Business DocTypes**
10. Supplier Inquiry

### 4.2 For Each DocType

```bash
# Option A: Copy JSON and recreate
# Copy the .json file from backup, then:
bench --site development.localhost migrate

# Option B: Manual recreation via UI
# Use Frappe's DocType builder in v16 UI
```

### 4.3 DocType Files to Migrate
For each DocType, copy these files:
- `<doctype>.json` - DocType definition
- `<doctype>.py` - Python controller (review for v16 compatibility)
- `<doctype>.js` - Client script (review for v16 UI changes)
- `test_<doctype>.py` - Tests (update imports if needed)

### 4.4 v16 Breaking Changes to Check

| Change | Action Required |
|--------|-----------------|
| `frappe.whitelist()` | Still supported, no change |
| `frappe.get_doc()` | No change |
| `frappe.db.sql()` | No change |
| UI components | Review JS for new workspace API |
| Portal routes | Verify www/ structure |
| Workspace JSON | May need format updates |

---

## Phase 5: Migrate Custom Code

### 5.1 API Module
Copy and review: `siud/api/supplier_portal.py`

**Check for v16 compatibility:**
- [ ] Import statements
- [ ] `@frappe.whitelist()` decorators
- [ ] Response formats
- [ ] Permission checks

### 5.2 Portal Pages
Copy and review:
- `siud/www/supplier_dashboard.py`
- `siud/www/supplier-profile.py`

### 5.3 Hooks Configuration
Review and update `siud/hooks.py`:
- [ ] Portal menu configuration
- [ ] Role home pages
- [ ] Any deprecated hooks

### 5.4 Workspace
Copy: `siud/siud/workspace/supplier_and_inquiry_management.json`
- [ ] Verify workspace JSON format for v16
- [ ] Test workspace rendering

### 5.5 Translations
Copy all CSV files from `siud/translations/`:
- Primary: `he.csv` (Hebrew)
- Others: 16 additional language files

### 5.6 Templates & Static Assets
Copy directories:
- `siud/templates/`
- `siud/public/css/`
- `siud/public/js/`

---

## Phase 6: Data Migration

### 6.1 Export Data from v15
```bash
# In v15 container
bench --site development.localhost export-fixtures

# Or custom export script
bench --site development.localhost execute siud.utils.export_data
```

### 6.2 Data Export by DocType
```python
# Export script for each DocType
import frappe
import json

doctypes = [
    "Activity Domain Category",
    "Contact Person Role",
    "Delegated Supplier Scope",
    "Supplier Role",
    "Inquiry Topic Category",
    "Supplier",
    "Contact Person",
    "Delegated Supplier",
    "Supplier Inquiry"
]

for dt in doctypes:
    docs = frappe.get_all(dt, fields=["*"])
    with open(f"/tmp/{dt.replace(' ', '_')}.json", "w") as f:
        json.dump(docs, f, indent=2, default=str)
```

### 6.3 Import Data to v16
```python
# Import script
import frappe
import json

def import_doctype(doctype_name):
    file_path = f"/tmp/{doctype_name.replace(' ', '_')}.json"
    with open(file_path) as f:
        docs = json.load(f)

    for doc_data in docs:
        doc = frappe.get_doc({
            "doctype": doctype_name,
            **doc_data
        })
        doc.insert(ignore_permissions=True)

    frappe.db.commit()
```

### 6.4 Data Migration Order
1. Reference tables first (no foreign keys)
2. Parent entities (Supplier)
3. Child/related entities (Contact Person, Delegated Supplier)
4. Business documents (Supplier Inquiry)

---

## Phase 7: Testing & Validation

### 7.1 Functional Tests
- [ ] All DocTypes create/read/update/delete
- [ ] All API endpoints respond correctly
- [ ] Portal pages load and function
- [ ] Workspace displays correctly
- [ ] Hebrew RTL rendering works
- [ ] File attachments work

### 7.2 Data Validation
- [ ] Record counts match v15
- [ ] Data integrity verified
- [ ] Relationships intact
- [ ] No orphaned records

### 7.3 Permission Tests
- [ ] Role permissions work
- [ ] Portal user access correct
- [ ] Guest access for reference data

### 7.4 UI Tests
- [ ] v16 new UI renders correctly
- [ ] Hebrew labels display
- [ ] Status colors correct
- [ ] Charts/statistics work

### 7.5 Run Automated Tests
```bash
bench --site development.localhost run-tests --app siud
```

---

## Phase 8: Cutover & Go-Live

### 8.1 Pre-Cutover Checklist
- [ ] All tests passing
- [ ] Data migration verified
- [ ] Backup of v16 (before final data)
- [ ] User communication sent
- [ ] Rollback plan ready

### 8.2 Final Data Sync
```bash
# Export latest data from v15
# Import to v16
# Verify counts and integrity
```

### 8.3 DNS/Proxy Update
- [ ] Point domain to v16 instance
- [ ] Update any API integrations
- [ ] Clear CDN cache if applicable

### 8.4 Post-Cutover
- [ ] Verify production access
- [ ] Monitor error logs
- [ ] Keep v15 running for 1-2 weeks as fallback

---

## Phase 9: Cleanup

### 9.1 After Successful Cutover
- [ ] Archive v15 environment
- [ ] Update documentation
- [ ] Remove temporary migration scripts
- [ ] Update CLAUDE.md for v16

### 9.2 Update Project Files
- [ ] Update README.md
- [ ] Update CLAUDE.md version reference
- [ ] Commit all changes to git

---

## Rollback Plan

If critical issues occur:

1. **Immediate**: Switch DNS/proxy back to v15
2. **Data**: v15 remains untouched, no data loss
3. **Investigation**: Debug v16 issues
4. **Retry**: Fix and attempt migration again

---

## v16 New Features to Leverage

After successful migration, consider adopting:

| Feature | Benefit |
|---------|---------|
| 2x Performance | Faster page loads |
| New Workspace UI | Modern, cleaner interface |
| Improved Charts | Better visualization |
| Enhanced Search | Faster global search |
| Better Mobile | Improved responsive design |

---

## Timeline Tracking

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 1: Preparation | ✅ Complete | 2026-01-15 - All backups in v16_migration_backup/ |
| Phase 2: v16 Setup | ⬜ Pending | |
| Phase 3: App Structure | ⬜ Pending | |
| Phase 4: DocTypes | ⬜ Pending | |
| Phase 5: Custom Code | ⬜ Pending | |
| Phase 6: Data Migration | ⬜ Pending | |
| Phase 7: Testing | ⬜ Pending | |
| Phase 8: Cutover | ⬜ Pending | |
| Phase 9: Cleanup | ⬜ Pending | |

**Legend**: ⬜ Pending | 🔄 In Progress | ✅ Complete | ❌ Blocked

---

## Resources

- [Frappe v16 Release Notes](https://tcbinfotech.com/frappe-version-16-release-notes/)
- [Migration Guide (Community)](https://immanuelraj.dev/frappe-v15-to-v16-beta-migration-guide/)
- [ERPNext v16 Migration Wiki](https://github.com/frappe/erpnext/wiki/Migration-Guide-To-ERPNext-Version-16)
- [Frappe Forum Discussions](https://discuss.frappe.io/t/erpnext-hrms-frappe-framework-v16-release-dates/156349)
- [Official Frappe Releases](https://github.com/frappe/frappe/releases)

---

## Notes

- v16 Final Release: January 12, 2026
- Keep v15 as fallback for 1-2 weeks post-migration
- Test thoroughly in development before production cutover
- Hebrew RTL support should be improved in v16's new UI
