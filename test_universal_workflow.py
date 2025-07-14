#!/usr/bin/env python3
"""
Test the Universal Creative Workflow with a simple example
"""

import shutil
import tempfile
from pathlib import Path

from universal_creative_workflow import UniversalCreativeWorkflow


def test_universal_workflow():
    """Test the universal workflow with a simple project"""

    # Create a temporary project directory
    temp_dir = Path(tempfile.mkdtemp())
    print(f"🧪 Testing in temporary directory: {temp_dir}")

    try:
        # Create a simple DEV_PLAN.md
        dev_plan_content = """# Test Universal Project

## Overview
This is a simple Python CLI application for testing the Universal Creative Workflow.

## Technology Stack
- Language: Python 3.9
- Type: CLI tool
- Testing: pytest

## Phases

### 1. Environment Setup
- [ ] Setup Python environment
- [ ] Install basic dependencies

### 2. Core Development  
- [ ] Create main CLI module
- [ ] Implement core functionality
- [ ] Add configuration support

### 3. Testing and Validation
- [ ] Write unit tests
- [ ] Integration testing
- [ ] Documentation
"""

        dev_plan_path = temp_dir / "DEV_PLAN.md"
        dev_plan_path.write_text(dev_plan_content)
        print(f"✅ Created test DEV_PLAN.md")

        # Initialize the workflow
        workflow = UniversalCreativeWorkflow(str(temp_dir), pause_duration=0.1)

        # Register a simple test hook
        def test_hook(context):
            action = context.get("action")
            if action == "create_component":
                component_name = context.get("component_name", "test_component")
                print(f"🎨 Test hook creating: {component_name}")

                # Create a simple test file
                src_dir = temp_dir / "src"
                src_dir.mkdir(exist_ok=True)

                test_file = src_dir / f"{component_name}.py"
                test_file.write_text(
                    f'"""Test component: {component_name}"""\n\nprint("Hello from {component_name}!")\n'
                )
                print(f"   📝 Created {test_file}")
                return True
            return False

        workflow.register_creative_hook("creative_solution", test_hook)

        # Run the workflow
        print("\n🚀 Running Universal Creative Workflow Test...")
        workflow.run_universal_workflow()

        # Check results
        print("\n📊 Test Results:")
        src_dir = temp_dir / "src"
        if src_dir.exists():
            created_files = list(src_dir.glob("*.py"))
            print(f"   ✅ Created {len(created_files)} Python files in src/")
            for file in created_files:
                print(f"      📄 {file.name}")
        else:
            print("   ⚠️  No src/ directory found")

        # Check task structure
        task_file = temp_dir / "UNIVERSAL_TASK_STRUCTURE.json"
        if task_file.exists():
            print(f"   ✅ Task structure saved: {task_file}")

        # Check analysis report
        analysis_file = temp_dir / "UNIVERSAL_ANALYSIS_REPORT.md"
        if analysis_file.exists():
            print(f"   ✅ Analysis report saved: {analysis_file}")

        print(f"\n🎯 Test completed successfully!")
        print(f"📁 Results saved in: {temp_dir}")

        return temp_dir

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return None


def test_different_project_types():
    """Test different project types"""

    project_types = [
        {
            "name": "React Web App",
            "content": """# React Application
            
## Tech Stack
- Frontend: React 18, TypeScript
- Build: Vite
- Testing: Jest
""",
            "expected_type": "web_application",
        },
        {
            "name": "AI Agent",
            "content": """# AI Agent System
            
## Overview
Multi-agent AI system with machine learning capabilities.

## Tech Stack  
- Language: Python 3.10
- ML: TensorFlow, PyTorch
- Agents: Custom agent framework
""",
            "expected_type": "ai_agent",
        },
        {
            "name": "Desktop App",
            "content": """# Desktop Application

## Overview
Cross-platform desktop application.

## Tech Stack
- GUI: Qt 6, PySide6
- Language: Python 3.9
""",
            "expected_type": "desktop_application",
        },
    ]

    for project in project_types:
        print(f"\n🧪 Testing {project['name']}...")

        temp_dir = Path(tempfile.mkdtemp())
        dev_plan = temp_dir / "DEV_PLAN.md"
        dev_plan.write_text(project["content"])

        workflow = UniversalCreativeWorkflow(str(temp_dir), pause_duration=0.1)
        detected_type = workflow.project_config["project_type"]

        if detected_type == project["expected_type"]:
            print(f"   ✅ Correctly detected: {detected_type}")
        else:
            print(f"   ⚠️  Expected {project['expected_type']}, got {detected_type}")

        # Cleanup
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    print("🚀 Universal Creative Workflow Testing Suite")
    print("=" * 50)

    # Test 1: Basic workflow
    test_result = test_universal_workflow()

    # Test 2: Different project types
    test_different_project_types()

    print("\n✅ All tests completed!")

    if test_result:
        print(f"\n📁 Check the results in: {test_result}")
        print("   (Temporary directory - will be cleaned up by system later)")
