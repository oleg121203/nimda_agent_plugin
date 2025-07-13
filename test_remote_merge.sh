#!/bin/bash
# Test remote merge strategy for Codex branches
# Usage: ./test_remote_merge.sh <codex-branch-name>

CODEX_BRANCH="$1"
BASE_BRANCH="main"

if [ -z "$CODEX_BRANCH" ]; then
    echo "❌ Error: Please provide Codex branch name"
    echo "Usage: $0 <codex-branch-name>"
    exit 1
fi

# Check if branch name contains codex
if [[ "$CODEX_BRANCH" != *"codex"* ]]; then
    echo "⚠️  Warning: Branch name '$CODEX_BRANCH' doesn't contain 'codex'"
    echo "Are you sure this is a Codex branch? (y/N)"
    read -r confirmation
    if [[ ! "$confirmation" =~ ^[Yy]$ ]]; then
        echo "❌ Aborted"
        exit 1
    fi
fi

echo "🤖 Testing remote merge strategy for Codex branch: $CODEX_BRANCH"
echo "📋 Base branch: $BASE_BRANCH"

# Simulate remote repository state
echo ""
echo "🔄 Fetching latest changes..."
git fetch --all

# Check if branches exist
if ! git show-ref --verify --quiet "refs/remotes/origin/$BASE_BRANCH"; then
    echo "❌ Error: Base branch 'origin/$BASE_BRANCH' not found"
    exit 1
fi

if ! git show-ref --verify --quiet "refs/remotes/origin/$CODEX_BRANCH"; then
    echo "❌ Error: Codex branch 'origin/$CODEX_BRANCH' not found"
    exit 1
fi

# Create temporary branch for testing
TEST_BRANCH="test-merge-$BASE_BRANCH-$(date +%s)"
echo "🧪 Creating test branch: $TEST_BRANCH"
git checkout -b "$TEST_BRANCH" "origin/$BASE_BRANCH"

# Configure merge strategy
echo "⚙️  Configuring Codex priority merge strategy..."
git config merge.ours.driver true

# Attempt merge
echo "🔀 Attempting merge with Codex priority..."
if git merge "origin/$CODEX_BRANCH" --no-ff; then
    echo "✅ Clean merge successful!"
    MERGE_TYPE="clean"
else
    echo "⚡ Merge conflicts detected. Applying Codex priority resolution..."
    
    # Count conflicts
    CONFLICTS=$(git status --porcelain | grep -c "^UU\|^DU\|^UD\|^AU\|^UA")
    echo "📊 Found $CONFLICTS conflict(s)"
    
    # Resolve conflicts with Codex priority
    git status --porcelain | grep "^UU" | while read -r line; do
        file=$(echo "$line" | cut -c4-)
        echo "  🔧 Resolving conflict in $file with Codex priority"
        git checkout --theirs "$file"
        git add "$file"
    done
    
    # Handle add/delete conflicts
    git status --porcelain | grep "^DU\|^UD\|^AU\|^UA" | while read -r line; do
        file=$(echo "$line" | cut -c4-)
        echo "  🔧 Resolving add/delete conflict in $file with Codex priority"
        git checkout --theirs "$file" 2>/dev/null || git rm "$file" 2>/dev/null || true
        git add "$file" 2>/dev/null || true
    done
    
    # Complete the merge
    git commit -m "Test merge: Codex branch '$CODEX_BRANCH' with priority resolution

🤖 Simulated remote merge with Codex priority
📋 Branch: $CODEX_BRANCH -> $BASE_BRANCH
🎯 Strategy: Codex changes take precedence
✅ All conflicts resolved in favor of Codex implementation"
    
    MERGE_TYPE="with-conflicts"
fi

# Show merge result
echo ""
echo "📊 Merge Summary:"
echo "├── Codex branch: $CODEX_BRANCH"
echo "├── Base branch: $BASE_BRANCH"
echo "├── Merge type: $MERGE_TYPE"
echo "└── Test branch: $TEST_BRANCH"

# Show what would be pushed
echo ""
echo "📤 Changes that would be pushed to remote:"
git log --oneline "origin/$BASE_BRANCH..$TEST_BRANCH"

echo ""
echo "🔍 Files changed:"
git diff --name-status "origin/$BASE_BRANCH" "$TEST_BRANCH"

echo ""
echo "✅ Test completed successfully!"
echo "🧹 To clean up test branch: git branch -D $TEST_BRANCH"
echo "🚀 To apply this merge to actual $BASE_BRANCH:"
echo "   git checkout $BASE_BRANCH"
echo "   git merge $TEST_BRANCH"
echo "   git push origin $BASE_BRANCH"
