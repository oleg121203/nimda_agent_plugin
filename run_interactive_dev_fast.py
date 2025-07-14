#!/usr/bin/env python3
"""
Швидкий запуск інтерактивного воркфлоу NIMDA
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Головна функція"""
    print("🚀 Швидкий запуск інтерактивного воркфлоу NIMDA")
    print("=" * 50)

    # Перевіряємо що ми в правильній папці
    current_dir = Path.cwd()
    project_dir = Path("/Users/dev/Documents/nimda_agent_plugin")

    if current_dir != project_dir:
        print(f"⚠️  Зміна каталогу: {current_dir} -> {project_dir}")
        import os

        os.chdir(project_dir)

    # Запускаємо інтерактивний воркфлоу
    try:
        result = subprocess.run(
            [sys.executable, "interactive_dev_workflow.py"], cwd=project_dir
        )

        return result.returncode

    except KeyboardInterrupt:
        print("\n⚠️  Виконання перервано користувачем")
        return 1

    except Exception as e:
        print(f"❌ Помилка запуску: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
