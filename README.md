# NIMDA Agent Plugin

The **NIMDA Agent Plugin** provides an automated development assistant that can be embedded into any project. It reads a `DEV_PLAN.md`, executes tasks, manages Git repositories and keeps a changelog.

## 🚀 Features

- **Development plan processing** – read and execute `DEV_PLAN.md` tasks
- **Git integration** – automatic commits, pushes and pull operations  
- **Autonomous mode** – run tasks without manual intervention
- **Automatic fixes** – detect and resolve issues in the project
- **Retries** – each subtask is executed several times until success
- **Changelog updates** – keep `CHANGELOG.md` in sync with progress
- **Codex integration** – remote control using Codex commands
- **macOS optimized** – Native integration for Mac Studio M1 Max

## 🛠 Quick Start

```bash
# Initialize a new project
python nimda_agent_plugin/run_nimda_agent.py --init

# Execute the full development plan
python nimda_agent_plugin/run_nimda_agent.py --command "run full dev"

# Or use the shorter command
python nimda_agent_plugin/run_nimda_agent.py --command "run dev"

# Check system status
python nimda_agent_plugin/run_nimda_agent.py --command "status"
```

You can also send the command **`run dev`** directly in the Codex chat to perform the entire development plan in your mobile app.

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

## Automatic Codex Priority Merge System

### 🤖 Auto-Synchronization Features

The repository includes automated synchronization mechanisms to ensure Codex changes are properly merged and synchronized:

#### 1. Remote Auto-Merge (GitHub Actions)
- **Trigger**: Pull requests with `codex` or `bgrzdn-codex` in branch name
- **Action**: Automatic merge with Codex priority conflict resolution
- **Location**: `.github/workflows/codex-priority-merge.yml`

#### 2. Local Auto-Merge (Git Hooks)
- **Trigger**: Local merge operations involving Codex branches
- **Action**: Conflict resolution favoring Codex changes
- **Location**: `.git/hooks/pre-merge-commit`

#### 3. Auto-Sync After Remote Merge
- **Trigger**: Detection of Codex auto-merge commits on remote
- **Action**: Automatic synchronization of local repository
- **Location**: `.git/hooks/post-merge` and `sync_codex_repo.sh`

### 🔄 Manual Synchronization

To manually check and sync the repository:

```bash
./sync_codex_repo.sh
```

This script will:
- Check if local repository is behind remote
- Detect Codex auto-merge commits
- Automatically synchronize if safe
- Maintain Codex priority in all operations

### ⚡ How It Works

1. **Codex branch created** → GitHub Actions triggers
2. **Auto-merge executed** → Remote repository updated
3. **Local sync triggered** → Repository synchronized
4. **Codex priority maintained** → Throughout the process

## 🕐 Temporal Priority System

### Overview
The system now includes intelligent temporal priority logic that determines merge priority based on **timestamp comparison** of commits, ensuring that more recent changes take precedence while maintaining Codex priority for simultaneous or close-time commits.

### ⏱️ How Temporal Priority Works

1. **Time Synchronization**: Before any comparison, the system synchronizes system time using:
   - SNTP (Simple Network Time Protocol)
   - ntpdate
   - HTTP date headers as fallback

2. **Timestamp Analysis**: 
   - Compares commit timestamps between local and remote branches
   - Uses configurable threshold (default: 60 seconds)
   - Accounts for timezone differences

3. **Priority Decision**:
   - **Local Priority**: If local changes are newer by > threshold
   - **Codex Priority**: If remote/Codex changes are newer or within threshold
   - **Default**: Codex priority when timestamps are unclear

### 🔧 Configuration

Edit `.codex_temporal_config` to customize behavior:

```bash
# Time threshold for priority decision (seconds)
TEMPORAL_THRESHOLD=60

# Enable/disable temporal priority logic
TEMPORAL_PRIORITY_ENABLED=true

# Default to Codex priority when unclear
CODEX_DEFAULT_PRIORITY=true

# Automatically resolve conflicts based on priority
AUTO_RESOLVE_CONFLICTS=true
```

### 🧪 Testing Temporal Logic

```bash
# Test the complete temporal priority system
./test_temporal_priority.sh test-all

# Test only time synchronization
./test_temporal_priority.sh test-time

# Test temporal comparison logic
./test_temporal_priority.sh test-compare
```

### 📋 Merge Strategies

#### Local Priority (Newer Local Changes)
- Uses `git merge -X ours` strategy
- Conflicts resolved in favor of local changes
- Logs indicate "LOCAL PRIORITY" decision

#### Codex Priority (Newer Remote/Within Threshold)
- Uses `git merge -X theirs` or `git rebase` strategy  
- Conflicts resolved in favor of Codex changes
- Logs indicate "CODEX PRIORITY" decision

### 🛡️ Safety Features

- **Time sync verification** before decisions
- **Backup creation** before complex merges
- **Recovery mechanisms** for failed operations
- **Comprehensive logging** of all decisions
- **Manual review triggers** for complex conflicts

## License

MIT License.
