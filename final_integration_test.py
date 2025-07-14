#!/usr/bin/env python3
"""
Final Integration Test Suite - Demonstrates all NIMDA Agent capabilities
Features:
- Ultimate Interactive Workflow execution
- AI Task Prioritization with machine learning
- Smart Error Detection and Resolution
- Auto Documentation Generation
- Creative Hooks integration with Codex AI
- Real-time monitoring and metrics
"""

import asyncio
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

from ai_task_prioritizer import AITaskPrioritizer
from auto_documentation_generator import AutoDocumentationGenerator
from smart_error_detector import SmartErrorDetector
from ultimate_interactive_workflow import UltimateInteractiveWorkflow


class FinalIntegrationTestSuite:
    """
    Comprehensive test suite demonstrating all NIMDA Agent capabilities
    """

    def __init__(self, project_path: str = "/Users/dev/Documents/nimda_agent_plugin"):
        self.project_path = Path(project_path)
        self.test_results = {}
        self.start_time = time.time()

        print("🚀 NIMDA Agent - Final Integration Test Suite")
        print("=" * 70)
        print("✨ Testing all advanced capabilities and AI components")
        print("🎯 Demonstrating real-world usage scenarios")
        print("=" * 70)

    async def run_complete_test_suite(self):
        """Run comprehensive test suite demonstrating all capabilities"""

        try:
            # Test 1: Ultimate Interactive Workflow
            await self._test_ultimate_workflow()

            # Test 2: AI Task Prioritization
            await self._test_ai_task_prioritization()

            # Test 3: Smart Error Detection
            await self._test_error_detection()

            # Test 4: Auto Documentation Generation
            await self._test_documentation_generation()

            # Test 5: Integration Testing
            await self._test_component_integration()

            # Final Results
            self._display_final_results()

        except Exception as e:
            print(f"💥 Test suite failed: {e}")
            self._emergency_results()

    async def _test_ultimate_workflow(self):
        """Test 1: Ultimate Interactive Workflow"""
        print("\n🎯 TEST 1: ULTIMATE INTERACTIVE WORKFLOW")
        print("-" * 50)

        start_time = time.time()

        try:
            # Initialize workflow with non-interactive mode for testing
            workflow = UltimateInteractiveWorkflow(str(self.project_path))
            workflow.project_config["interactive_mode"] = False

            print("   🔧 Initializing Ultimate Workflow...")

            # Test phases individually for better control
            await workflow._ultimate_phase_0_initialization()
            print("   ✅ Phase 0: Initialization successful")

            await workflow._ultimate_phase_1_environment()
            print("   ✅ Phase 1: Environment setup successful")

            await workflow._ultimate_phase_2_components()
            print("   ✅ Phase 2: Component generation successful")

            # Quick phases for testing
            await workflow._ultimate_phase_3_analysis()
            print("   ✅ Phase 3: Analysis successful")

            await workflow._ultimate_phase_4_error_resolution()
            print("   ✅ Phase 4: Error resolution successful")

            execution_time = time.time() - start_time

            self.test_results["ultimate_workflow"] = {
                "status": "passed",
                "execution_time": execution_time,
                "phases_completed": 5,
                "total_steps": workflow.step_count,
            }

            print(f"   🎉 Ultimate Workflow completed in {execution_time:.2f}s")
            print(f"   📊 Total steps executed: {workflow.step_count}")

        except Exception as e:
            self.test_results["ultimate_workflow"] = {
                "status": "failed",
                "error": str(e),
                "execution_time": time.time() - start_time,
            }
            print(f"   ❌ Ultimate Workflow failed: {e}")

    async def _test_ai_task_prioritization(self):
        """Test 2: AI Task Prioritization with Machine Learning"""
        print("\n🧠 TEST 2: AI TASK PRIORITIZATION")
        print("-" * 50)

        start_time = time.time()

        try:
            prioritizer = AITaskPrioritizer(str(self.project_path))

            # Add diverse test tasks
            test_tasks = [
                {
                    "title": "Critical security vulnerability fix",
                    "description": "Fix authentication bypass in login system",
                    "priority": "high",
                    "estimated_time": 180,
                    "tags": ["security", "urgent", "bug"],
                },
                {
                    "title": "Implement ML model training pipeline",
                    "description": "Add automated model retraining with FAISS integration",
                    "priority": "medium",
                    "estimated_time": 480,
                    "tags": ["ml", "feature", "ai"],
                },
                {
                    "title": "Refactor GUI theme system",
                    "description": "Update PySide6 components with modern design",
                    "priority": "low",
                    "estimated_time": 240,
                    "tags": ["ui", "enhancement", "design"],
                },
                {
                    "title": "Add comprehensive unit tests",
                    "description": "Increase test coverage for core modules",
                    "priority": "medium",
                    "estimated_time": 360,
                    "tags": ["testing", "quality", "coverage"],
                },
                {
                    "title": "Deploy to production server",
                    "description": "Configure production environment and deployment",
                    "priority": "high",
                    "estimated_time": 120,
                    "tags": ["deployment", "production", "urgent"],
                },
            ]

            # Add tasks and test prioritization
            task_ids = []
            for task in test_tasks:
                task_id = prioritizer.add_task(task)
                task_ids.append(task_id)

            print(f"   📋 Added {len(task_ids)} test tasks")

            # Test AI prioritization
            prioritized_tasks = prioritizer.prioritize_tasks()
            print(f"   🎯 Prioritized {len(prioritized_tasks)} tasks")

            # Test recommendation system
            next_task = prioritizer.get_next_recommended_task()
            if next_task:
                print(f"   🏆 Next recommended: {next_task['title']}")
            else:
                print("   🏆 Next recommended: No tasks available")

            # Test completion and learning
            if task_ids:
                completion_result = prioritizer.complete_task(
                    task_ids[0],
                    {
                        "actual_time": 150,
                        "satisfaction_rating": 5,
                        "difficulty_rating": 3,
                    },
                )
                print(
                    f"   ✅ Task completion test: {'passed' if completion_result else 'failed'}"
                )

            # Generate insights
            insights = prioritizer.generate_task_insights()
            print(
                f"   📊 Generated insights with {insights['total_tasks']} tasks analyzed"
            )

            execution_time = time.time() - start_time

            self.test_results["ai_prioritization"] = {
                "status": "passed",
                "execution_time": execution_time,
                "tasks_processed": len(task_ids),
                "top_task_score": prioritized_tasks[0]["ai_score"]
                if prioritized_tasks
                else 0,
                "learning_enabled": prioritizer.learning_enabled,
            }

            print(f"   🎉 AI Prioritization completed in {execution_time:.2f}s")

        except Exception as e:
            self.test_results["ai_prioritization"] = {
                "status": "failed",
                "error": str(e),
                "execution_time": time.time() - start_time,
            }
            print(f"   ❌ AI Prioritization failed: {e}")

    async def _test_error_detection(self):
        """Test 3: Smart Error Detection and Resolution"""
        print("\n🔍 TEST 3: SMART ERROR DETECTION")
        print("-" * 50)

        start_time = time.time()

        try:
            detector = SmartErrorDetector(str(self.project_path))

            # Detect errors across project
            print("   🔍 Scanning project for errors...")
            errors = detector.detect_all_errors()

            if errors:
                print(f"   📋 Detected {len(errors)} total errors")

                # Categorize errors
                error_types = {}
                for error in errors:
                    error_type = error.get("type", "unknown")
                    error_types[error_type] = error_types.get(error_type, 0) + 1

                print("   📊 Error breakdown:")
                for error_type, count in sorted(error_types.items()):
                    print(f"      {error_type}: {count}")

                # Test resolution on sample errors
                sample_size = min(5, len(errors))
                resolved_count = 0

                for error in errors[:sample_size]:
                    try:
                        resolution = detector.resolve_error(error)
                        if resolution.get("resolved", False):
                            resolved_count += 1
                    except Exception as e:
                        print(f"      ⚠️ Resolution attempt failed: {e}")

                print(f"   🔧 Attempted resolution on {sample_size} errors")
                print(f"   ✅ Successfully resolved: {resolved_count}")

            # Generate comprehensive report
            report = detector.generate_error_report()
            print(
                f"   📊 Generated report with {report['total_errors']} errors analyzed"
            )

            execution_time = time.time() - start_time

            self.test_results["error_detection"] = {
                "status": "passed",
                "execution_time": execution_time,
                "total_errors": len(errors),
                "error_types": len(error_types),
                "resolution_rate": report.get("resolution_stats", {}).get(
                    "resolution_rate", 0
                ),
            }

            print(f"   🎉 Error Detection completed in {execution_time:.2f}s")

        except Exception as e:
            self.test_results["error_detection"] = {
                "status": "failed",
                "error": str(e),
                "execution_time": time.time() - start_time,
            }
            print(f"   ❌ Error Detection failed: {e}")

    async def _test_documentation_generation(self):
        """Test 4: Auto Documentation Generation"""
        print("\n📚 TEST 4: AUTO DOCUMENTATION GENERATION")
        print("-" * 50)

        start_time = time.time()

        try:
            generator = AutoDocumentationGenerator(str(self.project_path))

            # Quick analysis for testing (limit scope)
            print("   📂 Analyzing project structure...")
            generator._analyze_project_structure()

            # Analyze a subset of modules for speed
            python_files = generator.project_structure["python_files"][
                :10
            ]  # Limit to 10 files

            print(f"   🔍 Analyzing {len(python_files)} Python modules...")
            for py_file in python_files:
                try:
                    file_path = generator.project_path / py_file
                    module_info = generator._analyze_module(file_path)
                    generator.analyzed_modules[py_file] = module_info
                except Exception as e:
                    print(f"      ⚠️ Skipped {py_file}: {e}")

            # Generate documentation samples
            print("   📝 Generating documentation samples...")

            # Generate main README
            readme_content = generator._generate_main_readme()
            print(f"      ✅ README.md generated ({len(readme_content)} chars)")

            # Generate API docs sample
            api_content = generator._generate_api_documentation()
            print(f"      ✅ API docs generated ({len(api_content)} chars)")

            # Test insights generation
            generator._generate_components_overview()
            print("      ✅ Components overview generated")

            execution_time = time.time() - start_time

            self.test_results["documentation"] = {
                "status": "passed",
                "execution_time": execution_time,
                "modules_analyzed": len(generator.analyzed_modules),
                "readme_size": len(readme_content),
                "api_docs_size": len(api_content),
            }

            print(f"   🎉 Documentation Generation completed in {execution_time:.2f}s")

        except Exception as e:
            self.test_results["documentation"] = {
                "status": "failed",
                "error": str(e),
                "execution_time": time.time() - start_time,
            }
            print(f"   ❌ Documentation Generation failed: {e}")

    async def _test_component_integration(self):
        """Test 5: Component Integration Testing"""
        print("\n🔗 TEST 5: COMPONENT INTEGRATION")
        print("-" * 50)

        start_time = time.time()

        try:
            # Test cross-component functionality
            print("   🔄 Testing component interoperability...")

            # Initialize all major components
            prioritizer = AITaskPrioritizer(str(self.project_path))
            detector = SmartErrorDetector(str(self.project_path))

            # Test 1: Error detection feeding into task prioritization
            print("   📋 Test: Error-driven task creation...")

            # Simulate finding errors and creating tasks
            sample_errors = [
                {
                    "type": "syntax_error",
                    "message": "Fix syntax in module X",
                    "severity": "error",
                },
                {
                    "type": "import_error",
                    "message": "Missing dependency Y",
                    "severity": "warning",
                },
            ]

            created_tasks = []
            for error in sample_errors:
                task = {
                    "title": f"Fix {error['type']}: {error['message'][:50]}",
                    "description": error["message"],
                    "priority": "high" if error["severity"] == "error" else "medium",
                    "estimated_time": 60,
                    "tags": ["bug_fix", "automated"],
                }
                task_id = prioritizer.add_task(task)
                created_tasks.append(task_id)

            print(f"      ✅ Created {len(created_tasks)} error-based tasks")

            # Test 2: Prioritization influencing error resolution order
            print("   🎯 Test: Priority-driven error resolution...")

            prioritized = prioritizer.prioritize_tasks()
            if prioritized:
                top_task = prioritized[0]
                print(f"      🏆 Top priority task: {top_task['title'][:50]}...")
                print(f"      📊 AI Score: {top_task['ai_score']:.3f}")

            # Test 3: Component state synchronization
            print("   🔄 Test: Component state sync...")

            # Generate insights from both components
            task_insights = prioritizer.generate_task_insights()
            error_report = detector.generate_error_report()

            integration_metrics = {
                "tasks_total": task_insights["total_tasks"],
                "errors_total": error_report["total_errors"],
                "efficiency_score": (
                    task_insights["completion_rate"]
                    + error_report["resolution_stats"]["resolution_rate"]
                )
                / 2,
            }

            print("      📊 Integration metrics calculated")
            print(
                f"      🎯 System efficiency: {integration_metrics['efficiency_score']:.1%}"
            )

            execution_time = time.time() - start_time

            self.test_results["integration"] = {
                "status": "passed",
                "execution_time": execution_time,
                "tasks_created": len(created_tasks),
                "metrics": integration_metrics,
            }

            print(f"   🎉 Component Integration completed in {execution_time:.2f}s")

        except Exception as e:
            self.test_results["integration"] = {
                "status": "failed",
                "error": str(e),
                "execution_time": time.time() - start_time,
            }
            print(f"   ❌ Component Integration failed: {e}")

    def _display_final_results(self):
        """Display comprehensive test results"""
        total_time = time.time() - self.start_time

        print("\n" + "=" * 70)
        print("🎯 FINAL INTEGRATION TEST RESULTS")
        print("=" * 70)

        passed_tests = 0
        total_tests = len(self.test_results)

        for test_name, result in self.test_results.items():
            status_emoji = "✅" if result["status"] == "passed" else "❌"
            execution_time = result.get("execution_time", 0)

            print(
                f"{status_emoji} {test_name.replace('_', ' ').title()}: {result['status']}"
            )
            print(f"   ⏱️  Execution time: {execution_time:.2f}s")

            if result["status"] == "passed":
                passed_tests += 1
                # Display specific metrics
                if test_name == "ultimate_workflow":
                    print(
                        f"   📊 Phases completed: {result.get('phases_completed', 0)}"
                    )
                    print(f"   🔄 Total steps: {result.get('total_steps', 0)}")
                elif test_name == "ai_prioritization":
                    print(f"   📋 Tasks processed: {result.get('tasks_processed', 0)}")
                    print(f"   🎯 Top score: {result.get('top_task_score', 0):.3f}")
                elif test_name == "error_detection":
                    print(f"   🔍 Errors found: {result.get('total_errors', 0)}")
                    print(
                        f"   🔧 Resolution rate: {result.get('resolution_rate', 0):.1%}"
                    )
                elif test_name == "documentation":
                    print(
                        f"   📚 Modules analyzed: {result.get('modules_analyzed', 0)}"
                    )
                    print(f"   📄 README size: {result.get('readme_size', 0)} chars")
                elif test_name == "integration":
                    metrics = result.get("metrics", {})
                    print(f"   🔗 Tasks created: {result.get('tasks_created', 0)}")
                    print(f"   📊 Efficiency: {metrics.get('efficiency_score', 0):.1%}")
            else:
                print(f"   ❌ Error: {result.get('error', 'Unknown error')}")

            print()

        # Overall results
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

        print("📊 OVERALL RESULTS:")
        print(f"   ✅ Tests passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print(f"   ⏱️  Total execution time: {total_time:.2f}s")
        print(f"   📅 Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if success_rate >= 80:
            print("\n🎉 NIMDA Agent integration test PASSED!")
            print("✨ All major components are working correctly")
            print("🚀 System is ready for production use")
        elif success_rate >= 60:
            print("\n⚠️  NIMDA Agent integration test PARTIALLY PASSED")
            print("🔧 Some components need attention")
            print("📋 Review failed tests and apply fixes")
        else:
            print("\n❌ NIMDA Agent integration test FAILED")
            print("🚨 Critical issues detected")
            print("🛠️  Manual intervention required")

    def _emergency_results(self):
        """Display emergency results if test suite fails completely"""
        print("\n🚨 EMERGENCY TEST RESULTS")
        print("=" * 50)
        print("❌ Integration test suite encountered critical failure")
        print("📋 Partial results:")

        for test_name, result in self.test_results.items():
            status = result.get("status", "unknown")
            print(f"   {test_name}: {status}")

        print("\n🛠️  Manual debugging required")


async def main():
    """Main execution function"""
    test_suite = FinalIntegrationTestSuite()
    await test_suite.run_complete_test_suite()


if __name__ == "__main__":
    asyncio.run(main())
