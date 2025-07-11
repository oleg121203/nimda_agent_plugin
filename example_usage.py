#!/usr/bin/env python3
"""
Приклад використання ProjectInitializer
"""

import logging
import sys
from pathlib import Path

# Додаємо шлях до модуля
sys.path.insert(0, "/Users/dev/Documents/NIMDA/NIMDA-CLI/nimda_agent_plugin")
from project_initializer_clean import ProjectInitializer


def example_python_project():
    """Приклад створення Python проекту"""
    print("📦 Створення Python проекту...")

    # Створюємо тестову директорію
    project_path = Path("/tmp/example_python_project")
    project_path.mkdir(exist_ok=True)

    # Створюємо Python файл для визначення типу
    (project_path / "app.py").write_text("""#!/usr/bin/env python3
# Головний модуль додатку

def main():
    print("Привіт з Python проекту!")

if __name__ == "__main__":
    main()
""")

    # Ініціалізуємо проект
    initializer = ProjectInitializer(project_path)
    success = initializer.initialize()

    if success:
        print(f"✅ Python проект створено в: {project_path}")
        print("📋 Створені файли:")
        for file in sorted(project_path.rglob("*")):
            if file.is_file():
                print(f"   - {file.relative_to(project_path)}")
    else:
        print("❌ Помилка створення проекту")


def example_web_project():
    """Приклад створення веб проекту"""
    print("\n🌐 Створення веб проекту...")

    # Створюємо тестову директорію
    project_path = Path("/tmp/example_web_project")
    project_path.mkdir(exist_ok=True)

    # Створюємо HTML файл для визначення типу
    (project_path / "page.html").write_text("""<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Мій сайт</title>
</head>
<body>
    <h1>Ласкаво просимо!</h1>
</body>
</html>
""")

    # Ініціалізуємо проект
    initializer = ProjectInitializer(project_path)
    success = initializer.initialize()

    if success:
        print(f"✅ Веб проект створено в: {project_path}")
        print("📋 Створені файли:")
        for file in sorted(project_path.rglob("*")):
            if file.is_file():
                print(f"   - {file.relative_to(project_path)}")
    else:
        print("❌ Помилка створення проекту")


def example_javascript_project():
    """Приклад створення JavaScript проекту"""
    print("\n⚡ Створення JavaScript проекту...")

    # Створюємо тестову директорію
    project_path = Path("/tmp/example_js_project")
    project_path.mkdir(exist_ok=True)

    # Створюємо JS файл для визначення типу
    (project_path / "utils.js").write_text("""// Утилітарні функції

function greet(name) {
    console.log(`Привіт, ${name}!`);
}

module.exports = { greet };
""")

    # Ініціалізуємо проект
    initializer = ProjectInitializer(project_path)
    success = initializer.initialize()

    if success:
        print(f"✅ JavaScript проект створено в: {project_path}")
        print("📋 Створені файли:")
        for file in sorted(project_path.rglob("*")):
            if file.is_file():
                print(f"   - {file.relative_to(project_path)}")
    else:
        print("❌ Помилка створення проекту")


def show_project_content(project_path: Path, filename: str):
    """Показує вміст конкретного файлу"""
    file_path = project_path / filename
    if file_path.exists():
        print(f"\n📄 Вміст {filename}:")
        print("=" * 40)
        print(
            file_path.read_text()[:300] + "..."
            if len(file_path.read_text()) > 300
            else file_path.read_text()
        )
        print("=" * 40)


def main():
    """Головна функція з прикладами"""
    print("🚀 Демонстрація ProjectInitializer")
    print("=" * 50)

    # Налаштування логування
    logging.basicConfig(level=logging.INFO)

    try:
        # Приклади різних типів проектів
        example_python_project()
        example_web_project()
        example_javascript_project()

        # Показуємо вміст деяких файлів
        print("\n📖 Приклади створеного контенту:")

        # Python проект
        python_path = Path("/tmp/example_python_project")
        if python_path.exists():
            show_project_content(python_path, "README.md")
            show_project_content(python_path, "requirements.txt")

        print("\n🎉 Демонстрація завершена!")
        print("\n💡 Підказки:")
        print("   - Запустіть ./setup.sh в будь-якому створеному проекті")
        print("   - Перегляньте DEV_PLAN.md для планування розробки")
        print("   - Використовуйте GitHub Actions для CI/CD")

    except Exception as e:
        print(f"❌ Помилка: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
