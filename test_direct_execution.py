#!/usr/bin/env python3
"""
Direct test for worker_agent creation
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

import logging

from dev_plan_manager import DevPlanManager

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(name)s - %(message)s")


def test_direct_execution():
    """Test direct execution of worker_agent creation"""
    project_path = Path(".")
    manager = DevPlanManager(project_path)

    print("=== DIRECT EXECUTION TEST ===")

    # Test individual creation methods directly
    print("\n1. Testing _create_worker_agent() directly:")
    try:
        result = manager._create_worker_agent()
        print(f"_create_worker_agent() result: {result}")
    except Exception as e:
        print(f"Error calling _create_worker_agent(): {e}")

    print("\n2. Testing _create_chat_agent() directly:")
    try:
        result = manager._create_chat_agent()
        print(f"_create_chat_agent() result: {result}")
    except Exception as e:
        print(f"Error calling _create_chat_agent(): {e}")

    print("\n3. Testing _create_learning_module() directly:")
    try:
        result = manager._create_learning_module()
        print(f"_create_learning_module() result: {result}")
    except Exception as e:
        print(f"Error calling _create_learning_module(): {e}")

    # Check if files were created
    print("\n=== CHECKING CREATED FILES ===")
    files_to_check = ["chat_agent.py", "worker_agent.py", "learning_module.py"]
    for filename in files_to_check:
        file_path = project_path / filename
        exists = file_path.exists()
        size = file_path.stat().st_size if exists else 0
        print(f"{filename}: {'✓ EXISTS' if exists else '✗ NOT FOUND'} ({size} bytes)")


if __name__ == "__main__":
    test_direct_execution()
