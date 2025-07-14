"""
Git manager - manages local and remote repository
"""

import json
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class GitManager:
    """
    Manager for Git repository operations

    Functions:
    - Local Git repository management
    - GitHub synchronization
    - Automatic commits and pushes
    - Conflict resolution
    - Branch management
    """

    def __init__(self, project_path: Path):
        """
        Initialize Git manager

        Args:
            project_path: Path to project
        """
        self.project_path = project_path
        self.logger = logging.getLogger("GitManager")

        # Configuration
        self.config = {
            "auto_commit": True,
            "auto_push": True,
            "auto_pull": True,
            "commit_message_prefix": "🤖 NIMDA:",
            "main_branch": "main",
            "backup_branch": "nimda-backup",
        }

        # Check and initialize Git
        self._ensure_git_initialized()

    def _ensure_git_initialized(self):
        """Check and initialize Git repository"""
        git_dir = self.project_path / ".git"

        if not git_dir.exists():
            self.logger.info("Git repository not found. Initializing...")
            self._run_git_command(["git", "init"])

            # Create initial commit
            self._create_gitignore()
            self._run_git_command(["git", "add", ".gitignore"])
            self._run_git_command(
                ["git", "commit", "-m", "🚀 Initial NIMDA Agent commit"]
            )

    def _create_gitignore(self):
        """Create basic .gitignore file"""
        gitignore_content = """# NIMDA Agent
nimda_logs/
nimda_agent_config.json
*.tmp
*.temp

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Node modules (if using JavaScript)
node_modules/

# Backup files
*.bak
*.backup
"""

        gitignore_file = self.project_path / ".gitignore"

        if not gitignore_file.exists():
            try:
                with open(gitignore_file, "w", encoding="utf-8") as f:
                    f.write(gitignore_content)
                self.logger.info(".gitignore created")
            except Exception as e:
                self.logger.error(f"Error creating .gitignore: {e}")

    def _run_git_command(
        self, command: List[str], capture_output: bool = True
    ) -> Optional[str]:
        """
        execution Git команди

        Args:
            command: Команда для execution
            capture_output: Чи захоплювати вивід

        Returns:
            Вивід команди або None при помилці
        """
        try:
            result = subprocess.run(
                command,
                cwd=self.project_path,
                capture_output=capture_output,
                text=True,
                check=True,
            )

            if capture_output:
                return result.stdout.strip()

            return "Success"

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error executing command {' '.join(command)}: {e}")
            if capture_output and e.stdout:
                self.logger.error(f"STDOUT: {e.stdout}")
            if capture_output and e.stderr:
                self.logger.error(f"STDERR: {e.stderr}")
            return None
        except Exception as e:
            self.logger.error(f"Неочікувана Git error команди: {e}")
            return None

    def get_status(self) -> Dict[str, Any]:
        """
        Receiving статусу Git repository

        Returns:
            status repository
        """
        try:
            # Перевірка чи є Git repository
            git_dir = self.project_path / ".git"
            if not git_dir.exists():
                return {
                    "initialized": False,
                    "message": "Git repository not initialized",
                }

            # current branch
            current_branch = self._run_git_command(["git", "branch", "--show-current"])

            # status files
            status_output = self._run_git_command(["git", "status", "--porcelain"])

            # Аналіз статусу
            has_changes = bool(status_output)
            staged_files = []
            unstaged_files = []
            untracked_files = []

            if status_output:
                for line in status_output.split("\n"):
                    if line:
                        status_code = line[:2]
                        file_path = line[3:]

                        if status_code[0] != " " and status_code[0] != "?":
                            staged_files.append(file_path)

                        if status_code[1] != " ":
                            if status_code[0] == "?":
                                untracked_files.append(file_path)
                            else:
                                unstaged_files.append(file_path)

            # Інформація про remote repository
            remote_url = self._run_git_command(
                ["git", "config", "--get", "remote.origin.url"]
            )

            # last commit
            last_commit = self._run_git_command(["git", "log", "-1", "--oneline"])

            # commit count ahead/behind
            behind_ahead = self._get_behind_ahead_count()

            return {
                "initialized": True,
                "current_branch": current_branch,
                "has_changes": has_changes,
                "staged_files": staged_files,
                "unstaged_files": unstaged_files,
                "untracked_files": untracked_files,
                "remote_url": remote_url,
                "last_commit": last_commit,
                "behind_count": behind_ahead.get("behind", 0),
                "ahead_count": behind_ahead.get("ahead", 0),
                "total_files": len(staged_files)
                + len(unstaged_files)
                + len(untracked_files),
            }

        except Exception as e:
            self.logger.error(f"Error getting status Git: {e}")
            return {
                "initialized": False,
                "error": str(e),
                "message": "Error getting status repository",
            }

    def _get_behind_ahead_count(self) -> Dict[str, int]:
        """Receiving кількості комітів behind/ahead віддаленої branch"""
        try:
            # Спочатку fetch щоб отримати останню інформацію
            self._run_git_command(["git", "fetch"], capture_output=False)

            # Отримуємо commit count
            output = self._run_git_command(
                ["git", "rev-list", "--left-right", "--count", "HEAD...@{u}"]
            )

            if output:
                parts = output.split("\t")
                if len(parts) == 2:
                    return {"ahead": int(parts[0]), "behind": int(parts[1])}

            return {"ahead": 0, "behind": 0}

        except Exception:
            return {"ahead": 0, "behind": 0}

    def has_changes(self) -> bool:
        """
        Перевірка чи є незбережені changes

        Returns:
            True якщо є changes
        """
        status = self.get_status()
        return status.get("has_changes", False)

    def commit_changes(self, message: str, add_all: bool = True) -> Dict[str, Any]:
        """
        Creating commit зі змінами

        Args:
            message: Повідомлення commit
            add_all: Чи додавати all files автоматично

        Returns:
            Результат Creating commit
        """
        try:
            if not self.has_changes():
                return {
                    "success": True,
                    "message": "No changes to commit",
                    "commit_hash": None,
                }

            # Додавання files
            if add_all:
                self._run_git_command(["git", "add", "."])

            # Creating commit
            full_message = f"{self.config['commit_message_prefix']} {message}"
            result = self._run_git_command(["git", "commit", "-m", full_message])

            if result is None:
                return {"success": False, "message": "Error creating commit"}

            # Receiving хешу commit
            commit_hash = self._run_git_command(["git", "rev-parse", "HEAD"])

            if commit_hash:
                self.logger.info(f"Commit created: {commit_hash[:8]} - {full_message}")

                # Автоматичний push якщо налаштовано
                push_result = None
                if self.config["auto_push"]:
                    push_result = self.push_changes()

                return {
                    "success": True,
                    "message": f"Commit created: {commit_hash[:8]}",
                    "commit_hash": commit_hash,
                    "commit_message": full_message,
                    "push_result": push_result,
                }
            else:
                return {"success": False, "message": "Error Receiving хешу commit"}

        except Exception as e:
            self.logger.error(f"Error creating commit: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Error creating commit",
            }

    def push_changes(self, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Sending changes до remote repository

        Args:
            branch: branch для push. Якщо None - current branch

        Returns:
            Результат відправки
        """
        try:
            if not branch:
                branch = self._run_git_command(["git", "branch", "--show-current"])

            if not branch:
                return {
                    "success": False,
                    "message": "failed to визначити поточну гілку",
                }

            # Перевірка наявності remote repository
            remote_url = self._run_git_command(
                ["git", "config", "--get", "remote.origin.url"]
            )
            if not remote_url:
                self.logger.warning(
                    "Remote repository not configured - skipping push"
                )
                return {
                    "success": True,
                    "skipped": True,
                    "message": "Remote repository not configured, skipping push",
                }

            # Push changes
            result = self._run_git_command(["git", "push", "origin", branch])

            if result is None:
                return {"success": False, "message": "Error pushing changes"}

            self.logger.info(f"Changes pushed to remote repository: {branch}")

            return {
                "success": True,
                "message": f"changes відправлено до branch {branch}",
                "branch": branch,
                "remote_url": remote_url,
            }

        except Exception as e:
            self.logger.error(f"Error pushing changes: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Error pushing changes до remote repository",
            }

    def pull_changes(self) -> Dict[str, Any]:
        """
        Receiving changes з remote repository

        Returns:
            Результат Receiving changes
        """
        try:
            # Перевірка наявності remote repository
            remote_url = self._run_git_command(
                ["git", "config", "--get", "remote.origin.url"]
            )
            if not remote_url:
                return {
                    "success": False,
                    "message": "remote repository not configured",
                }

            # Saving local changes перед pull
            if self.has_changes():
                stash_result = self._run_git_command(
                    ["git", "stash", "push", "-m", "NIMDA auto-stash before pull"]
                )
                if stash_result is None:
                    return {
                        "success": False,
                        "message": "Error Saving local changes",
                    }

            # Pull changes
            result = self._run_git_command(["git", "pull", "origin"])

            if result is None:
                return {"success": False, "message": "Error pulling changes"}

            # Відновлення local changes якщо були
            if "NIMDA auto-stash before pull" in str(result):
                stash_pop_result = self._run_git_command(["git", "stash", "pop"])
                if stash_pop_result is None:
                    self.logger.warning(
                        "failed to відновити local changes після pull"
                    )

            self.logger.info("Changes pulled from remote repository")

            return {
                "success": True,
                "message": "Changes successfully received",
                "pull_output": result,
                "remote_url": remote_url,
            }

        except Exception as e:
            self.logger.error(f"Error pulling changes: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Error pulling changes з remote repository",
            }

    def setup_github_remote(self, github_url: str) -> Dict[str, Any]:
        """
        configuration remote GitHub repository

        Args:
            github_url: URL GitHub repository

        Returns:
            Результат configuration
        """
        try:
            # Перевірка існуючого remote
            existing_remote = self._run_git_command(
                ["git", "config", "--get", "remote.origin.url"]
            )

            if existing_remote:
                # Updating існуючого remote
                result = self._run_git_command(
                    ["git", "remote", "set-url", "origin", github_url]
                )
            else:
                # Додавання нового remote
                result = self._run_git_command(
                    ["git", "remote", "add", "origin", github_url]
                )

            if result is None:
                return {
                    "success": False,
                    "message": "Error setting up remote repository",
                }

            # Перевірка з'єднання
            test_result = self._run_git_command(["git", "ls-remote", "origin"])

            if test_result is None:
                return {
                    "success": False,
                    "message": "failed to підключитися до remote repository",
                }

            self.logger.info(f"Remote repository configured: {github_url}")

            return {
                "success": True,
                "message": f"GitHub repository configured: {github_url}",
                "remote_url": github_url,
                "action": "updated" if existing_remote else "added",
            }

        except Exception as e:
            self.logger.error(f"Error configuration GitHub: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Error configuration GitHub repository",
            }

    def create_backup_branch(self) -> Dict[str, Any]:
        """
        Creating резервної branch

        Returns:
            Результат Creating резервної branch
        """
        try:
            backup_branch_name = f"{self.config['backup_branch']}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

            # Creating нової branch
            result = self._run_git_command(
                ["git", "checkout", "-b", backup_branch_name]
            )

            if result is None:
                return {
                    "success": False,
                    "message": "Error creating backup branch",
                }

            # commit поточного стану
            if self.has_changes():
                commit_result = self.commit_changes(
                    "backup копія перед автоматичними змінами"
                )
                if not commit_result["success"]:
                    return {
                        "success": False,
                        "message": "Error Creating резервного commit",
                    }

            # Повернення до основної branch
            main_branch_result = self._run_git_command(
                ["git", "checkout", self.config["main_branch"]]
            )

            if main_branch_result is None:
                self.logger.warning(
                    f"failed to повернутися до branch {self.config['main_branch']}"
                )

            self.logger.info(f"Backup branch created: {backup_branch_name}")

            return {
                "success": True,
                "message": f"Backup branch created: {backup_branch_name}",
                "backup_branch": backup_branch_name,
                "current_branch": self.config["main_branch"],
            }

        except Exception as e:
            self.logger.error(f"Error creating backup branch: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Error creating backup branch",
            }

    def sync_with_remote(self) -> Dict[str, Any]:
        """
        Повна synchronization з віддаленим репозиторієм

        Returns:
            Результат synchronization
        """
        try:
            self.logger.info("Початок synchronization з віддаленим репозиторієм")

            results = []

            # 1. Receiving changes з remote repository
            if self.config["auto_pull"]:
                pull_result = self.pull_changes()
                results.append(("pull", pull_result))

            # 2. commit local changes
            if self.has_changes() and self.config["auto_commit"]:
                commit_result = self.commit_changes("Автоматична synchronization changes")
                results.append(("commit", commit_result))

            # 3. Sending changes
            if self.config["auto_push"]:
                push_result = self.push_changes()
                results.append(("push", push_result))

            # Аналіз результатів
            all_successful = all(result[1]["success"] for result in results)

            return {
                "success": all_successful,
                "message": "synchronization completed"
                if all_successful
                else "synchronization completed with errors",
                "operations": results,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Synchronization error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "critical Synchronization error",
            }
