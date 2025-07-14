#!/usr/bin/env python3
"""
NIMDA Agent GUI - Main Application Launcher
Entry point for NIMDA Agent with GUI self-improvement capabilities
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Check for PySide6 availability
try:
    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import QApplication, QMessageBox

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("⚠️ PySide6 не встановлено. GUI недоступний.")
    print("Встановіть за допомогою: pip install PySide6")


def check_dependencies():
    """Check and install required dependencies"""
    missing_deps = []

    # Check PySide6
    if not PYSIDE6_AVAILABLE:
        missing_deps.append("PySide6")

    # Check other GUI dependencies
    try:
        import sys

        if sys.platform == "darwin":  # macOS
            try:
                import objc
            except ImportError:
                missing_deps.append("PyObjC")
    except Exception:
        pass

    if missing_deps:
        print("❌ Відсутні залежності:")
        for dep in missing_deps:
            print(f"   • {dep}")
        print("\n💡 Встановіть залежності:")
        print("   pip install PySide6")
        if "PyObjC" in missing_deps:
            print("   pip install PyObjC")
        return False

    return True


def install_dependencies():
    """Attempt to install missing dependencies"""
    import subprocess

    dependencies = ["PySide6"]
    if sys.platform == "darwin":
        dependencies.append("PyObjC")

    print("🔧 Встановлення залежностей...")

    for dep in dependencies:
        try:
            print(f"   Встановлення {dep}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", dep],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print(f"   ✅ {dep} встановлено")
            else:
                print(f"   ❌ Помилка встановлення {dep}: {result.stderr}")
                return False

        except Exception as e:
            print(f"   ❌ Помилка встановлення {dep}: {e}")
            return False

    print("✅ Всі залежності встановлено")
    return True


def run_gui_application():
    """Run the GUI application"""
    if not PYSIDE6_AVAILABLE:
        print("GUI недоступний через відсутність PySide6")
        return 1

    try:
        # Import GUI components
        from GUI.gui_controller import get_gui_controller
        from GUI.main_window import NIMDAMainWindow
        from GUI.theme import NIMDATheme

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("NIMDA Agent")
        app.setApplicationVersion("1.0")
        app.setOrganizationName("NIMDA Project")

        # Set up controller
        controller = get_gui_controller()

        # Create and show main window
        window = NIMDAMainWindow()
        controller.set_main_window(window)

        # Apply theme
        theme = NIMDATheme()
        theme.apply_theme(app)

        window.show()

        print("🚀 NIMDA Agent GUI запущено")
        print(
            "💡 Використовуйте кнопки самовдосконалення для автоматичного покращення системи"
        )

        return app.exec()

    except ImportError as e:
        print(f"❌ Помилка імпорту GUI компонентів: {e}")
        print("💡 Переконайтеся, що всі GUI файли створені правильно")
        return 1
    except Exception as e:
        print(f"❌ Помилка запуску GUI: {e}")
        return 1


def run_console_mode():
    """Run in console mode if GUI is not available"""
    print("🖥️ Запуск NIMDA Agent в консольному режимі")
    print("=" * 50)

    # Import core components
    try:
        from deep_system_analyzer import DeepSystemAnalyzer
        from dev_plan_manager import DevPlanManager

        project_path = Path(__file__).parent.parent

        print(f"📁 Проект: {project_path.name}")

        # Dev Plan status
        print("\n📋 Статус Dev Plan:")
        try:
            dev_manager = DevPlanManager(project_path)
            status = dev_manager.get_plan_status()
            print(f"   Прогрес: {status['progress_percentage']:.1f}%")
            print(
                f"   Завершено: {status['completed_subtasks']}/{status['total_subtasks']} підзадач"
            )
        except Exception as e:
            print(f"   ❌ Помилка: {e}")

        # Quick analysis
        print("\n🔍 Швидкий аналіз:")
        try:
            analyzer = DeepSystemAnalyzer(str(project_path))
            analysis = analyzer.analyze_full_system(pause_duration=0.1)

            structure = analysis.get("structure", {})
            print(f"   Python файлів: {len(structure.get('python_files', []))}")
            print(f"   Проблем: {len(analysis.get('issues', []))}")
            print(f"   Рекомендацій: {len(analysis.get('recommendations', []))}")

        except Exception as e:
            print(f"   ❌ Помилка аналізу: {e}")

        # Console interface
        print("\n💬 Консольний інтерфейс:")
        print("Команди:")
        print("  expand  - Розширити dev plan")
        print("  analyze - Глибокий аналіз")
        print("  status  - Статус системи")
        print("  gui     - Спробувати запустити GUI")
        print("  exit    - Вихід")

        while True:
            try:
                command = input("\nNIMDA> ").strip().lower()

                if command in ["exit", "quit", "q"]:
                    print("👋 До побачення!")
                    break

                elif command == "expand":
                    print("📋 Розширення dev plan...")
                    try:
                        dev_manager = DevPlanManager(project_path)
                        result = dev_manager.update_and_expand_plan()
                        print("✅ Dev plan розширено")
                    except Exception as e:
                        print(f"❌ Помилка: {e}")

                elif command == "analyze":
                    print("🧠 Глибокий аналіз...")
                    try:
                        analyzer = DeepSystemAnalyzer(str(project_path))
                        analyzer.analyze_full_system(pause_duration=0.5)
                        report_path = analyzer.save_report()
                        print(f"✅ Аналіз завершено. Звіт: {report_path}")
                    except Exception as e:
                        print(f"❌ Помилка: {e}")

                elif command == "status":
                    print("📊 Статус системи:")
                    python_files = list(project_path.glob("**/*.py"))
                    print(f"   Python файлів: {len(python_files)}")
                    print(f"   GUI доступний: {'✅' if PYSIDE6_AVAILABLE else '❌'}")
                    print(
                        f"   Dev Plan: {'✅' if (project_path / 'DEV_PLAN.md').exists() else '❌'}"
                    )

                elif command == "gui":
                    if PYSIDE6_AVAILABLE:
                        print("🚀 Запуск GUI...")
                        return run_gui_application()
                    else:
                        print("❌ GUI недоступний. Встановіть PySide6")

                else:
                    print("❓ Невідома команда. Введіть 'exit' для виходу")

            except KeyboardInterrupt:
                print("\n👋 До побачення!")
                break
            except Exception as e:
                print(f"❌ Помилка: {e}")

        return 0

    except Exception as e:
        print(f"❌ Помилка запуску консольного режиму: {e}")
        return 1


def main():
    """Main application entry point"""
    print("🤖 NIMDA Agent - Intelligent Development Assistant")
    print("=" * 60)

    # Parse command line arguments
    import argparse

    parser = argparse.ArgumentParser(description="NIMDA Agent with GUI")
    parser.add_argument(
        "--mode",
        choices=["gui", "console", "auto"],
        default="auto",
        help="Application mode",
    )
    parser.add_argument(
        "--install-deps", action="store_true", help="Install missing dependencies"
    )

    args = parser.parse_args()

    # Install dependencies if requested
    if args.install_deps:
        if install_dependencies():
            print("🔄 Перезапустіть програму для використання GUI")
        return 0

    # Check dependencies
    if not check_dependencies() and args.mode in ["gui", "auto"]:
        print("\n💡 Запустіть з --install-deps для автоматичного встановлення")
        if args.mode == "auto":
            print("🔄 Перехід до консольного режиму...")
            return run_console_mode()
        else:
            return 1

    # Run appropriate mode
    if args.mode == "gui" or (args.mode == "auto" and PYSIDE6_AVAILABLE):
        return run_gui_application()
    else:
        return run_console_mode()


if __name__ == "__main__":
    sys.exit(main())
