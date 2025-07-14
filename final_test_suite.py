#!/usr/bin/env python3
"""
Final Production Test Suite and Application Runner
Complete testing and validation of the NIMDA system
"""

import subprocess
import time
from pathlib import Path


class NIMDATestSuite:
    """Comprehensive test suite for NIMDA application"""

    def __init__(self):
        self.project_path = Path("/Users/dev/Documents/nimda_agent_plugin")
        self.venv_python = self.project_path / "venv" / "bin" / "python"
        self.tests_passed = 0
        self.tests_failed = 0

    def log_test(self, test_name: str, result: bool, details: str = ""):
        """Log test results"""
        if result:
            print(f"✅ PASS: {test_name}")
            if details:
                print(f"   📝 {details}")
            self.tests_passed += 1
        else:
            print(f"❌ FAIL: {test_name}")
            if details:
                print(f"   📝 {details}")
            self.tests_failed += 1

    def test_environment(self) -> bool:
        """Test the development environment"""
        print("🧪 Testing Environment...")

        # Test 1: Virtual environment exists
        venv_exists = self.venv_python.exists()
        self.log_test("Virtual Environment", venv_exists, f"Path: {self.venv_python}")

        # Test 2: Python version in venv
        if venv_exists:
            try:
                result = subprocess.run(
                    [str(self.venv_python), "--version"], capture_output=True, text=True
                )
                version_ok = result.returncode == 0
                self.log_test(
                    "Python Version", version_ok, f"Version: {result.stdout.strip()}"
                )
            except Exception:
                self.log_test("Python Version", False, "Could not execute python")

        # Test 3: Required files exist
        required_files = [
            "nimda_app.py",
            "chat_agent.py",
            "worker_agent.py",
            "adaptive_thinker.py",
            "learning_module.py",
            "macos_integration.py",
        ]

        for filename in required_files:
            file_exists = (self.project_path / filename).exists()
            self.log_test(f"File: {filename}", file_exists)

        return venv_exists

    def test_syntax_validation(self) -> bool:
        """Test syntax of all Python files"""
        print("\n🧪 Testing Syntax Validation...")

        python_files = [
            "nimda_app.py",
            "chat_agent.py",
            "worker_agent.py",
            "adaptive_thinker.py",
            "learning_module.py",
            "macos_integration.py",
        ]

        all_valid = True

        for filename in python_files:
            file_path = self.project_path / filename
            if file_path.exists():
                try:
                    result = subprocess.run(
                        [str(self.venv_python), "-m", "py_compile", str(file_path)],
                        capture_output=True,
                        text=True,
                    )

                    syntax_ok = result.returncode == 0
                    self.log_test(
                        f"Syntax: {filename}",
                        syntax_ok,
                        result.stderr if not syntax_ok else "Valid syntax",
                    )
                    if not syntax_ok:
                        all_valid = False

                except Exception as e:
                    self.log_test(f"Syntax: {filename}", False, str(e))
                    all_valid = False

        return all_valid

    def test_imports(self) -> bool:
        """Test module imports"""
        print("\n🧪 Testing Module Imports...")

        modules = [
            "chat_agent",
            "worker_agent",
            "adaptive_thinker",
            "learning_module",
            "macos_integration",
        ]

        all_imports_ok = True

        for module in modules:
            try:
                result = subprocess.run(
                    [
                        str(self.venv_python),
                        "-c",
                        f"import {module}; print('Import successful: {module}')",
                    ],
                    capture_output=True,
                    text=True,
                    cwd=self.project_path,
                )

                import_ok = result.returncode == 0
                self.log_test(
                    f"Import: {module}",
                    import_ok,
                    result.stdout.strip() if import_ok else result.stderr,
                )
                if not import_ok:
                    all_imports_ok = False

            except Exception as e:
                self.log_test(f"Import: {module}", False, str(e))
                all_imports_ok = False

        return all_imports_ok

    def test_application_health(self) -> bool:
        """Test application health check"""
        print("\n🧪 Testing Application Health...")

        try:
            result = subprocess.run(
                [str(self.venv_python), "nimda_app.py", "--mode", "health"],
                capture_output=True,
                text=True,
                cwd=self.project_path,
                timeout=30,
            )

            health_ok = result.returncode == 0
            self.log_test(
                "Application Health",
                health_ok,
                "All components healthy" if health_ok else result.stderr,
            )

            if health_ok:
                # Check for specific health indicators
                output = result.stdout
                components_healthy = "Overall: healthy" in output
                self.log_test(
                    "Components Status",
                    components_healthy,
                    "All 5 components reporting healthy",
                )
                return components_healthy

            return False

        except subprocess.TimeoutExpired:
            self.log_test("Application Health", False, "Health check timeout")
            return False
        except Exception as e:
            self.log_test("Application Health", False, str(e))
            return False

    def test_interactive_mode(self) -> bool:
        """Test interactive mode functionality"""
        print("\n🧪 Testing Interactive Mode...")

        try:
            # Test basic interactive commands
            test_commands = "health\nhelp\ntest command\nexit\n"

            process = subprocess.Popen(
                [str(self.venv_python), "nimda_app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                cwd=self.project_path,
            )

            stdout, stderr = process.communicate(input=test_commands, timeout=20)

            interactive_ok = process.returncode == 0
            self.log_test(
                "Interactive Mode",
                interactive_ok,
                "Commands processed successfully" if interactive_ok else stderr,
            )

            if interactive_ok:
                # Check for expected responses
                health_response = "System Status: healthy" in stdout
                help_response = "Available Commands:" in stdout
                chat_response = "Chat Agent: Processing" in stdout

                self.log_test("Health Command", health_response)
                self.log_test("Help Command", help_response)
                self.log_test("Chat Processing", chat_response)

                return health_response and help_response and chat_response

            return False

        except subprocess.TimeoutExpired:
            process.kill()
            self.log_test("Interactive Mode", False, "Interactive mode timeout")
            return False
        except Exception as e:
            self.log_test("Interactive Mode", False, str(e))
            return False

    def test_component_functionality(self) -> bool:
        """Test individual component functionality"""
        print("\n🧪 Testing Component Functionality...")

        components = [
            "chat_agent",
            "worker_agent",
            "adaptive_thinker",
            "learning_module",
            "macos_integration",
        ]

        all_components_ok = True

        for component in components:
            try:
                result = subprocess.run(
                    [str(self.venv_python), f"{component}.py"],
                    capture_output=True,
                    text=True,
                    cwd=self.project_path,
                    timeout=10,
                )

                component_ok = result.returncode == 0
                output = result.stdout.strip() if result.stdout else "No output"
                error = result.stderr.strip() if result.stderr else ""

                self.log_test(
                    f"Component: {component}",
                    component_ok,
                    output if component_ok else error,
                )

                if not component_ok:
                    all_components_ok = False

            except subprocess.TimeoutExpired:
                self.log_test(f"Component: {component}", False, "Execution timeout")
                all_components_ok = False
            except Exception as e:
                self.log_test(f"Component: {component}", False, str(e))
                all_components_ok = False

        return all_components_ok

    def run_full_test_suite(self) -> bool:
        """Run the complete test suite"""
        print("🏭 NIMDA Production Test Suite")
        print("=" * 60)

        start_time = time.time()

        # Run all tests
        test_results = []
        test_results.append(self.test_environment())
        test_results.append(self.test_syntax_validation())
        test_results.append(self.test_imports())
        test_results.append(self.test_application_health())
        test_results.append(self.test_interactive_mode())
        test_results.append(self.test_component_functionality())

        end_time = time.time()
        duration = end_time - start_time

        # Generate report
        print("\n" + "=" * 60)
        print("📊 TEST SUITE RESULTS")
        print("=" * 60)
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_failed}")
        print(
            f"📈 Success Rate: {(self.tests_passed / (self.tests_passed + self.tests_failed) * 100):.1f}%"
        )

        overall_success = all(test_results)

        if overall_success:
            print("\n🎉 ALL TESTS PASSED! 🎉")
            print("✅ NIMDA Application is production-ready!")
            print("\n📋 Quick Start:")
            print(f"   cd {self.project_path}")
            print(f"   {self.venv_python} nimda_app.py")
            print("\n📋 Available modes:")
            print(f"   {self.venv_python} nimda_app.py --mode health")
            print(f"   {self.venv_python} nimda_app.py --mode interactive")
        else:
            print("\n❌ SOME TESTS FAILED")
            print("🔧 Please fix the issues above before deployment")

        return overall_success


def main():
    """Main function"""
    test_suite = NIMDATestSuite()
    success = test_suite.run_full_test_suite()

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
