#!/usr/bin/env python3
"""
🚀 NIMDA Workflow Launcher v2.0
Головний лаунчер для NIMDA Agent Workflow System

Цей файл запускає повний workflow NIMDA Agent з інтегрованою системою плагінів.
Включає: Core системи, Plugin Manager, DEV_PLAN Executor та Advanced Tools.

Створено: 15 липня 2025
Архітектура: nimda_src_v2 - Unified Workflow System
"""

import asyncio
import logging
import sys
from pathlib import Path

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("nimda_workflow.log")],
)

logger = logging.getLogger("NIMDA-Workflow-Launcher")


def setup_paths():
    """Налаштування шляхів для імпортів"""
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    return current_dir


async def main():
    """Головна функція запуску NIMDA Workflow"""
    logger.info("🚀 Запуск NIMDA Agent Workflow System v2.0")

    try:
        # Налаштування шляхів
        workflow_dir = setup_paths()
        logger.info(f"📁 Робочий каталог: {workflow_dir}")

        # Імпорт Core системи
        from Core.plugin_system_runner import NIMDAPluginSystemRunner

        # Створення та запуск системи
        system_runner = NIMDAPluginSystemRunner()

        logger.info("🔧 Ініціалізація системи плагінів...")
        await system_runner.initialize()

        logger.info("▶️ Запуск виконання DEV_PLAN...")
        result = await system_runner.run_dev_plan_execution()

        logger.info("🚀 Запуск оптимізованого виконання...")
        optimization_result = await system_runner.run_optimized_execution()

        logger.info("✅ NIMDA Workflow завершено успішно!")
        logger.info(f"📊 Результат DEV_PLAN: {result.get('status', 'Unknown')}")
        logger.info(f"⚡ Оптимізація: {optimization_result.get('status', 'Unknown')}")

    except ImportError as e:
        logger.error(f"❌ Помилка імпорту: {e}")
        logger.error("Перевірте, чи правильно встановлені всі залежності")
        sys.exit(1)

    except Exception as e:
        logger.error(f"❌ Критична помилка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("🌟 NIMDA Agent Workflow System v2.0")
    print("═" * 50)
    print("🎯 Автоматизоване виконання DEV_PLAN")
    print("🔧 Інтегровані плагіни та інструменти")
    print("🚀 Запуск системи...")
    print("═" * 50)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Зупинка системи користувачем")
    except Exception as e:
        print(f"\n❌ Помилка запуску: {e}")
        sys.exit(1)
