#!/usr/bin/env python3
"""
Direct test of the real execution methods
"""

import sys

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

from pathlib import Path

from dev_plan_manager import DevPlanManager

# Initialize the DevPlanManager
project_path = Path("/Users/dev/Documents/nimda_agent_plugin")
manager = DevPlanManager(project_path)

print("=== TESTING REAL EXECUTION METHODS ===")

# Test directory creation
print("\n1. Testing _create_directory_structure:")
try:
    result = manager._create_directory_structure()
    print(f"  Result: {result}")
except Exception as e:
    print(f"  Error: {e}")

# Test chat agent creation
print("\n2. Testing _create_chat_agent:")
try:
    result = manager._create_chat_agent()
    print(f"  Result: {result}")
except Exception as e:
    print(f"  Error: {e}")

# Test worker agent creation
print("\n3. Testing _create_worker_agent:")
try:
    result = manager._create_worker_agent()
    print(f"  Result: {result}")
except Exception as e:
    print(f"  Error: {e}")

# Test adaptive thinker creation
print("\n4. Testing _create_adaptive_thinker:")
try:
    result = manager._create_adaptive_thinker()
    print(f"  Result: {result}")
except Exception as e:
    print(f"  Error: {e}")

# Test learning module creation
print("\n5. Testing _create_learning_module:")
try:
    result = manager._create_learning_module()
    print(f"  Result: {result}")
except Exception as e:
    print(f"  Error: {e}")

# Test macOS integration
print("\n6. Testing _setup_macos_integration:")
try:
    result = manager._setup_macos_integration()
    print(f"  Result: {result}")
except Exception as e:
    print(f"  Error: {e}")

print("\n=== CHECKING FILES AFTER DIRECT EXECUTION ===")
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
