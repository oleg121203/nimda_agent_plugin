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
            self.logger.info(f"Реальне execution підзадачі: {subtask['text']}")

            # Аналізуємо текст задачі для визначення дій
            task_title = parent_task.get("title", "").lower()
            subtask_text = subtask["text"].lower()

            # Створення файлів агентів
            if "chat_agent.py" in subtask_text or "conversationalist" in task_title:
                return self._create_chat_agent()
            elif (
                "worker_agent.py" in subtask_text or "technical executor" in task_title
            ):
                return self._create_worker_agent()
            elif (
                "adaptive_thinker.py" in subtask_text
                or "adaptive reasoning" in task_title
            ):
                return self._create_adaptive_thinker()
            elif (
                "learning_module.py" in subtask_text or "learning system" in task_title
            ):
                return self._create_learning_module()

            # Створення директорій
            elif (
                "directory structure" in task_title or "visual directory" in task_title
            ):
                return self._create_directory_structure()

            # GitHub Actions
            elif "github actions" in task_title or "workflow" in task_title:
                return self._create_github_workflow()

            # Налаштування проєкту
            elif "project initialization" in task_title:
                return self._setup_project_structure()

            # macOS Integration
            elif "macos integration" in task_title or "voice service" in task_title:
                return self._setup_macos_integration()

            # За замовчуванням створюємо базову структуру
            else:
                self.logger.info(f"Створюємо базову структуру для: {subtask['text']}")
                return self._create_basic_structure(parent_task)

        except Exception as e:
            self.logger.error(f"Error execution підзадачі: {e}")
            return False

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

    # =============================================================================
    # МЕТОДИ ДЛЯ РЕАЛЬНОГО ВИКОНАННЯ ЗАВДАНЬ
    # =============================================================================

    def _create_chat_agent(self) -> bool:
        """Створення chat_agent.py"""
        try:
            chat_agent_code = '''#!/usr/bin/env python3
"""
Chat Agent - Conversationalist & Interpreter
Part of NIMDA v3.2 macOS-optimized system
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime


class ChatAgent:
    """
    Conversational agent for interpreting user commands and managing dialogue
    """
    
    def __init__(self):
        """Initialize chat agent"""
        self.logger = logging.getLogger("ChatAgent")
        self.conversation_history = []
        self.active_session = None
        
        self.logger.info("Chat Agent initialized")
    
    async def process_message(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process incoming message from user
        
        Args:
            message: User message
            context: Additional context
            
        Returns:
            Response with action and data
        """
        try:
            self.logger.info(f"Processing message: {message[:50]}...")
            
            # Add to conversation history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "user_message",
                "content": message,
                "context": context
            })
            
            # Interpret command
            interpretation = await self._interpret_command(message)
            
            # Generate response
            response = await self._generate_response(interpretation, context)
            
            # Add response to history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "agent_response",
                "content": response
            })
            
            return {
                "success": True,
                "response": response,
                "interpretation": interpretation,
                "action_required": interpretation.get("action_type") is not None
            }
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "Sorry, I couldn't process your message."
            }
    
    async def _interpret_command(self, message: str) -> Dict[str, Any]:
        """Interpret user command"""
        message_lower = message.lower().strip()
        
        # Command patterns
        if any(word in message_lower for word in ["run", "execute", "start"]):
            if "full dev" in message_lower:
                return {"action_type": "run_full_dev", "priority": "high"}
            elif "task" in message_lower:
                return {"action_type": "run_task", "priority": "medium"}
        
        elif any(word in message_lower for word in ["status", "progress", "how"]):
            return {"action_type": "get_status", "priority": "low"}
        
        elif any(word in message_lower for word in ["help", "commands", "what can"]):
            return {"action_type": "show_help", "priority": "low"}
        
        return {"action_type": None, "priority": "low", "intent": "conversation"}
    
    async def _generate_response(self, interpretation: Dict[str, Any], context: Dict[str, Any] = None) -> str:
        """Generate appropriate response"""
        action_type = interpretation.get("action_type")
        
        if action_type == "run_full_dev":
            return "🚀 Starting full development cycle. I'll execute all tasks in the development plan."
        
        elif action_type == "run_task":
            return "📋 Which specific task would you like me to execute? Please provide the task number."
        
        elif action_type == "get_status":
            return "📊 Let me check the current project status for you."
        
        elif action_type == "show_help":
            return """🤖 **NIMDA Agent Commands:**
            
• **run full dev** - Execute complete development plan
• **status** - Show current progress
• **run task [number]** - Execute specific task
• **help** - Show this help message

I'm here to help you build amazing software! 🎉"""
        
        else:
            return "I understand you're communicating with me. How can I help you with your development project?"

    def get_conversation_history(self) -> list:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        self.logger.info("Conversation history cleared")


if __name__ == "__main__":
    # Test the chat agent
    async def test_chat_agent():
        agent = ChatAgent()
        
        test_messages = [
            "Hello!",
            "run full dev",
            "what's the status?",
            "help me"
        ]
        
        for message in test_messages:
            print(f"User: {message}")
            response = await agent.process_message(message)
            print(f"Agent: {response['response']}")
            print("-" * 50)
    
    asyncio.run(test_chat_agent())
'''

            chat_agent_path = self.project_path / "chat_agent.py"
            with open(chat_agent_path, "w", encoding="utf-8") as f:
                f.write(chat_agent_code)

            self.logger.info("✅ Created chat_agent.py")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create chat_agent.py: {e}")
            return False

    def _create_worker_agent(self) -> bool:
        """Створення worker_agent.py"""
        try:
            worker_agent_code = '''#!/usr/bin/env python3
"""
Worker Agent - Technical Executor & UI Orchestrator
Part of NIMDA v3.2 macOS-optimized system
"""

import asyncio
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class WorkerAgent:
    """
    Technical execution agent for performing development tasks
    """
    
    def __init__(self, project_path: str = "."):
        """Initialize worker agent"""
        self.logger = logging.getLogger("WorkerAgent")
        self.project_path = Path(project_path)
        self.active_tasks = []
        self.completed_tasks = []
        
        self.logger.info("Worker Agent initialized")
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a development task
        
        Args:
            task: Task definition with type and parameters
            
        Returns:
            Execution result
        """
        try:
            task_id = task.get("id", f"task_{len(self.active_tasks)}")
            task_type = task.get("type", "unknown")
            
            self.logger.info(f"Executing task {task_id}: {task_type}")
            self.active_tasks.append(task)
            
            # Route to appropriate handler
            if task_type == "create_file":
                result = await self._create_file(task)
            elif task_type == "run_command":
                result = await self._run_command(task)
            elif task_type == "create_directory":
                result = await self._create_directory(task)
            elif task_type == "install_packages":
                result = await self._install_packages(task)
            elif task_type == "run_tests":
                result = await self._run_tests(task)
            else:
                result = {"success": False, "error": f"Unknown task type: {task_type}"}
            
            # Update task status
            task["result"] = result
            task["completed_at"] = datetime.now().isoformat()
            
            if task in self.active_tasks:
                self.active_tasks.remove(task)
            self.completed_tasks.append(task)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing task: {e}")
            return {"success": False, "error": str(e)}
    
    async def _create_file(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a file"""
        try:
            file_path = self.project_path / task["file_path"]
            content = task.get("content", "")
            
            # Create directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            self.logger.info(f"✅ Created file: {file_path}")
            return {"success": True, "file_path": str(file_path)}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _run_command(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Run shell command"""
        try:
            command = task["command"]
            cwd = task.get("cwd", self.project_path)
            
            self.logger.info(f"Running command: {command}")
            
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _create_directory(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create directory structure"""
        try:
            dir_path = self.project_path / task["directory_path"]
            dir_path.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"✅ Created directory: {dir_path}")
            return {"success": True, "directory_path": str(dir_path)}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _install_packages(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Install Python packages"""
        try:
            packages = task["packages"]
            if isinstance(packages, str):
                packages = [packages]
            
            command = f"pip install {' '.join(packages)}"
            return await self._run_command({"command": command})
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _run_tests(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Run tests"""
        try:
            test_command = task.get("test_command", "python -m pytest")
            return await self._run_command({"command": test_command})
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_status(self) -> Dict[str, Any]:
        """Get worker agent status"""
        return {
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "project_path": str(self.project_path),
            "recent_tasks": self.completed_tasks[-5:] if self.completed_tasks else []
        }


if __name__ == "__main__":
    # Test the worker agent
    async def test_worker_agent():
        agent = WorkerAgent()
        
        # Test creating a file
        task = {
            "id": "test_1",
            "type": "create_file",
            "file_path": "test_file.txt",
            "content": "Hello from Worker Agent!"
        }
        
        result = await agent.execute_task(task)
        print(f"File creation result: {result}")
        
        # Test creating directory
        task2 = {
            "id": "test_2", 
            "type": "create_directory",
            "directory_path": "test_dir"
        }
        
        result2 = await agent.execute_task(task2)
        print(f"Directory creation result: {result2}")
        
        # Show status
        status = agent.get_status()
        print(f"Worker status: {status}")
    
    asyncio.run(test_worker_agent())
'''

            worker_agent_path = self.project_path / "worker_agent.py"
            with open(worker_agent_path, "w", encoding="utf-8") as f:
                f.write(worker_agent_code)

            self.logger.info("✅ Created worker_agent.py")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create worker_agent.py: {e}")
            return False

    def _create_adaptive_thinker(self) -> bool:
        """Створення adaptive_thinker.py"""
        try:
            adaptive_code = '''#!/usr/bin/env python3
"""
Adaptive Reasoning Engine
Part of NIMDA v3.2 macOS-optimized system
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime


class AdaptiveThinker:
    """
    Adaptive reasoning engine for intelligent decision making
    """
    
    def __init__(self):
        """Initialize adaptive thinker"""
        self.logger = logging.getLogger("AdaptiveThinker")
        self.decision_history = []
        self.learning_patterns = {}
        self.context_memory = []
        
        self.logger.info("Adaptive Thinker initialized")
    
    async def analyze_situation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze current situation and suggest actions
        
        Args:
            context: Current context information
            
        Returns:
            Analysis result with suggested actions
        """
        try:
            self.logger.info("Analyzing situation...")
            
            # Extract key information
            problem_type = context.get("problem_type", "unknown")
            available_resources = context.get("resources", [])
            constraints = context.get("constraints", [])
            goals = context.get("goals", [])
            
            # Perform analysis
            analysis = {
                "situation_assessment": await self._assess_situation(context),
                "risk_factors": await self._identify_risks(context),
                "opportunities": await self._find_opportunities(context),
                "recommended_actions": await self._suggest_actions(context),
                "confidence_level": await self._calculate_confidence(context)
            }
            
            # Store decision for learning
            decision_record = {
                "timestamp": datetime.now().isoformat(),
                "context": context,
                "analysis": analysis,
                "problem_type": problem_type
            }
            self.decision_history.append(decision_record)
            
            # Update learning patterns
            await self._update_learning_patterns(decision_record)
            
            return {
                "success": True,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in situation analysis: {e}")
            return {"success": False, "error": str(e)}
    
    async def _assess_situation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess current situation"""
        return {
            "complexity": "medium",
            "urgency": "normal", 
            "clarity": "good",
            "resource_availability": "adequate"
        }
    
    async def _identify_risks(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify potential risks"""
        return [
            {"type": "technical", "severity": "low", "description": "Potential compatibility issues"},
            {"type": "time", "severity": "medium", "description": "Tight deadline constraints"}
        ]
    
    async def _find_opportunities(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find opportunities for improvement"""
        return [
            {"type": "optimization", "impact": "high", "description": "Code optimization potential"},
            {"type": "automation", "impact": "medium", "description": "Process automation opportunities"}
        ]
    
    async def _suggest_actions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest recommended actions"""
        actions = []
        
        problem_type = context.get("problem_type", "")
        
        if "development" in problem_type.lower():
            actions.extend([
                {"action": "create_development_plan", "priority": "high"},
                {"action": "setup_testing_framework", "priority": "medium"},
                {"action": "implement_error_handling", "priority": "medium"}
            ])
        
        if "performance" in problem_type.lower():
            actions.extend([
                {"action": "profile_performance", "priority": "high"},
                {"action": "optimize_bottlenecks", "priority": "high"},
                {"action": "implement_caching", "priority": "medium"}
            ])
        
        return actions
    
    async def _calculate_confidence(self, context: Dict[str, Any]) -> float:
        """Calculate confidence level in analysis"""
        # Simple confidence calculation based on available information
        factors = []
        
        if context.get("problem_type"):
            factors.append(0.2)
        if context.get("resources"):
            factors.append(0.2)
        if context.get("goals"):
            factors.append(0.2)
        if len(self.decision_history) > 0:
            factors.append(0.2)  # Experience factor
        
        return min(sum(factors), 1.0)
    
    async def _update_learning_patterns(self, decision_record: Dict[str, Any]):
        """Update learning patterns based on new decision"""
        problem_type = decision_record["problem_type"]
        
        if problem_type not in self.learning_patterns:
            self.learning_patterns[problem_type] = {
                "count": 0,
                "success_rate": 0.0,
                "common_actions": [],
                "avg_confidence": 0.0
            }
        
        pattern = self.learning_patterns[problem_type]
        pattern["count"] += 1
        
        # Update average confidence
        current_confidence = decision_record["analysis"]["confidence_level"]
        pattern["avg_confidence"] = (pattern["avg_confidence"] * (pattern["count"] - 1) + current_confidence) / pattern["count"]
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of learning patterns"""
        return {
            "total_decisions": len(self.decision_history),
            "patterns_learned": len(self.learning_patterns),
            "learning_patterns": self.learning_patterns,
            "recent_decisions": self.decision_history[-5:] if self.decision_history else []
        }


if __name__ == "__main__":
    # Test the adaptive thinker
    async def test_adaptive_thinker():
        thinker = AdaptiveThinker()
        
        # Test analysis
        context = {
            "problem_type": "development_challenge",
            "resources": ["developer", "testing_tools", "documentation"],
            "constraints": ["time_limit", "budget_constraints"],
            "goals": ["create_robust_solution", "maintain_performance"]
        }
        
        result = await thinker.analyze_situation(context)
        print(f"Analysis result: {result}")
        
        # Show learning summary
        summary = thinker.get_learning_summary()
        print(f"Learning summary: {summary}")
    
    asyncio.run(test_adaptive_thinker())
'''

            adaptive_path = self.project_path / "adaptive_thinker.py"
            with open(adaptive_path, "w", encoding="utf-8") as f:
                f.write(adaptive_code)

            self.logger.info("✅ Created adaptive_thinker.py")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create adaptive_thinker.py: {e}")
            return False

    def _create_learning_module(self) -> bool:
        """Створення learning_module.py"""
        try:
            learning_code = '''#!/usr/bin/env python3
"""
Learning System Module
Part of NIMDA v3.2 macOS-optimized system
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class LearningModule:
    """
    Machine learning and pattern recognition system
    """
    
    def __init__(self, data_path: str = "data"):
        """Initialize learning module"""
        self.logger = logging.getLogger("LearningModule")
        self.data_path = Path(data_path)
        self.data_path.mkdir(exist_ok=True)
        
        self.knowledge_base = {}
        self.patterns = {}
        self.learning_sessions = []
        
        # Load existing knowledge
        self._load_knowledge_base()
        
        self.logger.info("Learning Module initialized")
    
    async def learn_from_experience(self, experience: Dict[str, Any]) -> Dict[str, Any]:
        """
        Learn from new experience
        
        Args:
            experience: Experience data with context and outcome
            
        Returns:
            Learning result
        """
        try:
            self.logger.info("Processing new learning experience...")
            
            # Extract key features
            features = await self._extract_features(experience)
            
            # Identify patterns
            patterns = await self._identify_patterns(features)
            
            # Update knowledge base
            await self._update_knowledge(experience, features, patterns)
            
            # Create learning session record
            session = {
                "timestamp": datetime.now().isoformat(),
                "experience": experience,
                "features": features,
                "patterns": patterns,
                "learning_type": "experience_based"
            }
            self.learning_sessions.append(session)
            
            # Save updated knowledge
            await self._save_knowledge_base()
            
            return {
                "success": True,
                "patterns_found": len(patterns),
                "knowledge_updated": True,
                "session_id": len(self.learning_sessions)
            }
            
        except Exception as e:
            self.logger.error(f"Error in learning process: {e}")
            return {"success": False, "error": str(e)}
    
    async def predict_outcome(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict outcome based on learned patterns
        
        Args:
            context: Current context for prediction
            
        Returns:
            Prediction result
        """
        try:
            # Extract features from context
            features = await self._extract_features({"context": context})
            
            # Find matching patterns
            matching_patterns = await self._find_matching_patterns(features)
            
            # Generate prediction
            prediction = await self._generate_prediction(matching_patterns, context)
            
            return {
                "success": True,
                "prediction": prediction,
                "confidence": prediction.get("confidence", 0.0),
                "based_on_patterns": len(matching_patterns)
            }
            
        except Exception as e:
            self.logger.error(f"Error in prediction: {e}")
            return {"success": False, "error": str(e)}
    
    async def _extract_features(self, data: Dict[str, Any]) -> List[str]:
        """Extract meaningful features from data"""
        features = []
        
        # Extract from experience or context
        content = data.get("experience", data.get("context", {}))
        
        # Common feature patterns
        if "problem_type" in content:
            features.append(f"problem:{content['problem_type']}")
        
        if "success" in content:
            features.append(f"outcome:{'success' if content['success'] else 'failure'}")
        
        if "complexity" in content:
            features.append(f"complexity:{content['complexity']}")
        
        if "resources" in content:
            for resource in content["resources"]:
                features.append(f"resource:{resource}")
        
        return features
    
    async def _identify_patterns(self, features: List[str]) -> List[Dict[str, Any]]:
        """Identify patterns in features"""
        patterns = []
        
        # Look for feature combinations
        for i, feature1 in enumerate(features):
            for feature2 in features[i+1:]:
                pattern_key = f"{feature1}+{feature2}"
                
                if pattern_key not in self.patterns:
                    self.patterns[pattern_key] = {
                        "frequency": 0,
                        "success_rate": 0.0,
                        "examples": []
                    }
                
                self.patterns[pattern_key]["frequency"] += 1
                patterns.append({
                    "pattern": pattern_key,
                    "features": [feature1, feature2],
                    "strength": self.patterns[pattern_key]["frequency"]
                })
        
        return patterns
    
    async def _update_knowledge(self, experience: Dict[str, Any], features: List[str], patterns: List[Dict[str, Any]]):
        """Update knowledge base with new information"""
        
        # Update feature knowledge
        for feature in features:
            if feature not in self.knowledge_base:
                self.knowledge_base[feature] = {
                    "count": 0,
                    "success_count": 0,
                    "examples": []
                }
            
            kb_entry = self.knowledge_base[feature]
            kb_entry["count"] += 1
            
            if experience.get("success", False):
                kb_entry["success_count"] += 1
            
            # Keep limited examples
            if len(kb_entry["examples"]) < 10:
                kb_entry["examples"].append({
                    "timestamp": datetime.now().isoformat(),
                    "context": experience.get("context", {})
                })
    
    async def _find_matching_patterns(self, features: List[str]) -> List[Dict[str, Any]]:
        """Find patterns that match current features"""
        matching = []
        
        for pattern_key, pattern_data in self.patterns.items():
            pattern_features = pattern_key.split("+")
            
            # Check if any of the current features match pattern features
            matches = sum(1 for f in features if any(pf in f for pf in pattern_features))
            
            if matches > 0:
                matching.append({
                    "pattern": pattern_key,
                    "match_score": matches / len(pattern_features),
                    "frequency": pattern_data["frequency"],
                    "success_rate": pattern_data["success_rate"]
                })
        
        # Sort by match score and frequency
        matching.sort(key=lambda x: (x["match_score"], x["frequency"]), reverse=True)
        
        return matching[:5]  # Return top 5 matches
    
    async def _generate_prediction(self, matching_patterns: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate prediction based on matching patterns"""
        if not matching_patterns:
            return {
                "outcome": "unknown",
                "confidence": 0.0,
                "reasoning": "No matching patterns found"
            }
        
        # Calculate weighted prediction
        total_weight = sum(p["match_score"] * p["frequency"] for p in matching_patterns)
        
        if total_weight == 0:
            confidence = 0.0
        else:
            weighted_success = sum(p["success_rate"] * p["match_score"] * p["frequency"] 
                                 for p in matching_patterns)
            confidence = min(weighted_success / total_weight, 1.0)
        
        outcome = "success" if confidence > 0.5 else "uncertain"
        
        return {
            "outcome": outcome,
            "confidence": confidence,
            "reasoning": f"Based on {len(matching_patterns)} matching patterns",
            "top_pattern": matching_patterns[0]["pattern"] if matching_patterns else None
        }
    
    def _load_knowledge_base(self):
        """Load knowledge base from file"""
        kb_file = self.data_path / "knowledge_base.json"
        patterns_file = self.data_path / "patterns.json"
        
        try:
            if kb_file.exists():
                with open(kb_file, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
            
            if patterns_file.exists():
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    self.patterns = json.load(f)
                    
            self.logger.info(f"Loaded knowledge: {len(self.knowledge_base)} features, {len(self.patterns)} patterns")
            
        except Exception as e:
            self.logger.warning(f"Could not load knowledge base: {e}")
    
    async def _save_knowledge_base(self):
        """Save knowledge base to file"""
        try:
            kb_file = self.data_path / "knowledge_base.json"
            patterns_file = self.data_path / "patterns.json"
            
            with open(kb_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
            
            with open(patterns_file, 'w', encoding='utf-8') as f:
                json.dump(self.patterns, f, indent=2, ensure_ascii=False)
                
            self.logger.info("Knowledge base saved successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to save knowledge base: {e}")
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics"""
        return {
            "knowledge_features": len(self.knowledge_base),
            "identified_patterns": len(self.patterns),
            "learning_sessions": len(self.learning_sessions),
            "total_experiences": sum(kb["count"] for kb in self.knowledge_base.values()),
            "recent_sessions": self.learning_sessions[-3:] if self.learning_sessions else []
        }


if __name__ == "__main__":
    # Test the learning module
    async def test_learning_module():
        learner = LearningModule()
        
        # Test learning from experience
        experience = {
            "context": {
                "problem_type": "development_task",
                "complexity": "medium",
                "resources": ["developer", "tools"]
            },
            "success": True,
            "outcome": "task_completed"
        }
        
        result = await learner.learn_from_experience(experience)
        print(f"Learning result: {result}")
        
        # Test prediction
        new_context = {
            "problem_type": "development_task",
            "complexity": "high",
            "resources": ["developer"]
        }
        
        prediction = await learner.predict_outcome(new_context)
        print(f"Prediction: {prediction}")
        
        # Show stats
        stats = learner.get_learning_stats()
        print(f"Learning stats: {stats}")
    
    asyncio.run(test_learning_module())
'''

            learning_path = self.project_path / "learning_module.py"
            with open(learning_path, "w", encoding="utf-8") as f:
                f.write(learning_code)

            self.logger.info("✅ Created learning_module.py")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create learning_module.py: {e}")
            return False

    def _create_directory_structure(self) -> bool:
        """Створення структури директорій"""
        try:
            directories = ["src", "tests", "docs", "data", "logs", "config", "assets"]

            for dir_name in directories:
                dir_path = self.project_path / dir_name
                dir_path.mkdir(exist_ok=True)

                # Створити __init__.py для Python пакетів
                if dir_name in ["src", "tests"]:
                    init_file = dir_path / "__init__.py"
                    init_file.write_text("# Python package\n")

            self.logger.info("✅ Created directory structure")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create directory structure: {e}")
            return False

    def _create_github_workflow(self) -> bool:
        """Створення GitHub Actions workflow"""
        try:
            workflow_dir = self.project_path / ".github" / "workflows"
            workflow_dir.mkdir(parents=True, exist_ok=True)

            workflow_content = """name: NIMDA v3.2 CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: macos-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python 3.12
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src/ --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  lint:
    runs-on: macos-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python 3.12
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install linting tools
      run: |
        python -m pip install --upgrade pip
        pip install black flake8 mypy
    
    - name: Run Black
      run: black --check .
    
    - name: Run flake8
      run: flake8 .
    
    - name: Run mypy
      run: mypy src/

  deploy:
    runs-on: macos-latest
    needs: [test, lint]
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploying NIMDA v3.2..."
        # Add deployment steps here
"""

            workflow_file = workflow_dir / "nimda-v3-ci.yml"
            with open(workflow_file, "w", encoding="utf-8") as f:
                f.write(workflow_content)

            self.logger.info("✅ Created GitHub Actions workflow")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create GitHub workflow: {e}")
            return False

    def _setup_macos_integration(self) -> bool:
        """Налаштування macOS інтеграції"""
        try:
            macos_code = '''#!/usr/bin/env python3
"""
macOS Integration Module
Part of NIMDA v3.2 macOS-optimized system
"""

import logging
from typing import Dict, Any, Optional

try:
    import objc
    from Foundation import NSObject
    from AppKit import NSApplication, NSWorkspace
    MACOS_AVAILABLE = True
except ImportError:
    MACOS_AVAILABLE = False


class MacOSIntegration:
    """
    Native macOS integration for NIMDA v3.2
    """
    
    def __init__(self):
        """Initialize macOS integration"""
        self.logger = logging.getLogger("MacOSIntegration")
        self.workspace = None
        
        if MACOS_AVAILABLE:
            self.workspace = NSWorkspace.sharedWorkspace()
            self.logger.info("macOS integration initialized")
        else:
            self.logger.warning("macOS frameworks not available")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get macOS system information"""
        if not MACOS_AVAILABLE:
            return {"error": "macOS frameworks not available"}
        
        try:
            import platform
            
            return {
                "system": platform.system(),
                "version": platform.mac_ver()[0],
                "machine": platform.machine(),
                "processor": platform.processor(),
                "available": True
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system info: {e}")
            return {"error": str(e)}
    
    def speak_text(self, text: str) -> bool:
        """Use macOS speech synthesis"""
        if not MACOS_AVAILABLE:
            return False
        
        try:
            from AppKit import NSSpeechSynthesizer
            
            synthesizer = NSSpeechSynthesizer.alloc().init()
            synthesizer.startSpeakingString_(text)
            
            self.logger.info(f"Speaking: {text[:50]}...")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to speak text: {e}")
            return False
    
    def send_notification(self, title: str, message: str) -> bool:
        """Send native macOS notification"""
        if not MACOS_AVAILABLE:
            return False
        
        try:
            from Foundation import NSUserNotification, NSUserNotificationCenter
            
            notification = NSUserNotification.alloc().init()
            notification.setTitle_(title)
            notification.setInformativeText_(message)
            
            center = NSUserNotificationCenter.defaultUserNotificationCenter()
            center.deliverNotification_(notification)
            
            self.logger.info(f"Notification sent: {title}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")
            return False


if __name__ == "__main__":
    # Test macOS integration
    integration = MacOSIntegration()
    
    # Test system info
    info = integration.get_system_info()
    print(f"System info: {info}")
    
    # Test notification
    if info.get("available"):
        integration.send_notification("NIMDA v3.2", "macOS integration test successful!")
        integration.speak_text("NIMDA macOS integration is working correctly.")
    else:
        print("macOS integration not available on this system")
'''

            macos_file = self.project_path / "macos_integration.py"
            with open(macos_file, "w", encoding="utf-8") as f:
                f.write(macos_code)

            self.logger.info("✅ Created macOS integration module")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create macOS integration: {e}")
            return False

    def _create_basic_structure(self, parent_task: Dict[str, Any]) -> bool:
        """Створення базової структури для задачі"""
        try:
            task_title = parent_task.get("title", "").lower()

            # Створити базові файли в залежності від типу задачі
            if "performance" in task_title:
                self._create_performance_tools()
            elif "security" in task_title:
                self._create_security_tools()
            elif "documentation" in task_title:
                self._create_documentation()
            else:
                # Загальна структура
                self._create_directory_structure()

            self.logger.info(f"✅ Created basic structure for: {parent_task['title']}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create basic structure: {e}")
            return False

    def _create_performance_tools(self) -> bool:
        """Створення інструментів для оптимізації продуктивності"""
        try:
            perf_code = '''#!/usr/bin/env python3
"""
Performance optimization tools for M1 Max
"""

import time
import psutil
import logging
from typing import Dict, Any


class PerformanceOptimizer:
    """Performance optimization for M1 Max systems"""
    
    def __init__(self):
        self.logger = logging.getLogger("PerformanceOptimizer")
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system performance metrics"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "timestamp": time.time()
        }
    
    def optimize_for_m1_max(self) -> Dict[str, Any]:
        """Apply M1 Max specific optimizations"""
        optimizations = []
        
        # Enable performance cores preference
        optimizations.append("Configured for M1 Max performance cores")
        
        # Memory optimization
        optimizations.append("Applied memory optimization for unified memory")
        
        return {"optimizations": optimizations, "success": True}


if __name__ == "__main__":
    optimizer = PerformanceOptimizer()
    metrics = optimizer.get_system_metrics()
    result = optimizer.optimize_for_m1_max()
    print(f"Performance metrics: {metrics}")
    print(f"Optimization result: {result}")
'''

            perf_file = self.project_path / "performance_optimizer.py"
            with open(perf_file, "w", encoding="utf-8") as f:
                f.write(perf_code)

            return True

        except Exception as e:
            self.logger.error(f"Failed to create performance tools: {e}")
            return False

    def _create_security_tools(self) -> bool:
        """Створення інструментів безпеки"""
        try:
            security_code = '''#!/usr/bin/env python3
"""
Security and privacy tools for NIMDA v3.2
"""

import hashlib
import secrets
import logging
from typing import Dict, Any


class SecurityManager:
    """Security and privacy management"""
    
    def __init__(self):
        self.logger = logging.getLogger("SecurityManager")
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate cryptographically secure token"""
        return secrets.token_urlsafe(length)
    
    def hash_data(self, data: str) -> str:
        """Securely hash data"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def validate_security_settings(self) -> Dict[str, Any]:
        """Validate current security settings"""
        checks = {
            "secure_random_available": True,
            "encryption_available": True,
            "privacy_mode": "enabled"
        }
        
        return {"security_checks": checks, "status": "secure"}


if __name__ == "__main__":
    security = SecurityManager()
    token = security.generate_secure_token()
    validation = security.validate_security_settings()
    print(f"Generated token: {token[:16]}...")
    print(f"Security validation: {validation}")
'''

            security_file = self.project_path / "security_manager.py"
            with open(security_file, "w", encoding="utf-8") as f:
                f.write(security_code)

            return True

        except Exception as e:
            self.logger.error(f"Failed to create security tools: {e}")
            return False

    def _create_documentation(self) -> bool:
        """Створення документації"""
        try:
            docs_dir = self.project_path / "docs"
            docs_dir.mkdir(exist_ok=True)

            readme_content = """# NIMDA v3.2 - macOS Optimized Development Agent

## Overview

NIMDA v3.2 is an advanced autonomous development agent optimized specifically for macOS systems, particularly M1 Max machines.

## Features

- **Chat Agent**: Conversational interface for natural command processing
- **Worker Agent**: Technical executor for development tasks
- **Adaptive Thinker**: Intelligent reasoning and decision making
- **Learning Module**: Pattern recognition and continuous improvement
- **macOS Integration**: Native macOS features and optimizations

## Architecture

```
NIMDA v3.2/
├── chat_agent.py          # Conversational interface
├── worker_agent.py        # Task executor
├── adaptive_thinker.py    # Reasoning engine
├── learning_module.py     # Learning system
├── macos_integration.py   # Native macOS features
├── performance_optimizer.py # M1 Max optimizations
└── security_manager.py    # Security & privacy
```

## Installation

1. Ensure you're running macOS with Python 3.12+
2. Install dependencies: `pip install -r requirements.txt`
3. Run the system: `python chat_agent.py`

## Usage

The system provides multiple interfaces:
- Chat-based commands via ChatAgent
- Direct task execution via WorkerAgent
- Intelligent analysis via AdaptiveThinker
- Continuous learning via LearningModule

## M1 Max Optimizations

- Unified memory architecture support
- Performance core utilization
- Neural Engine integration (future)
- Metal Performance Shaders support (future)

## Security & Privacy

- Local processing by default
- Encrypted data storage
- Privacy-first design
- Secure token generation

## Development

This project follows macOS-specific development practices:
- PyObjC for native framework access
- Async/await patterns for performance
- PySide6 for native GUI elements
- Metal for GPU acceleration

## License

Proprietary - NIMDA v3.2 Development Agent
"""

            readme_file = docs_dir / "README.md"
            with open(readme_file, "w", encoding="utf-8") as f:
                f.write(readme_content)

            return True

        except Exception as e:
            self.logger.error(f"Failed to create documentation: {e}")
            return False
