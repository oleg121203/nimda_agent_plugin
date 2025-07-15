# NIMDA Agent Plugin System - Copilot Instructions

## Architecture Overview

NIMDA (Neural Intelligent Multi-Domain Agent) is a Ukrainian-language plugin-based system for automated development plan execution. The project follows a dual-path architecture with legacy code in the root and the active v2 system in `nimda_src_v2/`.

### Core Components

- **Active System**: All development happens in `nimda_src_v2/` 
- **Entry Point**: `nimda_workflow_launcher.py` - main system launcher
- **Core Engine**: `Core/plugin_system_runner.py` - orchestrates all plugin execution
- **Plugin System**: `plugins/` directory contains all extensible functionality
- **DEV_PLAN**: Markdown file containing development tasks with checkbox syntax `- [x] **TaskName** - Description`

### Plugin Architecture

All plugins inherit from `BasePlugin` in `plugins/base_plugin.py`:

```python
class YourPlugin(BasePlugin):
    def __init__(self, name: str = "Your Plugin Name", *, workspace_path=None):
        super().__init__(name)
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()
    
    async def execute_task(self, task: Dict[str, Any]) -> PluginResult:
        # Implementation here
        return PluginResult(success=True, message="Done")
```

**Key Plugin Patterns**:
- Use keyword-only arguments for `workspace_path` in constructors
- Return `PluginResult` objects with `success`, `message`, `data`, and optional `error`
- Implement `get_supported_tasks()` to declare task types handled
- Use `self.logger` for logging (automatically configured)
- Update status via `self.update_status(PluginStatus.RUNNING)`
- Update GUI via `self.update_gui({"type": "event_name", "data": value})`

### Critical Plugin Loading

The `PluginManager` in `plugins/plugin_manager.py` auto-discovers plugins by scanning for `*_plugin.py` files. **Special case**: `DevPlanValidatorPlugin` is loaded first and requires `workspace_path` parameter - handle this in the manager's `_load_plugin_from_file` method.

### Triple Parallel Execution Pattern

The `DevPlanExecutorPlugin` uses a unique **triple parallel execution** pattern:

```python
async def _execute_triple_parallel_tasks(self, tasks: List[Dict]) -> List[Dict]:
    """For each task, runs simultaneously:
    1. Main execution (according to DEV_PLAN)
    2. Quality control 
    3. Advanced tools checking
    """
    main_task = self._execute_main_task(task)
    quality_task = self._execute_quality_control(task) 
    tools_task = self._execute_advanced_tools_check(task)
    
    results = await asyncio.gather(main_task, quality_task, tools_task, return_exceptions=True)
```

This pattern ensures every task is executed with comprehensive validation and quality assurance.

### Development Workflow

**Start the system**:
```bash
cd nimda_src_v2
python3 nimda_workflow_launcher.py
```

**Python 3.11+ Required**: The codebase uses modern Python 3.11 syntax including `type | None` union syntax. Do not use `typing.Optional` or `typing.Union`.

**Task Execution Flow**:
1. `NIMDAPluginSystemRunner` initializes the system
2. `PluginManager` loads and manages all plugins  
3. `DevPlanValidatorPlugin` runs first to validate task checkboxes
4. DEV_PLAN tasks are parsed and distributed to appropriate plugins
5. Plugins execute in parallel with triple validation (main + quality + tools)

### DEV_PLAN Integration

DEV_PLAN.md uses specific checkbox syntax:
```markdown
- [x] **CompletedTask** - Description of completed work
- [ ] **PendingTask** - Description of pending work  
```

The system automatically:
- Parses phases using regex: `## 🎮 (Phase \d+): (.+?)\n`
- Extracts sections using: `### (\d+\.\d+) (.+?)\n`
- Finds tasks using: `-\s+\[([ x])\]\s+\*\*(.+?)\*\*\s+-\s+(.+?)`
- Validates checkboxes against actual code implementation

### Task Type Classification

Tasks are automatically classified by keywords in their names:
- **GUI tasks**: "gui", "interface", "visual", "theme" → `_execute_gui_task()`
- **AI tasks**: "ai", "neural", "machine learning", "intelligence" → `_execute_ai_task()`  
- **System tasks**: "system", "performance", "security", "monitoring" → `_execute_system_task()`
- **Default**: `_execute_generic_task()`

### Callback System

Use `setattr()` for dynamic callback assignment in `PluginManager`:

```python
setattr(self.plugin_manager, "on_plugin_loaded", self._on_plugin_loaded)
setattr(self.plugin_manager, "on_task_completed", self._on_task_completed)
```

### Testing

Run integration tests with:
```bash
python3 -m pytest tests/ -v
```

The system includes comprehensive integration tests in `test_plugin_integration.py` demonstrating plugin interaction patterns.

### Code Conventions

- **Language**: All code, comments, and strings must be in English
- **Async**: Heavy use of `async/await` throughout the system
- **Type Hints**: Use Python 3.11+ `|` syntax, not `typing.Union`
- **Error Handling**: Wrap exceptions in `PluginResult` objects
- **Logging**: Use structured logging with emoji prefixes (🎯, ✅, ❌, 🔍)
- **GUI Updates**: Always call `self.update_gui()` for UI integration

### File Organization

```
nimda_src_v2/
├── nimda_workflow_launcher.py    # Main entry point
├── Core/
│   └── plugin_system_runner.py  # Core orchestration engine
├── plugins/
│   ├── base_plugin.py           # Plugin base class with callbacks
│   ├── plugin_manager.py        # Plugin lifecycle management  
│   ├── dev_plan_executor_plugin.py      # Triple parallel execution
│   ├── dev_plan_validator_plugin.py     # Validates task checkboxes
│   └── advanced_tools_plugin.py         # AI-enhanced tools
└── DEV_PLAN.md                  # Main development plan
```

When extending the system, follow the established plugin pattern and ensure your plugin handles workspace path injection correctly.
