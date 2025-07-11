"""
Git менеджер - управління локальним та віддаленим репозиторієм
"""

import os
import subprocess
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import logging


class GitManager:
    """
    Менеджер для роботи з Git репозиторієм

    Функції:
    - Управління локальним Git репозиторієм
    - Синхронізація з GitHub
    - Автоматичні коміти та пуші
    - Резолюція конфліктів
    - Управління гілками
    """

    def __init__(self, project_path: Path):
        """
        Ініціалізація Git менеджера

        Args:
            project_path: Шлях до проекту
        """
        self.project_path = project_path
        self.logger = logging.getLogger('GitManager')

        # Конфігурація
        self.config = {
            "auto_commit": True,
            "auto_push": True,
            "auto_pull": True,
            "commit_message_prefix": "🤖 NIMDA:",
            "main_branch": "main",
            "backup_branch": "nimda-backup"
        }

        # Перевірка та ініціалізація Git
        self._ensure_git_initialized()

    def _ensure_git_initialized(self):
        """Перевірка та ініціалізація Git репозиторію"""
        git_dir = self.project_path / ".git"

        if not git_dir.exists():
            self.logger.info("Git репозиторій не знайдено. Ініціалізація...")
            self._run_git_command(["git", "init"])

            # Створення початкового коміту
            self._create_gitignore()
            self._run_git_command(["git", "add", ".gitignore"])
            self._run_git_command(["git", "commit", "-m", "🚀 Початковий коміт NIMDA Agent"])

    def _create_gitignore(self):
        """Створення базового .gitignore файлу"""
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

# Node modules (якщо використовується JavaScript)
node_modules/

# Backup files
*.bak
*.backup
"""

        gitignore_file = self.project_path / ".gitignore"

        if not gitignore_file.exists():
            try:
                with open(gitignore_file, 'w', encoding='utf-8') as f:
                    f.write(gitignore_content)
                self.logger.info(".gitignore створено")
            except Exception as e:
                self.logger.error(f"Помилка створення .gitignore: {e}")

    def _run_git_command(self, command: List[str], capture_output: bool = True) -> Optional[str]:
        """
        Виконання Git команди

        Args:
            command: Команда для виконання
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
                check=True
            )

            if capture_output:
                return result.stdout.strip()

            return "Success"

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Помилка виконання команди {' '.join(command)}: {e}")
            if capture_output and e.stdout:
                self.logger.error(f"STDOUT: {e.stdout}")
            if capture_output and e.stderr:
                self.logger.error(f"STDERR: {e.stderr}")
            return None
        except Exception as e:
            self.logger.error(f"Неочікувана помилка Git команди: {e}")
            return None

    def get_status(self) -> Dict[str, Any]:
        """
        Отримання статусу Git репозиторію

        Returns:
            Статус репозиторію
        """
        try:
            # Перевірка чи є Git репозиторій
            git_dir = self.project_path / ".git"
            if not git_dir.exists():
                return {
                    "initialized": False,
                    "message": "Git репозиторій не ініціалізовано"
                }

            # Поточна гілка
            current_branch = self._run_git_command(["git", "branch", "--show-current"])

            # Статус файлів
            status_output = self._run_git_command(["git", "status", "--porcelain"])

            # Аналіз статусу
            has_changes = bool(status_output)
            staged_files = []
            unstaged_files = []
            untracked_files = []

            if status_output:
                for line in status_output.split('\n'):
                    if line:
                        status_code = line[:2]
                        file_path = line[3:]

                        if status_code[0] != ' ' and status_code[0] != '?':
                            staged_files.append(file_path)

                        if status_code[1] != ' ':
                            if status_code[0] == '?':
                                untracked_files.append(file_path)
                            else:
                                unstaged_files.append(file_path)

            # Інформація про віддалений репозиторій
            remote_url = self._run_git_command(["git", "config", "--get", "remote.origin.url"])

            # Останній коміт
            last_commit = self._run_git_command(["git", "log", "-1", "--oneline"])

            # Кількість комітів попереду/позаду
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
                "total_files": len(staged_files) + len(unstaged_files) + len(untracked_files)
            }

        except Exception as e:
            self.logger.error(f"Помилка отримання статусу Git: {e}")
            return {
                "initialized": False,
                "error": str(e),
                "message": "Помилка отримання статусу репозиторію"
            }

    def _get_behind_ahead_count(self) -> Dict[str, int]:
        """Отримання кількості комітів позаду/попереду віддаленої гілки"""
        try:
            # Спочатку fetch щоб отримати останню інформацію
            self._run_git_command(["git", "fetch"], capture_output=False)

            # Отримуємо кількість комітів
            output = self._run_git_command(["git", "rev-list", "--left-right", "--count", "HEAD...@{u}"])

            if output:
                parts = output.split('\t')
                if len(parts) == 2:
                    return {
                        "ahead": int(parts[0]),
                        "behind": int(parts[1])
                    }

            return {"ahead": 0, "behind": 0}

        except Exception:
            return {"ahead": 0, "behind": 0}

    def has_changes(self) -> bool:
        """
        Перевірка чи є незбережені зміни

        Returns:
            True якщо є зміни
        """
        status = self.get_status()
        return status.get("has_changes", False)

    def commit_changes(self, message: str, add_all: bool = True) -> Dict[str, Any]:
        """
        Створення коміту зі змінами

        Args:
            message: Повідомлення коміту
            add_all: Чи додавати всі файли автоматично

        Returns:
            Результат створення коміту
        """
        try:
            if not self.has_changes():
                return {
                    "success": True,
                    "message": "Немає змін для коміту",
                    "commit_hash": None
                }

            # Додавання файлів
            if add_all:
                self._run_git_command(["git", "add", "."])

            # Створення коміту
            full_message = f"{self.config['commit_message_prefix']} {message}"
            result = self._run_git_command(["git", "commit", "-m", full_message])

            if result is None:
                return {
                    "success": False,
                    "message": "Помилка створення коміту"
                }

            # Отримання хешу коміту
            commit_hash = self._run_git_command(["git", "rev-parse", "HEAD"])

            if commit_hash:
                self.logger.info(f"Коміт створено: {commit_hash[:8]} - {full_message}")

                # Автоматичний push якщо налаштовано
                push_result = None
                if self.config["auto_push"]:
                    push_result = self.push_changes()

                return {
                    "success": True,
                    "message": f"Коміт створено: {commit_hash[:8]}",
                    "commit_hash": commit_hash,
                    "commit_message": full_message,
                    "push_result": push_result
                }
            else:
                return {
                    "success": False,
                    "message": "Помилка отримання хешу коміту"
                }

        except Exception as e:
            self.logger.error(f"Помилка створення коміту: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Помилка створення коміту"
            }

    def push_changes(self, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Відправка змін до віддаленого репозиторію

        Args:
            branch: Гілка для push. Якщо None - поточна гілка

        Returns:
            Результат відправки
        """
        try:
            if not branch:
                branch = self._run_git_command(["git", "branch", "--show-current"])

            if not branch:
                return {
                    "success": False,
                    "message": "Не вдалося визначити поточну гілку"
                }

            # Перевірка наявності віддаленого репозиторію
            remote_url = self._run_git_command(["git", "config", "--get", "remote.origin.url"])
            if not remote_url:
                return {
                    "success": False,
                    "message": "Віддалений репозиторій не налаштовано"
                }

            # Push змін
            result = self._run_git_command(["git", "push", "origin", branch])

            if result is None:
                return {
                    "success": False,
                    "message": "Помилка відправки змін"
                }

            self.logger.info(f"Зміни відправлено до віддаленого репозиторію: {branch}")

            return {
                "success": True,
                "message": f"Зміни відправлено до гілки {branch}",
                "branch": branch,
                "remote_url": remote_url
            }

        except Exception as e:
            self.logger.error(f"Помилка відправки змін: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Помилка відправки змін до віддаленого репозиторію"
            }

    def pull_changes(self) -> Dict[str, Any]:
        """
        Отримання змін з віддаленого репозиторію

        Returns:
            Результат отримання змін
        """
        try:
            # Перевірка наявності віддаленого репозиторію
            remote_url = self._run_git_command(["git", "config", "--get", "remote.origin.url"])
            if not remote_url:
                return {
                    "success": False,
                    "message": "Віддалений репозиторій не налаштовано"
                }

            # Збереження локальних змін перед pull
            if self.has_changes():
                stash_result = self._run_git_command(["git", "stash", "push", "-m", "NIMDA auto-stash before pull"])
                if stash_result is None:
                    return {
                        "success": False,
                        "message": "Помилка збереження локальних змін"
                    }

            # Pull змін
            result = self._run_git_command(["git", "pull", "origin"])

            if result is None:
                return {
                    "success": False,
                    "message": "Помилка отримання змін"
                }

            # Відновлення локальних змін якщо були
            if "NIMDA auto-stash before pull" in str(result):
                stash_pop_result = self._run_git_command(["git", "stash", "pop"])
                if stash_pop_result is None:
                    self.logger.warning("Не вдалося відновити локальні зміни після pull")

            self.logger.info("Зміни отримано з віддаленого репозиторію")

            return {
                "success": True,
                "message": "Зміни успішно отримано",
                "pull_output": result,
                "remote_url": remote_url
            }

        except Exception as e:
            self.logger.error(f"Помилка отримання змін: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Помилка отримання змін з віддаленого репозиторію"
            }

    def setup_github_remote(self, github_url: str) -> Dict[str, Any]:
        """
        Налаштування віддаленого GitHub репозиторію

        Args:
            github_url: URL GitHub репозиторію

        Returns:
            Результат налаштування
        """
        try:
            # Перевірка існуючого remote
            existing_remote = self._run_git_command(["git", "config", "--get", "remote.origin.url"])

            if existing_remote:
                # Оновлення існуючого remote
                result = self._run_git_command(["git", "remote", "set-url", "origin", github_url])
            else:
                # Додавання нового remote
                result = self._run_git_command(["git", "remote", "add", "origin", github_url])

            if result is None:
                return {
                    "success": False,
                    "message": "Помилка налаштування віддаленого репозиторію"
                }

            # Перевірка з'єднання
            test_result = self._run_git_command(["git", "ls-remote", "origin"])

            if test_result is None:
                return {
                    "success": False,
                    "message": "Не вдалося підключитися до віддаленого репозиторію"
                }

            self.logger.info(f"Віддалений репозиторій налаштовано: {github_url}")

            return {
                "success": True,
                "message": f"GitHub репозиторій налаштовано: {github_url}",
                "remote_url": github_url,
                "action": "updated" if existing_remote else "added"
            }

        except Exception as e:
            self.logger.error(f"Помилка налаштування GitHub: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Помилка налаштування GitHub репозиторію"
            }

    def create_backup_branch(self) -> Dict[str, Any]:
        """
        Створення резервної гілки

        Returns:
            Результат створення резервної гілки
        """
        try:
            backup_branch_name = f"{self.config['backup_branch']}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

            # Створення нової гілки
            result = self._run_git_command(["git", "checkout", "-b", backup_branch_name])

            if result is None:
                return {
                    "success": False,
                    "message": "Помилка створення резервної гілки"
                }

            # Коміт поточного стану
            if self.has_changes():
                commit_result = self.commit_changes("Резервна копія перед автоматичними змінами")
                if not commit_result["success"]:
                    return {
                        "success": False,
                        "message": "Помилка створення резервного коміту"
                    }

            # Повернення до основної гілки
            main_branch_result = self._run_git_command(["git", "checkout", self.config["main_branch"]])

            if main_branch_result is None:
                self.logger.warning(f"Не вдалося повернутися до гілки {self.config['main_branch']}")

            self.logger.info(f"Резервну гілку створено: {backup_branch_name}")

            return {
                "success": True,
                "message": f"Резервну гілку створено: {backup_branch_name}",
                "backup_branch": backup_branch_name,
                "current_branch": self.config["main_branch"]
            }

        except Exception as e:
            self.logger.error(f"Помилка створення резервної гілки: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Помилка створення резервної гілки"
            }

    def sync_with_remote(self) -> Dict[str, Any]:
        """
        Повна синхронізація з віддаленим репозиторієм

        Returns:
            Результат синхронізації
        """
        try:
            self.logger.info("Початок синхронізації з віддаленим репозиторієм")

            results = []

            # 1. Отримання змін з віддаленого репозиторію
            if self.config["auto_pull"]:
                pull_result = self.pull_changes()
                results.append(("pull", pull_result))

            # 2. Коміт локальних змін
            if self.has_changes() and self.config["auto_commit"]:
                commit_result = self.commit_changes("Автоматична синхронізація змін")
                results.append(("commit", commit_result))

            # 3. Відправка змін
            if self.config["auto_push"]:
                push_result = self.push_changes()
                results.append(("push", push_result))

            # Аналіз результатів
            all_successful = all(result[1]["success"] for result in results)

            return {
                "success": all_successful,
                "message": "Синхронізація завершена" if all_successful else "Синхронізація завершена з помилками",
                "operations": results,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Помилка синхронізації: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Критична помилка синхронізації"
            }
