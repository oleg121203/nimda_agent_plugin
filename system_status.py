#!/usr/bin/env python3
"""
NIMDA System Status Report Generator
Generates comprehensive status reports for all NIMDA components
"""

import json
import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_system_check() -> Dict[str, Any]:
    """Run comprehensive system check"""

    report = {
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "status": "unknown",
        "components": {},
        "features": {},
        "recommendations": [],
        "summary": {},
    }

    print("🔍 NIMDA System Status Report")
    print("=" * 50)

    # Check core files
    core_files = [
        "translate_all.py",
        "offline_queue.py",
        "backup_rotation.py",
        "nimda_cli.py",
        "performance_monitor.py",
        "health_dashboard.py",
    ]

    print("\n📁 Core Files:")
    for file in core_files:
        exists = Path(file).exists()
        status = "✅" if exists else "❌"
        print(f"   {status} {file}")
        report["components"][file] = {
            "exists": exists,
            "status": "healthy" if exists else "missing",
        }

    # Check Python syntax
    print("\n🐍 Python Syntax Check:")
    syntax_ok = True
    for file in core_files:
        if Path(file).exists():
            try:
                result = subprocess.run(
                    ["python", "-m", "py_compile", file],
                    capture_output=True,
                    timeout=10,
                )
                ok = result.returncode == 0
                status = "✅" if ok else "❌"
                print(f"   {status} {file}")
                if not ok:
                    syntax_ok = False
                    print(f"      Error: {result.stderr.decode()}")
            except Exception as e:
                print(f"   ❌ {file} - Error: {e}")
                syntax_ok = False

    report["features"]["syntax_check"] = {
        "status": "healthy" if syntax_ok else "critical",
        "all_files_valid": syntax_ok,
    }

    # Test imports
    print("\n📦 Import Test:")
    import_results = {}
    modules_to_test = [
        ("offline_queue", "OfflineQueue"),
        ("backup_rotation", "BackupManager"),
        ("performance_monitor", "PerformanceMonitor"),
        ("health_dashboard", "run_health_check"),
    ]

    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name)
            getattr(module, class_name)
            print(f"   ✅ {module_name}.{class_name}")
            import_results[module_name] = "healthy"
        except ImportError as e:
            print(f"   ❌ {module_name} - Import Error: {e}")
            import_results[module_name] = "critical"
        except AttributeError as e:
            print(f"   ⚠️  {module_name} - Attribute Error: {e}")
            import_results[module_name] = "warning"
        except Exception as e:
            print(f"   ❌ {module_name} - Error: {e}")
            import_results[module_name] = "critical"

    report["features"]["imports"] = import_results

    # Test CLI
    print("\n🖥️  CLI Test:")
    try:
        result = subprocess.run(
            ["python", "nimda_cli.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        cli_ok = result.returncode == 0 and "NIMDA CLI" in result.stdout
        status = "✅" if cli_ok else "❌"
        print(f"   {status} nimda_cli.py --help")
        report["features"]["cli"] = {
            "status": "healthy" if cli_ok else "critical",
            "help_command_works": cli_ok,
        }
    except Exception as e:
        print(f"   ❌ CLI test failed: {e}")
        report["features"]["cli"] = {"status": "critical", "error": str(e)}

    # Test health dashboard
    print("\n🩺 Health Dashboard Test:")
    try:
        from health_dashboard import run_health_check

        health_results = run_health_check()
        overall_status = health_results.get("overall_status", "unknown")
        summary = health_results.get("summary", {})

        print(f"   📊 Overall Status: {overall_status.upper()}")
        print(f"   ✅ Healthy: {summary.get('healthy', 0)}")
        print(f"   ⚠️  Warning: {summary.get('warning', 0)}")
        print(f"   ❌ Critical: {summary.get('critical', 0)}")

        report["features"]["health_dashboard"] = {
            "status": overall_status,
            "component_summary": summary,
            "details": health_results,
        }
    except Exception as e:
        print(f"   ❌ Health dashboard test failed: {e}")
        report["features"]["health_dashboard"] = {"status": "critical", "error": str(e)}

    # Test offline queue
    print("\n🔄 Offline Queue Test:")
    try:
        from offline_queue import OfflineQueue

        queue = OfflineQueue()
        stats = queue.get_queue_stats()
        print(f"   ✅ Queue initialized")
        print(f"   📊 Total operations: {stats.get('total_operations', 0)}")
        report["features"]["offline_queue"] = {"status": "healthy", "stats": stats}
    except Exception as e:
        print(f"   ❌ Offline queue test failed: {e}")
        report["features"]["offline_queue"] = {"status": "critical", "error": str(e)}

    # Translation status
    print("\n🌐 Translation Status:")
    translation_backup_dir = Path(".translation_backups")
    if translation_backup_dir.exists():
        backup_files = list(translation_backup_dir.glob("*.bak"))
        print(f"   ✅ Translation completed")
        print(f"   📁 Backup files: {len(backup_files)}")
        report["features"]["translation"] = {
            "status": "healthy",
            "backup_files": len(backup_files),
            "completed": True,
        }
    else:
        print(f"   ⚠️  No translation backups found")
        report["features"]["translation"] = {"status": "warning", "completed": False}

    # Configuration files
    print("\n⚙️  Configuration:")
    config_files = [".env.example", ".bulletproof_enhanced_config", "requirements.txt"]

    for config_file in config_files:
        exists = Path(config_file).exists()
        status = "✅" if exists else "❌"
        print(f"   {status} {config_file}")
        report["components"][config_file] = {
            "exists": exists,
            "status": "healthy" if exists else "missing",
        }

    # Generate overall status
    critical_count = len(
        [f for f in report["features"].values() if f.get("status") == "critical"]
    )
    warning_count = len(
        [f for f in report["features"].values() if f.get("status") == "warning"]
    )

    if critical_count > 0:
        overall_status = "critical"
    elif warning_count > 0:
        overall_status = "warning"
    else:
        overall_status = "healthy"

    report["status"] = overall_status
    report["summary"] = {
        "critical_issues": critical_count,
        "warnings": warning_count,
        "healthy_components": len(
            [f for f in report["features"].values() if f.get("status") == "healthy"]
        ),
    }

    # Generate recommendations
    recommendations = []

    if critical_count > 0:
        recommendations.append("❌ Fix critical issues before deploying to production")

    if warning_count > 0:
        recommendations.append("⚠️  Address warnings to improve system reliability")

    if not report["features"].get("translation", {}).get("completed"):
        recommendations.append(
            "🌐 Run translation script to complete English conversion"
        )

    if report["features"].get("health_dashboard", {}).get("status") == "warning":
        recommendations.append("🩺 Review health dashboard warnings")

    if overall_status == "healthy":
        recommendations.append("✅ System is ready for production use")
        recommendations.append("📚 Consider adding comprehensive documentation")
        recommendations.append("🧪 Implement full test coverage")

    report["recommendations"] = recommendations

    # Print summary
    print(f"\n📊 System Summary:")
    print(f"   Overall Status: {overall_status.upper()}")
    print(f"   Critical Issues: {critical_count}")
    print(f"   Warnings: {warning_count}")
    print(f"   Healthy Components: {report['summary']['healthy_components']}")

    print(f"\n💡 Recommendations:")
    for rec in recommendations:
        print(f"   {rec}")

    return report


def save_report(report: Dict[str, Any]) -> Path:
    """Save report to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = Path(f"nimda_system_report_{timestamp}.json")

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return report_file


def main():
    """Main function"""
    report = run_system_check()
    report_file = save_report(report)

    print(f"\n💾 Report saved: {report_file}")
    print(f"\n🎉 NIMDA System Check Complete!")

    return report["status"] == "healthy"


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
