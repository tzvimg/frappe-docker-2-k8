#!/bin/bash

# Create new Frappe app with all prompts answered
docker exec frappe_docker_devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && printf 'Test Clinic\nTest Clinic app for testing\ntest@example.com\n' | bench new-app test_clinic --no-git"
