#!/usr/bin/env python3
"""Automated runner to execute the full development plan in an isolated project."""

import argparse
import subprocess
import time
from pathlib import Path

from agent import NIMDAAgent

# State file used to detect incomplete development cycles
STATE_FILE = ".dev_cycle_in_progress"


def run_tests(project_path: Path) -> bool:
    """Run pytest in the specified project directory."""
    try:
        result = subprocess.run(["pytest", "-q"], cwd=project_path, check=True)
        return result.returncode == 0
    except FileNotFoundError:
        print("pytest is not installed. Skipping tests.")
        return False
    except subprocess.CalledProcessError as exc:
        print(f"Tests failed with exit code {exc.returncode}")
        return False


def run_cycle_until_complete(agent: NIMDAAgent) -> dict:
    """Run full development cycles until the plan is completed."""
    attempt = 0
    result = {}

    while True:
        attempt += 1
        print(f"\n🚀 Starting development cycle attempt {attempt}...")
        result = agent.run_full_dev_cycle()

        status = agent.dev_plan_manager.get_plan_status()
        total = status.get("total_tasks", 0)
        completed = status.get("completed_tasks", 0)

        if completed >= total:
            print("✅ Development plan completed")
            break

        print(
            f"⚠️  Plan incomplete ({completed}/{total} tasks). Retrying in 5s..."
        )
        time.sleep(5)

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run NIMDA Agent on a project folder")
    parser.add_argument(
        "project",
        nargs="?",
        default=".",
        help="Path to the project folder (default: current directory)",
    )
    args = parser.parse_args()

    project_path = Path(args.project).resolve()

    # Ensure we're in a valid project directory
    if not project_path.exists():
        project_path.mkdir(parents=True, exist_ok=True)

    agent = NIMDAAgent(str(project_path))

    if not agent.dev_plan_manager.dev_plan_file.exists():
        print("No DEV_PLAN.md found. Creating template...")
        agent.dev_plan_manager._create_template()
        return

    print(f"Initializing project in: {project_path}")
    agent.initialize_project()

    state_file = project_path / STATE_FILE
    state_file.write_text(str(time.time()))

    print("Running full development cycle...")
    result = run_cycle_until_complete(agent)
    print(result)

    if state_file.exists():
        state_file.unlink()

    if (project_path / "tests").exists():
        print("Running tests...")
        run_tests(project_path)

    agent.shutdown()


if __name__ == "__main__":
    main()
