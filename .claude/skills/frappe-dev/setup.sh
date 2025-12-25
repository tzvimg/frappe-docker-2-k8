#!/bin/bash
# Setup Frappe development skill - make all scripts executable and create symlinks
# Usage: ./setup.sh

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"

echo "Frappe Development Skill Setup"
echo "==============================="
echo ""
echo "Skill directory: $SKILL_DIR"
echo "Project root: $PROJECT_ROOT"
echo ""

# Make all shell scripts executable
echo "Making scripts executable..."
chmod +x "$SKILL_DIR"/*.sh
echo "✓ All scripts are now executable"
echo ""

# Optionally create symlinks in project root for convenience
read -p "Create symlinks in project root for easy access? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating symlinks..."

    # Create symlinks
    ln -sf "$SKILL_DIR/run_doctype_script.sh" "$PROJECT_ROOT/run_doctype_script.sh" 2>/dev/null || true
    ln -sf "$SKILL_DIR/clear_cache.sh" "$PROJECT_ROOT/clear_cache.sh" 2>/dev/null || true
    ln -sf "$SKILL_DIR/migrate.sh" "$PROJECT_ROOT/migrate.sh" 2>/dev/null || true
    ln -sf "$SKILL_DIR/console.sh" "$PROJECT_ROOT/console.sh" 2>/dev/null || true

    echo "✓ Symlinks created in project root"
    echo ""
    echo "You can now run scripts from project root:"
    echo "  ./run_doctype_script.sh creation.create_all_entities.create_all_doctypes"
    echo "  ./clear_cache.sh"
    echo "  ./migrate.sh"
    echo "  ./console.sh"
else
    echo "Skipped symlink creation"
    echo ""
    echo "To run scripts, use full path:"
    echo "  .claude/skills/frappe-dev/run_doctype_script.sh <command>"
fi

echo ""
echo "✓ Setup complete!"
