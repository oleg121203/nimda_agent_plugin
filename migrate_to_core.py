#!/usr/bin/env python3
"""
🔄 Міграційний скрипт для організації NIMDA Agent
Безпечне переміщення файлів до модульної структури
"""

import shutil
import sys
from pathlib import Path


def migrate_project():
    """Міграція проекту до нової структури"""
    print("🔄 Початок міграції NIMDA Agent до модульної структури...")

    project_root = Path(__file__).parent

    # Перевірка існування Core модуля
    core_dir = project_root / "Core"
    if not core_dir.exists():
        print("❌ Папка Core не знайдена!")
        return False

    # Перевірка нового файлу
    new_runner = core_dir / "plugin_system_runner.py"
    if not new_runner.exists():
        print("❌ Новий plugin_system_runner.py не знайдений у Core!")
        return False

    # Створення backup директорії
    backup_dir = project_root / ".migration_backup"
    backup_dir.mkdir(exist_ok=True)

    # Перенесення старого файлу
    old_runner = project_root / "run_plugin_system.py"
    if old_runner.exists():
        backup_file = backup_dir / "run_plugin_system_backup.py"
        shutil.copy2(old_runner, backup_file)
        print(f"✅ Створено backup: {backup_file}")

        # Видалення старого файлу
        old_runner.unlink()
        print(f"✅ Видалено старий файл: {old_runner}")

    # Перейменування нового launcher
    new_launcher = project_root / "run_plugin_system_new.py"
    final_launcher = project_root / "run_plugin_system.py"

    if new_launcher.exists():
        shutil.move(str(new_launcher), str(final_launcher))
        print(f"✅ Launcher перейменовано: {final_launcher}")

    print("\n🎊 Міграція завершена успішно!")
    print("📁 Нова структура:")
    print("   ├── Core/plugin_system_runner.py  - основна логіка")
    print("   ├── run_plugin_system.py          - точка входу")
    print("   └── .migration_backup/            - backup файли")

    return True


if __name__ == "__main__":
    try:
        if migrate_project():
            print("\n✅ Проект успішно мігровано до модульної структури!")
            print("💡 Тепер можна безпечно запускати: python run_plugin_system.py")
        else:
            print("\n❌ Міграція не вдалася!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Помилка міграції: {e}")
        sys.exit(1)
