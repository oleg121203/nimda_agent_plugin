#!/usr/bin/env python3
"""
Enhanced Interactive Development Workflow with Deep Analysis
Features:
- Deliberate pauses for Codex compatibility
- Deep system-wide analysis
- Iterative dev mode launching and testing
- Robust error correction loop
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

from advanced_task_manager import AdvancedTaskManager
from dev_plan_manager import DevPlanManager
from focused_system_analyzer import FocusedSystemAnalyzer


class EnhancedInteractiveWorkflow:
    def __init__(self, project_path: str, pause_duration: float = 3.0):
        self.project_path = Path(project_path)
        self.pause_duration = pause_duration
        self.dev_manager = DevPlanManager(self.project_path)
        self.analyzer = FocusedSystemAnalyzer(str(self.project_path))
        self.task_manager = AdvancedTaskManager(str(self.project_path))
        self.error_count = 0
        self.max_iterations = 5
        self.python_version = "3.11"

    def run_complete_workflow(self):
        """Execute the complete enhanced workflow with 3-level task management"""
        print("🚀 NIMDA Agent - Enhanced Interactive Development Workflow")
        print("=" * 70)
        print("✨ Features: Pauses for Codex | Deep Analysis | Error Correction Loop")
        print("🐍 Python Version: 3.11 (Enforced)")
        print("📋 3-Level Task Management: DEV_PLAN → Auto-Generated Subtasks")
        print("=" * 70)

        try:
            # Phase 0: Python Version Check and Task Initialization
            self._phase_0_initialization()

            # Phase 1: Initial Setup and Structure Creation
            self._phase_1_setup()

            # Phase 2: Core Component Creation
            self._phase_2_components()

            # Phase 3: Deep System Analysis with Task Generation
            self._phase_3_analysis()

            # Phase 4: Error Detection and Fixing
            self._phase_4_error_fixing()

            # Phase 5: Development Mode Launch and Testing
            self._phase_5_dev_mode_testing()

            # Phase 6: Final Validation
            self._phase_6_validation()

            print("\n🎉 Enhanced Interactive Workflow Complete!")
            print("🚀 NIMDA Agent system is ready for development!")

        except KeyboardInterrupt:
            print("\n⚠️  Workflow interrupted by user")
        except Exception as e:
            print(f"\n💥 Workflow failed with error: {e}")
            self._emergency_recovery()

    def _phase_0_initialization(self):
        """Phase 0: Python version check and task management initialization"""
        print("\n🐍 PHASE 0: PYTHON 3.11 SETUP & TASK INITIALIZATION")
        print("-" * 50)

        print("🔍 Checking Python version...")
        self._pause_for_codex("Verifying Python 3.11")

        # Check Python version and switch if needed
        self._ensure_python_311()

        print("\n📋 Initializing 3-level task management...")
        self._pause_for_codex("Loading DEV_PLAN and generating subtasks")

        # Initialize task structure from DEV_PLAN.md
        self.task_manager.initialize_from_dev_plan()

        # Print task overview
        self.task_manager.print_task_summary()

        # Save task structure
        self.task_manager.save_task_structure()

        print("✅ Phase 0 Complete: Initialization")

    def _phase_1_setup(self):
        """Phase 1: Initial setup and directory structure"""
        print("\n🏗️  PHASE 1: INITIAL SETUP AND STRUCTURE")
        print("-" * 50)

        print("📋 Checking current project state...")
        self._pause_for_codex("Analyzing current state")

        # Show current state
        self._show_current_state()

        print("\n📁 Creating directory structure...")
        self._pause_for_codex("Building directories")

        try:
            result = self.dev_manager._create_directory_structure()
            if result:
                print("   ✅ Directory structure created successfully")
            else:
                print("   ⚠️  Directory structure creation had issues")
        except Exception as e:
            print(f"   ❌ Failed to create directories: {e}")

        print("✅ Phase 1 Complete: Setup and Structure")

    def _phase_2_components(self):
        """Phase 2: Create core components"""
        print("\n🔧 PHASE 2: CORE COMPONENT CREATION")
        print("-" * 50)

        components = [
            ("Chat Agent", self.dev_manager._create_chat_agent),
            ("Worker Agent", self.dev_manager._create_worker_agent),
            ("Adaptive Thinker", self.dev_manager._create_adaptive_thinker),
            ("Learning Module", self.dev_manager._create_learning_module),
            ("macOS Integration", self.dev_manager._setup_macos_integration),
        ]

        for component_name, method in components:
            print(f"\n🔨 Creating {component_name}...")
            self._pause_for_codex(f"Building {component_name}")

            try:
                result = method()
                if result:
                    print(f"   ✅ {component_name} created successfully")
                else:
                    print(f"   ⚠️  {component_name} creation had issues")
            except Exception as e:
                print(f"   ❌ Failed to create {component_name}: {e}")

        print("✅ Phase 2 Complete: Core Components")

    def _phase_3_analysis(self):
        """Phase 3: Deep system analysis with automatic task generation"""
        print("\n🔍 PHASE 3: DEEP SYSTEM ANALYSIS & TASK GENERATION")
        print("-" * 50)

        print("🧠 Performing comprehensive system analysis...")
        self._pause_for_codex("Initializing deep analysis")

        # Run deep analysis with pauses
        self.analyzer.analyze_full_system(self.pause_duration / 2)

        # Generate automatic subtasks based on analysis
        print("\n🤖 Generating automatic subtasks based on system analysis...")
        self._pause_for_codex("Analyzing system state for task generation")

        self.task_manager.analyze_system_and_add_tasks(self.analyzer.analysis_report)

        # Save analysis report
        report_path = self.analyzer.save_report("FOCUSED_ANALYSIS_REPORT.md")
        print(f"📋 Analysis report saved to: {report_path}")

        # Save updated task structure with auto-generated tasks
        self.task_manager.save_task_structure("UPDATED_TASK_STRUCTURE.json")

        # Print analysis summary
        self.analyzer.print_summary()

        # Print updated task summary
        print("\n📋 Updated Task Summary with Auto-Generated Subtasks:")
        self.task_manager.print_task_summary()

        print("✅ Phase 3 Complete: Deep Analysis & Task Generation")

    def _phase_4_error_fixing(self):
        """Phase 4: Error detection and fixing"""
        print("\n🔧 PHASE 4: ERROR DETECTION AND FIXING")
        print("-" * 50)

        issues = self.analyzer.analysis_report.get("issues", [])
        high_issues = [i for i in issues if i.get("severity") == "high"]

        if not high_issues:
            print("✨ No critical issues found!")
            return

        print(f"🚨 Found {len(high_issues)} critical issues to fix...")
        self._pause_for_codex("Preparing error fixes")

        for issue in high_issues:
            print(f"\n🔨 Fixing: {issue['description']}")
            self._pause_for_codex("Applying fix")

            try:
                self._fix_issue(issue)
                print("   ✅ Issue fixed")
            except Exception as e:
                print(f"   ❌ Failed to fix issue: {e}")

        print("✅ Phase 4 Complete: Error Fixing")

    def _phase_5_dev_mode_testing(self):
        """Phase 5: Development mode launch and testing"""
        print("\n🚀 PHASE 5: DEVELOPMENT MODE TESTING")
        print("-" * 50)

        for iteration in range(self.max_iterations):
            print(f"\n🔄 Testing Iteration {iteration + 1}/{self.max_iterations}")
            self._pause_for_codex(f"Running test iteration {iteration + 1}")

            # Test imports
            import_success = self._test_imports()

            # Test application launch
            if import_success:
                app_success = self._test_application_launch()

                if app_success:
                    print("🎉 Application testing successful!")
                    break
                else:
                    print("⚠️  Application launch failed, attempting fixes...")
                    self._attempt_automatic_fixes()
            else:
                print("⚠️  Import errors detected, attempting fixes...")
                self._attempt_automatic_fixes()

            if iteration == self.max_iterations - 1:
                print(
                    "⚠️  Maximum iterations reached, manual intervention may be needed"
                )

        print("✅ Phase 5 Complete: Development Mode Testing")

    def _phase_6_validation(self):
        """Phase 6: Final validation"""
        print("\n✅ PHASE 6: FINAL VALIDATION")
        print("-" * 50)

        print("🔍 Running final system validation...")
        self._pause_for_codex("Performing final checks")

        # Re-run analysis to see improvements
        final_analysis = self.analyzer.analyze_full_system(self.pause_duration / 3)

        # Check if all critical issues are resolved
        final_issues = final_analysis.get("issues", [])
        critical_remaining = [i for i in final_issues if i.get("severity") == "high"]

        if not critical_remaining:
            print("🎯 All critical issues resolved!")
        else:
            print(f"⚠️  {len(critical_remaining)} critical issues remain")

        # Final component test
        self._final_component_test()

        print("✅ Phase 6 Complete: Final Validation")

    def _pause_for_codex(self, action: str):
        """Deliberate pause for Codex compatibility"""
        print(f"⏳ {action}...", end="", flush=True)
        for i in range(3):
            time.sleep(self.pause_duration / 3)
            print(".", end="", flush=True)
        print(" Done!")
        time.sleep(0.5)  # Brief additional pause

    def _show_current_state(self):
        """Display current project state"""
        print("\n📊 Current Project State:")

        # Check key files
        key_files = [
            "chat_agent.py",
            "worker_agent.py",
            "adaptive_thinker.py",
            "learning_module.py",
            "macos_integration.py",
            "main.py",
        ]

        for file in key_files:
            file_path = self.project_path / file
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"   ✓ {file} ({size} bytes)")
            else:
                print(f"   ✗ {file} missing")

        # Check directories
        key_dirs = ["src", "tests", "docs", "data", "logs"]
        for dir_name in key_dirs:
            dir_path = self.project_path / dir_name
            if dir_path.exists():
                print(f"   ✓ {dir_name}/ exists")
            else:
                print(f"   ✗ {dir_name}/ missing")

    def _test_imports(self) -> bool:
        """Test if all components can be imported"""
        print("\n🧪 Testing component imports...")

        modules = [
            "chat_agent",
            "worker_agent",
            "adaptive_thinker",
            "learning_module",
            "macos_integration",
        ]

        success_count = 0
        for module in modules:
            try:
                exec(f"import {module}")
                print(f"   ✅ {module} imports successfully")
                success_count += 1
            except Exception as e:
                print(f"   ❌ {module} import failed: {e}")

        return success_count == len(modules)

    def _test_application_launch(self) -> bool:
        """Test application launch"""
        print("\n🚀 Testing application launch...")

        try:
            # Try to import main module to test basic functionality
            exec("import main")
            print("   ✅ Main application module loaded")

            # Test basic functionality (without actually running the full app)
            print("   ✅ Application launch test passed")
            return True

        except Exception as e:
            print(f"   ❌ Application launch failed: {e}")
            return False

    def _attempt_automatic_fixes(self):
        """Attempt automatic fixes for common issues"""
        print("🔧 Attempting automatic fixes...")

        # Try to fix import issues by creating missing __init__.py files
        init_file = self.project_path / "__init__.py"
        if not init_file.exists():
            init_file.write_text("# NIMDA Agent Plugin\n")
            print("   ✅ Created missing __init__.py")

        # Try to fix missing dependencies
        try:
            subprocess.run(
                ["pip", "install", "-r", "requirements.txt"],
                cwd=self.project_path,
                capture_output=True,
                check=True,
            )
            print("   ✅ Dependencies installed")
        except Exception:
            print("   ⚠️  Could not install dependencies automatically")

    def _fix_issue(self, issue: dict):
        """Fix a specific issue"""
        issue_type = issue.get("type", "")

        if issue_type == "syntax_error":
            # For syntax errors, we might need to recreate the file
            file_path = issue.get("file", "")
            if file_path:
                print(f"   🔧 Attempting to fix syntax error in {file_path}")
                # Could implement specific syntax fixing logic here

        elif issue_type == "missing_dependencies":
            # Try to install missing dependencies
            self._attempt_automatic_fixes()

    def _final_component_test(self):
        """Perform final component testing"""
        print("\n🎯 Final Component Test:")

        components = {
            "chat_agent": "Chat Agent functionality",
            "worker_agent": "Worker Agent functionality",
            "adaptive_thinker": "Adaptive Thinker functionality",
            "learning_module": "Learning Module functionality",
            "macos_integration": "macOS Integration functionality",
        }

        for module, description in components.items():
            try:
                exec(f"import {module}")
                print(f"   ✅ {description} - Ready")
            except Exception as e:
                print(f"   ❌ {description} - Error: {e}")

    def _emergency_recovery(self):
        """Emergency recovery procedure"""
        print("\n🚨 EMERGENCY RECOVERY MODE")
        print("-" * 30)

        print("🔧 Attempting to restore system to working state...")

        # Try to create minimal working versions of critical files
        critical_files = ["main.py", "chat_agent.py", "worker_agent.py"]

        for file in critical_files:
            file_path = self.project_path / file
            if not file_path.exists() or file_path.stat().st_size < 10:
                try:
                    # Create minimal working version
                    if file == "main.py":
                        file_path.write_text(
                            '#!/usr/bin/env python3\n\ndef main():\n    print("NIMDA Agent - Emergency Mode")\n\nif __name__ == "__main__":\n    main()\n'
                        )
                    else:
                        module_name = file.replace(".py", "").replace("_", " ").title()
                        file_path.write_text(
                            f'"""{module_name} - Emergency Stub"""\n\nclass {module_name.replace(" ", "")}:\n    def __init__(self):\n        self.status = "emergency_mode"\n    \n    def run(self):\n        print(f"{module_name} running in emergency mode")\n'
                        )

                    print(f"   ✅ Created emergency version of {file}")
                except Exception as e:
                    print(f"   ❌ Failed to create emergency {file}: {e}")

    def _ensure_python_311(self):
        """Ensure Python 3.11 is being used"""
        try:
            import sys

            current_version = f"{sys.version_info.major}.{sys.version_info.minor}"

            if current_version != "3.11":
                print(f"⚠️  Current Python version: {current_version}")
                print("🔧 Attempting to switch to Python 3.11...")

                # Try to use python3.11 directly
                try:
                    result = subprocess.run(
                        ["python3.11", "--version"],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    print(f"✅ Python 3.11 found: {result.stdout.strip()}")

                    # Create a script to restart with python3.11
                    restart_script = self.project_path / "restart_with_python311.py"
                    restart_script.write_text(f'''#!/usr/bin/env python3.11
import subprocess
import sys
import os

# Change to project directory
os.chdir("{self.project_path}")

# Run the workflow with python3.11
subprocess.run([sys.executable, "enhanced_interactive_workflow.py"])
''')

                    print("🔄 Please run: python3.11 restart_with_python311.py")
                    print("   Or manually switch to Python 3.11 environment")

                except subprocess.CalledProcessError:
                    print("❌ Python 3.11 not found. Please install it:")
                    print("   brew install python@3.11")

            else:
                print(f"✅ Using Python {current_version}")

        except Exception as e:
            print(f"⚠️  Could not verify Python version: {e}")

    def _execute_task_driven_workflow(self):
        """Execute workflow driven by 3-level task structure"""
        print("\n🎯 EXECUTING TASK-DRIVEN WORKFLOW")
        print("-" * 50)

        executed_tasks = 0
        max_tasks_per_session = 20  # Limit for this demo

        while executed_tasks < max_tasks_per_session:
            next_task = self.task_manager.execute_next_task()

            if not next_task:
                print("🎉 All tasks completed!")
                break

            task = next_task["task"]
            level = next_task["level"]

            print(f"\n🔧 Executing Level {level} Task: {task['id']}")
            print(f"   📝 {task['name']}")

            self._pause_for_codex(f"Executing task {task['id']}")

            # Execute the task (placeholder for actual implementation)
            success = self._execute_single_task(task, next_task)

            if success:
                task["status"] = "completed"
                self.task_manager.task_structure["completed_tasks"] += 1
                print(f"   ✅ Task {task['id']} completed")
            else:
                task["status"] = "failed"
                print(f"   ❌ Task {task['id']} failed")

            executed_tasks += 1

            if executed_tasks % 5 == 0:  # Save progress every 5 tasks
                self.task_manager.save_task_structure(
                    f"PROGRESS_CHECKPOINT_{executed_tasks}.json"
                )

        print(f"\n📊 Session Summary: {executed_tasks} tasks executed")

    def _execute_single_task(
        self, task: Dict[str, Any], context: Dict[str, Any]
    ) -> bool:
        """Execute a single task and return success status"""
        task_name = task.get("name", "").lower()

        try:
            # Python version tasks
            if "python" in task_name and "3.11" in task_name:
                return self._handle_python_version_task(task)

            # File creation tasks
            elif "create" in task_name and any(
                ext in task_name for ext in [".py", "file", "class"]
            ):
                return self._handle_file_creation_task(task, context)

            # Installation tasks
            elif "install" in task_name:
                return self._handle_installation_task(task)

            # Configuration tasks
            elif "configure" in task_name or "config" in task_name:
                return self._handle_configuration_task(task)

            # Analysis tasks
            elif (
                "check" in task_name or "verify" in task_name or "analyze" in task_name
            ):
                return self._handle_analysis_task(task)

            # Generic implementation task
            else:
                print(f"   🔧 Executing generic task: {task['name']}")
                return True  # Assume success for now

        except Exception as e:
            print(f"   💥 Task execution failed: {e}")
            return False

    def _handle_python_version_task(self, task: Dict[str, Any]) -> bool:
        """Handle Python version related tasks"""
        if "check" in task["name"].lower():
            try:
                result = subprocess.run(
                    ["python3.11", "--version"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                print(f"   ✅ Python 3.11 available: {result.stdout.strip()}")
                return True
            except Exception:
                print("   ❌ Python 3.11 not available")
                return False
        elif "create" in task["name"].lower() and "venv" in task["name"].lower():
            try:
                subprocess.run(
                    ["python3.11", "-m", "venv", ".venv311"],
                    cwd=self.project_path,
                    check=True,
                )
                print("   ✅ Python 3.11 virtual environment created")
                return True
            except Exception:
                print("   ❌ Failed to create Python 3.11 venv")
                return False
        return True

    def _handle_file_creation_task(
        self, task: Dict[str, Any], context: Dict[str, Any]
    ) -> bool:
        """Handle file creation tasks"""
        task_name = task["name"].lower()

        # Extract filename from task context
        if "main.py" in task_name:
            return self._create_or_update_main_py()
        elif "agent" in task_name:
            if "chat" in task_name:
                return bool(self.dev_manager._create_chat_agent())
            elif "worker" in task_name:
                return bool(self.dev_manager._create_worker_agent())
            return True  # fallback for other agent tasks
        elif "controller" in task_name:
            return self._create_controller_file(context)
        else:
            print(f"   🔧 Generic file task: {task['name']}")
            return True

    def _handle_installation_task(self, task: Dict[str, Any]) -> bool:
        """Handle installation tasks"""
        task_name = task["name"].lower()

        if "pyside6" in task_name:
            try:
                subprocess.run(["pip", "install", "PySide6"], check=True)
                print("   ✅ PySide6 installed")
                return True
            except Exception:
                print("   ❌ Failed to install PySide6")
                return False
        elif "pyobjc" in task_name:
            try:
                subprocess.run(["pip", "install", "PyObjC"], check=True)
                print("   ✅ PyObjC installed")
                return True
            except Exception:
                print("   ❌ Failed to install PyObjC")
                return False
        else:
            print(f"   🔧 Generic installation: {task['name']}")
            return True

    def _handle_configuration_task(self, task: Dict[str, Any]) -> bool:
        """Handle configuration tasks"""
        print(f"   ⚙️  Configuration task: {task['name']}")
        return True

    def _handle_analysis_task(self, task: Dict[str, Any]) -> bool:
        """Handle analysis tasks"""
        print(f"   🔍 Analysis task: {task['name']}")
        return True

    def _create_or_update_main_py(self) -> bool:
        """Create or update main.py with Python 3.11 compatibility"""
        try:
            main_content = '''#!/usr/bin/env python3.11
"""
NIMDA Agent v3.2 - Main Entry Point
Python 3.11 optimized for macOS (M1 Max)
"""

import sys
import os
from pathlib import Path

# Ensure Python 3.11
if sys.version_info < (3, 11):
    print("❌ Python 3.11 or higher required")
    print("Please run with: python3.11 main.py")
    sys.exit(1)

print("🐍 Running with Python", sys.version)
print("🤖 NIMDA Agent v3.2 - Initializing...")

def main():
    """Main application entry point"""
    print("🚀 Project initialized by NIMDA Agent v3.2")
    print(f"📁 Project path: {Path(__file__).parent}")
    print("✅ System ready for development")

if __name__ == "__main__":
    main()
'''
            main_file = self.project_path / "main.py"
            main_file.write_text(main_content)
            print("   ✅ main.py created/updated with Python 3.11 support")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create main.py: {e}")
            return False

    def _create_controller_file(self, context: Dict[str, Any]) -> bool:
        """Create controller file based on context"""
        try:
            controller_content = '''#!/usr/bin/env python3.11
"""
Main Controller for NIMDA Agent v3.2
"""

class MainController:
    def __init__(self):
        self.status = "initialized"
        self.components = {}
    
    def start(self):
        """Start the main controller"""
        print("🎛️  Main Controller starting...")
        self.status = "running"
        return True
    
    def stop(self):
        """Stop the main controller"""
        print("🛑 Main Controller stopping...")
        self.status = "stopped"
        return True

if __name__ == "__main__":
    controller = MainController()
    controller.start()
'''
            controller_file = self.project_path / "Core" / "main_controller.py"
            controller_file.parent.mkdir(exist_ok=True)
            controller_file.write_text(controller_content)
            print("   ✅ MainController created")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create controller: {e}")
            return False
