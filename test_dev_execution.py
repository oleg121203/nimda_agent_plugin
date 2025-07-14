#!/usr/bin/env python3
"""
Test script for dev_plan_manager real execution
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

import logging

from dev_plan_manager import DevPlanManager

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(name)s - %(message)s")


def test_execution():
    """Test real execution of dev plan tasks"""
    project_path = Path(".")
    manager = DevPlanManager(project_path)

    print("=== DEV PLAN MANAGER TESTING ===")

    # Get plan status
    status = manager.get_plan_status()
    print(
        f"Plan status: {status['completed_subtasks']}/{status['total_subtasks']} subtasks completed"
    )

    # Find tasks with uncompleted subtasks
    print("\n=== TASKS WITH UNCOMPLETED SUBTASKS ===")
    for task in manager.plan_structure["tasks"]:
        uncompleted_subtasks = [st for st in task["subtasks"] if not st["completed"]]
        if uncompleted_subtasks:
            print(f"Task #{task['number']}: {task['title']}")
            for subtask in uncompleted_subtasks:
                print(f"  - [ ] {subtask['text']}")

    # Try to execute a specific task that has uncompleted subtasks
    print("\n=== EXECUTING WORKER AGENT TASK ===")
    for task in manager.plan_structure["tasks"]:
        if "worker_agent.py" in task["title"].lower() and not task["completed"]:
            print(f"Executing task #{task['number']}: {task['title']}")
            result = manager.execute_task(task["number"])
            print(f"Result: {result}")
            break

    # Check if files were created
    print("\n=== CHECKING CREATED FILES ===")
    files_to_check = [
        "chat_agent.py",
        "worker_agent.py",
        "adaptive_thinker.py",
        "learning_module.py",
        "macos_integration.py",
    ]
    for filename in files_to_check:
        file_path = project_path / filename
        exists = file_path.exists()
        print(f"{filename}: {'✓ EXISTS' if exists else '✗ NOT FOUND'}")


if __name__ == "__main__":
    test_execution()
