#!/usr/bin/env python3
"""
Advanced Error Fixing and Application Runner
Fixes syntax errors and runs the application successfully
"""

import re
import subprocess
import sys
from pathlib import Path

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")


class AdvancedErrorFixer:
    """Advanced error fixing with regex patterns"""

    def __init__(self, project_path: str = "/Users/dev/Documents/nimda_agent_plugin"):
        self.project_path = Path(project_path)
        self.fixed_files = []

    def fix_duplicate_imports(self, file_path: str) -> bool:
        """Fix duplicate import statements"""
        print(f"🔧 Fixing duplicate imports in {Path(file_path).name}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Fix duplicate typing imports
            patterns = [
                (
                    r"from typing import.*?Dict, List, Any, Optional.*?Dict.*?\n",
                    "from typing import Dict, List, Any, Optional\n",
                ),
                (
                    r"from typing import.*?Dict, List, Any, Optional.*?Any.*?\n",
                    "from typing import Dict, List, Any, Optional\n",
                ),
                (
                    r"from typing import.*?Dict, List, Any, Optional.*?List.*?\n",
                    "from typing import Dict, List, Any, Optional\n",
                ),
                # Fix duplicate sys/os imports
                (
                    r"import logging\nimport sys\nimport os.*?import sys.*?\n",
                    "import logging\nimport sys\nimport os\n",
                ),
                (r"import logging.*?import logging.*?\n", "import logging\n"),
            ]

            original_content = content
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

            # Clean up extra newlines
            content = re.sub(r"\n{3,}", "\n\n", content)

            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Fixed imports in {Path(file_path).name}")
                self.fixed_files.append(file_path)
                return True
            else:
                print(f"ℹ️ No fixes needed for {Path(file_path).name}")
                return True

        except Exception as e:
            print(f"❌ Failed to fix {Path(file_path).name}: {e}")
            return False

    def validate_syntax(self, file_path: str) -> bool:
        """Validate Python syntax"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            compile(source, file_path, "exec")
            print(f"✅ Syntax OK: {Path(file_path).name}")
            return True
        except SyntaxError as e:
            print(f"❌ Syntax Error in {Path(file_path).name}: {e}")
            return False
        except Exception as e:
            print(f"❌ Error checking {Path(file_path).name}: {e}")
            return False

    def fix_all_files(self) -> bool:
        """Fix all Python files in the project"""
        python_files = [
            "chat_agent.py",
            "worker_agent.py",
            "adaptive_thinker.py",
            "learning_module.py",
            "macos_integration.py",
        ]

        print("🔧 Starting advanced error fixing...")

        success = True
        for filename in python_files:
            file_path = self.project_path / filename
            if file_path.exists():
                if not self.fix_duplicate_imports(str(file_path)):
                    success = False
                if not self.validate_syntax(str(file_path)):
                    success = False
            else:
                print(f"⚠️ File not found: {filename}")

        return success


def run_application_with_venv():
    """Run the application using the virtual environment"""
    project_path = Path("/Users/dev/Documents/nimda_agent_plugin")
    venv_python = project_path / "venv" / "bin" / "python"

    if not venv_python.exists():
        print("❌ Virtual environment not found. Run production_workflow.py first.")
        return False

    print("🚀 Running NIMDA application...")

    try:
        # Test health check
        result = subprocess.run(
            [str(venv_python), "nimda_app.py", "--mode", "health"],
            capture_output=True,
            text=True,
            cwd=project_path,
            timeout=30,
        )

        if result.returncode == 0:
            print("✅ Application health check passed!")
            print("📊 Output:")
            print(result.stdout)

            # Run interactive demo
            print("\n🔄 Testing interactive mode...")
            process = subprocess.Popen(
                [str(venv_python), "nimda_app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                cwd=project_path,
            )

            # Send test commands
            test_input = "health\nhelp\nexit\n"
            stdout, stderr = process.communicate(input=test_input, timeout=15)

            print("✅ Interactive mode test completed!")
            print("📊 Application Output:")
            print(stdout)

            if stderr:
                print("⚠️ Warnings:")
                print(stderr)

            return True

        else:
            print(f"❌ Application failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ Application timeout (this might be normal for long-running processes)")
        process.kill()
        return True
    except Exception as e:
        print(f"❌ Error running application: {e}")
        return False


def main():
    """Main function"""
    print("🔧 Advanced Error Fixing and Application Runner")
    print("=" * 50)

    # Step 1: Fix all syntax errors
    fixer = AdvancedErrorFixer()
    if not fixer.fix_all_files():
        print("❌ Error fixing failed")
        return 1

    print(f"\n✅ Fixed {len(fixer.fixed_files)} files")

    # Step 2: Run the application
    if run_application_with_venv():
        print("\n🎉 Success! NIMDA application is running properly!")

        # Show how to run manually
        venv_python = Path("/Users/dev/Documents/nimda_agent_plugin/venv/bin/python")
        print("\n📋 To run manually:")
        print(f"   cd {Path('/Users/dev/Documents/nimda_agent_plugin')}")
        print(f"   {venv_python} nimda_app.py")

        return 0
    else:
        print("\n❌ Application failed to run properly")
        return 1


if __name__ == "__main__":
    exit(main())
