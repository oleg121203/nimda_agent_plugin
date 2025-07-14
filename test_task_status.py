#!/usr/bin/env python3
"""
Test script to check which tasks are marked as completed in DEV_PLAN.md
"""

import sys

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

from pathlib import Path

from dev_plan_manager import DevPlanManager

# Initialize the DevPlanManager
project_path = Path("/Users/dev/Documents/nimda_agent_plugin")
manager = DevPlanManager(project_path)

print("=== TASK COMPLETION STATUS ===")
for i, task in enumerate(manager.plan_structure["tasks"]):
    print(f"Task #{task['number']}: {task['title']}")
    print(f"  Completed: {task['completed']}")
    print(f"  Subtasks ({len(task['subtasks'])}):")
    for j, subtask in enumerate(task["subtasks"]):
        status = "✓" if subtask["completed"] else "✗"
        print(f"    {status} {subtask['text']}")
    print()

print(f"Total tasks: {len(manager.plan_structure['tasks'])}")
print(
    f"Completed tasks: {len([t for t in manager.plan_structure['tasks'] if t['completed']])}"
)
print(
    f"Incomplete tasks: {len([t for t in manager.plan_structure['tasks'] if not t['completed']])}"
)
