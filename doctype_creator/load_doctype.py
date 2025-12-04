#!/usr/bin/env python3
"""
DocType Creator - Main CLI

Validates and loads DocType from YAML specification into Frappe
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from validator import DocTypeValidator
from loader import DocTypeLoader
import frappe


def main():
    parser = argparse.ArgumentParser(
        description='Create Frappe DocType from YAML specification',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate only
  python load_doctype.py yaml_specs/service_provider.yaml --validate-only

  # Load DocType
  python load_doctype.py yaml_specs/service_provider.yaml

  # Overwrite existing
  python load_doctype.py yaml_specs/service_provider.yaml --overwrite

  # Load to specific site
  python load_doctype.py yaml_specs/service_provider.yaml --site production.localhost
        """
    )

    parser.add_argument('yaml_file', help='Path to YAML specification file')
    parser.add_argument('--site', default='development.localhost', help='Frappe site name')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing DocType')
    parser.add_argument('--validate-only', action='store_true', help='Only validate, do not load')
    parser.add_argument('--no-validate', action='store_true', help='Skip validation (not recommended)')

    args = parser.parse_args()

    yaml_path = Path(args.yaml_file)

    if not yaml_path.exists():
        print(f"ERROR - File not found: {yaml_path}")
        sys.exit(1)

    # Step 1: Validation
    if not args.no_validate:
        print("=" * 60)
        print("STEP 1: YAML VALIDATION")
        print("=" * 60)

        validator = DocTypeValidator()
        is_valid, errors, warnings = validator.validate_yaml_file(yaml_path)

        if warnings:
            print("\nWARNING - Warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        if not is_valid:
            print("\nERROR - Validation failed with errors:")
            for error in errors:
                print(f"  - {error}")
            print("\nPlease fix the errors and try again.")
            sys.exit(1)

        print("\nSUCCESS - Validation passed!")

        if args.validate_only:
            sys.exit(0)

    # Step 2: Loading
    print("\n" + "=" * 60)
    print("STEP 2: LOADING DOCTYPE")
    print("=" * 60)

    try:
        # Initialize Frappe
        frappe.init(site=args.site)
        frappe.connect()

        loader = DocTypeLoader(site=args.site)
        result = loader.load_from_yaml(yaml_path, overwrite=args.overwrite)

        print("\n" + "=" * 60)
        print("SUCCESS")
        print("=" * 60)
        print(f"DocType '{result['name']}' has been created successfully!")
        print(f"\nAccess it at: http://localhost:8000/app/{result['name'].lower().replace(' ', '-')}")
        print("\nNext steps:")
        print(f"  1. Clear cache: bench --site {args.site} clear-cache")
        print("  2. View in UI: http://localhost:8000")
        print("  3. Add Python controller if needed")

        sys.exit(0)

    except Exception as e:
        print(f"\nERROR - Error loading DocType: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
