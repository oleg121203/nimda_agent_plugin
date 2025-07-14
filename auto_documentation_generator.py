#!/usr/bin/env python3
"""
Auto Documentation Generator - Intelligent documentation creation
Features:
- Automated code analysis and documentation extraction
- Markdown generation with structure and formatting
- API documentation with examples
- Integration with creative hooks for enhanced descriptions
- Multi-language support (Ukrainian, English, Russian)
"""

import ast
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

from creative_hooks_examples import CreativeHookRegistry


class AutoDocumentationGenerator:
    """
    Intelligent documentation generator with AI assistance
    """

    def __init__(self, project_path: str = "/Users/dev/Documents/nimda_agent_plugin"):
        self.project_path = Path(project_path)
        self.creative_hooks = CreativeHookRegistry()

        # Documentation settings
        self.languages = ["ukrainian", "english"]  # Primary languages
        self.output_formats = ["markdown", "html", "json"]
        self.include_private = False
        self.include_examples = True

        # Analysis results
        self.analyzed_modules = {}
        self.project_structure = {}
        self.api_endpoints = []

        # Templates
        self.templates = self._load_templates()

    def generate_complete_documentation(self) -> Dict[str, str]:
        """Generate complete project documentation"""
        print("📚 Generating complete project documentation...")

        # Analyze project structure
        self._analyze_project_structure()

        # Analyze code modules
        self._analyze_all_modules()

        # Generate different types of documentation
        docs = {}

        # Main README
        docs["README.md"] = self._generate_main_readme()

        # API Documentation
        docs["API_DOCUMENTATION.md"] = self._generate_api_documentation()

        # Developer Guide
        docs["DEVELOPER_GUIDE.md"] = self._generate_developer_guide()

        # Architecture Overview
        docs["ARCHITECTURE.md"] = self._generate_architecture_documentation()

        # User Manual
        docs["USER_MANUAL.md"] = self._generate_user_manual()

        # Installation Guide
        docs["INSTALLATION.md"] = self._generate_installation_guide()

        # Save all documentation
        self._save_documentation(docs)

        print(f"✅ Generated {len(docs)} documentation files")
        return docs

    def _analyze_project_structure(self):
        """Analyze the overall project structure"""
        print("   📂 Analyzing project structure...")

        structure = {
            "name": self.project_path.name,
            "path": str(self.project_path),
            "files": [],
            "directories": [],
            "python_files": [],
            "config_files": [],
            "documentation_files": [],
        }

        for item in self.project_path.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(self.project_path)
                structure["files"].append(str(rel_path))

                if item.suffix == ".py":
                    structure["python_files"].append(str(rel_path))
                elif item.suffix in [".md", ".rst", ".txt"]:
                    structure["documentation_files"].append(str(rel_path))
                elif item.name in [
                    "requirements.txt",
                    "setup.py",
                    "pyproject.toml",
                    ".gitignore",
                ]:
                    structure["config_files"].append(str(rel_path))

            elif item.is_dir() and not any(
                skip in str(item) for skip in ["__pycache__", ".git", ".venv"]
            ):
                rel_path = item.relative_to(self.project_path)
                structure["directories"].append(str(rel_path))

        self.project_structure = structure

    def _analyze_all_modules(self):
        """Analyze all Python modules in the project"""
        print("   🔍 Analyzing Python modules...")

        for py_file in self.project_structure["python_files"]:
            file_path = self.project_path / py_file
            try:
                module_info = self._analyze_module(file_path)
                self.analyzed_modules[py_file] = module_info
            except Exception as e:
                print(f"   ⚠️ Could not analyze {py_file}: {e}")

    def _analyze_module(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python module"""
        module_info = {
            "file_path": str(file_path),
            "name": file_path.stem,
            "docstring": "",
            "classes": [],
            "functions": [],
            "constants": [],
            "imports": [],
            "complexity_score": 0,
        }

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)

            # Extract module docstring
            if (
                tree.body
                and isinstance(tree.body[0], ast.Expr)
                and isinstance(tree.body[0].value, ast.Constant)
            ):
                module_info["docstring"] = tree.body[0].value.value

            # Analyze AST nodes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = self._analyze_class(node, source)
                    module_info["classes"].append(class_info)

                elif isinstance(node, ast.FunctionDef):
                    if not any(
                        node.name in cls["methods"] for cls in module_info["classes"]
                    ):
                        func_info = self._analyze_function(node, source)
                        module_info["functions"].append(func_info)

                elif isinstance(node, ast.Assign):
                    const_info = self._analyze_constant(node, source)
                    if const_info:
                        module_info["constants"].append(const_info)

                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_info = self._analyze_import(node)
                    module_info["imports"].extend(import_info)

            # Calculate complexity
            module_info["complexity_score"] = self._calculate_complexity(tree)

        except Exception as e:
            print(f"   ⚠️ Error analyzing {file_path}: {e}")

        return module_info

    def _analyze_class(self, node: ast.ClassDef, source: str) -> Dict[str, Any]:
        """Analyze a class definition"""
        class_info = {
            "name": node.name,
            "docstring": ast.get_docstring(node) or "",
            "methods": [],
            "attributes": [],
            "inheritance": [
                base.id for base in node.bases if isinstance(base, ast.Name)
            ],
            "line_number": node.lineno,
        }

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._analyze_function(item, source, is_method=True)
                class_info["methods"].append(method_info)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        class_info["attributes"].append(target.id)

        return class_info

    def _analyze_function(
        self, node: ast.FunctionDef, source: str, is_method: bool = False
    ) -> Dict[str, Any]:
        """Analyze a function definition"""
        func_info = {
            "name": node.name,
            "docstring": ast.get_docstring(node) or "",
            "parameters": [],
            "return_type": None,
            "is_async": isinstance(node, ast.AsyncFunctionDef),
            "is_method": is_method,
            "is_private": node.name.startswith("_"),
            "line_number": node.lineno,
            "complexity": len(list(ast.walk(node))),
        }

        # Analyze parameters
        for arg in node.args.args:
            param_info = {"name": arg.arg, "annotation": None, "default": None}

            if arg.annotation:
                param_info["annotation"] = ast.unparse(arg.annotation)

            func_info["parameters"].append(param_info)

        # Analyze return type
        if node.returns:
            func_info["return_type"] = ast.unparse(node.returns)

        return func_info

    def _analyze_constant(
        self, node: ast.Assign, source: str
    ) -> Optional[Dict[str, Any]]:
        """Analyze constant assignments"""
        if (
            len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id.isupper()
        ):
            return {
                "name": node.targets[0].id,
                "value": ast.unparse(node.value) if hasattr(ast, "unparse") else "...",
                "line_number": node.lineno,
            }
        return None

    def _analyze_import(self, node) -> List[Dict[str, Any]]:
        """Analyze import statements"""
        imports = []

        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    {
                        "type": "import",
                        "module": alias.name,
                        "alias": alias.asname,
                        "line_number": node.lineno,
                    }
                )
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append(
                    {
                        "type": "from_import",
                        "module": node.module,
                        "name": alias.name,
                        "alias": alias.asname,
                        "line_number": node.lineno,
                    }
                )

        return imports

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.Try):
                complexity += len(node.handlers)
            elif isinstance(
                node, (ast.Lambda, ast.ListComp, ast.DictComp, ast.SetComp)
            ):
                complexity += 1

        return complexity

    def _generate_main_readme(self) -> str:
        """Generate main README.md file"""
        print("   📝 Generating main README...")

        readme_content = f"""# {self.project_structure["name"].replace("_", " ").title()}

## 🚀 Огляд проекту

**NIMDA Agent** - це інтелектуальний багатодоменний AI-агент з глибоким розумінням контексту та адаптивними можливостями.

### ✨ Ключові особливості

- 🧠 **Інтелектуальна обробка**: Адаптивне мислення та творче вирішення проблем
- 🔧 **Універсальність**: Підтримка різних технологій без хардкоду
- 🎨 **Творчі хуки**: Інтеграція з Codex AI для розширених можливостей
- 📋 **Трирівневе управління задачами**: Автоматична генерація підзадач
- 🛡️ **Надійність**: Система самовідновлення та аварійного відновлення

## 📁 Структура проекту

```
{self.project_structure["name"]}/
├── 📄 Основні модулі ({len(self.project_structure["python_files"])})
├── 📁 Каталоги ({len(self.project_structure["directories"])})
├── ⚙️ Конфігураційні файли ({len(self.project_structure["config_files"])})
└── 📚 Документація ({len(self.project_structure["documentation_files"])})
```

## 🔧 Основні компоненти

{self._generate_components_overview()}

## 🚀 Швидкий старт

### Встановлення

```bash
# Клонування репозиторію
git clone https://github.com/oleg121203/nimda_agent_plugin.git
cd nimda_agent_plugin

# Встановлення залежностей
pip install -r requirements.txt

# Запуск системи
python main.py
```

### Базове використання

```python
from nimda_agent import NIMDAAgent

# Ініціалізація агента
agent = NIMDAAgent()

# Запуск інтерактивного режиму
agent.run_interactive_mode()
```

## 📚 Документація

- [📖 Посібник розробника](DEVELOPER_GUIDE.md)
- [🏗️ Архітектура системи](ARCHITECTURE.md)
- [📋 API документація](API_DOCUMENTATION.md)
- [👤 Посібник користувача](USER_MANUAL.md)
- [⚙️ Інструкція з встановлення](INSTALLATION.md)

## 🤝 Внесок у розробку

Ми вітаємо внески у розвиток проекту! Будь ласка, ознайомтеся з [посібником розробника](DEVELOPER_GUIDE.md) для отримання детальної інформації.

## 📄 Ліцензія

Цей проект розповсюджується під ліцензією MIT. Дивіться файл [LICENSE](LICENSE) для деталей.

## 👥 Автори

- **Oleg Palamarchuk** - *Основний розробник* - [@oleg121203](https://github.com/oleg121203)

## 🔗 Корисні посилання

- [GitHub Repository](https://github.com/oleg121203/nimda_agent_plugin)
- [Issues](https://github.com/oleg121203/nimda_agent_plugin/issues)
- [Releases](https://github.com/oleg121203/nimda_agent_plugin/releases)

---

*Згенеровано автоматично • {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

        return readme_content

    def _generate_components_overview(self) -> str:
        """Generate overview of main components"""
        components = []

        for module_name, module_info in self.analyzed_modules.items():
            if module_info["classes"] or module_info["functions"]:
                component_desc = f"**{module_name}** - {module_info.get('docstring', 'Опис недоступний')[:100]}..."
                components.append(component_desc)

        return "\n".join(f"- {comp}" for comp in components[:10])  # Limit to 10

    def _generate_api_documentation(self) -> str:
        """Generate API documentation"""
        print("   📋 Generating API documentation...")

        api_content = f"""# API Документація

## 🔗 Огляд API

Цей документ містить повну документацію API для NIMDA Agent системи.

## 📋 Зміст

{self._generate_api_toc()}

## 🏗️ Модулі та класи

{self._generate_api_modules()}

## 📝 Приклади використання

{self._generate_api_examples()}

---

*Згенеровано автоматично • {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

        return api_content

    def _generate_api_toc(self) -> str:
        """Generate table of contents for API documentation"""
        toc_items = []

        for module_name, module_info in self.analyzed_modules.items():
            if module_info["classes"]:
                toc_items.append(
                    f"- [{module_name}](#{module_name.replace('.', '').replace('_', '-')})"
                )

        return "\n".join(toc_items)

    def _generate_api_modules(self) -> str:
        """Generate detailed API module documentation"""
        modules_content = []

        for module_name, module_info in self.analyzed_modules.items():
            if not module_info["classes"] and not module_info["functions"]:
                continue

            module_section = f"""
### {module_name}

{module_info.get("docstring", "*Опис недоступний*")}

**Складність модуля**: {module_info.get("complexity_score", 0)}

#### Класи

{self._generate_classes_docs(module_info["classes"])}

#### Функції

{self._generate_functions_docs(module_info["functions"])}

#### Константи

{self._generate_constants_docs(module_info["constants"])}
"""
            modules_content.append(module_section)

        return "\n".join(modules_content)

    def _generate_classes_docs(self, classes: List[Dict]) -> str:
        """Generate documentation for classes"""
        if not classes:
            return "*Класи відсутні*"

        classes_docs = []

        for class_info in classes:
            class_doc = f"""
##### `{class_info["name"]}`

{class_info.get("docstring", "*Опис недоступний*")}

**Успадкування**: {", ".join(class_info["inheritance"]) if class_info["inheritance"] else "Відсутнє"}

**Методи** ({len(class_info["methods"])}):
{self._generate_methods_list(class_info["methods"])}

**Атрибути**: {", ".join(class_info["attributes"]) if class_info["attributes"] else "Відсутні"}
"""
            classes_docs.append(class_doc)

        return "\n".join(classes_docs)

    def _generate_methods_list(self, methods: List[Dict]) -> str:
        """Generate list of methods"""
        if not methods:
            return "*Методи відсутні*"

        method_items = []
        for method in methods:
            visibility = "🔒" if method["is_private"] else "🔓"
            async_marker = "⚡" if method["is_async"] else ""

            params = ", ".join([p["name"] for p in method["parameters"]])
            method_signature = f"`{method['name']}({params})`"

            method_items.append(f"- {visibility}{async_marker} {method_signature}")
            if method["docstring"]:
                method_items.append(f"  *{method['docstring'][:100]}...*")

        return "\n".join(method_items)

    def _generate_functions_docs(self, functions: List[Dict]) -> str:
        """Generate documentation for functions"""
        if not functions:
            return "*Функції відсутні*"

        func_docs = []

        for func in functions:
            if self.include_private or not func["is_private"]:
                params = ", ".join(
                    [
                        f"{p['name']}: {p.get('annotation', 'Any')}"
                        for p in func["parameters"]
                    ]
                )

                func_signature = f"`{func['name']}({params})`"
                if func["return_type"]:
                    func_signature += f" -> `{func['return_type']}`"

                func_doc = f"""
**{func_signature}**

{func.get("docstring", "*Опис недоступний*")}

*Складність*: {func.get("complexity", 0)} | *Асинхронна*: {"Так" if func["is_async"] else "Ні"}
"""
                func_docs.append(func_doc)

        return "\n".join(func_docs)

    def _generate_constants_docs(self, constants: List[Dict]) -> str:
        """Generate documentation for constants"""
        if not constants:
            return "*Константи відсутні*"

        const_items = []
        for const in constants:
            const_items.append(f"- `{const['name']}` = `{const['value']}`")

        return "\n".join(const_items)

    def _generate_api_examples(self) -> str:
        """Generate API usage examples"""
        return """
### Базові приклади

#### Ініціалізація системи

```python
from nimda_agent import NIMDAAgent
from advanced_task_manager import AdvancedTaskManager

# Створення агента
agent = NIMDAAgent(project_path="/path/to/project")

# Ініціалізація менеджера задач
task_manager = AdvancedTaskManager("/path/to/project")
task_manager.initialize_from_dev_plan()
```

#### Робота з творчими хуками

```python
from creative_hooks_examples import CreativeHookRegistry

# Ініціалізація хуків
hooks = CreativeHookRegistry()

# Використання хука для налаштування середовища
context = {
    "language": "python",
    "version": "3.11",
    "project_config": {"type": "ai_system"}
}

result = hooks.environment_setup_hook(context)
```

#### Інтелектуальна пріоритизація задач

```python
from ai_task_prioritizer import AITaskPrioritizer

# Створення пріоритизатора
prioritizer = AITaskPrioritizer()

# Додавання задачі
task_id = prioritizer.add_task({
    "title": "Реалізувати новий AI модуль",
    "description": "Додати можливості машинного навчання",
    "priority": "high",
    "estimated_time": 240
})

# Отримання пріоритизованого списку
prioritized_tasks = prioritizer.prioritize_tasks()
```
"""

    def _generate_developer_guide(self) -> str:
        """Generate developer guide"""
        print("   👨‍💻 Generating developer guide...")

        return f"""# Посібник розробника

## 🎯 Вступ

Цей посібник допоможе вам розпочати розробку та внесення змін у проект NIMDA Agent.

## 🏗️ Архітектура системи

### Основні принципи

1. **Модульність** - Кожен компонент є незалежним
2. **Універсальність** - Відсутність хардкоду технологій
3. **Інтелектуальність** - AI-driven рішення
4. **Адаптивність** - Динамічне налаштування

### Структура коду

{self._generate_code_structure_docs()}

## 🔧 Налаштування середовища розробки

### Вимоги

- Python 3.11+
- Git
- VS Code (рекомендовано)

### Кроки встановлення

```bash
# 1. Клонування репозиторію
git clone https://github.com/oleg121203/nimda_agent_plugin.git
cd nimda_agent_plugin

# 2. Створення віртуального середовища
python -m venv venv
source venv/bin/activate  # Linux/Mac
# або
venv\\Scripts\\activate  # Windows

# 3. Встановлення залежностей
pip install -r requirements.txt

# 4. Запуск тестів
python -m pytest tests/
```

## 🧪 Тестування

### Запуск тестів

```bash
# Всі тести
python -m pytest

# Конкретний модуль
python -m pytest tests/test_advanced_task_manager.py

# З покриттям
python -m pytest --cov=.
```

### Написання тестів

```python
import unittest
from advanced_task_manager import AdvancedTaskManager

class TestAdvancedTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = AdvancedTaskManager("/test/path")
    
    def test_initialization(self):
        self.assertIsNotNone(self.manager)
        self.assertEqual(self.manager.python_version, "3.11")
```

## 📝 Стиль коду

### Конвенції

- Використовуйте **snake_case** для функцій та змінних
- Використовуйте **PascalCase** для класів
- Докстрінги у форматі Google Style
- Максимальна довжина рядка: 88 символів

### Приклад коду

```python
class ExampleClass:
    \"\"\"
    Приклад класу з правильним форматуванням.
    
    Args:
        param1: Опис першого параметра
        param2: Опис другого параметра
    \"\"\"
    
    def __init__(self, param1: str, param2: int):
        self.param1 = param1
        self.param2 = param2
    
    def example_method(self) -> str:
        \"\"\"Приклад методу з документацією.\"\"\"
        return f"{{self.param1}}: {{self.param2}}"
```

## 🔄 Робочий процес

### Внесення змін

1. Створіть нову гілку: `git checkout -b feature/your-feature`
2. Внесіть зміни та додайте тести
3. Запустіть тести: `python -m pytest`
4. Зафіксуйте зміни: `git commit -m "Add: your feature"`
5. Відправте на GitHub: `git push origin feature/your-feature`
6. Створіть Pull Request

### Код-рев'ю

Всі Pull Request проходять код-рев'ю. Переконайтеся, що:

- ✅ Всі тести проходять
- ✅ Код відповідає стилю проекту
- ✅ Додана документація
- ✅ Немає критичних помилок

## 🚀 Розгортання

### Локальне розгортання

```bash
python main.py
```

### Продуктивне розгортання

```bash
# Створення дистрибутива
python setup.py sdist bdist_wheel

# Встановлення
pip install dist/nimda_agent-*.whl
```

## 📚 Корисні ресурси

- [Документація Python AST](https://docs.python.org/3/library/ast.html)
- [PEP 8 - Style Guide](https://pep8.org/)
- [Type Hints Guide](https://docs.python.org/3/library/typing.html)

---

*Згенеровано автоматично • {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    def _generate_code_structure_docs(self) -> str:
        """Generate code structure documentation"""
        structure_info = []

        # Group files by type
        core_modules = [
            f
            for f in self.project_structure["python_files"]
            if not f.startswith("test_")
        ]
        test_modules = [
            f for f in self.project_structure["python_files"] if f.startswith("test_")
        ]

        if core_modules:
            structure_info.append("**Основні модулі:**")
            for module in core_modules[:10]:  # Limit to 10
                structure_info.append(
                    f"- `{module}` - {self._get_module_description(module)}"
                )

        if test_modules:
            structure_info.append("\n**Тестові модулі:**")
            for module in test_modules[:5]:  # Limit to 5
                structure_info.append(f"- `{module}`")

        return "\n".join(structure_info)

    def _get_module_description(self, module_name: str) -> str:
        """Get brief description of a module"""
        module_info = self.analyzed_modules.get(module_name, {})
        docstring = module_info.get("docstring", "")

        if docstring:
            return docstring.split("\n")[0][:80] + "..."
        return "Опис недоступний"

    def _generate_architecture_documentation(self) -> str:
        """Generate architecture documentation"""
        print("   🏗️ Generating architecture documentation...")

        return f"""# Архітектура системи

## 🏗️ Огляд архітектури

NIMDA Agent побудований на основі модульної архітектури з чіткими межами між компонентами.

## 📊 Схема компонентів

```
┌─────────────────────────────────────────────────────────────┐
│                    NIMDA Agent System                      │
├─────────────────────────────────────────────────────────────┤
│  🎯 Ultimate Interactive Workflow                          │
│  ├── 🧠 AI Task Prioritizer                               │
│  ├── 🔍 Smart Error Detector                              │
│  └── 📚 Auto Documentation Generator                      │
├─────────────────────────────────────────────────────────────┤
│  📋 Task Management Layer                                  │
│  ├── AdvancedTaskManager (3-level tasks)                  │
│  ├── UniversalTaskManager (universal execution)           │
│  └── DevPlanManager (plan parsing)                        │
├─────────────────────────────────────────────────────────────┤
│  🎨 Creative Hooks Layer                                   │
│  ├── CreativeHookRegistry (hook management)               │
│  ├── EnvironmentSetupHook (environment)                   │
│  ├── ComponentCreationHook (AI generation)                │
│  └── ErrorResolutionHook (error fixing)                   │
├─────────────────────────────────────────────────────────────┤
│  🔍 Analysis Layer                                         │
│  ├── FocusedSystemAnalyzer (code analysis)                │
│  ├── DeepContextWorkflow (context analysis)               │
│  └── PerformanceMonitor (metrics)                         │
├─────────────────────────────────────────────────────────────┤
│  🤖 Agent Layer                                            │
│  ├── ChatAgent (communication)                            │
│  ├── AdaptiveThinker (problem solving)                    │
│  ├── LearningModule (ML capabilities)                     │
│  └── WorkerAgent (task execution)                         │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Основні компоненти

{self._generate_component_details()}

## 🔄 Потоки даних

### 1. Ініціалізація системи
1. **Завантаження конфігурації** з DEV_PLAN.md
2. **Ініціалізація творчих хуків**
3. **Створення менеджерів задач**
4. **Запуск аналізаторів**

### 2. Виконання задач
1. **Парсинг DEV_PLAN.md** → Основні задачі (Level 1)
2. **Автогенерація підзадач** → Деталізовані задачі (Level 2)
3. **AI пріоритизація** → Оптимізований порядок
4. **Виконання з моніторингом** → Мікрозадачі (Level 3)

### 3. Обробка помилок
1. **Виявлення помилок** Smart Error Detector
2. **Класифікація та аналіз**
3. **Застосування творчих рішень**
4. **Валідація виправлень**

## 🎨 Система творчих хуків

Творчі хуки забезпечують розширюваність системи:

```python
# Реєстрація хука
def custom_hook(context):
    # Кастомна логіка
    return result

workflow.register_creative_hook("custom_action", custom_hook)
```

### Типи хуків

- **environment_setup** - Налаштування середовища
- **component_creation** - Генерація компонентів
- **error_resolution** - Вирішення помилок
- **creative_solution** - Загальні рішення

## 📋 Управління станом

### Стан системи

```python
{{
    "current_phase": 2,
    "completed_tasks": 15,
    "total_tasks": 75,
    "errors_detected": 3,
    "errors_resolved": 2,
    "last_update": "2025-07-14T20:30:00"
}}
```

### Персистентність

- **Задачі**: `task_structure.json`
- **Помилки**: `error_history.json`
- **Налаштування**: `project_config.json`
- **Логи**: `nimda_app.log`

## 🔒 Безпека

### Принципи безпеки

1. **Валідація вводу** - Всі дані перевіряються
2. **Ізоляція процесів** - Безпечне виконання
3. **Логування дій** - Аудит всіх операцій
4. **Обмеження доступу** - Контроль привілеїв

## 📈 Масштабованість

### Горизонтальне масштабування

- Розподілення задач між воркерами
- Асинхронне виконання
- Черги задач

### Вертикальне масштабування

- Оптимізація алгоритмів
- Кешування результатів
- Індексування даних

## 🔮 Майбутній розвиток

### Плани розширення

1. **Розподілена архітектура** - Кластер агентів
2. **Машинне навчання** - Покращення AI компонентів
3. **Хмарна інтеграція** - Підтримка AWS/Azure/GCP
4. **Мобільні додатки** - Клієнти для iOS/Android

---

*Згенеровано автоматично • {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    def _generate_component_details(self) -> str:
        """Generate detailed component information"""
        components = [
            {
                "name": "Ultimate Interactive Workflow",
                "description": "Головний оркестратор системи, об'єднує всі компоненти",
                "responsibilities": [
                    "Координація фаз",
                    "Інтерактивний режим",
                    "Відновлення помилок",
                ],
            },
            {
                "name": "AI Task Prioritizer",
                "description": "Інтелектуальна пріоритизація задач з машинним навчанням",
                "responsibilities": [
                    "Аналіз контексту",
                    "Навчання з історії",
                    "Оптимізація порядку",
                ],
            },
            {
                "name": "Smart Error Detector",
                "description": "Система виявлення та виправлення помилок",
                "responsibilities": [
                    "Статичний аналіз",
                    "Виявлення паттернів",
                    "Автоматичне виправлення",
                ],
            },
            {
                "name": "Creative Hook Registry",
                "description": "Система розширень для Codex AI інтеграції",
                "responsibilities": [
                    "Реєстрація хуків",
                    "Контекстуальні рішення",
                    "AI розширення",
                ],
            },
        ]

        component_docs = []
        for comp in components:
            comp_doc = f"""
### {comp["name"]}

{comp["description"]}

**Відповідальності:**
{chr(10).join(f"- {resp}" for resp in comp["responsibilities"])}
"""
            component_docs.append(comp_doc)

        return "\n".join(component_docs)

    def _generate_user_manual(self) -> str:
        """Generate user manual"""
        print("   👤 Generating user manual...")

        return f"""# Посібник користувача

## 👋 Ласкаво просимо до NIMDA Agent

Цей посібник допоможе вам розпочати роботу з NIMDA Agent - інтелектуальною системою розробки.

## 🚀 Швидкий старт

### Перший запуск

1. **Встановлення системи**
   ```bash
   cd nimda_agent_plugin
   python main.py
   ```

2. **Вибір режиму роботи**
   - 🎯 Інтерактивний режим (рекомендовано)
   - ⚡ Автоматичний режим
   - 🔍 Режим аналізу

3. **Налаштування проекту**
   - Система автоматично проаналізує DEV_PLAN.md
   - Створить структуру задач
   - Ініціалізує необхідні компоненти

## 🎯 Режими роботи

### Інтерактивний режим

Найкращий для навчання та контролю процесу:

```bash
python ultimate_interactive_workflow.py
```

**Особливості:**
- Паузи для перегляду результатів
- Можливість втручання на кожному кроці
- Детальне логування процесу
- Інтеграція з Codex AI

### Автоматичний режим

Для повністю автономного виконання:

```bash
python auto_dev_runner.py
```

**Особливості:**
- Повна автоматизація
- Мінімальне втручання користувача
- Швидке виконання
- Автоматичне відновлення

## 📋 Управління задачами

### Перегляд задач

```python
from ai_task_prioritizer import AITaskPrioritizer

prioritizer = AITaskPrioritizer()
tasks = prioritizer.prioritize_tasks()

for task in tasks:
    print(f"{{task['title']}} - Пріоритет: {{task['ai_score']:.2f}}")
```

### Додавання нових задач

```python
task_id = prioritizer.add_task({{
    "title": "Ваша задача",
    "description": "Детальний опис",
    "priority": "high",  # high, medium, low
    "estimated_time": 120,  # хвилини
    "tags": ["feature", "ui"]
}})
```

### Відзначення як виконано

```python
prioritizer.complete_task(task_id, {{
    "actual_time": 90,
    "satisfaction_rating": 5,  # 1-5
    "difficulty_rating": 3    # 1-5
}})
```

## 🔍 Моніторинг помилок

### Автоматичне виявлення

Система автоматично сканує проект на наявність:

- ❌ Синтаксичні помилки
- 📦 Проблеми з імпортами
- ⚠️ Потенційні runtime помилки
- 🎨 Порушення стилю коду
- 📋 Проблеми залежностей

### Ручне сканування

```python
from smart_error_detector import SmartErrorDetector

detector = SmartErrorDetector()
errors = detector.detect_all_errors()

for error in errors:
    print(f"{{error['type']}}: {{error['message']}}")
```

### Автоматичне виправлення

```python
for error in errors:
    result = detector.resolve_error(error)
    if result['resolved']:
        print(f"Виправлено: {{error['message']}}")
```

## 🎨 Творчі можливості

### Використання AI хуків

Система підтримує розширення через творчі хуки:

```python
from creative_hooks_examples import CreativeHookRegistry

hooks = CreativeHookRegistry()

# Налаштування середовища з AI
result = hooks.environment_setup_hook({{
    "language": "python",
    "version": "3.11",
    "project_config": {{"type": "ai_system"}}
}})
```

### Генерація компонентів

```python
# AI генерація нових компонентів
result = hooks.component_creation_hook({{
    "action": "create_component",
    "component_name": "NewAIModule",
    "config": {{"type": "learning_module"}},
    "project_config": {{"type": "ai_system"}}
}})
```

## 📊 Аналітика та звіти

### Перегляд метрик

```python
# Метрики задач
insights = prioritizer.generate_task_insights()
print(f"Завершено задач: {{insights['completed_tasks']}}")
print(f"Рівень завершення: {{insights['completion_rate']:.1%}}")

# Звіт про помилки
report = detector.generate_error_report()
print(f"Всього помилок: {{report['total_errors']}}")
print(f"Рівень вирішення: {{report['resolution_stats']['resolution_rate']:.1%}}")
```

### Експорт звітів

Система автоматично генерує звіти у форматах:
- 📄 Markdown
- 📊 JSON
- 📋 HTML

## ⚙️ Налаштування

### Конфігураційні файли

- `DEV_PLAN.md` - Основний план розробки
- `ai_task_data.json` - Дані задач та навчання
- `error_history.json` - Історія помилок
- `project_config.json` - Налаштування проекту

### Персоналізація

```python
# Налаштування пріоритизатора
prioritizer.context_weights = {{
    "urgency": 0.4,      # Більше уваги до терміновості
    "complexity": 0.1,   # Менше уваги до складності
    "dependencies": 0.3,
    "user_preference": 0.2
}}

# Налаштування детектора помилок
detector.detection_sources = [
    "syntax_errors",
    "import_errors",
    "runtime_errors"
]
```

## 🆘 Допомога та підтримка

### Часті питання

**Q: Система не знаходить Python 3.11**
A: Переконайтеся, що Python 3.11 встановлений та додано до PATH

**Q: Помилки імпорту модулів**
A: Запустіть `pip install -r requirements.txt`

**Q: Система працює повільно**
A: Збільште `pause_duration` або відключіть детальне логування

### Отримання допомоги

- 📧 Email: support@nimda-agent.com
- 🐛 Issues: [GitHub Issues](https://github.com/oleg121203/nimda_agent_plugin/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/oleg121203/nimda_agent_plugin/discussions)

## 🔗 Додаткові ресурси

- [📖 Документація API](API_DOCUMENTATION.md)
- [🏗️ Архітектура](ARCHITECTURE.md)
- [👨‍💻 Посібник розробника](DEVELOPER_GUIDE.md)

---

*Згенеровано автоматично • {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    def _generate_installation_guide(self) -> str:
        """Generate installation guide"""
        print("   ⚙️ Generating installation guide...")

        return f"""# Інструкція з встановлення

## 📋 Системні вимоги

### Мінімальні вимоги

- **Операційна система**: macOS 10.15+, Windows 10+, Linux Ubuntu 18.04+
- **Python**: 3.11 або вище
- **Пам'ять**: 4 GB RAM
- **Дисковий простір**: 2 GB вільного місця
- **Інтернет**: Для завантаження залежностей

### Рекомендовані вимоги

- **Python**: 3.11.5+
- **Пам'ять**: 8 GB RAM
- **Процесор**: 4+ ядра
- **SSD**: Для кращої продуктивності

## 🐍 Встановлення Python 3.11

### macOS

```bash
# Через Homebrew (рекомендовано)
brew install python@3.11

# Через pyenv
pyenv install 3.11.5
pyenv global 3.11.5

# Перевірка версії
python3.11 --version
```

### Windows

```powershell
# Завантажте з офіційного сайту
# https://www.python.org/downloads/windows/

# Або через Chocolatey
choco install python311

# Перевірка версії
python --version
```

### Linux (Ubuntu/Debian)

```bash
# Додавання репозиторію
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Встановлення Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-pip

# Перевірка версії
python3.11 --version
```

## 📥 Завантаження NIMDA Agent

### Через Git (рекомендовано)

```bash
# Клонування репозиторію
git clone https://github.com/oleg121203/nimda_agent_plugin.git
cd nimda_agent_plugin

# Перевірка цілісності
git log --oneline -5
```

### Завантаження ZIP

1. Перейдіть на https://github.com/oleg121203/nimda_agent_plugin
2. Натисніть "Code" → "Download ZIP"
3. Розпакуйте архів
4. Перейдіть до папки проекту

## 🔧 Налаштування середовища

### Створення віртуального середовища

```bash
# Створення venv
python3.11 -m venv nimda_env

# Активація (macOS/Linux)
source nimda_env/bin/activate

# Активація (Windows)
nimda_env\\Scripts\\activate

# Перевірка активації
which python  # має показати шлях до venv
```

### Встановлення залежностей

```bash
# Оновлення pip
python -m pip install --upgrade pip

# Встановлення основних залежностей
pip install -r requirements.txt

# Встановлення додаткових залежностей (опціонально)
pip install -r requirements_nimda_v3.txt

# Перевірка встановлення
pip list
```

## 📋 Основні залежності

Автоматично встановлюються:

```
# Core dependencies
pyside6>=6.5.0          # GUI framework
aiohttp>=3.8.0          # Async HTTP client
asyncio-mqtt>=0.13.0    # MQTT support
python-dotenv>=1.0.0    # Environment variables
psutil>=5.9.0           # System monitoring
watchdog>=3.0.0         # File system monitoring

# AI/ML dependencies  
numpy>=1.24.0           # Numerical computing
scipy>=1.10.0           # Scientific computing
scikit-learn>=1.3.0     # Machine learning
transformers>=4.30.0    # NLP models

# Development dependencies
pytest>=7.4.0           # Testing framework
black>=23.0.0           # Code formatting
flake8>=6.0.0           # Linting
mypy>=1.5.0             # Type checking
```

## ✅ Перевірка встановлення

### Базова перевірка

```bash
# Перевірка Python версії
python --version
# Має показати: Python 3.11.x

# Перевірка основних модулів
python -c "import PySide6; print('PySide6:', PySide6.__version__)"
python -c "import numpy; print('NumPy:', numpy.__version__)"
python -c "import aiohttp; print('aiohttp:', aiohttp.__version__)"
```

### Тест базової функціональності

```bash
# Тест імпортів
python -c "
from dev_plan_manager import DevPlanManager
from advanced_task_manager import AdvancedTaskManager
from creative_hooks_examples import CreativeHookRegistry
print('✅ Всі основні модулі імпортуються успішно')
"

# Тест ініціалізації
python -c "
from ultimate_interactive_workflow import UltimateInteractiveWorkflow
workflow = UltimateInteractiveWorkflow()
print('✅ Основний воркфлоу ініціалізується успішно')
"
```

## 🚀 Перший запуск

### Швидкий тест

```bash
# Запуск демо режиму
python -c "
from ai_task_prioritizer import AITaskPrioritizer
prioritizer = AITaskPrioritizer()
print('🎯 AI Task Prioritizer готовий')

from smart_error_detector import SmartErrorDetector  
detector = SmartErrorDetector()
print('🔍 Smart Error Detector готовий')

print('🎉 Система готова до роботи!')
"
```

### Повний запуск

```bash
# Запуск інтерактивного режиму
python ultimate_interactive_workflow.py

# Або автоматичного режиму
python auto_dev_runner.py
```

## 🔧 Налаштування IDE

### VS Code

Рекомендовані розширення:

```json
{{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter", 
    "ms-python.flake8",
    "ms-python.mypy-type-checker",
    "ms-vscode.vscode-json"
  ]
}}
```

Налаштування `.vscode/settings.json`:

```json
{{
  "python.defaultInterpreterPath": "./nimda_env/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.testing.pytestEnabled": true
}}
```

### PyCharm

1. **File** → **Settings** → **Project** → **Python Interpreter**
2. Виберіть `nimda_env/bin/python`
3. **Tools** → **External Tools** → Додайте Black та Flake8

## 🐛 Усунення проблем

### Поширені помилки

**1. ModuleNotFoundError: No module named 'PySide6'**

```bash
# Переактивуйте venv та переустановіть
deactivate
source nimda_env/bin/activate
pip install --force-reinstall PySide6
```

**2. Permission denied (macOS/Linux)**

```bash
# Надайте права виконання
chmod +x *.py
chmod +x *.sh
```

**3. Python version mismatch**

```bash
# Явно вкажіть версію Python
python3.11 -m venv nimda_env
```

**4. SSL certificate errors**

```bash
# Оновіть сертифікати
pip install --trusted-host pypi.org --trusted-host pypi.python.org --upgrade pip
```

### Діагностика системи

```bash
# Запуск діагностики
python -c "
import sys
print(f'Python: {{sys.version}}')
print(f'Executable: {{sys.executable}}')
print(f'Path: {{sys.path[:3]}}')

import platform
print(f'OS: {{platform.system()}} {{platform.release()}}')
print(f'Architecture: {{platform.machine()}}')
"
```

## 📞 Підтримка

### Отримання допомоги

Якщо виникли проблеми:

1. 📋 Перевірте [Issues](https://github.com/oleg121203/nimda_agent_plugin/issues)
2. 🔍 Запустіть діагностику системи
3. 📧 Створіть новий Issue з деталями помилки

### Лог файли

Корисні файли для діагностики:

- `nimda_app.log` - Основні логи
- `error_history.json` - Історія помилок
- `emergency_backup.json` - Резервні дані

---

*Згенеровано автоматично • {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    def _load_templates(self) -> Dict[str, str]:
        """Load documentation templates"""
        return {
            "function": """
### `{name}({params})`

{docstring}

**Параметри:**
{parameters}

**Повертає:** `{return_type}`

**Приклад:**
```python
{example}
```
""",
            "class": """
## {name}

{docstring}

**Наслідування:** {inheritance}

### Методи

{methods}

### Атрибути

{attributes}
""",
        }

    def _save_documentation(self, docs: Dict[str, str]):
        """Save generated documentation to files"""
        docs_dir = self.project_path / "docs"
        docs_dir.mkdir(exist_ok=True)

        for filename, content in docs.items():
            file_path = docs_dir / filename
            file_path.write_text(content, encoding="utf-8")
            print(f"   💾 Saved: {filename}")

        # Also save to root for main files
        for main_file in ["README.md"]:
            if main_file in docs:
                (self.project_path / main_file).write_text(
                    docs[main_file], encoding="utf-8"
                )


def main():
    """Demo of Auto Documentation Generator"""
    print("📚 Auto Documentation Generator Demo")
    print("=" * 50)

    generator = AutoDocumentationGenerator()

    # Generate complete documentation
    docs = generator.generate_complete_documentation()

    print("\n✅ Generated documentation:")
    for filename in docs.keys():
        print(f"   📄 {filename}")

    print("\n📊 Statistics:")
    print(f"   Python files analyzed: {len(generator.analyzed_modules)}")
    print(
        f"   Classes found: {sum(len(m['classes']) for m in generator.analyzed_modules.values())}"
    )
    print(
        f"   Functions found: {sum(len(m['functions']) for m in generator.analyzed_modules.values())}"
    )


if __name__ == "__main__":
    main()
