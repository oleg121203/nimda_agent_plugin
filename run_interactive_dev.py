#!/usr/bin/env python3
"""
Interactive full development plan execution with real-time progress
"""

import sys
import time

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

import logging
from pathlib import Path

from dev_plan_manager import DevPlanManager

# Setup console logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def main():
    print("🚀 NIMDA Agent - Interactive Full Development Plan Execution")
    print("=" * 60)

    # Initialize the DevPlanManager
    project_path = Path("/Users/dev/Documents/nimda_agent_plugin")
    manager = DevPlanManager(project_path)

    print(f"📁 Project path: {project_path}")
    print(f"📋 Total tasks: {len(manager.plan_structure['tasks'])}")
    print("=" * 60)

    # Show current status
    completed_count = len(
        [t for t in manager.plan_structure["tasks"] if t["completed"]]
    )
    print(
        f"📊 Current progress: {completed_count}/{len(manager.plan_structure['tasks'])} tasks completed"
    )
    print()

    # Execute all tasks with real-time feedback
    print("🔄 Starting full plan execution...")
    print("-" * 40)

    for i, task in enumerate(manager.plan_structure["tasks"], 1):
        task_num = task["number"]
        task_title = task["title"]

        print(
            f"\n[{i}/{len(manager.plan_structure['tasks'])}] 📝 Task #{task_num}: {task_title}"
        )

        if task["completed"]:
            print("   ✅ Already completed - skipping")
            continue

        if not task["subtasks"]:
            print("   ⚠️  No subtasks defined - marking as completed")
            task["completed"] = True
            continue

        print(f"   🔍 Found {len(task['subtasks'])} subtasks")

        # Execute task with detailed feedback
        try:
            result = manager.execute_task(task_num)

            if result["success"]:
                print("   ✅ Task completed successfully!")
                if result.get("executed_subtasks"):
                    for subtask in result["executed_subtasks"]:
                        print(f"      ✓ {subtask['text']}")
                if result.get("failed_subtasks"):
                    for subtask in result["failed_subtasks"]:
                        print(f"      ✗ {subtask['text']}")
            else:
                print(f"   ❌ Task failed: {result.get('message', 'Unknown error')}")

        except Exception as e:
            print(f"   💥 Exception: {e}")

        # Small delay for readability
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("🎉 Full plan execution completed!")

    # Final status check
    final_completed = len(
        [t for t in manager.plan_structure["tasks"] if t["completed"]]
    )
    print(
        f"📊 Final progress: {final_completed}/{len(manager.plan_structure['tasks'])} tasks completed"
    )

    # Check created files
    print("\n📁 Checking created files:")
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
            size = file_path.stat().st_size
            print(f"   ✓ {filename} ({size} bytes)")
        else:
            print(f"   ✗ {filename} missing")

    # Check directories
    print("\n📂 Checking directories:")
    expected_dirs = ["src", "tests", "docs", "data", "logs"]
    for dirname in expected_dirs:
        dir_path = project_path / dirname
        if dir_path.exists():
            print(f"   ✓ {dirname}/ exists")
        else:
            print(f"   ✗ {dirname}/ missing")

    print("\n🚀 NIMDA Agent development plan execution complete!")


if __name__ == "__main__":
    main()
