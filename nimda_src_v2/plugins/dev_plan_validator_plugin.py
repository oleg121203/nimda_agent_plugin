"""
🔍 NIMDA DEV_PLAN Validator Plugin
Автоматична перевірка та корекція відміток у DEV_PLAN.md
"""

import asyncio
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from .base_plugin import BasePlugin, PluginResult


@dataclass
class TaskCheckResult:
    """Результат перевірки завдання"""

    task_name: str
    current_status: bool  # Поточний статус у DEV_PLAN
    actual_status: bool  # Реальний статус на основі коду
    needs_update: bool  # Чи потрібно оновити
    evidence: List[str]  # Докази реалізації
    confidence: float  # Впевненість у результаті (0-100%)


class DevPlanValidatorPlugin(BasePlugin):
    """
    🔍 Плагін валідації DEV_PLAN.md

    Перевіряє кожну задачу у DEV_PLAN.md та порівнює з реально реалізованим кодом.
    Автоматично корегує галочки при необхідності.
    """

    def __init__(self, name: str = "DEV_PLAN Validator", *, workspace_path=None):
        super().__init__(name)
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()
        self.dev_plan_path = self.workspace_path / "DEV_PLAN.md"
        self.plugin_name = "DEV_PLAN Validator"

        # Ключові слова для пошуку реалізації
        self.implementation_keywords = {
            # GUI компоненти
            "glassmorphism": ["glass", "blur", "transparency", "translucent"],
            "neon": ["neon", "glow", "particle", "effect"],
            "dashboard": ["dashboard", "analytics", "chart", "metric"],
            "chat": ["chat", "conversation", "message", "dialogue"],
            # AI функції
            "neural": ["neural", "network", "model", "ai", "ml"],
            "prediction": ["predict", "forecast", "anticipate"],
            "automation": ["automat", "workflow", "trigger"],
            # Безпека
            "encryption": ["encrypt", "decrypt", "cipher", "crypto"],
            "auth": ["auth", "login", "credential", "biometric"],
            # SSH плагін
            "ssh": ["ssh", "secure_shell", "remote", "connection"],
            "mikrotik": ["mikrotik", "routeros", "router"],
            "cisco": ["cisco", "ios", "nexus"],
            # Архітектура
            "plugin": ["plugin", "extension", "module", "component"],
            "api": ["api", "endpoint", "service", "interface"],
            "database": ["database", "db", "storage", "persistence"],
        }

    async def execute_task(self, task: Dict[str, Any]) -> PluginResult:
        """Виконання валідації DEV_PLAN"""
        try:
            self.logger.info("🔍 Початок валідації DEV_PLAN.md...")

            # 1. Парсинг DEV_PLAN.md
            tasks_data = await self._parse_dev_plan()
            if not tasks_data:
                return PluginResult(
                    success=False, message="❌ Не вдалося прочитати DEV_PLAN.md"
                )

            # 2. Аналіз кожної задачі
            validation_results = []
            for task_info in tasks_data:
                result = await self._validate_task(task_info)
                validation_results.append(result)
                await asyncio.sleep(0.01)  # Невелика пауза

            # 3. Підрахунок статистики
            total_tasks = len(validation_results)
            tasks_needing_update = [r for r in validation_results if r.needs_update]
            high_confidence_updates = [
                r for r in tasks_needing_update if r.confidence >= 80
            ]

            # 4. Оновлення DEV_PLAN.md (якщо потрібно)
            updated_count = 0
            if high_confidence_updates:
                updated_count = await self._update_dev_plan(high_confidence_updates)

            # 5. Генерація звіту
            report = self._generate_validation_report(validation_results)

            success = len(tasks_needing_update) == 0 or updated_count > 0

            return PluginResult(
                success=success,
                message=f"✅ Валідація завершена: {updated_count} оновлень з {len(tasks_needing_update)} потрібних",
                data={
                    "total_tasks": total_tasks,
                    "tasks_needing_update": len(tasks_needing_update),
                    "updated_count": updated_count,
                    "validation_results": [r.__dict__ for r in validation_results],
                    "report": report,
                },
            )

        except Exception as e:
            return PluginResult(
                success=False, message=f"❌ Помилка валідації: {e}", error=e
            )

    async def _parse_dev_plan(self) -> List[Dict[str, Any]]:
        """Парсинг DEV_PLAN.md та витягування задач"""
        try:
            if not self.dev_plan_path.exists():
                self.logger.error("DEV_PLAN.md не знайдено")
                return []

            content = self.dev_plan_path.read_text(encoding="utf-8")
            tasks = []

            # Регекс для пошуку задач з чекбоксами
            task_pattern = (
                r"^[\s]*-[\s]*\[([x\s])\][\s]*\*\*([^*]+)\*\*[\s]*-[\s]*(.+)$"
            )

            for line_num, line in enumerate(content.split("\n"), 1):
                match = re.match(task_pattern, line, re.IGNORECASE)
                if match:
                    is_completed = match.group(1).lower() == "x"
                    task_name = match.group(2).strip()
                    description = match.group(3).strip()

                    tasks.append(
                        {
                            "line_number": line_num,
                            "raw_line": line,
                            "is_completed": is_completed,
                            "task_name": task_name,
                            "description": description,
                        }
                    )

            self.logger.info(f"📋 Знайдено {len(tasks)} задач у DEV_PLAN.md")
            return tasks

        except Exception as e:
            self.logger.error(f"Помилка парсингу DEV_PLAN: {e}")
            return []

    async def _validate_task(self, task_info: Dict[str, Any]) -> TaskCheckResult:
        """Валідація окремої задачі"""
        task_name = task_info["task_name"]
        current_status = task_info["is_completed"]

        # Пошук доказів реалізації
        evidence = await self._find_implementation_evidence(
            task_name, task_info["description"]
        )

        # Розрахунок впевненості
        confidence = self._calculate_confidence(evidence, task_name)

        # Визначення реального статусу
        actual_status = confidence >= 70  # Поріг для вважання реалізованим

        # Чи потрібно оновлення
        needs_update = current_status != actual_status

        return TaskCheckResult(
            task_name=task_name,
            current_status=current_status,
            actual_status=actual_status,
            needs_update=needs_update,
            evidence=evidence,
            confidence=confidence,
        )

    async def _find_implementation_evidence(
        self, task_name: str, description: str
    ) -> List[str]:
        """Пошук доказів реалізації задачі в коді"""
        evidence = []

        # Ключові слова для пошуку
        search_terms = self._extract_search_terms(task_name, description)

        # Пошук у Python файлах
        python_files = list(self.workspace_path.glob("**/*.py"))
        for py_file in python_files:
            try:
                content = py_file.read_text(encoding="utf-8").lower()

                for term in search_terms:
                    if term.lower() in content:
                        # Знаходимо контекст
                        lines = content.split("\n")
                        for i, line in enumerate(lines):
                            if term.lower() in line:
                                context = self._get_line_context(lines, i, 2)
                                evidence.append(f"{py_file.name}:{i + 1} - {context}")
                                break

                        if len(evidence) >= 10:  # Обмежуємо кількість доказів
                            break

            except Exception:
                continue

        # Пошук у JS/TS файлах (для GUI)
        js_files = list(self.workspace_path.glob("**/*.js")) + list(
            self.workspace_path.glob("**/*.ts")
        )
        for js_file in js_files:
            try:
                content = js_file.read_text(encoding="utf-8").lower()

                for term in search_terms:
                    if term.lower() in content:
                        evidence.append(f"{js_file.name} - містить '{term}'")
                        if len(evidence) >= 15:
                            break

            except Exception:
                continue

        # Пошук у конфігураційних файлах
        config_files = (
            list(self.workspace_path.glob("**/*.json"))
            + list(self.workspace_path.glob("**/*.yaml"))
            + list(self.workspace_path.glob("**/*.yml"))
            + list(self.workspace_path.glob("**/*.toml"))
        )

        for config_file in config_files:
            try:
                content = config_file.read_text(encoding="utf-8").lower()

                for term in search_terms:
                    if term.lower() in content:
                        evidence.append(
                            f"{config_file.name} - конфігурація для '{term}'"
                        )

            except Exception:
                continue

        return evidence

    def _extract_search_terms(self, task_name: str, description: str) -> List[str]:
        """Витягування ключових слів для пошуку"""
        terms = []

        # Додаємо назву задачі
        terms.append(task_name)

        # Шукаємо відповідні ключові слова
        text_to_search = (task_name + " " + description).lower()

        for category, keywords in self.implementation_keywords.items():
            for keyword in keywords:
                if keyword in text_to_search:
                    terms.extend(keywords)
                    break

        # Додаємо специфічні терміни з опису
        specific_terms = re.findall(
            r"\b[A-Z][a-zA-Z]+\b", task_name + " " + description
        )
        terms.extend(specific_terms)

        # Видаляємо дублікати та повертаємо
        return list(set(terms))

    def _get_line_context(
        self, lines: List[str], line_index: int, context_size: int = 2
    ) -> str:
        """Отримання контексту навколо рядка"""
        start = max(0, line_index - context_size)
        end = min(len(lines), line_index + context_size + 1)

        context_lines = []
        for i in range(start, end):
            prefix = ">>> " if i == line_index else "    "
            context_lines.append(f"{prefix}{lines[i].strip()}")

        return " | ".join(context_lines)

    def _calculate_confidence(self, evidence: List[str], task_name: str) -> float:
        """Розрахунок впевненості у реалізації"""
        if not evidence:
            return 0.0

        base_score = min(len(evidence) * 10, 60)  # Базова оцінка за кількістю доказів

        # Бонуси за якість доказів
        quality_bonus = 0

        # Бонус за наявність класів/функцій
        for ev in evidence:
            if any(
                keyword in ev.lower()
                for keyword in ["class ", "def ", "function", "async def"]
            ):
                quality_bonus += 15
            if "plugin" in ev.lower() and "plugin" in task_name.lower():
                quality_bonus += 20
            if ".py:" in ev:  # Конкретний рядок у коді
                quality_bonus += 10

        # Штраф за загальні терміни
        penalty = 0
        generic_terms = ["test", "example", "todo", "fixme", "placeholder"]
        for ev in evidence:
            if any(term in ev.lower() for term in generic_terms):
                penalty += 5

        total_score = base_score + quality_bonus - penalty
        return min(max(total_score, 0), 100)  # Обмежуємо 0-100%

    async def _update_dev_plan(self, updates: List[TaskCheckResult]) -> int:
        """Оновлення DEV_PLAN.md з новими відмітками"""
        try:
            content = self.dev_plan_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            updated_count = 0

            for update in updates:
                # Знаходимо рядок для оновлення
                for i, line in enumerate(lines):
                    if update.task_name in line:
                        # Оновлюємо чекбокс
                        if update.actual_status:
                            # Ставимо галочку
                            new_line = re.sub(r"\[\s*\]", "[x]", line)
                        else:
                            # Знімаємо галочку
                            new_line = re.sub(
                                r"\[x\]", "[ ]", line, flags=re.IGNORECASE
                            )

                        if new_line != line:
                            lines[i] = new_line
                            updated_count += 1
                            self.logger.info(
                                f"✅ Оновлено: {update.task_name} -> {'[x]' if update.actual_status else '[ ]'}"
                            )
                        break

            # Зберігаємо оновлений файл
            if updated_count > 0:
                updated_content = "\n".join(lines)
                self.dev_plan_path.write_text(updated_content, encoding="utf-8")
                self.logger.info(f"💾 Збережено {updated_count} оновлень у DEV_PLAN.md")

            return updated_count

        except Exception as e:
            self.logger.error(f"Помилка оновлення DEV_PLAN: {e}")
            return 0

    def _generate_validation_report(
        self, results: List[TaskCheckResult]
    ) -> Dict[str, Any]:
        """Генерація детального звіту валідації"""
        total = len(results)
        completed = len([r for r in results if r.current_status])
        actually_completed = len([r for r in results if r.actual_status])
        needs_update = len([r for r in results if r.needs_update])

        # Категоризація за впевненістю
        high_confidence = [r for r in results if r.confidence >= 80]
        medium_confidence = [r for r in results if 50 <= r.confidence < 80]
        low_confidence = [r for r in results if r.confidence < 50]

        # Топ-задачі з найбільшою кількістю доказів
        top_evidence = sorted(results, key=lambda r: len(r.evidence), reverse=True)[:5]

        return {
            "summary": {
                "total_tasks": total,
                "marked_completed": completed,
                "actually_completed": actually_completed,
                "needs_update": needs_update,
                "accuracy_percentage": round((total - needs_update) / total * 100, 1)
                if total > 0
                else 0,
            },
            "confidence_distribution": {
                "high_confidence": len(high_confidence),
                "medium_confidence": len(medium_confidence),
                "low_confidence": len(low_confidence),
            },
            "top_evidence_tasks": [
                {
                    "task": task.task_name,
                    "evidence_count": len(task.evidence),
                    "confidence": round(task.confidence, 1),
                }
                for task in top_evidence
            ],
            "discrepancies": [
                {
                    "task": result.task_name,
                    "marked_as": "completed" if result.current_status else "incomplete",
                    "actually_is": "completed"
                    if result.actual_status
                    else "incomplete",
                    "confidence": round(result.confidence, 1),
                    "evidence_sample": result.evidence[:3],
                }
                for result in results
                if result.needs_update
            ],
        }

    def get_supported_tasks(self) -> List[str]:
        """Підтримувані типи задач"""
        return ["dev_plan_validation", "validate_dev_plan", "check_dev_plan"]

    def get_gui_configuration(self) -> Dict[str, Any]:
        """Конфігурація GUI для плагіну"""
        return {
            "name": "DEV_PLAN Validator",
            "icon": "🔍",
            "color": "#4A90E2",
            "description": "Автоматична перевірка та корекція відміток у DEV_PLAN.md",
            "widgets": [
                {
                    "type": "progress_bar",
                    "label": "Прогрес валідації",
                    "key": "validation_progress",
                },
                {
                    "type": "metrics_grid",
                    "label": "Статистика",
                    "metrics": [
                        {"key": "total_tasks", "label": "Всього задач"},
                        {"key": "needs_update", "label": "Потребують оновлення"},
                        {"key": "accuracy_percentage", "label": "Точність %"},
                    ],
                },
                {
                    "type": "list",
                    "label": "Невідповідності",
                    "key": "discrepancies",
                    "max_items": 10,
                },
            ],
        }

    async def _execute_gui_task(self, task: Dict[str, Any]) -> bool:
        """Виконання GUI задачі"""
        return await self._execute_generic_task(task)

    async def _execute_ai_task(self, task: Dict[str, Any]) -> bool:
        """Виконання AI задачі"""
        return await self._execute_generic_task(task)

    async def _execute_system_task(self, task: Dict[str, Any]) -> bool:
        """Виконання системної задачі"""
        return await self._execute_generic_task(task)

    async def _execute_generic_task(self, task: Dict[str, Any]) -> bool:
        """Виконання загальної задачі"""
        result = await self.execute_task(task)
        return result.success
