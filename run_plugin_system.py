#!/usr/bin/env python3
"""
🚀 NIMDA Agent Plugin System Launcher
Точка входу для системи плагінів NIMDA Agent

Цей файл перенаправляє на основний модуль у Core/
для кращої організації проекту.
"""

import asyncio
import sys
from pathlib import Path

# Додаємо шлях до проекту
sys.path.insert(0, str(Path(__file__).parent))

try:
    from Core.plugin_system_runner import main
except ImportError:
    print("❌ Не вдалося імпортувати Core модуль")
    print("Переконайтеся, що файл Core/plugin_system_runner.py існує")
    sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
