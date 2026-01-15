# Configuration Summary - Siud App (v15)

## Exported: 2026-01-15

## Custom Fields
**Status:** None found - all fields are defined in DocType JSONs

## Property Setters
**Status:** None found

## Hooks Configuration (hooks.py)

### Active Configuration
| Setting | Value |
|---------|-------|
| App Name | siud |
| App Title | Siud |
| Publisher | Tzvi |
| License | MIT |

### Role Home Pages
| Role | Page |
|------|------|
| Supplier Portal User | /supplier-dashboard |

### Portal Menu Items (Hebrew)
| Title | Route | DocType Reference | Role |
|-------|-------|-------------------|------|
| דף הבית (Home) | /supplier-dashboard | - | Supplier Portal User |
| הפניות שלי (My Inquiries) | /supplier-inquiry-form/list | Supplier Inquiry | Supplier Portal User |
| פנייה חדשה (New Inquiry) | /supplier-inquiry-form/new | Supplier Inquiry | Supplier Portal User |
| פרופיל הספק (Supplier Profile) | /supplier-profile | Supplier | Supplier Portal User |

### Inactive/Commented Configuration
- No custom CSS/JS includes
- No scheduled tasks
- No document events
- No permission hooks
- No auth hooks

## Portal Pages (www/)

| File | Type | Description |
|------|------|-------------|
| supplier_dashboard.html | Template | Main supplier dashboard (17KB) |
| supplier_dashboard.py | Controller | Dashboard logic (3KB) |
| supplier-profile.html | Template | Supplier profile view (11KB) |
| supplier-profile.py | Controller | Profile logic (3KB) |

## Workspace

| Name | Location |
|------|----------|
| supplier_and_inquiry_management | siud/siud/workspace/ |

## API Module

| File | Description |
|------|-------------|
| siud/api/supplier_portal.py | Main API module (581 lines per plan) |

## Translations

17 language files in `siud/translations/`:
- Primary: he.csv (Hebrew)
- Others: ar, de, es, fr, it, ja, ko, nl, pl, pt, ru, th, tr, vi, zh

## Files Backed Up

```
v16_migration_backup/config/
├── hooks.py
├── workspace/
│   └── supplier_and_inquiry_management/
│       └── supplier_and_inquiry_management.json
└── www/
    ├── supplier_dashboard.html
    ├── supplier_dashboard.py
    ├── supplier-profile.html
    └── supplier-profile.py
```
