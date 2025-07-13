#!/usr/bin/env python3
"""Automated runner to execute the full development plan in an isolated project."""
import argparse
import subprocess
from pathlib import Path

from agent import NIMDAAgent


def run_tests(project_path: Path) -> bool:
    """Run pytest in the specified project directory."""
    try:
        result = subprocess.run([
            "pytest",
            "-q"
        ], cwd=project_path, check=True)
        return result.returncode == 0
    except FileNotFoundError:
        print("pytest is not installed. Skipping tests.")
        return False
    except subprocess.CalledProcessError as exc:
        print(f"Tests failed with exit code {exc.returncode}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Run NIMDA Agent on a dedicated project folder")
    parser.add_argument("project", help="Path to the project folder")
    args = parser.parse_args()

    project_path = Path(args.project).resolve()
    project_path.mkdir(parents=True, exist_ok=True)

    agent = NIMDAAgent(str(project_path))

    if not agent.dev_plan_manager.dev_plan_file.exists():
        agent.dev_plan_manager._create_template()

    print("Initializing project...")
    agent.initialize_project()

    print("Running full development cycle...")
    result = agent.run_full_dev_cycle()
    print(result)

    if (project_path / "tests").exists():
        print("Running tests...")
        run_tests(project_path)

    agent.shutdown()


if __name__ == "__main__":
    main()
