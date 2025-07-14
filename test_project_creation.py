#!/usr/bin/env python3
"""Test new project creation from DEV_PLAN"""

import sys
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from dev_plan_manager import DevPlanManager

    print("🧪 Testing DEV_PLAN project creation...")

    # Create test manager
    current_path = Path(".")
    manager = DevPlanManager(current_path)

    print(f"📁 Current DEV_PLAN: {manager.dev_plan_file}")

    # Check if current DEV_PLAN has project creation instructions
    if manager.dev_plan_file.exists():
        with open(manager.dev_plan_file, "r", encoding="utf-8") as f:
            content = f.read()

        has_project_location = (
            "~/Projects/" in content and "Project Location:" in content
        )
        print(f"🎯 Contains project creation instructions: {has_project_location}")

        if has_project_location:
            print("🚀 Would create new project (test mode)")
            result = manager._extract_project_info(content)
            print(f"📋 Extracted info: {result}")
        else:
            print("📝 Would execute in current directory")
    else:
        print("❌ No DEV_PLAN.md found")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
