#!/usr/bin/env python3
"""
NIMDA Health Dashboard and System Monitor
Real-time monitoring of all NIMDA components
"""

import http.server
import json
import logging
import socketserver
import subprocess
import time
import webbrowser
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class ComponentHealth:
    """Health status of a NIMDA component"""

    name: str
    status: str  # "healthy", "warning", "critical", "unknown"
    last_check: str
    response_time_ms: float
    error_message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class SystemMetrics:
    """Overall system metrics"""

    timestamp: str
    cpu_usage_percent: float
    memory_usage_mb: float
    disk_usage_percent: float
    network_latency_ms: float
    active_operations: int
    queue_size: int
    backup_count: int
    sync_success_rate: float
    uptime_hours: float


class HealthChecker:
    """Checks health of NIMDA components"""

    def __init__(self):
        self.start_time = datetime.now()

    def check_git_health(self) -> ComponentHealth:
        """Check Git repository health"""
        start_time = time.time()
        try:
            # Check if we're in a git repo
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            response_time = (time.time() - start_time) * 1000

            if result.returncode == 0:
                dirty_files = (
                    len(result.stdout.strip().split("\n"))
                    if result.stdout.strip()
                    else 0
                )
                return ComponentHealth(
                    name="Git Repository",
                    status="healthy" if dirty_files == 0 else "warning",
                    last_check=datetime.now().isoformat(),
                    response_time_ms=response_time,
                    details={"dirty_files": dirty_files, "output": result.stdout[:200]},
                )
            else:
                return ComponentHealth(
                    name="Git Repository",
                    status="critical",
                    last_check=datetime.now().isoformat(),
                    response_time_ms=response_time,
                    error_message=result.stderr,
                )

        except Exception as e:
            return ComponentHealth(
                name="Git Repository",
                status="critical",
                last_check=datetime.now().isoformat(),
                response_time_ms=(time.time() - start_time) * 1000,
                error_message=str(e),
            )

    def check_queue_health(self) -> ComponentHealth:
        """Check offline queue health"""
        start_time = time.time()
        try:
            from offline_queue import OfflineQueue

            queue = OfflineQueue()
            status = queue.get_queue_stats()

            response_time = (time.time() - start_time) * 1000

            # Determine health based on queue status
            total_ops = status.get("total_operations", 0)
            failed_ops = status.get("failed_operations", 0)

            if total_ops == 0:
                health_status = "healthy"
            elif failed_ops > total_ops * 0.5:
                health_status = "critical"
            elif failed_ops > 0:
                health_status = "warning"
            else:
                health_status = "healthy"

            return ComponentHealth(
                name="Offline Queue",
                status=health_status,
                last_check=datetime.now().isoformat(),
                response_time_ms=response_time,
                details=status,
            )

        except Exception as e:
            return ComponentHealth(
                name="Offline Queue",
                status="critical",
                last_check=datetime.now().isoformat(),
                response_time_ms=(time.time() - start_time) * 1000,
                error_message=str(e),
            )

    def check_backup_health(self) -> ComponentHealth:
        """Check backup system health"""
        start_time = time.time()
        try:
            from backup_rotation import BackupManager

            backup_manager = BackupManager()
            backups = backup_manager.list_backups()

            response_time = (time.time() - start_time) * 1000

            # Check if we have recent backups
            if not backups:
                health_status = "warning"
                error_msg = "No backups found"
            else:
                # Get the most recent backup timestamp
                latest_time = None
                for backup in backups:
                    backup_time = datetime.fromisoformat(
                        backup.timestamp.replace("Z", "+00:00")
                    )
                    if latest_time is None or backup_time > latest_time:
                        latest_time = backup_time

                if latest_time:
                    age_hours = (
                        datetime.now() - latest_time.replace(tzinfo=None)
                    ).total_seconds() / 3600

                    if age_hours > 24:
                        health_status = "warning"
                        error_msg = f"Latest backup is {age_hours:.1f} hours old"
                    else:
                        health_status = "healthy"
                        error_msg = None
                else:
                    health_status = "warning"
                    error_msg = "Cannot determine backup age"

            return ComponentHealth(
                name="Backup System",
                status=health_status,
                last_check=datetime.now().isoformat(),
                response_time_ms=response_time,
                error_message=error_msg,
                details={"backup_count": len(backups)},
            )

        except Exception as e:
            return ComponentHealth(
                name="Backup System",
                status="critical",
                last_check=datetime.now().isoformat(),
                response_time_ms=(time.time() - start_time) * 1000,
                error_message=str(e),
            )

    def check_performance_health(self) -> ComponentHealth:
        """Check performance monitor health"""
        start_time = time.time()
        try:
            from performance_monitor import PerformanceMonitor

            monitor = PerformanceMonitor()
            metrics = monitor.get_current_metrics()

            response_time = (time.time() - start_time) * 1000

            # Analyze metrics for health
            memory_usage = metrics.get("memory_usage_mb", 0)

            if memory_usage > 1000:  # > 1GB
                health_status = "warning"
                error_msg = f"High memory usage: {memory_usage:.1f}MB"
            else:
                health_status = "healthy"
                error_msg = None

            return ComponentHealth(
                name="Performance Monitor",
                status=health_status,
                last_check=datetime.now().isoformat(),
                response_time_ms=response_time,
                error_message=error_msg,
                details=metrics,
            )

        except Exception as e:
            return ComponentHealth(
                name="Performance Monitor",
                status="critical",
                last_check=datetime.now().isoformat(),
                response_time_ms=(time.time() - start_time) * 1000,
                error_message=str(e),
            )

    def check_network_health(self) -> ComponentHealth:
        """Check network connectivity"""
        start_time = time.time()
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "3", "8.8.8.8"],
                capture_output=True,
                timeout=5,
            )

            response_time = (time.time() - start_time) * 1000

            if result.returncode == 0:
                return ComponentHealth(
                    name="Network Connectivity",
                    status="healthy",
                    last_check=datetime.now().isoformat(),
                    response_time_ms=response_time,
                )
            else:
                return ComponentHealth(
                    name="Network Connectivity",
                    status="critical",
                    last_check=datetime.now().isoformat(),
                    response_time_ms=response_time,
                    error_message="Cannot reach external network",
                )

        except Exception as e:
            return ComponentHealth(
                name="Network Connectivity",
                status="critical",
                last_check=datetime.now().isoformat(),
                response_time_ms=(time.time() - start_time) * 1000,
                error_message=str(e),
            )


class HealthDashboard:
    """Web-based health dashboard for NIMDA"""

    def __init__(self, port: int = 8080):
        self.port = port
        self.checker = HealthChecker()
        self.dashboard_dir = Path(".nimda_dashboard")
        self.dashboard_dir.mkdir(exist_ok=True)

    def generate_html_dashboard(self) -> str:
        """Generate HTML dashboard"""
        # Get health status for all components
        components = [
            self.checker.check_git_health(),
            self.checker.check_queue_health(),
            self.checker.check_backup_health(),
            self.checker.check_performance_health(),
            self.checker.check_network_health(),
        ]

        # Count statuses
        healthy = len([c for c in components if c.status == "healthy"])
        warning = len([c for c in components if c.status == "warning"])
        critical = len([c for c in components if c.status == "critical"])

        # Generate HTML
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NIMDA Health Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0; }}
        .summary {{ display: flex; gap: 20px; margin-bottom: 30px; }}
        .summary-card {{ background: white; padding: 20px; border-radius: 8px; flex: 1; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .summary-card.healthy {{ border-left: 4px solid #27ae60; }}
        .summary-card.warning {{ border-left: 4px solid #f39c12; }}
        .summary-card.critical {{ border-left: 4px solid #e74c3c; }}
        .component {{ background: white; margin-bottom: 15px; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .component-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        .status {{ padding: 4px 12px; border-radius: 4px; color: white; font-size: 12px; font-weight: bold; }}
        .status.healthy {{ background: #27ae60; }}
        .status.warning {{ background: #f39c12; }}
        .status.critical {{ background: #e74c3c; }}
        .details {{ color: #666; font-size: 14px; }}
        .refresh {{ position: fixed; bottom: 20px; right: 20px; background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 20px; cursor: pointer; }}
        .timestamp {{ color: #7f8c8d; font-size: 12px; }}
    </style>
    <meta http-equiv="refresh" content="30">
</head>
<body>
    <div class="header">
        <h1>🩺 NIMDA Health Dashboard</h1>
        <div class="timestamp">Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
    </div>
    
    <div class="summary">
        <div class="summary-card healthy">
            <h2>{healthy}</h2>
            <p>Healthy Components</p>
        </div>
        <div class="summary-card warning">
            <h2>{warning}</h2>
            <p>Warning Components</p>
        </div>
        <div class="summary-card critical">
            <h2>{critical}</h2>
            <p>Critical Components</p>
        </div>
    </div>
    
    <div class="components">
"""

        for component in components:
            details_html = ""
            if component.details:
                details_html = f"<div class='details'>Details: {json.dumps(component.details, indent=2)}</div>"

            error_html = ""
            if component.error_message:
                error_html = f"<div class='details' style='color: #e74c3c;'>Error: {component.error_message}</div>"

            html += f"""
        <div class="component">
            <div class="component-header">
                <h3>{component.name}</h3>
                <span class="status {component.status}">{component.status.upper()}</span>
            </div>
            <div class="details">Response time: {component.response_time_ms:.1f}ms</div>
            <div class="details">Last check: {component.last_check}</div>
            {error_html}
            {details_html}
        </div>
"""

        html += """
    </div>
    
    <button class="refresh" onclick="location.reload()">🔄 Refresh</button>
</body>
</html>
"""
        return html

    def save_dashboard(self):
        """Save dashboard HTML to file"""
        html = self.generate_html_dashboard()
        dashboard_file = self.dashboard_dir / "index.html"

        with open(dashboard_file, "w", encoding="utf-8") as f:
            f.write(html)

        return dashboard_file

    def serve_dashboard(self):
        """Serve dashboard via HTTP server"""
        dashboard_file = self.save_dashboard()

        class DashboardHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(dashboard_file.parent), **kwargs)

        try:
            with socketserver.TCPServer(("", self.port), DashboardHandler) as httpd:
                print(
                    f"🌐 NIMDA Health Dashboard running at http://localhost:{self.port}"
                )
                print(f"📊 Dashboard file: {dashboard_file}")
                print("Press Ctrl+C to stop")

                # Auto-open browser
                webbrowser.open(f"http://localhost:{self.port}")

                httpd.serve_forever()

        except KeyboardInterrupt:
            print("\n👋 Dashboard stopped")
        except Exception as e:
            print(f"❌ Error starting dashboard: {e}")


def run_health_check() -> Dict[str, Any]:
    """Run complete health check and return results"""
    checker = HealthChecker()

    components = [
        checker.check_git_health(),
        checker.check_queue_health(),
        checker.check_backup_health(),
        checker.check_performance_health(),
        checker.check_network_health(),
    ]

    # Calculate overall health
    statuses = [c.status for c in components]
    if "critical" in statuses:
        overall_status = "critical"
    elif "warning" in statuses:
        overall_status = "warning"
    else:
        overall_status = "healthy"

    return {
        "overall_status": overall_status,
        "components": [asdict(c) for c in components],
        "summary": {
            "healthy": len([s for s in statuses if s == "healthy"]),
            "warning": len([s for s in statuses if s == "warning"]),
            "critical": len([s for s in statuses if s == "critical"]),
            "total": len(components),
        },
        "timestamp": datetime.now().isoformat(),
    }


def main():
    """Main health dashboard function"""
    import argparse

    parser = argparse.ArgumentParser(description="NIMDA Health Dashboard")
    parser.add_argument("--serve", action="store_true", help="Start web dashboard")
    parser.add_argument("--port", type=int, default=8080, help="Dashboard port")
    parser.add_argument("--check", action="store_true", help="Run health check only")

    args = parser.parse_args()

    if args.check:
        print("🩺 Running NIMDA health check...")
        results = run_health_check()

        print(f"\n📊 Overall Status: {results['overall_status'].upper()}")
        print(f"✅ Healthy: {results['summary']['healthy']}")
        print(f"⚠️  Warning: {results['summary']['warning']}")
        print(f"❌ Critical: {results['summary']['critical']}")

        print("\n📋 Component Details:")
        for component in results["components"]:
            status_icon = {"healthy": "✅", "warning": "⚠️", "critical": "❌"}.get(
                component["status"], "❓"
            )

            print(f"  {status_icon} {component['name']}: {component['status']}")
            if component["error_message"]:
                print(f"     Error: {component['error_message']}")

    elif args.serve:
        dashboard = HealthDashboard(port=args.port)
        dashboard.serve_dashboard()

    else:
        print("🩺 NIMDA Health Dashboard")
        print("Use --check for health check or --serve for web dashboard")


if __name__ == "__main__":
    main()
