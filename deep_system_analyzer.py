#!/usr/bin/env python3
"""
Deep System Analyzer - Comprehensive codebase analysis tool
Analyzes structure, metrics, dependencies, issues, and provides recommendations
"""

import ast
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class DeepSystemAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.analysis_report = {
            "timestamp": datetime.now().isoformat(),
            "project_path": str(project_path),
            "structure": {},
            "metrics": {},
            "dependencies": {},
            "issues": [],
            "recommendations": [],
        }

    def analyze_full_system(self, pause_duration: float = 2.0) -> Dict[str, Any]:
        """Perform complete system analysis with pauses"""
        print("🔍 Starting Deep System Analysis...")
        print("=" * 60)

        # Phase 1: Project Structure Analysis
        print("\n📂 Phase 1: Analyzing Project Structure...")
        time.sleep(pause_duration)
        self._analyze_structure()
        print("   ✅ Structure analysis complete")

        # Phase 2: Code Metrics Analysis
        print("\n📊 Phase 2: Computing Code Metrics...")
        time.sleep(pause_duration)
        self._analyze_metrics()
        print("   ✅ Metrics analysis complete")

        # Phase 3: Dependency Analysis
        print("\n🔗 Phase 3: Analyzing Dependencies...")
        time.sleep(pause_duration)
        self._analyze_dependencies()
        print("   ✅ Dependency analysis complete")

        # Phase 4: Issue Detection
        print("\n🚨 Phase 4: Detecting Issues...")
        time.sleep(pause_duration)
        self._detect_issues()
        print("   ✅ Issue detection complete")

        # Phase 5: Generate Recommendations
        print("\n💡 Phase 5: Generating Recommendations...")
        time.sleep(pause_duration)
        self._generate_recommendations()
        print("   ✅ Recommendations generated")

        print("\n🎯 Deep System Analysis Complete!")
        return self.analysis_report

    def _analyze_structure(self):
        """Analyze project directory structure"""
        structure = {
            "total_files": 0,
            "total_directories": 0,
            "python_files": [],
            "config_files": [],
            "documentation": [],
            "test_files": [],
            "other_files": [],
        }

        for root, dirs, files in os.walk(self.project_path):
            structure["total_directories"] += len(dirs)

            for file in files:
                structure["total_files"] += 1
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_path)

                if file.endswith(".py"):
                    structure["python_files"].append(str(relative_path))
                elif file.endswith((".md", ".txt", ".rst")):
                    structure["documentation"].append(str(relative_path))
                elif "test" in file.lower() or file.startswith("test_"):
                    structure["test_files"].append(str(relative_path))
                elif file.endswith((".json", ".yml", ".yaml", ".toml", ".ini")):
                    structure["config_files"].append(str(relative_path))
                else:
                    structure["other_files"].append(str(relative_path))

        self.analysis_report["structure"] = structure

    def _analyze_metrics(self):
        """Analyze code metrics for Python files"""
        metrics = {
            "total_lines": 0,
            "total_functions": 0,
            "total_classes": 0,
            "complexity_scores": [],
            "file_metrics": {},
        }

        for py_file in self.analysis_report["structure"]["python_files"]:
            file_path = self.project_path / py_file
            if file_path.exists():
                file_metrics = self._analyze_python_file(file_path)
                metrics["file_metrics"][py_file] = file_metrics
                metrics["total_lines"] += file_metrics["lines"]
                metrics["total_functions"] += file_metrics["functions"]
                metrics["total_classes"] += file_metrics["classes"]
                if file_metrics["complexity"]:
                    metrics["complexity_scores"].append(file_metrics["complexity"])

        if metrics["complexity_scores"]:
            metrics["avg_complexity"] = sum(metrics["complexity_scores"]) / len(
                metrics["complexity_scores"]
            )
        else:
            metrics["avg_complexity"] = 0

        self.analysis_report["metrics"] = metrics

    def _analyze_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = len(content.splitlines())

            tree = ast.parse(content)

            functions = sum(
                1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
            )
            classes = sum(
                1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
            )

            # Simple complexity metric (number of control flow statements)
            complexity = sum(
                1
                for node in ast.walk(tree)
                if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try))
            )

            return {
                "lines": lines,
                "functions": functions,
                "classes": classes,
                "complexity": complexity,
                "parsed": True,
            }
        except Exception as e:
            return {
                "lines": 0,
                "functions": 0,
                "classes": 0,
                "complexity": 0,
                "parsed": False,
                "error": str(e),
            }

    def _analyze_dependencies(self):
        """Analyze project dependencies"""
        dependencies = {
            "requirements_files": [],
            "imports": [],
            "missing_imports": [],
            "circular_imports": [],
        }

        # Find requirements files
        req_patterns = ["requirements*.txt", "setup.py", "pyproject.toml"]
        for pattern in req_patterns:
            for req_file in self.project_path.glob(pattern):
                dependencies["requirements_files"].append(
                    str(req_file.relative_to(self.project_path))
                )

        # Analyze imports in Python files
        all_imports = set()
        for py_file in self.analysis_report["structure"]["python_files"]:
            file_path = self.project_path / py_file
            file_imports = self._extract_imports(file_path)
            all_imports.update(file_imports)

        dependencies["imports"] = sorted(list(all_imports))

        # Check for missing imports
        for imp in all_imports:
            if not self._can_import(imp):
                dependencies["missing_imports"].append(imp)

        self.analysis_report["dependencies"] = dependencies

    def _extract_imports(self, file_path: Path) -> List[str]:
        """Extract imports from a Python file"""
        imports = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        except Exception:
            pass

        return imports

    def _can_import(self, module_name: str) -> bool:
        """Check if a module can be imported"""
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False

    def _detect_issues(self):
        """Detect potential issues in the codebase"""
        issues = []

        # Check for syntax errors
        for py_file in self.analysis_report["structure"]["python_files"]:
            if not self.analysis_report["metrics"]["file_metrics"][py_file]["parsed"]:
                issues.append(
                    {
                        "type": "syntax_error",
                        "file": py_file,
                        "description": "File has syntax errors",
                        "severity": "high",
                    }
                )

        # Check for missing imports
        if self.analysis_report["dependencies"]["missing_imports"]:
            issues.append(
                {
                    "type": "missing_dependencies",
                    "description": f"Missing imports: {', '.join(self.analysis_report['dependencies']['missing_imports'])}",
                    "severity": "high",
                }
            )

        # Check for high complexity files
        for py_file, metrics in self.analysis_report["metrics"]["file_metrics"].items():
            if metrics["complexity"] > 15:
                issues.append(
                    {
                        "type": "high_complexity",
                        "file": py_file,
                        "description": f"High complexity score: {metrics['complexity']}",
                        "severity": "medium",
                    }
                )

        # Check for empty Python files
        for py_file, metrics in self.analysis_report["metrics"]["file_metrics"].items():
            if metrics["lines"] < 5:
                issues.append(
                    {
                        "type": "empty_file",
                        "file": py_file,
                        "description": "File appears to be empty or minimal",
                        "severity": "low",
                    }
                )

        self.analysis_report["issues"] = issues

    def _generate_recommendations(self):
        """Generate actionable recommendations"""
        recommendations = []

        # Recommendations based on issues
        high_issues = [
            i for i in self.analysis_report["issues"] if i["severity"] == "high"
        ]
        if high_issues:
            recommendations.append(
                {
                    "category": "critical",
                    "title": "Fix Critical Issues",
                    "description": f"Address {len(high_issues)} high-severity issues immediately",
                    "actions": ["Fix syntax errors", "Install missing dependencies"],
                }
            )

        # Code organization recommendations
        if self.analysis_report["metrics"]["total_functions"] > 50:
            recommendations.append(
                {
                    "category": "organization",
                    "title": "Consider Code Modularization",
                    "description": "Large number of functions detected",
                    "actions": [
                        "Group related functions into classes",
                        "Split large modules",
                    ],
                }
            )

        # Testing recommendations
        test_ratio = len(self.analysis_report["structure"]["test_files"]) / max(
            1, len(self.analysis_report["structure"]["python_files"])
        )
        if test_ratio < 0.3:
            recommendations.append(
                {
                    "category": "testing",
                    "title": "Improve Test Coverage",
                    "description": f"Test-to-code ratio is {test_ratio:.2f}",
                    "actions": ["Add unit tests", "Create integration tests"],
                }
            )

        # Documentation recommendations
        doc_ratio = len(self.analysis_report["structure"]["documentation"]) / max(
            1, self.analysis_report["structure"]["total_files"]
        )
        if doc_ratio < 0.1:
            recommendations.append(
                {
                    "category": "documentation",
                    "title": "Add Documentation",
                    "description": "Limited documentation found",
                    "actions": [
                        "Create README files",
                        "Add docstrings",
                        "Document APIs",
                    ],
                }
            )

        self.analysis_report["recommendations"] = recommendations

    def save_report(self, output_file: str = "SYSTEM_ANALYSIS_REPORT.md") -> Path:
        """Save analysis report as markdown"""
        report_path = self.project_path / output_file

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Deep System Analysis Report\n\n")
            f.write(f"**Generated:** {self.analysis_report['timestamp']}\n")
            f.write(f"**Project:** {self.analysis_report['project_path']}\n\n")

            # Structure section
            f.write("## Project Structure\n\n")
            structure = self.analysis_report["structure"]
            f.write(f"- **Total Files:** {structure['total_files']}\n")
            f.write(f"- **Total Directories:** {structure['total_directories']}\n")
            f.write(f"- **Python Files:** {len(structure['python_files'])}\n")
            f.write(f"- **Test Files:** {len(structure['test_files'])}\n")
            f.write(f"- **Documentation:** {len(structure['documentation'])}\n\n")

            # Metrics section
            f.write("## Code Metrics\n\n")
            metrics = self.analysis_report["metrics"]
            f.write(f"- **Total Lines:** {metrics['total_lines']}\n")
            f.write(f"- **Total Functions:** {metrics['total_functions']}\n")
            f.write(f"- **Total Classes:** {metrics['total_classes']}\n")
            f.write(
                f"- **Average Complexity:** {metrics.get('avg_complexity', 0):.2f}\n\n"
            )

            # Issues section
            f.write("## Issues Found\n\n")
            for issue in self.analysis_report["issues"]:
                f.write(f"- **{issue['severity'].upper()}:** {issue['description']}")
                if "file" in issue:
                    f.write(f" (in {issue['file']})")
                f.write("\n")
            f.write("\n")

            # Recommendations section
            f.write("## Recommendations\n\n")
            for rec in self.analysis_report["recommendations"]:
                f.write(f"### {rec['title']} ({rec['category']})\n")
                f.write(f"{rec['description']}\n\n")
                f.write("**Actions:**\n")
                for action in rec["actions"]:
                    f.write(f"- {action}\n")
                f.write("\n")

        return report_path

    def print_summary(self):
        """Print a concise analysis summary"""
        print("\n" + "=" * 60)
        print("📋 DEEP SYSTEM ANALYSIS SUMMARY")
        print("=" * 60)

        structure = self.analysis_report["structure"]
        metrics = self.analysis_report["metrics"]
        issues = self.analysis_report["issues"]

        print(
            f"📁 Files: {structure['total_files']} | Python: {len(structure['python_files'])}"
        )
        print(
            f"📊 Code: {metrics['total_lines']} lines | {metrics['total_functions']} functions | {metrics['total_classes']} classes"
        )
        print(
            f"🚨 Issues: {len(issues)} total ({len([i for i in issues if i['severity'] == 'high'])} high severity)"
        )
        print(f"💡 Recommendations: {len(self.analysis_report['recommendations'])}")

        if issues:
            print("\n🔴 Critical Issues:")
            for issue in issues[:3]:  # Show first 3 issues
                print(f"   • {issue['description']}")
