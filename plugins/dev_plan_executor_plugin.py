"""
NIMDA Agent Plugin для виконання DEV_PLAN завдань
Глибока інтеграція з агентом для автоматизованого виконання плану розробки
"""

import asyncio
import json
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base_plugin import BasePlugin, PluginResult, PluginStatus


class DevPlanExecutorPlugin(BasePlugin):
    """
    Плагін для виконання завдань з DEV_PLAN.md

    Особливості:
    - Парсинг та аналіз DEV_PLAN.md
    - Автоматичне виконання завдань по фазах
    - Інтеграція з GUI для відображення прогресу
    - Адаптивне управління завантаженням
    - Глибока інтеграція з NIMDA Agent
    """

    def __init__(self, config: Optional[Dict] = None):
        """Ініціалізація плагіна"""
        super().__init__(name="DevPlanExecutor", version="2.0.0", config=config or {})

        # Основні параметри
        self.workspace_path = Path(self.config.get("workspace_path", "."))
        self.dev_plan_path = self.workspace_path / "DEV_PLAN.md"
        self.backup_enabled = self.config.get("backup_enabled", True)
        self.max_parallel_tasks = self.config.get("max_parallel_tasks", 3)

        # Структура плану
        self.dev_plan = {
            "phases": {},
            "metadata": {},
            "statistics": {
                "total_tasks": 0,
                "completed_tasks": 0,
                "failed_tasks": 0,
                "current_phase": None,
            },
        }

        # Поточне виконання
        self.current_phase = None
        self.current_section = None
        self.execution_queue = []
        self.running_tasks = []

        # Продуктивність
        self.task_execution_times = []
        self.phase_completion_times = {}

        self.logger.info("DevPlanExecutorPlugin ініціалізовано")

    async def execute(
        self, task: Dict[str, Any], context: Optional[Dict] = None
    ) -> PluginResult:
        """
        Виконання основного завдання плагіна

        Args:
            task: Завдання для виконання
            context: Контекст виконання

        Returns:
            PluginResult: Результат виконання
        """
        start_time = time.time()
        self.update_status(PluginStatus.RUNNING)

        try:
            task_type = task.get("type", "")

            if task_type == "parse_dev_plan":
                result = await self._parse_dev_plan()
            elif task_type == "execute_phase":
                phase_name = task.get("phase_name")
                result = await self._execute_phase(phase_name)
            elif task_type == "execute_section":
                phase_name = task.get("phase_name")
                section_name = task.get("section_name")
                result = await self._execute_section(phase_name, section_name)
            elif task_type == "execute_task":
                task_data = task.get("task_data")
                result = await self._execute_task(task_data)
            elif task_type == "get_progress":
                result = await self._get_progress()
            elif task_type == "optimize_execution":
                result = await self._optimize_execution()
            else:
                result = PluginResult(
                    success=False, message=f"Невідомий тип завдання: {task_type}"
                )

            execution_time = time.time() - start_time
            result.execution_time = execution_time
            self.task_execution_times.append(execution_time)

            if result.success:
                self.update_status(PluginStatus.COMPLETED)
            else:
                self.update_status(PluginStatus.ERROR)

            return result

        except Exception as e:
            self.logger.error(f"Помилка виконання завдання: {e}")
            execution_time = time.time() - start_time

            self.update_status(PluginStatus.ERROR)

            return PluginResult(
                success=False,
                message=f"Помилка виконання: {e}",
                execution_time=execution_time,
                error=e,
            )

    async def _parse_dev_plan(self) -> PluginResult:
        """Парсинг DEV_PLAN.md файлу"""
        try:
            if not self.dev_plan_path.exists():
                return PluginResult(
                    success=False,
                    message=f"DEV_PLAN.md не знайдено за шляхом: {self.dev_plan_path}",
                )

            content = self.dev_plan_path.read_text(encoding="utf-8")

            # Парсинг фаз
            phases = self._extract_phases(content)
            self.dev_plan["phases"] = phases

            # Парсинг метаданих
            metadata = self._extract_metadata(content)
            self.dev_plan["metadata"] = metadata

            # Підрахунок статистики
            total_tasks = sum(
                len(section.get("tasks", []))
                for phase in phases.values()
                for section in phase.get("sections", {}).values()
            )

            self.dev_plan["statistics"]["total_tasks"] = total_tasks

            self.logger.info(
                f"DEV_PLAN парсено: {len(phases)} фаз, {total_tasks} завдань"
            )

            # Оновлення GUI
            self.update_gui(
                {
                    "type": "dev_plan_parsed",
                    "phases": list(phases.keys()),
                    "total_tasks": total_tasks,
                    "metadata": metadata,
                }
            )

            return PluginResult(
                success=True,
                message=f"DEV_PLAN успішно парсено: {len(phases)} фаз, {total_tasks} завдань",
                data={
                    "phases": phases,
                    "metadata": metadata,
                    "statistics": self.dev_plan["statistics"],
                },
            )

        except Exception as e:
            return PluginResult(
                success=False, message=f"Помилка парсингу DEV_PLAN: {e}", error=e
            )

    def _extract_phases(self, content: str) -> Dict[str, Any]:
        """Витягування фаз з контенту"""
        phases = {}

        # Регулярний вираз для пошуку фаз
        phase_pattern = r"## 🎮 (Phase \d+): (.+?)\n(.*?)(?=## 🎮 Phase|\## 📊|\Z)"

        for match in re.finditer(phase_pattern, content, re.DOTALL):
            phase_id = match.group(1)
            phase_title = match.group(2).strip()
            phase_content = match.group(3)

            sections = self._extract_sections(phase_content)

            phases[phase_id] = {
                "title": phase_title,
                "sections": sections,
                "status": "pending",
            }

        return phases

    def _extract_sections(self, phase_content: str) -> Dict[str, Any]:
        """Витягування секцій з контенту фази"""
        sections = {}

        # Регулярний вираз для пошуку секцій
        section_pattern = r"### (\d+\.\d+) (.+?)\n(.*?)(?=### \d+\.\d+|\Z)"

        for match in re.finditer(section_pattern, phase_content, re.DOTALL):
            section_id = match.group(1)
            section_title = match.group(2).strip()
            section_content = match.group(3)

            tasks = self._extract_tasks(section_content)

            sections[section_id] = {
                "title": section_title,
                "tasks": tasks,
                "status": "pending",
            }

        return sections

    def _extract_tasks(self, section_content: str) -> List[Dict[str, Any]]:
        """Витягування завдань з контенту секції"""
        tasks = []

        # Регулярний вираз для пошуку завдань
        task_pattern = r"-\s+\[([ x])\]\s+\*\*(.+?)\*\*\s+-\s+(.+?)(?=\n-|\Z)"

        for match in re.finditer(task_pattern, section_content, re.DOTALL):
            completed = match.group(1) == "x"
            task_name = match.group(2).strip()
            task_description = match.group(3).strip()

            tasks.append(
                {
                    "name": task_name,
                    "description": task_description,
                    "completed": completed,
                    "status": "completed" if completed else "pending",
                }
            )

        return tasks

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Витягування метаданих з контенту"""
        metadata = {}

        # Пошук версії плану
        version_match = re.search(r"Plan v(\d+\.\d+)", content)
        if version_match:
            metadata["version"] = version_match.group(1)

        # Пошук дати створення
        date_match = re.search(r"Created.*?(\d{4}-\d{2}-\d{2})", content)
        if date_match:
            metadata["created"] = date_match.group(1)

        # Пошук цільової продуктивності
        performance_match = re.search(r"(\d+\.\d+)\+ tasks/second", content)
        if performance_match:
            metadata["target_performance"] = float(performance_match.group(1))

        return metadata

    async def _execute_phase(self, phase_name: str) -> PluginResult:
        """Виконання цілої фази"""
        if phase_name not in self.dev_plan["phases"]:
            return PluginResult(success=False, message=f"Фаза {phase_name} не знайдена")

        self.current_phase = phase_name
        phase = self.dev_plan["phases"][phase_name]
        phase_start_time = time.time()

        self.logger.info(f"Початок виконання фази: {phase_name}")
        self.update_gui(
            {"type": "phase_started", "phase": phase_name, "title": phase["title"]}
        )

        completed_sections = 0
        failed_sections = 0

        for section_id, section in phase["sections"].items():
            try:
                result = await self._execute_section(phase_name, section_id)
                if result.success:
                    completed_sections += 1
                else:
                    failed_sections += 1

                # Оновлення прогресу
                progress = completed_sections / len(phase["sections"])
                self.update_progress(progress, f"Секція {section_id} виконана")

            except Exception as e:
                self.logger.error(f"Помилка виконання секції {section_id}: {e}")
                failed_sections += 1

        phase_time = time.time() - phase_start_time
        self.phase_completion_times[phase_name] = phase_time

        success = failed_sections == 0
        phase["status"] = "completed" if success else "failed"

        self.update_gui(
            {
                "type": "phase_completed",
                "phase": phase_name,
                "success": success,
                "completed_sections": completed_sections,
                "failed_sections": failed_sections,
                "execution_time": phase_time,
            }
        )

        return PluginResult(
            success=success,
            message=f"Фаза {phase_name} {'завершена' if success else 'завершена з помилками'}: {completed_sections}/{len(phase['sections'])} секцій",
            data={
                "completed_sections": completed_sections,
                "failed_sections": failed_sections,
                "execution_time": phase_time,
            },
        )

    async def _execute_section(self, phase_name: str, section_id: str) -> PluginResult:
        """Виконання секції завдань"""
        phase = self.dev_plan["phases"][phase_name]
        section = phase["sections"][section_id]

        self.current_section = section_id
        self.logger.info(f"Виконання секції {section_id}: {section['title']}")

        completed_tasks = 0
        failed_tasks = 0

        # Виконання завдань паралельно
        tasks_to_execute = [task for task in section["tasks"] if not task["completed"]]

        if not tasks_to_execute:
            return PluginResult(
                success=True, message=f"Всі завдання секції {section_id} вже виконані"
            )

        # Групування завдань для паралельного виконання
        task_groups = self._group_tasks_for_parallel_execution(tasks_to_execute)

        for group in task_groups:
            # Виконання групи завдань паралельно
            tasks_coroutines = [self._execute_task(task) for task in group]
            results = await asyncio.gather(*tasks_coroutines, return_exceptions=True)

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.logger.error(f"Помилка виконання завдання: {result}")
                    failed_tasks += 1
                    group[i]["status"] = "failed"
                elif result.success:
                    completed_tasks += 1
                    group[i]["status"] = "completed"
                    group[i]["completed"] = True
                else:
                    failed_tasks += 1
                    group[i]["status"] = "failed"

        success = failed_tasks == 0
        section["status"] = "completed" if success else "failed"

        return PluginResult(
            success=success,
            message=f"Секція {section_id}: {completed_tasks}/{len(tasks_to_execute)} завдань виконано",
            data={"completed_tasks": completed_tasks, "failed_tasks": failed_tasks},
        )

    def _group_tasks_for_parallel_execution(
        self, tasks: List[Dict]
    ) -> List[List[Dict]]:
        """Групування завдань для паралельного виконання"""
        groups = []
        current_group = []

        for task in tasks:
            # Простий алгоритм групування
            if len(current_group) < self.max_parallel_tasks:
                current_group.append(task)
            else:
                groups.append(current_group)
                current_group = [task]

        if current_group:
            groups.append(current_group)

        return groups

    async def _execute_task(self, task: Dict[str, Any]) -> PluginResult:
        """Виконання одного завдання"""
        task_name = task.get("name", "Unknown Task")
        self.logger.info(f"Виконання завдання: {task_name}")

        # Симуляція виконання завдання
        # В реальній імплементації тут буде логіка виконання конкретного завдання
        await asyncio.sleep(0.1)  # Симуляція роботи

        # Оновлення GUI
        self.update_gui(
            {"type": "task_progress", "task": task_name, "status": "executing"}
        )

        # Детальна логіка виконання залежно від типу завдання
        success = await self._execute_task_by_type(task)

        return PluginResult(
            success=success,
            message=f"Завдання {task_name} {'виконано' if success else 'не виконано'}",
        )

    async def _execute_task_by_type(self, task: Dict[str, Any]) -> bool:
        """Виконання завдання залежно від його типу"""
        task_name = task.get("name", "").lower()

        # GUI завдання
        if any(
            gui_keyword in task_name
            for gui_keyword in ["gui", "interface", "visual", "theme"]
        ):
            return await self._execute_gui_task(task)

        # AI завдання
        elif any(
            ai_keyword in task_name
            for ai_keyword in ["ai", "neural", "machine learning", "intelligence"]
        ):
            return await self._execute_ai_task(task)

        # Системні завдання
        elif any(
            sys_keyword in task_name
            for sys_keyword in ["system", "performance", "security", "monitoring"]
        ):
            return await self._execute_system_task(task)

        # За замовчуванням
        else:
            return await self._execute_generic_task(task)

    async def _execute_gui_task(self, task: Dict[str, Any]) -> bool:
        """Виконання GUI завдання"""
        # Тут буде логіка для GUI завдань
        self.logger.info(f"Виконання GUI завдання: {task['name']}")
        await asyncio.sleep(0.2)  # Симуляція роботи
        return True

    async def _execute_ai_task(self, task: Dict[str, Any]) -> bool:
        """Виконання AI завдання"""
        # Тут буде логіка для AI завдань
        self.logger.info(f"Виконання AI завдання: {task['name']}")
        await asyncio.sleep(0.3)  # Симуляція роботи
        return True

    async def _execute_system_task(self, task: Dict[str, Any]) -> bool:
        """Виконання системного завдання"""
        # Тут буде логіка для системних завдань
        self.logger.info(f"Виконання системного завдання: {task['name']}")
        await asyncio.sleep(0.15)  # Симуляція роботи
        return True

    async def _execute_generic_task(self, task: Dict[str, Any]) -> bool:
        """Виконання загального завдання"""
        # Тут буде логіка для загальних завдань
        self.logger.info(f"Виконання завдання: {task['name']}")
        await asyncio.sleep(0.1)  # Симуляція роботи
        return True

    async def _get_progress(self) -> PluginResult:
        """Отримання поточного прогресу"""
        completed_tasks = sum(
            sum(1 for task in section["tasks"] if task["completed"])
            for phase in self.dev_plan["phases"].values()
            for section in phase["sections"].values()
        )

        total_tasks = self.dev_plan["statistics"]["total_tasks"]
        progress = (completed_tasks / total_tasks) if total_tasks > 0 else 0

        return PluginResult(
            success=True,
            message=f"Прогрес: {completed_tasks}/{total_tasks} ({progress:.1%})",
            data={
                "completed_tasks": completed_tasks,
                "total_tasks": total_tasks,
                "progress": progress,
                "current_phase": self.current_phase,
                "current_section": self.current_section,
            },
        )

    async def _optimize_execution(self) -> PluginResult:
        """Оптимізація виконання завдань"""
        # Аналіз продуктивності
        avg_task_time = (
            sum(self.task_execution_times) / len(self.task_execution_times)
            if self.task_execution_times
            else 0
        )

        # Оптимізація параметрів
        if avg_task_time > 0.5:  # Якщо завдання виконуються повільно
            self.max_parallel_tasks = max(1, self.max_parallel_tasks - 1)
        elif avg_task_time < 0.1:  # Якщо завдання виконуються швидко
            self.max_parallel_tasks = min(5, self.max_parallel_tasks + 1)

        return PluginResult(
            success=True,
            message=f"Оптимізація виконання: паралельні завдання = {self.max_parallel_tasks}",
            data={
                "average_task_time": avg_task_time,
                "max_parallel_tasks": self.max_parallel_tasks,
            },
        )

    def get_supported_tasks(self) -> List[str]:
        """Отримання списку підтримуваних типів завдань"""
        return [
            "parse_dev_plan",
            "execute_phase",
            "execute_section",
            "execute_task",
            "get_progress",
            "optimize_execution",
        ]

    def get_gui_configuration(self) -> Dict[str, Any]:
        """Отримання конфігурації GUI для плагіна"""
        return {
            "window_type": "adaptive_panel",
            "position": "center",
            "size": {"width": 800, "height": 600},
            "transparency": 0.9,
            "theme": "dark_neon",
            "components": [
                {
                    "type": "progress_bar",
                    "id": "main_progress",
                    "label": "Загальний прогрес",
                },
                {
                    "type": "phase_selector",
                    "id": "phase_list",
                    "label": "Фази виконання",
                },
                {"type": "task_grid", "id": "task_overview", "label": "Огляд завдань"},
                {
                    "type": "performance_chart",
                    "id": "performance_metrics",
                    "label": "Метрики продуктивності",
                },
            ],
            "actions": [
                {"id": "start_execution", "label": "Почати виконання"},
                {"id": "pause_execution", "label": "Пауза"},
                {"id": "optimize_performance", "label": "Оптимізувати"},
            ],
        }
