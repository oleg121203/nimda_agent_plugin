# Git Merge Strategy for Codex Branches

## Overview
This repository is configured to prioritize changes from Codex branches over the main branch when merge conflicts occur.

## Automatic Configuration
The following files have been configured for Codex priority:

### `.gitattributes`
- Documentation files (*.md): Uses union merge strategy
- Code files (*.py, *.js, *.ts): Uses recursive strategy with "theirs" preference
- Configuration files: Uses union merge strategy

### Git Hooks
- `pre-merge-commit`: Automatically resolves conflicts in favor of Codex branches

## Manual Merge with Codex Priority
If you need to manually merge a Codex branch with conflicts:

```bash
# Merge with Codex branch priority
git merge <codex-branch-name>

# If conflicts occur, prioritize Codex changes
git checkout --theirs .
git add .
git commit

# Or use the provided script
./merge_codex_priority.sh <codex-branch-name>
```

## Branch Naming Convention
For automatic Codex priority detection, use branch names containing:
- `codex`
- `bgrzdn-codex`

## Examples
```bash
# These branches will get automatic priority:
git checkout -b codex/new-feature
git checkout -b bgrzdn-codex/translate-code
git checkout -b feature-codex-integration

# Regular merge (no special priority):
git checkout -b feature/new-functionality
```

## Troubleshooting
If the automatic merge strategy doesn't work:

1. Check Git configuration:
   ```bash
   git config --list | grep merge
   ```

2. Manually resolve with Codex priority:
   ```bash
   git checkout --theirs conflicted-file.md
   git add conflicted-file.md
   ```

3. Verify hooks are executable:
   ```bash
   ls -la .git/hooks/pre-merge-commit
   ```
