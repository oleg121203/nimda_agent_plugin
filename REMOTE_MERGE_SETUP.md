# Codex Priority Remote Merge Strategy

## GitHub Settings

### 1. Branch Protection Rules
Navigate to: **Settings → Branches → Add rule**

**Main branch protection:**
```
Branch name pattern: main
☐ Require pull request reviews before merging
☑ Allow auto-merge
☐ Require status checks to pass before merging
☐ Require conversation resolution before merging
☐ Include administrators
```

### 2. Auto-merge Labels
Create these labels in **Issues → Labels → New label**:

- **codex-priority** 
  - Color: `#0052cc`
  - Description: "Codex branch with merge priority"

- **auto-merge**
  - Color: `#7fba00` 
  - Description: "Enable automatic merging"

### 3. Repository Secrets
Add in **Settings → Secrets and variables → Actions**:
- `GITHUB_TOKEN` (usually provided automatically)

## GitLab Settings

### 1. Merge Request Settings
Navigate to: **Settings → General → Merge requests**

```
☑ Enable merge when pipeline succeeds
☑ Enable auto-merge
☐ Enable fast-forward merge
☑ Enable merge commits
```

### 2. Push Rules
Navigate to: **Settings → Repository → Push Rules**

```
☑ GitLab will automatically resolve merge conflicts
Branch name pattern for auto-merge: *codex*
```

### 3. CI/CD Variables  
Add in **Settings → CI/CD → Variables**:
- `GITLAB_TOKEN` with appropriate permissions

## Bitbucket Settings

### 1. Branch Permissions
Navigate to: **Repository settings → Branch permissions**

```
Branch pattern: main
☑ Allow auto-merge for pull requests
☐ Require pull request reviews
```

### 2. Merge Strategies
Navigate to: **Repository settings → Pull requests**

```
Default merge strategy: Merge commit
☑ Allow auto-merge when all checks pass
```

## Generic Git Server Setup

For self-hosted Git servers, configure these hooks:

### Pre-receive Hook
```bash
#!/bin/bash
# In hooks/pre-receive

while read oldrev newrev refname; do
    branch=$(echo $refname | sed 's/refs\/heads\///')
    
    if [[ "$branch" == "main" ]]; then
        # Check if merge is from Codex branch
        merge_source=$(git log --format="%s" $newrev -1)
        if [[ "$merge_source" == *"codex"* ]]; then
            echo "✅ Codex priority merge detected for $branch"
        fi
    fi
done
```

### Post-receive Hook
```bash
#!/bin/bash
# In hooks/post-receive

while read oldrev newrev refname; do
    branch=$(echo $refname | sed 's/refs\/heads\///')
    
    if [[ "$branch" == "main" ]]; then
        echo "🚀 Main branch updated with potential Codex changes"
        # Add notification logic here
    fi
done
```

## Testing the Setup

Use the provided test script:
```bash
./test_remote_merge.sh your-codex-branch-name
```

This will simulate the remote merge process locally before pushing.

## Troubleshooting

### GitHub Actions not triggering
1. Check branch name contains "codex"
2. Verify workflow file syntax
3. Ensure proper permissions in repository settings

### Merge conflicts not resolved automatically  
1. Check .gitattributes configuration
2. Verify Git hooks are executable
3. Test locally with test_remote_merge.sh

### Auto-merge not working
1. Verify labels are applied to PR
2. Check branch protection rules
3. Ensure no required status checks are failing
