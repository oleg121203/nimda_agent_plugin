#!/usr/bin/env python3.11
"""
Python 3.11 Compliance and English Localization System
Ensures all components use Python 3.11+ features and English development standards
"""

import ast
import asyncio
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure Python 3.11+
if sys.version_info < (3, 11):
    print("❌ ERROR: Python 3.11+ is required for NIMDA development")
    print(f"Current version: {sys.version}")
    print("Please upgrade to Python 3.11 or higher")
    sys.exit(1)

print(
    f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Compliance check passed"
)


class Python311ComplianceSystem:
    """
    Advanced system for ensuring Python 3.11+ compliance and English development standards
    """

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.compliance_issues = []
        self.recommendations = []

    async def run_compliance_check(self) -> Dict[str, Any]:
        """Run complete compliance check"""
        print("🔍 PYTHON 3.11 COMPLIANCE & ENGLISH LOCALIZATION CHECK")
        print("=" * 60)

        results = {
            "python_version_check": await self._check_python_version(),
            "code_analysis": await self._analyze_python_files(),
            "english_compliance": await self._check_english_compliance(),
            "feature_opportunities": await self._identify_python311_opportunities(),
            "compliance_score": 0,
            "recommendations": [],
        }

        # Calculate compliance score
        results["compliance_score"] = await self._calculate_compliance_score(results)
        results["recommendations"] = self.recommendations

        await self._generate_compliance_report(results)

        return results

    async def _check_python_version(self) -> Dict[str, Any]:
        """Check Python version compliance"""
        print("🐍 Checking Python version compliance...")

        version_info = {
            "current_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "is_compliant": sys.version_info >= (3, 11),
            "required_version": "3.11+",
            "features_available": [],
        }

        if sys.version_info >= (3, 11):
            version_info["features_available"] = [
                "Enhanced error messages",
                "Pattern matching improvements",
                "Exception groups",
                "Faster CPython implementation",
                "TOML support in stdlib",
                "Improved typing features",
            ]
            print("   ✅ Python 3.11+ compliance verified")
        else:
            print("   ❌ Python version not compliant")
            self.compliance_issues.append("Python version below 3.11")

        return version_info

    async def _analyze_python_files(self) -> Dict[str, Any]:
        """Analyze Python files for compliance"""
        print("📄 Analyzing Python files for 3.11+ features...")

        analysis = {
            "files_analyzed": 0,
            "syntax_errors": [],
            "deprecated_features": [],
            "python311_features_used": [],
            "missing_type_hints": [],
        }

        python_files = list(self.project_path.rglob("*.py"))

        for file_path in python_files:
            analysis["files_analyzed"] += 1

            try:
                content = file_path.read_text(encoding="utf-8")

                # Parse AST for analysis
                tree = ast.parse(content)

                # Check for Python 3.11 features
                await self._analyze_ast_for_features(tree, file_path, analysis)

                # Check for deprecated patterns
                await self._check_deprecated_patterns(content, file_path, analysis)

            except SyntaxError as e:
                analysis["syntax_errors"].append(
                    {
                        "file": str(file_path.relative_to(self.project_path)),
                        "error": str(e),
                    }
                )
            except Exception as e:
                print(f"   ⚠️  Error analyzing {file_path.name}: {e}")

        print(f"   📊 Analyzed {analysis['files_analyzed']} Python files")

        return analysis

    async def _analyze_ast_for_features(
        self, tree: ast.AST, file_path: Path, analysis: Dict[str, Any]
    ):
        """Analyze AST for Python 3.11 features and typing"""

        project_path = self.project_path  # Store reference for inner class

        class FeatureVisitor(ast.NodeVisitor):
            def __init__(self):
                self.has_type_hints = False
                self.has_match_statement = False
                self.functions_without_hints = []

            def visit_FunctionDef(self, node):
                # Check for type hints
                has_return_annotation = node.returns is not None
                has_arg_annotations = any(arg.annotation for arg in node.args.args)

                if not (has_return_annotation or has_arg_annotations):
                    self.functions_without_hints.append(node.name)
                else:
                    self.has_type_hints = True

                self.generic_visit(node)

            def visit_Match(self, node):
                self.has_match_statement = True
                analysis["python311_features_used"].append(
                    {
                        "feature": "match_statement",
                        "file": str(file_path.relative_to(project_path)),
                        "line": node.lineno,
                    }
                )
                self.generic_visit(node)

        visitor = FeatureVisitor()
        visitor.visit(tree)

        if visitor.functions_without_hints:
            analysis["missing_type_hints"].extend(
                [
                    {
                        "file": str(file_path.relative_to(self.project_path)),
                        "functions": visitor.functions_without_hints,
                    }
                ]
            )

    async def _check_deprecated_patterns(
        self, content: str, file_path: Path, analysis: Dict[str, Any]
    ):
        """Check for deprecated patterns"""
        deprecated_patterns = [
            (
                r"from typing import Dict, List",
                "Use built-in dict, list in Python 3.9+",
            ),
            (r"typing\.Dict\[", "Use dict[] instead of typing.Dict[]"),
            (r"typing\.List\[", "Use list[] instead of typing.List[]"),
            (r"\.format\(", "Consider using f-strings for better performance"),
        ]

        for pattern, suggestion in deprecated_patterns:
            if re.search(pattern, content):
                analysis["deprecated_features"].append(
                    {
                        "file": str(file_path.relative_to(self.project_path)),
                        "pattern": pattern,
                        "suggestion": suggestion,
                    }
                )

    async def _check_english_compliance(self) -> Dict[str, Any]:
        """Check for English compliance in comments and strings"""
        print("🌍 Checking English language compliance...")

        compliance = {
            "non_english_comments": [],
            "non_english_strings": [],
            "compliance_percentage": 0,
        }

        # Patterns for non-English text (basic detection)
        non_english_patterns = [
            r"[а-яё]",  # Cyrillic
            r"[ґєії]",  # Ukrainian specific
            r"#.*[а-яё]",  # Comments with Cyrillic
        ]

        python_files = list(self.project_path.rglob("*.py"))
        total_items = 0
        compliant_items = 0

        for file_path in python_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                lines = content.split("\n")

                for line_num, line in enumerate(lines, 1):
                    total_items += 1

                    # Check comments
                    if "#" in line:
                        comment = line[line.index("#") :]
                        has_non_english = any(
                            re.search(pattern, comment, re.IGNORECASE)
                            for pattern in non_english_patterns
                        )

                        if has_non_english:
                            compliance["non_english_comments"].append(
                                {
                                    "file": str(
                                        file_path.relative_to(self.project_path)
                                    ),
                                    "line": line_num,
                                    "content": comment.strip(),
                                }
                            )
                        else:
                            compliant_items += 1
                    else:
                        compliant_items += 1

            except Exception as e:
                print(f"   ⚠️  Error checking {file_path.name}: {e}")

        if total_items > 0:
            compliance["compliance_percentage"] = (compliant_items / total_items) * 100

        print(f"   📊 English compliance: {compliance['compliance_percentage']:.1f}%")

        return compliance

    async def _identify_python311_opportunities(self) -> List[Dict[str, Any]]:
        """Identify opportunities to use Python 3.11+ features"""
        print("💡 Identifying Python 3.11+ enhancement opportunities...")

        opportunities = [
            {
                "feature": "Enhanced Error Messages",
                "description": "Python 3.11 provides more detailed error messages",
                "implementation": "Already available - no changes needed",
                "benefit": "Better debugging experience",
            },
            {
                "feature": "Pattern Matching",
                "description": "Use match/case statements for complex conditionals",
                "implementation": "Replace complex if/elif chains with match statements",
                "benefit": "More readable and maintainable code",
            },
            {
                "feature": "Exception Groups",
                "description": "Handle multiple exceptions simultaneously",
                "implementation": "Use ExceptionGroup for batch operations",
                "benefit": "Better error handling in async operations",
            },
            {
                "feature": "TOML Support",
                "description": "Built-in TOML parsing with tomllib",
                "implementation": "Use tomllib instead of third-party TOML libraries",
                "benefit": "Reduced dependencies",
            },
            {
                "feature": "Improved Type Hints",
                "description": "Self, TypeVarTuple, and other typing improvements",
                "implementation": "Enhance type annotations throughout codebase",
                "benefit": "Better IDE support and static analysis",
            },
        ]

        return opportunities

    async def _calculate_compliance_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall compliance score"""
        score = 0.0

        # Python version (40 points)
        if results["python_version_check"]["is_compliant"]:
            score += 40

        # Code quality (30 points)
        code_analysis = results["code_analysis"]
        if code_analysis["syntax_errors"]:
            score -= len(code_analysis["syntax_errors"]) * 5

        if code_analysis["files_analyzed"] > 0:
            type_hint_coverage = 1 - (
                len(code_analysis["missing_type_hints"])
                / code_analysis["files_analyzed"]
            )
            score += type_hint_coverage * 15

            deprecated_penalty = min(len(code_analysis["deprecated_features"]) * 2, 10)
            score += 15 - deprecated_penalty

        # English compliance (30 points)
        english_score = (
            results["english_compliance"]["compliance_percentage"] / 100 * 30
        )
        score += english_score

        return min(max(score, 0), 100)

    async def _generate_compliance_report(self, results: Dict[str, Any]):
        """Generate compliance report"""
        report_path = self.project_path / "PYTHON311_COMPLIANCE_REPORT.md"

        report = f"""# Python 3.11 Compliance Report

**Generated**: {asyncio.get_event_loop().time()}
**Compliance Score**: {results["compliance_score"]:.1f}/100

## Python Version Check
- **Current Version**: {results["python_version_check"]["current_version"]}
- **Compliant**: {"✅" if results["python_version_check"]["is_compliant"] else "❌"}
- **Available Features**: {len(results["python_version_check"]["features_available"])}

## Code Analysis
- **Files Analyzed**: {results["code_analysis"]["files_analyzed"]}
- **Syntax Errors**: {len(results["code_analysis"]["syntax_errors"])}
- **Deprecated Features**: {len(results["code_analysis"]["deprecated_features"])}
- **Python 3.11 Features Used**: {len(results["code_analysis"]["python311_features_used"])}

## English Compliance
- **Compliance Percentage**: {results["english_compliance"]["compliance_percentage"]:.1f}%
- **Non-English Comments**: {len(results["english_compliance"]["non_english_comments"])}

## Enhancement Opportunities
{len(results["feature_opportunities"])} Python 3.11+ features available for implementation

## Recommendations
"""

        for rec in self.recommendations:
            report += f"- {rec}\n"

        report_path.write_text(report, encoding="utf-8")
        print(f"📄 Compliance report saved to: {report_path}")


async def modernize_codebase_to_python311():
    """Modernize existing codebase to Python 3.11 standards"""
    print("\n🔧 MODERNIZING CODEBASE TO PYTHON 3.11 STANDARDS")
    print("=" * 55)

    project_path = Path(".")

    # Update shebang lines
    print("📝 Updating shebang lines...")
    python_files = list(project_path.rglob("*.py"))

    for file_path in python_files:
        try:
            content = file_path.read_text(encoding="utf-8")

            # Update shebang to Python 3.11
            if content.startswith("#!/usr/bin/env python3"):
                content = content.replace(
                    "#!/usr/bin/env python3", "#!/usr/bin/env python3.11", 1
                )
                file_path.write_text(content, encoding="utf-8")
                print(f"   ✅ Updated shebang in {file_path.name}")
        except Exception as e:
            print(f"   ⚠️  Error updating {file_path.name}: {e}")

    # Create requirements.txt with Python 3.11 requirement
    print("📦 Creating Python 3.11 requirements.txt...")
    requirements_content = """# NIMDA Agent System Requirements
# Requires Python 3.11+

# Core dependencies for high-level development
asyncio-mqtt>=0.11.1
aiofiles>=23.1.0
rich>=13.3.5

# Optional dependencies (install as needed)
# PySide6>=6.5.0              # For GUI development
# faiss-cpu>=1.7.4           # For vector search (already detected)
# PyObjC-core>=9.2           # For macOS integration
# pytest>=7.3.1             # For testing
# black>=23.3.0              # For code formatting
# mypy>=1.3.0               # For type checking

# Development tools
pre-commit>=3.3.2
"""

    requirements_path = project_path / "requirements.txt"
    requirements_path.write_text(requirements_content, encoding="utf-8")
    print(f"   ✅ Created requirements.txt with Python 3.11+ specification")

    # Create setup.py with Python 3.11 requirement
    print("⚙️  Creating setup.py with Python 3.11 requirement...")
    setup_content = '''#!/usr/bin/env python3.11
"""
Setup script for NIMDA Agent System
Requires Python 3.11+ for advanced features and performance
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

setup(
    name="nimda-agent-system",
    version="1.0.0",
    description="High-level AI-enhanced agent system with deep context awareness",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="NIMDA Development Team", 
    author_email="dev@nimda-system.ai",
    url="https://github.com/nimda-ai/agent-system",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "asyncio-mqtt>=0.11.1",
        "aiofiles>=23.1.0", 
        "rich>=13.3.5",
    ],
    extras_require={
        "gui": ["PySide6>=6.5.0"],
        "macos": ["PyObjC-core>=9.2"],
        "vector-search": ["faiss-cpu>=1.7.4"],
        "dev": [
            "pytest>=7.3.1",
            "black>=23.3.0",
            "mypy>=1.3.0",
            "pre-commit>=3.3.2"
        ]
    },
    entry_points={
        "console_scripts": [
            "nimda=run_nimda:main",
            "nimda-deep=run_deep_workflow:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords="ai agents automation development high-level context-aware",
    project_urls={
        "Bug Reports": "https://github.com/nimda-ai/agent-system/issues",
        "Source": "https://github.com/nimda-ai/agent-system",
        "Documentation": "https://nimda-docs.ai",
    }
)
'''

    setup_path = project_path / "setup.py"
    setup_path.write_text(setup_content, encoding="utf-8")
    print(f"   ✅ Created setup.py with Python 3.11+ requirement")


async def main():
    """Main function for compliance checking and modernization"""
    print("🚀 PYTHON 3.11 COMPLIANCE AND MODERNIZATION SYSTEM")
    print("=" * 60)
    print("🎯 Ensuring Python 3.11+ compliance and English development standards")
    print("🌍 Converting all development to English language")
    print("=" * 60)

    # Check current directory
    project_path = Path(".")

    # Run compliance check
    compliance_system = Python311ComplianceSystem(str(project_path))
    results = await compliance_system.run_compliance_check()

    print(f"\n📊 COMPLIANCE RESULTS:")
    print(f"   Score: {results['compliance_score']:.1f}/100")

    if results["compliance_score"] < 85:
        print("⚠️  Compliance below optimal level - running modernization...")
        await modernize_codebase_to_python311()
    else:
        print("✅ Compliance level acceptable")

    print("\n🎉 Python 3.11 compliance check and modernization complete!")
    return results


if __name__ == "__main__":
    asyncio.run(main())
