#!/usr/bin/env python3
"""
Enhanced interactive development plan execution with file creation verification
"""

import sys
import time

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

from pathlib import Path

from dev_plan_manager import DevPlanManager


def main():
    print("🚀 NIMDA Agent - Enhanced Interactive Development Plan")
    print("=" * 60)

    # Initialize the DevPlanManager
    project_path = Path("/Users/dev/Documents/nimda_agent_plugin")
    manager = DevPlanManager(project_path)

    print(f"📁 Project path: {project_path}")
    print(f"📋 Total tasks: {len(manager.plan_structure['tasks'])}")

    # Show files before execution
    print("\n📄 Current agent files:")
    agent_files = [
        "chat_agent.py",
        "worker_agent.py",
        "adaptive_thinker.py",
        "learning_module.py",
        "macos_integration.py",
    ]
    for filename in agent_files:
        if Path(filename).exists():
            print(f"   ✓ {filename} exists")
        else:
            print(f"   ✗ {filename} missing")

    print("\n📂 Current directories:")
    dirs = ["src", "tests", "docs", "data", "logs"]
    for dirname in dirs:
        if Path(dirname).exists():
            print(f"   ✓ {dirname}/ exists")
        else:
            print(f"   ✗ {dirname}/ missing")

    print("\n🔄 Let's force execution of key tasks...")
    print("=" * 60)

    # Force execute key tasks regardless of completion status
    key_tasks = [
        (2, "Visual Directory Structure", manager._create_directory_structure),
        (3, "Chat Agent", manager._create_chat_agent),
        (3, "Worker Agent", manager._create_worker_agent),
        (4, "Adaptive Thinker", manager._create_adaptive_thinker),
        (4, "Learning Module", manager._create_learning_module),
        (5, "macOS Integration", manager._setup_macos_integration),
    ]

    for task_num, task_name, method in key_tasks:
        print(f"\n🔧 Executing: {task_name}")
        try:
            result = method()
            if result:
                print(f"   ✅ {task_name} completed successfully!")
            else:
                print(f"   ❌ {task_name} failed!")
        except Exception as e:
            print(f"   💥 Exception in {task_name}: {e}")

        # Check what was created
        time.sleep(0.2)  # Small delay to ensure file system updates

    print("\n" + "=" * 60)
    print("🔍 Verification after execution:")

    # Check files after execution
    print("\n📄 Agent files after execution:")
    for filename in agent_files:
        if Path(filename).exists():
            size = Path(filename).stat().st_size
            print(f"   ✓ {filename} ({size} bytes)")
        else:
            print(f"   ✗ {filename} still missing")

    print("\n📂 Directories after execution:")
    for dirname in dirs:
        if Path(dirname).exists():
            print(f"   ✓ {dirname}/ created")
        else:
            print(f"   ✗ {dirname}/ still missing")

    # Test importing the created files
    print("\n🧪 Testing imports:")
    for filename in agent_files:
        if Path(filename).exists():
            module_name = filename[:-3]  # Remove .py
            try:
                exec(f"import {module_name}")
                print(f"   ✓ {module_name} imports successfully")
            except Exception as e:
                print(f"   ✗ {module_name} import error: {e}")
        else:
            print(f"   ⚠️  {filename} doesn't exist to test")

    print("\n🎉 Enhanced execution completed!")
    print("🚀 All key NIMDA Agent components should now be ready!")


if __name__ == "__main__":
    main()
