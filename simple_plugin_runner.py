#!/usr/bin/env python3
"""
🚀 NIMDA Plugin System - Простий запускач
Демонстрація роботи системи плагінів без складних залежностей

Створено: 15 липня 2025
Версія: 2.0.0 - Simple Runner
"""

import asyncio
import json
import sys
import time
from pathlib import Path

# Додаємо шлях до плагінів
sys.path.append(str(Path(__file__).parent))

from plugins.dev_plan_executor_plugin import DevPlanExecutorPlugin


class SimpleNIMDARunner:
    """
    Простий запускач для демонстрації NIMDA плагіна
    """

    def __init__(self, workspace_path: str = "."):
        """Ініціалізація"""
        self.workspace_path = Path(workspace_path)
        self.plugin = None

        print("🚀 NIMDA Plugin System - Простий запускач")
        print("=" * 50)

    async def run_demo(self):
        """Запуск демонстрації"""
        try:
            # Ініціалізація плагіна
            print("🔧 Ініціалізація плагіна...")
            self.plugin = DevPlanExecutorPlugin(
                {
                    "workspace_path": str(self.workspace_path),
                    "backup_enabled": True,
                    "max_parallel_tasks": 2,
                }
            )

            # Демонстрація основних функцій
            await self._demo_parsing()
            await self._demo_task_execution()
            await self._demo_performance()

            print("\n🎊 Демонстрація завершена успішно!")

        except Exception as e:
            print(f"💥 Помилка демонстрації: {e}")

    async def _demo_parsing(self):
        """Демонстрація парсингу DEV_PLAN"""
        print("\n📄 Демонстрація парсингу DEV_PLAN...")

        try:
            task = {
                "type": "parse_dev_plan",
                "description": "Парсинг DEV_PLAN.md для демонстрації",
            }

            start_time = time.time()
            result = await self.plugin.execute(task)
            execution_time = time.time() - start_time

            if result.success:
                phases = result.data.get("phases", {})
                total_tasks = result.data.get("statistics", {}).get("total_tasks", 0)

                print(f"✅ Парсинг успішний за {execution_time:.3f}с")
                print(f"   📊 Знайдено: {len(phases)} фаз, {total_tasks} завдань")

                # Виведення короткої інформації про фази
                for phase_name, phase_data in list(phases.items())[
                    :3
                ]:  # Показуємо перші 3 фази
                    sections_count = len(phase_data.get("sections", {}))
                    print(
                        f"   🎯 {phase_name}: {phase_data['title']} ({sections_count} секцій)"
                    )

                if len(phases) > 3:
                    print(f"   ... і ще {len(phases) - 3} фаз")

            else:
                print(f"❌ Помилка парсингу: {result.message}")

        except Exception as e:
            print(f"💥 Помилка демонстрації парсингу: {e}")

    async def _demo_task_execution(self):
        """Демонстрація виконання завдань"""
        print("\n⚙️ Демонстрація виконання завдань...")

        try:
            # Тестові завдання різних типів
            demo_tasks = [
                {
                    "name": "HyperGlassUI",
                    "description": "Демонстрація GUI завдання - Ultra-realistic glassmorphism",
                    "completed": False,
                    "status": "pending",
                },
                {
                    "name": "NeuralNetworkEngine",
                    "description": "Демонстрація AI завдання - Deep learning engine",
                    "completed": False,
                    "status": "pending",
                },
                {
                    "name": "AdvancedEncryption",
                    "description": "Демонстрація системного завдання - Military-grade encryption",
                    "completed": False,
                    "status": "pending",
                },
            ]

            print("🔄 Виконання демонстраційних завдань...")

            execution_times = []

            for i, demo_task in enumerate(demo_tasks, 1):
                task = {
                    "type": "execute_task",
                    "task_data": demo_task,
                    "description": f"Демонстрація завдання {i}",
                }

                start_time = time.time()
                result = await self.plugin.execute(task)
                execution_time = time.time() - start_time
                execution_times.append(execution_time)

                status = "✅" if result.success else "❌"
                print(f"   {status} {demo_task['name']}: {execution_time:.3f}с")

            avg_time = (
                sum(execution_times) / len(execution_times) if execution_times else 0
            )
            tasks_per_second = 1 / avg_time if avg_time > 0 else 0

            print(f"\n📈 Статистика виконання:")
            print(f"   ⏱️ Середній час завдання: {avg_time:.3f}с")
            print(f"   🚀 Продуктивність: {tasks_per_second:.2f} завдань/с")

            # Порівняння з цільовою продуктивністю (2.5+ задач/с з DEV_PLAN)
            target_performance = 2.5
            if tasks_per_second >= target_performance:
                print(f"   🎯 ЦІЛЬ ДОСЯГНУТА! (≥{target_performance} завдань/с)")
            else:
                ratio = (tasks_per_second / target_performance) * 100
                print(
                    f"   📊 Прогрес до цілі: {ratio:.1f}% від {target_performance} завдань/с"
                )

        except Exception as e:
            print(f"💥 Помилка демонстрації виконання: {e}")

    async def _demo_performance(self):
        """Демонстрація метрик продуктивності"""
        print("\n⚡ Демонстрація оптимізації продуктивності...")

        try:
            # Отримання поточної статистики
            stats = self.plugin.get_statistics()

            print("📊 Статистика плагіна:")
            print(f"   👤 Назва: {stats['name']} v{stats['version']}")
            print(f"   📈 Виконано завдань: {stats['execution_count']}")
            print(f"   ✅ Успішних: {stats['success_count']}")
            print(f"   ❌ Помилок: {stats['error_count']}")
            print(f"   🎯 Рівень успіху: {stats['success_rate']}%")
            print(f"   ⏱️ Загальний час: {stats['total_execution_time']}с")
            print(f"   📊 Середній час: {stats['average_execution_time']}с")

            # Тест оптимізації
            print("\n🔧 Тестування оптимізації...")

            task = {
                "type": "optimize_execution",
                "description": "Демонстрація оптимізації продуктивності",
            }

            result = await self.plugin.execute(task)

            if result.success:
                print(f"✅ Оптимізація виконана: {result.message}")
                if result.data:
                    max_parallel = result.data.get("max_parallel_tasks", "N/A")
                    avg_time = result.data.get("average_task_time", "N/A")
                    print(f"   🔄 Паралельні завдання: {max_parallel}")
                    print(f"   ⏱️ Середній час завдання: {avg_time}")
            else:
                print(f"❌ Помилка оптимізації: {result.message}")

        except Exception as e:
            print(f"💥 Помилка демонстрації продуктивності: {e}")

    async def run_quick_test(self):
        """Швидкий тест основних функцій"""
        print("\n🧪 Швидкий тест функціональності...")

        try:
            # Ініціалізація
            self.plugin = DevPlanExecutorPlugin(
                {"workspace_path": str(self.workspace_path)}
            )

            # Тести
            tests = [
                ("parse_dev_plan", "Парсинг DEV_PLAN"),
                ("get_progress", "Отримання прогресу"),
                ("optimize_execution", "Оптимізація"),
            ]

            passed = 0

            for test_type, test_name in tests:
                try:
                    task = {
                        "type": test_type,
                        "description": f"Швидкий тест: {test_name}",
                    }

                    result = await self.plugin.execute(task)

                    if result.success:
                        print(f"   ✅ {test_name}")
                        passed += 1
                    else:
                        print(f"   ❌ {test_name}: {result.message}")

                except Exception as e:
                    print(f"   💥 {test_name}: {e}")

            print(f"\n📊 Результат тестування: {passed}/{len(tests)} тестів пройдено")

            if passed == len(tests):
                print("🎊 Всі базові функції працюють!")
            else:
                print("⚠️ Деякі функції потребують перевірки")

        except Exception as e:
            print(f"💥 Помилка швидкого тесту: {e}")


async def main():
    """Головна функція"""
    import argparse

    parser = argparse.ArgumentParser(description="NIMDA Plugin Simple Runner")
    parser.add_argument(
        "--workspace", type=str, default=".", help="Шлях до робочого простору"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["demo", "test"],
        default="demo",
        help="Режим роботи: demo - повна демонстрація, test - швидкий тест",
    )

    args = parser.parse_args()

    # Перевірка DEV_PLAN.md
    dev_plan_path = Path(args.workspace) / "DEV_PLAN.md"
    if not dev_plan_path.exists():
        print(f"⚠️ УВАГА: DEV_PLAN.md не знайдено за шляхом: {dev_plan_path}")
        print("   Деякі функції можуть працювати некоректно")
        print()

    # Запуск
    runner = SimpleNIMDARunner(args.workspace)

    try:
        if args.mode == "demo":
            await runner.run_demo()
        else:
            await runner.run_quick_test()

    except KeyboardInterrupt:
        print("\n⏹️ Роботу перервано користувачем")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Критична помилка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
