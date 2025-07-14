#!/usr/bin/env python3
"""
Utility for setting up NIMDA Agent environment variables
"""

import os
from pathlib import Path


def setup_environment():
    """Interactive environment variables setup"""

    print("🔧 Setting up NIMDA Agent environment variables")
    print("=" * 50)

    env_file = Path(".env")
    env_vars = {}

    # Required variables
    print("\n📋 Required settings:")

    git_name = input("Git user name (GIT_USER_NAME): ").strip()
    if git_name:
        env_vars["GIT_USER_NAME"] = git_name

    git_email = input("Git email (GIT_USER_EMAIL): ").strip()
    if git_email:
        env_vars["GIT_USER_EMAIL"] = git_email

    # GitHub settings
    print("\n🔗 GitHub settings (optional):")

    github_token = input("GitHub token (GITHUB_TOKEN): ").strip()
    if github_token:
        env_vars["GITHUB_TOKEN"] = github_token

    github_username = input("GitHub username (GITHUB_USERNAME): ").strip()
    if github_username:
        env_vars["GITHUB_USERNAME"] = github_username

    github_repo = input("GitHub repository URL (GITHUB_REPO_URL): ").strip()
    if github_repo:
        env_vars["GITHUB_REPO_URL"] = github_repo

    # Project settings
    print("\n⚙️ Project settings (optional):")

    project_name = input("Project name (PROJECT_NAME) [NIMDA-CLI]: ").strip()
    env_vars["PROJECT_NAME"] = project_name or "NIMDA-CLI"

    auto_commit = input("Auto commits (AUTO_COMMIT) [true/false]: ").strip().lower()
    env_vars["AUTO_COMMIT"] = (
        auto_commit if auto_commit in ["true", "false"] else "true"
    )

    auto_push = input("Auto push (AUTO_PUSH) [true/false]: ").strip().lower()
    env_vars["AUTO_PUSH"] = auto_push if auto_push in ["true", "false"] else "true"

    # Save to file
    if env_vars:
        with open(env_file, "w") as f:
            f.write("# NIMDA Agent Environment Variables\n")
            f.write("# Auto-generated\n\n")

            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")

        print(f"\n✅ Environment variables saved to {env_file}")
        print("🚀 Now you can run NIMDA Agent!")
    else:
        print("\n⚠️ No variables entered")


def show_current_env():
    """Show current environment variables"""

    env_file = Path(".env")

    if not env_file.exists():
        print("❌ .env file not found")
        return

    print("📋 Current environment variables:")
    print("=" * 40)

    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                print(f"  {line}")


def main():
    """Main function"""

    import argparse

    parser = argparse.ArgumentParser(
        description="Setup NIMDA Agent environment variables"
    )
    parser.add_argument(
        "--setup", action="store_true", help="Setup environment variables"
    )
    parser.add_argument("--show", action="store_true", help="Show current variables")

    args = parser.parse_args()

    if args.setup:
        setup_environment()
    elif args.show:
        show_current_env()
    else:
        # Interactive mode
        print("🤖 NIMDA Agent - Environment Variables Setup")
        print("1. Setup variables")
        print("2. Show current variables")
        print("0. Exit")

        choice = input("\nChoose option: ").strip()

        if choice == "1":
            setup_environment()
        elif choice == "2":
            show_current_env()
        else:
            print("👋 Goodbye!")


if __name__ == "__main__":
    main()
