#!/usr/bin/env python3
"""
YAML Validator - Standalone CLI

Validates DocType YAML specifications without loading into Frappe
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from validator import DocTypeValidator


def main():
    parser = argparse.ArgumentParser(
        description='Validate DocType YAML specification',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a YAML file
  python validate_yaml.py yaml_specs/service_provider.yaml

  # Use custom schema
  python validate_yaml.py yaml_specs/service_provider.yaml --schema custom_schema.json

  # Validate multiple files
  python validate_yaml.py yaml_specs/*.yaml
        """
    )

    parser.add_argument('yaml_files', nargs='+', help='Path to YAML file(s)')
    parser.add_argument('--schema', help='Path to JSON schema (optional)')

    args = parser.parse_args()

    # Initialize validator
    validator = DocTypeValidator(schema_path=Path(args.schema) if args.schema else None)

    total_files = len(args.yaml_files)
    passed_files = 0
    failed_files = 0

    for yaml_file in args.yaml_files:
        yaml_path = Path(yaml_file)

        if not yaml_path.exists():
            print(f"\nERROR - File not found: {yaml_path}")
            failed_files += 1
            continue

        print(f"\n{'=' * 60}")
        print(f"Validating: {yaml_path.name}")
        print('=' * 60)

        is_valid, errors, warnings = validator.validate_yaml_file(yaml_path)

        if warnings:
            print("\nWARNING - Warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        if not is_valid:
            print("\nERROR - Validation failed:")
            for error in errors:
                print(f"  - {error}")
            failed_files += 1
        else:
            print("\nSUCCESS - YAML validation passed!")
            passed_files += 1

    # Summary
    if total_files > 1:
        print(f"\n{'=' * 60}")
        print("SUMMARY")
        print('=' * 60)
        print(f"Total files: {total_files}")
        print(f"Passed: {passed_files}")
        print(f"Failed: {failed_files}")

    # Exit code
    sys.exit(0 if failed_files == 0 else 1)


if __name__ == '__main__':
    main()
