#!/usr/bin/env python3
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
    env_vars = {}
    
    # Обов'язкові змінні
    print("\n📋 Обов'язкові налаштування:")
    
    git_name = input("Git ім'я користувача (GIT_USER_NAME): ").strip()
    if git_name:
        env_vars["GIT_USER_NAME"] = git_name
    
    git_email = input("Git email (GIT_USER_EMAIL): ").strip()
    if git_email:
        env_vars["GIT_USER_EMAIL"] = git_email
    
    # GitHub налаштування
    print("\n🔗 GitHub налаштування (опціонально):")
    
    github_token = input("GitHub токен (GITHUB_TOKEN): ").strip()
    if github_token:
        env_vars["GITHUB_TOKEN"] = github_token
    
    github_username = input("GitHub username (GITHUB_USERNAME): ").strip()
    if github_username:
        env_vars["GITHUB_USERNAME"] = github_username
    
    github_repo = input("GitHub репозиторій URL (GITHUB_REPO_URL): ").strip()
    if github_repo:
        env_vars["GITHUB_REPO_URL"] = github_repo
    
    # Налаштування проекту
    print("\n⚙️ Налаштування проекту (опціонально):")
    
    project_name = input("Назва проекту (PROJECT_NAME) [NIMDA-CLI]: ").strip()
    env_vars["PROJECT_NAME"] = project_name or "NIMDA-CLI"
    
    auto_commit = input("Автоматичні коміти (AUTO_COMMIT) [true/false]: ").strip().lower()
    env_vars["AUTO_COMMIT"] = auto_commit if auto_commit in ["true", "false"] else "true"
    
    auto_push = input("Автоматичний push (AUTO_PUSH) [true/false]: ").strip().lower()
    env_vars["AUTO_PUSH"] = auto_push if auto_push in ["true", "false"] else "true"
    
    # Запис у файл
    if env_vars:
        with open(env_file, "w") as f:
            f.write("# NIMDA Agent Environment Variables\n")
            f.write("# Автоматично згенеровано\n\n")
            
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        
        print(f"\n✅ Змінні середовища збережено у {env_file}")
        print("🚀 Тепер можна запускати NIMDA Agent!")
    else:
        print("\n⚠️ Не введено жодної змінної")


def show_current_env():
    """Показати поточні змінні середовища"""
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ Файл .env не знайдено")
        return
    
    print("📋 Поточні змінні середовища:")
    print("=" * 40)
    
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                print(f"  {line}")


def main():
    """Головна функція"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Налаштування змінних середовища NIMDA Agent")
    parser.add_argument("--setup", action="store_true", help="Налаштувати змінні середовища")
    parser.add_argument("--show", action="store_true", help="Показати поточні змінні")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_environment()
    elif args.show:
        show_current_env()
    else:
        # Інтерактивний режим
        print("🤖 NIMDA Agent - Налаштування змінних середовища")
        print("1. Налаштувати змінні")
        print("2. Показати поточні змінні")
        print("0. Вихід")
        
        choice = input("\nВиберіть опцію: ").strip()
        
        if choice == "1":
            setup_environment()
        elif choice == "2":
            show_current_env()
        else:
            print("👋 До побачення!")


if __name__ == "__main__":
    main()
