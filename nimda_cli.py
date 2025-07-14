#!/usr/bin/env python3
"""
NIMDA CLI - Command Line Interface for NIMDA Agent
Provides easy-to-use commands for all NIMDA operations
"""

import argparse
import logging
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

# Add current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from agent import NIMDAAgent
    from backup_rotation import BackupManager
    from changelog_manager import ChangelogManager
    from dev_plan_manager import DevPlanManager
    from git_manager import GitManager
    from offline_queue import OfflineQueue, OperationType
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the NIMDA directory")
    sys.exit(1)

# Setup logging
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


class NIMDACLIColors:
    """ANSI color codes for terminal output"""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class NIMDACLI:
    """Main CLI class for NIMDA operations"""

    def __init__(self):
        self.colors = NIMDACLIColors()
        self.project_path = Path.cwd()

        # Initialize components
        try:
            self.agent = NIMDAAgent(str(self.project_path))
            self.git_manager = GitManager(self.project_path)
            self.dev_plan_manager = DevPlanManager(self.project_path)
            self.changelog_manager = ChangelogManager(self.project_path)
            self.offline_queue = OfflineQueue()
            self.backup_manager = BackupManager()
        except Exception as e:
            self.print_error(f"Failed to initialize NIMDA components: {e}")
            sys.exit(1)

    def print_header(self, text: str):
        """Print colored header"""
        print(f"{self.colors.HEADER}{self.colors.BOLD}{text}{self.colors.ENDC}")

    def print_success(self, text: str):
        """Print success message"""
        print(f"{self.colors.OKGREEN}✅ {text}{self.colors.ENDC}")

    def print_warning(self, text: str):
        """Print warning message"""
        print(f"{self.colors.WARNING}⚠️  {text}{self.colors.ENDC}")

    def print_error(self, text: str):
        """Print error message"""
        print(f"{self.colors.FAIL}❌ {text}{self.colors.ENDC}")

    def print_info(self, text: str):
        """Print info message"""
        print(f"{self.colors.OKBLUE}ℹ️  {text}{self.colors.ENDC}")

    def cmd_init(self, args):
        """Initialize new NIMDA project"""
        self.print_header("🚀 Initializing NIMDA Project")

        try:
            result = self.agent.initialize_project()

            if result:
                self.print_success("Project initialized successfully")

                # Show some basic info about initialization
                print("\n📁 Project initialized with basic structure")
                print(f"  • Path: {self.project_path}")
                print("  • Files created based on project type")
            else:
                self.print_error("Initialization failed")
                return 1

        except Exception as e:
            self.print_error(f"Initialization error: {e}")
            return 1

        return 0

    def cmd_status(self, args):
        """Show project status"""
        self.print_header("📊 NIMDA Project Status")

        try:
            # Git status
            git_status = self.git_manager.get_status()
            print("\n🔗 Git Repository:")
            if git_status.get("initialized"):
                print(f"  • Branch: {git_status.get('current_branch', 'unknown')}")
                print(f"  • Changes: {git_status.get('total_files', 0)} files")
                print(f"  • Remote: {git_status.get('remote_url', 'not configured')}")

                # Show behind/ahead if available
                behind = git_status.get("behind_count", 0)
                ahead = git_status.get("ahead_count", 0)
                if behind > 0:
                    self.print_warning(f"Behind remote by {behind} commits")
                if ahead > 0:
                    self.print_info(f"Ahead of remote by {ahead} commits")
            else:
                self.print_warning("Git repository not initialized")

            # Dev Plan status
            try:
                plan_status = self.dev_plan_manager.get_plan_status()
                print("\n📋 Development Plan:")
                if plan_status.get("exists", False):
                    total = plan_status.get("total_tasks", 0)
                    completed = plan_status.get("completed_tasks", 0)
                    progress = (completed / total * 100) if total > 0 else 0
                    print(f"  • Tasks: {completed}/{total} completed ({progress:.1f}%)")

                    tasks = plan_status.get("tasks", [])
                    categories = set()
                    for task in tasks:
                        if "category" in task:
                            categories.add(task["category"])
                    print(f"  • Categories: {len(categories)}")
                else:
                    self.print_warning("DEV_PLAN.md not found")
            except Exception as e:
                self.print_warning(f"Could not read dev plan: {e}")

            # Changelog status
            try:
                changelog_stats = self.changelog_manager.get_changelog_stats()
                print("\n📝 Changelog:")
                if changelog_stats.get("exists"):
                    print(f"  • Entries: {changelog_stats.get('total_tasks', 0)}")
                    print(f"  • Completed: {changelog_stats.get('completed_tasks', 0)}")
                    print(
                        f"  • Latest version: {changelog_stats.get('latest_version', 'none')}"
                    )
                else:
                    self.print_warning("CHANGELOG.md not found")
            except Exception as e:
                self.print_warning(f"Could not read changelog: {e}")

            # Queue status
            queue_stats = self.offline_queue.get_queue_stats()
            print("\n🔄 Offline Queue:")
            print(f"  • Pending: {queue_stats.get('pending', 0)}")
            print(f"  • Processing: {queue_stats.get('processing', 0)}")
            print(f"  • Completed: {queue_stats.get('completed', 0)}")
            print(f"  • Failed: {queue_stats.get('failed', 0)}")
            print(
                f"  • Network: {'🟢 Online' if queue_stats.get('network_online') else '🔴 Offline'}"
            )

            # Backup status
            backup_stats = self.backup_manager.get_backup_stats()
            print("\n💾 Backups:")
            print(f"  • Total: {backup_stats.get('total_backups', 0)}")
            print(f"  • Size: {backup_stats.get('total_size_gb', 0):.2f} GB")

        except Exception as e:
            self.print_error(f"Status error: {e}")
            return 1

        return 0

    def cmd_sync(self, args):
        """Synchronize with remote repository"""
        self.print_header("🔄 Synchronizing Repository")

        # Add to offline queue for reliable execution
        try:
            operation_id = self.offline_queue.enqueue_operation(
                operation_type=OperationType.GIT_SYNC,
                data={
                    "auto_commit": not args.no_commit,
                    "auto_push": not args.no_push,
                    "force": args.force,
                },
                priority=10,
            )

            self.print_info(f"Sync operation queued: {operation_id}")

            # Start processing if not already running
            self.offline_queue.start_processing()

            # Wait for completion if requested
            if not args.async_mode:
                import time

                max_wait = 120  # 2 minutes
                waited = 0

                while waited < max_wait:
                    operation = self.offline_queue.get_operation_status(operation_id)
                    if operation and operation.status.value in ["completed", "failed"]:
                        break
                    time.sleep(2)
                    waited += 2

                operation = self.offline_queue.get_operation_status(operation_id)
                if operation:
                    if operation.status.value == "completed":
                        self.print_success("Synchronization completed")
                        if operation.result:
                            print(
                                f"  Result: {operation.result.get('message', 'Success')}"
                            )
                    else:
                        self.print_error(f"Synchronization failed: {operation.error}")
                        return 1
                else:
                    self.print_warning("Synchronization status unknown")

        except Exception as e:
            self.print_error(f"Sync error: {e}")
            return 1

        return 0

    def cmd_plan(self, args):
        """Development plan operations"""
        if args.plan_action == "show":
            self.print_header("📋 Development Plan")
            try:
                summary = self.dev_plan_manager.get_plan_status()
                if summary.get("exists", False):
                    print("\n📊 Summary:")
                    print(f"  • Total tasks: {summary.get('total_tasks', 0)}")
                    print(f"  • Completed: {summary.get('completed_tasks', 0)}")

                    tasks = summary.get("tasks", [])
                    categories = set()
                    for task in tasks:
                        if "category" in task:
                            categories.add(task["category"])
                    print(f"  • Categories: {len(categories)}")

                    print("\n📝 Categories:")
                    for category in categories:
                        print(f"  • {category}")

                    if args.verbose:
                        print("\n📋 Tasks:")
                        for i, task in enumerate(tasks[:10], 1):  # Show first 10
                            completed = task.get("completed", False)
                            status = "✅" if completed else "⭕"
                            text = task.get("text", task.get("title", ""))
                            print(f"  {i}. {status} {text[:60]}...")
                else:
                    self.print_warning("DEV_PLAN.md not found")
            except Exception as e:
                self.print_error(f"Plan error: {e}")
                return 1

        elif args.plan_action == "update":
            self.print_header("🔄 Updating Development Plan")
            try:
                result = self.dev_plan_manager.update_and_expand_plan()
                if result.get("success"):
                    added = len(result.get("added_tasks", []))
                    self.print_success(f"Plan updated with {added} new tasks")
                else:
                    self.print_error(f"Update failed: {result.get('error')}")
                    return 1
            except Exception as e:
                self.print_error(f"Update error: {e}")
                return 1

        elif args.plan_action == "execute":
            task_num = args.task_number
            if task_num:
                self.print_header(f"⚡ Executing Task #{task_num}")
                try:
                    result = self.dev_plan_manager.execute_task(task_num)
                    if result.get("success"):
                        self.print_success(f"Task #{task_num} executed successfully")
                    else:
                        self.print_error(
                            f"Task execution failed: {result.get('error')}"
                        )
                        return 1
                except Exception as e:
                    self.print_error(f"Execution error: {e}")
                    return 1
            else:
                self.print_error("Task number required for execution")
                return 1

        return 0

    def cmd_backup(self, args):
        """Backup operations"""
        if args.backup_action == "create":
            backup_type = args.type or "full"
            self.print_header(f"💾 Creating {backup_type} backup")

            try:
                if backup_type == "full":
                    backup_id = self.backup_manager.create_full_backup(
                        str(self.project_path),
                        description=args.description,
                        tags=args.tags.split(",") if args.tags else None,
                    )
                elif backup_type == "snapshot":
                    backup_id = self.backup_manager.create_snapshot_backup(
                        str(self.project_path), description=args.description
                    )
                elif backup_type == "git":
                    backup_id = self.backup_manager.create_git_bundle_backup(
                        str(self.project_path), description=args.description
                    )
                else:
                    self.print_error(f"Unknown backup type: {backup_type}")
                    return 1

                self.print_success(f"Backup created: {backup_id}")

            except Exception as e:
                self.print_error(f"Backup error: {e}")
                return 1

        elif args.backup_action == "list":
            self.print_header("📋 Backup List")
            try:
                backups = self.backup_manager.list_backups()
                if backups:
                    print(
                        f"\n{'ID':<25} {'Type':<12} {'Size':<10} {'Status':<12} {'Date'}"
                    )
                    print("-" * 80)
                    for backup in backups[:20]:  # Show last 20
                        size_mb = backup.size_bytes / (1024**2)
                        date = backup.timestamp[:19].replace("T", " ")
                        print(
                            f"{backup.backup_id:<25} {backup.backup_type.value:<12} "
                            f"{size_mb:>8.1f}MB {backup.status.value:<12} {date}"
                        )
                else:
                    self.print_info("No backups found")
            except Exception as e:
                self.print_error(f"List error: {e}")
                return 1

        elif args.backup_action == "verify":
            backup_id = args.backup_id
            if backup_id:
                self.print_header(f"🔍 Verifying backup {backup_id}")
                try:
                    is_valid = self.backup_manager.verify_backup(backup_id)
                    if is_valid:
                        self.print_success("Backup verification passed")
                    else:
                        self.print_error("Backup verification failed")
                        return 1
                except Exception as e:
                    self.print_error(f"Verification error: {e}")
                    return 1
            else:
                self.print_error("Backup ID required for verification")
                return 1

        elif args.backup_action == "clean":
            self.print_header("🧹 Cleaning old backups")
            try:
                stats = self.backup_manager.apply_rotation_policy()
                self.print_success(f"Removed {stats['removed']} old backups")
                print(f"  Space freed: {stats['total_size_freed'] / (1024**2):.1f} MB")
            except Exception as e:
                self.print_error(f"Cleanup error: {e}")
                return 1

        return 0

    def cmd_queue(self, args):
        """Queue operations"""
        if args.queue_action == "status":
            self.print_header("🔄 Queue Status")
            stats = self.offline_queue.get_queue_stats()

            print("\n📊 Statistics:")
            print(f"  • Total operations: {stats['total_operations']}")
            print(f"  • Pending: {stats['pending']}")
            print(f"  • Processing: {stats['processing']}")
            print(f"  • Completed: {stats['completed']}")
            print(f"  • Failed: {stats['failed']}")
            print(
                f"  • Network: {'🟢 Online' if stats['network_online'] else '🔴 Offline'}"
            )

            if args.verbose:
                recent_ops = self.offline_queue.get_recent_operations(10)
                if recent_ops:
                    print("\n📋 Recent Operations:")
                    for op in recent_ops:
                        status_icon = {
                            "pending": "⏳",
                            "processing": "⚡",
                            "completed": "✅",
                            "failed": "❌",
                            "retrying": "🔄",
                        }.get(op["status"], "❓")

                        print(
                            f"  {status_icon} {op['operation_type']} - {op['status']} ({op['timestamp'][:16]})"
                        )

        elif args.queue_action == "retry":
            self.print_header("🔄 Retrying failed operations")
            try:
                count = self.offline_queue.force_retry_failed()
                self.print_success(f"Queued {count} failed operations for retry")
            except Exception as e:
                self.print_error(f"Retry error: {e}")
                return 1

        elif args.queue_action == "clear":
            self.print_header("🧹 Clearing completed operations")
            try:
                count = self.offline_queue.clear_completed_operations(args.days or 7)
                self.print_success(f"Cleared {count} old completed operations")
            except Exception as e:
                self.print_error(f"Clear error: {e}")
                return 1

        return 0

    def cmd_changelog(self, args):
        """Changelog operations"""
        if args.changelog_action == "add":
            self.print_header("📝 Adding changelog entry")
            try:
                success = self.changelog_manager.add_entry(
                    message=args.message,
                    category=args.category or "Added",
                    completed=not args.pending,
                )
                if success:
                    self.print_success("Changelog entry added")
                else:
                    self.print_error("Failed to add changelog entry")
                    return 1
            except Exception as e:
                self.print_error(f"Changelog error: {e}")
                return 1

        elif args.changelog_action == "stats":
            self.print_header("📊 Changelog Statistics")
            try:
                stats = self.changelog_manager.get_changelog_stats()
                if stats.get("exists"):
                    print("\n📊 Statistics:")
                    print(f"  • Total entries: {stats.get('total_tasks', 0)}")
                    print(f"  • Completed: {stats.get('completed_tasks', 0)}")
                    print(f"  • Pending: {stats.get('pending_tasks', 0)}")
                    print(f"  • Latest version: {stats.get('latest_version', 'none')}")
                    print(f"  • File size: {stats.get('file_size', 0):,} bytes")
                else:
                    self.print_warning("CHANGELOG.md not found")
            except Exception as e:
                self.print_error(f"Stats error: {e}")
                return 1

        return 0

    def cmd_doctor(self, args):
        """Health check and diagnostics"""
        self.print_header("🩺 NIMDA Health Check")

        issues = []

        # Check Git repository
        print("\n🔗 Checking Git repository...")
        try:
            git_status = self.git_manager.get_status()
            if git_status.get("initialized"):
                self.print_success("Git repository initialized")
                if not git_status.get("remote_url"):
                    issues.append("No remote repository configured")
            else:
                issues.append("Git repository not initialized")
        except Exception as e:
            issues.append(f"Git check failed: {e}")

        # Check required files
        print("\n📁 Checking required files...")
        required_files = ["DEV_PLAN.md", "CHANGELOG.md", "README.md"]
        for file_name in required_files:
            file_path = self.project_path / file_name
            if file_path.exists():
                self.print_success(f"{file_name} exists")
            else:
                issues.append(f"Missing required file: {file_name}")

        # Check Python environment
        print("\n🐍 Checking Python environment...")
        try:
            # Try to import modules to check availability
            import importlib.util

            modules_to_check = ["changelog_manager", "dev_plan_manager", "git_manager"]
            missing_modules = []

            for module_name in modules_to_check:
                spec = importlib.util.find_spec(module_name)
                if spec is None:
                    missing_modules.append(module_name)

            if missing_modules:
                issues.append(f"Missing modules: {', '.join(missing_modules)}")
            else:
                self.print_success("All NIMDA modules available")

        except ImportError as e:
            issues.append(f"Module import error: {e}")

        # Check network connectivity
        print("\n🌐 Checking network connectivity...")
        network_online = self.offline_queue.network_monitor.is_online()
        if network_online:
            self.print_success("Network connectivity OK")
        else:
            self.print_warning("Network connectivity issues detected")

        # Check disk space
        print("\n💾 Checking disk space...")
        try:
            total, used, free = shutil.disk_usage(self.project_path)
            free_gb = free / (1024**3)
            if free_gb > 1:
                self.print_success(f"Sufficient disk space: {free_gb:.1f} GB free")
            else:
                issues.append(f"Low disk space: {free_gb:.1f} GB free")
        except Exception as e:
            issues.append(f"Disk space check failed: {e}")

        # Summary
        print("\n📋 Health Check Summary:")
        if issues:
            self.print_warning(f"Found {len(issues)} issues:")
            for issue in issues:
                print(f"  • {issue}")

            if args.fix:
                print("\n🔧 Attempting to fix issues...")
                self._auto_fix_issues(issues)
        else:
            self.print_success("All health checks passed!")

        return len(issues)

    def _auto_fix_issues(self, issues: List[str]):
        """Attempt to automatically fix common issues"""
        for issue in issues:
            if "Git repository not initialized" in issue:
                self.print_info("Initializing Git repository...")
                try:
                    subprocess.run(["git", "init"], cwd=self.project_path, check=True)
                    self.print_success("Git repository initialized")
                except Exception as e:
                    self.print_error(f"Failed to initialize Git: {e}")

            elif "Missing required file:" in issue:
                file_name = issue.split(": ")[1]
                self.print_info(f"Creating {file_name}...")
                try:
                    file_path = self.project_path / file_name
                    if file_name == "README.md":
                        content = (
                            f"# {self.project_path.name}\n\nProject description here.\n"
                        )
                    elif file_name == "DEV_PLAN.md":
                        content = (
                            "# Development Plan\n\n## Tasks\n\n- [ ] Initial setup\n"
                        )
                    elif file_name == "CHANGELOG.md":
                        content = "# Changelog\n\n## [Unreleased]\n\n### Added\n- Initial project setup\n"
                    else:
                        content = f"# {file_name}\n\nContent for {file_name}\n"

                    file_path.write_text(content, encoding="utf-8")
                    self.print_success(f"Created {file_name}")
                except Exception as e:
                    self.print_error(f"Failed to create {file_name}: {e}")


def create_parser():
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        description="NIMDA CLI - Command Line Interface for NIMDA Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nimda init                    # Initialize new project
  nimda status                  # Show project status
  nimda sync                    # Synchronize with remote
  nimda plan show               # Show development plan
  nimda plan execute 5          # Execute task number 5
  nimda backup create --type git # Create Git bundle backup
  nimda doctor --fix            # Run health check with auto-fix
        """,
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    subparsers.add_parser("init", help="Initialize new NIMDA project")

    # Status command
    subparsers.add_parser("status", help="Show project status")

    # Sync command
    sync_parser = subparsers.add_parser(
        "sync", help="Synchronize with remote repository"
    )
    sync_parser.add_argument(
        "--no-commit", action="store_true", help="Skip auto-commit"
    )
    sync_parser.add_argument("--no-push", action="store_true", help="Skip auto-push")
    sync_parser.add_argument(
        "--force", action="store_true", help="Force synchronization"
    )
    sync_parser.add_argument(
        "--async",
        dest="async_mode",
        action="store_true",
        help="Run asynchronously (don't wait for completion)",
    )

    # Plan command
    plan_parser = subparsers.add_parser("plan", help="Development plan operations")
    plan_subparsers = plan_parser.add_subparsers(
        dest="plan_action", help="Plan actions"
    )

    plan_show = plan_subparsers.add_parser("show", help="Show development plan")
    plan_show.add_argument(
        "--verbose", action="store_true", help="Show detailed task list"
    )

    plan_subparsers.add_parser("update", help="Update development plan")

    plan_execute = plan_subparsers.add_parser(
        "execute", help="Execute development plan task"
    )
    plan_execute.add_argument("task_number", type=int, help="Task number to execute")

    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Backup operations")
    backup_subparsers = backup_parser.add_subparsers(
        dest="backup_action", help="Backup actions"
    )

    backup_create = backup_subparsers.add_parser("create", help="Create backup")
    backup_create.add_argument(
        "--type",
        choices=["full", "snapshot", "git"],
        default="full",
        help="Backup type",
    )
    backup_create.add_argument("--description", help="Backup description")
    backup_create.add_argument("--tags", help="Comma-separated tags")

    backup_subparsers.add_parser("list", help="List backups")

    backup_verify = backup_subparsers.add_parser("verify", help="Verify backup")
    backup_verify.add_argument("backup_id", help="Backup ID to verify")

    backup_subparsers.add_parser("clean", help="Clean old backups")

    # Queue command
    queue_parser = subparsers.add_parser("queue", help="Queue operations")
    queue_subparsers = queue_parser.add_subparsers(
        dest="queue_action", help="Queue actions"
    )

    queue_status = queue_subparsers.add_parser("status", help="Show queue status")
    queue_status.add_argument(
        "--verbose", action="store_true", help="Show recent operations"
    )

    queue_subparsers.add_parser("retry", help="Retry failed operations")

    queue_clear = queue_subparsers.add_parser(
        "clear", help="Clear completed operations"
    )
    queue_clear.add_argument(
        "--days", type=int, help="Clear operations older than N days"
    )

    # Changelog command
    changelog_parser = subparsers.add_parser("changelog", help="Changelog operations")
    changelog_subparsers = changelog_parser.add_subparsers(
        dest="changelog_action", help="Changelog actions"
    )

    changelog_add = changelog_subparsers.add_parser("add", help="Add changelog entry")
    changelog_add.add_argument("message", help="Entry message")
    changelog_add.add_argument(
        "--category", help="Entry category (Added, Changed, Fixed, etc.)"
    )
    changelog_add.add_argument("--pending", action="store_true", help="Mark as pending")

    changelog_subparsers.add_parser("stats", help="Show changelog statistics")

    # Doctor command
    doctor_parser = subparsers.add_parser("doctor", help="Health check and diagnostics")
    doctor_parser.add_argument(
        "--fix", action="store_true", help="Attempt to fix issues"
    )

    return parser


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Initialize CLI
    try:
        cli = NIMDACLI()

        # Disable colors if requested
        if args.no_color:
            # Create a simple class with empty color codes that matches NIMDACLIColors
            class NoColors:
                HEADER = ""
                OKBLUE = ""
                OKCYAN = ""
                OKGREEN = ""
                WARNING = ""
                FAIL = ""
                ENDC = ""
                BOLD = ""
                UNDERLINE = ""

            # Use object.__setattr__ to bypass type checking
            object.__setattr__(cli, "colors", NoColors())

        # Route to appropriate command handler
        command_handlers = {
            "init": cli.cmd_init,
            "status": cli.cmd_status,
            "sync": cli.cmd_sync,
            "plan": cli.cmd_plan,
            "backup": cli.cmd_backup,
            "queue": cli.cmd_queue,
            "changelog": cli.cmd_changelog,
            "doctor": cli.cmd_doctor,
        }

        handler = command_handlers.get(args.command)
        if handler:
            return handler(args)
        else:
            cli.print_error(f"Unknown command: {args.command}")
            return 1

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        return 130
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
