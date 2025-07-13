#!/usr/bin/env python3
"""Main entry file for the NIMDA Agent Plugin.
Provides a universal autonomous development agent."""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any

# Add plugin path to PYTHONPATH
plugin_dir = Path(__file__).parent
sys.path.insert(0, str(plugin_dir))

from agent import NIMDAAgent


def main():
    """Main function for running NIMDA Agent"""

    parser = argparse.ArgumentParser(
        description="NIMDA Agent - Universal autonomous development agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:

  # Start in interactive mode
  python run_nimda_agent.py

  # Execute a specific command
  python run_nimda_agent.py --command "status"
  python run_nimda_agent.py --command "execute task number 1"
  python run_nimda_agent.py --command "run full dev"

  # Initialize a new project
  python run_nimda_agent.py --init

  # Run as a daemon
  python run_nimda_agent.py --daemon

  # Configure GitHub repository
  python run_nimda_agent.py --setup-github https://github.com/user/repo.git

Supported commands:
- "status" - show current agent status
- "update devplan" - update the development plan
- "execute task number X" - run a specific task
- "run full dev" - execute the entire plan
- "sync" - synchronize with Git
- "fix errors" - automatically fix issues
- "initialize" - create project structure
- "help" - list available commands
        """
    )

    parser.add_argument(
        "--project-path",
        type=str,
        default=".",
        help="Path to the project (default: current directory)"
    )

    parser.add_argument(
        "--command",
        type=str,
        help="Command to execute"
    )

    parser.add_argument(
        "--init",
        action="store_true",
        help="Initialize a new project"
    )

    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run in daemon mode (waiting for commands)"
    )

    parser.add_argument(
        "--setup-github",
        type=str,
        metavar="URL",
        help="Configure GitHub repository"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )

    args = parser.parse_args()

    try:
        # Initialize the agent
        project_path = Path(args.project_path).resolve()

        if args.verbose:
            print(f"🤖 Initializing NIMDA Agent for project: {project_path}")

        agent = NIMDAAgent(str(project_path))

        # Argument handling
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
        print("\n🛑 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Critical error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def handle_init(agent: NIMDAAgent, args):
    """Handle project initialization"""
    print("🚀 Initializing new project...")

    success = agent.initialize_project()

    if success:
        result = {
            "success": True,
            "message": "Project initialized successfully",
            "project_path": str(agent.project_path)
        }
    else:
        result = {
            "success": False,
            "message": "Project initialization failed"
        }

    output_result(result, args)


def handle_github_setup(agent: NIMDAAgent, github_url: str, args):
    """Handle GitHub configuration"""
    print(f"🔗 Configuring GitHub repository: {github_url}")

    result = agent.git_manager.setup_github_remote(github_url)
    output_result(result, args)


def handle_command(agent: NIMDAAgent, command: str, args):
    """Handle a single command"""
    if args.verbose:
        print(f"📝 Executing command: {command}")

    result = agent.process_command(command)

    # Display message for the user
    if "user_message" in result:
        if not args.json:
            print(result["user_message"])

    output_result(result, args)


def handle_daemon_mode(agent: NIMDAAgent, args):
    """Handle daemon mode"""
    print("🔄 Starting NIMDA Agent in daemon mode...")
    print("Enter commands or 'exit' to quit:")

    while True:
        try:
            command = input("\nNIMDA> ").strip()

            if command.lower() in ['exit', 'quit']:
                break

            if not command:
                continue

            if command.lower() in ['help']:
                show_help()
                continue

            result = agent.process_command(command)

            # Output the result
            if "user_message" in result:
                print(result["user_message"])
            elif result.get("success"):
                print(f"✅ {result.get('message', 'Command executed')}")
            else:
                print(f"❌ {result.get('message', 'Помилка виконання команди')}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Помилка: {e}")

    print("\n👋 NIMDA Agent завершує роботу...")
    agent.shutdown()


def handle_interactive_mode(agent: NIMDAAgent, args):
    """Handle interactive mode"""
    print("🤖 NIMDA Agent - Універсальний автономний агент розробки")
    print("=" * 60)

    # Show status
    status = agent.get_status()

    if not args.json:
        print(f"📁 Project: {status['project_path']}")
        print(f"🎯 Plan: {status['dev_plan']['completed_subtasks']}/{status['dev_plan']['total_subtasks']} subtasks")
        print(f"🔧 Git: {status['git']['current_branch'] if status['git'].get('current_branch') else 'not initialized'}")
        print(f"🤖 Status: {'Running' if status['agent_running'] else 'Idle'}")
        print()

        # Quick commands
        print("Quick commands:")
        print("1. Show status")
        print("2. Update development plan")
        print("3. Run all tasks")
        print("4. Sync with Git")
        print("5. Interactive mode")
        print("0. Exit")
        print()

        choice = input("Choose an option (0-5) or enter a command: ").strip()

        if choice == "0":
            return
        elif choice == "1":
            result = agent.process_command("status")
        elif choice == "2":
            result = agent.process_command("update devplan")
        elif choice == "3":
            result = agent.process_command("run full dev")
        elif choice == "4":
            result = agent.process_command("sync")
        elif choice == "5":
            handle_daemon_mode(agent, args)
            return
        else:
            result = agent.process_command(choice)

        # Output the result
        if "user_message" in result:
            print(result["user_message"])
    else:
        output_result(status, args)


def show_help():
    """Display help message"""
    help_text = """
🤖 NIMDA Agent - Available commands:

📋 Development plan:
  • update devplan          - update and expand DEV_PLAN.md
  • execute task number X   - run a specific task
  • run full dev            - execute the entire plan

📊 Status and info:
  • status                  - show current progress
  • help                    - display this message

🔧 Git and sync:
  • sync                    - synchronize with the remote repository
  • fix errors              - automatically fix problems

🚀 Project management:
  • initialize              - create basic project structure

💡 Examples:
  • "update devplan and add new tasks"
  • "execute task number 3"
  • "run full dev plan from start to finish"
  • "show current project status"

🔧 System commands:
  • exit, quit              - stop the agent
  • help                    - show this message
"""
    print(help_text)


def output_result(result: Dict[str, Any], args):
    """Output the result"""
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result.get("success"):
            print(f"✅ {result.get('message', 'Operation completed successfully')}")
        else:
            print(f"❌ {result.get('message', 'Operation failed')}")

            if "error" in result and args.verbose:
                print(f"Деталі помилки: {result['error']}")


if __name__ == "__main__":
    main()
