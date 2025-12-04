"""
Unit tests for DocType YAML validator
"""

import unittest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from validator import DocTypeValidator


class TestDocTypeValidator(unittest.TestCase):
    """Test cases for DocTypeValidator"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = DocTypeValidator()
        self.fixtures_dir = Path(__file__).parent / 'fixtures'

    def test_valid_simple_yaml(self):
        """Test validation of a simple valid YAML"""
        yaml_path = self.fixtures_dir / 'valid_simple.yaml'
        is_valid, errors, warnings = self.validator.validate_yaml_file(yaml_path)

        self.assertTrue(is_valid, f"Expected valid YAML but got errors: {errors}")
        self.assertEqual(len(errors), 0)

    def test_invalid_missing_name(self):
        """Test detection of missing required 'name' field"""
        yaml_path = self.fixtures_dir / 'invalid_missing_name.yaml'
        is_valid, errors, warnings = self.validator.validate_yaml_file(yaml_path)

        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        # Check that error mentions 'name' requirement
        error_text = ' '.join(errors).lower()
        self.assertIn('name', error_text)

    def test_invalid_reserved_field(self):
        """Test detection of reserved field names"""
        yaml_path = self.fixtures_dir / 'invalid_reserved_field.yaml'
        is_valid, errors, warnings = self.validator.validate_yaml_file(yaml_path)

        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        # Check that error mentions reserved field
        error_text = ' '.join(errors).lower()
        self.assertIn('reserved', error_text)

    def test_invalid_bad_fieldname(self):
        """Test detection of non-snake_case field names"""
        yaml_path = self.fixtures_dir / 'invalid_bad_fieldname.yaml'
        is_valid, errors, warnings = self.validator.validate_yaml_file(yaml_path)

        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        # Check that error mentions the pattern or fieldname validation
        error_text = ' '.join(errors).lower()
        # Schema validation will catch the pattern mismatch
        self.assertTrue('providername' in error_text or 'snake_case' in error_text or 'match' in error_text)

    def test_invalid_select_no_options(self):
        """Test detection of Select field without options"""
        yaml_path = self.fixtures_dir / 'invalid_select_no_options.yaml'
        is_valid, errors, warnings = self.validator.validate_yaml_file(yaml_path)

        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        # Check that error mentions options requirement
        error_text = ' '.join(errors).lower()
        self.assertIn('options', error_text)

    def test_reserved_fields_list(self):
        """Test that reserved fields list is properly defined"""
        reserved = self.validator.RESERVED_FIELDS

        # Check some common reserved fields
        self.assertIn('name', reserved)
        self.assertIn('owner', reserved)
        self.assertIn('creation', reserved)
        self.assertIn('modified', reserved)
        self.assertIn('docstatus', reserved)

    def test_valid_field_types(self):
        """Test that valid field types list is properly defined"""
        field_types = self.validator.VALID_FIELD_TYPES

        # Check some common field types
        self.assertIn('Data', field_types)
        self.assertIn('Text', field_types)
        self.assertIn('Select', field_types)
        self.assertIn('Link', field_types)
        self.assertIn('Date', field_types)
        self.assertIn('Int', field_types)
        self.assertIn('Section Break', field_types)

    def test_valid_naming_rules(self):
        """Test that valid naming rules are properly defined"""
        naming_rules = self.validator.VALID_NAMING_RULES

        self.assertIn('autoname', naming_rules)
        self.assertIn('by_fieldname', naming_rules)

    def test_nonexistent_file(self):
        """Test handling of non-existent file"""
        yaml_path = self.fixtures_dir / 'does_not_exist.yaml'
        is_valid, errors, warnings = self.validator.validate_yaml_file(yaml_path)

        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)


class TestValidationLayers(unittest.TestCase):
    """Test individual validation layers"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = DocTypeValidator()

    def test_schema_validation_layer(self):
        """Test JSON schema validation layer"""
        # Valid spec
        valid_spec = {
            'doctype': {
                'name': 'Test',
                'module': 'Test Module',
                'naming_rule': 'autoname',
                'autoname': 'format:TEST-{####}',
                'fields': [
                    {
                        'fieldname': 'test_field',
                        'fieldtype': 'Data'
                    }
                ]
            }
        }
        errors = self.validator._validate_schema(valid_spec)
        self.assertEqual(len(errors), 0)

        # Invalid spec - missing required field
        invalid_spec = {
            'doctype': {
                'module': 'Test Module'
            }
        }
        errors = self.validator._validate_schema(invalid_spec)
        self.assertGreater(len(errors), 0)

    def test_business_rules_validation_layer(self):
        """Test business rules validation layer"""
        # Test autoname format validation
        spec_bad_autoname = {
            'doctype': {
                'naming_rule': 'autoname',
                'autoname': 'TEST-{####}',  # Missing 'format:' prefix
                'fields': []
            }
        }
        errors, warnings = self.validator._validate_business_rules(spec_bad_autoname)
        self.assertGreater(len(errors), 0)

        # Test by_fieldname validation
        spec_by_field = {
            'doctype': {
                'naming_rule': 'by_fieldname',
                'autoname': 'field:test_field',
                'fields': [
                    {
                        'fieldname': 'test_field',
                        'fieldtype': 'Data',
                        'label': 'Test'
                    }
                ]
            }
        }
        errors, warnings = self.validator._validate_business_rules(spec_by_field)
        self.assertEqual(len(errors), 0)

    def test_frappe_compatibility_layer(self):
        """Test Frappe compatibility validation layer"""
        # Test missing module
        spec_no_module = {
            'doctype': {
                'fields': []
            }
        }
        errors, warnings = self.validator._validate_frappe_compatibility(spec_no_module)
        self.assertGreater(len(errors), 0)

        # Test no permissions warning
        spec_no_perms = {
            'doctype': {
                'module': 'Test Module',
                'permissions': []
            }
        }
        errors, warnings = self.validator._validate_frappe_compatibility(spec_no_perms)
        self.assertGreater(len(warnings), 0)


if __name__ == '__main__':
    unittest.main()
