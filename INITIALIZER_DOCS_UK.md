# Project Initializer Clean - Documentation

## Description
`project_initializer_clean.py` is an optimized version of the project initializer that automatically creates necessary files and structure for different project types.

## Functionality

### Supported project types:
- **Python** - automatically detected by `.py` files
- **JavaScript** - automatically detected by `.js`, `.jsx`, `.ts`, `.tsx` files
- **Web** - automatically detected by `.html`, `.css` files
- **Generic** - basic type for all other projects

### Created files and structures:

#### For all projects:
- `README.md` - project documentation
- `.gitignore` - Git rules
- `DEV_PLAN.md` - development plan
- `CHANGELOG.md` - changelog
- `setup.sh` - скрипт автоматичного налаштування
- `.github/workflows/ci.yml` - GitHub Actions

#### Додатково для Python:
```
src/
├── __init__.py
tests/
├── __init__.py
docs/
requirements.txt
main.py
```

#### Додатково для JavaScript:
```
src/
tests/
docs/
package.json
index.js
```

#### Додатково для Web:
```
css/
js/
images/
index.html
style.css
script.js
```

## Використання

### Командний рядок:
```bash
python project_initializer_clean.py /path/to/project
```

### Програмно:
```python
from pathlib import Path
from project_initializer_clean import ProjectInitializer

# Створення ініціалізатора
initializer = ProjectInitializer(Path("/path/to/project"))

# Ініціалізація проекту
success = initializer.initialize()

if success:
    print("Проект ініціалізовано")
else:
    print("Помилка ініціалізації")
```

## Приклади використання

### 1. Ініціалізація Python проекту:
```bash
mkdir my_python_app
cd my_python_app
echo 'print("Hello")' > app.py
python /path/to/project_initializer_clean.py .
```

### 2. Ініціалізація веб-проекту:
```bash
mkdir my_website
cd my_website
echo '<h1>Hello</h1>' > index.html
python /path/to/project_initializer_clean.py .
```

### 3. Ініціалізація JavaScript проекту:
```bash
mkdir my_js_app
cd my_js_app
echo 'console.log("Hello")' > app.js
python /path/to/project_initializer_clean.py .
```

## Автоматичне налаштування

Після ініціалізації ви можете запустити скрипт `setup.sh`:
```bash
./setup.sh
```

Цей скрипт:
- Створить віртуальне середовище (для Python)
- Встановить залежності
- Ініціалізує Git репозиторій

## Тестування

Для тестування функціональності:
```bash
python test_initializer.py
```

## Переваги над оригінальним project_initializer.py

1. **Компактність** - 500+ рядків замість 2154
2. **Простота** - зрозуміла структура та логіка
3. **Ефективність** - швидша робота
4. **Розширюваність** - легко додавати нові типи проектів
5. **Тестованість** - включені автоматичні тести

## Структура коду

```python
class ProjectInitializer:
    def __init__(self, project_path)           # Ініціалізація
    def initialize(self)                       # Головна функція
    def detect_project_type(self)              # Визначення типу
    def create_structure(self, project_type)   # Створення структури
    def create_basic_files(self, project_type) # Базові файли
    def create_gitignore(self, project_type)   # .gitignore
    def create_github_workflow(self, project_type) # CI/CD
    def create_dev_plan(self)                  # План розробки
    def create_changelog(self)                 # Журнал змін
    def create_setup_script(self)              # Скрипт налаштування
```

## Логування

Всі операції логуються з рівнем INFO:
```
2025-07-11 06:26:13,299 - ProjectInitializer - INFO - Початок ініціалізації проекту
2025-07-11 06:26:13,299 - ProjectInitializer - INFO - Тип проекту: python
2025-07-11 06:26:13,299 - ProjectInitializer - INFO - Створено файл: requirements.txt
...
```

## Підтримка

Для додавання нового типу проекту додайте його в `self.templates`:

```python
"new_type": {
    "files": ["specific_file.ext"],
    "dirs": ["specific_dir"],
    "gitignore": ["*.tmp"]
}
```

Та оновіть метод `detect_project_type()` для його визначення.
