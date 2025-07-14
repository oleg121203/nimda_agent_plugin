"""
Main NIMDA Agent class - autonomous development agent
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from changelog_manager import ChangelogManager
from command_processor import CommandProcessor
from dev_plan_manager import DevPlanManager
from git_manager import GitManager
from project_initializer import ProjectInitializer


class NIMDAAgent:
    """
    Universal autonomous development agent NIMDA

    Functions:
    - Reads and executes DEV_PLAN.md
    - Manages Git repository (local and GitHub)
    - Fixes errors automatically
    - Creates necessary project files
    - Maintains changelog in CHANGELOG.md
    """

    def __init__(self, project_path: Optional[str] = None):
        """
        Initialize the agent

        Args:
            project_path: Path to the project. If None - uses current directory
        """
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.config_file = self.project_path / "nimda_agent_config.json"

        # Setup logging first
        self._setup_logging()

        # Load environment variables
        # NOTE: load_dotenv импортируется безусловно, но используется только при наличии .env файлов
        # Это позволяет агенту работать с переменными окружения из системы, если .env отсутствует
        env_file = self.project_path / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            self.logger.info(f"Loaded environment from: {env_file}")
        else:
            # Try to load from plugin root folder
            plugin_env = Path(__file__).parent / ".env"
            if plugin_env.exists():
                load_dotenv(plugin_env)
                self.logger.info(f"Loaded environment from plugin: {plugin_env}")
            else:
                self.logger.info(
                    "No .env files found, using system environment variables"
                )

        # Load configuration before initializing components
        self.config = self._load_config()

        # Initialize components
        self.dev_plan_manager = DevPlanManager(
            self.project_path, max_retries=self.config.get("max_retries", 3)
        )
        self.git_manager = GitManager(self.project_path)
        self.command_processor = CommandProcessor(self)
        self.project_initializer = ProjectInitializer(self.project_path)
        self.changelog_manager = ChangelogManager(self.project_path)

        # Agent status
        self.is_running = False
        self.current_task = None
        self.execution_log = []

        self.logger.info(f"NIMDA Agent initialized for project: {self.project_path}")

    def _setup_logging(self):
        """Setup logging system"""
        log_dir = self.project_path / "nimda_logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"nimda_agent_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )

        self.logger = logging.getLogger("NIMDAAgent")

    def _load_config(self) -> Dict[str, Any]:
        """Load agent configuration"""
        default_config = {
            "version": "1.0.0",
            "auto_commit": os.getenv("AUTO_COMMIT", "true").lower() == "true",
            "auto_push": os.getenv("AUTO_PUSH", "true").lower() == "true",
            "create_backups": os.getenv("CREATE_BACKUPS", "true").lower() == "true",
            "max_retries": int(os.getenv("MAX_RETRIES", "3")),
            "github_integration": True,
            "codex_integration": True,
            "languages": [],
            "frameworks": [],
            "last_execution": None,
            "github_token": os.getenv("GITHUB_TOKEN"),
            "github_username": os.getenv("GITHUB_USERNAME"),
            "github_repo_url": os.getenv("GITHUB_REPO_URL"),
            "git_user_name": os.getenv("GIT_USER_NAME"),
            "git_user_email": os.getenv("GIT_USER_EMAIL"),
            "project_name": os.getenv("PROJECT_NAME", "NIMDA-CLI"),
            "enable_debug": os.getenv("ENABLE_DEBUG", "false").lower() == "true",
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    # Update configuration with default values
                    for key, value in default_config.items():
                        config.setdefault(key, value)
                    return config
            except Exception as e:
                self.logger.warning(f"Error loading configuration: {e}")

        return default_config

    def _save_config(self):
        """Save agent configuration"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")

    def initialize_project(self) -> bool:
        """
        Project initialization - create necessary files and structure

        Returns:
            bool: True if initialization successful
        """
        try:
            self.logger.info("Starting project initialization...")

            # Initialize main project files
            success = self.project_initializer.initialize()

            if success:
                self.logger.info("Project successfully initialized")
                self.changelog_manager.add_entry(
                    "🚀 Project initialized by NIMDA Agent"
                )
                return True
            else:
                self.logger.error("Project initialization error")
                return False

        except Exception as e:
            self.logger.error(f"Critical initialization error: {e}")
            return False

    def process_command(self, command: str) -> Dict[str, Any]:
        """
        Process command from user via Codex

        Args:
            command: Command from user

        Returns:
            Dict with execution result
        """
        self.logger.info(f"Received command: {command}")

        try:
            result = self.command_processor.process(command)

            # Log result
            self.execution_log.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "command": command,
                    "result": result,
                    "success": result.get("success", False),
                }
            )

            return result

        except Exception as e:
            self.logger.error(f"Command processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Command execution error",
            }

    def execute_dev_plan(self, task_number: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute DEV_PLAN.md completely or specific task

        Args:
            task_number: Specific task number. If None - execute entire plan

        Returns:
            Dict with execution result
        """
        try:
            self.is_running = True

            if task_number:
                self.logger.info(f"Executing task #{task_number} from DEV_PLAN.md")
                result = self.dev_plan_manager.execute_task(task_number)
            else:
                self.logger.info("Executing full DEV_PLAN.md")

                # Check if this is a new project creation plan
                plan_content = ""
                if self.dev_plan_manager.dev_plan_file.exists():
                    with open(
                        self.dev_plan_manager.dev_plan_file, "r", encoding="utf-8"
                    ) as f:
                        plan_content = f.read()

                # If plan contains project creation instructions, create new project
                if (
                    "~/Projects/" in plan_content
                    and "Project Location:" in plan_content
                ):
                    self.logger.info("DEV_PLAN indicates new project creation")
                    result = self.dev_plan_manager.create_project_from_plan()
                else:
                    # Execute plan in current directory
                    result = self.dev_plan_manager.execute_full_plan()

            # Update execution status
            if result.get("success"):
                completed_tasks = result.get("completed_tasks", [])
                for task in completed_tasks:
                    self.changelog_manager.mark_task_completed(task)

            self.is_running = False
            return result

        except Exception as e:
            self.is_running = False
            self.logger.error(f"DEV_PLAN execution error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Critical development plan execution error",
            }

    def run_full_dev_cycle(self) -> Dict[str, Any]:
        """Full DEV_PLAN execution cycle with automatic GitHub synchronization"""
        try:
            self.logger.info("🔄 Starting full DEV cycle")

            pre_sync = self.git_manager.sync_with_remote()

            plan_result = self.execute_dev_plan()

            commit_result = self.git_manager.commit_changes(
                "Automatic DEV_PLAN execution"
            )

            push_result = (
                self.git_manager.push_changes()
                if commit_result.get("success")
                else None
            )

            return {
                "success": plan_result.get("success", False)
                and commit_result.get("success", True)
                and (push_result.get("success", True) if push_result else True),
                "plan": plan_result,
                "commit": commit_result,
                "push": push_result,
                "pre_sync": pre_sync,
            }

        except Exception as e:
            self.logger.error(f"Automatic DEV cycle error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Automatic DEV cycle error",
            }

    def update_dev_plan(self) -> Dict[str, Any]:
        """
        Update and expand DEV_PLAN.md

        Returns:
            Dict with update result
        """
        try:
            self.logger.info("Updating DEV_PLAN.md")

            result = self.dev_plan_manager.update_and_expand_plan()

            if result.get("success"):
                self.changelog_manager.add_entry("📋 DEV_PLAN.md updated and expanded")

            return result

        except Exception as e:
            self.logger.error(f"DEV_PLAN update error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Development plan update error",
            }

    def auto_fix_errors(self) -> Dict[str, Any]:
        """
        Automatic error fixing in the project

        Returns:
            Dict with fixing result
        """
        try:
            self.logger.info("Starting automatic error fixing")

            # Check code errors
            errors = self._detect_errors()

            if not errors:
                return {
                    "success": True,
                    "message": "No errors detected",
                    "fixed_count": 0,
                }

            fixed_count = 0
            for error in errors:
                if self._fix_error(error):
                    fixed_count += 1

            # Commit changes
            if fixed_count > 0:
                self.git_manager.commit_changes(
                    f"🔧 Automatically fixed {fixed_count} errors"
                )
                self.changelog_manager.add_entry(
                    f"🔧 Automatically fixed {fixed_count} errors"
                )

            return {
                "success": True,
                "message": f"Fixed {fixed_count} of {len(errors)} errors",
                "fixed_count": fixed_count,
                "total_errors": len(errors),
            }

        except Exception as e:
            self.logger.error(f"Automatic fixing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Automatic fixing system error",
            }

    def _detect_errors(self) -> List[Dict[str, Any]]:
        """Detect errors in the project"""
        errors = []

        # Here will be error detection logic
        # Currently stub

        return errors

    def _fix_error(self, error: Dict[str, Any]) -> bool:
        """Fix specific error"""
        # Here will be error fixing logic
        # Currently stub
        return True

    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status

        Returns:
            Dict with agent status
        """
        dev_plan_status = self.dev_plan_manager.get_plan_status()
        git_status = self.git_manager.get_status()

        return {
            "agent_running": self.is_running,
            "current_task": self.current_task,
            "project_path": str(self.project_path),
            "dev_plan": dev_plan_status,
            "git": git_status,
            "last_execution": self.config.get("last_execution"),
            "execution_log_size": len(self.execution_log),
        }

    def shutdown(self):
        """Agent shutdown"""
        self.logger.info("NIMDA Agent shutdown")

        # Save configuration
        self.config["last_execution"] = datetime.now().isoformat()
        self._save_config()

        # Final commit if there are unsaved changes
        if self.git_manager.has_changes():
            self.git_manager.commit_changes(
                "💾 Automatic save changes on NIMDA Agent shutdown"
            )

        self.is_running = False

    def get_env_var(self, key: str, default: Any = None) -> str:
        """
        Get environment variable

        Args:
            key: Variable name
            default: Default value

        Returns:
            Environment variable value
        """
        return os.getenv(key, default)

    def is_env_configured(self) -> bool:
        """
        Check if main environment variables are configured

        Returns:
            True if main variables are configured
        """
        required_vars = ["GIT_USER_NAME", "GIT_USER_EMAIL"]
        return all(os.getenv(var) for var in required_vars)
