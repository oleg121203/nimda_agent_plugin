# Branch protection rules for Codex priority
# These settings should be applied in GitHub repository settings

## Main branch protection
- Branch name pattern: `main`
- Protect matching branches: ✅
- Restrict pushes that create files: ❌
- Require status checks to pass: ✅
  - Require branches to be up to date: ❌
- Require pull request reviews: ❌ (for Codex auto-merge)
- Require conversation resolution: ❌
- Include administrators: ❌

## Auto-merge settings for Codex branches
- Enable auto-merge for PRs with labels: `codex-priority`, `auto-merge`
- Merge method: `Merge commit` (preserves Codex priority strategy)

## Required labels for auto-merge
Create these labels in your repository:
1. `codex-priority` (color: #0052cc) - Indicates Codex branch with merge priority
2. `auto-merge` (color: #7fba00) - Enables automatic merging
3. `codex-integration` (color: #ff6b35) - General Codex-related changes

## Webhook settings (optional)
For advanced integration, configure webhooks to:
- Trigger on pull request events
- Send to: your-server.com/codex-merge-webhook
- Events: Pull requests, Pushes
