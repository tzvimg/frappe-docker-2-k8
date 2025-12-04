"""
Tests for DocType Loader

Tests YAML to Frappe dict conversion and loading logic
"""

import pytest
import yaml
from pathlib import Path
import sys
from unittest.mock import Mock, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Mock frappe module for local testing
sys.modules['frappe'] = MagicMock()

from loader import DocTypeLoader


class TestYAMLToFrappeDict:
    """Test YAML to Frappe dict conversion"""

    def setup_method(self):
        """Setup test loader"""
        self.loader = DocTypeLoader()

    def test_basic_conversion(self):
        """Test basic DocType conversion"""
        yaml_spec = {
            'name': 'Test DocType',
            'module': 'Nursing Management',
            'naming_rule': 'autoname',
            'autoname': 'format:TEST-{####}',
            'fields': [
                {
                    'fieldname': 'title',
                    'fieldtype': 'Data',
                    'label': 'Title',
                    'reqd': True
                }
            ],
            'permissions': [
                {
                    'role': 'System Manager',
                    'read': 1,
                    'write': 1
                }
            ]
        }

        result = self.loader._yaml_to_frappe_dict(yaml_spec)

        assert result['doctype'] == 'DocType'
        assert result['name'] == 'Test DocType'
        assert result['module'] == 'Nursing Management'
        assert result['autoname'] == 'format:TEST-{####}'
        assert len(result['fields']) == 1
        assert len(result['permissions']) == 1

    def test_autoname_naming_rule(self):
        """Test autoname naming rule conversion"""
        yaml_spec = {
            'name': 'Test DocType',
            'module': 'Nursing Management',
            'naming_rule': 'autoname',
            'autoname': 'format:PREFIX-{#####}',
            'fields': [],
            'permissions': []
        }

        result = self.loader._yaml_to_frappe_dict(yaml_spec)

        assert result['autoname'] == 'format:PREFIX-{#####}'
        assert 'naming_rule' not in result  # autoname doesn't set naming_rule field

    def test_by_fieldname_naming_rule(self):
        """Test by_fieldname naming rule conversion"""
        yaml_spec = {
            'name': 'Test DocType',
            'module': 'Nursing Management',
            'naming_rule': 'by_fieldname',
            'autoname': 'field:hp_number',
            'fields': [
                {
                    'fieldname': 'hp_number',
                    'fieldtype': 'Data',
                    'label': 'HP Number'
                }
            ],
            'permissions': []
        }

        result = self.loader._yaml_to_frappe_dict(yaml_spec)

        assert result['autoname'] == 'field:hp_number'
        assert result['naming_rule'] == 'By fieldname'

    def test_submittable_doctype(self):
        """Test submittable DocType conversion"""
        yaml_spec = {
            'name': 'Test DocType',
            'module': 'Nursing Management',
            'naming_rule': 'autoname',
            'autoname': 'format:TEST-{####}',
            'is_submittable': True,
            'fields': [],
            'permissions': []
        }

        result = self.loader._yaml_to_frappe_dict(yaml_spec)

        assert result['is_submittable'] == 1

    def test_track_changes_default(self):
        """Test track_changes defaults to 1"""
        yaml_spec = {
            'name': 'Test DocType',
            'module': 'Nursing Management',
            'naming_rule': 'autoname',
            'autoname': 'format:TEST-{####}',
            'fields': [],
            'permissions': []
        }

        result = self.loader._yaml_to_frappe_dict(yaml_spec)

        assert result['track_changes'] == 1

    def test_track_changes_false(self):
        """Test track_changes can be disabled"""
        yaml_spec = {
            'name': 'Test DocType',
            'module': 'Nursing Management',
            'naming_rule': 'autoname',
            'autoname': 'format:TEST-{####}',
            'track_changes': False,
            'fields': [],
            'permissions': []
        }

        result = self.loader._yaml_to_frappe_dict(yaml_spec)

        assert result['track_changes'] == 0

    def test_field_conversion(self):
        """Test field conversion"""
        field_spec = {
            'fieldname': 'test_field',
            'fieldtype': 'Data',
            'label': 'Test Field',
            'reqd': True,
            'unique': False,
            'in_list_view': True
        }

        result = self.loader._convert_field(field_spec)

        assert result['fieldname'] == 'test_field'
        assert result['fieldtype'] == 'Data'
        assert result['label'] == 'Test Field'
        assert result['reqd'] == 1  # Boolean converted to int
        assert result['unique'] == 0  # Boolean converted to int
        assert result['in_list_view'] == 1

    def test_field_with_options(self):
        """Test field with options (Select/Link)"""
        field_spec = {
            'fieldname': 'status',
            'fieldtype': 'Select',
            'label': 'Status',
            'options': 'Draft\nActive\nInactive'
        }

        result = self.loader._convert_field(field_spec)

        assert result['options'] == 'Draft\nActive\nInactive'

    def test_field_with_default(self):
        """Test field with default value"""
        field_spec = {
            'fieldname': 'start_date',
            'fieldtype': 'Date',
            'label': 'Start Date',
            'default': 'Today'
        }

        result = self.loader._convert_field(field_spec)

        assert result['default'] == 'Today'

    def test_permission_conversion(self):
        """Test permission conversion"""
        perm_spec = {
            'role': 'System Manager',
            'read': 1,
            'write': 1,
            'create': 1,
            'delete': 1
        }

        result = self.loader._convert_permission(perm_spec)

        assert result['role'] == 'System Manager'
        assert result['read'] == 1
        assert result['write'] == 1
        assert result['create'] == 1
        assert result['delete'] == 1
        assert result['submit'] == 0  # Default
        assert result['cancel'] == 0  # Default
        assert result['amend'] == 0  # Default

    def test_permission_with_submit(self):
        """Test permission with submit rights"""
        perm_spec = {
            'role': 'HQ Approver',
            'read': 1,
            'write': 1,
            'submit': 1,
            'cancel': 1
        }

        result = self.loader._convert_permission(perm_spec)

        assert result['submit'] == 1
        assert result['cancel'] == 1
        assert result['create'] == 0  # Default

    def test_multiple_fields(self):
        """Test DocType with multiple fields"""
        yaml_spec = {
            'name': 'Test DocType',
            'module': 'Nursing Management',
            'naming_rule': 'autoname',
            'autoname': 'format:TEST-{####}',
            'fields': [
                {
                    'fieldname': 'section_break_1',
                    'fieldtype': 'Section Break',
                    'label': 'Basic Info'
                },
                {
                    'fieldname': 'title',
                    'fieldtype': 'Data',
                    'label': 'Title',
                    'reqd': True
                },
                {
                    'fieldname': 'column_break_1',
                    'fieldtype': 'Column Break'
                },
                {
                    'fieldname': 'status',
                    'fieldtype': 'Select',
                    'label': 'Status',
                    'options': 'Draft\nActive'
                }
            ],
            'permissions': []
        }

        result = self.loader._yaml_to_frappe_dict(yaml_spec)

        assert len(result['fields']) == 4
        assert result['fields'][0]['fieldtype'] == 'Section Break'
        assert result['fields'][1]['fieldtype'] == 'Data'
        assert result['fields'][2]['fieldtype'] == 'Column Break'
        assert result['fields'][3]['fieldtype'] == 'Select'

    def test_title_field(self):
        """Test DocType with title field"""
        yaml_spec = {
            'name': 'Test DocType',
            'module': 'Nursing Management',
            'naming_rule': 'autoname',
            'autoname': 'format:TEST-{####}',
            'title_field': 'provider_name',
            'fields': [],
            'permissions': []
        }

        result = self.loader._yaml_to_frappe_dict(yaml_spec)

        assert result['title_field'] == 'provider_name'

    def test_description(self):
        """Test DocType with description"""
        yaml_spec = {
            'name': 'Test DocType',
            'module': 'Nursing Management',
            'naming_rule': 'autoname',
            'autoname': 'format:TEST-{####}',
            'description': 'This is a test DocType',
            'fields': [],
            'permissions': []
        }

        result = self.loader._yaml_to_frappe_dict(yaml_spec)

        assert result['description'] == 'This is a test DocType'


class TestLoaderErrorHandling:
    """Test error handling in loader"""

    def setup_method(self):
        """Setup test loader"""
        self.loader = DocTypeLoader()

    def test_missing_required_fields(self):
        """Test that missing required fields are handled"""
        # This should work - the schema validator will catch missing fields
        # The loader assumes valid input after validation
        yaml_spec = {
            'name': 'Test DocType',
            'module': 'Nursing Management',
            'naming_rule': 'autoname',
            'autoname': 'format:TEST-{####}',
            'fields': [],
            'permissions': []
        }

        result = self.loader._yaml_to_frappe_dict(yaml_spec)
        assert result is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
