#!/usr/bin/env python3
"""
🚀 NIMDA Agent Plugin System Runner
Головний виконавець системи плагінів для NIMDA Agent

Створено: 15 липня 2025
Версія: 2.0.0 - Complete Plugin Integration
Фокус: Глибока інтеграція та автоматизоване виконання DEV_PLAN

Перенесено до Core модуля для кращої організації проекту.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Any, Dict

# Додаємо шлях до кореневої директорії проекту
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from plugins.dev_plan_executor_plugin import DevPlanExecutorPlugin
    from plugins.plugin_manager import PluginManager
except ImportError as e:
    print(f"Помилка імпорту плагінів: {e}")
    sys.exit(1)


class NIMDAPluginSystemRunner:
    """
    Головний виконавець системи плагінів NIMDA Agent

    Особливості:
    - Автоматичне завантаження плагінів
    - Управління життєвим циклом
    - Інтелектуальне планування завдань
    - Моніторинг продуктивності
    - GUI інтеграція
    """

    def __init__(self, workspace_path: str = "."):
        """Ініціалізація системи"""
        self.workspace_path = Path(workspace_path)
        self.setup_logging()

        # Ініціалізація менеджера плагінів
        plugins_dir = project_root / "plugins"
        self.plugin_manager = PluginManager(plugins_dir=str(plugins_dir), max_workers=4)

        # Налаштування логгера
        self.logger = logging.getLogger("NIMDAPluginSystem")

        # Зворотні виклики будуть налаштовані через API PluginManager
        self.logger.info("🚀 NIMDA Plugin System Runner ініціалізовано")

    def setup_logging(self):
        """Налаштування системи логування"""
        log_dir = self.workspace_path / "logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "nimda_plugin_system.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )

    async def initialize(self) -> bool:
        """Ініціалізація системи плагінів"""
        try:
            self.logger.info("Ініціалізація системи плагінів...")

            # Налаштовуємо зворотні виклики PluginManager (безпечно)
            try:
                setattr(self.plugin_manager, "on_plugin_loaded", self._on_plugin_loaded)
                setattr(self.plugin_manager, "on_plugin_error", self._on_plugin_error)
                setattr(
                    self.plugin_manager, "on_task_completed", self._on_task_completed
                )
                self.logger.info("Зворотні виклики налаштовано успішно")
            except Exception as e:
                self.logger.warning(f"Не вдалося налаштувати зворотні виклики: {e}")

            # Завантажуємо плагіни
            await self.plugin_manager.load_plugins()

            # Реєструємо основний плагін виконання DEV_PLAN
            dev_plan_plugin = DevPlanExecutorPlugin(
                {
                    "workspace_path": str(self.workspace_path),
                    "backup_enabled": True,
                    "max_parallel_tasks": 3,
                }
            )

            await self.plugin_manager.register_plugin(dev_plan_plugin)

            self.logger.info("✅ Система плагінів ініціалізована успішно")
            return True

        except Exception as e:
            self.logger.error(f"❌ Помилка ініціалізації: {e}")
            return False

    async def run_dev_plan_execution(self) -> Dict[str, Any]:
        """Запуск виконання DEV_PLAN"""
        try:
            self.logger.info("🚀 Початок виконання DEV_PLAN...")

            # 1. Парсинг DEV_PLAN
            parse_task = {
                "type": "parse_dev_plan",
                "description": "Парсинг DEV_PLAN.md файлу",
            }

            parse_result = await self.plugin_manager.execute_task(parse_task)

            if not parse_result.success:
                return {
                    "success": False,
                    "message": f"Помилка парсингу DEV_PLAN: {parse_result.message}",
                    "results": [],
                }

            self.logger.info("✅ DEV_PLAN успішно парсено")

            # 2. Отримання списку фаз
            phases = {}
            if parse_result.data and hasattr(parse_result.data, "get"):
                phases = parse_result.data.get("phases", {})
            elif parse_result.data and isinstance(parse_result.data, dict):
                phases = parse_result.data.get("phases", {})
            execution_results = []

            # 3. Виконання фаз по черзі
            for phase_name, phase_data in phases.items():
                self.logger.info(f"🎯 Виконання фази: {phase_name}")

                phase_task = {
                    "type": "execute_phase",
                    "phase_name": phase_name,
                    "description": f"Виконання фази {phase_name}: {phase_data['title']}",
                }

                phase_result = await self.plugin_manager.execute_task(phase_task)
                execution_results.append(
                    {
                        "phase": phase_name,
                        "result": phase_result,
                        "title": phase_data["title"],
                    }
                )

                if phase_result.success:
                    self.logger.info(f"✅ Фаза {phase_name} виконана успішно")
                else:
                    self.logger.warning(
                        f"⚠️ Фаза {phase_name} завершена з помилками: {phase_result.message}"
                    )

            # 4. Отримання фінального прогресу
            progress_task = {
                "type": "get_progress",
                "description": "Отримання фінального прогресу",
            }

            progress_result = await self.plugin_manager.execute_task(progress_task)

            # 5. Підготовка звіту
            successful_phases = sum(
                1 for result in execution_results if result["result"].success
            )
            total_phases = len(execution_results)

            final_report = {
                "success": successful_phases == total_phases,
                "message": f"Виконання завершено: {successful_phases}/{total_phases} фаз успішно",
                "results": execution_results,
                "progress": progress_result.data if progress_result.success else None,
                "statistics": self.plugin_manager.get_system_statistics(),
            }

            self.logger.info(
                f"🎊 Виконання DEV_PLAN завершено: {successful_phases}/{total_phases} фаз успішно"
            )

            return final_report

        except Exception as e:
            self.logger.error(f"❌ Помилка виконання DEV_PLAN: {e}")
            return {
                "success": False,
                "message": f"Критична помилка: {e}",
                "results": [],
            }

    async def run_optimized_execution(self) -> Dict[str, Any]:
        """Запуск оптимізованого виконання з адаптивною продуктивністю"""
        try:
            self.logger.info("⚡ Початок оптимізованого виконання...")

            # Оптимізація перед виконанням
            optimize_task = {
                "type": "optimize_execution",
                "description": "Оптимізація параметрів виконання",
            }

            optimize_result = await self.plugin_manager.execute_task(optimize_task)
            self.logger.info(f"🔧 Оптимізація: {optimize_result.message}")

            # Запуск основного виконання
            return await self.run_dev_plan_execution()

        except Exception as e:
            self.logger.error(f"❌ Помилка оптимізованого виконання: {e}")
            return {
                "success": False,
                "message": f"Помилка оптимізації: {e}",
                "results": [],
            }

    async def shutdown(self):
        """Завершення роботи системи"""
        self.logger.info("🔻 Завершення роботи системи плагінів...")
        await self.plugin_manager.shutdown()
        self.logger.info("✅ Система плагінів завершена")

    def _on_plugin_loaded(self, plugin):
        """Обробка завантаження плагіна"""
        self.logger.info(f"📦 Плагін завантажено: {plugin.name} v{plugin.version}")

    def _on_plugin_error(self, plugin, task, error):
        """Обробка помилки плагіна"""
        plugin_name = plugin.name if plugin else "Unknown"
        self.logger.error(f"💥 Помилка плагіна {plugin_name}: {error}")

    def _on_task_completed(self, plugin, task, result):
        """Обробка завершення завдання"""
        status = "✅" if result.success else "❌"
        self.logger.info(
            f"{status} Завдання {task.get('type', 'unknown')} плагіном {plugin.name}: {result.message}"
        )


async def main():
    """Головна функція для запуску системи"""
    import argparse

    parser = argparse.ArgumentParser(description="NIMDA Plugin System Runner")
    parser.add_argument(
        "--workspace",
        type=str,
        default=".",
        help="Шлях до робочого простору (за замовчуванням: поточна директорія)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["standard", "optimized"],
        default="optimized",
        help="Режим виконання (за замовчуванням: optimized)",
    )

    args = parser.parse_args()

    # Ініціалізація системи
    runner = NIMDAPluginSystemRunner(args.workspace)

    try:
        # Ініціалізація
        if not await runner.initialize():
            print("❌ Не вдалося ініціалізувати систему плагінів")
            sys.exit(1)

        # Виконання
        if args.mode == "optimized":
            result = await runner.run_optimized_execution()
        else:
            result = await runner.run_dev_plan_execution()

        # Виведення результатів
        print("\n" + "=" * 60)
        print("🎊 ФІНАЛЬНИЙ ЗВІТ ВИКОНАННЯ DEV_PLAN")
        print("=" * 60)
        print(f"Статус: {'✅ УСПІШНО' if result['success'] else '❌ ПОМИЛКИ'}")
        print(f"Повідомлення: {result['message']}")

        if result.get("progress"):
            progress = result["progress"]
            print(
                f"Прогрес: {progress['completed_tasks']}/{progress['total_tasks']} ({progress['progress']:.1%})"
            )

        if result.get("statistics"):
            stats = result["statistics"]
            print(
                f"Статистика: {stats['total_tasks_executed']} завдань, {stats['total_execution_time']:.2f}с"
            )

        print("=" * 60)

        # Завершення
        await runner.shutdown()

        sys.exit(0 if result["success"] else 1)

    except KeyboardInterrupt:
        print("\n⏹️ Виконання перервано користувачем")
        await runner.shutdown()
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Критична помилка: {e}")
        await runner.shutdown()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
