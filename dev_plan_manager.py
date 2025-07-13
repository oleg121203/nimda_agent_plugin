"""DEV_PLAN.md manager - reading, parsing and executing the development plan"""

import re
import os
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
import logging


class DevPlanManager:
    """Manager for handling DEV_PLAN.md

    Features:
    - Read and parse DEV_PLAN.md
    - Execute tasks from the plan
    - Track progress
    - Expand the plan when needed
    """

    def __init__(self, project_path: Path, max_retries: int = 3):
        """Initialize the manager

        Args:
            project_path: Path to the project
        """
        self.project_path = project_path
        self.max_retries = max(1, max_retries)
        self.dev_plan_file = project_path / "DEV_PLAN.md"
        self.logger = logging.getLogger('DevPlanManager')

        # Структура плану
        self.plan_structure = {
            "title": "",
            "description": "",
            "tasks": [],
            "completed_tasks": [],
            "metadata": {}
        }

        # Завантаження плану
        self._load_plan()

    def _load_plan(self):
        """Завантаження плану з файлу DEV_PLAN.md"""
        if not self.dev_plan_file.exists():
            self.logger.warning("DEV_PLAN.md not found. Creating template.")
            self._create_template()
            return

        try:
            with open(self.dev_plan_file, 'r', encoding='utf-8') as f:
                content = f.read()

            self.plan_structure = self._parse_plan(content)
            self.logger.info(f"DEV_PLAN.md loaded. Found {len(self.plan_structure['tasks'])} tasks.")

        except Exception as e:
            self.logger.error(f"Error loading DEV_PLAN.md: {e}")
            self._create_template()

    def _create_template(self):
        """Create a DEV_PLAN.md template"""
        template = """# Project Development Plan

## Project Description
Describe your project and its goals here.

## Main Tasks

### 1. Project initialization
- [ ] Create basic structure
- [ ] Configure development environment
- [ ] Create documentation

### 2. Core functionality development
- [ ] Implement key features
- [ ] Write tests
- [ ] Optimize performance

### 3. Testing and deployment
- [ ] Comprehensive testing
- [ ] Fix bugs
- [ ] Prepare for release

## Metadata
- **Created**: {date}
- **Status**: In progress
- **Priority**: High
""".format(date=datetime.now().strftime('%Y-%m-%d'))

        try:
            with open(self.dev_plan_file, 'w', encoding='utf-8') as f:
                f.write(template)

            self.logger.info("DEV_PLAN.md template created")
            self._load_plan()

        except Exception as e:
            self.logger.error(f"Error creating template: {e}")

    def _parse_plan(self, content: str) -> Dict[str, Any]:
        """
        Parse the contents of DEV_PLAN.md

        Args:
            content: File contents

        Returns:
            Structured plan information
        """
        plan = {
            "title": "",
            "description": "",
            "tasks": [],
            "completed_tasks": [],
            "metadata": {}
        }

        lines = content.split('\n')
        current_section = None
        current_task = None
        task_counter = 0

        for line in lines:
            line = line.strip()

            # Заголовок документа
            if line.startswith('# '):
                plan["title"] = line[2:].strip()
                continue

            # Розділи
            if line.startswith('## '):
                current_section = line[3:].strip().lower()
                continue

            # Задачі (заголовки з номерами)
            task_match = re.match(r'^### (\d+)\.\s*(.*)', line)
            if task_match:
                task_counter += 1
                current_task = {
                    "id": task_counter,
                    "number": int(task_match.group(1)),
                    "title": task_match.group(2),
                    "subtasks": [],
                    "completed": False,
                    "priority": "medium"
                }
                plan["tasks"].append(current_task)
                continue

            # Підзадачі (чекбокси)
            subtask_match = re.match(r'^- \[([ x])\]\s*(.*)', line)
            if subtask_match and current_task:
                completed = subtask_match.group(1) == 'x'
                subtask = {
                    "text": subtask_match.group(2),
                    "completed": completed,
                    "id": len(current_task["subtasks"]) + 1
                }
                current_task["subtasks"].append(subtask)

                # Якщо всі підзадачі виконані - позначити задачу як виконану
                if all(st["completed"] for st in current_task["subtasks"]):
                    current_task["completed"] = True

                continue

            # Опис проекту
            if current_section == "опис проекту" and line:
                plan["description"] += line + " "

        # Очищення опису
        plan["description"] = plan["description"].strip()

        # Підрахунок виконаних задач
        plan["completed_tasks"] = [task for task in plan["tasks"] if task["completed"]]

        return plan

    def get_plan_status(self) -> Dict[str, Any]:
        """
        Отримання статусу виконання плану

        Returns:
            Статус плану
        """
        total_tasks = len(self.plan_structure["tasks"])
        completed_tasks = len(self.plan_structure["completed_tasks"])

        total_subtasks = sum(len(task["subtasks"]) for task in self.plan_structure["tasks"])
        completed_subtasks = sum(
            len([st for st in task["subtasks"] if st["completed"]])
            for task in self.plan_structure["tasks"]
        )

        progress_percentage = (completed_subtasks / total_subtasks * 100) if total_subtasks > 0 else 0

        return {
            "title": self.plan_structure["title"],
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "total_subtasks": total_subtasks,
            "completed_subtasks": completed_subtasks,
            "progress_percentage": round(progress_percentage, 2),
            "file_exists": self.dev_plan_file.exists(),
            "last_modified": datetime.fromtimestamp(
                os.path.getmtime(self.dev_plan_file)
            ).isoformat() if self.dev_plan_file.exists() else None
        }

    def execute_task(self, task_number: int) -> Dict[str, Any]:
        """
        Виконання конкретної задачі з плану

        Args:
            task_number: Номер задачі для виконання

        Returns:
            Результат виконання
        """
        try:
            # Пошук задачі
            target_task = None
            for task in self.plan_structure["tasks"]:
                if task["number"] == task_number:
                    target_task = task
                    break

            if not target_task:
                return {
                    "success": False,
                    "message": f"Task #{task_number} not found in the plan"
                }

            if target_task["completed"]:
                return {
                    "success": True,
                    "message": f"Task #{task_number} already completed",
                    "task": target_task
                }

            self.logger.info(f"Executing task #{task_number}: {target_task['title']}")

            # Виконання підзадач з повторами
            executed_subtasks = []
            failed_subtasks = []
            for subtask in target_task["subtasks"]:
                if subtask["completed"]:
                    continue

                attempts = 0
                while attempts < self.max_retries and not subtask["completed"]:
                    success = self._execute_subtask(subtask, target_task)
                    if success:
                        subtask["completed"] = True
                        executed_subtasks.append(subtask)
                    else:
                        attempts += 1
                        if attempts < self.max_retries:
                            self.logger.warning(
                                f"Retry {attempts} for subtask: {subtask['text']}"
                            )

                if not subtask["completed"]:
                    failed_subtasks.append(subtask)

            # Перевірка завершення задачі
            if all(st["completed"] for st in target_task["subtasks"]):
                target_task["completed"] = True
                if target_task not in self.plan_structure["completed_tasks"]:
                    self.plan_structure["completed_tasks"].append(target_task)

            # Збереження оновленого плану
            self._save_plan()

            task_success = len(failed_subtasks) == 0

            return {
                "success": task_success,
                "message": (
                    f"Task #{task_number} completed successfully"
                    if task_success
                    else f"{len(failed_subtasks)} subtasks not completed"
                ),
                "task": target_task,
                "executed_subtasks": executed_subtasks,
                "failed_subtasks": failed_subtasks,
            }

        except Exception as e:
            self.logger.error(f"Error executing task #{task_number}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Error executing task #{task_number}"
            }

    def execute_full_plan(self) -> Dict[str, Any]:
        """
        Виконання повного плану розробки

        Returns:
            Результат виконання всього плану
        """
        try:
            self.logger.info("Starting full DEV_PLAN.md execution")

            executed_tasks = []
            failed_tasks = []

            attempt = 0
            while True:
                progress = False
                for task in self.plan_structure["tasks"]:
                    if task["completed"]:
                        continue

                    result = self.execute_task(task["number"])

                    if result["success"]:
                        executed_tasks.append(task)
                        progress = True
                    else:
                        failed_tasks.append({
                            "task": task,
                            "error": result.get("error", "Unknown error")
                        })
                        if result.get("executed_subtasks") or result.get("failed_subtasks"):
                            progress = True

                if all(t["completed"] for t in self.plan_structure["tasks"]):
                    break

                attempt += 1
                if not progress or attempt >= self.max_retries:
                    break

            success = all(t["completed"] for t in self.plan_structure["tasks"])

            return {
                "success": success,
                "message": f"Виконано {len([t for t in self.plan_structure['tasks'] if t['completed']])}/{len(self.plan_structure['tasks'])} задач",
                "executed_tasks": executed_tasks,
                "failed_tasks": failed_tasks,
                "total_tasks": len(self.plan_structure["tasks"])
            }

        except Exception as e:
            self.logger.error(f"Critical error executing plan: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Critical error executing plan"
            }

    def _execute_subtask(self, subtask: Dict[str, Any], parent_task: Dict[str, Any]) -> bool:
        """
        Виконання конкретної підзадачі

        Args:
            subtask: Підзадача для виконання
            parent_task: Батьківська задача

        Returns:
            True if the subtask completed successfully
        """
        try:
            self.logger.info(f"Executing subtask: {subtask['text']}")

            # Тут буде логіка виконання конкретних підзадач
            # На основі тексту підзадачі визначати що саме потрібно зробити

            subtask_text = subtask["text"].lower()

            # Створення файлів
            if "створення" in subtask_text or "create" in subtask_text:
                return self._handle_file_creation(subtask_text)

            # Налаштування
            elif "налаштування" in subtask_text or "setup" in subtask_text:
                return self._handle_setup(subtask_text)

            # Розробка
            elif "розробка" in subtask_text or "implement" in subtask_text:
                return self._handle_implementation(subtask_text)

            # Тестування
            elif "тест" in subtask_text or "test" in subtask_text:
                return self._handle_testing(subtask_text)

            # Документація
            elif "документація" in subtask_text or "documentation" in subtask_text:
                return self._handle_documentation(subtask_text)

            # За замовчуванням вважаємо виконаним
            else:
                self.logger.info(f"Subtask '{subtask['text']}' marked as completed")
                return True

        except Exception as e:
            self.logger.error(f"Error executing subtask: {e}")
            return False

    def _handle_file_creation(self, task_text: str) -> bool:
        """Handle file creation tasks"""
        # Логіка створення файлів
        self.logger.info(f"Creating files for: {task_text}")
        return True

    def _handle_setup(self, task_text: str) -> bool:
        """Handle setup tasks"""
        # Логіка налаштування
        self.logger.info(f"Setup for: {task_text}")
        return True

    def _handle_implementation(self, task_text: str) -> bool:
        """Handle implementation tasks"""
        # Логіка реалізації
        self.logger.info(f"Implementation for: {task_text}")
        return True

    def _handle_testing(self, task_text: str) -> bool:
        """Handle testing tasks"""
        # Логіка тестування
        self.logger.info(f"Testing for: {task_text}")
        return True

    def _handle_documentation(self, task_text: str) -> bool:
        """Handle documentation tasks"""
        # Логіка документації
        self.logger.info(f"Documentation for: {task_text}")
        return True

    def update_and_expand_plan(self) -> Dict[str, Any]:
        """
        Update and expand the development plan

        Returns:
            Update result
        """
        try:
            self.logger.info("Analyzing and expanding DEV_PLAN.md")

            # Аналіз поточного стану проекту
            current_files = list(self.project_path.glob("**/*"))

            # Визначення що потрібно додати до плану
            suggestions = self._analyze_project_and_suggest_tasks(current_files)

            # Додавання нових задач до плану
            added_tasks = []
            for suggestion in suggestions:
                if self._should_add_task(suggestion):
                    new_task = self._create_task_from_suggestion(suggestion)
                    self.plan_structure["tasks"].append(new_task)
                    added_tasks.append(new_task)

            # Збереження оновленого плану
            if added_tasks:
                self._save_plan()

            return {
                "success": True,
                "message": f"Plan expanded with {len(added_tasks)} new tasks",
                "added_tasks": added_tasks,
                "suggestions": suggestions
            }

        except Exception as e:
            self.logger.error(f"Error updating plan: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Error updating development plan"
            }

    def _analyze_project_and_suggest_tasks(self, files: List[Path]) -> List[Dict[str, Any]]:
        """Analyze the project and suggest new tasks"""
        suggestions = []

        # Analyze file structure
        has_tests = any("test" in str(f).lower() for f in files)
        has_docs = any("doc" in str(f).lower() or f.suffix == ".md" for f in files)
        has_config = any("config" in str(f).lower() for f in files)

        if not has_tests:
            suggestions.append({
                "type": "testing",
                "title": "Create testing system",
                "description": "Project lacks a testing framework",
                "priority": "high"
            })

        if not has_docs:
            suggestions.append({
                "type": "documentation",
                "title": "Create documentation",
                "description": "No detailed project docs",
                "priority": "medium"
            })

        if not has_config:
            suggestions.append({
                "type": "configuration",
                "title": "Add configuration",
                "description": "Configuration files missing",
                "priority": "medium"
            })

        return suggestions

    def _should_add_task(self, suggestion: Dict[str, Any]) -> bool:
        """Перевірка чи потрібно додавати задачу до плану"""
        # Перевіряємо чи немає вже схожої задачі
        suggestion_keywords = suggestion["title"].lower().split()

        for task in self.plan_structure["tasks"]:
            task_keywords = task["title"].lower().split()
            common_words = set(suggestion_keywords) & set(task_keywords)

            if len(common_words) >= 2:  # Якщо є 2+ спільних слова - задача вже існує
                return False

        return True

    def _create_task_from_suggestion(self, suggestion: Dict[str, Any]) -> Dict[str, Any]:
        """Створення нової задачі на основі пропозиції"""
        task_id = len(self.plan_structure["tasks"]) + 1

        # Базові підзадачі залежно від типу
        subtasks = []

        if suggestion["type"] == "testing":
            subtasks = [
                {"text": "Створення структури тестів", "completed": False, "id": 1},
                {"text": "Написання unit тестів", "completed": False, "id": 2},
                {"text": "Написання integration тестів", "completed": False, "id": 3},
                {"text": "Налаштування CI/CD", "completed": False, "id": 4}
            ]
        elif suggestion["type"] == "documentation":
            subtasks = [
                {"text": "Створення README.md", "completed": False, "id": 1},
                {"text": "Документація API", "completed": False, "id": 2},
                {"text": "Створення інструкцій користувача", "completed": False, "id": 3}
            ]
        elif suggestion["type"] == "configuration":
            subtasks = [
                {"text": "Створення config файлів", "completed": False, "id": 1},
                {"text": "Налаштування environment", "completed": False, "id": 2},
                {"text": "Створення .gitignore", "completed": False, "id": 3}
            ]

        return {
            "id": task_id,
            "number": task_id,
            "title": suggestion["title"],
            "subtasks": subtasks,
            "completed": False,
            "priority": suggestion.get("priority", "medium"),
            "auto_generated": True,
            "created_at": datetime.now().isoformat()
        }

    def _save_plan(self):
        """Збереження оновленого плану в файл"""
        try:
            content = self._generate_plan_content()

            with open(self.dev_plan_file, 'w', encoding='utf-8') as f:
                f.write(content)

            self.logger.info("DEV_PLAN.md успішно збережено")

        except Exception as e:
            self.logger.error(f"Error saving plan: {e}")

    def _generate_plan_content(self) -> str:
        """Генерація вмісту файлу DEV_PLAN.md"""
        content = []

        # Заголовок
        content.append(f"# {self.plan_structure['title']}")
        content.append("")

        # Опис
        if self.plan_structure["description"]:
            content.append("## Опис проекту")
            content.append(self.plan_structure["description"])
            content.append("")

        # Задачі
        content.append("## Головні задачі")
        content.append("")

        for task in self.plan_structure["tasks"]:
            # Заголовок задачі
            content.append(f"### {task['number']}. {task['title']}")

            # Підзадачі
            for subtask in task["subtasks"]:
                status = "x" if subtask["completed"] else " "
                content.append(f"- [{status}] {subtask['text']}")

            content.append("")

        # Metadata
        status = self.get_plan_status()
        content.append("## Metadata")
        content.append(f"- **Progress**: {status['completed_subtasks']}/{status['total_subtasks']} subtasks ({status['progress_percentage']}%)")
        content.append(f"- **Last update**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")

        return "\n".join(content)
