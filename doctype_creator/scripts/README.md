# DocType Creator Scripts

Convenience scripts for working with the DocType Creator from the host machine.

## Prerequisites

- Docker must be running
- Frappe container must be running (`frappe_docker_devcontainer-frappe-1`)

## Scripts

### load.sh

Load a DocType from YAML file into Frappe.

**Usage:**
```bash
./scripts/load.sh <yaml_file> [site]
```

**Examples:**
```bash
# Load to default site (development.localhost)
./scripts/load.sh yaml_specs/service_provider.yaml

# Load to specific site
./scripts/load.sh yaml_specs/contract.yaml production.localhost
```

**Features:**
- Validates YAML before loading
- Automatically clears cache after loading
- Checks container is running
- Provides clear error messages

---

### validate.sh

Validate a YAML file without loading it into Frappe.

**Usage:**
```bash
./scripts/validate.sh <yaml_file>
```

**Examples:**
```bash
# Validate a YAML file
./scripts/validate.sh yaml_specs/service_provider.yaml

# Validate an example
./scripts/validate.sh templates/examples/simple_doctype.yaml
```

**Features:**
- Schema validation
- Business rules validation
- Frappe compatibility checks
- Clear pass/fail output

---

### batch_validate.sh

Validate all YAML files in a directory.

**Usage:**
```bash
./scripts/batch_validate.sh [directory]
```

**Examples:**
```bash
# Validate all files in yaml_specs (default)
./scripts/batch_validate.sh

# Validate all files in a specific directory
./scripts/batch_validate.sh templates/examples
```

**Features:**
- Batch processing
- Summary statistics
- Continues on error
- Lists all files with pass/fail status

---

## Quick Start Workflow

```bash
# 1. Validate your YAML file
./scripts/validate.sh yaml_specs/my_doctype.yaml

# 2. If validation passes, load it
./scripts/load.sh yaml_specs/my_doctype.yaml

# 3. Access in browser
# http://localhost:8000
```

## Troubleshooting

### Error: "Container not running"

**Problem:** The Frappe Docker container is not running.

**Solution:**
```bash
# Check container status
docker ps

# Start the container if needed
cd frappe_docker
docker-compose up -d
```

### Error: "File not found"

**Problem:** The YAML file path is incorrect.

**Solution:**
- Use relative paths from the doctype_creator directory
- Check the file exists: `ls yaml_specs/`

### Error: "DocType already exists"

**Problem:** A DocType with the same name already exists.

**Solution:**
- Use a different name in your YAML file, or
- Manually delete the existing DocType in Frappe UI, or
- Modify load.sh to add `--overwrite` flag (use with caution)

---

## Script Details

### Container Name

All scripts use the container name:
```
frappe_docker_devcontainer-frappe-1
```

If your container has a different name, edit the scripts and change the `CONTAINER_NAME` variable.

### Default Site

The default site is:
```
development.localhost
```

You can override this by passing the site name as the second argument to `load.sh`.

---

## Advanced Usage

### Overwrite Existing DocType

If you need to overwrite an existing DocType, modify the load.sh script to include the `--overwrite` flag:

```bash
# Edit load.sh and change the docker exec command:
docker exec -it $CONTAINER_NAME bash -c "
  cd /workspace/development/frappe-bench && \
  python /workspace/doctype_creator/load_doctype.py \
    /workspace/doctype_creator/$YAML_FILE \
    --site $SITE --overwrite && \
  bench --site $SITE clear-cache
"
```

**Warning:** This will delete the existing DocType and all its data!

### Validate Multiple Directories

```bash
# Validate all examples
./scripts/batch_validate.sh templates/examples

# Validate all specs
./scripts/batch_validate.sh yaml_specs

# Validate test fixtures
./scripts/batch_validate.sh tests/fixtures
```

---

## Integration with Development Workflow

These scripts integrate seamlessly with the DocType Creator workflow:

1. **Create YAML** (manually or with AI)
   ```bash
   # Edit or generate YAML
   vim yaml_specs/my_doctype.yaml
   ```

2. **Validate**
   ```bash
   ./scripts/validate.sh yaml_specs/my_doctype.yaml
   ```

3. **Load**
   ```bash
   ./scripts/load.sh yaml_specs/my_doctype.yaml
   ```

4. **Test in UI**
   - Open http://localhost:8000
   - Navigate to your new DocType
   - Create test records

5. **Iterate**
   - Modify YAML
   - Re-validate
   - Reload with overwrite

---

## See Also

- [Main README](../README.md) - Full documentation
- [Integration Tests](../tests/test_integration.py) - Automated testing
- [Sprint 3 Report](../SPRINT3_COMPLETION.md) - Implementation details

---
