# 🔌 NIMDA Agent Plugin System Documentation

## 📖 Огляд

Система плагінів NIMDA Agent - це потужна архітектура для розширення функціональності агента через модульні компоненти. Система забезпечує глибоку інтеграцію, адаптивну продуктивність та інтелектуальне управління завданнями.

## 🏗️ Архітектура

### Основні компоненти:

#### 1. BasePlugin (Базовий клас плагіна)
- Абстрактний базовий клас для всіх плагінів
- Стандартизує інтерфейс та життєвий цикл
- Забезпечує інтеграцію з GUI та моніторинг

#### 2. PluginManager (Менеджер плагінів)  
- Управління життєвим циклом плагінів
- Автоматичне завантаження та реєстрація
- Розподіл завдань між плагінами
- Моніторинг продуктивності

#### 3. DevPlanExecutorPlugin (Плагін виконання DEV_PLAN)
- Спеціалізований плагін для виконання завдань з DEV_PLAN.md
- Парсинг структури плану розробки
- Паралельне виконання завдань
- Адаптивна оптимізація продуктивності

## 🚀 Основні можливості

### ⚡ Продуктивність
- **Цільова продуктивність**: 2.5+ завдань/секунду
- **Паралельне виконання**: До 5 одночасних завдань
- **Адаптивна оптимізація**: Автоматичне підлаштування параметрів
- **Кешування**: Оптимізація повторних операцій

### 🎮 GUI Інтеграція
- **Адаптивні панелі**: Динамічне масштабування вікон
- **Прогрес-індикатори**: Візуалізація виконання завдань
- **Тематизація**: Підтримка dark/neon тем
- **Інтерактивність**: Управління через GUI

### 🧠 Інтелектуальність
- **Автоматичний парсинг**: Розуміння структури DEV_PLAN
- **Типізація завдань**: Розпізнавання GUI, AI, системних завдань
- **Контекстне виконання**: Врахування залежностей завдань
- **Самооптимізація**: Покращення продуктивності на основі досвіду

## 📋 Підтримувані типи завдань

### 1. `parse_dev_plan`
Парсинг файлу DEV_PLAN.md та витягування структури фаз і завдань.

```python
task = {
    'type': 'parse_dev_plan',
    'description': 'Парсинг DEV_PLAN.md файлу'
}
```

### 2. `execute_phase`
Виконання цілої фази розробки з усіма секціями.

```python
task = {
    'type': 'execute_phase',
    'phase_name': 'Phase 8',
    'description': 'Виконання Phase 8: Revolutionary GUI System'
}
```

### 3. `execute_section`
Виконання конкретної секції всередині фази.

```python
task = {
    'type': 'execute_section',
    'phase_name': 'Phase 8',
    'section_name': '8.1',
    'description': 'Виконання секції 8.1: Advanced Visual Engine'
}
```

### 4. `execute_task`
Виконання окремого завдання.

```python
task = {
    'type': 'execute_task',
    'task_data': {
        'name': 'HyperGlassUI',
        'description': 'Ultra-realistic glassmorphism implementation',
        'completed': False
    }
}
```

### 5. `get_progress`
Отримання поточного прогресу виконання.

```python
task = {
    'type': 'get_progress',
    'description': 'Отримання статистики прогресу'
}
```

### 6. `optimize_execution`
Оптимізація параметрів виконання для покращення продуктивності.

```python
task = {
    'type': 'optimize_execution',
    'description': 'Адаптивна оптимізація продуктивності'
}
```

## 🛠️ Використання

### Базовий приклад

```python
from plugins.dev_plan_executor_plugin import DevPlanExecutorPlugin

# Ініціалізація плагіна
plugin = DevPlanExecutorPlugin({
    'workspace_path': '/path/to/project',
    'backup_enabled': True,
    'max_parallel_tasks': 3
})

# Виконання завдання
task = {
    'type': 'parse_dev_plan',
    'description': 'Парсинг плану розробки'
}

result = await plugin.execute(task)

if result.success:
    print(f"Успіх: {result.message}")
    print(f"Дані: {result.data}")
else:
    print(f"Помилка: {result.message}")
```

### Використання з менеджером

```python
from plugins.plugin_manager import PluginManager
from plugins.dev_plan_executor_plugin import DevPlanExecutorPlugin

# Ініціалізація менеджера
manager = PluginManager(max_workers=4)

# Реєстрація плагіна
plugin = DevPlanExecutorPlugin()
await manager.register_plugin(plugin)

# Виконання завдання через менеджер
task = {'type': 'get_progress'}
result = await manager.execute_task(task)
```

## 🔧 Конфігурація

### Параметри DevPlanExecutorPlugin

| Параметр | Тип | За замовчуванням | Опис |
|----------|-----|------------------|------|
| `workspace_path` | str | "." | Шлях до робочого простору |
| `backup_enabled` | bool | True | Увімкнення автоматичних бекапів |
| `max_parallel_tasks` | int | 3 | Максимум паралельних завдань |

### GUI Конфігурація

```python
gui_config = plugin.get_gui_configuration()

# Результат:
{
    'window_type': 'adaptive_panel',
    'position': 'center',
    'size': {'width': 800, 'height': 600},
    'transparency': 0.9,
    'theme': 'dark_neon',
    'components': [
        {'type': 'progress_bar', 'id': 'main_progress'},
        {'type': 'phase_selector', 'id': 'phase_list'},
        {'type': 'task_grid', 'id': 'task_overview'},
        {'type': 'performance_chart', 'id': 'performance_metrics'}
    ]
}
```

## 📊 Моніторинг та статистика

### Статистика плагіна

```python
stats = plugin.get_statistics()

# Приклад результату:
{
    'name': 'DevPlanExecutor',
    'version': '2.0.0',
    'status': 'completed',
    'execution_count': 42,
    'success_count': 40,
    'error_count': 2,
    'success_rate': 95.24,
    'total_execution_time': 12.45,
    'average_execution_time': 0.296
}
```

### Системна статистика

```python
system_stats = manager.get_system_statistics()

# Приклад результату:
{
    'total_plugins': 1,
    'active_plugins': 0,
    'total_tasks_executed': 42,
    'total_execution_time': 12.45,
    'average_execution_time': 0.296,
    'plugin_statistics': [...]
}
```

## 🚀 Запуск

### Простий запускач

```bash
# Демонстрація всіх функцій
python simple_plugin_runner.py --mode demo

# Швидкий тест
python simple_plugin_runner.py --mode test

# З вказанням робочого простору
python simple_plugin_runner.py --workspace /path/to/project
```

### Повний запускач системи

```bash
# Стандартний режим
python run_plugin_system.py

# Оптимізований режим
python run_plugin_system.py --mode optimized

# З кастомним робочим простором
python run_plugin_system.py --workspace /path/to/project
```

### Інтеграційні тести

```bash
# Запуск всіх тестів
python test_plugin_integration.py

# З збереженням результатів
python test_plugin_integration.py --save-results

# З кастомним робочим простором
python test_plugin_integration.py --workspace /path/to/project
```

## 🎯 Результати виконання

### PluginResult структура

```python
@dataclass
class PluginResult:
    success: bool                    # Успішність виконання
    message: str                     # Повідомлення про результат
    data: Optional[Dict[str, Any]]   # Дані результату (опціонально)
    execution_time: Optional[float]  # Час виконання (опціонально)
    error: Optional[Exception]       # Помилка (якщо є)
```

## 📈 Продуктивність

### Цільові показники (з DEV_PLAN v5.0)

- **Продуктивність виконання**: 2.5+ завдань/секунду
- **Час запуску**: < 2 секунди
- **Час відгуку GUI**: < 16ms (60+ FPS)
- **Використання пам'яті**: < 512MB базове споживання

### Оптимізація

Система автоматично оптимізує продуктивність на основі:
- Середнього часу виконання завдань
- Завантаження системи
- Типу завдань
- Доступних ресурсів

## 🔍 Налагодження

### Логування

Система використовує стандартне Python логування:

```python
import logging

# Увімкнення детального логування
logging.basicConfig(level=logging.DEBUG)

# Або тільки для плагінів
logging.getLogger("Plugin").setLevel(logging.DEBUG)
```

### Типові проблеми

1. **DEV_PLAN.md не знайдено**
   - Перевірте шлях до файлу
   - Переконайтеся що файл існує та доступний для читання

2. **Низька продуктивність**
   - Запустіть оптимізацію: `optimize_execution`
   - Зменште `max_parallel_tasks`
   - Перевірте системні ресурси

3. **Помилки парсингу**
   - Перевірте формат DEV_PLAN.md
   - Переконайтеся в коректності markdown структури

## 🔮 Розвиток

### Планові покращення

1. **SSH Plugin Integration**
   - Інтеграція з SSH плагіном для віддаленого виконання
   - Підтримка MikroTik, Linux, Cisco пристроїв

2. **Advanced AI Features**
   - Машинне навчання для оптимізації
   - Передбачення помилок
   - Автоматичне покращення алгоритмів

3. **Enhanced GUI**
   - Покращена візуалізація прогресу
   - Інтерактивне управління завданнями
   - Кастомізація інтерфейсу

### Розширення

Для створення власного плагіна:

1. Наслідуйте `BasePlugin`
2. Реалізуйте абстрактні методи
3. Додайте до `plugins/` директорії
4. Зареєструйте в менеджері

```python
class CustomPlugin(BasePlugin):
    def __init__(self):
        super().__init__("CustomPlugin", "1.0.0")
    
    async def execute(self, task, context=None):
        # Ваша логіка тут
        return PluginResult(success=True, message="Завдання виконано")
    
    def get_supported_tasks(self):
        return ['custom_task_type']
    
    def get_gui_configuration(self):
        return {'window_type': 'basic_panel'}
```

## 📞 Підтримка

Для отримання допомоги:
1. Перевірте логи в `logs/nimda_plugin_system.log`
2. Запустіть діагностичні тести
3. Перегляньте документацію API
4. Зверніться до команди розробки

---

**Версія документації**: 2.0.0  
**Останнє оновлення**: 15 липня 2025  
**Автор**: NIMDA Development Team
