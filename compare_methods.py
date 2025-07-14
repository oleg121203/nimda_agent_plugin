#!/usr/bin/env python3
"""
Порівняння прямого виклику методів VS команди codex
"""

import sys
import time

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

import subprocess
from pathlib import Path

from dev_plan_manager import DevPlanManager


def test_direct_methods():
    """Тест прямого виклику методів"""
    print("🔧 ТЕСТ 1: Прямий виклик методів")
    print("-" * 40)

    project_path = Path("/Users/dev/Documents/nimda_agent_plugin")
    manager = DevPlanManager(project_path)

    # Створюємо файли прямо
    manager._create_chat_agent()
    manager._create_worker_agent()

    # Перевіряємо результат
    chat_exists = Path("chat_agent.py").exists()
    worker_exists = Path("worker_agent.py").exists()

    print(f"   chat_agent.py створено: {'✅' if chat_exists else '❌'}")
    print(f"   worker_agent.py створено: {'✅' if worker_exists else '❌'}")

    return chat_exists and worker_exists


def test_codex_command():
    """Тест команди codex"""
    print("\n🤖 ТЕСТ 2: Команда codex run full dev")
    print("-" * 40)

    # Видаляємо файли перед тестом
    if Path("chat_agent.py").exists():
        Path("chat_agent.py").unlink()
    if Path("worker_agent.py").exists():
        Path("worker_agent.py").unlink()

    # Перевіряємо що файли видалені
    print("   Файли видалені для тесту...")

    # Запускаємо команду codex
    result = subprocess.run(
        ["python", "main.py", "codex", "run", "full", "dev"],
        capture_output=True,
        text=True,
    )

    print(f"   Команда виконана з кодом: {result.returncode}")

    # Перевіряємо результат
    chat_exists = Path("chat_agent.py").exists()
    worker_exists = Path("worker_agent.py").exists()

    print(f"   chat_agent.py створено: {'✅' if chat_exists else '❌'}")
    print(f"   worker_agent.py створено: {'✅' if worker_exists else '❌'}")

    return chat_exists and worker_exists


def main():
    print("🧪 ПОРІВНЯННЯ МЕТОДІВ СТВОРЕННЯ ФАЙЛІВ")
    print("=" * 50)

    # Видаляємо всі файли для чистого тесту
    for filename in [
        "chat_agent.py",
        "worker_agent.py",
        "adaptive_thinker.py",
        "learning_module.py",
        "macos_integration.py",
    ]:
        if Path(filename).exists():
            Path(filename).unlink()

    # Тест 1: Прямі методи
    direct_success = test_direct_methods()

    # Тест 2: Команда codex
    codex_success = test_codex_command()

    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТИ:")
    print(f"   Прямі методи: {'✅ ПРАЦЮЮТЬ' if direct_success else '❌ НЕ ПРАЦЮЮТЬ'}")
    print(f"   Команда codex: {'✅ ПРАЦЮЄ' if codex_success else '❌ НЕ ПРАЦЮЄ'}")

    if direct_success and not codex_success:
        print("\n⚠️  ВИСНОВОК: Команда codex НЕ викликає реальні методи створення!")
        print(
            "   Потрібно виправити логіку в command_processor.py або dev_plan_manager.py"
        )
    elif direct_success and codex_success:
        print("\n✅ ВИСНОВОК: Обидва методи працюють!")
    else:
        print("\n❌ ВИСНОВОК: Є проблеми з обома методами!")


if __name__ == "__main__":
    main()
