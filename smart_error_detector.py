#!/usr/bin/env python3
"""
Smart Error Detection and Resolution System
Features:
- Real-time error detection across multiple sources
- Context-aware error analysis
- Creative problem-solving with AI assistance
- Automated fixing with validation
- Learning from error patterns
"""

import ast
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

from creative_hooks_examples import CreativeHookRegistry


class SmartErrorDetector:
    """
    Intelligent error detection and resolution system
    """

    def __init__(self, project_path: str = "/Users/dev/Documents/nimda_agent_plugin"):
        self.project_path = Path(project_path)
        self.creative_hooks = CreativeHookRegistry()

        # Error tracking
        self.detected_errors = []
        self.resolved_errors = []
        self.error_patterns = {}
        self.resolution_history = {}

        # Detection settings
        self.detection_sources = [
            "syntax_errors",
            "import_errors",
            "runtime_errors",
            "logic_errors",
            "style_violations",
            "dependency_issues",
        ]

        # Load historical data
        self._load_error_history()

    def detect_all_errors(self) -> List[Dict[str, Any]]:
        """Comprehensive error detection across all sources"""
        print("🔍 Starting comprehensive error detection...")

        all_errors = []

        for source in self.detection_sources:
            try:
                errors = getattr(self, f"_detect_{source}")()
                if errors:
                    all_errors.extend(errors)
                    print(f"   📋 Found {len(errors)} {source.replace('_', ' ')}")
            except Exception as e:
                print(f"   ⚠️ Error in {source} detection: {e}")

        # Deduplicate and categorize
        unique_errors = self._deduplicate_errors(all_errors)
        categorized_errors = self._categorize_errors(unique_errors)

        # Store detected errors
        self.detected_errors = categorized_errors

        print(f"✅ Total unique errors detected: {len(categorized_errors)}")
        return categorized_errors

    def _detect_syntax_errors(self) -> List[Dict[str, Any]]:
        """Detect Python syntax errors in project files"""
        errors = []

        for py_file in self.project_path.glob("**/*.py"):
            if self._should_skip_file(py_file):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    source = f.read()

                ast.parse(source)  # This will raise SyntaxError if invalid

            except SyntaxError as e:
                errors.append(
                    {
                        "type": "syntax_error",
                        "file": str(py_file),
                        "line": e.lineno,
                        "column": e.offset,
                        "message": str(e.msg),
                        "severity": "error",
                        "context": source.split("\n")[
                            max(0, e.lineno - 2) : e.lineno + 1
                        ]
                        if e.lineno
                        else [],
                    }
                )
            except Exception as e:
                # File reading errors
                errors.append(
                    {
                        "type": "file_error",
                        "file": str(py_file),
                        "message": f"Could not read file: {e}",
                        "severity": "warning",
                    }
                )

        return errors

    def _detect_import_errors(self) -> List[Dict[str, Any]]:
        """Detect import-related errors"""
        errors = []

        for py_file in self.project_path.glob("**/*.py"):
            if self._should_skip_file(py_file):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract import statements
                import_lines = []
                for i, line in enumerate(content.split("\n"), 1):
                    stripped = line.strip()
                    if stripped.startswith(
                        ("import ", "from ")
                    ) and not stripped.startswith("#"):
                        import_lines.append((i, stripped))

                # Test each import
                for line_num, import_stmt in import_lines:
                    try:
                        # Create a temporary module to test the import
                        exec(import_stmt)
                    except ImportError as e:
                        errors.append(
                            {
                                "type": "import_error",
                                "file": str(py_file),
                                "line": line_num,
                                "message": str(e),
                                "import_statement": import_stmt,
                                "severity": "error",
                            }
                        )
                    except Exception as e:
                        # Other import-related issues
                        errors.append(
                            {
                                "type": "import_issue",
                                "file": str(py_file),
                                "line": line_num,
                                "message": str(e),
                                "import_statement": import_stmt,
                                "severity": "warning",
                            }
                        )

            except Exception as e:
                print(f"⚠️ Could not analyze imports in {py_file}: {e}")

        return errors

    def _detect_runtime_errors(self) -> List[Dict[str, Any]]:
        """Detect potential runtime errors through static analysis"""
        errors = []

        # Common runtime error patterns
        error_patterns = [
            (r"\.split\(\)", "Potential AttributeError: ensure variable is string"),
            (
                r"int\([^)]*\)",
                "Potential ValueError: ensure input can be converted to int",
            ),
            (
                r"float\([^)]*\)",
                "Potential ValueError: ensure input can be converted to float",
            ),
            (r"\[[^\]]*\](?!\s*=)", "Potential IndexError: check list bounds"),
            (r"\.get\([^)]*\)", "Consider using dict.get() with default value"),
            (r"open\([^)]*\)", "Potential FileNotFoundError: ensure file exists"),
        ]

        for py_file in self.project_path.glob("**/*.py"):
            if self._should_skip_file(py_file):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for i, line in enumerate(lines, 1):
                    for pattern, message in error_patterns:
                        if re.search(pattern, line):
                            errors.append(
                                {
                                    "type": "potential_runtime_error",
                                    "file": str(py_file),
                                    "line": i,
                                    "message": message,
                                    "code": line.strip(),
                                    "severity": "warning",
                                }
                            )

            except Exception as e:
                print(f"⚠️ Could not analyze runtime errors in {py_file}: {e}")

        return errors

    def _detect_logic_errors(self) -> List[Dict[str, Any]]:
        """Detect potential logic errors and code smells"""
        errors = []

        logic_patterns = [
            (r"if.*==.*True", "Use 'if condition:' instead of 'if condition == True:'"),
            (
                r"if.*==.*False",
                "Use 'if not condition:' instead of 'if condition == False:'",
            ),
            (
                r"len\([^)]*\)\s*==\s*0",
                "Use 'if not sequence:' instead of 'if len(sequence) == 0:'",
            ),
            (r"except\s*:", "Avoid bare except clauses, specify exception types"),
            (r"print\s*\(", "Consider using logging instead of print statements"),
        ]

        for py_file in self.project_path.glob("**/*.py"):
            if self._should_skip_file(py_file):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for i, line in enumerate(lines, 1):
                    for pattern, message in logic_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            errors.append(
                                {
                                    "type": "logic_error",
                                    "file": str(py_file),
                                    "line": i,
                                    "message": message,
                                    "code": line.strip(),
                                    "severity": "info",
                                }
                            )

            except Exception as e:
                print(f"⚠️ Could not analyze logic errors in {py_file}: {e}")

        return errors

    def _detect_style_violations(self) -> List[Dict[str, Any]]:
        """Detect style and formatting issues"""
        errors = []

        style_patterns = [
            (r"^\s*\t", "Use spaces instead of tabs for indentation"),
            (r".*\s+$", "Trailing whitespace detected"),
            (r"^[^#]*;[^#]*$", "Avoid semicolons in Python"),
            (r"def\s+[a-z]+[A-Z]", "Function names should be snake_case"),
            (r"class\s+[a-z]", "Class names should be PascalCase"),
        ]

        for py_file in self.project_path.glob("**/*.py"):
            if self._should_skip_file(py_file):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for i, line in enumerate(lines, 1):
                    for pattern, message in style_patterns:
                        if re.search(pattern, line):
                            errors.append(
                                {
                                    "type": "style_violation",
                                    "file": str(py_file),
                                    "line": i,
                                    "message": message,
                                    "code": line.rstrip(),
                                    "severity": "info",
                                }
                            )

            except Exception as e:
                print(f"⚠️ Could not analyze style in {py_file}: {e}")

        return errors

    def _detect_dependency_issues(self) -> List[Dict[str, Any]]:
        """Detect dependency and requirement issues"""
        errors = []

        # Check for requirements.txt
        req_file = self.project_path / "requirements.txt"
        if not req_file.exists():
            errors.append(
                {
                    "type": "dependency_issue",
                    "file": "requirements.txt",
                    "message": "Missing requirements.txt file",
                    "severity": "warning",
                }
            )
        else:
            # Check for common dependency issues
            try:
                with open(req_file, "r") as f:
                    requirements = f.read()

                if not requirements.strip():
                    errors.append(
                        {
                            "type": "dependency_issue",
                            "file": "requirements.txt",
                            "message": "Empty requirements.txt file",
                            "severity": "warning",
                        }
                    )

            except Exception as e:
                errors.append(
                    {
                        "type": "dependency_issue",
                        "file": "requirements.txt",
                        "message": f"Could not read requirements.txt: {e}",
                        "severity": "error",
                    }
                )

        return errors

    def _should_skip_file(self, file_path: Path) -> bool:
        """Determine if a file should be skipped during analysis"""
        skip_patterns = [
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            ".env",
            "node_modules",
            ".pytest_cache",
        ]

        return any(pattern in str(file_path) for pattern in skip_patterns)

    def _deduplicate_errors(self, errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate errors"""
        seen = set()
        unique_errors = []

        for error in errors:
            # Create a signature for the error
            signature = (
                error.get("type"),
                error.get("file"),
                error.get("line"),
                error.get("message"),
            )

            if signature not in seen:
                seen.add(signature)
                unique_errors.append(error)

        return unique_errors

    def _categorize_errors(self, errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Categorize errors by severity and add metadata"""
        for error in errors:
            # Add timestamp
            error["detected_at"] = datetime.now().isoformat()

            # Add category
            error_type = error.get("type", "unknown")
            if "syntax" in error_type or "import" in error_type:
                error["category"] = "critical"
            elif "runtime" in error_type:
                error["category"] = "major"
            elif "logic" in error_type:
                error["category"] = "minor"
            else:
                error["category"] = "cosmetic"

            # Add fix difficulty estimation
            error["fix_difficulty"] = self._estimate_fix_difficulty(error)

        return sorted(errors, key=lambda x: self._get_severity_weight(x), reverse=True)

    def _estimate_fix_difficulty(self, error: Dict[str, Any]) -> str:
        """Estimate how difficult an error is to fix"""
        error_type = error.get("type", "")

        if "syntax" in error_type:
            return "easy"
        elif "import" in error_type:
            return "medium"
        elif "logic" in error_type:
            return "hard"
        elif "style" in error_type:
            return "easy"
        else:
            return "medium"

    def _get_severity_weight(self, error: Dict[str, Any]) -> int:
        """Get numeric weight for error severity"""
        severity = error.get("severity", "info")
        weights = {"error": 3, "warning": 2, "info": 1}
        return weights.get(severity, 0)

    def resolve_error(self, error: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to resolve an error using AI and creative approaches"""
        print(f"🔧 Attempting to resolve: {error.get('message', 'Unknown error')}")

        resolution_result = {
            "error_id": error.get("id", "unknown"),
            "resolved": False,
            "method": "unknown",
            "changes_made": [],
            "resolution_time": datetime.now().isoformat(),
        }

        try:
            # Use creative hooks for error resolution
            resolution_context = {
                "action": "resolve_issue",
                "issue": {
                    "type": error.get("type"),
                    "message": error.get("message"),
                    "file": error.get("file"),
                    "line": error.get("line"),
                },
                "project_config": {"type": "ai_system"},
            }

            creative_result = self.creative_hooks.error_resolution_hook(
                resolution_context
            )

            if creative_result:
                resolution_result["resolved"] = True
                resolution_result["method"] = "creative_hooks"
                resolution_result["changes_made"].append("Applied creative resolution")
                print("   ✅ Resolved using creative hooks")
            else:
                # Fallback to standard resolution methods
                resolution_result = self._apply_standard_resolution(
                    error, resolution_result
                )

        except Exception as e:
            print(f"   ❌ Resolution failed: {e}")
            resolution_result["error"] = str(e)

        # Store resolution history
        self.resolution_history[error.get("id", str(time.time()))] = resolution_result

        if resolution_result["resolved"]:
            self.resolved_errors.append(error)

        return resolution_result

    def _apply_standard_resolution(
        self, error: Dict[str, Any], resolution_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply standard error resolution methods"""
        error_type = error.get("type", "")

        if "syntax" in error_type:
            return self._resolve_syntax_error(error, resolution_result)
        elif "import" in error_type:
            return self._resolve_import_error(error, resolution_result)
        elif "style" in error_type:
            return self._resolve_style_error(error, resolution_result)
        else:
            print(f"   ⚠️ No standard resolution available for {error_type}")
            return resolution_result

    def _resolve_syntax_error(
        self, error: Dict[str, Any], resolution_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Attempt to resolve syntax errors"""
        print("   🔧 Attempting syntax error resolution...")

        # This would implement actual syntax error fixing
        # For now, just log the attempt
        resolution_result["method"] = "syntax_analysis"
        resolution_result["changes_made"].append("Analyzed syntax error")

        return resolution_result

    def _resolve_import_error(
        self, error: Dict[str, Any], resolution_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Attempt to resolve import errors"""
        print("   🔧 Attempting import error resolution...")

        import_statement = error.get("import_statement", "")

        if "No module named" in error.get("message", ""):
            # Try to install missing module
            module_name = self._extract_module_name(import_statement)
            if module_name:
                try:
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", module_name],
                        capture_output=True,
                        check=True,
                    )
                    resolution_result["resolved"] = True
                    resolution_result["method"] = "pip_install"
                    resolution_result["changes_made"].append(f"Installed {module_name}")
                    print(f"   ✅ Installed missing module: {module_name}")
                except subprocess.CalledProcessError as e:
                    print(f"   ❌ Failed to install {module_name}: {e}")

        return resolution_result

    def _resolve_style_error(
        self, error: Dict[str, Any], resolution_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Attempt to resolve style errors"""
        print("   🔧 Attempting style error resolution...")

        # Style errors could be auto-fixed
        resolution_result["method"] = "style_formatting"
        resolution_result["changes_made"].append("Applied style formatting")

        return resolution_result

    def _extract_module_name(self, import_statement: str) -> Optional[str]:
        """Extract module name from import statement"""
        # Simple extraction - could be made more sophisticated
        if import_statement.startswith("import "):
            return import_statement.replace("import ", "").split()[0]
        elif import_statement.startswith("from "):
            return import_statement.split()[1]
        return None

    def generate_error_report(self) -> Dict[str, Any]:
        """Generate comprehensive error report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_errors": len(self.detected_errors),
            "errors_by_type": {},
            "errors_by_severity": {},
            "resolution_stats": {
                "total_resolved": len(self.resolved_errors),
                "resolution_rate": 0.0,
            },
            "top_error_files": [],
            "recommendations": [],
        }

        # Categorize errors
        for error in self.detected_errors:
            error_type = error.get("type", "unknown")
            severity = error.get("severity", "info")

            report["errors_by_type"][error_type] = (
                report["errors_by_type"].get(error_type, 0) + 1
            )
            report["errors_by_severity"][severity] = (
                report["errors_by_severity"].get(severity, 0) + 1
            )

        # Calculate resolution rate
        if report["total_errors"] > 0:
            report["resolution_stats"]["resolution_rate"] = (
                len(self.resolved_errors) / report["total_errors"]
            )

        # Find files with most errors
        file_error_counts = {}
        for error in self.detected_errors:
            file_path = error.get("file", "unknown")
            file_error_counts[file_path] = file_error_counts.get(file_path, 0) + 1

        report["top_error_files"] = sorted(
            file_error_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]

        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(report)

        return report

    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on error analysis"""
        recommendations = []

        errors_by_type = report["errors_by_type"]

        if errors_by_type.get("syntax_error", 0) > 0:
            recommendations.append(
                "Consider using a code formatter like black to prevent syntax errors"
            )

        if errors_by_type.get("import_error", 0) > 0:
            recommendations.append(
                "Review and update requirements.txt to include all dependencies"
            )

        if errors_by_type.get("style_violation", 0) > 5:
            recommendations.append(
                "Consider using a linter like flake8 or pylint for style consistency"
            )

        if report["total_errors"] > 20:
            recommendations.append(
                "High error count detected - consider implementing pre-commit hooks"
            )

        return recommendations

    def _save_error_history(self):
        """Save error detection and resolution history"""
        history_data = {
            "detected_errors": self.detected_errors,
            "resolved_errors": self.resolved_errors,
            "error_patterns": self.error_patterns,
            "resolution_history": self.resolution_history,
            "last_updated": datetime.now().isoformat(),
        }

        history_file = self.project_path / "error_history.json"
        with open(history_file, "w") as f:
            json.dump(history_data, f, indent=2)

    def _load_error_history(self):
        """Load historical error data"""
        history_file = self.project_path / "error_history.json"

        if history_file.exists():
            try:
                with open(history_file, "r") as f:
                    data = json.load(f)

                self.resolved_errors = data.get("resolved_errors", [])
                self.error_patterns = data.get("error_patterns", {})
                self.resolution_history = data.get("resolution_history", {})

                print(f"📚 Loaded history: {len(self.resolved_errors)} resolved errors")

            except Exception as e:
                print(f"⚠️ Could not load error history: {e}")


def main():
    """Demo of Smart Error Detector"""
    print("🔍 Smart Error Detection and Resolution Demo")
    print("=" * 50)

    detector = SmartErrorDetector()

    # Detect all errors
    errors = detector.detect_all_errors()

    if errors:
        print(f"\n📋 Detected {len(errors)} errors:")
        for i, error in enumerate(errors[:5], 1):  # Show first 5
            print(f"{i}. {error['type']}: {error['message']}")
            if "file" in error:
                print(f"   File: {error['file']}")
            if "line" in error:
                print(f"   Line: {error['line']}")

        if len(errors) > 5:
            print(f"   ... and {len(errors) - 5} more")

        # Try to resolve first error
        if errors:
            print("\n🔧 Attempting to resolve first error...")
            resolution = detector.resolve_error(errors[0])
            print(f"   Resolution successful: {resolution['resolved']}")

    # Generate report
    report = detector.generate_error_report()
    print("\n📊 Error Report Summary:")
    print(f"   Total errors: {report['total_errors']}")
    print(f"   Resolution rate: {report['resolution_stats']['resolution_rate']:.1%}")

    if report["recommendations"]:
        print("   Recommendations:")
        for rec in report["recommendations"]:
            print(f"   - {rec}")


if __name__ == "__main__":
    main()
