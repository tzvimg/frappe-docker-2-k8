"""
Integration Tests for DocType Creator

Tests the full workflow including validation and loading into Frappe.
These tests require a running Frappe container.
"""

import os
import sys
import subprocess
from pathlib import Path

# Test configuration
CONTAINER_NAME = "frappe_docker_devcontainer-frappe-1"
SITE_NAME = "development.localhost"


def check_container_running():
    """Check if the Frappe container is running"""
    result = subprocess.run(
        ["docker", "ps", "--filter", f"name={CONTAINER_NAME}", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    return CONTAINER_NAME in result.stdout


def docker_exec(command):
    """Execute a command in the Frappe container"""
    full_command = [
        "docker", "exec", CONTAINER_NAME, "bash", "-c", command
    ]
    result = subprocess.run(full_command, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def test_container_access():
    """Test 1: Check if container is accessible"""
    print("\n=== Test 1: Container Access ===")

    if not check_container_running():
        print(f"✗ FAILED: Container {CONTAINER_NAME} is not running")
        return False

    print(f"✓ PASSED: Container {CONTAINER_NAME} is running")
    return True


def test_volume_mount():
    """Test 2: Check if doctype_creator is mounted"""
    print("\n=== Test 2: Volume Mount ===")

    code, stdout, stderr = docker_exec("ls -la /workspace/doctype_creator")

    if code != 0:
        print("✗ FAILED: /workspace/doctype_creator not found in container")
        print(f"Error: {stderr}")
        return False

    print("✓ PASSED: /workspace/doctype_creator is accessible")

    # Check for key directories
    code, stdout, stderr = docker_exec(
        "ls /workspace/doctype_creator/ | grep -E '(src|schemas|templates)'"
    )

    if code != 0:
        print("✗ FAILED: Expected directories not found")
        return False

    print("✓ PASSED: All expected directories present")
    return True


def test_python_dependencies():
    """Test 3: Check if Python dependencies are available"""
    print("\n=== Test 3: Python Dependencies ===")

    # Test imports
    test_imports = [
        "import yaml",
        "import jsonschema",
        "import frappe"
    ]

    for import_stmt in test_imports:
        code, stdout, stderr = docker_exec(
            f"cd /workspace/development/frappe-bench && python -c '{import_stmt}'"
        )

        if code != 0:
            print(f"✗ FAILED: {import_stmt}")
            print(f"Error: {stderr}")
            return False

        print(f"✓ PASSED: {import_stmt}")

    return True


def test_validate_yaml_script():
    """Test 4: Test validate_yaml.py script"""
    print("\n=== Test 4: Validate YAML Script ===")

    # Test with valid fixture
    code, stdout, stderr = docker_exec(
        "cd /workspace/doctype_creator && "
        "python validate_yaml.py tests/fixtures/valid_simple.yaml"
    )

    if code != 0:
        print("✗ FAILED: Validation of valid file failed")
        print(f"Output: {stdout}")
        print(f"Error: {stderr}")
        return False

    print("✓ PASSED: Valid file accepted")

    # Test with invalid fixture
    code, stdout, stderr = docker_exec(
        "cd /workspace/doctype_creator && "
        "python validate_yaml.py tests/fixtures/invalid_missing_name.yaml"
    )

    if code == 0:
        print("✗ FAILED: Invalid file was accepted")
        return False

    print("✓ PASSED: Invalid file rejected")
    return True


def test_doctype_loading():
    """Test 5: Test DocType loading into Frappe"""
    print("\n=== Test 5: DocType Loading ===")

    # First, check if test DocType already exists and delete it
    print("Checking for existing test DocType...")
    code, stdout, stderr = docker_exec(
        f"cd /workspace/development/frappe-bench && "
        f"bench --site {SITE_NAME} console <<< \""
        "import frappe; "
        "frappe.connect(); "
        "if frappe.db.exists('DocType', 'Test Integration DocType'): "
        "    frappe.delete_doc('DocType', 'Test Integration DocType', force=True); "
        "    frappe.db.commit(); "
        "    print('Deleted existing test DocType')"
        "\""
    )

    # Create a test YAML file
    test_yaml = """doctype:
  name: "Test Integration DocType"
  module: "Nursing Management"
  naming_rule: "autoname"
  autoname: "format:TESTINT-{####}"
  track_changes: true
  description: "Integration test DocType"

  fields:
    - fieldname: "title"
      fieldtype: "Data"
      label: "Title"
      reqd: true
      in_list_view: true

    - fieldname: "description"
      fieldtype: "Text"
      label: "Description"

  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
      delete: 1
"""

    # Write test YAML to container
    print("Creating test YAML file...")
    code, stdout, stderr = docker_exec(
        f"cat > /workspace/doctype_creator/test_integration.yaml << 'EOF'\n{test_yaml}\nEOF"
    )

    if code != 0:
        print("✗ FAILED: Could not create test YAML file")
        print(f"Error: {stderr}")
        return False

    # Load the DocType
    print("Loading DocType into Frappe...")
    code, stdout, stderr = docker_exec(
        f"cd /workspace/development/frappe-bench && "
        f"python /workspace/doctype_creator/load_doctype.py "
        f"/workspace/doctype_creator/test_integration.yaml "
        f"--site {SITE_NAME}"
    )

    if code != 0:
        print("✗ FAILED: DocType loading failed")
        print(f"Output: {stdout}")
        print(f"Error: {stderr}")
        return False

    print("✓ PASSED: DocType loaded successfully")

    # Verify DocType exists in database
    print("Verifying DocType in database...")
    code, stdout, stderr = docker_exec(
        f"cd /workspace/development/frappe-bench && "
        f"bench --site {SITE_NAME} console <<< \""
        "import frappe; "
        "frappe.connect(); "
        "exists = frappe.db.exists('DocType', 'Test Integration DocType'); "
        "print('EXISTS' if exists else 'NOT_FOUND')"
        "\""
    )

    if "EXISTS" not in stdout:
        print("✗ FAILED: DocType not found in database")
        return False

    print("✓ PASSED: DocType verified in database")

    # Cleanup
    print("Cleaning up test DocType...")
    docker_exec(
        f"cd /workspace/development/frappe-bench && "
        f"bench --site {SITE_NAME} console <<< \""
        "import frappe; "
        "frappe.connect(); "
        "frappe.delete_doc('DocType', 'Test Integration DocType', force=True); "
        "frappe.db.commit()"
        "\""
    )
    docker_exec("rm /workspace/doctype_creator/test_integration.yaml")

    return True


def test_overwrite_scenario():
    """Test 6: Test overwrite functionality"""
    print("\n=== Test 6: Overwrite Scenario ===")

    # Create test YAML
    test_yaml = """doctype:
  name: "Test Overwrite DocType"
  module: "Nursing Management"
  naming_rule: "autoname"
  autoname: "format:TESTOVR-{####}"

  fields:
    - fieldname: "title"
      fieldtype: "Data"
      label: "Title"
      reqd: true

  permissions:
    - role: "System Manager"
      read: 1
      write: 1
      create: 1
"""

    # Write test YAML
    docker_exec(
        f"cat > /workspace/doctype_creator/test_overwrite.yaml << 'EOF'\n{test_yaml}\nEOF"
    )

    # Load first time
    print("Loading DocType (first time)...")
    code, stdout, stderr = docker_exec(
        f"cd /workspace/development/frappe-bench && "
        f"python /workspace/doctype_creator/load_doctype.py "
        f"/workspace/doctype_creator/test_overwrite.yaml "
        f"--site {SITE_NAME}"
    )

    if code != 0:
        print("✗ FAILED: First load failed")
        print(f"Error: {stderr}")
        return False

    print("✓ PASSED: First load successful")

    # Try loading again without --overwrite (should fail)
    print("Attempting load without --overwrite (should fail)...")
    code, stdout, stderr = docker_exec(
        f"cd /workspace/development/frappe-bench && "
        f"python /workspace/doctype_creator/load_doctype.py "
        f"/workspace/doctype_creator/test_overwrite.yaml "
        f"--site {SITE_NAME}"
    )

    if code == 0:
        print("✗ FAILED: Second load should have failed but succeeded")
        return False

    print("✓ PASSED: Second load correctly rejected")

    # Try loading again with --overwrite (should succeed)
    print("Attempting load with --overwrite (should succeed)...")
    code, stdout, stderr = docker_exec(
        f"cd /workspace/development/frappe-bench && "
        f"python /workspace/doctype_creator/load_doctype.py "
        f"/workspace/doctype_creator/test_overwrite.yaml "
        f"--site {SITE_NAME} --overwrite"
    )

    if code != 0:
        print("✗ FAILED: Overwrite load failed")
        print(f"Error: {stderr}")
        return False

    print("✓ PASSED: Overwrite successful")

    # Cleanup
    print("Cleaning up test DocType...")
    docker_exec(
        f"cd /workspace/development/frappe-bench && "
        f"bench --site {SITE_NAME} console <<< \""
        "import frappe; "
        "frappe.connect(); "
        "frappe.delete_doc('DocType', 'Test Overwrite DocType', force=True); "
        "frappe.db.commit()"
        "\""
    )
    docker_exec("rm /workspace/doctype_creator/test_overwrite.yaml")

    return True


def main():
    """Run all integration tests"""
    print("=" * 60)
    print("DocType Creator - Integration Tests")
    print("=" * 60)
    print(f"Container: {CONTAINER_NAME}")
    print(f"Site: {SITE_NAME}")
    print("=" * 60)

    tests = [
        ("Container Access", test_container_access),
        ("Volume Mount", test_volume_mount),
        ("Python Dependencies", test_python_dependencies),
        ("Validate YAML Script", test_validate_yaml_script),
        ("DocType Loading", test_doctype_loading),
        ("Overwrite Scenario", test_overwrite_scenario),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n✗ EXCEPTION in {test_name}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("=" * 60)

    if failed == 0:
        print("\n✓ ALL TESTS PASSED")
        return 0
    else:
        print(f"\n✗ {failed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
