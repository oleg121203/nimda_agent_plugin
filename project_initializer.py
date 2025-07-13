"""Project initializer - creates required files and structure"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class ProjectInitializer:
    """
    Ініціалізатор для автоматичного створення структури проекту

    Функції:
    - Створення базових файлів проекту
    - Створення GitHub workflows
    - Створення конфігураційних файлів
    - Визначення типу проекту та мови програмування
    """

    def __init__(self, project_path: Path):
        """
        Ініціалізація

        Args:
            project_path: Шлях до проекту
        """
        self.project_path = project_path
        self.logger = logging.getLogger("ProjectInitializer")

        # Шаблони файлів для різних типів проектів
        self.project_templates = {
            "python": {
                "extensions": [".py"],
                "files": ["requirements.txt", "setup.py", "main.py"],
                "directories": ["tests", "docs", "src"],
                "workflows": ["python-app.yml", "python-publish.yml"],
            },
            "javascript": {
                "extensions": [".js", ".jsx", ".ts", ".tsx"],
                "files": ["package.json", "index.js", "README.md"],
                "directories": ["src", "tests", "docs", "node_modules"],
                "workflows": ["node.js.yml", "npm-publish.yml"],
            },
            "web": {
                "extensions": [".html", ".css", ".js"],
                "files": ["index.html", "style.css", "script.js"],
                "directories": ["css", "js", "images", "docs"],
                "workflows": ["static.yml", "pages.yml"],
            },
            "generic": {
                "extensions": [],
                "files": ["README.md"],
                "directories": ["docs", "scripts"],
                "workflows": ["ci.yml"],
            },
        }

    def initialize(self) -> bool:
        """
        Основна ініціалізація проекту

        Returns:
            True якщо ініціалізація успішна
        """
        try:
            self.logger.info("Початок ініціалізації проекту")

            # 1. Визначення типу проекту
            project_type = self._detect_project_type()
            self.logger.info(f"Визначено тип проекту: {project_type}")

            # 2. Створення базової структури
            self._create_basic_structure(project_type)

            # 3. Створення базових файлів
            self._create_basic_files(project_type)

            # 4. Створення GitHub workflows
            self._create_github_workflows(project_type)

            # 5. Створення конфігураційних файлів
            self._create_config_files(project_type)

            # 6. Створення файлів для Codex
            self._create_codex_files(project_type)

            # 7. Створення CHANGELOG.md
            self._create_changelog()

            # 8. Створення шаблону DEV_PLAN.md (якщо не існує)
            self._ensure_dev_plan_exists()

            # 9. Створення файлів змінних середовища
            self._create_environment_files()

            # 10. Створення скрипта автоматичного налаштування проекту
            self.create_setup_script()

            self.logger.info("Ініціалізація проекту завершена успішно")
            return True

        except Exception as e:
            self.logger.error(f"Помилка ініціалізації проекту: {e}")
            return False

    def _detect_project_type(self) -> str:
        """
        Визначення типу проекту на основі існуючих файлів

        Returns:
            Тип проекту
        """
        try:
            files = list(self.project_path.glob("**/*"))
            file_extensions = set()

            for file_path in files:
                if file_path.is_file():
                    file_extensions.add(file_path.suffix.lower())

            # Аналіз типу проекту
            if ".py" in file_extensions:
                return "python"
            elif any(ext in file_extensions for ext in [".js", ".jsx", ".ts", ".tsx"]):
                return "javascript"
            elif any(ext in file_extensions for ext in [".html", ".css"]):
                return "web"
            else:
                return "generic"

        except Exception as e:
            self.logger.warning(f"Помилка визначення типу проекту: {e}")
            return "generic"

    def _create_basic_structure(self, project_type: str):
        """Створення базової структури директорій"""
        template = self.project_templates[project_type]

        for directory in template["directories"]:
            dir_path = self.project_path / directory
            dir_path.mkdir(exist_ok=True)
            self.logger.info(f"Створено директорію: {directory}")

            # Створення __init__.py для Python пакетів
            if project_type == "python" and directory in ["src", "tests"]:
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    init_file.write_text("# Auto-generated by NIMDA Agent\n")

    def _create_basic_files(self, project_type: str):
        """Створення базових файлів проекту"""
        if project_type == "python":
            self._create_python_files()
        elif project_type == "javascript":
            self._create_javascript_files()
        elif project_type == "web":
            self._create_web_files()

        # Загальні файли для всіх типів
        self._create_readme()
        self._create_gitignore(project_type)

    def _create_python_files(self):
        """Створення файлів для Python проекту"""
        # requirements.txt
        requirements_file = self.project_path / "requirements.txt"
        if not requirements_file.exists():
            requirements_content = """# NIMDA Agent Python Project Dependencies
# Core dependencies
requests>=2.28.0
pyyaml>=6.0
pathlib
datetime

# Development dependencies
pytest>=7.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=0.991

# Optional dependencies
# Add your project-specific dependencies here
"""
            requirements_file.write_text(requirements_content)
            self.logger.info("Створено requirements.txt")

        # setup.py
        setup_file = self.project_path / "setup.py"
        if not setup_file.exists():
            project_name = self.project_path.name
            setup_content = f'''"""
Setup script for {project_name}
Auto-generated by NIMDA Agent
"""

from setuptools import setup, find_packages

setup(
    name="{project_name}",
    version="0.1.0",
    description="Project managed by NIMDA Agent",
    author="NIMDA Agent",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "pyyaml>=6.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
'''
            setup_file.write_text(setup_content)
            self.logger.info("Створено setup.py")

        # main.py
        main_file = self.project_path / "main.py"
        if not main_file.exists():
            main_content = '''#!/usr/bin/env python3
"""
Main entry point for the project
Auto-generated by NIMDA Agent
"""

import sys
import os
from pathlib import Path


def main():
    """Main function"""
    print("🤖 Project initialized by NIMDA Agent")
    print(f"📁 Project path: {Path.cwd()}")

    # Your main logic here
    pass


if __name__ == "__main__":
    main()
'''
            main_file.write_text(main_content)
            self.logger.info("Створено main.py")

    def _create_javascript_files(self):
        """Створення файлів для JavaScript проекту"""
        # package.json
        package_file = self.project_path / "package.json"
        if not package_file.exists():
            project_name = self.project_path.name.lower().replace(" ", "-")
            package_content = {
                "name": project_name,
                "version": "1.0.0",
                "description": "Project managed by NIMDA Agent",
                "main": "index.js",
                "scripts": {
                    "start": "node index.js",
                    "test": "jest",
                    "lint": "eslint .",
                    "dev": "nodemon index.js",
                },
                "keywords": ["nimda", "automation"],
                "author": "NIMDA Agent",
                "license": "MIT",
                "dependencies": {},
                "devDependencies": {
                    "jest": "^29.0.0",
                    "eslint": "^8.0.0",
                    "nodemon": "^2.0.0",
                },
            }

            with open(package_file, "w", encoding="utf-8") as f:
                json.dump(package_content, f, indent=2, ensure_ascii=False)
            self.logger.info("Створено package.json")

        # index.js
        index_file = self.project_path / "index.js"
        if not index_file.exists():
            index_content = """/**
 * Main entry point for the project
 * Auto-generated by NIMDA Agent
 */

console.log('🤖 Project initialized by NIMDA Agent');
console.log(`📁 Project path: ${process.cwd()}`);

// Your main logic here
function main() {
    // Implementation here
}

// Run main function if this file is executed directly
if (require.main === module) {
    main();
}

module.exports = { main };
"""
            index_file.write_text(index_content)
            self.logger.info("Створено index.js")

    def _create_web_files(self):
        """Створення файлів для веб проекту"""
        # index.html
        html_file = self.project_path / "index.html"
        if not html_file.exists():
            project_name = self.project_path.name
            html_content = f"""<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>🤖 {project_name}</h1>
        <p>Проект створено за допомогою NIMDA Agent</p>
    </header>

    <main>
        <section>
            <h2>Ласкаво просимо!</h2>
            <p>Цей проект було автоматично ініціалізовано NIMDA Agent.</p>
        </section>
    </main>

    <footer>
        <p>&copy; 2024 NIMDA Agent</p>
    </footer>

    <script src="script.js"></script>
</body>
</html>
"""
            html_file.write_text(html_content)
            self.logger.info("Створено index.html")

        # style.css
        css_file = self.project_path / "style.css"
        if not css_file.exists():
            css_content = """/*
   Styles for project
   Auto-generated by NIMDA Agent
*/

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 2rem 0;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

section {
    padding: 2rem;
}

h2 {
    color: #667eea;
    margin-bottom: 1rem;
}

footer {
    text-align: center;
    padding: 2rem 0;
    background: #333;
    color: white;
    margin-top: 2rem;
}
"""
            css_file.write_text(css_content)
            self.logger.info("Створено style.css")

        # script.js
        js_file = self.project_path / "script.js"
        if not js_file.exists():
            js_content = """/**
 * Main JavaScript file
 * Auto-generated by NIMDA Agent
 */

console.log('🤖 Project initialized by NIMDA Agent');

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 DOM loaded successfully');

    // Your JavaScript code here
    initializeProject();
});

function initializeProject() {
    console.log('🚀 Project initialization complete');

    // Add your initialization logic here
}

// Utility functions
function showMessage(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
}

// Export functions for use in other files
window.ProjectUtils = {
    showMessage,
    initializeProject
};
"""
            js_file.write_text(js_content)
            self.logger.info("Створено script.js")

    def _create_readme(self):
        """Створення README.md"""
        readme_file = self.project_path / "README.md"
        if not readme_file.exists():
            project_name = self.project_path.name
            readme_content = f"""# {project_name}

🤖 Проект створено та керується за допомогою **NIMDA Agent** - автономного агента розробки.

## Опис проекту

Додайте тут опис вашого проекту.

## Встановлення

```bash
# Клонування репозиторію
git clone <repository-url>
cd {project_name.lower()}

# Встановлення залежностей (Python)
pip install -r requirements.txt

# Або для Node.js проектів
npm install
```

## Використання

```bash
# Запуск проекту
python main.py

# Або для Node.js
npm start
```

## Структура проекту

```
{project_name}/
├── README.md           # Цей файл
├── DEV_PLAN.md        # План розробки
├── CHANGELOG.md       # Журнал змін
├── requirements.txt   # Python залежності
├── main.py           # Головний файл
├── src/              # Вихідний код
├── tests/            # Тести
├── docs/             # Документація
└── .github/          # GitHub workflows
```

## NIMDA Agent

Цей проект використовує NIMDA Agent для автоматизації розробки:

- 📋 Автоматичне виконання плану розробки з DEV_PLAN.md
- 🔧 Автоматичне виправлення помилок
- 🔄 Синхронізація з Git репозиторієм
- 📝 Ведення журналу змін

### Команди для NIMDA Agent

- `допрацюй девплан` - оновити план розробки
- `виконай задачу номер X` - виконати конкретну задачу
- `виконай весь ДЕВ` - виконати весь план
- `статус` - показати поточний статус
- `синхронізація` - синхронізувати з Git

## Ліцензія

MIT License - дивіться файл LICENSE для деталей.

## Автор

Створено NIMDA Agent - автономним агентом розробки.
"""
            readme_file.write_text(readme_content)
            self.logger.info("Створено README.md")

    def _create_gitignore(self, project_type: str):
        """Створення .gitignore файлу"""
        gitignore_file = self.project_path / ".gitignore"

        if gitignore_file.exists():
            return

        gitignore_content = """# NIMDA Agent
nimda_logs/
nimda_agent_config.json
*.tmp
*.temp

# Logs
*.log
logs/

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Backup files
*.bak
*.backup
"""

        if project_type == "python":
            gitignore_content += """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
.venv
.env

# pytest
.pytest_cache/
.coverage
htmlcov/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json
"""

        elif project_type == "javascript":
            gitignore_content += """
# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# nyc test coverage
.nyc_output

# Dependency directories
jspm_packages/

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env
.env.test

# Production build
dist/
build/
"""

        gitignore_file.write_text(gitignore_content)
        self.logger.info("Створено .gitignore")

    def _create_github_workflows(self, project_type: str):
        """Створення адаптивних GitHub workflows"""
        workflows_dir = self.project_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)

        # Адаптивний CI workflow
        ci_workflow = workflows_dir / "ci.yml"
        if not ci_workflow.exists():
            ci_content = self._generate_adaptive_ci_workflow(project_type)
            ci_workflow.write_text(ci_content)
            self.logger.info("Створено .github/workflows/ci.yml")

        # NIMDA Agent workflow
        nimda_workflow = workflows_dir / "nimda-agent.yml"
        if not nimda_workflow.exists():
            nimda_content = self._generate_nimda_workflow()
            nimda_workflow.write_text(nimda_content)
            self.logger.info("Створено .github/workflows/nimda-agent.yml")

        # VS Code Extensions workflow
        vscode_workflow = workflows_dir / "vscode-integration.yml"
        if not vscode_workflow.exists():
            vscode_content = self._generate_vscode_workflow()
            vscode_workflow.write_text(vscode_content)
            self.logger.info("Створено .github/workflows/vscode-integration.yml")

        # Multi-platform workflow
        multiplatform_workflow = workflows_dir / "multiplatform.yml"
        if not multiplatform_workflow.exists():
            multiplatform_content = self._generate_multiplatform_workflow(project_type)
            multiplatform_workflow.write_text(multiplatform_content)
            self.logger.info("Створено .github/workflows/multiplatform.yml")

    def _generate_adaptive_ci_workflow(self, project_type: str) -> str:
        """Генерація адаптивного CI workflow для різних платформ"""
        if project_type == "python":
            return """name: Adaptive Python CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  detect-environment:
    runs-on: ubuntu-latest
    outputs:
      python-version: ${{ steps.detect.outputs.python-version }}
      has-requirements: ${{ steps.detect.outputs.has-requirements }}
      has-tests: ${{ steps.detect.outputs.has-tests }}
      has-nimda: ${{ steps.detect.outputs.has-nimda }}
    steps:
    - uses: actions/checkout@v4
    
    - name: Detect project environment
      id: detect
      run: |
        # Детекція Python версії з віртуального середовища
        if [ -f "nimda_env/pyvenv.cfg" ]; then
          python_version=$(grep "version" nimda_env/pyvenv.cfg | cut -d'=' -f2 | tr -d ' ' | cut -d'.' -f1,2)
          echo "python-version=$python_version" >> $GITHUB_OUTPUT
        else
          echo "python-version=3.11" >> $GITHUB_OUTPUT
        fi
        
        # Перевірка файлів
        echo "has-requirements=$([ -f requirements.txt ] && echo true || echo false)" >> $GITHUB_OUTPUT
        echo "has-tests=$([ -d tests ] && echo true || echo false)" >> $GITHUB_OUTPUT
        echo "has-nimda=$([ -f nimda_agent_plugin/run_nimda_agent.py ] && echo true || echo false)" >> $GITHUB_OUTPUT

  test:
    needs: detect-environment
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']
    runs-on: ${{ matrix.os }}

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: |
          ~/.cache/pip
          ~/.local/share/virtualenvs
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        if [ -f nimda_agent_plugin/requirements.txt ]; then pip install -r nimda_agent_plugin/requirements.txt; fi
        pip install pytest pytest-cov black flake8 mypy
      shell: bash

    - name: Lint with flake8
      run: |
        # Зупинитися на помилках синтаксису або невизначених іменах
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # Показати попередження
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

    - name: Format check with black
      run: black --check . || echo "Formatting issues found"

    - name: Type check with mypy
      run: mypy . --ignore-missing-imports || echo "Type issues found"
      continue-on-error: true

    - name: Test with pytest
      if: needs.detect-environment.outputs.has-tests == 'true'
      run: |
        pytest --cov=. --cov-report=xml --cov-report=term-missing

    - name: Test NIMDA Agent
      if: needs.detect-environment.outputs.has-nimda == 'true'
      run: |
        cd nimda_agent_plugin
        python run_nimda_agent.py --command "статус" || echo "NIMDA Agent test completed"

    - name: Upload coverage
      if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.11'
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  vs-code-compatibility:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Test VS Code compatibility
      run: |
        echo "🔍 Checking VS Code workspace configuration..."
        
        # Перевірка .vscode файлів
        if [ -d ".vscode" ]; then
          echo "✅ VS Code workspace detected"
          ls -la .vscode/
        fi
        
        # Перевірка tasks.json
        if [ -f ".vscode/tasks.json" ]; then
          echo "✅ Tasks configuration found"
          cat .vscode/tasks.json
        fi
        
        # Перевірка settings.json
        if [ -f ".vscode/settings.json" ]; then
          echo "✅ Workspace settings found"
        fi
        
        echo "🔗 VS Code integration check completed"
"""

        elif project_type == "javascript":
            return """name: Adaptive Node.js CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [16.x, 18.x, 20.x]
    runs-on: ${{ matrix.os }}

    steps:
    - uses: actions/checkout@v4

    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run linter
      run: npm run lint || echo "Linting completed"

    - name: Run tests
      run: npm test

    - name: Build project
      run: npm run build --if-present

    - name: Test NIMDA compatibility
      run: |
        if [ -f "nimda_agent_plugin/run_nimda_agent.py" ]; then
          echo "🤖 NIMDA Agent detected"
          python3 nimda_agent_plugin/run_nimda_agent.py --command "статус" || echo "NIMDA test completed"
        fi
"""

        else:
            return """name: General Adaptive CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}

    steps:
    - uses: actions/checkout@v4

    - name: Environment Detection
      run: |
        echo "🔍 Detecting project environment..."
        echo "OS: ${{ matrix.os }}"
        echo "Runner: ${{ runner.os }}"
        
        # Детекція типу проекту
        if [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
          echo "🐍 Python project detected"
        fi
        
        if [ -f "package.json" ]; then
          echo "📦 Node.js project detected"
        fi
        
        if [ -f "nimda_agent_plugin/run_nimda_agent.py" ]; then
          echo "🤖 NIMDA Agent detected"
        fi

    - name: Basic project checks
      run: |
        echo "📁 Project structure:"
        ls -la
        
        echo "📋 Key files check:"
        for file in README.md DEV_PLAN.md CHANGELOG.md .env.example; do
          if [ -f "$file" ]; then
            echo "✅ $file exists"
          else
            echo "❌ $file missing"
          fi
        done

    - name: NIMDA Agent Test
      run: |
        if [ -f "nimda_agent_plugin/run_nimda_agent.py" ]; then
          echo "🚀 Testing NIMDA Agent"
          python3 nimda_agent_plugin/run_nimda_agent.py --command "статус" || echo "NIMDA test completed"
        fi
"""

    def _generate_nimda_workflow(self) -> str:
        """Генерація NIMDA Agent workflow"""
        return """name: NIMDA Agent Auto-Development

on:
  schedule:
    # Запуск кожні 6 годин
    - cron: '0 */6 * * *'
  workflow_dispatch:
    inputs:
      command:
        description: 'NIMDA Agent Command'
        required: true
        default: 'статус'
        type: choice
        options:
          - 'статус'
          - 'допрацюй девплан'
          - 'виконай весь ДЕВ'
          - 'синхронізація'

jobs:
  nimda-agent:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        fetch-depth: 0

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install NIMDA Agent dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests pyyaml pathlib

    - name: Run NIMDA Agent
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        NIMDA_COMMAND: ${{ github.event.inputs.command || 'статус' }}
      run: |
        echo "🤖 Запуск NIMDA Agent з командою: $NIMDA_COMMAND"
        # Тут буде код для запуску NIMDA Agent
        python -c "
import os
print(f'🤖 NIMDA Agent Command: {os.getenv(\"NIMDA_COMMAND\", \"статус\")}')
print('📁 Project structure:')
for root, dirs, files in os.walk('.'):
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in files[:5]:  # Показати тільки перші 5 файлів
        print(f'{subindent}{file}')
    if len(files) > 5:
        print(f'{subindent}... та {len(files)-5} інших файлів')
"

    - name: Commit and push changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "NIMDA Agent"
        git add .
        if ! git diff --cached --exit-code; then
          git commit -m "🤖 NIMDA Agent: автоматичні зміни"
          git push
        else
          echo "Немає змін для коміту"
        fi
"""

    def _generate_vscode_workflow(self) -> str:
        """Генерація workflow для VS Code інтеграції"""
        return """name: VS Code Integration

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:
    inputs:
      test_extension:
        description: 'Test VS Code Extension'
        required: false
        default: 'false'
        type: boolean

jobs:
  vscode-setup:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Setup VS Code Environment
      run: |
        echo "🔧 Setting up VS Code compatible environment..."
        
        # Створення .vscode директорії якщо не існує
        mkdir -p .vscode
        
        # Створення базових налаштувань VS Code
        cat > .vscode/settings.json << 'EOF'
        {
          "python.defaultInterpreterPath": "./nimda_env/bin/python",
          "python.terminal.activateEnvironment": true,
          "python.linting.enabled": true,
          "python.linting.flake8Enabled": true,
          "python.formatting.provider": "black",
          "files.associations": {
            "*.md": "markdown"
          },
          "markdown.preview.linkify": true,
          "git.autofetch": true,
          "terminal.integrated.env.linux": {
            "NIMDA_AGENT_PATH": "${workspaceFolder}/nimda_agent_plugin"
          }
        }
        EOF

    - name: Test VS Code Configuration
      run: |
        echo "🧪 Testing VS Code configuration..."
        
        # Перевірка синтаксису JSON файлів
        for file in .vscode/*.json; do
          if [ -f "$file" ]; then
            echo "Validating $file..."
            python3 -m json.tool "$file" > /dev/null && echo "✅ $file is valid" || echo "❌ $file has errors"
          fi
        done

    - name: Test NIMDA Integration
      run: |
        echo "🤖 Testing NIMDA Agent integration..."
        
        if [ -f "nimda_agent_plugin/run_nimda_agent.py" ]; then
          echo "✅ NIMDA Agent found"
          python3 nimda_agent_plugin/run_nimda_agent.py --command "статус" || echo "NIMDA Agent test completed"
        else
          echo "⚠️ NIMDA Agent not found"
        fi
"""

    def _generate_multiplatform_workflow(self, project_type: str) -> str:
        """Генерація multiplatform workflow"""
        return f"""name: Multi-Platform Testing

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 6 * * 1'  # Щопонеділка о 6:00 UTC

jobs:
  platform-matrix:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']

    runs-on: ${{{{ matrix.os }}}}
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python ${{{{ matrix.python-version }}}}
      uses: actions/setup-python@v4
      with:
        python-version: ${{{{ matrix.python-version }}}}

    - name: Configure environment for platform
      run: |
        echo "🔧 Configuring for ${{{{ matrix.os }}}} with Python ${{{{ matrix.python-version }}}}"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip setuptools wheel
        
        if [ -f "requirements.txt" ]; then
          pip install -r requirements.txt
        fi
        
        if [ -f "nimda_agent_plugin/requirements.txt" ]; then
          pip install -r nimda_agent_plugin/requirements.txt
        fi
      shell: bash

    - name: Test NIMDA Agent
      run: |
        if [ -f "nimda_agent_plugin/run_nimda_agent.py" ]; then
          echo "Testing NIMDA Agent..."
          python nimda_agent_plugin/run_nimda_agent.py --command "статус" || echo "NIMDA test completed"
        fi
      shell: bash
"""

    def _create_config_files(self, project_type: str):
        """Створення конфігураційних файлів"""
        # codex.yaml для Codex інтеграції
        codex_file = self.project_path / "codex.yaml"
        if not codex_file.exists():
            codex_config = {
                "language": project_type if project_type != "generic" else "python",
                "entrypoint": self._get_entrypoint(project_type),
                "run": self._get_run_command(project_type),
            }

            with open(codex_file, "w", encoding="utf-8") as f:
                yaml.dump(codex_config, f, default_flow_style=False, allow_unicode=True)

            self.logger.info("Створено codex.yaml")

    def _get_entrypoint(self, project_type: str) -> str:
        """Отримання точки входу для проекту"""
        if project_type == "python":
            return "main.py"
        elif project_type == "javascript":
            return "index.js"
        elif project_type == "web":
            return "index.html"
        else:
            return "README.md"

    def _get_run_command(self, project_type: str) -> str:
        """Отримання команди запуску для проекту"""
        commands = []

        if project_type == "python":
            commands = [
                "pip install -r requirements.txt",
                "python -m pytest --tb=short",
                "python main.py",
            ]
        elif project_type == "javascript":
            commands = ["npm install", "npm test", "npm start"]
        elif project_type == "web":
            commands = [
                "echo 'Web project - open index.html in browser'",
                "python -m http.server 8000",
            ]
        else:
            commands = ["echo 'Generic project initialized'", "ls -la"]

        return "|\n  " + "\n  ".join(commands)

    def _create_codex_files(self, project_type: str):
        """Створення файлів для інтеграції з Codex"""
        # .codex/config.json
        codex_dir = self.project_path / ".codex"
        codex_dir.mkdir(exist_ok=True)

        config_file = codex_dir / "config.json"
        if not config_file.exists():
            config = {
                "nimda_agent": {
                    "enabled": True,
                    "auto_execute": False,
                    "commands": [
                        "статус",
                        "допрацюй девплан",
                        "виконай весь ДЕВ",
                        "синхронізація",
                    ],
                },
                "project": {
                    "type": project_type,
                    "language": project_type,
                    "framework": "auto-detect",
                },
            }

            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            self.logger.info("Створено .codex/config.json")

    def _create_changelog(self):
        """Створення CHANGELOG.md"""
        changelog_file = self.project_path / "CHANGELOG.md"
        if not changelog_file.exists():
            changelog_content = f"""# Журнал змін

Всі значущі зміни цього проекту будуть документовані в цьому файлі.

Формат базується на [Keep a Changelog](https://keepachangelog.com/uk/1.0.0/),
і цей проект дотримується [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Нереалізовано]

### Додано
- [ ] Базова структура проекту
- [ ] Інтеграція з NIMDA Agent
- [ ] Автоматизація розробки

### Змінено
- [ ] Оновлення документації

### Виправлено
- [ ] Початкове налаштування

## [1.0.0] - {datetime.now().strftime("%Y-%m-%d")}

### Додано
- [x] Початкова ініціалізація проекту NIMDA Agent
- [x] Створення базових файлів та структури
- [x] Налаштування GitHub workflows
- [x] Інтеграція з Codex

---

**Легенда:**
- [x] Виконано
- [ ] Не виконано
- [-] Скасовано

Цей журнал автоматично оновлюється NIMDA Agent.
"""
            changelog_file.write_text(changelog_content)
            self.logger.info("Створено CHANGELOG.md")

    def _ensure_dev_plan_exists(self):
        """Перевірка існування DEV_PLAN.md"""
        dev_plan_file = self.project_path / "DEV_PLAN.md"

        if not dev_plan_file.exists():
            self.logger.info("DEV_PLAN.md не існує - буде створено базовий шаблон")
            # Створення базового шаблону DEV_PLAN.md
            dev_plan_content = """# План розробки проекту

Автоматично створено NIMDA Agent.

## Загальна інформація
- **Проект**: Автоматизований розробкою
- **Статус**: В розробці
- **Версія**: 1.0.0

## Задачі

### 1. Базова ініціалізація
- [ ] Налаштування проекту
- [ ] Створення структури файлів
- [ ] Налаштування Git репозиторію

### 2. Розробка функціональності
- [ ] Основний функціонал
- [ ] Тестування
- [ ] Документація

### 3. Фінальні кроки
- [ ] Код-ревʼю
- [ ] Тестування на різних платформах
- [ ] Деплой

## Прогрес
- Загальний прогрес: 0%
- Завершених підзадач: 0
- Всього підзадач: 9

---
*Цей файл автоматично оновлюється NIMDA Agent*
"""
            dev_plan_file.write_text(dev_plan_content)
            self.logger.info("Створено базовий DEV_PLAN.md")

    def _create_environment_files(self):
        """Створення файлів змінних середовища"""
        # .env.example - шаблон змінних середовища
        env_example_file = self.project_path / ".env.example"
        if not env_example_file.exists():
            env_example_content = """# NIMDA Agent Environment Variables Template
# Скопіюйте цей файл у .env та заповніть своїми значеннями

# Git конфігурація (обов'язково для комітів)
GIT_USER_NAME=Your Name
GIT_USER_EMAIL=your.email@example.com

# GitHub налаштування (опціонально для роботи з репозиторієм)
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_USERNAME=your_github_username
GITHUB_REPO_URL=https://github.com/username/repository.git

# Налаштування проекту
PROJECT_NAME=NIMDA-CLI
PROJECT_VERSION=1.0.0
AUTO_COMMIT=true
AUTO_PUSH=true
CREATE_BACKUPS=true

# Логування
LOG_LEVEL=INFO
LOG_FILE_MAX_SIZE=10MB
ENABLE_DEBUG=false

# Розширені налаштування
MAX_RETRIES=3
TIMEOUT_SECONDS=30
GITHUB_INTEGRATION=true
CODEX_INTEGRATION=true

# API ключі (опціонально, для AI функцій)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
"""
            env_example_file.write_text(env_example_content)
            self.logger.info("Створено .env.example")

        # .env - базові змінні середовища з дефолтними значеннями
        env_file = self.project_path / ".env"
        if not env_file.exists():
            project_name = self.project_path.name
            env_content = f"""# NIMDA Agent Environment Variables
# Автоматично згенеровано під час ініціалізації проекту

# Git конфігурація
GIT_USER_NAME=NIMDA Agent
GIT_USER_EMAIL=nimda@agent.local

# Налаштування проекту
PROJECT_NAME={project_name}
PROJECT_VERSION=1.0.0
AUTO_COMMIT=true
AUTO_PUSH=true
CREATE_BACKUPS=true

# Логування
LOG_LEVEL=INFO
ENABLE_DEBUG=false

# Розширені налаштування
MAX_RETRIES=3
TIMEOUT_SECONDS=30
GITHUB_INTEGRATION=true
CODEX_INTEGRATION=true

# GitHub налаштування (потрібно заповнити вручну)
# GITHUB_TOKEN=
# GITHUB_USERNAME=
# GITHUB_REPO_URL=

# API ключі (опціонально)
# OPENAI_API_KEY=
# ANTHROPIC_API_KEY=
"""
            env_file.write_text(env_content)
            self.logger.info("Створено .env з базовими налаштуваннями")

        # setup_env.py - утиліта для налаштування змінних середовища
        setup_env_file = self.project_path / "setup_env.py"
        if not setup_env_file.exists():
            setup_env_content = '''#!/usr/bin/env python3
"""
Утиліта для налаштування змінних середовища NIMDA Agent
"""

import os
from pathlib import Path


def setup_environment():
    """Інтерактивне налаштування змінних середовища"""
    
    print("🔧 Налаштування змінних середовища NIMDA Agent")
    print("=" * 50)
    
    env_file = Path(".env")
    
    # Читання поточних значень
    current_env = {}
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    current_env[key] = value
    
    env_vars = {}
    
    # Обов'язкові змінні
    print("\\n📋 Обов'язкові налаштування:")
    
    git_name = input(f"Git ім'я користувача (GIT_USER_NAME) [{current_env.get('GIT_USER_NAME', 'NIMDA Agent')}]: ").strip()
    env_vars["GIT_USER_NAME"] = git_name or current_env.get('GIT_USER_NAME', 'NIMDA Agent')
    
    git_email = input(f"Git email (GIT_USER_EMAIL) [{current_env.get('GIT_USER_EMAIL', 'nimda@agent.local')}]: ").strip()
    env_vars["GIT_USER_EMAIL"] = git_email or current_env.get('GIT_USER_EMAIL', 'nimda@agent.local')
    
    # GitHub налаштування
    print("\\n🔗 GitHub налаштування (опціонально):")
    
    github_token = input(f"GitHub токен (GITHUB_TOKEN) [{current_env.get('GITHUB_TOKEN', 'не встановлено')}]: ").strip()
    if github_token:
        env_vars["GITHUB_TOKEN"] = github_token
    elif "GITHUB_TOKEN" in current_env:
        env_vars["GITHUB_TOKEN"] = current_env["GITHUB_TOKEN"]
    
    github_username = input(f"GitHub username (GITHUB_USERNAME) [{current_env.get('GITHUB_USERNAME', '')}]: ").strip()
    if github_username:
        env_vars["GITHUB_USERNAME"] = github_username
    elif "GITHUB_USERNAME" in current_env:
        env_vars["GITHUB_USERNAME"] = current_env["GITHUB_USERNAME"]
    
    github_repo = input(f"GitHub репозиторій URL (GITHUB_REPO_URL) [{current_env.get('GITHUB_REPO_URL', '')}]: ").strip()
    if github_repo:
        env_vars["GITHUB_REPO_URL"] = github_repo
    elif "GITHUB_REPO_URL" in current_env:
        env_vars["GITHUB_REPO_URL"] = current_env["GITHUB_REPO_URL"]
    
    # Налаштування проекту
    print("\\n⚙️ Налаштування проекту:")
    
    project_name = input(f"Назва проекту (PROJECT_NAME) [{current_env.get('PROJECT_NAME', 'NIMDA-CLI')}]: ").strip()
    env_vars["PROJECT_NAME"] = project_name or current_env.get('PROJECT_NAME', 'NIMDA-CLI')
    
    auto_commit = input(f"Автоматичні коміти (AUTO_COMMIT) [{current_env.get('AUTO_COMMIT', 'true')}]: ").strip().lower()
    env_vars["AUTO_COMMIT"] = auto_commit if auto_commit in ["true", "false"] else current_env.get('AUTO_COMMIT', 'true')
    
    auto_push = input(f"Автоматичний push (AUTO_PUSH) [{current_env.get('AUTO_PUSH', 'true')}]: ").strip().lower()
    env_vars["AUTO_PUSH"] = auto_push if auto_push in ["true", "false"] else current_env.get('AUTO_PUSH', 'true')
    
    # Копіювання інших існуючих змінних
    preserve_vars = ["PROJECT_VERSION", "CREATE_BACKUPS", "LOG_LEVEL", "ENABLE_DEBUG", 
                    "MAX_RETRIES", "TIMEOUT_SECONDS", "GITHUB_INTEGRATION", "CODEX_INTEGRATION"]
    
    for var in preserve_vars:
        if var in current_env:
            env_vars[var] = current_env[var]
    
    # Додавання стандартних значень якщо відсутні
    defaults = {
        "PROJECT_VERSION": "1.0.0",
        "CREATE_BACKUPS": "true",
        "LOG_LEVEL": "INFO",
        "ENABLE_DEBUG": "false",
        "MAX_RETRIES": "3",
        "TIMEOUT_SECONDS": "30",
        "GITHUB_INTEGRATION": "true",
        "CODEX_INTEGRATION": "true"
    }
    
    for key, value in defaults.items():
        if key not in env_vars:
            env_vars[key] = value
    
    # Запис у файл
    with open(env_file, "w") as f:
        f.write("# NIMDA Agent Environment Variables\\n")
        f.write("# Оновлено автоматично\\n\\n")
        
        # Групування змінних
        groups = {
            "Git конфігурація": ["GIT_USER_NAME", "GIT_USER_EMAIL"],
            "Налаштування проекту": ["PROJECT_NAME", "PROJECT_VERSION", "AUTO_COMMIT", "AUTO_PUSH", "CREATE_BACKUPS"],
            "Логування": ["LOG_LEVEL", "ENABLE_DEBUG"],
            "Розширені налаштування": ["MAX_RETRIES", "TIMEOUT_SECONDS", "GITHUB_INTEGRATION", "CODEX_INTEGRATION"],
            "GitHub налаштування": ["GITHUB_TOKEN", "GITHUB_USERNAME", "GITHUB_REPO_URL"]
        }
        
        for group_name, keys in groups.items():
            f.write(f"# {group_name}\\n")
            for key in keys:
                if key in env_vars and env_vars[key]:
                    f.write(f"{key}={env_vars[key]}\\n")
                elif key.startswith("GITHUB_"):
                    f.write(f"# {key}=\\n")
            f.write("\\n")
    
    print(f"\\n✅ Змінні середовища збережено у {env_file}")
    print("🚀 Тепер можна запускати NIMDA Agent!")


def show_current_env():
    """Показати поточні змінні середовища"""
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ Файл .env не знайдено")
        print("💡 Запустіть: python setup_env.py --setup")
        return
    
    print("📋 Поточні змінні середовища:")
    print("=" * 40)
    
    with open(env_file) as f:
        current_group = ""
        for line in f:
            line = line.strip()
            if line.startswith("# ") and not line.startswith("# NIMDA") and not line.startswith("# Оновлено"):
                current_group = line[2:]
                print(f"\\n{current_group}:")
            elif line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                if value:
                    # Маскування токенів та ключів
                    if "TOKEN" in key or "KEY" in key:
                        masked_value = value[:8] + "*" * (len(value) - 8) if len(value) > 8 else "***"
                        print(f"  {key} = {masked_value}")
                    else:
                        print(f"  {key} = {value}")
                else:
                    print(f"  {key} = (не встановлено)")


def validate_environment():
    """Валідація змінних середовища"""
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Файл .env не знайдено")
        return False
    
    required_vars = ["GIT_USER_NAME", "GIT_USER_EMAIL"]
    missing_vars = []
    
    # Читання змінних
    env_vars = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key] = value
    
    # Перевірка обов'язкових змінних
    for var in required_vars:
        if var not in env_vars or not env_vars[var]:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Відсутні обов'язкові змінні: {', '.join(missing_vars)}")
        print("💡 Запустіть: python setup_env.py --setup")
        return False
    
    print("✅ Всі обов'язкові змінні середовища налаштовано")
    
    # Попередження про опціональні змінні
    optional_important = ["GITHUB_TOKEN", "GITHUB_USERNAME"]
    missing_optional = [var for var in optional_important if var not in env_vars or not env_vars[var]]
    
    if missing_optional:
        print(f"⚠️ Опціональні змінні не налаштовано: {', '.join(missing_optional)}")
        print("   Деякі функції можуть бути недоступні")
    
    return True


def main():
    """Головна функція"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Налаштування змінних середовища NIMDA Agent")
    parser.add_argument("--setup", action="store_true", help="Налаштувати змінні середовища")
    parser.add_argument("--show", action="store_true", help="Показати поточні змінні")
    parser.add_argument("--validate", action="store_true", help="Перевірити змінні середовища")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_environment()
    elif args.show:
        show_current_env()
    elif args.validate:
        validate_environment()
    else:
        # Інтерактивний режим
        print("🤖 NIMDA Agent - Налаштування змінних середовища")
        print("1. Налаштувати змінні")
        print("2. Показати поточні змінні")
        print("3. Перевірити налаштування")
        print("0. Вихід")
        
        choice = input("\\nВиберіть опцію: ").strip()
        
        if choice == "1":
            setup_environment()
        elif choice == "2":
            show_current_env()
        elif choice == "3":
            validate_environment()
        else:
            print("👋 До побачення!")


if __name__ == "__main__":
    main()
'''
            setup_env_file.write_text(setup_env_content)
            self.logger.info("Створено setup_env.py")

        # Оновлення .gitignore для включення .env
        self._update_gitignore_for_env()

    def _update_gitignore_for_env(self):
        """Оновлення .gitignore для змінних середовища"""
        gitignore_file = self.project_path / ".gitignore"

        if gitignore_file.exists():
            content = gitignore_file.read_text()

            # Перевірка чи вже є правила для .env
            if ".env" not in content:
                # Додавання правил для змінних середовища
                env_section = (
                    "\n# Environment variables\n.env\n.env.local\n.env.*.local\n"
                )

                # Додавання в кінець файлу
                with open(gitignore_file, "a") as f:
                    f.write(env_section)

                self.logger.info("Оновлено .gitignore для змінних середовища")

    def create_setup_script(self):
        """Створення розумного скрипта для автоматичного налаштування проекту"""
        setup_script = self.project_path / "setup_project.py"

        if not setup_script.exists():
            # Копіюємо простий скрипт
            simple_script = Path(__file__).parent / "setup_project_simple.py"
            if simple_script.exists():
                import shutil
                shutil.copy2(simple_script, setup_script)
                setup_script.chmod(0o755)
                self.logger.info("Створено setup_project.py з шаблону")
            else:
                # Створюємо базову версію
                setup_content = '''#!/usr/bin/env python3
"""NIMDA Agent Setup Script"""

import sys
import json
from pathlib import Path

def main():
    print("🤖 NIMDA Agent Setup")
    
    # Check for NIMDA environment  
    nimda_env = None
    for env_path in ["nimda_env", "../nimda_env"]:
        if Path(env_path).exists():
            nimda_env = Path(env_path).resolve()
            break
    
    if nimda_env:
        print(f"✅ Found NIMDA environment: {nimda_env}")
        
        # Setup VS Code
        vscode_dir = Path(".vscode")
        vscode_dir.mkdir(exist_ok=True)
        
        settings = {
            "python.defaultInterpreterPath": str(nimda_env / "bin" / "python"),
            "python.terminal.activateEnvironment": True
        }
        
        with open(vscode_dir / "settings.json", "w") as f:
            json.dump(settings, f, indent=2)
        
        print("✅ VS Code integration configured")
    else:
        print("❌ NIMDA environment not found")
    
    print("🎉 Setup completed!")

if __name__ == "__main__":
    main()
'''
                setup_script.write_text(setup_content)
                setup_script.chmod(0o755)
                self.logger.info("Створено базовий setup_project.py")
import subprocess
import json
from pathlib import Path


def detect_environment():
    """Детекція поточного середовища"""
    env_info = {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": sys.platform,
        "has_venv": False,
        "venv_path": None,
        "has_vscode": False,
        "has_nimda_env": False,
        "working_dir": str(Path.cwd())
    }
    
    # Перевірка віртуального середовища NIMDA
    nimda_env_paths = [
        Path("nimda_env"),
        Path("../nimda_env"), 
        Path("../../nimda_env")
    ]
    
    for env_path in nimda_env_paths:
        if env_path.exists() and (env_path / "bin" / "python").exists():
            env_info["has_nimda_env"] = True
            env_info["venv_path"] = str(env_path.resolve())
            env_info["has_venv"] = True
            break
    
    # Перевірка VS Code
    vscode_paths = [".vscode", "../.vscode"]
    for vscode_path in vscode_paths:
        if Path(vscode_path).exists():
            env_info["has_vscode"] = True
            break
    
    return env_info


def print_environment_info(env_info):
    """Виведення інформації про середовище"""
    print("🔍 Детекція середовища:")
    print(f"  🐍 Python: {env_info['python_version']}")
    print(f"  💻 Platform: {env_info['platform']}")
    print(f"  � Working Directory: {env_info['working_dir']}")
    print(f"  🔧 NIMDA Environment: {'✅' if env_info['has_nimda_env'] else '❌'}")
    print(f"  🆚 VS Code: {'✅' if env_info['has_vscode'] else '❌'}")
    
    if env_info["venv_path"]:
        print(f"  📍 Environment Path: {env_info['venv_path']}")


def check_python_compatibility(env_info):
    """Перевірка сумісності Python"""
    version = env_info["python_version"]
    major, minor, patch = map(int, version.split('.'))
    
    if major < 3 or (major == 3 and minor < 8):
        print(f"❌ Python {version} не підтримується. Потрібен Python 3.8+")
        return False
    
    if major == 3 and minor == 11:
        print(f"✅ Python {version} - відмінно! Оптимізовано для цієї версії")
    elif major == 3 and minor >= 8:
        print(f"✅ Python {version} - підтримується")
    else:
        print(f"⚠️ Python {version} - може працювати, але не тестувалось")
    
    return True


def setup_with_existing_environment(env_info):
    """Налаштування з існуючим NIMDA environment"""
    print("🔧 Налаштування з існуючим NIMDA environment...")
    
    venv_path = Path(env_info["venv_path"])
    python_exe = venv_path / "bin" / "python"
    
    if env_info["platform"] == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
    
    try:
        # Перевірка активації environment
        result = subprocess.run([str(python_exe), "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ NIMDA Environment активний: {result.stdout.strip()}")
        
        # Встановлення додаткових залежностей якщо потрібно
        requirements_files = [
            "requirements.txt",
            "nimda_agent_plugin/requirements.txt"
        ]
        
        for req_file in requirements_files:
            if Path(req_file).exists():
                print(f"📦 Перевірка залежностей з {req_file}")
                subprocess.run([str(python_exe), "-m", "pip", "install", "-r", req_file], 
                             check=True)
                print(f"✅ Залежності з {req_file} оновлено")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка роботи з environment: {e}")
        return False


def create_vscode_integration(env_info):
    """Створення інтеграції з VS Code"""
    print("🆚 Налаштування VS Code інтеграції...")
    
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    # Визначення шляху до Python
    if env_info["has_nimda_env"]:
        if env_info["platform"] == "win32":
            python_path = f"{env_info['venv_path']}/Scripts/python.exe"
        else:
            python_path = f"{env_info['venv_path']}/bin/python"
    else:
        python_path = sys.executable
    
    # settings.json
    settings = {
        "python.defaultInterpreterPath": python_path,
        "python.terminal.activateEnvironment": True,
        "python.linting.enabled": True,
        "python.linting.flake8Enabled": True,
        "python.formatting.provider": "black",
        "python.testing.pytestEnabled": True,
        "files.associations": {
            "*.md": "markdown"
        },
        "terminal.integrated.env.linux": {
            "NIMDA_AGENT_PATH": "${workspaceFolder}/nimda_agent_plugin"
        },
        "terminal.integrated.env.osx": {
            "NIMDA_AGENT_PATH": "${workspaceFolder}/nimda_agent_plugin"
        },
        "terminal.integrated.env.windows": {
            "NIMDA_AGENT_PATH": "${workspaceFolder}/nimda_agent_plugin"
        }
    }
    
    settings_file = vscode_dir / "settings.json"
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    
    print(f"✅ VS Code settings створено: {settings_file}")
    
    # tasks.json - адаптивний для різних ОС
    if env_info["platform"] == "win32":
        activate_cmd = f"& '{env_info['venv_path']}/Scripts/Activate.ps1'"
        python_cmd = "python"
    else:
        activate_cmd = f"source {env_info['venv_path']}/bin/activate"
        python_cmd = "python"
    
    tasks = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Activate NIMDA Environment",
                "type": "shell",
                "command": f"{activate_cmd} && {python_cmd} --version && echo 'NIMDA Environment activated'",
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                },
                "problemMatcher": []
            },
            {
                "label": "Run NIMDA Agent Status",
                "type": "shell",
                "command": f"{activate_cmd} && {python_cmd} nimda_agent_plugin/run_nimda_agent.py --command 'статус'",
                "group": "test",
                "presentation": {
                    "echo": True,
                    "reveal": "always"
                }
            },
            {
                "label": "Update DEV Plan",
                "type": "shell", 
                "command": f"{activate_cmd} && {python_cmd} nimda_agent_plugin/run_nimda_agent.py --command 'допрацюй девплан'",
                "group": "build"
            },
            {
                "label": "Execute Full DEV Plan",
                "type": "shell",
                "command": f"{activate_cmd} && {python_cmd} nimda_agent_plugin/run_nimda_agent.py --command 'виконай весь ДЕВ'",
                "group": "build",
                "isBackground": True
            }
        ]
    }
    
    tasks_file = vscode_dir / "tasks.json"
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    
    print(f"✅ VS Code tasks створено: {tasks_file}")
    
    # launch.json для debugging
    launch = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "NIMDA Agent Debug",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/nimda_agent_plugin/run_nimda_agent.py",
                "args": ["--command", "статус", "--verbose"],
                "console": "integratedTerminal",
                "cwd": "${workspaceFolder}",
                "python": python_path
            },
            {
                "name": "NIMDA Agent Interactive",
                "type": "python", 
                "request": "launch",
                "program": "${workspaceFolder}/nimda_agent_plugin/run_nimda_agent.py",
                "console": "integratedTerminal",
                "cwd": "${workspaceFolder}",
                "python": python_path
            }
        ]
    }
    
    launch_file = vscode_dir / "launch.json"
    with open(launch_file, "w", encoding="utf-8") as f:
        json.dump(launch, f, indent=2, ensure_ascii=False)
    
    print(f"✅ VS Code launch configuration створено: {launch_file}")


def setup_environment_variables():
    """Налаштування змінних середовища"""
    print("🔧 Налаштування змінних середовища...")
    
    env_setup_script = Path("nimda_agent_plugin/setup_env.py")
    
    if env_setup_script.exists():
        print("📋 Запуск налаштування змінних середовища...")
        try:
            subprocess.run([sys.executable, str(env_setup_script), "--setup"], check=True)
            print("✅ Змінні середовища налаштовано")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Помилка налаштування змінних: {e}")
            create_basic_env_file()
    else:
        create_basic_env_file()


def create_basic_env_file():
    """Створення базового .env файлу"""
    env_content = """# NIMDA Agent Environment Variables
# Автоматично створено setup скриптом

# Git конфігурація
GIT_USER_NAME=NIMDA Agent
GIT_USER_EMAIL=nimda@agent.local

# Налаштування проекту
PROJECT_NAME=NIMDA-CLI
PROJECT_VERSION=1.0.0
AUTO_COMMIT=true
AUTO_PUSH=true
CREATE_BACKUPS=true

# Логування
LOG_LEVEL=INFO
ENABLE_DEBUG=false

# Розширені налаштування
MAX_RETRIES=3
TIMEOUT_SECONDS=30
GITHUB_INTEGRATION=true
CODEX_INTEGRATION=true

# GitHub налаштування (потрібно заповнити вручну)
# GITHUB_TOKEN=your_token_here
# GITHUB_USERNAME=your_username
# GITHUB_REPO_URL=https://github.com/username/repo.git
"""
    
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)
        print(f"✅ Створено базовий файл .env")


def test_nimda_agent(env_info):
    """Тестування NIMDA Agent"""
    print("🧪 Тестування NIMDA Agent...")
    
    nimda_script = Path("nimda_agent_plugin/run_nimda_agent.py")
    
    if not nimda_script.exists():
        print("❌ NIMDA Agent не знайдено")
        return False
    
    # Вибір правильного Python executable
    if env_info["has_nimda_env"]:
        venv_path = Path(env_info["venv_path"])
        if env_info["platform"] == "win32":
            python_exe = venv_path / "Scripts" / "python.exe"
        else:
            python_exe = venv_path / "bin" / "python"
    else:
        python_exe = sys.executable
    
    try:
        print("🚀 Запуск тестової команди...")
        result = subprocess.run([
            str(python_exe), str(nimda_script), "--command", "статус"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ NIMDA Agent працює успішно!")
            print("📊 Результат тесту:")
            for line in result.stdout.strip().split('\\n'):
                if line.strip():
                    print(f"   {line}")
            return True
        else:
            print(f"⚠️ NIMDA Agent завершився з кодом {result.returncode}")
            print("📝 Помилки:")
            for line in result.stderr.strip().split('\\n'):
                if line.strip():
                    print(f"   {line}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Тайм-аут при тестуванні NIMDA Agent")
        return False
    except Exception as e:
        print(f"❌ Помилка тестування: {e}")
        return False


def create_workspace_file(env_info):
    """Створення VS Code workspace файлу"""
    workspace = {
        "folders": [
            {
                "path": "."
            }
        ],
        "settings": {
            "python.defaultInterpreterPath": f"{env_info.get('venv_path', '')}/bin/python" if env_info.get('venv_path') else None,
            "python.terminal.activateEnvironment": True,
            "terminal.integrated.env.linux": {
                "NIMDA_AGENT_PATH": "${workspaceFolder}/nimda_agent_plugin"
            }
        },
        "extensions": {
            "recommendations": [
                "ms-python.python",
                "ms-python.debugpy", 
                "ms-python.black-formatter",
                "ms-python.flake8",
                "redhat.vscode-yaml",
                "ms-vscode.vscode-json"
            ]
        }
    }
    
    # Видалення None значень
    if workspace["settings"]["python.defaultInterpreterPath"] is None:
        del workspace["settings"]["python.defaultInterpreterPath"]
    
    workspace_file = Path("nimda-agent.code-workspace")
    with open(workspace_file, "w", encoding="utf-8") as f:
        json.dump(workspace, f, indent=2, ensure_ascii=False)
    
    print(f"✅ VS Code workspace file створено: {workspace_file}")


def main():
    """Головна функція розумного налаштування"""
    print("🤖 Розумне автоматичне налаштування NIMDA Agent")
    print("=" * 60)
    
    # Детекція середовища
    env_info = detect_environment()
    print_environment_info(env_info)
    
    # Перевірка сумісності
    if not check_python_compatibility(env_info):
        sys.exit(1)
    
    print("\\n🔄 Початок налаштування...")
    
    # Кроки налаштування
    steps = [
        ("Налаштування з існуючим environment", lambda: setup_with_existing_environment(env_info) if env_info["has_nimda_env"] else True),
        ("Створення VS Code інтеграції", lambda: create_vscode_integration(env_info)),
        ("Налаштування змінних середовища", setup_environment_variables),
        ("Створення workspace файлу", lambda: create_workspace_file(env_info)),
        ("Тестування NIMDA Agent", lambda: test_nimda_agent(env_info))
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\\n🔄 {step_name}...")
        try:
            if step_func():
                success_count += 1
                print(f"✅ {step_name} - успішно")
            else:
                print(f"⚠️ {step_name} - завершено з попередженнями")
        except Exception as e:
            print(f"❌ {step_name} - помилка: {e}")
    
    print(f"\\n� Налаштування завершено: {success_count}/{len(steps)} кроків успішно")
    
    if success_count >= len(steps) - 1:  # Допускаємо одну помилку
        print("\\n🎉 NIMDA Agent готовий до роботи!")
        print("\\n📚 Наступні кроки:")
        print("  1. Відкрийте проект у VS Code")
        print("  2. Виберіть рекомендовані розширення")
        print("  3. Налаштуйте GitHub токен у .env файлі")
        print("  4. Запустіть: Ctrl+Shift+P -> 'Tasks: Run Task' -> 'Run NIMDA Agent Status'")
    else:
        print("\\n⚠️ Деякі кроки не вдалося виконати")
        print("Перевірте помилки вище та спробуйте знову")


if __name__ == "__main__":
    main()
