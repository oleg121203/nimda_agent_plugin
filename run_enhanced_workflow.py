#!/usr/bin/env python3
"""
Quick launcher for the Enhanced Interactive Workflow
Run this for a complete system build with deep analysis and error correction
"""

import os
import sys

# Add project to path
project_path = "/Users/dev/Documents/nimda_agent_plugin"
sys.path.append(project_path)


def main():
    print("🚀 NIMDA Agent - Quick Enhanced Workflow Launcher")
    print("=" * 60)

    # Change to project directory
    os.chdir(project_path)
    print(f"📁 Working directory: {project_path}")

    try:
        # Import and run the enhanced workflow
        from enhanced_interactive_workflow import EnhancedInteractiveWorkflow

        print("\n✨ Starting Enhanced Interactive Workflow...")
        print("   Features: Deep Analysis | Error Correction | Dev Mode Testing")

        # Create workflow with moderate pause duration for good balance
        workflow = EnhancedInteractiveWorkflow(project_path, pause_duration=1.5)

        # Run the complete workflow
        workflow.run_complete_workflow()

    except ImportError as e:
        print(f"❌ Failed to import workflow: {e}")
        print("💡 Make sure all required files are present")

    except Exception as e:
        print(f"💥 Workflow execution failed: {e}")
        print("🔧 Check the logs and try again")


if __name__ == "__main__":
    main()
