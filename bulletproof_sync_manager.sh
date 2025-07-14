#!/bin/bash
# Bulletproof Sync Manager - handles all branch synchronization with absolute priorities
# Remote/Codex ALWAYS has priority except when user manually commits recent changes

set -euo pipefail

# Configuration - bulletproof sync settings
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/.bulletproof_sync_config"
LOG_FILE="$SCRIPT_DIR/logs/bulletproof_sync.log"
FALLBACK_LOG="$SCRIPT_DIR/.fallback_operations.log"
RECOVERY_QUEUE="$SCRIPT_DIR/.recovery_queue.log"

# Default configuration
MAX_RETRIES=5
RETRY_DELAY=15
WAIT_INTERVAL=30
MAX_WAIT_TIME=900
TIME_SYNC_THRESHOLD=300  # 5 minutes for manual commits
EMERGENCY_THRESHOLD=1800  # 30 minutes emergency override
HEALTH_CHECK_INTERVAL=60

# Priority rules (ABSOLUTE):
# 1. Remote/Codex ALWAYS wins in automatic scenarios
# 2. Local wins ONLY when user manually commits AND it's very recent
# 3. Unresolved conflicts = force remote priority (nuclear option)
# 4. When remote unavailable = local mode with sync queue

# Load configuration if exists
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        source "$CONFIG_FILE"
        log_message "📋 Configuration loaded from $CONFIG_FILE"
    else
        create_default_config
    fi
}

# Create default configuration
create_default_config() {
    cat > "$CONFIG_FILE" << 'EOF'
# Bulletproof Sync Manager Configuration
# Remote/Codex priority settings (ABSOLUTE PRIORITY SYSTEM)

MAX_RETRIES=5
RETRY_DELAY=15
WAIT_INTERVAL=30
MAX_WAIT_TIME=900
TIME_SYNC_THRESHOLD=300
EMERGENCY_THRESHOLD=1800
HEALTH_CHECK_INTERVAL=60

# Remote branches in priority order (highest to lowest)
REMOTE_PRIORITY_BRANCHES=("origin/codex" "origin/work" "origin/main")

# Local branches for fallback mode
LOCAL_FALLBACK_BRANCHES=("codex" "work" "main")

# Enable bulletproof logging
VERBOSE_LOGGING=true
EMERGENCY_MODE=false
NUCLEAR_OPTION_ENABLED=true
EOF
    log_message "📋 Default configuration created at $CONFIG_FILE"
}

# Enhanced logging with timestamps
log_message() {
    local message="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$message"
    
    # Create log directory if it doesn't exist
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "$message" >> "$LOG_FILE"
}

# System health check
check_system_health() {
    local health_status="healthy"
    local issues=()
    
    # Check Git repository
    if ! git status --porcelain >/dev/null 2>&1; then
        health_status="unhealthy"
        issues+=("git_repo_locked")
    fi
    
    # Check network connectivity
    if ! ping -c 1 -W 3 github.com >/dev/null 2>&1 && 
       ! ping -c 1 -W 3 8.8.8.8 >/dev/null 2>&1; then
        health_status="unhealthy"
        issues+=("network_down")
    fi
    
    # Check remote accessibility
    if ! git ls-remote origin HEAD >/dev/null 2>&1; then
        health_status="unhealthy"
        issues+=("remote_unavailable")
    fi
    
    # Check for lock files
    if [ -f ".git/index.lock" ] || [ -f ".git/HEAD.lock" ]; then
        health_status="unhealthy"
        issues+=("git_locks")
    fi
    
    echo "$health_status:${issues[*]}"
}

# Detect commit context (automatic vs manual)
detect_commit_context() {
    local commit_ref="$1"
    local commit_msg=$(git log -1 --format="%s" "$commit_ref" 2>/dev/null)
    local commit_author=$(git log -1 --format="%an" "$commit_ref" 2>/dev/null)
    local commit_email=$(git log -1 --format="%ae" "$commit_ref" 2>/dev/null)
    
    # Automatic indicators
    if [[ "$commit_msg" == *"Auto-merge"* ]] || 
       [[ "$commit_msg" == *"Automatic"* ]] ||
       [[ "$commit_msg" == *"Bot:"* ]] ||
       [[ "$commit_author" == *"Bot"* ]] ||
       [[ "$commit_author" == *"GitHub"* ]] ||
       [[ "$commit_author" == *"Codex"* ]] ||
       [[ "$commit_email" == *"noreply"* ]] ||
       [[ "$commit_email" == *"bot"* ]]; then
        echo "automatic"
    else
        echo "manual"
    fi
}

# Determine merge priority with bulletproof logic
determine_merge_priority() {
    local local_commit="$1"
    local remote_commit="$2"
    
    log_message "🧠 BULLETPROOF PRIORITY ANALYSIS..."
    
    # Get commit details
    local local_time=$(git log -1 --format="%ct" "$local_commit" 2>/dev/null)
    local remote_time=$(git log -1 --format="%ct" "$remote_commit" 2>/dev/null)
    local local_context=$(detect_commit_context "$local_commit")
    local remote_context=$(detect_commit_context "$remote_commit")
    
    # Validate timestamps
    if [ -z "$local_time" ] || [ -z "$remote_time" ]; then
        log_message "⚠️  Missing timestamps - FORCING REMOTE/CODEX PRIORITY"
        return 1  # Force remote priority
    fi
    
    local time_diff=$((local_time - remote_time))
    
    log_message "📅 Local: $(date -r $local_time '+%Y-%m-%d %H:%M:%S') ($local_context)"
    log_message "📅 Remote: $(date -r $remote_time '+%Y-%m-%d %H:%M:%S') ($remote_context)"
    log_message "⏱️  Time difference: ${time_diff}s"
    
    # ABSOLUTE PRIORITY RULES:
    
    # RULE 1: Remote/Codex automatic ALWAYS wins
    if [[ "$remote_context" == "automatic" ]]; then
        log_message "🤖 REMOTE/CODEX AUTOMATIC - ABSOLUTE PRIORITY"
        return 1
    fi
    
    # RULE 2: Local automatic loses to remote
    if [[ "$local_context" == "automatic" ]]; then
        log_message "🤖 LOCAL AUTOMATIC - REMOTE WINS"
        return 1
    fi
    
    # RULE 3: Both manual - strict time-based with emergency override
    if [[ "$local_context" == "manual" ]] && [[ "$remote_context" == "manual" ]]; then
        # Emergency override - if too old, always prefer remote
        if [ $time_diff -gt $EMERGENCY_THRESHOLD ]; then
            log_message "🚨 EMERGENCY OVERRIDE - LOCAL TOO OLD, REMOTE PRIORITY"
            return 1
        fi
        
        # Normal case - local wins if significantly newer
        if [ $time_diff -gt $TIME_SYNC_THRESHOLD ]; then
            log_message "🏠 MANUAL LOCAL PRIORITY (recent and verified)"
            return 0
        else
            log_message "🤖 MANUAL REMOTE PRIORITY (within threshold)"
            return 1
        fi
    fi
    
    # RULE 4: Default - always remote/codex
    log_message "🤖 DEFAULT FALLBACK - REMOTE/CODEX PRIORITY"
    return 1
}

# Perform bulletproof merge with nuclear option
perform_bulletproof_merge() {
    local target_branch="$1"
    
    log_message "🚀 BULLETPROOF MERGE INITIATED - TARGET: $target_branch"
    
    # Get commits
    local local_commit=$(git rev-parse HEAD)
    local remote_commit=$(git rev-parse "$target_branch" 2>/dev/null)
    
    if [ -z "$remote_commit" ]; then
        log_message "❌ Target branch $target_branch not found"
        return 1
    fi
    
    # Create safety backup
    local backup_branch="bulletproof-backup-$(date +%s)"
    git branch "$backup_branch" HEAD
    log_message "📦 Safety backup created: $backup_branch"
    
    # Determine priority
    if determine_merge_priority "$local_commit" "$remote_commit"; then
        perform_local_priority_merge "$target_branch"
    else
        perform_remote_priority_merge "$target_branch"
    fi
}

# Local priority merge (rare case)
perform_local_priority_merge() {
    local target_branch="$1"
    
    log_message "🏠 EXECUTING LOCAL PRIORITY MERGE"
    
    if git merge "$target_branch" --no-edit -X ours >/dev/null 2>&1; then
        log_message "✅ Local priority merge successful"
        return 0
    else
        log_message "⚠️  Conflicts detected - resolving with local priority"
        if ! resolve_conflicts_local_priority "$target_branch"; then
            log_message "🚨 Local priority failed - falling back to remote priority"
            perform_remote_priority_merge "$target_branch"
        fi
    fi
}

# Remote priority merge (standard case)
perform_remote_priority_merge() {
    local target_branch="$1"
    
    log_message "🤖 EXECUTING REMOTE/CODEX PRIORITY MERGE"
    
    if git merge "$target_branch" --no-edit -X theirs >/dev/null 2>&1; then
        log_message "✅ Remote priority merge successful"
        return 0
    else
        log_message "⚠️  Conflicts detected - FORCING REMOTE PRIORITY"
        if ! resolve_conflicts_remote_priority "$target_branch"; then
            log_message "🚨 EMERGENCY: Applying nuclear option"
            apply_nuclear_option "$target_branch"
        fi
    fi
}

# Resolve conflicts with local priority
resolve_conflicts_local_priority() {
    local target_branch="$1"
    
    log_message "🔧 Resolving conflicts with LOCAL priority"
    
    # Get all conflicted files
    local conflicted_files=($(git status --porcelain | grep "^UU" | cut -c4-))
    
    if [ ${#conflicted_files[@]} -eq 0 ]; then
        log_message "ℹ️  No conflicts found"
        return 0
    fi
    
    for file in "${conflicted_files[@]}"; do
        if [ -f "$file" ]; then
            log_message "⚡ Resolving $file with LOCAL version"
            git checkout --ours "$file"
            git add "$file"
        fi
    done
    
    # Handle add/delete conflicts
    git status --porcelain | grep "^DU\|^UD" | while read -r line; do
        file=$(echo "$line" | cut -c4-)
        log_message "⚡ Resolving add/delete conflict: $file"
        git checkout --ours "$file" 2>/dev/null || git rm "$file" 2>/dev/null || true
        git add "$file" 2>/dev/null || true
    done
    
    if git commit --no-edit >/dev/null 2>&1; then
        log_message "✅ Conflicts resolved with local priority"
        return 0
    else
        log_message "❌ Failed to commit local priority resolution"
        return 1
    fi
}

# Resolve conflicts with remote priority (bulletproof)
resolve_conflicts_remote_priority() {
    local target_branch="$1"
    
    log_message "🔧 FORCING REMOTE/CODEX PRIORITY RESOLUTION"
    
    # Get all conflicted files
    local conflicted_files=($(git status --porcelain | grep "^UU" | cut -c4-))
    
    for file in "${conflicted_files[@]}"; do
        if [ -f "$file" ]; then
            log_message "⚡ FORCING $file to REMOTE/CODEX version"
            git checkout --theirs "$file"
            git add "$file"
        fi
    done
    
    # Handle all types of conflicts
    git status --porcelain | grep "^DU\|^UD\|^AU\|^UA" | while read -r line; do
        file=$(echo "$line" | cut -c4-)
        log_message "⚡ FORCING conflict resolution: $file"
        git checkout --theirs "$file" 2>/dev/null || git rm "$file" 2>/dev/null || true
        git add "$file" 2>/dev/null || true
    done
    
    if git commit --no-edit >/dev/null 2>&1; then
        log_message "✅ REMOTE/CODEX PRIORITY ENFORCED"
        return 0
    else
        log_message "❌ Failed to enforce remote priority"
        return 1
    fi
}

# Nuclear option - force remote state (emergency)
apply_nuclear_option() {
    local target_branch="$1"
    
    log_message "🚨 APPLYING NUCLEAR OPTION - FORCING REMOTE STATE"
    
    # Abort any ongoing operations
    git merge --abort >/dev/null 2>&1 || true
    git rebase --abort >/dev/null 2>&1 || true
    git reset --hard HEAD >/dev/null 2>&1 || true
    
    # Force reset to remote state
    if git reset --hard "$target_branch" >/dev/null 2>&1; then
        log_message "✅ NUCLEAR OPTION SUCCESS - Repository forced to remote state"
        
        # Log nuclear option usage
        echo "$(date '+%Y-%m-%d %H:%M:%S'): Nuclear option applied - forced to $target_branch" >> "$RECOVERY_QUEUE"
        return 0
    else
        log_message "❌ NUCLEAR OPTION FAILED - Manual intervention required"
        
        # Create emergency marker
        echo "$(date '+%Y-%m-%d %H:%M:%S'): EMERGENCY - Nuclear option failed" >> "$RECOVERY_QUEUE"
        return 1
    fi
}

# Sync with all remote branches
sync_all_branches() {
    log_message "🔄 Syncing all remote branches..."
    
    # Fetch all remotes
    if ! git fetch --all --prune >/dev/null 2>&1; then
        log_message "⚠️  Failed to fetch all remotes"
        return 1
    fi
    
    # Check each priority branch
    for branch in "${REMOTE_PRIORITY_BRANCHES[@]}"; do
        if git rev-parse "$branch" >/dev/null 2>&1; then
            local unmerged=$(git rev-list --count HEAD.."$branch" 2>/dev/null || echo "0")
            if [ "$unmerged" -gt 0 ]; then
                log_message "📥 $branch has $unmerged unmerged commits"
                
                if ! perform_bulletproof_merge "$branch"; then
                    log_message "⚠️  Failed to merge $branch"
                fi
            else
                log_message "✅ $branch is up to date"
            fi
        fi
    done
}

# Fallback mode when remote is unavailable
enter_fallback_mode() {
    log_message "🔄 ENTERING FALLBACK MODE - Remote unavailable"
    
    # Create fallback marker
    echo "$(date '+%Y-%m-%d %H:%M:%S'): Entered fallback mode" >> "$FALLBACK_LOG"
    
    # Work with local branches
    for branch in "${LOCAL_FALLBACK_BRANCHES[@]}"; do
        if git rev-parse "$branch" >/dev/null 2>&1; then
            local unmerged=$(git rev-list --count HEAD.."$branch" 2>/dev/null || echo "0")
            if [ "$unmerged" -gt 0 ]; then
                log_message "🔄 Merging local branch: $branch"
                
                if git merge "$branch" --no-edit >/dev/null 2>&1; then
                    log_message "✅ Merged local branch: $branch"
                else
                    log_message "⚠️  Conflicts in local branch: $branch"
                    resolve_conflicts_local_priority "$branch"
                fi
            fi
        fi
    done
    
    # Queue for remote sync when available
    echo "$(date '+%Y-%m-%d %H:%M:%S'): Fallback operations completed, needs remote sync" >> "$RECOVERY_QUEUE"
    log_message "📝 Fallback mode completed, queued for remote sync"
}

# Main bulletproof sync function
bulletproof_sync() {
    log_message "🚀 BULLETPROOF SYNC INITIATED"
    
    # Health check
    local health_result=$(check_system_health)
    local health_status=$(echo "$health_result" | cut -d: -f1)
    local health_issues=$(echo "$health_result" | cut -d: -f2)
    
    log_message "📊 System health: $health_status"
    if [ -n "$health_issues" ]; then
        log_message "⚠️  Issues detected: $health_issues"
    fi
    
    # If unhealthy, try to recover or enter fallback
    if [ "$health_status" = "unhealthy" ]; then
        if [[ "$health_issues" == *"remote_unavailable"* ]] || [[ "$health_issues" == *"network_down"* ]]; then
            log_message "🔄 Remote/Network issues detected - entering fallback mode"
            enter_fallback_mode
            return 0
        elif [[ "$health_issues" == *"git_locks"* ]]; then
            log_message "🔄 Git locks detected - waiting for release"
            sleep $RETRY_DELAY
            # Retry after lock release
            bulletproof_sync
            return $?
        else
            log_message "❌ System unhealthy and cannot proceed"
            return 1
        fi
    fi
    
    # Proceed with sync
    if sync_all_branches; then
        log_message "✅ BULLETPROOF SYNC COMPLETED SUCCESSFULLY"
        
        # Clear any fallback markers if successful
        [ -f "$FALLBACK_LOG" ] && rm -f "$FALLBACK_LOG"
        return 0
    else
        log_message "⚠️  Bulletproof sync encountered issues"
        return 1
    fi
}

# Main execution
main() {
    # Setup
    load_config
    
    # Execute based on arguments
    case "${1:-sync}" in
        "sync")
            bulletproof_sync
            ;;
        "health")
            health_result=$(check_system_health)
            echo "System Health: $(echo "$health_result" | cut -d: -f1)"
            echo "Issues: $(echo "$health_result" | cut -d: -f2)"
            ;;
        "status")
            log_message "📊 Bulletproof Sync Manager Status"
            [ -f "$FALLBACK_LOG" ] && log_message "⚠️  Fallback mode active"
            [ -f "$RECOVERY_QUEUE" ] && log_message "🔄 Recovery operations queued"
            ;;
        "force-remote")
            log_message "🚨 FORCING REMOTE PRIORITY ON ALL BRANCHES"
            for branch in "${REMOTE_PRIORITY_BRANCHES[@]}"; do
                if git rev-parse "$branch" >/dev/null 2>&1; then
                    apply_nuclear_option "$branch"
                fi
            done
            ;;
        "help")
            echo "Bulletproof Sync Manager - Remote/Codex Priority System"
            echo ""
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  sync         - Perform bulletproof sync (default)"
            echo "  health       - Check system health"
            echo "  status       - Show current status"
            echo "  force-remote - Force remote priority on all branches"
            echo "  help         - Show this help"
            ;;
        *)
            echo "Unknown command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Execute main function with all arguments
main "$@"
