"""
Python Controller Injector

Injects Python controller files into DocType directories
"""

import shutil
import os
from pathlib import Path
from typing import Optional, Tuple, List
import re


class InjectionError(Exception):
    """Raised when controller injection fails"""
    pass


class ControllerInjector:
    """Injects Python controllers into Frappe DocTypes"""

    def __init__(self, bench_path: Path = None):
        """
        Initialize injector

        Args:
            bench_path: Path to Frappe bench directory
        """
        if bench_path is None:
            # Default for Docker container
            bench_path = Path('/workspace/development/frappe-bench')
        self.bench_path = Path(bench_path)

    def inject_controller(
        self,
        doctype_name: str,
        controller_path: Path,
        app: str = 'nursing_management',
        backup: bool = True,
        validate: bool = True
    ) -> Tuple[bool, str]:
        """
        Inject Python controller into DocType directory

        Args:
            doctype_name: Name of DocType (e.g., "Service Provider")
            controller_path: Path to controller .py file
            app: App name (default: nursing_management)
            backup: Whether to backup existing controller
            validate: Whether to validate controller syntax

        Returns:
            Tuple of (success: bool, message: str)
        """
        print(f"Starting controller injection for DocType: {doctype_name}")

        # Step 1: Validate controller file exists
        if not controller_path.exists():
            raise InjectionError(f"Controller file not found: {controller_path}")

        # Step 2: Validate Python syntax if requested
        if validate:
            print("  - Validating Python syntax...")
            is_valid, errors = self._validate_controller_syntax(controller_path)
            if not is_valid:
                raise InjectionError(f"Controller validation failed:\n" + "\n".join(errors))
            print("    ✓ Syntax validation passed")

        # Step 3: Find target directory
        print("  - Locating DocType directory...")
        target_dir = self._find_doctype_directory(doctype_name, app)
        if not target_dir:
            raise InjectionError(
                f"DocType directory not found for '{doctype_name}' in app '{app}'\n"
                f"  Expected pattern: {self.bench_path}/apps/{app}/*/doctype/{self._to_snake_case(doctype_name)}/"
            )
        print(f"    ✓ Found: {target_dir}")

        # Step 4: Determine target filename
        doctype_dir_name = target_dir.name
        target_file = target_dir / f"{doctype_dir_name}.py"

        # Step 5: Backup existing controller if it exists
        if target_file.exists():
            if backup:
                backup_path = self._backup_controller(target_file)
                print(f"    ⚠ Backed up existing controller to: {backup_path}")
            else:
                print(f"    ⚠ Overwriting existing controller without backup")
        else:
            print("    - No existing controller found (creating new)")

        # Step 6: Copy controller file
        print("  - Copying controller file...")
        try:
            shutil.copy2(controller_path, target_file)
        except Exception as e:
            raise InjectionError(f"Failed to copy controller file: {e}")

        # Step 7: Verify injection
        if not target_file.exists():
            raise InjectionError("Controller injection failed - file not found after copy")

        # Step 8: Verify controller can be imported (basic check)
        if validate:
            print("  - Verifying controller class...")
            has_class = self._verify_controller_class(target_file, doctype_name)
            if not has_class:
                print("    ⚠ Warning: Controller file doesn't define expected class")
            else:
                print("    ✓ Controller class found")

        print(f"✓ Controller injected successfully: {target_file}")

        return True, str(target_file)

    def _find_doctype_directory(self, doctype_name: str, app: str) -> Optional[Path]:
        """
        Find the DocType directory in the app

        Args:
            doctype_name: DocType name (e.g., "Service Provider")
            app: App name

        Returns:
            Path to DocType directory or None if not found
        """
        snake_name = self._to_snake_case(doctype_name)

        # Search in app directory
        app_path = self.bench_path / 'apps' / app
        if not app_path.exists():
            return None

        # Look for doctype directory (could be in nested modules)
        # Pattern: apps/{app}/{module}/doctype/{doctype_name}/
        for doctype_base in app_path.glob('*/doctype'):
            doctype_dir = doctype_base / snake_name
            if doctype_dir.exists() and doctype_dir.is_dir():
                # Verify it's a valid DocType directory (has .json file)
                json_file = doctype_dir / f"{snake_name}.json"
                if json_file.exists():
                    return doctype_dir

        return None

    def _to_snake_case(self, name: str) -> str:
        """
        Convert DocType name to snake_case

        Args:
            name: DocType name (e.g., "Service Provider")

        Returns:
            snake_case name (e.g., "service_provider")
        """
        # Replace spaces and hyphens with underscores
        name = name.replace(' ', '_').replace('-', '_')
        # Insert underscore before uppercase letters
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        # Convert to lowercase
        return name.lower()

    def _validate_controller_syntax(self, controller_path: Path) -> Tuple[bool, List[str]]:
        """
        Validate Python syntax of controller file

        Args:
            controller_path: Path to controller file

        Returns:
            Tuple of (is_valid: bool, errors: List[str])
        """
        errors = []

        try:
            with open(controller_path, 'r', encoding='utf-8') as f:
                code = f.read()

            # Try to compile the code
            compile(code, str(controller_path), 'exec')

        except SyntaxError as e:
            errors.append(f"Syntax error at line {e.lineno}: {e.msg}")
        except Exception as e:
            errors.append(f"Validation error: {e}")

        return len(errors) == 0, errors

    def _verify_controller_class(self, controller_path: Path, doctype_name: str) -> bool:
        """
        Verify controller file defines expected class

        Args:
            controller_path: Path to controller file
            doctype_name: Expected DocType name

        Returns:
            True if class found, False otherwise
        """
        try:
            with open(controller_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for class definition matching DocType name
            # Expected pattern: class ServiceProvider(Document):
            class_name = doctype_name.replace(' ', '').replace('-', '')
            pattern = rf'class\s+{class_name}\s*\('

            return bool(re.search(pattern, content))

        except Exception:
            return False

    def _backup_controller(self, controller_path: Path) -> Path:
        """
        Backup existing controller file

        Args:
            controller_path: Path to controller file

        Returns:
            Path to backup file
        """
        # Generate backup filename with timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = controller_path.parent / f"{controller_path.stem}.{timestamp}.bak"

        # If backup already exists, add counter
        counter = 1
        while backup_path.exists():
            backup_path = controller_path.parent / f"{controller_path.stem}.{timestamp}_{counter}.bak"
            counter += 1

        shutil.copy2(controller_path, backup_path)
        return backup_path

    def list_backups(self, doctype_name: str, app: str = 'nursing_management') -> List[Path]:
        """
        List all backup files for a DocType controller

        Args:
            doctype_name: DocType name
            app: App name

        Returns:
            List of backup file paths
        """
        target_dir = self._find_doctype_directory(doctype_name, app)
        if not target_dir:
            return []

        doctype_dir_name = target_dir.name
        pattern = f"{doctype_dir_name}.*.bak"

        return sorted(target_dir.glob(pattern), reverse=True)

    def restore_backup(
        self,
        doctype_name: str,
        backup_path: Path,
        app: str = 'nursing_management'
    ) -> bool:
        """
        Restore a controller from backup

        Args:
            doctype_name: DocType name
            backup_path: Path to backup file
            app: App name

        Returns:
            True if successful
        """
        if not backup_path.exists():
            raise InjectionError(f"Backup file not found: {backup_path}")

        target_dir = self._find_doctype_directory(doctype_name, app)
        if not target_dir:
            raise InjectionError(f"DocType directory not found for '{doctype_name}'")

        doctype_dir_name = target_dir.name
        target_file = target_dir / f"{doctype_dir_name}.py"

        # Backup current file before restore
        if target_file.exists():
            self._backup_controller(target_file)

        # Restore from backup
        shutil.copy2(backup_path, target_file)
        print(f"✓ Restored controller from: {backup_path}")

        return True


# CLI interface
def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='Inject Python controller into Frappe DocType',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Inject controller
  python -m src.controller_injector "Service Provider" controllers/service_provider.py

  # Inject without backup
  python -m src.controller_injector "Service Provider" controllers/service_provider.py --no-backup

  # Skip validation
  python -m src.controller_injector "Service Provider" controllers/service_provider.py --no-validate

  # Specify app
  python -m src.controller_injector "Custom DocType" my_controller.py --app my_app

  # List backups
  python -m src.controller_injector "Service Provider" --list-backups

  # Restore from backup
  python -m src.controller_injector "Service Provider" --restore backup_file.bak
        """
    )

    parser.add_argument('doctype_name', help='DocType name (e.g., "Service Provider")')
    parser.add_argument('controller_file', nargs='?', help='Path to controller .py file')
    parser.add_argument('--app', default='nursing_management', help='App name (default: nursing_management)')
    parser.add_argument('--bench-path', help='Path to Frappe bench directory')
    parser.add_argument('--no-backup', action='store_true', help='Skip backup of existing controller')
    parser.add_argument('--no-validate', action='store_true', help='Skip controller validation')
    parser.add_argument('--list-backups', action='store_true', help='List all backup files')
    parser.add_argument('--restore', help='Restore from backup file')

    args = parser.parse_args()

    try:
        # Initialize injector
        bench_path = Path(args.bench_path) if args.bench_path else None
        injector = ControllerInjector(bench_path=bench_path)

        # List backups mode
        if args.list_backups:
            backups = injector.list_backups(args.doctype_name, app=args.app)
            if not backups:
                print(f"No backups found for DocType '{args.doctype_name}'")
                sys.exit(0)
            print(f"Backup files for '{args.doctype_name}':")
            for backup in backups:
                print(f"  - {backup.name}")
            sys.exit(0)

        # Restore mode
        if args.restore:
            backup_path = Path(args.restore)
            injector.restore_backup(args.doctype_name, backup_path, app=args.app)
            sys.exit(0)

        # Inject mode (default)
        if not args.controller_file:
            print("Error: controller_file is required for injection")
            parser.print_help()
            sys.exit(1)

        success, target_path = injector.inject_controller(
            args.doctype_name,
            Path(args.controller_file),
            app=args.app,
            backup=not args.no_backup,
            validate=not args.no_validate
        )

        print("\n" + "=" * 60)
        print("✓ CONTROLLER INJECTION COMPLETE")
        print("=" * 60)
        print(f"DocType: {args.doctype_name}")
        print(f"Controller: {target_path}")
        print("\nNext steps:")
        print("  1. Restart Frappe: bench restart")
        print("  2. Clear cache: bench --site development.localhost clear-cache")
        print("  3. Test in UI: http://localhost:8000")

        sys.exit(0)

    except InjectionError as e:
        print(f"\n❌ Controller injection failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
