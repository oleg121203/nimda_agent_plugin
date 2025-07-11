"""
Обробник команд від користувача через Codex
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging


class CommandProcessor:
    """
    Обробник команд для NIMDA Agent

    Підтримувані команди:
    - "допрацюй девплан" - робота тільки з планом
    - "виконай задачу номер X" - виконання конкретної задачі
    - "виконай весь ДЕВ" - виконання всього плану
    - "статус" - отримання статусу
    - "синхронізація" - синхронізація з Git
    """

    def __init__(self, agent):
        """
        Ініціалізація обробника команд

        Args:
            agent: Екземпляр NIMDAAgent
        """
        self.agent = agent
        self.logger = logging.getLogger('CommandProcessor')

        # Шаблони команд
        self.command_patterns = {
            "update_plan": [
                r"допрацюй девплан",
                r"update.*dev.*plan",
                r"оновити.*план",
                r"розширити.*план"
            ],
            "execute_task": [
                r"виконай.*задач[у|і].*номер\s*(\d+)",
                r"execute.*task.*(\d+)",
                r"зроби.*задач[у|і]\s*(\d+)",
                r"task\s*(\d+)"
            ],
            "execute_full_plan": [
                r"виконай.*весь.*дев",
                r"execute.*full.*dev",
                r"виконай.*повний.*план",
                r"зроби.*все",
                r"run.*full.*plan"
            ],
            "status": [
                r"статус",
                r"status",
                r"стан",
                r"що.*робиш",
                r"how.*going"
            ],
            "sync": [
                r"синхронізація",
                r"sync",
                r"git.*sync",
                r"оновити.*git"
            ],
            "fix_errors": [
                r"виправити.*помилки",
                r"fix.*errors",
                r"debug",
                r"виправлення"
            ],
            "initialize": [
                r"ініціалізація",
                r"initialize",
                r"setup",
                r"налаштування",
                r"створи.*проект"
            ],
            "help": [
                r"допомога",
                r"help",
                r"команди",
                r"що.*можеш"
            ]
        }

    def process(self, command: str) -> Dict[str, Any]:
        """
        Обробка команди від користувача

        Args:
            command: Команда від користувача

        Returns:
            Результат виконання команди
        """
        try:
            # Нормалізація команди
            normalized_command = command.lower().strip()

            self.logger.info(f"Обробка команди: {command}")

            # Визначення типу команди
            command_type, params = self._identify_command(normalized_command)

            if not command_type:
                return self._handle_unknown_command(command)

            # Виконання команди
            return self._execute_command(command_type, params, command)

        except Exception as e:
            self.logger.error(f"Помилка обробки команди: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Помилка обробки команди",
                "command": command
            }

    def _identify_command(self, command: str) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Визначення типу команди за шаблонами

        Args:
            command: Нормалізована команда

        Returns:
            Тип команди та параметри
        """
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, command, re.IGNORECASE | re.UNICODE)
                if match:
                    params = {}

                    # Витягування параметрів з груп regex
                    if match.groups():
                        if command_type == "execute_task":
                            params["task_number"] = int(match.group(1))

                    return command_type, params

        return None, {}

    def _execute_command(self, command_type: str, params: Dict[str, Any], original_command: str) -> Dict[str, Any]:
        """
        Виконання конкретної команди

        Args:
            command_type: Тип команди
            params: Параметри команди
            original_command: Оригінальна команда

        Returns:
            Результат виконання
        """
        try:
            self.logger.info(f"Виконання команди типу: {command_type}")

            if command_type == "update_plan":
                return self._handle_update_plan()

            elif command_type == "execute_task":
                task_number = params.get("task_number")
                if task_number:
                    return self._handle_execute_task(task_number)
                else:
                    return {
                        "success": False,
                        "message": "Не вказано номер задачі"
                    }

            elif command_type == "execute_full_plan":
                return self._handle_execute_full_plan()

            elif command_type == "status":
                return self._handle_status()

            elif command_type == "sync":
                return self._handle_sync()

            elif command_type == "fix_errors":
                return self._handle_fix_errors()

            elif command_type == "initialize":
                return self._handle_initialize()

            elif command_type == "help":
                return self._handle_help()

            else:
                return {
                    "success": False,
                    "message": f"Команда '{command_type}' не реалізована"
                }

        except Exception as e:
            self.logger.error(f"Помилка виконання команди {command_type}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Помилка виконання команди {command_type}"
            }

    def _handle_update_plan(self) -> Dict[str, Any]:
        """Обробка команди оновлення плану"""
        self.logger.info("Виконання оновлення DEV_PLAN.md")

        result = self.agent.update_dev_plan()

        if result["success"]:
            # Додаткова інформація для користувача
            result["user_message"] = "✅ DEV_PLAN.md успішно оновлено та розширено"
        else:
            result["user_message"] = "❌ Помилка оновлення DEV_PLAN.md"

        return result

    def _handle_execute_task(self, task_number: int) -> Dict[str, Any]:
        """Обробка команди виконання конкретної задачі"""
        self.logger.info(f"Виконання задачі #{task_number}")

        # Перевірка існування задачі
        plan_status = self.agent.dev_plan_manager.get_plan_status()

        if task_number > plan_status["total_tasks"] or task_number <= 0:
            return {
                "success": False,
                "message": f"Задача #{task_number} не існує. Доступно {plan_status['total_tasks']} задач",
                "user_message": f"❌ Задача #{task_number} не знайдена"
            }

        result = self.agent.execute_dev_plan(task_number=task_number)

        if result["success"]:
            result["user_message"] = f"✅ Задача #{task_number} успішно виконана"
        else:
            result["user_message"] = f"❌ Помилка виконання задачі #{task_number}"

        return result

    def _handle_execute_full_plan(self) -> Dict[str, Any]:
        """Обробка команди виконання всього плану"""
        self.logger.info("Виконання повного DEV_PLAN.md")

        # Попередження користувача
        plan_status = self.agent.dev_plan_manager.get_plan_status()

        if plan_status["total_tasks"] == 0:
            return {
                "success": False,
                "message": "DEV_PLAN.md порожній або не містить задач",
                "user_message": "❌ Немає задач для виконання"
            }

        # Створення резервної копії перед виконанням
        backup_result = self.agent.git_manager.create_backup_branch()

        if not backup_result["success"]:
            self.logger.warning("Не вдалося створити резервну копію")

        # Виконання плану
        result = self.agent.execute_dev_plan()

        if result["success"]:
            executed_count = len(result.get("executed_tasks", []))
            total_count = result.get("total_tasks", 0)
            result["user_message"] = f"✅ План виконано: {executed_count}/{total_count} задач"
        else:
            result["user_message"] = "❌ Помилка виконання плану розробки"

        result["backup_created"] = backup_result["success"]

        return result

    def _handle_status(self) -> Dict[str, Any]:
        """Обробка команди статусу"""
        self.logger.info("Отримання статусу агента")

        try:
            status = self.agent.get_status()

            # Форматування статусу для користувача
            plan_status = status["dev_plan"]
            git_status = status["git"]

            status_message = f"""
📊 **Статус NIMDA Agent**

🎯 **План розробки:**
- Прогрес: {plan_status['completed_subtasks']}/{plan_status['total_subtasks']} підзадач ({plan_status['progress_percentage']}%)
- Виконано задач: {plan_status['completed_tasks']}/{plan_status['total_tasks']}

🔧 **Git репозиторій:**
- Поточна гілка: {git_status.get('current_branch', 'невідома')}
- Локальні зміни: {'Так' if git_status.get('has_changes') else 'Ні'}
- Файлів змінено: {git_status.get('total_files', 0)}

🤖 **Агент:**
- Статус: {'Працює' if status['agent_running'] else 'Простоює'}
- Поточна задача: {status.get('current_task') or 'Немає'}
- Проект: {status['project_path']}
"""

            return {
                "success": True,
                "message": "Статус отримано",
                "user_message": status_message.strip(),
                "raw_status": status
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Помилка отримання статусу",
                "user_message": "❌ Помилка отримання статусу"
            }

    def _handle_sync(self) -> Dict[str, Any]:
        """Обробка команди синхронізації"""
        self.logger.info("Виконання синхронізації з Git")

        result = self.agent.git_manager.sync_with_remote()

        if result["success"]:
            operations = result.get("operations", [])
            operations_summary = ", ".join([op[0] for op in operations if op[1]["success"]])
            result["user_message"] = f"✅ Синхронізація завершена: {operations_summary}"
        else:
            result["user_message"] = "❌ Помилка синхронізації з віддаленим репозиторієм"

        return result

    def _handle_fix_errors(self) -> Dict[str, Any]:
        """Обробка команди виправлення помилок"""
        self.logger.info("Виконання автоматичного виправлення помилок")

        result = self.agent.auto_fix_errors()

        if result["success"]:
            fixed_count = result.get("fixed_count", 0)
            total_errors = result.get("total_errors", 0)
            result["user_message"] = f"✅ Виправлено {fixed_count} з {total_errors} помилок"
        else:
            result["user_message"] = "❌ Помилка автоматичного виправлення"

        return result

    def _handle_initialize(self) -> Dict[str, Any]:
        """Обробка команди ініціалізації"""
        self.logger.info("Виконання ініціалізації проекту")

        result = self.agent.initialize_project()

        if result:
            return {
                "success": True,
                "message": "Проект ініціалізовано",
                "user_message": "✅ Проект успішно ініціалізовано"
            }
        else:
            return {
                "success": False,
                "message": "Помилка ініціалізації проекту",
                "user_message": "❌ Помилка ініціалізації проекту"
            }

    def _handle_help(self) -> Dict[str, Any]:
        """Обробка команди допомоги"""
        help_message = """
🤖 **NIMDA Agent - Доступні команди:**

📋 **Робота з планом:**
- `допрацюй девплан` - оновити та розширити DEV_PLAN.md
- `виконай задачу номер X` - виконати конкретну задачу
- `виконай весь ДЕВ` - виконати весь план повністю

📊 **Статус та інформація:**
- `статус` - поточний статус агента та прогрес
- `допомога` - показати цю довідку

🔧 **Git та синхронізація:**
- `синхронізація` - синхронізація з віддаленим репозиторієм
- `виправити помилки` - автоматичне виправлення помилок

🚀 **Ініціалізація:**
- `ініціалізація` - створити базову структуру проекту

💡 **Приклади використання:**
- "допрацюй девплан і додай нові задачі"
- "виконай задачу номер 3"
- "виконай весь ДЕВ план від початку до кінця"
- "покажи статус виконання"
"""

        return {
            "success": True,
            "message": "Довідка відображена",
            "user_message": help_message.strip()
        }

    def _handle_unknown_command(self, command: str) -> Dict[str, Any]:
        """Обробка невідомої команди"""
        self.logger.warning(f"Невідома команда: {command}")

        # Спроба знайти схожі команди
        suggestions = self._suggest_commands(command)

        suggestion_text = ""
        if suggestions:
            suggestion_text = f"\n\n💡 **Можливо ви мали на увазі:**\n" + "\n".join(f"- {s}" for s in suggestions)

        return {
            "success": False,
            "message": f"Невідома команда: {command}",
            "user_message": f"❓ Не розумію команду '{command}'{suggestion_text}\n\nНапишіть 'допомога' для списку доступних команд."
        }

    def _suggest_commands(self, command: str) -> List[str]:
        """Пропозиція схожих команд"""
        suggestions = []
        command_lower = command.lower()

        # Простий аналіз ключових слів
        if any(word in command_lower for word in ["план", "dev", "розробка"]):
            suggestions.extend(["допрацюй девплан", "виконай весь ДЕВ"])

        if any(word in command_lower for word in ["задач", "task", "номер"]):
            suggestions.append("виконай задачу номер X")

        if any(word in command_lower for word in ["статус", "стан", "status"]):
            suggestions.append("статус")

        if any(word in command_lower for word in ["git", "синхрон", "sync"]):
            suggestions.append("синхронізація")

        if any(word in command_lower for word in ["помилк", "error", "fix"]):
            suggestions.append("виправити помилки")

        return suggestions[:3]  # Максимум 3 пропозиції
