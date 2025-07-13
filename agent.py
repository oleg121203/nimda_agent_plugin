"""
Основний клас NIMDA Agent - автономний агент розробки
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from dev_plan_manager import DevPlanManager
from git_manager import GitManager
from command_processor import CommandProcessor
from project_initializer import ProjectInitializer
from changelog_manager import ChangelogManager


class NIMDAAgent:
    """
    Універсальний автономний агент розробки NIMDA

    Функції:
    - Читає та виконує DEV_PLAN.md
    - Управляє Git репозиторієм (локальним та GitHub)
    - Виправляє помилки автоматично
    - Створює необхідні файли проекту
    - Веде журнал змін у CHANGELOG.md
    """

    def __init__(self, project_path: Optional[str] = None):
        """
        Ініціалізація агента

        Args:
            project_path: Шлях до проекту. Якщо None - використовується поточна директорія
        """
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.config_file = self.project_path / "nimda_agent_config.json"

        # Завантаження змінних середовища
        env_file = self.project_path / ".env"
        if env_file.exists():
            load_dotenv(env_file)
        else:
            # Спробувати завантажити з кореневої папки плагіна
            plugin_env = Path(__file__).parent / ".env"
            if plugin_env.exists():
                load_dotenv(plugin_env)

        # Налаштування логування
        self._setup_logging()

        # Ініціалізація компонентів
        self.dev_plan_manager = DevPlanManager(
            self.project_path, max_retries=self.config.get("max_retries", 3)
        )
        self.git_manager = GitManager(self.project_path)
        self.command_processor = CommandProcessor(self)
        self.project_initializer = ProjectInitializer(self.project_path)
        self.changelog_manager = ChangelogManager(self.project_path)

        # Завантаження конфігурації
        self.config = self._load_config()

        # Статус агента
        self.is_running = False
        self.current_task = None
        self.execution_log = []

        self.logger.info(f"NIMDA Agent ініціалізовано для проекту: {self.project_path}")

    def _setup_logging(self):
        """Налаштування системи логування"""
        log_dir = self.project_path / "nimda_logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"nimda_agent_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger('NIMDAAgent')

    def _load_config(self) -> Dict[str, Any]:
        """Завантаження конфігурації агента"""
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
            "enable_debug": os.getenv("ENABLE_DEBUG", "false").lower() == "true"
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Оновлення конфігурації з default значеннями
                    for key, value in default_config.items():
                        config.setdefault(key, value)
                    return config
            except Exception as e:
                self.logger.warning(f"Помилка завантаження конфігурації: {e}")

        return default_config

    def _save_config(self):
        """Збереження конфігурації агента"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Помилка збереження конфігурації: {e}")

    def initialize_project(self) -> bool:
        """
        Ініціалізація проекту - створення необхідних файлів та структури

        Returns:
            bool: True якщо ініціалізація успішна
        """
        try:
            self.logger.info("Початок ініціалізації проекту...")

            # Ініціалізація основних файлів проекту
            success = self.project_initializer.initialize()

            if success:
                self.logger.info("Проект успішно ініціалізовано")
                self.changelog_manager.add_entry("🚀 Проект ініціалізовано NIMDA Agent")
                return True
            else:
                self.logger.error("Помилка ініціалізації проекту")
                return False

        except Exception as e:
            self.logger.error(f"Критична помилка ініціалізації: {e}")
            return False

    def process_command(self, command: str) -> Dict[str, Any]:
        """
        Обробка команди від користувача через Codex

        Args:
            command: Команда від користувача

        Returns:
            Dict з результатом виконання
        """
        self.logger.info(f"Отримано команду: {command}")

        try:
            result = self.command_processor.process(command)

            # Логування результату
            self.execution_log.append({
                "timestamp": datetime.now().isoformat(),
                "command": command,
                "result": result,
                "success": result.get("success", False)
            })

            return result

        except Exception as e:
            self.logger.error(f"Помилка обробки команди: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Помилка виконання команди"
            }

    def execute_dev_plan(self, task_number: Optional[int] = None) -> Dict[str, Any]:
        """
        Виконання DEV_PLAN.md повністю або конкретної задачі

        Args:
            task_number: Номер конкретної задачі. Якщо None - виконується весь план

        Returns:
            Dict з результатом виконання
        """
        try:
            self.is_running = True

            if task_number:
                self.logger.info(f"Виконання задачі #{task_number} з DEV_PLAN.md")
                result = self.dev_plan_manager.execute_task(task_number)
            else:
                self.logger.info("Виконання повного DEV_PLAN.md")
                result = self.dev_plan_manager.execute_full_plan()

            # Оновлення статусу виконання
            if result.get("success"):
                completed_tasks = result.get("completed_tasks", [])
                for task in completed_tasks:
                    self.changelog_manager.mark_task_completed(task)

            self.is_running = False
            return result

        except Exception as e:
            self.is_running = False
            self.logger.error(f"Помилка виконання DEV_PLAN: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Критична помилка виконання плану розробки"
            }

    def update_dev_plan(self) -> Dict[str, Any]:
        """
        Оновлення та розширення DEV_PLAN.md

        Returns:
            Dict з результатом оновлення
        """
        try:
            self.logger.info("Оновлення DEV_PLAN.md")

            result = self.dev_plan_manager.update_and_expand_plan()

            if result.get("success"):
                self.changelog_manager.add_entry("📋 DEV_PLAN.md оновлено та розширено")

            return result

        except Exception as e:
            self.logger.error(f"Помилка оновлення DEV_PLAN: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Помилка оновлення плану розробки"
            }

    def auto_fix_errors(self) -> Dict[str, Any]:
        """
        Автоматичне виправлення помилок в проекті

        Returns:
            Dict з результатом виправлення
        """
        try:
            self.logger.info("Початок автоматичного виправлення помилок")

            # Перевірка помилок в коді
            errors = self._detect_errors()

            if not errors:
                return {
                    "success": True,
                    "message": "Помилок не виявлено",
                    "fixed_count": 0
                }

            fixed_count = 0
            for error in errors:
                if self._fix_error(error):
                    fixed_count += 1

            # Фіксація змін
            if fixed_count > 0:
                self.git_manager.commit_changes(f"🔧 Автоматично виправлено {fixed_count} помилок")
                self.changelog_manager.add_entry(f"🔧 Автоматично виправлено {fixed_count} помилок")

            return {
                "success": True,
                "message": f"Виправлено {fixed_count} з {len(errors)} помилок",
                "fixed_count": fixed_count,
                "total_errors": len(errors)
            }

        except Exception as e:
            self.logger.error(f"Помилка автоматичного виправлення: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Помилка системи автоматичного виправлення"
            }

    def _detect_errors(self) -> List[Dict[str, Any]]:
        """Виявлення помилок в проекті"""
        errors = []

        # Тут буде логіка виявлення помилок
        # Поки що заглушка

        return errors

    def _fix_error(self, error: Dict[str, Any]) -> bool:
        """Виправлення конкретної помилки"""
        # Тут буде логіка виправлення помилок
        # Поки що заглушка
        return True

    def get_status(self) -> Dict[str, Any]:
        """
        Отримання поточного статусу агента

        Returns:
            Dict зі статусом агента
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
            "execution_log_size": len(self.execution_log)
        }

    def shutdown(self):
        """Завершення роботи агента"""
        self.logger.info("Завершення роботи NIMDA Agent")

        # Збереження конфігурації
        self.config["last_execution"] = datetime.now().isoformat()
        self._save_config()

        # Фінальний коміт якщо є незбережені зміни
        if self.git_manager.has_changes():
            self.git_manager.commit_changes("💾 Автоматичне збереження змін при завершенні NIMDA Agent")

        self.is_running = False

    def get_env_var(self, key: str, default: Any = None) -> str:
        """
        Отримання змінної середовища

        Args:
            key: Назва змінної
            default: Значення за замовчуванням

        Returns:
            Значення змінної середовища
        """
        return os.getenv(key, default)

    def is_env_configured(self) -> bool:
        """
        Перевірка чи налаштовані основні змінні середовища

        Returns:
            True якщо основні змінні налаштовані
        """
        required_vars = ["GIT_USER_NAME", "GIT_USER_EMAIL"]
        return all(os.getenv(var) for var in required_vars)
