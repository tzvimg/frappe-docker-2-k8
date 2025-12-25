# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

This repository contains a **Frappe Framework v15** implementation for a Nursing Management System (אגף סיעוד) for Israel's nursing care administration.

**IMPORTANT:** All Frappe development knowledge, tools, and resources are managed by the **frappe-dev skill**.

## Using the Frappe Development Skill

For ANY work involving:
- DocTypes (creating, modifying, querying)
- Frappe Framework operations
- Docker/bench commands
- Service providers, caregivers, contracts
- Hebrew (RTL) interface
- Workflows and permissions
- Database migrations
- Testing and verification

**→ Use the `frappe-dev` skill located in `.claude/skills/frappe-dev/`**

The skill contains:
- Complete development documentation
- Helper scripts for all common operations
- Command patterns and examples
- Business rules and validations
- Hebrew interface requirements
- Troubleshooting guides
- Architecture patterns

## Quick Setup

```bash
# Run the setup script to initialize helper scripts
.claude/skills/frappe-dev/setup.sh
```

This creates convenient symlinks for:
- `./run_doctype_script.sh` - Execute DocType creation scripts
- `./clear_cache.sh` - Clear Frappe cache
- `./migrate.sh` - Run database migrations
- `./console.sh` - Open Python console

## Key Resources

| Resource | Location |
|----------|----------|
| **Skill Documentation** | `.claude/skills/frappe-dev/skill.md` |
| **Helper Scripts** | `.claude/skills/frappe-dev/*.sh` |
| **DocType Scripts** | `doctypes_loading/` (creation, test_data, temp) |
| **Web Interface** | http://localhost:8000 |

## Docker Environment

- **Container:** `frappe_docker_devcontainer-frappe-1`
- **Site:** `development.localhost`
- **App:** `siud`
- **Bench Path:** `/workspace/development/frappe-bench` (inside container)

## Development Workflow

1. **Setup** (first time): `.claude/skills/frappe-dev/setup.sh`
2. **Create DocTypes**: `./run_doctype_script.sh <subdirectory>.<module>.<function>`
3. **Clear Cache**: `./clear_cache.sh`
4. **Migrate**: `./migrate.sh`
5. **Test**: `./console.sh`

## Additional Documentation

- Frappe Framework: https://frappeframework.com/docs
- Docker Setup: `frappe_docker/docs/`
- Skill Documentation: `.claude/skills/frappe-dev/skill.md`

---

**Note:** This file is intentionally kept minimal. All comprehensive Frappe development information is maintained in the frappe-dev skill to ensure consistency and avoid duplication.
