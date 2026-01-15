# Roles and Permissions - Siud App (v15)

## Exported: 2026-01-15

## Custom Roles

| Role Name | Purpose |
|-----------|---------|
| Supplier Portal User | Portal access for suppliers |

## Users with Supplier Portal User Role

| User Email |
|------------|
| tzvimg@gmail.com |
| tzvimg2@gmail.com |

## DocType Permissions (Siud App)

### Supplier
| Role | Read | Write | Create | Delete | Submit | Cancel | Amend | If Owner |
|------|------|-------|--------|--------|--------|--------|-------|----------|
| System Manager | ✓ | ✓ | ✓ | ✓ | - | - | - | - |

### Supplier Inquiry
| Role | Read | Write | Create | Delete | Submit | Cancel | Amend | If Owner |
|------|------|-------|--------|--------|--------|--------|-------|----------|
| System Manager | ✓ | ✓ | ✓ | ✓ | - | - | - | - |
| Website User | ✓ | ✓ | ✓ | ✓ | - | - | - | - |

### Activity Domain Category
| Role | Read | Write | Create | Delete | Submit | Cancel | Amend | If Owner |
|------|------|-------|--------|--------|--------|--------|-------|----------|
| System Manager | ✓ | ✓ | ✓ | ✓ | - | - | - | - |

### Contact Person
| Role | Read | Write | Create | Delete | Submit | Cancel | Amend | If Owner |
|------|------|-------|--------|--------|--------|--------|-------|----------|
| System Manager | ✓ | ✓ | ✓ | ✓ | - | - | - | - |

### Delegated Supplier
| Role | Read | Write | Create | Delete | Submit | Cancel | Amend | If Owner |
|------|------|-------|--------|--------|--------|--------|-------|----------|
| System Manager | ✓ | ✓ | ✓ | ✓ | - | - | - | - |

### Inquiry Topic Category
| Role | Read | Write | Create | Delete | Submit | Cancel | Amend | If Owner |
|------|------|-------|--------|--------|--------|--------|-------|----------|
| System Manager | ✓ | ✓ | ✓ | ✓ | - | - | - | - |

### Supplier Role
| Role | Read | Write | Create | Delete | Submit | Cancel | Amend | If Owner |
|------|------|-------|--------|--------|--------|--------|-------|----------|
| System Manager | ✓ | ✓ | ✓ | ✓ | - | - | - | - |

## Notes

1. **Supplier Portal User** role:
   - No explicit DocPerm entries (relies on portal web forms)
   - Home page: `/supplier-dashboard`
   - Access managed via portal menu items in hooks.py

2. **Website User** role:
   - Has access to Supplier Inquiry (for web form submissions)

3. All reference tables (Activity Domain Category, Supplier Role, etc.) are managed by System Manager only

## Permission Strategy

The siud app uses a portal-based approach:
- Internal users (System Manager) manage data via Desk
- External users (Supplier Portal User) access via portal pages
- Portal permissions are handled by the API module (`supplier_portal.py`)
