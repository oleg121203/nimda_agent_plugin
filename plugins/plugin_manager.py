"""
Менеджер плагінів для NIMDA Agent
Управління життєвим циклом плагінів та їх інтеграцією
"""

import asyncio
import importlib.util
import inspect
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type

from .base_plugin import BasePlugin, PluginResult, PluginStatus


class PluginManager:
    """
    Менеджер плагінів для NIMDA Agent

    Функції:
    - Автоматичне завантаження плагінів
    - Управління життєвим циклом
    - Розподіл завдань між плагінами
    - Моніторинг продуктивності
    - Інтеграція з GUI
    """

    def __init__(self, plugins_dir: Optional[str] = None, max_workers: int = 4):
        """
        Ініціалізація менеджера плагінів

        Args:
            plugins_dir: Шлях до директорії з плагінами
            max_workers: Максимальна кількість робітників для виконання
        """
        self.plugins_dir = Path(plugins_dir) if plugins_dir else Path(__file__).parent
        self.max_workers = max_workers
        self.logger = logging.getLogger("PluginManager")

        # Реєстр плагінів
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugin_classes: Dict[str, Type[BasePlugin]] = {}

        # Виконавець завдань
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        # Статистика
        self.total_tasks_executed = 0
        self.total_execution_time = 0.0

        # Зворотні виклики
        self.on_plugin_loaded = None
        self.on_plugin_error = None
        self.on_task_completed = None

        self.logger.info(f"PluginManager ініціалізовано з {max_workers} робітниками")

    async def load_plugins(self) -> bool:
        """
        Завантаження всіх плагінів з директорії

        Returns:
            bool: True якщо всі плагіни завантажені успішно
        """
        try:
            plugin_files = list(self.plugins_dir.glob("*_plugin.py"))

            for plugin_file in plugin_files:
                await self._load_plugin_from_file(plugin_file)

            self.logger.info(f"Завантажено {len(self.plugins)} плагінів")
            return True

        except Exception as e:
            self.logger.error(f"Помилка завантаження плагінів: {e}")
            return False

    async def _load_plugin_from_file(self, plugin_file: Path) -> bool:
        """
        Завантаження плагіна з файлу

        Args:
            plugin_file: Шлях до файлу плагіна

        Returns:
            bool: True якщо плагін завантажено успішно
        """
        try:
            module_name = plugin_file.stem
            spec = importlib.util.spec_from_file_location(module_name, plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Знаходимо клас плагіна
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, BasePlugin)
                    and obj != BasePlugin
                ):
                    self.plugin_classes[name] = obj
                    plugin_instance = obj()

                    # Ініціалізуємо плагін
                    if await plugin_instance.initialize():
                        self.plugins[plugin_instance.name] = plugin_instance

                        # Підключаємо зворотні виклики
                        plugin_instance.on_status_change = self._on_plugin_status_change
                        plugin_instance.on_progress_update = (
                            self._on_plugin_progress_update
                        )
                        plugin_instance.on_gui_update = self._on_plugin_gui_update

                        self.logger.info(f"Плагін {plugin_instance.name} завантажено")

                        if self.on_plugin_loaded:
                            self.on_plugin_loaded(plugin_instance)

                        return True

            return False

        except Exception as e:
            self.logger.error(f"Помилка завантаження плагіна {plugin_file}: {e}")
            return False

    async def register_plugin(self, plugin: BasePlugin) -> bool:
        """
        Ручна реєстрація плагіна

        Args:
            plugin: Екземпляр плагіна

        Returns:
            bool: True якщо плагін зареєстровано успішно
        """
        try:
            if await plugin.initialize():
                self.plugins[plugin.name] = plugin

                # Підключаємо зворотні виклики
                plugin.on_status_change = self._on_plugin_status_change
                plugin.on_progress_update = self._on_plugin_progress_update
                plugin.on_gui_update = self._on_plugin_gui_update

                self.logger.info(f"Плагін {plugin.name} зареєстровано")

                if self.on_plugin_loaded:
                    self.on_plugin_loaded(plugin)

                return True
            else:
                self.logger.error(f"Не вдалося ініціалізувати плагін {plugin.name}")
                return False

        except Exception as e:
            self.logger.error(f"Помилка реєстрації плагіна {plugin.name}: {e}")
            return False

    async def execute_task(
        self, task: Dict[str, Any], context: Optional[Dict] = None
    ) -> PluginResult:
        """
        Виконання завдання відповідним плагіном

        Args:
            task: Завдання для виконання
            context: Контекст виконання

        Returns:
            PluginResult: Результат виконання
        """
        start_time = asyncio.get_event_loop().time()

        try:
            # Знаходимо підходящий плагін
            plugin = self._find_plugin_for_task(task)

            if not plugin:
                return PluginResult(
                    success=False,
                    message=f"Не знайдено плагін для завдання типу '{task.get('type', 'unknown')}'",
                )

            # Виконуємо завдання
            self.logger.info(
                f"Виконання завдання '{task.get('description', '')}' плагіном {plugin.name}"
            )

            result = await plugin.execute(task, context)

            # Оновлюємо статистику
            execution_time = asyncio.get_event_loop().time() - start_time
            result.execution_time = execution_time

            self.total_tasks_executed += 1
            self.total_execution_time += execution_time

            plugin.execution_count += 1
            plugin.total_execution_time += execution_time

            if result.success:
                plugin.success_count += 1
            else:
                plugin.error_count += 1

            self.logger.info(
                f"Завдання виконано за {execution_time:.2f}с, результат: {result.success}"
            )

            if self.on_task_completed:
                self.on_task_completed(plugin, task, result)

            return result

        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            error_result = PluginResult(
                success=False,
                message=f"Помилка виконання завдання: {e}",
                execution_time=execution_time,
                error=e,
            )

            if self.on_plugin_error:
                self.on_plugin_error(None, task, e)

            return error_result

    def _find_plugin_for_task(self, task: Dict[str, Any]) -> Optional[BasePlugin]:
        """
        Знаходження підходящого плагіна для завдання

        Args:
            task: Завдання

        Returns:
            BasePlugin: Підходящий плагін або None
        """
        for plugin in self.plugins.values():
            if plugin.status != PluginStatus.DISABLED and plugin.can_handle_task(task):
                return plugin

        return None

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """
        Отримання плагіна за назвою

        Args:
            name: Назва плагіна

        Returns:
            BasePlugin: Плагін або None
        """
        return self.plugins.get(name)

    def get_all_plugins(self) -> List[BasePlugin]:
        """
        Отримання всіх зареєстрованих плагінів

        Returns:
            List[BasePlugin]: Список плагінів
        """
        return list(self.plugins.values())

    def get_plugins_by_status(self, status: PluginStatus) -> List[BasePlugin]:
        """
        Отримання плагінів за статусом

        Args:
            status: Статус плагінів

        Returns:
            List[BasePlugin]: Список плагінів
        """
        return [plugin for plugin in self.plugins.values() if plugin.status == status]

    def get_system_statistics(self) -> Dict[str, Any]:
        """
        Отримання системної статистики

        Returns:
            Dict: Статистика системи плагінів
        """
        active_plugins = len(self.get_plugins_by_status(PluginStatus.RUNNING))
        total_plugins = len(self.plugins)
        avg_execution_time = (
            (self.total_execution_time / self.total_tasks_executed)
            if self.total_tasks_executed > 0
            else 0
        )

        return {
            "total_plugins": total_plugins,
            "active_plugins": active_plugins,
            "total_tasks_executed": self.total_tasks_executed,
            "total_execution_time": round(self.total_execution_time, 2),
            "average_execution_time": round(avg_execution_time, 2),
            "plugin_statistics": [
                plugin.get_statistics() for plugin in self.plugins.values()
            ],
        }

    async def shutdown(self):
        """Завершення роботи менеджера плагінів"""
        self.logger.info("Завершення роботи PluginManager...")

        # Очищуємо всі плагіни
        for plugin in self.plugins.values():
            try:
                await plugin.cleanup()
            except Exception as e:
                self.logger.error(f"Помилка очищення плагіна {plugin.name}: {e}")

        # Закриваємо executor
        self.executor.shutdown(wait=True)

        self.logger.info("PluginManager завершено")

    def _on_plugin_status_change(
        self,
        plugin: BasePlugin,
        old_status: PluginStatus,
        new_status: PluginStatus,
        message: str,
    ):
        """Обробка зміни статусу плагіна"""
        self.logger.debug(
            f"Плагін {plugin.name}: {old_status.value} -> {new_status.value}"
        )

    def _on_plugin_progress_update(
        self, plugin: BasePlugin, progress: float, message: str
    ):
        """Обробка оновлення прогресу плагіна"""
        self.logger.debug(f"Плагін {plugin.name}: прогрес {progress:.1%}")

    def _on_plugin_gui_update(self, plugin: BasePlugin, gui_data: Dict[str, Any]):
        """Обробка оновлення GUI плагіна"""
        self.logger.debug(f"Плагін {plugin.name}: оновлення GUI")
