"""
DocType Loader

Loads DocType from YAML specification into Frappe
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Optional
import frappe
from frappe import _


class LoadError(Exception):
    """Raised when loading fails"""
    pass


class DocTypeLoader:
    """Loads DocType from YAML specification"""

    def __init__(self, site: str = 'development.localhost'):
        """Initialize loader"""
        self.site = site
        self.dry_run = False

    def load_from_yaml(self, yaml_path: Path, overwrite: bool = False) -> Dict:
        """
        Load DocType from YAML file

        Args:
            yaml_path: Path to YAML file
            overwrite: If True, delete existing DocType before creating

        Returns:
            Created DocType document dict
        """
        print(f"\n[1/5] Loading YAML file: {yaml_path.name}")
        # Load YAML
        with open(yaml_path, encoding='utf-8') as f:
            spec = yaml.safe_load(f)

        doctype_spec = spec.get('doctype', {})
        doctype_name = doctype_spec.get('name')
        print(f"      DocType name: {doctype_name}")

        print(f"\n[2/5] Checking if DocType exists...")
        # Check if exists
        if frappe.db.exists("DocType", doctype_name):
            if overwrite:
                print(f"      DocType exists - deleting for overwrite...")
                self._delete_doctype(doctype_name)
                print(f"      Deleted successfully")
            else:
                raise LoadError(f"DocType '{doctype_name}' already exists. Use --overwrite to replace.")
        else:
            print(f"      DocType does not exist - proceeding with creation")

        print(f"\n[3/5] Converting YAML to Frappe DocType format...")
        # Convert to Frappe dict
        frappe_dict = self._yaml_to_frappe_dict(doctype_spec)
        field_count = len(doctype_spec.get('fields', []))
        perm_count = len(doctype_spec.get('permissions', []))
        print(f"      Fields: {field_count}")
        print(f"      Permissions: {perm_count} roles")

        print(f"\n[4/5] Creating DocType in Frappe...")
        # Create DocType
        doc = frappe.get_doc(frappe_dict)
        doc.insert(ignore_permissions=True)
        print(f"      DocType created successfully")

        print(f"\n[5/5] Committing to database...")
        frappe.db.commit()
        print(f"      Committed successfully")

        print(f"\nSUCCESS - DocType '{doctype_name}' created successfully")
        print(f"  - Total fields: {len(doc.fields)}")
        print(f"  - Permissions: {len(doc.permissions)} roles")
        print(f"  - Module: {doc.module}")

        return doc.as_dict()

    def _yaml_to_frappe_dict(self, spec: Dict) -> Dict:
        """Convert YAML spec to Frappe DocType dict"""

        frappe_dict = {
            'doctype': 'DocType',
            'name': spec['name'],
            'module': spec['module'],
            'custom': 0,
            'is_submittable': spec.get('is_submittable', 0),
            'track_changes': spec.get('track_changes', 1),
            'is_tree': spec.get('is_tree', 0),
        }

        # Handle naming
        naming_rule = spec.get('naming_rule')
        autoname = spec.get('autoname', '')

        if naming_rule == 'autoname':
            # Format: "format:SP-{#####}" -> autoname = "format:SP-{#####}"
            frappe_dict['autoname'] = autoname
        elif naming_rule == 'by_fieldname':
            # Format: "field:hp_number" -> autoname = "field:hp_number"
            frappe_dict['autoname'] = autoname
            frappe_dict['naming_rule'] = 'By fieldname'

        # Title field
        if spec.get('title_field'):
            frappe_dict['title_field'] = spec['title_field']

        # Description
        if spec.get('description'):
            frappe_dict['description'] = spec['description']

        # Fields
        frappe_dict['fields'] = []
        for field_spec in spec.get('fields', []):
            field_dict = self._convert_field(field_spec)
            frappe_dict['fields'].append(field_dict)

        # Permissions
        frappe_dict['permissions'] = []
        for perm_spec in spec.get('permissions', []):
            perm_dict = self._convert_permission(perm_spec)
            frappe_dict['permissions'].append(perm_dict)

        return frappe_dict

    def _convert_field(self, spec: Dict) -> Dict:
        """Convert YAML field spec to Frappe field dict"""
        field = {
            'fieldname': spec['fieldname'],
            'fieldtype': spec['fieldtype'],
        }

        # Optional properties
        optional_props = [
            'label', 'reqd', 'unique', 'read_only', 'hidden',
            'in_list_view', 'in_standard_filter', 'default',
            'description', 'options', 'length', 'precision', 'fetch_from'
        ]

        for prop in optional_props:
            if prop in spec:
                value = spec[prop]
                # Convert boolean to int for Frappe (reqd, unique, etc.)
                if isinstance(value, bool):
                    value = 1 if value else 0
                field[prop] = value

        return field

    def _convert_permission(self, spec: Dict) -> Dict:
        """Convert YAML permission spec to Frappe permission dict"""
        perm = {
            'role': spec['role'],
            'read': spec.get('read', 0),
            'write': spec.get('write', 0),
            'create': spec.get('create', 0),
            'delete': spec.get('delete', 0),
            'submit': spec.get('submit', 0),
            'cancel': spec.get('cancel', 0),
            'amend': spec.get('amend', 0),
        }
        return perm

    def _delete_doctype(self, doctype_name: str):
        """Delete existing DocType"""
        try:
            frappe.delete_doc("DocType", doctype_name, force=True)
            frappe.db.commit()
        except Exception as e:
            raise LoadError(f"Failed to delete existing DocType: {e}")


# CLI interface
def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Load DocType from YAML')
    parser.add_argument('yaml_file', help='Path to YAML file')
    parser.add_argument('--site', default='development.localhost', help='Frappe site name')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing DocType')
    parser.add_argument('--validate-only', action='store_true', help='Only validate, do not load')

    args = parser.parse_args()

    # Validate first
    if args.validate_only:
        from .validator import DocTypeValidator
        validator = DocTypeValidator()
        is_valid, errors, warnings = validator.validate_yaml_file(Path(args.yaml_file))

        if warnings:
            print("WARNING - Warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        if errors:
            print("ERROR - Validation errors:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)

        print("SUCCESS - Validation passed!")
        sys.exit(0)

    # Initialize Frappe
    frappe.init(site=args.site)
    frappe.connect()

    try:
        loader = DocTypeLoader(site=args.site)
        result = loader.load_from_yaml(Path(args.yaml_file), overwrite=args.overwrite)
        print(f"\nSUCCESS - DocType loaded successfully: {result['name']}")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR - Error loading DocType: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
