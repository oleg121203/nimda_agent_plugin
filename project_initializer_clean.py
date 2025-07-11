"""
Оптимізований ініціалізатор проекту
Створює необхідні файли та структуру для різних типів проектів
"""

import json
import logging
from datetime import datetime
from pathlib import Path


class ProjectInitializer:
    """Оптимізований ініціалізатор проекту"""

    def __init__(self, project_path: Path):
        """
        Ініціалізація

        Args:
            project_path: Шлях до проекту
        """
        self.project_path = Path(project_path)
        self.logger = logging.getLogger("ProjectInitializer")

        # Базові шаблони для різних типів проектів
        self.templates = {
            "python": {
                "files": ["requirements.txt", "main.py", "README.md"],
                "dirs": ["src", "tests", "docs"],
                "gitignore": ["__pycache__/", "*.pyc", "venv/", ".env"],
            },
            "javascript": {
                "files": ["package.json", "index.js", "README.md"],
                "dirs": ["src", "tests", "docs"],
                "gitignore": ["node_modules/", "dist/", ".env"],
            },
            "web": {
                "files": ["index.html", "style.css", "script.js", "README.md"],
                "dirs": ["css", "js", "images"],
                "gitignore": ["dist/", "build/", ".env"],
            },
            "generic": {
                "files": ["README.md"],
                "dirs": ["docs"],
                "gitignore": [".env", "*.log"],
            },
        }

    def initialize(self) -> bool:
        """
        Основна ініціалізація проекту

        Returns:
            True якщо успішно
        """
        try:
            self.logger.info("Початок ініціалізації проекту")

            # Визначаємо тип проекту
            project_type = self.detect_project_type()
            self.logger.info(f"Тип проекту: {project_type}")

            # Створюємо структуру
            self.create_structure(project_type)
            self.create_basic_files(project_type)
            self.create_gitignore(project_type)
            self.create_github_workflow(project_type)
            self.create_dev_plan()
            self.create_changelog()
            self.create_setup_script()

            self.logger.info("Ініціалізація завершена")
            return True

        except Exception as e:
            self.logger.error(f"Помилка ініціалізації: {e}")
            return False

    def detect_project_type(self) -> str:
        """Визначає тип проекту за файлами"""
        try:
            files = list(self.project_path.glob("**/*"))
            extensions = {f.suffix.lower() for f in files if f.is_file()}

            if ".py" in extensions:
                return "python"
            elif any(ext in extensions for ext in [".js", ".jsx", ".ts", ".tsx"]):
                return "javascript"
            elif any(ext in extensions for ext in [".html", ".css"]):
                return "web"
            else:
                return "generic"

        except Exception:
            return "generic"

    def create_structure(self, project_type: str):
        """Створює базову структуру директорій"""
        template = self.templates[project_type]

        for directory in template["dirs"]:
            dir_path = self.project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)

            # Створюємо __init__.py для Python
            if project_type == "python" and directory in ["src", "tests"]:
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    init_file.write_text("# -*- coding: utf-8 -*-\n")

    def create_basic_files(self, project_type: str):
        """Створює базові файли проекту"""
        template = self.templates[project_type]

        for filename in template["files"]:
            file_path = self.project_path / filename
            if not file_path.exists():
                content = self.get_file_content(filename, project_type)
                file_path.write_text(content, encoding="utf-8")
                self.logger.info(f"Створено файл: {filename}")

    def get_file_content(self, filename: str, project_type: str) -> str:
        """Генерує контент для файлів"""
        project_name = self.project_path.name or "Project"

        if filename == "README.md":
            return self.get_readme_content(project_name, project_type)
        elif filename == "requirements.txt" and project_type == "python":
            return self.get_requirements_content()
        elif filename == "package.json" and project_type == "javascript":
            return self.get_package_json_content(project_name)
        elif filename == "main.py" and project_type == "python":
            return self.get_main_py_content()
        elif filename == "index.js" and project_type == "javascript":
            return self.get_index_js_content()
        elif filename == "index.html" and project_type == "web":
            return self.get_index_html_content(project_name)
        elif filename == "style.css" and project_type == "web":
            return self.get_style_css_content()
        elif filename == "script.js" and project_type == "web":
            return self.get_script_js_content()
        else:
            return f"# {filename}\n# Створено автоматично\n"

    def get_readme_content(self, project_name: str, project_type: str) -> str:
        """Генерує README.md"""
        return f"""# {project_name}

## Опис
Опис проекту {project_name}

## Встановлення
```bash
git clone <repository-url>
cd {project_name}
```

## Використання
{self.get_usage_instructions(project_type)}

## Розробка
- Дотримуйтесь правил кодування
- Додавайте тести для нової функціональності
- Оновлюйте документацію

## Ліцензія
MIT License

## Автор
Створено з NIMDA Agent
"""

    def get_usage_instructions(self, project_type: str) -> str:
        """Інструкції використання для різних типів проектів"""
        if project_type == "python":
            return """```bash
pip install -r requirements.txt
python main.py
```"""
        elif project_type == "javascript":
            return """```bash
npm install
npm start
```"""
        elif project_type == "web":
            return """Відкрийте index.html у браузері"""
        else:
            return "Дивіться документацію проекту"

    def get_requirements_content(self) -> str:
        """Базовий requirements.txt для Python"""
        return """# Основні залежності
requests>=2.25.0
python-dotenv>=0.19.0

# Розробка
pytest>=6.0.0
black>=21.0.0
flake8>=3.9.0
"""

    def get_package_json_content(self, project_name: str) -> str:
        """Базовий package.json"""
        return json.dumps(
            {
                "name": project_name.lower().replace(" ", "-"),
                "version": "1.0.0",
                "description": f"Проект {project_name}",
                "main": "index.js",
                "scripts": {
                    "start": "node index.js",
                    "test": 'echo "Error: no test specified" && exit 1',
                },
                "keywords": [],
                "author": "",
                "license": "MIT",
                "dependencies": {},
                "devDependencies": {"eslint": "^8.0.0", "prettier": "^2.0.0"},
            },
            indent=2,
            ensure_ascii=False,
        )

    def get_main_py_content(self) -> str:
        """Базовий main.py"""
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Головний модуль проекту
"""

import logging
import sys
from pathlib import Path


def setup_logging():
    """Налаштування логування"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Головна функція"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Запуск програми")
    
    # Ваш код тут
    print("Привіт, світ!")
    
    logger.info("Програма завершена")


if __name__ == "__main__":
    main()
'''

    def get_index_js_content(self) -> str:
        """Базовий index.js"""
        return """const path = require('path');

console.log('Привіт, світ!');

// Ваш код тут

module.exports = {
    // Експорти
};
"""

    def get_index_html_content(self, project_name: str) -> str:
        """Базовий index.html"""
        return f"""<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{project_name}</h1>
    </header>
    
    <main>
        <p>Ласкаво просимо до {project_name}!</p>
    </main>
    
    <footer>
        <p>&copy; 2025 {project_name}</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>
"""

    def get_style_css_content(self) -> str:
        """Базовий style.css"""
        return """/* Базові стилі */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
}

header {
    background: #333;
    color: white;
    text-align: center;
    padding: 1rem;
}

main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 2rem;
}

footer {
    text-align: center;
    padding: 1rem;
    margin-top: 2rem;
    color: #666;
}
"""

    def get_script_js_content(self) -> str:
        """Базовий script.js"""
        return """// Головний JavaScript файл

document.addEventListener('DOMContentLoaded', function() {
    console.log('Сторінка завантажена');
    
    // Ваш код тут
});

// Утилітарні функції
function showMessage(message) {
    console.log(message);
}
"""

    def create_gitignore(self, project_type: str):
        """Створює .gitignore файл"""
        gitignore_path = self.project_path / ".gitignore"
        if not gitignore_path.exists():
            template = self.templates[project_type]
            content = "\n".join(template["gitignore"]) + "\n"
            gitignore_path.write_text(content)
            self.logger.info("Створено .gitignore")

    def create_github_workflow(self, project_type: str):
        """Створює GitHub Actions workflow"""
        workflows_dir = self.project_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)

        workflow_file = workflows_dir / "ci.yml"
        if not workflow_file.exists():
            content = self.get_workflow_content(project_type)
            workflow_file.write_text(content)
            self.logger.info("Створено GitHub workflow")

    def get_workflow_content(self, project_type: str) -> str:
        """Генерує GitHub Actions workflow"""
        if project_type == "python":
            return """name: Python CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
"""
        elif project_type == "javascript":
            return """name: Node.js CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16.x, 18.x, 20.x]

    steps:
    - uses: actions/checkout@v3
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - run: npm ci
    - run: npm run build --if-present
    - run: npm test
"""
        else:
            return """name: CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup
      run: echo "Setting up project"
    
    - name: Build
      run: echo "Building project"
    
    - name: Test
      run: echo "Running tests"
"""

    def create_dev_plan(self):
        """Створює DEV_PLAN.md"""
        dev_plan_path = self.project_path / "DEV_PLAN.md"
        if not dev_plan_path.exists():
            content = f"""# План розробки - {self.project_path.name}

## 📋 Загальна інформація
- **Проект**: {self.project_path.name}
- **Дата створення**: {datetime.now().strftime("%Y-%m-%d")}
- **Статус**: В розробці

## 🎯 Цілі проекту
- [ ] Основна функціональність
- [ ] Тестування
- [ ] Документація
- [ ] Релізна версія

## 📝 Завдання

### Поточний спринт
- [ ] Налаштування проекту
- [ ] Базова структура

### Наступні кроки
- [ ] Розробка core функцій
- [ ] Додавання тестів
- [ ] Покращення UI/UX

## 🔧 Технічні деталі
- **Мова**: Визначається автоматично
- **Фреймворк**: TBD
- **База даних**: TBD

## 📚 Ресурси
- [Документація](./docs/)
- [Тести](./tests/)
- [Приклади](./examples/)

---
*Створено з NIMDA Agent*
"""
            dev_plan_path.write_text(content)
            self.logger.info("Створено DEV_PLAN.md")

    def create_changelog(self):
        """Створює CHANGELOG.md"""
        changelog_path = self.project_path / "CHANGELOG.md"
        if not changelog_path.exists():
            content = f"""# Changelog

Всі важливі зміни в цьому проекті будуть документовані в цьому файлі.

Формат базується на [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
і цей проект дотримується [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Початкова структура проекту
- Базові файли конфігурації

## [1.0.0] - {datetime.now().strftime("%Y-%m-%d")}

### Added
- Ініціальний реліз
- Основна функціональність

---
*Створено з NIMDA Agent*
"""
            changelog_path.write_text(content)
            self.logger.info("Створено CHANGELOG.md")

    def create_setup_script(self):
        """Створює скрипт налаштування проекту"""
        setup_script = self.project_path / "setup.sh"
        if not setup_script.exists():
            content = """#!/bin/bash
# Скрипт автоматичного налаштування проекту

echo "🚀 Налаштування проекту..."

# Перевірка Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3 знайдено"
    
    # Створення віртуального середовища
    if [ ! -d "venv" ]; then
        echo "📦 Створення віртуального середовища..."
        python3 -m venv venv
    fi
    
    # Активація і встановлення залежностей
    source venv/bin/activate
    if [ -f "requirements.txt" ]; then
        echo "📚 Встановлення залежностей..."
        pip install -r requirements.txt
    fi
fi

# Перевірка Node.js
if command -v npm &> /dev/null; then
    echo "✅ Node.js знайдено"
    
    if [ -f "package.json" ]; then
        echo "📚 Встановлення npm пакетів..."
        npm install
    fi
fi

# Ініціалізація Git
if [ ! -d ".git" ]; then
    echo "🔧 Ініціалізація Git..."
    git init
    git add .
    git commit -m "Initial commit"
fi

echo "✨ Налаштування завершено!"
"""
            setup_script.write_text(content)
            setup_script.chmod(0o755)
            self.logger.info("Створено setup.sh")


def main():
    """Головна функція для тестування"""
    import argparse

    parser = argparse.ArgumentParser(description="Ініціалізація проекту")
    parser.add_argument("path", help="Шлях до проекту")
    args = parser.parse_args()

    # Налаштування логування
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Ініціалізація проекту
    initializer = ProjectInitializer(Path(args.path))
    success = initializer.initialize()

    if success:
        print("✅ Проект успішно ініціалізовано")
    else:
        print("❌ Помилка ініціалізації проекту")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
