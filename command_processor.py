"""Command processor for NIMDA Agent.

Handles text commands from Codex."""

import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging


class CommandProcessor:
    """Process user commands received via Codex."""

    def __init__(self, agent):
        """Initialize the command processor

        Args:
            agent: Instance of NIMDAAgent
        """
        self.agent = agent
        self.logger = logging.getLogger('CommandProcessor')

        # Command patterns
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
                r"run full dev",
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
            command: User command

        Returns:
            Command result
        """
        try:
            # Command normalization
            normalized_command = command.lower().strip()

            self.logger.info(f"Обробка команди: {command}")

            # Detect command type
            command_type, params = self._identify_command(normalized_command)

            if not command_type:
                return self._handle_unknown_command(command)

            # Execute the command
            return self._execute_command(command_type, params, command)

        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Command processing error",
                "command": command
            }

    def _identify_command(self, command: str) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Визначення типу команди за шаблонами

        Args:
            command: Normalized command string

        Returns:
            Command type and parameters
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
        Execute a specific command

        Args:
            command_type: Command type
            params: Command parameters
            original_command: Original command text

        Returns:
            Execution result
        """
        try:
            self.logger.info(f"Executing command of type: {command_type}")

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
            self.logger.error(f"Command execution error {command_type}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Command execution error {command_type}"
            }

    def _handle_update_plan(self) -> Dict[str, Any]:
        """Handle update plan command"""
        self.logger.info("Running DEV_PLAN.md update")

        result = self.agent.update_dev_plan()

        if result["success"]:
            # Додаткова інформація для користувача
            result["user_message"] = "✅ DEV_PLAN.md updated and expanded"
        else:
            result["user_message"] = "❌ Error updating DEV_PLAN.md"

        return result

    def _handle_execute_task(self, task_number: int) -> Dict[str, Any]:
        """Обробка команди виконання конкретної задачі"""
        self.logger.info(f"Executing task #{task_number}")

        # Перевірка існування задачі
        plan_status = self.agent.dev_plan_manager.get_plan_status()

        if task_number > plan_status["total_tasks"] or task_number <= 0:
            return {
                "success": False,
                "message": f"Task #{task_number} does not exist. {plan_status['total_tasks']} tasks available",
                "user_message": f"❌ Task #{task_number} not found"
            }

        result = self.agent.execute_dev_plan(task_number=task_number)

        if result["success"]:
            result["user_message"] = f"✅ Task #{task_number} completed successfully"
        else:
            result["user_message"] = f"❌ Error executing task #{task_number}"

        return result

    def _handle_execute_full_plan(self) -> Dict[str, Any]:
        """Handle command to execute the full plan"""
        self.logger.info("Executing full DEV_PLAN.md")

        # Попередження користувача
        plan_status = self.agent.dev_plan_manager.get_plan_status()

        if plan_status["total_tasks"] == 0:
            return {
                "success": False,
                "message": "DEV_PLAN.md is empty or has no tasks",
                "user_message": "❌ No tasks to execute"
            }

        # Створення резервної копії перед виконанням
        backup_result = self.agent.git_manager.create_backup_branch()

        if not backup_result["success"]:
            self.logger.warning("Failed to create backup")

        # Виконання плану з повною синхронізацією
        cycle_result = self.agent.run_full_dev_cycle()

        plan_info = cycle_result.get("plan", {})

        if plan_info.get("success"):
            executed_count = len(plan_info.get("executed_tasks", []))
            total_count = plan_info.get("total_tasks", 0)
            cycle_result["user_message"] = (
                f"✅ Plan executed: {executed_count}/{total_count} tasks"
            )
        else:
            cycle_result["user_message"] = "❌ Error executing development plan"

        cycle_result["backup_created"] = backup_result["success"]

        return cycle_result

    def _handle_status(self) -> Dict[str, Any]:
        """Обробка команди статусу"""
        self.logger.info("Отримання статусу агента")

        try:
            status = self.agent.get_status()

            # Форматування статусу для користувача
            plan_status = status["dev_plan"]
            git_status = status["git"]

            status_message = f"""
📊 **NIMDA Agent Status**

🎯 **Development plan:**
- Progress: {plan_status['completed_subtasks']}/{plan_status['total_subtasks']} subtasks ({plan_status['progress_percentage']}%)
- Completed tasks: {plan_status['completed_tasks']}/{plan_status['total_tasks']}

🔧 **Git repository:***
- Current branch: {git_status.get('current_branch', 'unknown')}
- Local changes: {'Yes' if git_status.get('has_changes') else 'No'}
- Files changed: {git_status.get('total_files', 0)}

🤖 **Agent:***
- Status: {'Running' if status['agent_running'] else 'Idle'}
- Current task: {status.get('current_task') or 'None'}
- Project: {status['project_path']}
"""

            return {
                "success": True,
                "message": "Status retrieved",
                "user_message": status_message.strip(),
                "raw_status": status
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error fetching status",
                "user_message": "❌ Error fetching status"
            }

    def _handle_sync(self) -> Dict[str, Any]:
        """Handle sync command"""
        self.logger.info("Performing Git synchronization")

        result = self.agent.git_manager.sync_with_remote()

        if result["success"]:
            operations = result.get("operations", [])
            operations_summary = ", ".join([op[0] for op in operations if op[1]["success"]])
            result["user_message"] = f"✅ Sync complete: {operations_summary}"
        else:
            result["user_message"] = "❌ Error synchronizing with remote repository"

        return result

    def _handle_fix_errors(self) -> Dict[str, Any]:
        """Handle auto-fix errors command"""
        self.logger.info("Running automatic error correction")

        result = self.agent.auto_fix_errors()

        if result["success"]:
            fixed_count = result.get("fixed_count", 0)
            total_errors = result.get("total_errors", 0)
            result["user_message"] = f"✅ Fixed {fixed_count} of {total_errors} errors"
        else:
            result["user_message"] = "❌ Automatic fix failed"

        return result

    def _handle_initialize(self) -> Dict[str, Any]:
        """Обробка команди ініціалізації"""
        self.logger.info("Виконання ініціалізації проекту")

        result = self.agent.initialize_project()

        if result:
            return {
                "success": True,
                "message": "Project initialized",
                "user_message": "✅ Project initialized successfully"
            }
        else:
            return {
                "success": False,
                "message": "Project initialization error",
                "user_message": "❌ Project initialization error"
            }

    def _handle_help(self) -> Dict[str, Any]:
        """Обробка команди допомоги"""
        help_message = """
🤖 **NIMDA Agent - Available commands:**

📋 **Plan management:**
- `update devplan` - update and expand DEV_PLAN.md
- `execute task number X` - run a specific task
- `run full dev` - execute the entire plan

📊 **Status and info:**
- `status` - current agent status
- `help` - show this help

🔧 **Git and sync:**
- `sync` - synchronize with the remote repository
- `fix errors` - automatically fix problems

🚀 **Initialization:**
- `initialize` - create basic project structure

💡 **Usage examples:**
- "update devplan and add new tasks"
- "execute task number 3"
- "run full dev plan from start to finish"
- "show current status"
"""

        return {
            "success": True,
            "message": "Help displayed",
            "user_message": help_message.strip()
        }

    def _handle_unknown_command(self, command: str) -> Dict[str, Any]:
        """Обробка невідомої команди"""
        self.logger.warning(f"Unknown command: {command}")

        # Спроба знайти схожі команди
        suggestions = self._suggest_commands(command)

        suggestion_text = ""
        if suggestions:
            suggestion_text = f"\n\n💡 **Did you mean:**\n" + "\n".join(f"- {s}" for s in suggestions)

        return {
            "success": False,
            "message": f"Unknown command: {command}",
            "user_message": f"❓ Unknown command '{command}'{suggestion_text}\n\nType 'help' to list available commands."
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
