# NIMDA Agent Plugin

The **NIMDA Agent Plugin** provides an automated development assistant that can be embedded into any project. It reads a `DEV_PLAN.md`, executes tasks, manages Git repositories and keeps a changelog.

## Features

- **Development plan processing** – read and execute `DEV_PLAN.md` tasks
- **Git integration** – automatic commits, pushes and pull operations
- **Autonomous mode** – run tasks without manual intervention
- **Automatic fixes** – detect and resolve issues in the project
- **Retries** – each subtask is executed several times until success
- **Changelog updates** – keep `CHANGELOG.md` in sync with progress
- **Codex integration** – remote control using Codex commands

## Quick start

```bash
# initialize a new project
python nimda_agent_plugin/run_nimda_agent.py --init

# execute the full development plan
python nimda_agent_plugin/run_nimda_agent.py --command "run dev"
```

You can also send the command **`run dev`** directly in the Codex chat to
perform the entire development plan in your mobile app.

For a completely automated cycle, use **`auto_dev_runner.py`**:

```bash
python nimda_agent_plugin/auto_dev_runner.py /path/to/project
```

The script initializes the project (if required), runs the full development cycle and executes tests when they are available.

## Repository structure

```
nimda_agent_plugin/
├── agent.py               # Core agent class
├── command_processor.py   # Command parsing and handling
├── dev_plan_manager.py    # Development plan management
├── git_manager.py         # Git operations wrapper
├── auto_dev_runner.py     # Automated runner script
└── ...
```

## License

MIT License.
