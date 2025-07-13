#!/usr/bin/env python3
"""
Тестування оптимізованого ініціалізатора проекту
"""

import sys
import tempfile
from pathlib import Path

# Додаємо шлях до модуля
CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))
from project_initializer_clean import ProjectInitializer


def test_generic_project():
    """Тест створення генеричного проекту"""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_path = Path(temp_dir) / "generic_test"
        test_path.mkdir()

        initializer = ProjectInitializer(test_path)
        result = initializer.initialize()

        assert result
        assert (test_path / "README.md").exists()
        assert (test_path / ".gitignore").exists()
        assert (test_path / "DEV_PLAN.md").exists()
        assert (test_path / "CHANGELOG.md").exists()
        assert (test_path / "docs").exists()
        print("✅ Генеричний проект: OK")


def test_python_project():
    """Тест створення Python проекту"""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_path = Path(temp_dir) / "python_test"
        test_path.mkdir()

        # Створюємо Python файл для визначення типу
        (test_path / "app.py").write_text("print('hello')")

        initializer = ProjectInitializer(test_path)
        result = initializer.initialize()

        assert result
        assert (test_path / "requirements.txt").exists()
        assert (test_path / "main.py").exists()
        assert (test_path / "src").exists()
        assert (test_path / "tests").exists()
        assert (test_path / "src" / "__init__.py").exists()
        assert (test_path / "tests" / "__init__.py").exists()
        print("✅ Python проект: OK")


def test_web_project():
    """Тест створення веб проекту"""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_path = Path(temp_dir) / "web_test"
        test_path.mkdir()

        # Створюємо HTML файл для визначення типу
        (test_path / "page.html").write_text("<h1>Test</h1>")

        initializer = ProjectInitializer(test_path)
        result = initializer.initialize()

        assert result
        assert (test_path / "index.html").exists()
        assert (test_path / "style.css").exists()
        assert (test_path / "script.js").exists()
        assert (test_path / "css").exists()
        assert (test_path / "js").exists()
        assert (test_path / "images").exists()
        print("✅ Веб проект: OK")


def test_javascript_project():
    """Тест створення JavaScript проекту"""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_path = Path(temp_dir) / "js_test"
        test_path.mkdir()

        # Створюємо JS файл для визначення типу
        (test_path / "app.js").write_text("console.log('hello')")

        initializer = ProjectInitializer(test_path)
        result = initializer.initialize()

        assert result
        assert (test_path / "package.json").exists()
        assert (test_path / "index.js").exists()
        print("✅ JavaScript проект: OK")


def main():
    """Запуск всіх тестів"""
    print("🧪 Тестування project_initializer_clean.py")
    print("=" * 50)

    try:
        test_generic_project()
        test_python_project()
        test_web_project()
        test_javascript_project()

        print("=" * 50)
        print("🎉 Всі тести пройдені успішно!")

    except Exception as e:
        print(f"❌ Помилка тестування: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
