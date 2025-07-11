#!/usr/bin/env python3
"""
Головний файл запуску NIMDA Agent Plugin
Універсальний автономний агент розробки
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any

# Додавання шляху до плагіна
plugin_dir = Path(__file__).parent
sys.path.insert(0, str(plugin_dir))

from agent import NIMDAAgent


def main():
    """Головна функція запуску NIMDA Agent"""

    parser = argparse.ArgumentParser(
        description="NIMDA Agent - Універсальний автономний агент розробки",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади використання:

  # Запуск у інтерактивному режимі
  python run_nimda_agent.py

  # Виконання конкретної команди
  python run_nimda_agent.py --command "статус"
  python run_nimda_agent.py --command "виконай задачу номер 1"
  python run_nimda_agent.py --command "виконай весь ДЕВ"

  # Ініціалізація нового проекту
  python run_nimda_agent.py --init

  # Запуск у демон режимі
  python run_nimda_agent.py --daemon

  # Налаштування GitHub репозиторію
  python run_nimda_agent.py --setup-github https://github.com/user/repo.git

Підтримувані команди:
- "статус" - поточний статус агента
- "допрацюй девплан" - оновлення плану розробки
- "виконай задачу номер X" - виконання конкретної задачі
- "виконай весь ДЕВ" - виконання всього плану
- "синхронізація" - синхронізація з Git
- "виправити помилки" - автоматичне виправлення
- "ініціалізація" - створення структури проекту
- "допомога" - список команд
        """
    )

    parser.add_argument(
        "--project-path",
        type=str,
        default=".",
        help="Шлях до проекту (за замовчуванням: поточна директорія)"
    )

    parser.add_argument(
        "--command",
        type=str,
        help="Команда для виконання"
    )

    parser.add_argument(
        "--init",
        action="store_true",
        help="Ініціалізація нового проекту"
    )

    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Запуск у режимі демона (очікування команд)"
    )

    parser.add_argument(
        "--setup-github",
        type=str,
        metavar="URL",
        help="Налаштування GitHub репозиторію"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Шлях до файлу конфігурації"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Детальний вивід"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Вивід у форматі JSON"
    )

    args = parser.parse_args()

    try:
        # Ініціалізація агента
        project_path = Path(args.project_path).resolve()

        if args.verbose:
            print(f"🤖 Ініціалізація NIMDA Agent для проекту: {project_path}")

        agent = NIMDAAgent(str(project_path))

        # Обробка аргументів
        if args.init:
            handle_init(agent, args)
        elif args.setup_github:
            handle_github_setup(agent, args.setup_github, args)
        elif args.daemon:
            handle_daemon_mode(agent, args)
        elif args.command:
            handle_command(agent, args.command, args)
        else:
            handle_interactive_mode(agent, args)

    except KeyboardInterrupt:
        print("\n🛑 Перервано користувачем")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Критична помилка: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def handle_init(agent: NIMDAAgent, args):
    """Обробка ініціалізації проекту"""
    print("🚀 Ініціалізація нового проекту...")

    success = agent.initialize_project()

    if success:
        result = {
            "success": True,
            "message": "Проект успішно ініціалізовано",
            "project_path": str(agent.project_path)
        }
    else:
        result = {
            "success": False,
            "message": "Помилка ініціалізації проекту"
        }

    output_result(result, args)


def handle_github_setup(agent: NIMDAAgent, github_url: str, args):
    """Обробка налаштування GitHub"""
    print(f"🔗 Налаштування GitHub репозиторію: {github_url}")

    result = agent.git_manager.setup_github_remote(github_url)
    output_result(result, args)


def handle_command(agent: NIMDAAgent, command: str, args):
    """Обробка одноразової команди"""
    if args.verbose:
        print(f"📝 Виконання команди: {command}")

    result = agent.process_command(command)

    # Вивід повідомлення для користувача
    if "user_message" in result:
        if not args.json:
            print(result["user_message"])

    output_result(result, args)


def handle_daemon_mode(agent: NIMDAAgent, args):
    """Обробка режиму демона"""
    print("🔄 Запуск NIMDA Agent у режимі демона...")
    print("Введіть команди або 'exit' для виходу:")

    while True:
        try:
            command = input("\nNIMDA> ").strip()

            if command.lower() in ['exit', 'quit', 'вихід']:
                break

            if not command:
                continue

            if command.lower() in ['help', 'допомога']:
                show_help()
                continue

            result = agent.process_command(command)

            # Вивід результату
            if "user_message" in result:
                print(result["user_message"])
            elif result.get("success"):
                print(f"✅ {result.get('message', 'Команду виконано')}")
            else:
                print(f"❌ {result.get('message', 'Помилка виконання команди')}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Помилка: {e}")

    print("\n👋 NIMDA Agent завершує роботу...")
    agent.shutdown()


def handle_interactive_mode(agent: NIMDAAgent, args):
    """Обробка інтерактивного режиму"""
    print("🤖 NIMDA Agent - Універсальний автономний агент розробки")
    print("=" * 60)

    # Показ статусу
    status = agent.get_status()

    if not args.json:
        print(f"📁 Проект: {status['project_path']}")
        print(f"🎯 План: {status['dev_plan']['completed_subtasks']}/{status['dev_plan']['total_subtasks']} підзадач")
        print(f"🔧 Git: {status['git']['current_branch'] if status['git'].get('current_branch') else 'не ініціалізовано'}")
        print(f"🤖 Статус: {'Працює' if status['agent_running'] else 'Простоює'}")
        print()

        # Швидкі команди
        print("Швидкі команди:")
        print("1. Показати статус")
        print("2. Оновити план розробки")
        print("3. Виконати всі задачі")
        print("4. Синхронізувати з Git")
        print("5. Інтерактивний режим")
        print("0. Вихід")
        print()

        choice = input("Виберіть опцію (0-5) або введіть команду: ").strip()

        if choice == "0":
            return
        elif choice == "1":
            result = agent.process_command("статус")
        elif choice == "2":
            result = agent.process_command("допрацюй девплан")
        elif choice == "3":
            result = agent.process_command("виконай весь ДЕВ")
        elif choice == "4":
            result = agent.process_command("синхронізація")
        elif choice == "5":
            handle_daemon_mode(agent, args)
            return
        else:
            result = agent.process_command(choice)

        # Вивід результату
        if "user_message" in result:
            print(result["user_message"])
    else:
        output_result(status, args)


def show_help():
    """Показ довідки"""
    help_text = """
🤖 NIMDA Agent - Доступні команди:

📋 Робота з планом розробки:
  • допрацюй девплан          - оновити та розширити DEV_PLAN.md
  • виконай задачу номер X    - виконати конкретну задачу
  • виконай весь ДЕВ          - виконати весь план повністю

📊 Статус та інформація:
  • статус                    - поточний статус агента та прогрес
  • допомога                  - показати цю довідку

🔧 Git та синхронізація:
  • синхронізація             - синхронізація з віддаленим репозиторієм
  • виправити помилки         - автоматичне виправлення помилок

🚀 Управління проектом:
  • ініціалізація             - створити базову структуру проекту

💡 Приклади:
  • "допрацюй девплан і додай нові задачі"
  • "виконай задачу номер 3"
  • "виконай весь ДЕВ план від початку до кінця"
  • "покажи поточний статус проекту"

🔧 Системні команди:
  • exit, quit, вихід         - завершити роботу агента
  • help, допомога            - показати цю довідку
"""
    print(help_text)


def output_result(result: Dict[str, Any], args):
    """Вивід результату"""
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result.get("success"):
            print(f"✅ {result.get('message', 'Операцію виконано успішно')}")
        else:
            print(f"❌ {result.get('message', 'Помилка виконання операції')}")

            if "error" in result and args.verbose:
                print(f"Деталі помилки: {result['error']}")


if __name__ == "__main__":
    main()
