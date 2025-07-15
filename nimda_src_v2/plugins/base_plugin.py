"""
Базовий клас для всіх плагінів NIMDA Agent
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class PluginStatus(Enum):
    """Статуси плагіна"""

    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class PluginResult:
    """Результат виконання плагіна"""

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    execution_time: Optional[float] = None
    error: Optional[Exception] = None


class BasePlugin(ABC):
    """
    Базовий клас для всіх плагінів NIMDA Agent

    Забезпечує стандартний інтерфейс для:
    - Ініціалізації та конфігурації
    - Виконання завдань
    - Моніторингу стану
    - Інтеграції з GUI
    - Обробки помилок
    """

    def __init__(
        self, name: str, version: str = "1.0.0", config: Optional[Dict] = None
    ):
        """
        Ініціалізація базового плагіна

        Args:
            name: Назва плагіна
            version: Версія плагіна
            config: Конфігурація плагіна
        """
        self.name = name
        self.version = version
        self.config = config or {}
        self.status = PluginStatus.IDLE
        self.logger = logging.getLogger(f"Plugin.{name}")

        # Статистика виконання
        self.execution_count = 0
        self.success_count = 0
        self.error_count = 0
        self.total_execution_time = 0.0

        # Зворотні виклики для інтеграції
        self.on_status_change = (
            None  # Callable[[BasePlugin, PluginStatus, PluginStatus, str], None]
        )
        self.on_progress_update = None  # Callable[[BasePlugin, float, str], None]
        self.on_gui_update = None  # Callable[[BasePlugin, Dict[str, Any]], None]

        self.logger.info(f"Плагін {name} v{version} ініціалізовано")

    @abstractmethod
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
        pass

    @abstractmethod
    def get_supported_tasks(self) -> List[str]:
        """
        Отримання списку підтримуваних типів завдань

        Returns:
            List[str]: Список типів завдань
        """
        pass

    @abstractmethod
    def get_gui_configuration(self) -> Dict[str, Any]:
        """
        Отримання конфігурації GUI для плагіна

        Returns:
            Dict: Конфігурація GUI
        """
        pass

    def validate_task(self, task: Dict[str, Any]) -> bool:
        """
        Валідація завдання перед виконанням

        Args:
            task: Завдання для валідації

        Returns:
            bool: True якщо завдання валідне
        """
        required_fields = ["type", "description"]
        return all(field in task for field in required_fields)

    def update_status(self, status: PluginStatus, message: str = ""):
        """
        Оновлення статусу плагіна

        Args:
            status: Новий статус
            message: Повідомлення про статус
        """
        old_status = self.status
        self.status = status

        self.logger.info(f"Статус змінено: {old_status.value} -> {status.value}")

        if self.on_status_change:
            self.on_status_change(self, old_status, status, message)

    def update_progress(self, progress: float, message: str = ""):
        """
        Оновлення прогресу виконання

        Args:
            progress: Прогрес (0.0 - 1.0)
            message: Повідомлення про прогрес
        """
        if self.on_progress_update:
            self.on_progress_update(self, progress, message)

    def update_gui(self, gui_data: Dict[str, Any]):
        """
        Оновлення даних для GUI

        Args:
            gui_data: Дані для відображення в GUI
        """
        if self.on_gui_update:
            self.on_gui_update(self, gui_data)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Отримання статистики виконання плагіна

        Returns:
            Dict: Статистика
        """
        success_rate = (
            (self.success_count / self.execution_count * 100)
            if self.execution_count > 0
            else 0
        )
        avg_execution_time = (
            (self.total_execution_time / self.execution_count)
            if self.execution_count > 0
            else 0
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status.value,
            "execution_count": self.execution_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": round(success_rate, 2),
            "total_execution_time": round(self.total_execution_time, 2),
            "average_execution_time": round(avg_execution_time, 2),
        }

    async def initialize(self) -> bool:
        """
        Ініціалізація плагіна (опціональна)

        Returns:
            bool: True якщо ініціалізація успішна
        """
        return True

    async def cleanup(self) -> bool:
        """
        Очищення ресурсів плагіна (опціональна)

        Returns:
            bool: True якщо очищення успішне
        """
        return True

    def configure(self, config: Dict[str, Any]) -> bool:
        """
        Конфігурація плагіна

        Args:
            config: Нова конфігурація

        Returns:
            bool: True якщо конфігурація успішна
        """
        try:
            self.config.update(config)
            self.logger.info("Конфігурацію оновлено")
            return True
        except Exception as e:
            self.logger.error(f"Помилка конфігурації: {e}")
            return False

    def can_handle_task(self, task: Dict[str, Any]) -> bool:
        """
        Перевірка чи може плагін обробити завдання

        Args:
            task: Завдання для перевірки

        Returns:
            bool: True якщо плагін може обробити завдання
        """
        task_type = task.get("type", "")
        supported_tasks = self.get_supported_tasks()
        return task_type in supported_tasks and self.validate_task(task)
