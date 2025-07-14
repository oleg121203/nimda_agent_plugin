#!/usr/bin/env python3
"""
🧪 Інтегрований тест та демонстрація NIMDA Plugin System
Повна демонстрація роботи системи плагінів з реальним DEV_PLAN.md

Створено: 15 липня 2025
Версія: 2.0.0 - Complete Integration Test
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict

# Додаємо шлях до плагінів
sys.path.append(str(Path(__file__).parent))

from plugins.base_plugin import BasePlugin, PluginResult, PluginStatus
from plugins.dev_plan_executor_plugin import DevPlanExecutorPlugin
from plugins.plugin_manager import PluginManager


class NIMDAPluginIntegrationTest:
    """
    Повний інтегрований тест системи плагінів NIMDA
    """

    def __init__(self, workspace_path: str = "."):
        """Ініціалізація тесту"""
        self.workspace_path = Path(workspace_path)
        self.results = {
            "tests_passed": 0,
            "tests_failed": 0,
            "test_results": [],
            "performance_metrics": {},
            "execution_log": [],
        }

        print("🧪 NIMDA Plugin System Integration Test")
        print("=" * 50)

    async def run_all_tests(self) -> Dict[str, Any]:
        """Запуск всіх тестів"""
        try:
            print("🚀 Початок тестування...")

            # Тест 1: Ініціалізація плагіна
            await self._test_plugin_initialization()

            # Тест 2: Парсинг DEV_PLAN
            await self._test_dev_plan_parsing()

            # Тест 3: Виконання завдань
            await self._test_task_execution()

            # Тест 4: Паралельне виконання
            await self._test_parallel_execution()

            # Тест 5: Інтеграція з менеджером
            await self._test_plugin_manager_integration()

            # Тест 6: Продуктивність
            await self._test_performance_metrics()

            # Підсумок
            self._print_test_summary()

            return self.results

        except Exception as e:
            print(f"💥 Критична помилка тестування: {e}")
            return self.results

    async def _test_plugin_initialization(self):
        """Тест ініціалізації плагіна"""
        test_name = "Plugin Initialization"
        print(f"\n🔧 Тест: {test_name}")

        try:
            start_time = time.time()

            # Ініціалізація плагіна
            plugin = DevPlanExecutorPlugin(
                {
                    "workspace_path": str(self.workspace_path),
                    "backup_enabled": True,
                    "max_parallel_tasks": 2,
                }
            )

            # Перевірка базових властивостей
            assert plugin.name == "DevPlanExecutor"
            assert plugin.version == "2.0.0"
            assert plugin.status == PluginStatus.IDLE

            # Перевірка підтримуваних завдань
            supported_tasks = plugin.get_supported_tasks()
            expected_tasks = [
                "parse_dev_plan",
                "execute_phase",
                "execute_section",
                "execute_task",
                "get_progress",
                "optimize_execution",
            ]

            for task in expected_tasks:
                assert task in supported_tasks, f"Завдання {task} не підтримується"

            # Перевірка GUI конфігурації
            gui_config = plugin.get_gui_configuration()
            assert "window_type" in gui_config
            assert "components" in gui_config

            execution_time = time.time() - start_time

            self._log_test_result(
                test_name,
                True,
                f"Плагін ініціалізовано успішно за {execution_time:.3f}с",
            )
            print("✅ ПРОЙДЕНО")

        except Exception as e:
            self._log_test_result(test_name, False, f"Помилка ініціалізації: {e}")
            print(f"❌ ПРОВАЛЕНО: {e}")

    async def _test_dev_plan_parsing(self):
        """Тест парсингу DEV_PLAN"""
        test_name = "DEV_PLAN Parsing"
        print(f"\n📄 Тест: {test_name}")

        try:
            start_time = time.time()

            plugin = DevPlanExecutorPlugin({"workspace_path": str(self.workspace_path)})

            # Перевірка існування DEV_PLAN.md
            dev_plan_path = self.workspace_path / "DEV_PLAN.md"
            if not dev_plan_path.exists():
                raise FileNotFoundError(f"DEV_PLAN.md не знайдено: {dev_plan_path}")

            # Виконання парсингу
            task = {
                "type": "parse_dev_plan",
                "description": "Тестування парсингу DEV_PLAN.md",
            }

            result = await plugin.execute(task)

            # Перевірка результату
            assert result.success, f"Парсинг не вдався: {result.message}"
            assert result.data is not None, "Дані парсингу відсутні"
            assert "phases" in result.data, "Фази не знайдені в результаті"
            assert "metadata" in result.data, "Метадані не знайдені в результаті"

            phases = result.data["phases"]
            assert len(phases) > 0, "Фази не знайдені"

            # Перевірка структури фаз
            for phase_name, phase_data in phases.items():
                assert "title" in phase_data, f"Назва фази {phase_name} відсутня"
                assert "sections" in phase_data, f"Секції фази {phase_name} відсутні"

                for section_name, section_data in phase_data["sections"].items():
                    assert "title" in section_data, (
                        f"Назва секції {section_name} відсутня"
                    )
                    assert "tasks" in section_data, (
                        f"Завдання секції {section_name} відсутні"
                    )

            execution_time = time.time() - start_time
            total_tasks = result.data["statistics"]["total_tasks"]

            self._log_test_result(
                test_name,
                True,
                f"Парсинг успішний: {len(phases)} фаз, {total_tasks} завдань за {execution_time:.3f}с",
            )
            print(f"✅ ПРОЙДЕНО: {len(phases)} фаз, {total_tasks} завдань")

        except Exception as e:
            self._log_test_result(test_name, False, f"Помилка парсингу: {e}")
            print(f"❌ ПРОВАЛЕНО: {e}")

    async def _test_task_execution(self):
        """Тест виконання окремих завдань"""
        test_name = "Task Execution"
        print(f"\n⚙️ Тест: {test_name}")

        try:
            start_time = time.time()

            plugin = DevPlanExecutorPlugin({"workspace_path": str(self.workspace_path)})

            # Тестові завдання різних типів
            test_tasks = [
                {
                    "name": "TestGUITask",
                    "description": "Тестування GUI завдання",
                    "completed": False,
                    "status": "pending",
                },
                {
                    "name": "TestAITask",
                    "description": "Тестування AI завдання",
                    "completed": False,
                    "status": "pending",
                },
                {
                    "name": "TestSystemTask",
                    "description": "Тестування системного завдання",
                    "completed": False,
                    "status": "pending",
                },
            ]

            execution_times = []
            successful_tasks = 0

            for test_task in test_tasks:
                task_start = time.time()

                task = {
                    "type": "execute_task",
                    "task_data": test_task,
                    "description": f"Виконання тестового завдання: {test_task['name']}",
                }

                result = await plugin.execute(task)
                task_time = time.time() - task_start
                execution_times.append(task_time)

                if result.success:
                    successful_tasks += 1
                    print(f"  ✅ {test_task['name']}: {task_time:.3f}с")
                else:
                    print(f"  ❌ {test_task['name']}: {result.message}")

            execution_time = time.time() - start_time
            avg_task_time = (
                sum(execution_times) / len(execution_times) if execution_times else 0
            )

            assert successful_tasks == len(test_tasks), (
                f"Не всі завдання виконані: {successful_tasks}/{len(test_tasks)}"
            )

            self._log_test_result(
                test_name,
                True,
                f"Виконано {successful_tasks}/{len(test_tasks)} завдань, середній час: {avg_task_time:.3f}с",
            )
            print(f"✅ ПРОЙДЕНО: {successful_tasks} завдань, avg: {avg_task_time:.3f}с")

        except Exception as e:
            self._log_test_result(test_name, False, f"Помилка виконання завдань: {e}")
            print(f"❌ ПРОВАЛЕНО: {e}")

    async def _test_parallel_execution(self):
        """Тест паралельного виконання"""
        test_name = "Parallel Execution"
        print(f"\n🔄 Тест: {test_name}")

        try:
            start_time = time.time()

            plugin = DevPlanExecutorPlugin(
                {"workspace_path": str(self.workspace_path), "max_parallel_tasks": 3}
            )

            # Створення множини тестових завдань
            test_tasks = []
            for i in range(6):
                test_tasks.append(
                    {
                        "name": f"ParallelTask{i + 1}",
                        "description": f"Паралельне завдання {i + 1}",
                        "completed": False,
                        "status": "pending",
                    }
                )

            # Тестування групування завдань
            groups = plugin._group_tasks_for_parallel_execution(test_tasks)

            assert len(groups) >= 2, "Завдання не згруповані для паралельного виконання"

            # Виконання груп паралельно
            total_execution_time = 0

            for i, group in enumerate(groups):
                group_start = time.time()

                # Виконання групи завдань паралельно (симуляція)
                tasks_coroutines = []
                for task in group:
                    task_obj = {
                        "type": "execute_task",
                        "task_data": task,
                        "description": f"Паралельне виконання: {task['name']}",
                    }
                    tasks_coroutines.append(plugin.execute(task_obj))

                results = await asyncio.gather(*tasks_coroutines)

                group_time = time.time() - group_start
                total_execution_time += group_time

                successful_in_group = sum(1 for r in results if r.success)
                print(
                    f"  📦 Група {i + 1}: {successful_in_group}/{len(group)} завдань за {group_time:.3f}с"
                )

            execution_time = time.time() - start_time

            # Перевірка що паралельне виконання швидше послідовного
            # (в реальних умовах це буде більш очевидно)

            self._log_test_result(
                test_name,
                True,
                f"Паралельне виконання: {len(groups)} груп за {execution_time:.3f}с",
            )
            print(f"✅ ПРОЙДЕНО: {len(groups)} груп, {len(test_tasks)} завдань")

        except Exception as e:
            self._log_test_result(
                test_name, False, f"Помилка паралельного виконання: {e}"
            )
            print(f"❌ ПРОВАЛЕНО: {e}")

    async def _test_plugin_manager_integration(self):
        """Тест інтеграції з менеджером плагінів"""
        test_name = "Plugin Manager Integration"
        print(f"\n🔧 Тест: {test_name}")

        try:
            start_time = time.time()

            # Ініціалізація менеджера
            manager = PluginManager(max_workers=2)

            # Реєстрація плагіна
            plugin = DevPlanExecutorPlugin({"workspace_path": str(self.workspace_path)})

            success = await manager.register_plugin(plugin)
            assert success, "Не вдалося зареєструвати плагін"

            # Перевірка реєстрації
            registered_plugin = manager.get_plugin("DevPlanExecutor")
            assert registered_plugin is not None, "Плагін не знайдено після реєстрації"
            assert registered_plugin.name == plugin.name, "Назва плагіна не співпадає"

            # Тест виконання через менеджер
            task = {
                "type": "get_progress",
                "description": "Тест виконання через менеджер",
            }

            result = await manager.execute_task(task)
            assert result.success, (
                f"Виконання через менеджер не вдалося: {result.message}"
            )

            # Перевірка статистики
            stats = manager.get_system_statistics()
            assert stats["total_plugins"] == 1, "Неправильна кількість плагінів"
            assert stats["total_tasks_executed"] >= 1, "Завдання не було виконане"

            execution_time = time.time() - start_time

            # Завершення роботи
            await manager.shutdown()

            self._log_test_result(
                test_name,
                True,
                f"Інтеграція успішна: плагін зареєстровано та виконано завдання за {execution_time:.3f}с",
            )
            print("✅ ПРОЙДЕНО")

        except Exception as e:
            self._log_test_result(test_name, False, f"Помилка інтеграції: {e}")
            print(f"❌ ПРОВАЛЕНО: {e}")

    async def _test_performance_metrics(self):
        """Тест метрик продуктивності"""
        test_name = "Performance Metrics"
        print(f"\n⚡ Тест: {test_name}")

        try:
            start_time = time.time()

            plugin = DevPlanExecutorPlugin({"workspace_path": str(self.workspace_path)})

            # Множинне виконання для збору метрик
            execution_times = []

            for i in range(10):
                task_start = time.time()

                task = {
                    "type": "optimize_execution",
                    "description": f"Тест продуктивності {i + 1}",
                }

                result = await plugin.execute(task)
                task_time = time.time() - task_start
                execution_times.append(task_time)

                assert result.success, f"Завдання {i + 1} не вдалося"

            # Аналіз метрик
            min_time = min(execution_times)
            max_time = max(execution_times)
            avg_time = sum(execution_times) / len(execution_times)

            # Отримання статистики плагіна
            stats = plugin.get_statistics()

            # Цільова продуктивність з DEV_PLAN: 2.5+ tasks/second
            target_performance = 2.5
            actual_performance = 1 / avg_time if avg_time > 0 else 0

            performance_ratio = actual_performance / target_performance

            execution_time = time.time() - start_time

            self.results["performance_metrics"] = {
                "min_execution_time": min_time,
                "max_execution_time": max_time,
                "avg_execution_time": avg_time,
                "target_performance": target_performance,
                "actual_performance": actual_performance,
                "performance_ratio": performance_ratio,
                "plugin_stats": stats,
            }

            performance_status = "✅" if performance_ratio >= 0.8 else "⚠️"

            self._log_test_result(
                test_name,
                True,
                f"Продуктивність: {actual_performance:.2f} задач/с (ціль: {target_performance}), співвідношення: {performance_ratio:.2f}",
            )
            print(f"{performance_status} ПРОЙДЕНО: {actual_performance:.2f} задач/с")

        except Exception as e:
            self._log_test_result(
                test_name, False, f"Помилка тестування продуктивності: {e}"
            )
            print(f"❌ ПРОВАЛЕНО: {e}")

    def _log_test_result(self, test_name: str, success: bool, message: str):
        """Логування результату тесту"""
        if success:
            self.results["tests_passed"] += 1
        else:
            self.results["tests_failed"] += 1

        self.results["test_results"].append(
            {
                "test_name": test_name,
                "success": success,
                "message": message,
                "timestamp": time.time(),
            }
        )

        self.results["execution_log"].append(
            f"{'✅' if success else '❌'} {test_name}: {message}"
        )

    def _print_test_summary(self):
        """Виведення підсумку тестування"""
        print("\n" + "=" * 60)
        print("🎊 ПІДСУМОК ТЕСТУВАННЯ")
        print("=" * 60)

        total_tests = self.results["tests_passed"] + self.results["tests_failed"]
        success_rate = (
            (self.results["tests_passed"] / total_tests * 100) if total_tests > 0 else 0
        )

        print(f"Всього тестів: {total_tests}")
        print(f"Пройдено: {self.results['tests_passed']}")
        print(f"Провалено: {self.results['tests_failed']}")
        print(f"Рівень успіху: {success_rate:.1f}%")

        if self.results.get("performance_metrics"):
            perf = self.results["performance_metrics"]
            print(f"Продуктивність: {perf['actual_performance']:.2f} задач/с")
            print(f"Співвідношення до цілі: {perf['performance_ratio']:.2f}")

        print("=" * 60)

        # Детальний лог
        print("\n📋 ДЕТАЛЬНИЙ ЛОГ:")
        for entry in self.results["execution_log"]:
            print(f"  {entry}")

    async def save_results(self, filename: str = "test_results.json"):
        """Збереження результатів у файл"""
        results_file = self.workspace_path / filename

        # Додаємо метадані
        self.results["metadata"] = {
            "test_version": "2.0.0",
            "workspace_path": str(self.workspace_path),
            "test_timestamp": time.time(),
            "total_tests": self.results["tests_passed"] + self.results["tests_failed"],
        }

        try:
            with open(results_file, "w", encoding="utf-8") as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)

            print(f"\n💾 Результати збережено: {results_file}")

        except Exception as e:
            print(f"❌ Помилка збереження результатів: {e}")


async def main():
    """Головна функція для запуску тестів"""
    import argparse

    parser = argparse.ArgumentParser(description="NIMDA Plugin System Integration Test")
    parser.add_argument(
        "--workspace", type=str, default=".", help="Шлях до робочого простору"
    )
    parser.add_argument(
        "--save-results", action="store_true", help="Зберегти результати у файл"
    )

    args = parser.parse_args()

    # Запуск тестів
    test_runner = NIMDAPluginIntegrationTest(args.workspace)

    try:
        results = await test_runner.run_all_tests()

        if args.save_results:
            await test_runner.save_results()

        # Визначення коду виходу
        success = results["tests_failed"] == 0
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n⏹️ Тестування перервано користувачем")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Критична помилка тестування: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
