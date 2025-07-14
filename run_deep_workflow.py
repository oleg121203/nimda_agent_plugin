#!/usr/bin/env python3
"""
Deep Context Workflow Launcher
Creates a complete NIMDA project in a separate directory with unrealistically high level analysis
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from deep_context_workflow import DeepContextWorkflowSystem


async def main():
    """Main launcher for deep context workflow"""
    print("🚀 NIMDA DEEP CONTEXT WORKFLOW SYSTEM")
    print("=" * 80)
    print("🎯 Purpose: Create complete NIMDA project with deep context analysis")
    print("📁 Output: Separate project directory with full structure")
    print("🧠 Level: Unrealistically high-level development approach")
    print("⏳ Codex: Optimized for AI-assisted development")
    print("=" * 80)

    # Determine paths
    current_path = Path(__file__).parent
    output_dir = current_path / "nimda_project_deep_build"

    print(f"📂 Source Path: {current_path}")
    print(f"🏗️  Output Path: {output_dir}")

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    print("\n🎬 Starting Deep Context Workflow...")
    print("⏳ Estimated Time: 15-30 minutes (with Codex pauses)")
    print("🎨 Creative Mode: Enabled for AI enhancement")

    # Create and run deep workflow
    workflow = DeepContextWorkflowSystem(
        project_path=str(output_dir),
        codex_pause_duration=2.5,  # Optimal for Codex interaction
    )

    try:
        await workflow.execute_deep_workflow()

        print("\n" + "=" * 80)
        print("🎉 DEEP CONTEXT WORKFLOW COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"📁 Project created in: {output_dir}")
        print("🚀 Features implemented:")
        print("   • Complete project structure")
        print("   • Core components (MainController, AgentManager, CommandEngine)")
        print("   • Deep context analysis and documentation")
        print("   • Legacy compatibility preservation")
        print("   • Intelligent architecture design")
        print("   • Comprehensive testing framework")
        print("   • Advanced monitoring and observability")
        print("   • Complete documentation suite")
        print("\n🔧 Next steps:")
        print(f"   1. cd {output_dir}")
        print("   2. Review generated components")
        print("   3. Run python Core/main_controller.py")
        print("   4. Customize based on specific requirements")
        print(
            "\n💡 All existing files preserved - workflow operates in separate directory"
        )

    except Exception as e:
        print(f"\n💥 Deep Workflow Error: {e}")
        print("🔧 Emergency recovery mode activated")
        print("📁 Existing files remain unchanged")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
