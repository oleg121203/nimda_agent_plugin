#!/usr/bin/env python3
"""
Force reload and execute tasks
"""

import sys

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

from pathlib import Path

from dev_plan_manager import DevPlanManager

# Initialize a fresh DevPlanManager instance to force reload
project_path = Path("/Users/dev/Documents/nimda_agent_plugin")

print("=== RELOADING PLAN AND CHECKING STATUS ===")
manager = DevPlanManager(project_path)

# Force a fresh reload by re-reading the file
manager._load_plan()

# Check completion status
for i, task in enumerate(manager.plan_structure["tasks"]):
    if task["number"] in [2, 3, 4, 5]:
        print(f"Task #{task['number']}: {task['title']}")
        print(f"  Completed: {task['completed']}")
        print(
            f"  Subtasks completed: {sum(1 for st in task['subtasks'] if st['completed'])}/{len(task['subtasks'])}"
        )

print("\n=== EXECUTING AGENT FILE TASKS ===")

# Force execute the real methods directly for incomplete tasks
task_methods = {
    2: ("Directory Structure", manager._create_directory_structure),
    3: ("Chat Agent", manager._create_chat_agent),
    4: ("Adaptive Thinker", manager._create_adaptive_thinker),
    5: ("macOS Integration", manager._setup_macos_integration),
}

# Also execute worker_agent and learning_module directly
print("\nExecuting Worker Agent:")
result = manager._create_worker_agent()
print(f"  Result: {result}")

print("\nExecuting Learning Module:")
result = manager._create_learning_module()
print(f"  Result: {result}")

for task_num, (task_name, method) in task_methods.items():
    print(f"\nExecuting {task_name} (#{task_num}):")
    try:
        result = method()
        print(f"  Result: {result}")
    except Exception as e:
        print(f"  Error: {e}")

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
