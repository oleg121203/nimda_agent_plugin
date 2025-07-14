#!/usr/bin/env python3
"""
Direct execution test for agent file creation
"""

import sys

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

from pathlib import Path

from dev_plan_manager import DevPlanManager

# Initialize the DevPlanManager
project_path = Path("/Users/dev/Documents/nimda_agent_plugin")
manager = DevPlanManager(project_path)

print("=== EXECUTING SPECIFIC TASKS ===")

# Find tasks that contain agent file creation
tasks_to_execute = []
for task in manager.plan_structure["tasks"]:
    title = task["title"].lower()
    if any(
        agent in title
        for agent in [
            "chat_agent",
            "worker_agent",
            "adaptive",
            "learning",
            "directory structure",
            "macos integration",
        ]
    ):
        tasks_to_execute.append(task)

for task in tasks_to_execute:
    print(f"\nExecuting Task #{task['number']}: {task['title']}")
    result = manager.execute_task(task["number"])
    print(f"  Result: {result}")

print("\n=== CHECKING FILES ===")
expected_files = [
    "chat_agent.py",
    "worker_agent.py",
    "adaptive_thinker.py",
    "learning_module.py",
    "macos_integration.py",
]
for filename in expected_files:
    file_path = project_path / filename
    if file_path.exists():
        print(f"✓ {filename} exists")
    else:
        print(f"✗ {filename} missing")

# Check directories
expected_dirs = ["src", "tests", "docs", "data", "logs"]
for dirname in expected_dirs:
    dir_path = project_path / dirname
    if dir_path.exists():
        print(f"✓ {dirname}/ exists")
    else:
        print(f"✗ {dirname}/ missing")
