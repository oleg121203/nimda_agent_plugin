#!/usr/bin/env python3
"""
Performance Monitor for NIMDA Agent
Monitors and optimizes system performance (simplified version)
"""

import functools
import gc
import json
import logging
import os
import resource
import shutil
import threading
import time
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Single performance metric"""

    name: str
    value: float
    unit: str
    timestamp: str
    category: str
    source: str


@dataclass
class OperationProfile:
    """Profile data for an operation"""

    operation_name: str
    duration: float
    memory_used: int
    timestamp: str
    success: bool
    error: str = ""


class PerformanceProfiler:
    """Context manager for profiling operations"""

    def __init__(self, operation_name: str, monitor: "PerformanceMonitor"):
        self.operation_name = operation_name
        self.monitor = monitor
        self.start_time = None
        self.start_memory = None

    def __enter__(self):
        self.start_time = time.time()
        # Use resource module for memory tracking
        self.start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - (self.start_time or 0)
        current_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        memory_used = current_memory - (self.start_memory or 0)

        profile = OperationProfile(
            operation_name=self.operation_name,
            duration=duration,
            memory_used=memory_used,
            timestamp=datetime.now().isoformat(),
            success=exc_type is None,
            error=str(exc_val) if exc_val else "",
        )

        self.monitor.record_operation_profile(profile)


def performance_profile(operation_name: str = ""):
    """Decorator for profiling function performance"""

    def decorator(func: Callable) -> Callable:
        op_name = operation_name or f"{func.__module__}.{func.__name__}"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get monitor instance from global or create one
            monitor = getattr(wrapper, "_monitor", None)
            if not monitor:
                monitor = PerformanceMonitor()
                setattr(wrapper, "_monitor", monitor)

            with PerformanceProfiler(op_name, monitor):
                return func(*args, **kwargs)

        return wrapper

    return decorator


class SystemResourceMonitor:
    """Monitor system resources using basic system tools"""

    def __init__(self):
        pass

    def get_current_metrics(self) -> Dict[str, float]:
        """Get current system metrics using available tools"""
        try:
            metrics = {}

            # Memory metrics using resource module
            memory_info = resource.getrusage(resource.RUSAGE_SELF)
            metrics["process_memory_kb"] = float(memory_info.ru_maxrss)

            # Disk metrics
            try:
                disk_usage = shutil.disk_usage("/")
                metrics["disk_total"] = float(disk_usage.total)
                metrics["disk_free"] = float(disk_usage.free)
                metrics["disk_percent"] = float(
                    (disk_usage.total - disk_usage.free) / disk_usage.total * 100
                )
            except Exception:
                metrics["disk_total"] = 0.0
                metrics["disk_free"] = 0.0
                metrics["disk_percent"] = 0.0

            # Load average (Unix systems)
            try:
                load_avg = os.getloadavg()
                metrics["load_1min"] = float(load_avg[0])
                metrics["load_5min"] = float(load_avg[1])
                metrics["load_15min"] = float(load_avg[2])
            except Exception:
                metrics["load_1min"] = 0.0
                metrics["load_5min"] = 0.0
                metrics["load_15min"] = 0.0

            return metrics

        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}


class PerformanceAnalyzer:
    """Analyze performance data and provide insights"""

    def __init__(self):
        self.thresholds = {
            "disk_full": 90.0,
            "operation_slow": 5.0,  # seconds
            "memory_growth_kb": 100000,  # 100MB in KB
        }

    def analyze_operation_profiles(
        self, profiles: List[OperationProfile]
    ) -> Dict[str, Any]:
        """Analyze operation performance profiles"""
        if not profiles:
            return {"issues": [], "recommendations": []}

        analysis = {
            "total_operations": len(profiles),
            "failed_operations": sum(1 for p in profiles if not p.success),
            "average_duration": sum(p.duration for p in profiles) / len(profiles),
            "total_memory_used": sum(p.memory_used for p in profiles),
            "issues": [],
            "recommendations": [],
        }

        # Find slow operations
        slow_ops = [
            p for p in profiles if p.duration > self.thresholds["operation_slow"]
        ]
        if slow_ops:
            analysis["issues"].append(f"Found {len(slow_ops)} slow operations")
            analysis["recommendations"].append(
                "Consider optimizing slow operations or adding caching"
            )

        # Find memory-intensive operations
        memory_heavy = [
            p
            for p in profiles
            if abs(p.memory_used) > self.thresholds["memory_growth_kb"]
        ]
        if memory_heavy:
            analysis["issues"].append(
                f"Found {len(memory_heavy)} memory-intensive operations"
            )
            analysis["recommendations"].append(
                "Review memory usage in heavy operations"
            )

        # Find failed operations
        failed_ops = [p for p in profiles if not p.success]
        if failed_ops:
            analysis["issues"].append(f"Found {len(failed_ops)} failed operations")
            analysis["recommendations"].append(
                "Review error handling and retry mechanisms"
            )

        return analysis

    def analyze_system_metrics(
        self, metrics_history: List[Dict[str, float]]
    ) -> Dict[str, Any]:
        """Analyze system metrics for issues"""
        if not metrics_history:
            return {"issues": [], "recommendations": [], "current_status": "unknown"}

        latest = metrics_history[-1] if metrics_history else {}
        analysis = {"issues": [], "recommendations": [], "current_status": "healthy"}

        # Disk analysis
        disk_percent = latest.get("disk_percent", 0)
        if disk_percent > self.thresholds["disk_full"]:
            analysis["issues"].append(f"Low disk space: {disk_percent:.1f}% used")
            analysis["recommendations"].append(
                "Clean up old files, logs, or backups to free disk space"
            )
            analysis["current_status"] = "critical"

        # Load average analysis (Unix systems)
        load_1min = latest.get("load_1min", 0)
        if load_1min > 2.0:  # Simple threshold
            analysis["issues"].append(f"High system load: {load_1min:.2f}")
            analysis["recommendations"].append(
                "Consider reducing concurrent operations"
            )
            analysis["current_status"] = "warning"

        return analysis


class PerformanceOptimizer:
    """Provide performance optimization suggestions"""

    def __init__(self):
        self.optimizations = {"cache_enabled": False, "memory_cleanup": False}

    def suggest_optimizations(self, analysis: Dict[str, Any]) -> List[str]:
        """Suggest optimizations based on analysis"""
        suggestions = []

        # Suggest memory management improvements
        if "memory" in str(analysis.get("issues", [])):
            suggestions.append("Implement better memory management")
            suggestions.append(
                "  Implementation: Use context managers, del unused objects, gc.collect()"
            )

        # Suggest caching for frequent operations
        if analysis.get("total_operations", 0) > 50:
            suggestions.append("Consider caching for frequently called operations")
            suggestions.append(
                "  Implementation: Use functools.lru_cache or implement custom cache"
            )

        # Suggest optimization for slow operations
        if "slow operations" in str(analysis.get("issues", [])):
            suggestions.append("Optimize slow operations")
            suggestions.append(
                "  Implementation: Profile code, use better algorithms, async processing"
            )

        return suggestions

    def apply_optimization(self, optimization_type: str) -> bool:
        """Apply specific optimization"""
        try:
            if optimization_type == "memory_cleanup":
                # Force garbage collection
                collected = gc.collect()
                logger.info(f"Garbage collection freed {collected} objects")
                self.optimizations["memory_cleanup"] = True
                return True

            elif optimization_type == "cache_enable":
                # This would be implemented per-component
                self.optimizations["cache_enabled"] = True
                logger.info("Caching enabled")
                return True

            else:
                logger.warning(f"Unknown optimization type: {optimization_type}")
                return False

        except Exception as e:
            logger.error(f"Error applying optimization {optimization_type}: {e}")
            return False


class PerformanceMonitor:
    """Main performance monitoring class"""

    def __init__(self, metrics_file: str = ".nimda_performance_metrics.json"):
        self.metrics_file = Path(metrics_file)
        self.system_monitor = SystemResourceMonitor()
        self.analyzer = PerformanceAnalyzer()
        self.optimizer = PerformanceOptimizer()

        # In-memory storage
        self.metrics_history = deque(maxlen=1000)  # Keep last 1000 metrics
        self.operation_profiles = deque(maxlen=500)  # Keep last 500 operation profiles

        # Monitoring control
        self.monitoring = False
        self.monitor_thread = None
        self.collection_interval = 30  # seconds

        # Load existing metrics
        self.load_metrics()

    def start_monitoring(self, interval: int = 30):
        """Start background performance monitoring"""
        if self.monitoring:
            logger.info("Performance monitoring already running")
            return

        self.collection_interval = interval
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self.monitor_thread.start()
        logger.info(f"Started performance monitoring (interval: {interval}s)")

    def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Stopped performance monitoring")

    def _monitoring_loop(self):
        """Background monitoring loop"""
        while self.monitoring:
            try:
                # Collect system metrics
                metrics = self.system_monitor.get_current_metrics()
                if metrics:
                    # Add timestamp to metrics
                    timestamped_metrics = {
                        **metrics,
                        "timestamp": datetime.now().isoformat(),
                    }
                    self.metrics_history.append(timestamped_metrics)

                # Save metrics periodically
                if len(self.metrics_history) % 10 == 0:
                    self.save_metrics()

                time.sleep(self.collection_interval)

            except Exception as e:
                logger.error(f"Error in performance monitoring loop: {e}")
                time.sleep(self.collection_interval)

    def record_operation_profile(self, profile: OperationProfile):
        """Record operation performance profile"""
        self.operation_profiles.append(profile)

        # Log slow operations
        if profile.duration > 5.0:
            logger.warning(
                f"Slow operation detected: {profile.operation_name} took {profile.duration:.2f}s"
            )

        # Log failed operations
        if not profile.success:
            logger.error(
                f"Operation failed: {profile.operation_name} - {profile.error}"
            )

    def profile_operation(self, operation_name: str = ""):
        """Get profiler context manager for operation"""
        return PerformanceProfiler(operation_name, self)

    def get_current_status(self) -> Dict[str, Any]:
        """Get current performance status"""
        latest_metrics = (
            list(self.metrics_history)[-1:] if self.metrics_history else [{}]
        )
        recent_profiles = (
            list(self.operation_profiles)[-20:] if self.operation_profiles else []
        )

        # Analyze current state
        system_analysis = self.analyzer.analyze_system_metrics(latest_metrics)
        operation_analysis = self.analyzer.analyze_operation_profiles(recent_profiles)

        # Get optimization suggestions
        suggestions = self.optimizer.suggest_optimizations(
            {**system_analysis, **operation_analysis}
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "system_metrics": latest_metrics[0] if latest_metrics else {},
            "system_analysis": system_analysis,
            "operation_analysis": operation_analysis,
            "optimization_suggestions": suggestions,
            "monitoring_active": self.monitoring,
        }

    def get_performance_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate performance report for specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours)

        # Filter metrics by time
        recent_metrics = []
        for m in self.metrics_history:
            try:
                if (
                    datetime.fromisoformat(m.get("timestamp", "1970-01-01"))
                    > cutoff_time
                ):
                    recent_metrics.append(m)
            except ValueError:
                continue

        # Filter operation profiles by time
        recent_profiles = []
        for p in self.operation_profiles:
            try:
                if datetime.fromisoformat(p.timestamp) > cutoff_time:
                    recent_profiles.append(p)
            except ValueError:
                continue

        # Generate analysis
        system_analysis = self.analyzer.analyze_system_metrics(recent_metrics)
        operation_analysis = self.analyzer.analyze_operation_profiles(recent_profiles)
        suggestions = self.optimizer.suggest_optimizations(
            {**system_analysis, **operation_analysis}
        )

        return {
            "report_period_hours": hours,
            "generated_at": datetime.now().isoformat(),
            "metrics_collected": len(recent_metrics),
            "operations_profiled": len(recent_profiles),
            "system_analysis": system_analysis,
            "operation_analysis": operation_analysis,
            "optimization_suggestions": suggestions,
        }

    def save_metrics(self):
        """Save metrics to file"""
        try:
            data = {
                "last_updated": datetime.now().isoformat(),
                "collection_interval": self.collection_interval,
                "metrics_history": list(self.metrics_history)[-100:],  # Save last 100
                "operation_profiles": [
                    asdict(p) for p in list(self.operation_profiles)[-50:]
                ],  # Save last 50
            }

            with open(self.metrics_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)

        except Exception as e:
            logger.error(f"Error saving metrics: {e}")

    def load_metrics(self):
        """Load metrics from file"""
        try:
            if self.metrics_file.exists():
                with open(self.metrics_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Load metrics history
                metrics_data = data.get("metrics_history", [])
                self.metrics_history.extend(metrics_data)

                # Load operation profiles
                profiles_data = data.get("operation_profiles", [])
                for profile_data in profiles_data:
                    profile = OperationProfile(**profile_data)
                    self.operation_profiles.append(profile)

                logger.info(
                    f"Loaded {len(metrics_data)} metrics and {len(profiles_data)} profiles"
                )

        except Exception as e:
            logger.error(f"Error loading metrics: {e}")

    def optimize_performance(self) -> Dict[str, Any]:
        """Run automatic performance optimization"""
        logger.info("Running automatic performance optimization")

        # Get current status
        status = self.get_current_status()

        # Apply optimizations based on analysis
        optimizations_applied = []

        if "memory" in str(status.get("system_analysis", {}).get("issues", [])):
            if self.optimizer.apply_optimization("memory_cleanup"):
                optimizations_applied.append("memory_cleanup")

        return {
            "timestamp": datetime.now().isoformat(),
            "optimizations_applied": optimizations_applied,
            "status_after_optimization": self.get_current_status(),
        }


def main():
    """Example usage and testing"""
    print("📊 NIMDA Performance Monitor")
    print("=" * 40)

    # Initialize monitor
    monitor = PerformanceMonitor()

    # Start monitoring
    monitor.start_monitoring(interval=5)  # 5 second intervals for demo

    # Simulate some operations
    print("\n🔄 Simulating operations...")

    for i in range(5):
        with monitor.profile_operation(f"test_operation_{i}"):
            # Simulate work
            time.sleep(0.5)

            # Simulate memory usage
            dummy_data = [0] * (100000 * (i + 1))
            time.sleep(0.2)
            del dummy_data

    # Wait a bit for monitoring
    time.sleep(10)

    # Get current status
    print("\n📊 Current Performance Status:")
    status = monitor.get_current_status()

    print(
        f"System Status: {status['system_analysis'].get('current_status', 'unknown')}"
    )
    print(
        f"Operations Analyzed: {status['operation_analysis'].get('total_operations', 0)}"
    )

    if status["system_analysis"].get("issues"):
        print("\n⚠️  Issues Found:")
        for issue in status["system_analysis"]["issues"]:
            print(f"  • {issue}")

    if status["optimization_suggestions"]:
        print("\n💡 Optimization Suggestions:")
        for suggestion in status["optimization_suggestions"][:3]:
            print(f"  • {suggestion}")

    # Generate report
    print("\n📋 Performance Report:")
    report = monitor.get_performance_report(hours=1)
    print(f"Metrics collected: {report['metrics_collected']}")
    print(f"Operations profiled: {report['operations_profiled']}")

    # Test optimization
    print("\n🔧 Running optimization...")
    optimization_result = monitor.optimize_performance()
    print(f"Optimizations applied: {optimization_result['optimizations_applied']}")

    # Stop monitoring
    monitor.stop_monitoring()
    print("\n✅ Performance monitoring test completed")


if __name__ == "__main__":
    main()
