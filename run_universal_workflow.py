#!/usr/bin/env python3
"""
Universal Creative Workflow Launcher
- No hardcoded requirements
- Auto-detects environment
- Adapts to any project type
"""

import os
import subprocess
import sys
from pathlib import Path


def detect_python_command():
    """Detect the best Python command to use"""
    python_commands = [
        "python3",
        "python",
        "python3.11",
        "python3.10",
        "python3.9",
        "python3.8",
    ]

    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"🐍 Found {cmd}: {version}")
                return cmd
        except FileNotFoundError:
            continue

    print("❌ No Python installation found")
    return None


def main():
    print("🚀 Universal Creative Workflow - Auto-Launching")
    print("=" * 50)

    # Auto-detect project path
    project_path = Path(__file__).parent.resolve()
    print(f"📁 Project: {project_path}")

    # Auto-detect Python
    python_cmd = detect_python_command()
    if not python_cmd:
        print("Please install Python 3.8+ to continue")
        sys.exit(1)

    # Change to project directory
    os.chdir(project_path)
    sys.path.append(str(project_path))

    try:
        # Import and run universal workflow
        print("🔄 Loading Universal Creative Workflow...")
        from universal_creative_workflow import UniversalCreativeWorkflow

        # Create workflow with adaptive settings
        workflow = UniversalCreativeWorkflow(str(project_path), pause_duration=1.5)

        # Register some example creative hooks
        def example_creative_hook(context):
            """Example creative hook for demonstration"""
            action = context.get("action")
            if action == "create_component":
                print(
                    f"🎨 Creative hook activated for: {context.get('component_name')}"
                )
                return True
            return False

        # Register the hook
        workflow.register_creative_hook("creative_solution", example_creative_hook)

        # Run the complete universal workflow
        print("🎯 Starting Universal Creative Development...")
        workflow.run_universal_workflow()

        print("\n✨ Launch complete! Your project is ready.")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all required modules are available")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
