#!/usr/bin/env python3
"""
Утиліта для configuration змінних середовища NIMDA Agent
"""

import os
from pathlib import Path


def setup_environment():
    """Інтерактивне configuration змінних середовища"""
    
    print("🔧 configuration змінних середовища NIMDA Agent")
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
    print("\n📋 Обов'язкові configuration:")
    
    git_name = input(f"Git ім'я користувача (GIT_USER_NAME) [{current_env.get('GIT_USER_NAME', 'NIMDA Agent')}]: ").strip()
    env_vars["GIT_USER_NAME"] = git_name or current_env.get('GIT_USER_NAME', 'NIMDA Agent')
    
    git_email = input(f"Git email (GIT_USER_EMAIL) [{current_env.get('GIT_USER_EMAIL', 'nimda@agent.local')}]: ").strip()
    env_vars["GIT_USER_EMAIL"] = git_email or current_env.get('GIT_USER_EMAIL', 'nimda@agent.local')
    
    # GitHub configuration
    print("\n🔗 GitHub configuration (опціонально):")
    
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
    
    github_repo = input(f"GitHub repository URL (GITHUB_REPO_URL) [{current_env.get('GITHUB_REPO_URL', '')}]: ").strip()
    if github_repo:
        env_vars["GITHUB_REPO_URL"] = github_repo
    elif "GITHUB_REPO_URL" in current_env:
        env_vars["GITHUB_REPO_URL"] = current_env["GITHUB_REPO_URL"]
    
    # configuration project
    print("\n⚙️ configuration project:")
    
    project_name = input(f"Назва project (PROJECT_NAME) [{current_env.get('PROJECT_NAME', 'NIMDA-CLI')}]: ").strip()
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
    
    # entry у file
    with open(env_file, "w") as f:
        f.write("# NIMDA Agent Environment Variables\n")
        f.write("# Оновлено автоматично\n\n")
        
        # Групування змінних
        groups = {
            "Git конфігурація": ["GIT_USER_NAME", "GIT_USER_EMAIL"],
            "configuration project": ["PROJECT_NAME", "PROJECT_VERSION", "AUTO_COMMIT", "AUTO_PUSH", "CREATE_BACKUPS"],
            "Логування": ["LOG_LEVEL", "ENABLE_DEBUG"],
            "Розширені configuration": ["MAX_RETRIES", "TIMEOUT_SECONDS", "GITHUB_INTEGRATION", "CODEX_INTEGRATION"],
            "GitHub configuration": ["GITHUB_TOKEN", "GITHUB_USERNAME", "GITHUB_REPO_URL"]
        }
        
        for group_name, keys in groups.items():
            f.write(f"# {group_name}\n")
            for key in keys:
                if key in env_vars and env_vars[key]:
                    f.write(f"{key}={env_vars[key]}\n")
                elif key.startswith("GITHUB_"):
                    f.write(f"# {key}=\n")
            f.write("\n")
    
    print(f"\n✅ Змінні середовища збережено у {env_file}")
    print("🚀 Тепер можна запускати NIMDA Agent!")


def show_current_env():
    """Показати поточні змінні середовища"""
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ file .env not found")
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
                print(f"\n{current_group}:")
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
        print("❌ file .env not found")
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
        print(f"⚠️ Опціональні змінні not configured: {', '.join(missing_optional)}")
        print("   Деякі функції можуть бути недоступні")
    
    return True


def main():
    """Головна функція"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="configuration змінних середовища NIMDA Agent")
    parser.add_argument("--setup", action="store_true", help="configure змінні середовища")
    parser.add_argument("--show", action="store_true", help="Показати поточні змінні")
    parser.add_argument("--validate", action="store_true", help="check змінні середовища")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_environment()
    elif args.show:
        show_current_env()
    elif args.validate:
        validate_environment()
    else:
        # Інтерактивний режим
        print("🤖 NIMDA Agent - configuration змінних середовища")
        print("1. configure змінні")
        print("2. Показати поточні змінні")
        print("3. check configuration")
        print("0. Вихід")
        
        choice = input("\nВиберіть опцію: ").strip()
        
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
