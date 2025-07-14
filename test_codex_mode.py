#!/usr/bin/env python3
"""Test CODEX mode command processing"""

import sys
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from command_processor import CommandProcessor

    print("🧪 Testing CODEX MODE command detection...")

    # Create mock agent
    class MockAgent:
        def __init__(self):
            self.dev_plan_manager = MockDevPlanManager()
            self.git_manager = MockGitManager()

        def get_status(self):
            return {"dev_plan": {}, "git": {}}

    class MockDevPlanManager:
        def get_plan_status(self):
            return {"total_tasks": 5, "completed_tasks": 0}

        def execute_full_plan(self):
            return {"success": True, "executed_tasks": [1, 2, 3], "total_tasks": 5}

    class MockGitManager:
        def create_backup_branch(self):
            return {"success": True}

        def commit_changes(self, message):
            return {"success": True}

        def push_changes(self):
            return {"success": True}

    # Test command processor
    mock_agent = MockAgent()
    processor = CommandProcessor(mock_agent)

    # Test different commands
    test_commands = [
        "run full dev",  # Normal mode
        "codex run full dev",  # CODEX mode
        "codex execute full dev",  # CODEX mode
        "execute full dev",  # Normal mode
    ]

    for command in test_commands:
        print(f"\n🔍 Testing: '{command}'")
        command_type, params = processor._identify_command(command.lower())
        print(f"   Detected type: {command_type}")

        if command_type == "execute_codex_mode":
            print("   ✅ Will work with CURRENT agent (no new project)")
        elif command_type == "execute_full_plan":
            print("   📁 Will check for new project creation")
        else:
            print(f"   ❓ Other command type: {command_type}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
