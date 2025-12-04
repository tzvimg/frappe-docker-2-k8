"""
YAML DocType Specification Validator

Validates YAML files against schema and business rules before loading.
"""

import yaml
import jsonschema
import json
from pathlib import Path
from typing import Dict, List, Tuple
import re


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


class DocTypeValidator:
    """Validates DocType YAML specifications"""

    # Frappe reserved field names
    RESERVED_FIELDS = {
        'name', 'owner', 'creation', 'modified', 'modified_by',
        'docstatus', 'idx', 'parent', 'parentfield', 'parenttype',
        '_user_tags', '_comments', '_assign', '_liked_by'
    }

    # Valid field types for phase 1
    VALID_FIELD_TYPES = {
        'Data', 'Text', 'Text Editor', 'Small Text',
        'Select', 'Link', 'Date', 'Datetime',
        'Int', 'Float', 'Check', 'Attach',
        'Section Break', 'Column Break', 'Table'
    }

    # Valid naming rules
    VALID_NAMING_RULES = {'autoname', 'by_fieldname'}

    def __init__(self, schema_path: Path = None):
        """Initialize validator with JSON schema"""
        if schema_path is None:
            schema_path = Path(__file__).parent.parent / 'schemas' / 'doctype_schema.json'

        with open(schema_path) as f:
            self.schema = json.load(f)

    def validate_yaml_file(self, yaml_path: Path) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a YAML file

        Returns:
            (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        # Load YAML
        try:
            with open(yaml_path, encoding='utf-8') as f:
                spec = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return False, [f"Invalid YAML syntax: {e}"], []
        except Exception as e:
            return False, [f"Error reading file: {e}"], []

        # Layer 1: Schema validation
        schema_errors = self._validate_schema(spec)
        errors.extend(schema_errors)

        if errors:
            return False, errors, warnings

        # Layer 2: Business rules
        business_errors, business_warnings = self._validate_business_rules(spec)
        errors.extend(business_errors)
        warnings.extend(business_warnings)

        # Layer 3: Frappe compatibility
        frappe_errors, frappe_warnings = self._validate_frappe_compatibility(spec)
        errors.extend(frappe_errors)
        warnings.extend(frappe_warnings)

        is_valid = len(errors) == 0
        return is_valid, errors, warnings

    def _validate_schema(self, spec: Dict) -> List[str]:
        """Validate against JSON schema"""
        errors = []
        try:
            jsonschema.validate(instance=spec, schema=self.schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation failed: {e.message}")
        except Exception as e:
            errors.append(f"Schema validation error: {e}")
        return errors

    def _validate_business_rules(self, spec: Dict) -> Tuple[List[str], List[str]]:
        """Validate business rules"""
        errors = []
        warnings = []

        doctype = spec.get('doctype', {})

        # Validate naming
        naming_rule = doctype.get('naming_rule')
        if naming_rule not in self.VALID_NAMING_RULES:
            errors.append(f"Invalid naming_rule: {naming_rule}")

        if naming_rule == 'autoname':
            autoname = doctype.get('autoname', '')
            if not autoname.startswith('format:'):
                errors.append(f"autoname must start with 'format:' when using autoname rule")

        if naming_rule == 'by_fieldname':
            autoname = doctype.get('autoname', '')
            if not autoname.startswith('field:'):
                errors.append(f"autoname must start with 'field:' when using by_fieldname rule")
            else:
                field_name = autoname.replace('field:', '')
                field_names = [f['fieldname'] for f in doctype.get('fields', [])]
                if field_name not in field_names:
                    errors.append(f"autoname field '{field_name}' not found in fields")

        # Validate fields
        field_names = set()
        for idx, field in enumerate(doctype.get('fields', [])):
            fieldname = field.get('fieldname', '')
            fieldtype = field.get('fieldtype', '')
            label = field.get('label', '')

            # Check snake_case
            if fieldname and not re.match(r'^[a-z][a-z0-9_]*$', fieldname):
                errors.append(f"Field {idx}: fieldname '{fieldname}' must be snake_case")

            # Check uniqueness
            if fieldname in field_names:
                errors.append(f"Field {idx}: duplicate fieldname '{fieldname}'")
            field_names.add(fieldname)

            # Check reserved names
            if fieldname in self.RESERVED_FIELDS:
                errors.append(f"Field {idx}: '{fieldname}' is a reserved field name")

            # Check field type
            if fieldtype not in self.VALID_FIELD_TYPES:
                errors.append(f"Field {idx}: invalid fieldtype '{fieldtype}'")

            # Check label for non-break fields
            if fieldtype not in ['Section Break', 'Column Break']:
                if not label:
                    errors.append(f"Field {idx}: label required for fieldtype '{fieldtype}'")

            # Check options for Select/Link
            if fieldtype == 'Select':
                if not field.get('options'):
                    errors.append(f"Field {idx}: options required for Select field")

            if fieldtype == 'Link':
                if not field.get('options'):
                    errors.append(f"Field {idx}: options (target DocType) required for Link field")

            if fieldtype == 'Table':
                if not field.get('options'):
                    errors.append(f"Field {idx}: options (child DocType) required for Table field")

        return errors, warnings

    def _validate_frappe_compatibility(self, spec: Dict) -> Tuple[List[str], List[str]]:
        """Validate Frappe-specific compatibility"""
        errors = []
        warnings = []

        doctype = spec.get('doctype', {})

        # Check module (will warn if doesn't exist, but won't error)
        module = doctype.get('module')
        if not module:
            errors.append("module is required")

        # Check permissions
        permissions = doctype.get('permissions', [])
        if not permissions:
            warnings.append("No permissions defined - DocType will only be accessible to System Manager")

        for perm in permissions:
            role = perm.get('role')
            if not role:
                errors.append("Permission missing 'role' field")

        return errors, warnings


# CLI interface
def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Validate DocType YAML specification')
    parser.add_argument('yaml_file', help='Path to YAML file')
    parser.add_argument('--schema', help='Path to JSON schema (optional)')

    args = parser.parse_args()

    validator = DocTypeValidator(schema_path=args.schema if args.schema else None)
    is_valid, errors, warnings = validator.validate_yaml_file(Path(args.yaml_file))

    if warnings:
        print("WARNING - Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        print("ERROR - Errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print("SUCCESS - YAML validation passed!")
    sys.exit(0)


if __name__ == '__main__':
    main()
