# 🤖 CODEX MODE - Working with Current Agent

## 📋 **How it works:**

### 🎯 **Normal mode:**
```
run full dev
```
- Creates a new project in `~/Projects/NIMDA_v3.2/` (if specified in DEV_PLAN)
- Or works in the current directory

### 🔧 **CODEX MODE:**
```
codex run full dev
```
- **ALWAYS** works with the current agent
- **DOES NOT create** a new project  
- Executes DEV_PLAN in the agent's root

## 🚀 **CODEX MODE Commands:**

- `codex run full dev`
- `codex execute full dev`
- `codex run full plan`
- `codex do everything`

## 📱 **Mobile Usage:**

If you're writing from a mobile device and want to work with the current agent:

```
codex run full dev
```

The system automatically:
1. ✅ Detects CODEX MODE
2. 🏠 Stays in the current directory  
3. 🔄 Executes DEV_PLAN here
4. 💾 Makes a commit with "CODEX MODE" label

## 🔍 **Differences:**

| Command | Mode | Action |
|---------|------|--------|
| `run full dev` | Normal | Checks DEV_PLAN, may create a new project |
| `codex run full dev` | CODEX MODE | Always works in the current directory |

## 📝 **Usage Example:**

```bash
# From mobile in GPT chat:
codex run full dev

# System will respond:
✅ CODEX MODE: Plan executed in current agent: 5/5 tasks
```

**Now you can safely write from mobile!** 🎉

## ⚙️ **Setup GitHub Repository:**

To enable push operations, configure the GitHub repository:

### Option 1: Using NIMDA Agent
```bash
python run_nimda_agent.py --setup-github https://github.com/oleg121203/nimda_agent_plugin.git
```

### Option 2: Using Git directly
```bash
git remote add origin https://github.com/oleg121203/nimda_agent_plugin.git
git push --set-upstream origin main
```

### Option 3: Environment variables
```bash
export GITHUB_REPO_URL="https://github.com/oleg121203/nimda_agent_plugin.git"
export GITHUB_TOKEN="your_github_token"
```

After setup, `codex run full dev` will successfully push changes! ✅
