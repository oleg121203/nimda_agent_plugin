"""
NIMDA Agent Core Module
Основні компоненти системи NIMDA Agent

Містить:
- Головний виконавець системи плагінів
- Базові утиліти та сервіси
- Системні інтерфейси
"""

from .plugin_system_runner import NIMDAPluginSystemRunner, main

__all__ = ["NIMDAPluginSystemRunner", "main"]
