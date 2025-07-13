# Git Merge Strategy for Codex Branches

## Overview
This repository is configured to prioritize changes from Codex branches over the main branch when merge conflicts occur, both locally and on remote repositories.

## Local Configuration

### `.gitattributes`
- Documentation files (*.md): Uses union merge strategy
- Code files (*.py, *.js, *.ts): Uses recursive strategy with "theirs" preference
- Configuration files: Uses union merge strategy

### Git Hooks
- `pre-merge-commit`: Automatically resolves conflicts in favor of Codex branches

## Remote Repository Configuration

### GitHub Actions
- **Workflow**: `.github/workflows/codex-auto-merge.yml`
- **Trigger**: Pull requests from branches containing "codex"
- **Action**: Automatically merges with Codex priority and closes PR

### Platform-specific Setup
See `REMOTE_MERGE_SETUP.md` for detailed configuration instructions for:
- GitHub
- GitLab  
- Bitbucket
- Self-hosted Git servers

## Branch Naming Convention
For automatic Codex priority detection, use branch names containing:
- `codex`
- `bgrzdn-codex`

Examples:
```bash
git checkout -b codex/new-feature
git checkout -b bgrzdn-codex/translate-code
git checkout -b feature-codex-integration
```

## Usage

### Local Merge
```bash
# Automatic priority (if branch name contains codex)
git merge codex-branch-name

# Manual priority using script
./merge_codex_priority.sh codex-branch-name
```

### Remote Merge (GitHub)
1. Create PR from Codex branch to main
2. PR is automatically labeled with `codex-priority` and `auto-merge`
3. GitHub Action resolves conflicts with Codex priority
4. PR is automatically merged and closed

### Testing Remote Merge
```bash
# Test the merge strategy before pushing
./test_remote_merge.sh your-codex-branch-name
```

## What Happens During Codex Priority Merge

1. **Conflict Detection**: Git identifies conflicting files
2. **Automatic Resolution**: All conflicts resolved using Codex version (`--theirs`)
3. **File Conflicts**: Added/deleted file conflicts favor Codex implementation
4. **Commit Message**: Automatically generated with Codex priority indicator
5. **Notification**: Comments added to PR explaining the resolution

## Troubleshooting

### Local Issues
```bash
# Check Git configuration
git config --list | grep merge

# Verify hooks are executable
ls -la .git/hooks/pre-merge-commit

# Manual resolution with Codex priority
git checkout --theirs conflicted-file.md
git add conflicted-file.md
```

### Remote Issues
- Check branch name contains "codex"
- Verify GitHub Actions permissions
- Ensure repository labels exist
- Review workflow logs in Actions tab

## Files Created for Codex Priority

- `.gitattributes` - Local merge strategies
- `.git/hooks/pre-merge-commit` - Local auto-resolution
- `merge_codex_priority.sh` - Manual merge script
- `test_remote_merge.sh` - Remote merge testing
- `.github/workflows/codex-auto-merge.yml` - GitHub automation
- `REMOTE_MERGE_SETUP.md` - Platform setup instructions
