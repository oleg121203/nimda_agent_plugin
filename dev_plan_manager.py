"""
DEV_PLAN.md manager - reading, analyzing and executing development plan
"""

import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class DevPlanManager:
    """
    Manager for working with DEV_PLAN.md file

    Functions:
    - Reading and parsing DEV_PLAN.md
    - Task execution according to plan
    - Progress tracking
    - Plan extension when needed
    """

    def __init__(self, project_path: Path, max_retries: int = 3):
        """
        Initialize manager

        Args:
            project_path: Path to project
        """
        self.project_path = project_path
        self.max_retries = max(1, max_retries)
        self.dev_plan_file = project_path / "DEV_PLAN.md"
        self.logger = logging.getLogger("DevPlanManager")

        # Plan structure
        self.plan_structure = {
            "title": "",
            "description": "",
            "tasks": [],
            "completed_tasks": [],
            "metadata": {},
        }

        # Load plan
        self._load_plan()

    def _load_plan(self):
        """Loading plan з file DEV_PLAN.md"""
        if not self.dev_plan_file.exists():
            self.logger.warning("DEV_PLAN.md not found. Створюю шаблон.")
            self._create_template()
            return

        try:
            with open(self.dev_plan_file, "r", encoding="utf-8") as f:
                content = f.read()

            self.plan_structure = self._parse_plan(content)
            self.logger.info(
                f"DEV_PLAN.md завантажено. Знайдено {len(self.plan_structure['tasks'])} задач."
            )

        except Exception as e:
            self.logger.error(f"Error Loading DEV_PLAN.md: {e}")
            self._create_template()

    def _create_template(self):
        """Creating шаблону DEV_PLAN.md"""
        template = """# plan development project

## Опис project
Опишіть тут ваш project та його цілі.

## Головні task

### 1. initialization project
- [ ] Creating базової структури
- [ ] configuration середовища development
- [ ] Creating документації

### 2. development основної функціональності
- [ ] Реалізація ключових функцій
- [ ] Написання тестів
- [ ] Оптимізація продуктивності

### 3. testing та деплой
- [ ] Комплексне testing
- [ ] Виправлення помилок
- [ ] Підготовка до релізу

## Метадані
- **Створено**: {date}
- **status**: В процесі
- **Пріоритет**: Високий
""".format(date=datetime.now().strftime("%Y-%m-%d"))

        try:
            with open(self.dev_plan_file, "w", encoding="utf-8") as f:
                f.write(template)

            self.logger.info("Створено шаблон DEV_PLAN.md")
            self._load_plan()

        except Exception as e:
            self.logger.error(f"Error Creating шаблону: {e}")

    def _parse_plan(self, content: str) -> Dict[str, Any]:
        """
        Парсинг вмісту DEV_PLAN.md

        Args:
            content: Вміст file

        Returns:
            Структурована інформація про plan
        """
        plan = {
            "title": "",
            "description": "",
            "tasks": [],
            "completed_tasks": [],
            "metadata": {},
        }

        lines = content.split("\n")
        current_section = None
        current_task = None
        task_counter = 0

        for line in lines:
            line = line.strip()

            # Заголовок документа
            if line.startswith("# "):
                plan["title"] = line[2:].strip()
                continue

            # Розділи
            if line.startswith("## "):
                current_section = line[3:].strip().lower()
                continue

            # task (заголовки з номерами)
            task_match = re.match(r"^### (\d+)\.\s*(.*)", line)
            if task_match:
                task_counter += 1
                current_task = {
                    "id": task_counter,
                    "number": int(task_match.group(1)),
                    "title": task_match.group(2),
                    "subtasks": [],
                    "completed": False,
                    "priority": "medium",
                }
                plan["tasks"].append(current_task)
                continue

            # Підзадачі (чекбокси)
            subtask_match = re.match(r"^- \[([ x])\]\s*(.*)", line)
            if subtask_match and current_task:
                completed = subtask_match.group(1) == "x"
                subtask = {
                    "text": subtask_match.group(2),
                    "completed": completed,
                    "id": len(current_task["subtasks"]) + 1,
                }
                current_task["subtasks"].append(subtask)

                # Якщо всі підзадачі виконані - позначити задачу як виконану
                if all(st["completed"] for st in current_task["subtasks"]):
                    current_task["completed"] = True

                continue

            # Опис project
            if current_section == "опис project" and line:
                plan["description"] += line + " "

        # cleanup опису
        plan["description"] = plan["description"].strip()

        # Підрахунок виконаних задач
        plan["completed_tasks"] = [task for task in plan["tasks"] if task["completed"]]

        return plan

    def get_plan_status(self) -> Dict[str, Any]:
        """
        Receiving статусу execution plan

        Returns:
            status plan
        """
        total_tasks = len(self.plan_structure["tasks"])
        completed_tasks = len(self.plan_structure["completed_tasks"])

        total_subtasks = sum(
            len(task["subtasks"]) for task in self.plan_structure["tasks"]
        )
        completed_subtasks = sum(
            len([st for st in task["subtasks"] if st["completed"]])
            for task in self.plan_structure["tasks"]
        )

        progress_percentage = (
            (completed_subtasks / total_subtasks * 100) if total_subtasks > 0 else 0
        )

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
            ).isoformat()
            if self.dev_plan_file.exists()
            else None,
        }

    def execute_task(self, task_number: int) -> Dict[str, Any]:
        """
        execution конкретної task з plan

        Args:
            task_number: Номер task для execution

        Returns:
            Результат execution
        """
        try:
            # search task
            target_task = None
            for task in self.plan_structure["tasks"]:
                if task["number"] == task_number:
                    target_task = task
                    break

            if not target_task:
                return {
                    "success": False,
                    "message": f"Задачу #{task_number} not found в плані",
                }

            if target_task["completed"]:
                return {
                    "success": True,
                    "message": f"task #{task_number} вже виконана",
                    "task": target_task,
                }

            self.logger.info(f"execution task #{task_number}: {target_task['title']}")

            # execution підзадач з повторами
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
                                f"Повтор {attempts} для підзадачі: {subtask['text']}"
                            )

                if not subtask["completed"]:
                    failed_subtasks.append(subtask)

            # Перевірка завершення task
            if all(st["completed"] for st in target_task["subtasks"]):
                target_task["completed"] = True
                if target_task not in self.plan_structure["completed_tasks"]:
                    self.plan_structure["completed_tasks"].append(target_task)

            # Saving оновленого plan
            self._save_plan()

            task_success = len(failed_subtasks) == 0

            return {
                "success": task_success,
                "message": (
                    f"task #{task_number} Successfully виконана"
                    if task_success
                    else f"Не executed {len(failed_subtasks)} підзадач"
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
                "message": f"Error executing task #{task_number}",
            }

    def execute_full_plan(self) -> Dict[str, Any]:
        """
        execution повного plan development

        Returns:
            Результат execution всього plan
        """
        try:
            self.logger.info("Початок execution повного DEV_PLAN.md")

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
                        failed_tasks.append(
                            {
                                "task": task,
                                "error": result.get("error", "Невідома Error"),
                            }
                        )
                        if result.get("executed_subtasks") or result.get(
                            "failed_subtasks"
                        ):
                            progress = True

                if all(t["completed"] for t in self.plan_structure["tasks"]):
                    break

                attempt += 1
                if not progress or attempt >= self.max_retries:
                    break

            success = all(t["completed"] for t in self.plan_structure["tasks"])

            return {
                "success": success,
                "message": f"executed {len([t for t in self.plan_structure['tasks'] if t['completed']])}/{len(self.plan_structure['tasks'])} задач",
                "executed_tasks": executed_tasks,
                "failed_tasks": failed_tasks,
                "total_tasks": len(self.plan_structure["tasks"]),
            }

        except Exception as e:
            self.logger.error(f"critical Error execution plan: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "critical Error execution plan",
            }

    def _execute_subtask(
        self, subtask: Dict[str, Any], parent_task: Dict[str, Any]
    ) -> bool:
        """
        execution конкретної підзадачі

        Args:
            subtask: Підзадача для execution
            parent_task: Батьківська task

        Returns:
            True якщо підзадача виконана Successfully
        """
        try:
            self.logger.info(f"execution підзадачі: {subtask['text']}")

            # Тут буде логіка execution конкретних підзадач
            # На основі тексту підзадачі визначати що саме потрібно зробити

            subtask_text = subtask["text"].lower()

            # Creating files
            if "Creating" in subtask_text or "create" in subtask_text:
                return self._handle_file_creation(subtask_text)

            # configuration
            elif "configuration" in subtask_text or "setup" in subtask_text:
                return self._handle_setup(subtask_text)

            # development
            elif "development" in subtask_text or "implement" in subtask_text:
                return self._handle_implementation(subtask_text)

            # testing
            elif "тест" in subtask_text or "test" in subtask_text:
                return self._handle_testing(subtask_text)

            # documentation
            elif "documentation" in subtask_text or "documentation" in subtask_text:
                return self._handle_documentation(subtask_text)

            # За замовчуванням вважаємо виконаним
            else:
                self.logger.info(f"Підзадача '{subtask['text']}' позначена як виконана")
                return True

        except Exception as e:
            self.logger.error(f"Error execution підзадачі: {e}")
            return False

    def _handle_file_creation(self, task_text: str) -> bool:
        """processing задач Creating files"""
        # Логіка Creating files
        self.logger.info(f"Creating files для: {task_text}")
        return True

    def _handle_setup(self, task_text: str) -> bool:
        """processing задач configuration"""
        # Логіка configuration
        self.logger.info(f"configuration для: {task_text}")
        return True

    def _handle_implementation(self, task_text: str) -> bool:
        """processing задач development"""
        # Логіка реалізації
        self.logger.info(f"Реалізація для: {task_text}")
        return True

    def _handle_testing(self, task_text: str) -> bool:
        """processing задач testing"""
        # Логіка testing
        self.logger.info(f"testing для: {task_text}")
        return True

    def _handle_documentation(self, task_text: str) -> bool:
        """processing задач документації"""
        # Логіка документації
        self.logger.info(f"documentation для: {task_text}")
        return True

    def update_and_expand_plan(self) -> Dict[str, Any]:
        """
        Updating та розширення plan development

        Returns:
            Результат Updating
        """
        try:
            self.logger.info("Аналіз та розширення DEV_PLAN.md")

            # Аналіз поточного стану project
            current_files = list(self.project_path.glob("**/*"))

            # Визначення що потрібно додати до plan
            suggestions = self._analyze_project_and_suggest_tasks(current_files)

            # Додавання нових задач до plan
            added_tasks = []
            for suggestion in suggestions:
                if self._should_add_task(suggestion):
                    new_task = self._create_task_from_suggestion(suggestion)
                    self.plan_structure["tasks"].append(new_task)
                    added_tasks.append(new_task)

            # Saving оновленого plan
            if added_tasks:
                self._save_plan()

            return {
                "success": True,
                "message": f"Plan expanded by {len(added_tasks)} нових задач",
                "added_tasks": added_tasks,
                "suggestions": suggestions,
            }

        except Exception as e:
            self.logger.error(f"Error updating plan: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Error updating plan development",
            }

    def _analyze_project_and_suggest_tasks(
        self, files: List[Path]
    ) -> List[Dict[str, Any]]:
        """Аналіз project та пропозиції нових задач"""
        suggestions = []

        # Аналіз файлової структури
        has_tests = any("test" in str(f).lower() for f in files)
        has_docs = any("doc" in str(f).lower() or f.suffix == ".md" for f in files)
        has_config = any("config" in str(f).lower() for f in files)

        if not has_tests:
            suggestions.append(
                {
                    "type": "testing",
                    "title": "Creating system testing",
                    "description": "Відсутня system testing project",
                    "priority": "high",
                }
            )

        if not has_docs:
            suggestions.append(
                {
                    "type": "documentation",
                    "title": "Creating документації",
                    "description": "Відсутня детальна documentation project",
                    "priority": "medium",
                }
            )

        if not has_config:
            suggestions.append(
                {
                    "type": "configuration",
                    "title": "configuration конфігурації",
                    "description": "Відсутні конфігураційні files",
                    "priority": "medium",
                }
            )

        return suggestions

    def _should_add_task(self, suggestion: Dict[str, Any]) -> bool:
        """Перевірка чи потрібно додавати задачу до plan"""
        # Перевіряємо чи немає вже схожої task
        suggestion_keywords = suggestion["title"].lower().split()

        for task in self.plan_structure["tasks"]:
            task_keywords = task["title"].lower().split()
            common_words = set(suggestion_keywords) & set(task_keywords)

            if len(common_words) >= 2:  # Якщо є 2+ спільних слова - task вже існує
                return False

        return True

    def _create_task_from_suggestion(
        self, suggestion: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Creating нової task на основі пропозиції"""
        task_id = len(self.plan_structure["tasks"]) + 1

        # Базові підзадачі залежно від типу
        subtasks = []

        if suggestion["type"] == "testing":
            subtasks = [
                {"text": "Creating структури тестів", "completed": False, "id": 1},
                {"text": "Написання unit тестів", "completed": False, "id": 2},
                {"text": "Написання integration тестів", "completed": False, "id": 3},
                {"text": "configuration CI/CD", "completed": False, "id": 4},
            ]
        elif suggestion["type"] == "documentation":
            subtasks = [
                {"text": "Creating README.md", "completed": False, "id": 1},
                {"text": "documentation API", "completed": False, "id": 2},
                {
                    "text": "Creating інструкцій користувача",
                    "completed": False,
                    "id": 3,
                },
            ]
        elif suggestion["type"] == "configuration":
            subtasks = [
                {"text": "Creating config files", "completed": False, "id": 1},
                {"text": "configuration environment", "completed": False, "id": 2},
                {"text": "Creating .gitignore", "completed": False, "id": 3},
            ]

        return {
            "id": task_id,
            "number": task_id,
            "title": suggestion["title"],
            "subtasks": subtasks,
            "completed": False,
            "priority": suggestion.get("priority", "medium"),
            "auto_generated": True,
            "created_at": datetime.now().isoformat(),
        }

    def _save_plan(self):
        """Saving оновленого plan в file"""
        try:
            content = self._generate_plan_content()

            with open(self.dev_plan_file, "w", encoding="utf-8") as f:
                f.write(content)

            self.logger.info("DEV_PLAN.md Successfully збережено")

        except Exception as e:
            self.logger.error(f"Error Saving plan: {e}")

    def _generate_plan_content(self) -> str:
        """Генерація вмісту file DEV_PLAN.md"""
        content = []

        # Заголовок
        content.append(f"# {self.plan_structure['title']}")
        content.append("")

        # Опис
        if self.plan_structure["description"]:
            content.append("## Опис project")
            content.append(self.plan_structure["description"])
            content.append("")

        # task
        content.append("## Головні task")
        content.append("")

        for task in self.plan_structure["tasks"]:
            # Заголовок task
            content.append(f"### {task['number']}. {task['title']}")

            # Підзадачі
            for subtask in task["subtasks"]:
                status = "x" if subtask["completed"] else " "
                content.append(f"- [{status}] {subtask['text']}")

            content.append("")

        # Метадані
        status = self.get_plan_status()
        content.append("## Метадані")
        content.append(
            f"- **Прогрес**: {status['completed_subtasks']}/{status['total_subtasks']} підзадач ({status['progress_percentage']}%)"
        )
        content.append(
            f"- **Останнє Updating**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        content.append("")

        return "\n".join(content)

    def create_project_from_plan(self) -> Dict[str, Any]:
        """
        Create new project based on DEV_PLAN specifications

        Returns:
            Result of project creation
        """
        try:
            # Parse DEV_PLAN to extract project requirements
            plan_content = self._load_plan_content()
            project_info = self._extract_project_info(plan_content)

            # Create project directory according to plan
            if project_info.get("project_location"):
                project_path = Path(project_info["project_location"]).expanduser()
                self.logger.info(f"Creating project at: {project_path}")

                # Create project directory
                project_path.mkdir(parents=True, exist_ok=True)

                # Initialize project structure
                self._setup_project_structure(project_path, project_info)

                # Copy DEV_PLAN to new project
                new_dev_plan = project_path / "DEV_PLAN.md"
                if self.dev_plan_file.exists():
                    import shutil

                    shutil.copy2(self.dev_plan_file, new_dev_plan)

                # Update project path to new location
                self.project_path = project_path
                self.dev_plan_file = new_dev_plan

                return {
                    "success": True,
                    "message": f"Project created at {project_path}",
                    "project_path": str(project_path),
                }
            else:
                # Use current directory if no specific location specified
                return self.execute_full_plan()

        except Exception as e:
            self.logger.error(f"Failed to create project from plan: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create project from DEV_PLAN",
            }

    def _load_plan_content(self) -> str:
        """Load DEV_PLAN content"""
        if self.dev_plan_file.exists():
            with open(self.dev_plan_file, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def _extract_project_info(self, content: str) -> Dict[str, Any]:
        """Extract project information from DEV_PLAN"""
        import re

        info = {}

        # Extract project location
        location_match = re.search(r"\*\*Project Location:\*\*\s*`([^`]+)`", content)
        if location_match:
            info["project_location"] = location_match.group(1)

        # Extract tech stack
        tech_match = re.search(r"\*\*Tech Stack:\*\*\s*([^\n]+)", content)
        if tech_match:
            info["tech_stack"] = tech_match.group(1)

        # Extract target platform
        platform_match = re.search(r"\*\*Target Platform:\*\*\s*([^\n]+)", content)
        if platform_match:
            info["platform"] = platform_match.group(1)

        return info

    def _setup_project_structure(
        self, project_path: Path, project_info: Dict[str, Any]
    ):
        """Setup initial project structure"""
        try:
            # Create basic directories
            directories = [
                "src",
                "tests",
                "docs",
                "configs",
                "data",
                "logs",
                ".github/workflows",
            ]

            for dir_name in directories:
                (project_path / dir_name).mkdir(parents=True, exist_ok=True)

            # Create .gitignore
            gitignore_content = """# Python
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

# Config files with secrets
.env
*.secret

# Project specific
nimda_logs/
data/
"""

            with open(project_path / ".gitignore", "w", encoding="utf-8") as f:
                f.write(gitignore_content)

            # Initialize git repository
            import subprocess

            try:
                subprocess.run(
                    ["git", "init"],
                    cwd=project_path,
                    check=True,
                    capture_output=True,
                )
                self.logger.info("Git repository initialized")
            except subprocess.CalledProcessError as e:
                self.logger.warning(f"Failed to initialize git: {e}")

            # Create README.md
            readme_content = f"""# {project_info.get("project_name", "New Project")}

Created by NIMDA Agent on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Tech Stack
{project_info.get("tech_stack", "Not specified")}

## Platform
{project_info.get("platform", "Not specified")}

## Development
See DEV_PLAN.md for detailed development plan.
"""

            with open(project_path / "README.md", "w", encoding="utf-8") as f:
                f.write(readme_content)

        except Exception as e:
            self.logger.error(f"Failed to setup project structure: {e}")
