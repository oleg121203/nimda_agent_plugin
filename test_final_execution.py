#!/usr/bin/env python3
"""
Execute specific tasks that should create agent files
"""

import sys

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

from pathlib import Path

from dev_plan_manager import DevPlanManager

# Initialize the DevPlanManager
project_path = Path("/Users/dev/Documents/nimda_agent_plugin")
manager = DevPlanManager(project_path)

print("=== EXECUTING TASKS WITH SUBTASKS ===")

# Execute tasks #2, #3, #4, #5 (the agent file creation tasks)
task_numbers = [2, 3, 4, 5]

for task_num in task_numbers:
    print(f"\nExecuting Task #{task_num}:")
    result = manager.execute_task(task_num)
    print(f"  Success: {result['success']}")
    print(f"  Message: {result['message']}")
    if result.get("executed_subtasks"):
        print(f"  Executed subtasks: {len(result['executed_subtasks'])}")
    if result.get("failed_subtasks"):
        print(f"  Failed subtasks: {len(result['failed_subtasks'])}")

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
