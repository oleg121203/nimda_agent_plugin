#!/usr/bin/env python3
"""Resume NIMDA development cycle if tasks remain unfinished."""

from pathlib import Path

from agent import NIMDAAgent
from auto_dev_runner import run_cycle_until_complete, STATE_FILE


def main() -> None:
    project_path = Path(".").resolve()
    agent = NIMDAAgent(str(project_path))

    status = agent.dev_plan_manager.get_plan_status()
    if status["completed_tasks"] >= status["total_tasks"]:
        print("Development plan already completed.")
        return

    print(
        f"Resuming development cycle: {status['completed_tasks']}/{status['total_tasks']} tasks completed"
    )

    state_file = project_path / STATE_FILE
    state_file.write_text("resume")

    run_cycle_until_complete(agent)

    if state_file.exists():
        state_file.unlink()

    agent.shutdown()


if __name__ == "__main__":
    main()
