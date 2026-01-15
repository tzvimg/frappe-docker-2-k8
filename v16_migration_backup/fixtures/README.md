# Fixtures Export - Siud App (v15)

## Export Date: 2026-01-15

## Status
No fixtures configured in hooks.py.
All reference tables are empty (development environment).

## Tables Checked
- Activity Domain Category: 0 records
- Supplier Role: 0 records
- Contact Person Role: 0 records
- Delegated Supplier Scope: 0 records
- Inquiry Topic Category: 0 records

## Note
This appears to be a development environment with no production data.
Data migration (Phase 6) will need to be performed from the production environment
when migrating to v16.

## For Production Migration
When performing production migration, use these commands to export data:

```bash
# Inside container
bench --site siud.local export-fixtures --app siud

# Or manually export each DocType:
bench --site siud.local mariadb -e "SELECT * FROM \`tabSupplier\`;" > supplier_data.tsv
```
