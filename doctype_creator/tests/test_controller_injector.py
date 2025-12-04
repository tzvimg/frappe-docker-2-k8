"""
Tests for controller_injector.py
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from controller_injector import ControllerInjector, InjectionError


class TestControllerInjector:
    """Test suite for ControllerInjector"""

    @pytest.fixture
    def temp_bench(self, tmp_path):
        """Create temporary bench structure for testing"""
        bench_path = tmp_path / "frappe-bench"
        bench_path.mkdir()

        # Create app structure
        app_path = bench_path / "apps" / "nursing_management" / "nursing_management" / "doctype"
        app_path.mkdir(parents=True)

        # Create a sample DocType directory
        doctype_dir = app_path / "service_provider"
        doctype_dir.mkdir()

        # Create .json file to mark it as valid DocType
        json_file = doctype_dir / "service_provider.json"
        json_file.write_text('{"name": "Service Provider"}')

        return bench_path

    @pytest.fixture
    def sample_controller(self, tmp_path):
        """Create sample controller file"""
        controller = tmp_path / "controller.py"
        controller.write_text("""
from frappe.model.document import Document

class ServiceProvider(Document):
    def validate(self):
        pass
""")
        return controller

    @pytest.fixture
    def invalid_controller(self, tmp_path):
        """Create invalid controller file (syntax error)"""
        controller = tmp_path / "invalid_controller.py"
        controller.write_text("""
def broken syntax here
    invalid indentation
""")
        return controller

    def test_to_snake_case(self, temp_bench):
        """Test DocType name to snake_case conversion"""
        injector = ControllerInjector(bench_path=temp_bench)

        assert injector._to_snake_case("Service Provider") == "service_provider"
        assert injector._to_snake_case("ServiceProvider") == "service_provider"
        assert injector._to_snake_case("service-provider") == "service_provider"
        assert injector._to_snake_case("MyDocType") == "my_doc_type"
        assert injector._to_snake_case("Simple") == "simple"

    def test_find_doctype_directory_success(self, temp_bench):
        """Test finding existing DocType directory"""
        injector = ControllerInjector(bench_path=temp_bench)

        doctype_dir = injector._find_doctype_directory("Service Provider", "nursing_management")

        assert doctype_dir is not None
        assert doctype_dir.name == "service_provider"
        assert doctype_dir.exists()

    def test_find_doctype_directory_not_found(self, temp_bench):
        """Test finding non-existent DocType directory"""
        injector = ControllerInjector(bench_path=temp_bench)

        doctype_dir = injector._find_doctype_directory("Nonexistent DocType", "nursing_management")

        assert doctype_dir is None

    def test_find_doctype_directory_wrong_app(self, temp_bench):
        """Test finding DocType in wrong app"""
        injector = ControllerInjector(bench_path=temp_bench)

        doctype_dir = injector._find_doctype_directory("Service Provider", "wrong_app")

        assert doctype_dir is None

    def test_validate_controller_syntax_valid(self, temp_bench, sample_controller):
        """Test validation of valid controller"""
        injector = ControllerInjector(bench_path=temp_bench)

        is_valid, errors = injector._validate_controller_syntax(sample_controller)

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_controller_syntax_invalid(self, temp_bench, invalid_controller):
        """Test validation of invalid controller"""
        injector = ControllerInjector(bench_path=temp_bench)

        is_valid, errors = injector._validate_controller_syntax(invalid_controller)

        assert is_valid is False
        assert len(errors) > 0
        assert "Syntax error" in errors[0] or "syntax" in errors[0].lower()

    def test_verify_controller_class_present(self, temp_bench, sample_controller):
        """Test verification when controller class is present"""
        injector = ControllerInjector(bench_path=temp_bench)

        has_class = injector._verify_controller_class(sample_controller, "Service Provider")

        assert has_class is True

    def test_verify_controller_class_missing(self, temp_bench, tmp_path):
        """Test verification when controller class is missing"""
        injector = ControllerInjector(bench_path=temp_bench)

        # Create controller without expected class
        controller = tmp_path / "no_class.py"
        controller.write_text("""
def some_function():
    pass
""")

        has_class = injector._verify_controller_class(controller, "Service Provider")

        assert has_class is False

    def test_inject_controller_success(self, temp_bench, sample_controller):
        """Test successful controller injection"""
        injector = ControllerInjector(bench_path=temp_bench)

        success, target_path = injector.inject_controller(
            "Service Provider",
            sample_controller,
            app="nursing_management",
            backup=False
        )

        assert success is True
        assert Path(target_path).exists()
        assert Path(target_path).name == "service_provider.py"

        # Verify content was copied
        content = Path(target_path).read_text()
        assert "class ServiceProvider" in content

    def test_inject_controller_with_backup(self, temp_bench, sample_controller, tmp_path):
        """Test controller injection with backup of existing file"""
        injector = ControllerInjector(bench_path=temp_bench)

        # First injection
        success1, target_path1 = injector.inject_controller(
            "Service Provider",
            sample_controller,
            app="nursing_management",
            backup=False
        )
        assert success1 is True

        # Create different controller
        new_controller = tmp_path / "new_controller.py"
        new_controller.write_text("""
from frappe.model.document import Document

class ServiceProvider(Document):
    def validate(self):
        # New validation logic
        pass
""")

        # Second injection with backup
        success2, target_path2 = injector.inject_controller(
            "Service Provider",
            new_controller,
            app="nursing_management",
            backup=True
        )
        assert success2 is True

        # Check backup was created
        target_dir = Path(target_path2).parent
        backups = list(target_dir.glob("service_provider.*.bak"))
        assert len(backups) > 0

    def test_inject_controller_file_not_found(self, temp_bench, tmp_path):
        """Test injection with non-existent controller file"""
        injector = ControllerInjector(bench_path=temp_bench)

        nonexistent = tmp_path / "nonexistent.py"

        with pytest.raises(InjectionError, match="Controller file not found"):
            injector.inject_controller(
                "Service Provider",
                nonexistent,
                app="nursing_management"
            )

    def test_inject_controller_invalid_syntax(self, temp_bench, invalid_controller):
        """Test injection with invalid controller syntax"""
        injector = ControllerInjector(bench_path=temp_bench)

        with pytest.raises(InjectionError, match="validation failed"):
            injector.inject_controller(
                "Service Provider",
                invalid_controller,
                app="nursing_management",
                validate=True
            )

    def test_inject_controller_skip_validation(self, temp_bench, invalid_controller):
        """Test injection skipping validation (should succeed)"""
        injector = ControllerInjector(bench_path=temp_bench)

        # Should succeed even with invalid syntax when validation is disabled
        success, target_path = injector.inject_controller(
            "Service Provider",
            invalid_controller,
            app="nursing_management",
            validate=False
        )

        assert success is True
        assert Path(target_path).exists()

    def test_inject_controller_doctype_not_found(self, temp_bench, sample_controller):
        """Test injection for non-existent DocType"""
        injector = ControllerInjector(bench_path=temp_bench)

        with pytest.raises(InjectionError, match="DocType directory not found"):
            injector.inject_controller(
                "Nonexistent DocType",
                sample_controller,
                app="nursing_management"
            )

    def test_list_backups(self, temp_bench, sample_controller, tmp_path):
        """Test listing backup files"""
        injector = ControllerInjector(bench_path=temp_bench)

        # Create initial controller
        injector.inject_controller(
            "Service Provider",
            sample_controller,
            app="nursing_management",
            backup=False
        )

        # Create multiple backups
        new_controller = tmp_path / "new.py"
        new_controller.write_text("# New version")

        for i in range(3):
            injector.inject_controller(
                "Service Provider",
                new_controller,
                app="nursing_management",
                backup=True
            )

        # List backups
        backups = injector.list_backups("Service Provider", app="nursing_management")

        assert len(backups) == 3
        # Should be sorted in reverse order (newest first)
        for backup in backups:
            assert backup.suffix == ".bak"
            assert "service_provider" in backup.name

    def test_restore_backup(self, temp_bench, sample_controller, tmp_path):
        """Test restoring controller from backup"""
        injector = ControllerInjector(bench_path=temp_bench)

        # Create initial controller with specific content
        original_content = """
from frappe.model.document import Document

class ServiceProvider(Document):
    def validate(self):
        # Original version
        pass
"""
        original_controller = tmp_path / "original.py"
        original_controller.write_text(original_content)

        injector.inject_controller(
            "Service Provider",
            original_controller,
            app="nursing_management",
            backup=False
        )

        # Overwrite with new controller
        new_controller = tmp_path / "new.py"
        new_controller.write_text("# New version")

        injector.inject_controller(
            "Service Provider",
            new_controller,
            app="nursing_management",
            backup=True
        )

        # Get backup files
        backups = injector.list_backups("Service Provider", app="nursing_management")
        assert len(backups) > 0

        # Restore from backup
        success = injector.restore_backup(
            "Service Provider",
            backups[0],
            app="nursing_management"
        )

        assert success is True

        # Verify restored content
        target_dir = injector._find_doctype_directory("Service Provider", "nursing_management")
        target_file = target_dir / "service_provider.py"
        restored_content = target_file.read_text()

        assert "Original version" in restored_content

    def test_restore_backup_file_not_found(self, temp_bench, tmp_path):
        """Test restore with non-existent backup file"""
        injector = ControllerInjector(bench_path=temp_bench)

        nonexistent = tmp_path / "nonexistent.bak"

        with pytest.raises(InjectionError, match="Backup file not found"):
            injector.restore_backup(
                "Service Provider",
                nonexistent,
                app="nursing_management"
            )

    def test_backup_controller(self, temp_bench, sample_controller):
        """Test backup mechanism"""
        injector = ControllerInjector(bench_path=temp_bench)

        # First inject
        success, target_path = injector.inject_controller(
            "Service Provider",
            sample_controller,
            app="nursing_management",
            backup=False
        )

        # Backup the file
        target_file = Path(target_path)
        backup_path = injector._backup_controller(target_file)

        assert backup_path.exists()
        assert backup_path.suffix == ".bak"
        assert "service_provider" in backup_path.name

        # Verify backup content matches original
        original_content = target_file.read_text()
        backup_content = backup_path.read_text()
        assert original_content == backup_content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
