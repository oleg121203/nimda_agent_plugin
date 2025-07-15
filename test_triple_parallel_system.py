#!/usr/bin/env python3
"""
🎯 Тест тройної паралельної системи виконання завдань
Демонстрація роботи основного завдання + контроль якості + розширені інструменти
"""

import asyncio
from pathlib import Path

from plugins.dev_plan_executor_plugin import DevPlanExecutorPlugin


async def test_triple_parallel_execution():
    """Тестування тройної паралельної системи"""
    print("🎯 ТЕСТУВАННЯ ТРОЙНОЇ ПАРАЛЕЛЬНОЇ СИСТЕМИ")
    print("=" * 60)

    # Ініціалізація плагіна
    plugin = DevPlanExecutorPlugin(
        {"workspace_path": str(Path.cwd()), "max_parallel_tasks": 3}
    )

    # Симуляція завдань
    test_tasks = [
        {
            "name": "Створити GUI інтерфейс",
            "description": "Розробити користувацький інтерфейс з темною темою",
            "completed": False,
            "status": "pending",
        },
        {
            "name": "Реалізувати AI алгоритм",
            "description": "Створити нейронну мережу для обробки даних",
            "completed": False,
            "status": "pending",
        },
        {
            "name": "Налаштувати систему моніторингу",
            "description": "Встановити метрики продуктивності",
            "completed": False,
            "status": "pending",
        },
    ]

    print(f"📊 Тестуємо {len(test_tasks)} завдання з тройним контролем:")
    print("   1️⃣ Основне виконання (згідно DEV_PLAN)")
    print("   2️⃣ Контроль якості коду")
    print("   3️⃣ Розширені інструменти перевірки")
    print()

    # Виконання тестів
    results = await plugin._execute_triple_parallel_tasks(test_tasks)

    print("📊 РЕЗУЛЬТАТИ ТЕСТУВАННЯ:")
    print("-" * 40)

    overall_success = 0
    total_quality_score = 0

    for i, (task, result) in enumerate(zip(test_tasks, results), 1):
        main_status = "✅" if result["main"].success else "❌"
        quality_status = "✅" if result["quality"].success else "❌"
        tools_status = "✅" if result["tools"].success else "❌"

        quality_score = result["quality_score"]
        total_quality_score += quality_score

        overall_task_success = (
            result["main"].success
            and result["quality"].success
            and result["tools"].success
        )

        if overall_task_success:
            overall_success += 1

        print(f"🎯 Завдання {i}: {task['name']}")
        print(
            f"   Основне: {main_status} | Якість: {quality_status} | Інструменти: {tools_status}"
        )
        print(f"   Оцінка якості: {quality_score:.1f}%")
        print(
            f"   Загальний результат: {'✅ ПРОЙДЕНО' if overall_task_success else '❌ НЕ ПРОЙДЕНО'}"
        )
        print()

    # Підсумкові результати
    success_rate = (overall_success / len(test_tasks)) * 100
    avg_quality = total_quality_score / len(test_tasks)

    print("🏆 ПІДСУМКОВІ РЕЗУЛЬТАТИ:")
    print(
        f"   📈 Успішність: {success_rate:.1f}% ({overall_success}/{len(test_tasks)})"
    )
    print(f"   🎯 Середня якість: {avg_quality:.1f}%")
    print(
        f"   🚀 Статус системи: {'🎊 ВІДМІННО' if success_rate >= 80 else '⚠️ ПОТРЕБУЄ ПОКРАЩЕННЯ'}"
    )

    # Детальна статистика по перевіркам
    print("\n📊 ДЕТАЛЬНА СТАТИСТИКА ПЕРЕВІРОК:")
    quality_checks = ["imports", "linting", "interactions", "structure", "security"]
    tools_checks = [
        "performance",
        "formatting",
        "complexity",
        "coverage",
        "documentation",
        "dependencies",
    ]

    print("   🔍 Контроль якості:")
    for check in quality_checks:
        passed = sum(
            1
            for r in results
            if r["quality"].data
            and r["quality"].data.get("checks", {}).get(check, False)
        )
        print(
            f"      - {check}: {passed}/{len(test_tasks)} ({'✅' if passed >= len(test_tasks) // 2 else '⚠️'})"
        )

    print("   🚀 Розширені інструменти:")
    for check in tools_checks:
        passed = sum(
            1
            for r in results
            if r["tools"].data and r["tools"].data.get("tools", {}).get(check, False)
        )
        print(
            f"      - {check}: {passed}/{len(test_tasks)} ({'✅' if passed >= len(test_tasks) // 2 else '⚠️'})"
        )

    print("\n🎯 ВИСНОВОК:")
    if success_rate >= 80 and avg_quality >= 75:
        print("   🎊 Тройна паралельна система працює ВІДМІННО!")
        print("   ✨ Забезпечено високу якість та контроль коду")
        print("   🚀 Готово до продакшн використання")
    elif success_rate >= 60:
        print("   ⚠️ Система працює, але потребує налаштування")
        print("   🔧 Рекомендовано покращити деякі перевірки")
    else:
        print("   ❌ Потребує серйозного доопрацювання")
        print("   🛠️ Перевірте конфігурацію та залежності")

    return {
        "success_rate": success_rate,
        "avg_quality": avg_quality,
        "results": results,
    }


if __name__ == "__main__":
    asyncio.run(test_triple_parallel_execution())
