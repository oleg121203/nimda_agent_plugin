# Universal Creative Development Workflow

## Концепція

Універсальна система розробки, яка повністю адаптується до будь-якого типу проекту без жорстко заданих обмежень.

## Ключові принципи

### 1. Повна адаптивність
- Вся поведінка керується файлом `DEV_PLAN.md`
- Жодних жорстко заданих технологій або версій
- Автоматичне виявлення типу проекту та технологій

### 2. Codex/AI-дружність
- Хуки для креативних рішень
- Точки розширення для AI-асистентів
- Інтерактивні паузи для Codex

### 3. Універсальна підтримка
- Підтримка будь-яких мов програмування
- Адаптація до різних типів проектів
- Гнучка структура завдань

## Архітектура

```
universal_creative_workflow.py     # Головний workflow
├── universal_task_manager.py      # Універсальний менеджер задач
├── focused_system_analyzer.py     # Аналізатор системи
├── dev_plan_manager.py           # Менеджер DEV_PLAN.md
└── run_universal_workflow.py     # Універсальний лаунчер
```

## Підтримувані типи проектів

1. **Web Applications** - React, Vue, Angular, Django, Flask, etc.
2. **Desktop Applications** - Qt, Tkinter, Electron, etc.
3. **CLI Applications** - Command-line tools
4. **AI Systems** - ML/AI agents and tools
5. **Libraries** - Reusable code packages
6. **Universal Projects** - Any other type

## Використання

### Основний запуск
```bash
python3 run_universal_workflow.py
```

### Програмний запуск
```python
from universal_creative_workflow import UniversalCreativeWorkflow

workflow = UniversalCreativeWorkflow("/path/to/project")
workflow.run_universal_workflow()
```

### Реєстрація креативних хуків
```python
def my_creative_hook(context):
    if context.get("action") == "create_component":
        # Користувацька логіка для створення компонентів
        return True
    return False

workflow.register_creative_hook("creative_solution", my_creative_hook)
```

## Типи хуків

1. **before_phase** - Перед кожною фазою
2. **after_phase** - Після кожної фази
3. **on_error** - При виникненні помилок
4. **creative_solution** - Для креативних рішень
5. **technology_detection** - Для виявлення технологій
6. **environment_setup** - Для налаштування середовища

## Конфігурація через DEV_PLAN.md

Система автоматично витягує інформацію з `DEV_PLAN.md`:

- **Мови програмування** - Python, JavaScript, TypeScript, etc.
- **Фреймворки** - React, Django, Flask, PySide6, etc.
- **Версії** - Python 3.11, Node 18, etc.
- **Тип проекту** - Веб-додаток, десктоп, CLI, AI-система

### Приклад DEV_PLAN.md
```markdown
# My Universal Project

## Overview
This is a Python 3.10 web application using Django and React.

## Technology Stack
- Backend: Python 3.10, Django 4.2
- Frontend: React 18, TypeScript
- Database: PostgreSQL
- Deployment: Docker

## Phases
### 1. Environment Setup
- [ ] Setup Python 3.10 environment
- [ ] Install Django dependencies
- [ ] Configure database

### 2. Backend Development
- [ ] Create Django project
- [ ] Implement API endpoints
- [ ] Setup authentication
```

## Генерація завдань

Система створює 3-рівневу структуру завдань:

1. **Фази** (Phase) - Основні етапи розробки
2. **Задачі 1-го рівня** (Level 1) - Головні компоненти фази
3. **Задачі 2-го рівня** (Level 2) - Підзадачі компонентів
4. **Задачі 3-го рівня** (Level 3) - Атомарні дії

### Приклад структури
```json
{
  "phases": [
    {
      "id": 1,
      "name": "Environment Setup",
      "level_1_tasks": [
        {
          "id": "1.1",
          "name": "Python Environment",
          "level_2_tasks": [
            {
              "id": "1.1.1",
              "name": "Install Python 3.10",
              "level_3_tasks": [
                {"id": "1.1.1.1", "name": "Check Python availability"},
                {"id": "1.1.1.2", "name": "Create virtual environment"},
                {"id": "1.1.1.3", "name": "Activate environment"}
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Фази виконання

1. **Phase 0: Dynamic Setup** - Налаштування середовища
2. **Phase 1: Structure Creation** - Створення структури проекту
3. **Phase 2: Universal Components** - Створення компонентів
4. **Phase 3: Creative Analysis** - Аналіз та генерація задач
5. **Phase 4: Adaptive Fixing** - Виправлення помилок
6. **Phase 5: Universal Testing** - Тестування
7. **Phase 6: Creative Validation** - Фінальна валідація

## Переваги над попередньою системою

### Було (жорстко задано):
- ✗ Обов'язковий Python 3.11
- ✗ Фіксовані технології (PySide6, PyObjC)
- ✗ macOS-специфічні налаштування
- ✗ Жорстка структура каталогів

### Стало (адаптивно):
- ✅ Будь-яка версія Python (або інші мови)
- ✅ Автоматичне виявлення технологій
- ✅ Кросплатформенність
- ✅ Динамічна структура на основі потреб

## Розширюваність

### Додавання підтримки нової мови
```python
def setup_new_language_environment(language, version):
    # Логіка налаштування нової мови
    pass

workflow.register_creative_hook("environment_setup", setup_new_language_environment)
```

### Додавання нового типу проекту
```python
def detect_custom_project_type(content):
    if "my_framework" in content.lower():
        return "custom_project_type"
    return None

workflow.register_creative_hook("technology_detection", detect_custom_project_type)
```

## Вихідні файли

- `UNIVERSAL_TASK_STRUCTURE.json` - Структура завдань
- `UNIVERSAL_ANALYSIS_REPORT.md` - Звіт аналізу
- `CREATIVE_TASK_STRUCTURE.json` - Задачі з креативними розширеннями

## Сумісність

Система зберігає сумісність з попередніми компонентами через аліаси:
- `AdvancedTaskManager` → `UniversalTaskManager`
- `enhanced_interactive_workflow.py` → `universal_creative_workflow.py`

## Приклади використання

### Веб-додаток на Django
```bash
# DEV_PLAN.md містить "Django", "Python 3.9"
python3 run_universal_workflow.py
# Автоматично створить Django-проект з Python 3.9
```

### React/TypeScript додаток
```bash
# DEV_PLAN.md містить "React", "TypeScript", "Node 18"
python3 run_universal_workflow.py
# Автоматично налаштує Node.js та створить React-проект
```

### AI/ML проект
```bash
# DEV_PLAN.md містить "machine learning", "TensorFlow"
python3 run_universal_workflow.py
# Створить структуру для ML-проекту
```

## Налагодження

### Увімкнути детальне логування
```python
workflow = UniversalCreativeWorkflow(project_path, pause_duration=0.1)
```

### Перевірити виявлені технології
```python
print(workflow.project_config)
```

### Подивитись структуру завдань
```python
workflow.task_manager.print_task_summary()
```
