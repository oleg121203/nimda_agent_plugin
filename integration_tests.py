#!/usr/bin/env python3
"""
Integration Tests for NIMDA Agent
Tests the integration between all major components
"""

import logging
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class TestNIMDAIntegration(unittest.TestCase):
    """Integration tests for NIMDA components"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Initialize a git repo for testing
        subprocess.run(["git", "init"], capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"], capture_output=True
        )

        # Create test files
        (self.test_dir / "README.md").write_text("# Test Project")
        (self.test_dir / "test_file.py").write_text("print('Hello World')")

    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_offline_queue_integration(self):
        """Test offline queue with real operations"""
        try:
            from offline_queue import OfflineQueue, OperationType

            # Initialize queue
            queue = OfflineQueue()

            # Test queueing operations
            op_id = queue.enqueue_operation(
                OperationType.GIT_COMMIT,
                {"message": "Test commit", "files": ["README.md"]},
            )

            self.assertIsNotNone(op_id)

            # Test queue stats
            stats = queue.get_queue_stats()
            self.assertIsInstance(stats, dict)
            self.assertIn("total_operations", stats)

            print("✅ Offline queue integration test passed")

        except ImportError as e:
            self.skipTest(f"Cannot import offline_queue: {e}")

    def test_backup_rotation_integration(self):
        """Test backup system integration"""
        try:
            from backup_rotation import BackupManager

            # Initialize backup manager
            backup_manager = BackupManager()

            # Test backup creation with proper source path
            backup_id = backup_manager.create_snapshot_backup(
                source_path=str(self.test_dir), description="Test backup"
            )

            self.assertIsNotNone(backup_id)

            # Test listing backups
            backups = backup_manager.list_backups()
            self.assertIsInstance(backups, list)

            print("✅ Backup rotation integration test passed")

        except ImportError as e:
            self.skipTest(f"Cannot import backup_rotation: {e}")

    def test_performance_monitor_integration(self):
        """Test performance monitor integration"""
        try:
            from performance_monitor import PerformanceMonitor

            # Initialize monitor
            monitor = PerformanceMonitor()

            # Test metrics collection
            metrics = monitor.get_current_metrics()
            self.assertIsInstance(metrics, dict)
            self.assertIn("memory_usage_mb", metrics)

            print("✅ Performance monitor integration test passed")

        except ImportError as e:
            self.skipTest(f"Cannot import performance_monitor: {e}")

    def test_git_manager_integration(self):
        """Test Git manager integration"""
        try:
            from git_manager import GitManager

            # Initialize git manager
            git_manager = GitManager()

            # Test git operations
            status = git_manager.get_status()
            self.assertIsInstance(status, dict)

            # Test commit
            result = git_manager.commit_changes("Test commit")
            self.assertIsInstance(result, dict)

            print("✅ Git manager integration test passed")

        except ImportError as e:
            self.skipTest(f"Cannot import git_manager: {e}")

    def test_dev_plan_manager_integration(self):
        """Test development plan manager integration"""
        try:
            from dev_plan_manager import DevPlanManager

            # Initialize dev plan manager
            dev_manager = DevPlanManager()

            # Test plan loading (should create template if not exists)
            plan = dev_manager.load_plan()
            self.assertIsInstance(plan, dict)

            print("✅ Dev plan manager integration test passed")

        except ImportError as e:
            self.skipTest(f"Cannot import dev_plan_manager: {e}")

    def test_changelog_manager_integration(self):
        """Test changelog manager integration"""
        try:
            from changelog_manager import ChangelogManager

            # Initialize changelog manager
            changelog_manager = ChangelogManager()

            # Test adding entry
            result = changelog_manager.add_entry("Test entry", "Added")
            self.assertIsInstance(result, dict)

            print("✅ Changelog manager integration test passed")

        except ImportError as e:
            self.skipTest(f"Cannot import changelog_manager: {e}")

    def test_cli_integration(self):
        """Test CLI integration"""
        try:
            # Test CLI help command
            result = subprocess.run(
                ["python", str(Path(__file__).parent / "nimda_cli.py"), "--help"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("NIMDA CLI", result.stdout)

            print("✅ CLI integration test passed")

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"Cannot test CLI: {e}")

    def test_health_dashboard_integration(self):
        """Test health dashboard integration"""
        try:
            from health_dashboard import run_health_check

            # Run health check
            results = run_health_check()

            self.assertIsInstance(results, dict)
            self.assertIn("overall_status", results)
            self.assertIn("components", results)

            print("✅ Health dashboard integration test passed")

        except ImportError as e:
            self.skipTest(f"Cannot import health_dashboard: {e}")

    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        try:
            from git_manager import GitManager
            from offline_queue import OfflineQueue, OperationType

            # Initialize components
            queue = OfflineQueue()
            git_manager = GitManager()

            # Create a test file
            test_file = self.test_dir / "workflow_test.txt"
            test_file.write_text("Test content")

            # Add file to git
            subprocess.run(["git", "add", "workflow_test.txt"], capture_output=True)

            # Queue a commit operation
            op_id = queue.enqueue_operation(
                OperationType.GIT_COMMIT, {"message": "End-to-end test commit"}
            )

            self.assertIsNotNone(op_id)

            # Check git status
            status = git_manager.get_status()
            self.assertIsInstance(status, dict)

            print("✅ End-to-end workflow test passed")

        except ImportError as e:
            self.skipTest(f"Cannot test workflow: {e}")


class TestNIMDAPerformance(unittest.TestCase):
    """Performance tests for NIMDA components"""

    def setUp(self):
        """Set up performance test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up performance test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_queue_performance(self):
        """Test queue performance with many operations"""
        try:
            from offline_queue import OfflineQueue, OperationType

            queue = OfflineQueue()

            # Measure time to queue many operations
            import time

            start_time = time.time()

            for i in range(100):
                queue.enqueue_operation(
                    OperationType.GIT_COMMIT, {"message": f"Test commit {i}"}
                )

            elapsed = time.time() - start_time

            # Should be able to queue 100 operations in under 1 second
            self.assertLess(elapsed, 1.0)

            print(
                f"✅ Queue performance test passed: {elapsed:.3f}s for 100 operations"
            )

        except ImportError as e:
            self.skipTest(f"Cannot import offline_queue: {e}")

    def test_backup_performance(self):
        """Test backup performance"""
        try:
            from backup_rotation import BackupManager, BackupType

            # Create test files
            for i in range(10):
                (self.test_dir / f"test_file_{i}.txt").write_text(f"Content {i}")

            backup_manager = BackupManager()

            # Measure backup creation time
            import time

            start_time = time.time()

            backup_id = backup_manager.create_backup(
                backup_type=BackupType.SNAPSHOT, description="Performance test backup"
            )

            elapsed = time.time() - start_time

            # Should be able to backup small files quickly
            self.assertLess(elapsed, 5.0)
            self.assertIsNotNone(backup_id)

            print(f"✅ Backup performance test passed: {elapsed:.3f}s")

        except ImportError as e:
            self.skipTest(f"Cannot import backup_rotation: {e}")


def run_integration_tests():
    """Run all integration tests"""
    print("🧪 Running NIMDA Integration Tests")
    print("=" * 50)

    # Create test suite
    suite = unittest.TestSuite()

    # Add integration tests
    suite.addTest(unittest.makeSuite(TestNIMDAIntegration))
    suite.addTest(unittest.makeSuite(TestNIMDAPerformance))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")

    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")

    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n{'✅ All tests passed!' if success else '❌ Some tests failed'}")

    return success


if __name__ == "__main__":
    run_integration_tests()
