#!/usr/bin/env python3
"""
Demo version of Enhanced Workflow with fast execution for testing
"""

import os
import sys

# Add project to path
project_path = "/Users/dev/Documents/nimda_agent_plugin"
sys.path.append(project_path)


def main():
    print("⚡ NIMDA Agent - Fast Demo Enhanced Workflow")
    print("=" * 55)
    print("🚀 Fast execution for testing and demonstration")

    # Change to project directory
    os.chdir(project_path)

    try:
        from enhanced_interactive_workflow import EnhancedInteractiveWorkflow

        print("\n✨ Starting Fast Demo Workflow...")

        # Create workflow with very short pauses for demo
        workflow = EnhancedInteractiveWorkflow(project_path, pause_duration=0.3)

        # Run the complete workflow
        workflow.run_complete_workflow()

        print("\n⚡ Fast demo completed!")

    except Exception as e:
        print(f"💥 Demo failed: {e}")


if __name__ == "__main__":
    main()
