# 🚀 NIMDA Agent Workflow System v2.0

## 📖 Опис

NIMDA Agent Workflow System v2.0 - це повний уніфікований workflow для автоматизованого виконання планів розробки з інтегрованою системою плагінів.

## 🏗️ Архітектура

```
nimda_src_v2/
├── nimda_workflow_launcher.py   # 🚀 Головний лаунчер системи
├── Core/                        # 🔧 Основна система
│   ├── __init__.py             
│   ├── plugin_system_runner.py # 🏃 Виконавець системи плагінів
│   └── README.md               
├── plugins/                     # 🔌 Система плагінів
│   ├── __init__.py             
│   ├── base_plugin.py          # 📄 Базовий клас плагінів
│   ├── plugin_manager.py       # 🎛️ Менеджер плагінів
│   ├── dev_plan_executor_plugin.py  # 📋 Виконавець DEV_PLAN
│   └── advanced_tools_plugin.py     # 🛠️ Розширені інструменти
└── README.md                    # 📚 Ця документація
```

## 🎯 Ключові особливості

### 🔧 Core система
- **Plugin System Runner** - Головний виконавець з AI оптимізацією
- **Автоматичне виконання DEV_PLAN** - Повністю автоматизований process
- **Глибока інтеграція** - Seamless интеграція всіх компонентів

### 🔌 Система плагінів
- **Base Plugin** - Універсальний базовий клас для всіх плагінів
- **Plugin Manager** - Централізоване управління плагінами
- **DEV_PLAN Executor** - Спеціалізований плагін для виконання планів розробки
- **Advanced Tools** - AI-enhanced інструменти та метрики

### 🎮 DEV_PLAN Executor особливості
- **Тройне паралельне виконання** - Основне завдання + Контроль якості + Розширені інструменти
- **Адаптивне управління завантаженням** - Автоматична оптимізація продуктивності
- **GUI інтеграція** - Real-time відображення прогресу
- **Глибокий контроль якості** - 15+ перевірок якості коду

## 🚀 Швидкий старт

### 1. Запуск системи

```bash
python3 nimda_workflow_launcher.py
```

### 2. Програмний запуск

```python
import asyncio
from Core.plugin_system_runner import NIMDAPluginSystemRunner

async def run_workflow():
    system = NIMDAPluginSystemRunner()
    await system.initialize()
    result = await system.run_dev_plan_execution()
    return result

# Запуск
result = asyncio.run(run_workflow())
```

## 📋 Вимоги

- Python 3.8+
- asyncio
- pathlib
- logging

## 🔧 Конфігурація

Система автоматично налаштовується, але ви можете кастомізувати:

```python
config = {
    "workspace_path": "./my_project",
    "max_parallel_tasks": 5,
    "backup_enabled": True,
    "gui_enabled": True
}

system = NIMDAPluginSystemRunner(config=config)
```

## 🎯 Основні операції

### Виконання DEV_PLAN

```python
# Парсинг DEV_PLAN.md
await system.execute_task({
    "type": "parse_dev_plan"
})

# Виконання конкретної фази
await system.execute_task({
    "type": "execute_phase",
    "phase_name": "Phase 1"
})

# Отримання прогресу
progress = await system.execute_task({
    "type": "get_progress"
})
```

### Контроль якості

Автоматично виконується тройна перевірка:
- 🎯 **Основне завдання** - Виконання згідно DEV_PLAN
- 🔍 **Контроль якості** - Імпорти, лінтери, взаємодія модулів
- 🚀 **Розширені інструменти** - Продуктивність, документація, тести

## 📊 Моніторинг

Система веде детальний лог:
- `nimda_workflow.log` - Загальний лог workflow
- Real-time GUI updates - Прогрес виконання
- Performance метрики - Автоматична оптимізація

## 🛠️ Розробка

### Додавання нового плагіна

1. Наслідуйте від `BasePlugin`:

```python
from plugins.base_plugin import BasePlugin, PluginResult

class MyPlugin(BasePlugin):
    async def execute(self, task, context=None):
        # Ваша логіка
        return PluginResult(success=True, message="Done")
```

2. Зареєструйте в системі:

```python
system.plugin_manager.register_plugin("my_plugin", MyPlugin())
```

## 📈 Статистика продуктивності

- **Цільова продуктивність**: 0.8+ завдань/секунду
- **Паралельне виконання**: до 5 завдань одночасно
- **Контроль якості**: 15+ автоматичних перевірок
- **AI оптимізація**: Adaptive performance tuning

## 🔒 Безпека

- Автоматичне сканування вразливостей
- Перевірка небезпечних паттернів коду
- Контроль безпеки імпортів
- Ліцензійний аудит залежностей

## 📞 Підтримка

Для питань та покращень створюйте issues в репозиторії.

---

**Створено**: 15 липня 2025  
**Версія**: 2.0.0  
**Статус**: Production Ready 🚀
