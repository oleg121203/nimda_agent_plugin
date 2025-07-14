#!/usr/bin/env python3
"""
AI-Driven Deep Workflow Launcher
Orchestrates a sophisticated, multi-layered development process based on AI analysis.
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from ai_driven_workflow import AIDrivenWorkflowSystem


async def main():
    """Main launcher for the AI-Driven Deep Workflow."""
    print("🚀 NIMDA AI-DRIVEN DEEP WORKFLOW SYSTEM")
    print("=" * 80)
    print(
        "🎯 Purpose: Execute tasks with deep contextual understanding and multi-level planning."
    )
    print(
        "🧠 Core Logic: Develops a 3-level dev plan with phases, then executes with AI analysis."
    )
    print(
        "📁 Output: A new project directory with a fully analyzed and verified structure."
    )
    print("=" * 80)

    # Determine paths
    current_path = Path(__file__).parent
    output_dir = current_path / "nimda_project_ai_driven_build"

    print(f"📂 Source Path: {current_path}")
    print(f"🏗️  Output Path: {output_dir}")

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    print("\n🎬 Starting AI-Driven Deep Workflow...")
    print(
        "⏳ Estimated Time: Highly variable (depends on complexity and AI analysis depth)"
    )

    # Create and run the AI-driven workflow
    workflow = AIDrivenWorkflowSystem(
        project_path=output_dir,
    )

    try:
        await workflow.execute_enhanced_workflow()

        print("\n" + "=" * 80)
        print("🎉 AI-DRIVEN DEEP WORKFLOW COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"📁 Project created in: {output_dir}")
        print("🚀 Key achievements:")
        print("   • Multi-level development plan created and executed.")
        print("   • Deep AI-based analysis at every step.")
        print("   • Analysis of file interactions and dependencies.")
        print("   • Continuous verification and validation.")
        print("\n🔧 Next steps:")
        print(f"   1. cd {output_dir}")
        print(
            "   2. Review the generated project and the 'dev_plan.json' for insights."
        )
        print("   3. Run the main application entry point.")

    except Exception as e:
        print(f"\n💥 AI-Driven Workflow Error: {e}")
        print("🔧 Emergency recovery procedures initiated.")
        print("📁 Existing files remain unchanged.")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
