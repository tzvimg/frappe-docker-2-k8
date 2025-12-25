# Frappe Development Skill

This skill provides comprehensive guidance and tools for developing with the Frappe Framework in this project.

## What is This?

This is a **Claude Code skill** - a self-contained package of documentation and tools that AI agents automatically use when working with Frappe Framework in this repository.

## Contents

### Documentation
- **skill.md** - Complete Frappe development guide (17KB)
  - Container setup and environment
  - DocType creation methods
  - Workflow configuration
  - Hebrew (RTL) interface requirements
  - Validation patterns
  - Testing approaches
  - Troubleshooting guide

- **skill.json** - Skill metadata and triggers

### Helper Scripts

All scripts are designed to work from the project root and handle Docker container communication automatically.

| Script | Purpose |
|--------|---------|
| **setup.sh** | Initial setup - makes scripts executable, creates symlinks |
| **run_doctype_script.sh** | Execute DocType creation/test/verification scripts |
| **clear_cache.sh** | Clear Frappe cache (required after DocType changes) |
| **migrate.sh** | Run database migrations (required after JSON changes) |
| **console.sh** | Open Python console for testing and debugging |

## Quick Start

### First Time Setup

```bash
# From project root
.claude/skills/frappe-dev/setup.sh
```

This will:
1. Make all scripts executable
2. Optionally create symlinks in project root for convenience

### Using Helper Scripts

After setup, from project root:

```bash
# Execute DocType scripts
./run_doctype_script.sh creation.create_all_entities.create_all_doctypes

# Clear cache
./clear_cache.sh

# Run migrations
./migrate.sh

# Open Python console
./console.sh
```

## How It Works

### Automatic Activation

The skill automatically activates when:
- You mention "frappe", "doctype", "workflow", "siud"
- Working with service providers, caregivers, contracts
- Running bench commands
- Dealing with Hebrew/RTL interface
- Creating or modifying DocTypes

### What AI Agents Get

When activated, AI agents receive:
- Complete Frappe Framework context
- Exact command patterns for all operations
- Docker container paths and configuration
- Business rules and validation requirements
- Common pitfalls and solutions
- Hebrew label requirements
- Testing patterns

## Architecture

```
.claude/skills/frappe-dev/
├── README.md                    # This file
├── skill.json                   # Skill configuration
├── skill.md                     # Complete documentation (17KB)
├── setup.sh                     # Initial setup script
├── run_doctype_script.sh        # DocType script executor
├── clear_cache.sh               # Cache clearing utility
├── migrate.sh                   # Migration utility
└── console.sh                   # Python console launcher
```

## Benefits

### For Developers
- ✅ Single source of truth for all Frappe development
- ✅ Ready-to-use helper scripts
- ✅ No need to remember complex Docker commands
- ✅ Consistent workflow across the team

### For AI Agents
- ✅ Automatic context loading
- ✅ Exact command patterns
- ✅ Business rules and validations
- ✅ Container paths and configuration
- ✅ No guessing or struggling with commands

### For the Project
- ✅ Version-controlled documentation
- ✅ Self-contained tooling
- ✅ Reduced duplication (CLAUDE.md is minimal)
- ✅ Easy onboarding for new developers/agents

## Customization

### Changing Container/Site Names

If your Docker container or site name differs, edit the configuration at the top of each script:

```bash
CONTAINER="frappe_docker_devcontainer-frappe-1"
SITE="development.localhost"
APP="siud"
```

### Adding New Scripts

To add a new helper script:

1. Create the script in this directory
2. Make it executable: `chmod +x new_script.sh`
3. Document it in `skill.md`
4. Update this README
5. Optionally add to `setup.sh` for symlink creation

## Maintenance

### Updating Documentation

When Frappe development patterns change:

1. Update `skill.md` with new information
2. Add/modify helper scripts as needed
3. Keep CLAUDE.md minimal (it should just point here)
4. Version control all changes

### Keeping in Sync

The skill is the **single source of truth**. Don't duplicate information in:
- CLAUDE.md (keep minimal, reference skill)
- README files in other directories
- Comments in code

## Support

For issues or questions:
1. Check `skill.md` for comprehensive documentation
2. Review helper script comments
3. See CLAUDE.md for overview
4. Consult Frappe docs: https://frappeframework.com/docs

## Version

- **Version:** 1.0.0
- **Last Updated:** 2025-12-25
- **Frappe Version:** v15
- **Project:** Siud (Nursing Management System)
