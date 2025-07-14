#!/usr/bin/env python3.11
"""
Quick launcher for Enhanced Workflow with Python 3.11
"""

import os
import sys

# Ensure Python 3.11
if sys.version_info < (3, 11):
    print("❌ Python 3.11 required")
    sys.exit(1)

# Add project to path
project_path = "/Users/dev/Documents/nimda_agent_plugin"
sys.path.append(project_path)
os.chdir(project_path)


def main():
    print("🐍 Python", sys.version)
    print("🚀 NIMDA Agent - Enhanced Workflow with 3-Level Tasks")

    try:
        from enhanced_interactive_workflow import EnhancedInteractiveWorkflow

        # Create workflow with shorter pauses for testing
        workflow = EnhancedInteractiveWorkflow(project_path, pause_duration=1.0)

        # Run the complete workflow
        workflow.run_complete_workflow()

    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
