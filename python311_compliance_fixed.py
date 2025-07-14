#!/usr/bin/env python3.11
"""
Python 3.11 Compliance and English Localization System
Ensures all components use Python 3.11+ features and English development standards
"""

import ast
import asyncio
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

# Check Python version compatibility
if sys.version_info < (3, 8):
    print("❌ ERROR: Python 3.8+ is minimum requirement")
    print(f"Current version: {sys.version}")
    print("Please upgrade to Python 3.8 or higher")
    sys.exit(1)

if sys.version_info < (3, 11):
    print(
        f"⚠️  NOTICE: Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected"
    )
    print("🎯 Target version: Python 3.11+ for optimal performance")
    print("📋 Current version will work but with limited features")
else:
    print(
        f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Optimal version detected"
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
        """Run complete compliance check with flexibility for different Python versions"""
        print("🔍 PYTHON 3.11 READINESS & ENGLISH LOCALIZATION CHECK")
        print("=" * 60)

        results = {
            "python_version_check": await self._check_python_version(),
            "code_analysis": await self._analyze_python_files(),
            "english_compliance": await self._check_english_compliance(),
            "feature_opportunities": await self._identify_python311_opportunities(),
            "readiness_assessment": await self._assess_python311_readiness(),
            "compliance_score": 0,
            "readiness_score": 0,
            "recommendations": [],
        }

        # Calculate compliance score
        results["compliance_score"] = await self._calculate_compliance_score(results)
        results["readiness_score"] = await self._calculate_readiness_score(results)
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
                tree = ast.parse(content)
                await self._analyze_ast_for_features(tree, file_path, analysis)
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
        project_path = self.project_path

        class FeatureVisitor(ast.NodeVisitor):
            def __init__(self):
                self.has_type_hints = False
                self.has_match_statement = False
                self.functions_without_hints = []

            def visit_FunctionDef(self, node):
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
        ]

        return opportunities

    async def _assess_python311_readiness(self) -> Dict[str, Any]:
        """Assess readiness for Python 3.11 upgrade"""
        print("🔮 Assessing Python 3.11 upgrade readiness...")

        current_version = sys.version_info
        readiness = {
            "current_version": f"{current_version.major}.{current_version.minor}.{current_version.micro}",
            "target_version": "3.11.0",
            "is_ready_for_upgrade": current_version >= (3, 9),
            "compatibility_issues": [],
            "preparation_steps": [],
            "benefits_after_upgrade": [],
        }

        if current_version < (3, 9):
            readiness["compatibility_issues"].extend(
                [
                    "Assignment expressions (:=) may not be available",
                    "Dict union operators (|, |=) not available",
                ]
            )

        readiness["preparation_steps"] = [
            "Use type hints consistently for better 3.11 compatibility",
            "Avoid deprecated typing imports (Dict, List) - use built-ins",
            "Prepare code for match/case statements",
            "Use f-strings consistently instead of .format()",
        ]

        readiness["benefits_after_upgrade"] = [
            "Up to 25% faster execution speed",
            "Enhanced error messages with precise locations",
            "Pattern matching for cleaner conditional logic",
        ]

        return readiness

    async def _calculate_compliance_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall compliance score"""
        score = 0.0

        if results["python_version_check"]["is_compliant"]:
            score += 40

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

        english_score = (
            results["english_compliance"]["compliance_percentage"] / 100 * 30
        )
        score += english_score

        return min(max(score, 0), 100)

    async def _calculate_readiness_score(self, results: Dict[str, Any]) -> float:
        """Calculate Python 3.11 readiness score"""
        score = 0.0

        version_check = results["python_version_check"]
        if version_check["is_compliant"]:
            score += 40
        elif sys.version_info >= (3, 9):
            score += 30
        elif sys.version_info >= (3, 8):
            score += 20

        code_analysis = results["code_analysis"]
        if code_analysis["files_analyzed"] > 0:
            type_hint_penalty = len(code_analysis["missing_type_hints"]) * 2
            score += max(20 - type_hint_penalty, 0)

            deprecated_penalty = len(code_analysis["deprecated_features"]) * 1.5
            score += max(15 - deprecated_penalty, 0)

        english_score = (
            results["english_compliance"]["compliance_percentage"] / 100 * 25
        )
        score += english_score

        return min(max(score, 0), 100)

    async def _generate_compliance_report(self, results: Dict[str, Any]):
        """Generate comprehensive compliance and readiness report"""
        report_path = self.project_path / "PYTHON311_READINESS_REPORT.md"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        report = f"""# Python 3.11 Readiness & Compliance Report

**Generated**: {timestamp}
**Compliance Score**: {results["compliance_score"]:.1f}/100
**Readiness Score**: {results["readiness_score"]:.1f}/100

## Current Python Environment
- **Version**: {results["python_version_check"]["current_version"]}
- **Target Version**: 3.11+
- **Status**: {"✅ Compliant" if results["python_version_check"]["is_compliant"] else "⚠️ Preparing for upgrade"}

## Code Analysis
- **Files Analyzed**: {results["code_analysis"]["files_analyzed"]}
- **Syntax Errors**: {len(results["code_analysis"]["syntax_errors"])}
- **Deprecated Features**: {len(results["code_analysis"]["deprecated_features"])}

## English Compliance
- **Compliance Percentage**: {results["english_compliance"]["compliance_percentage"]:.1f}%

## Enhancement Opportunities
{len(results["feature_opportunities"])} Python 3.11+ features available for implementation

## Recommendations
1. Update to Python 3.11+ for optimal performance
2. Modernize type hints and remove deprecated imports
3. Convert all comments and documentation to English
"""

        report_path.write_text(report, encoding="utf-8")
        print(f"📋 Report saved to: {report_path}")


async def main():
    """Main function for compliance checking"""
    print("🚀 PYTHON 3.11 COMPLIANCE AND MODERNIZATION SYSTEM")
    print("=" * 60)

    project_path = Path(".")
    compliance_system = Python311ComplianceSystem(str(project_path))
    results = await compliance_system.run_compliance_check()

    print("\n📊 READINESS & COMPLIANCE RESULTS:")
    print(f"   Compliance Score: {results['compliance_score']:.1f}/100")
    print(f"   Readiness Score: {results['readiness_score']:.1f}/100")

    print("\n🎉 Python 3.11 compliance check complete!")
    return results


if __name__ == "__main__":
    asyncio.run(main())
