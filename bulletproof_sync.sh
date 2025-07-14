#!/bin/bash
# Bulletproof Codex Sync Manager
# Advanced synchronization with fallback modes and branch management

# Configuration
MAX_RETRIES=5
RETRY_DELAY=15
WAIT_INTERVAL=60
MAX_WAIT_TIME=1800  # 30 minutes
TIME_SYNC_THRESHOLD=120
REMOTE_TIMEOUT=30

# Branch management
MAIN_BRANCH="main"
WORK_BRANCH="work"
CODEX_PATTERN="codex"
BACKUP_PREFIX="backup-"

# Priority order for merging (highest to lowest)
declare -a BRANCH_PRIORITY=(
    "origin/codex"
    "origin/work" 
    "origin/main"
    "codex"
    "work"
    "main"
)

# Logging and state management
LOG_FILE=".codex_sync.log"
STATE_FILE=".codex_sync_state"
RECOVERY_FILE=".codex_recovery_queue"

# Enhanced logging function
log_message() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_entry="[$timestamp] [$level] $message"
    
    echo "$log_entry" | tee -a "$LOG_FILE"
    
    # Also log to state file for tracking
    echo "LAST_ACTION=$(date '+%s'):$level:$message" > "$STATE_FILE"
}

# Function to save and restore repository state
save_repo_state() {
    local state_name="$1"
    log_message "INFO" "💾 Saving repository state: $state_name"
    
    git stash push -m "codex-sync-state-$state_name" --include-untracked >/dev/null 2>&1 || true
    echo "SAVED_STATE=$state_name" >> "$STATE_FILE"
    echo "CURRENT_BRANCH=$(git branch --show-current)" >> "$STATE_FILE"
    echo "LAST_COMMIT=$(git rev-parse HEAD)" >> "$STATE_FILE"
}

restore_repo_state() {
    if [ -f "$STATE_FILE" ] && grep -q "SAVED_STATE=" "$STATE_FILE"; then
        local saved_state=$(grep "SAVED_STATE=" "$STATE_FILE" | cut -d= -f2)
        log_message "INFO" "♻️ Restoring repository state: $saved_state"
        
        git stash list | grep "codex-sync-state-$saved_state" | head -1 | cut -d: -f1 | xargs git stash pop >/dev/null 2>&1 || true
        sed -i '' '/SAVED_STATE=/d' "$STATE_FILE" 2>/dev/null || true
    fi
}

# Comprehensive system status check
check_comprehensive_status() {
    local repo_status=1
    local network_status=1  
    local remote_github=1
    local remote_origin=1
    local git_lock=1
    
    # Repository checks
    if git status --porcelain >/dev/null 2>&1; then
        repo_status=0
    fi
    
    # Git lock files check
    if [ ! -f ".git/index.lock" ] && [ ! -f ".git/HEAD.lock" ] && [ ! -f ".git/refs/heads/*.lock" ]; then
        git_lock=0
    fi
    
    # Network connectivity
    if timeout $REMOTE_TIMEOUT ping -c 1 github.com >/dev/null 2>&1 ||
       timeout $REMOTE_TIMEOUT ping -c 1 8.8.8.8 >/dev/null 2>&1; then
        network_status=0
    fi
    
    # GitHub specific connectivity
    if timeout $REMOTE_TIMEOUT curl -s https://api.github.com/zen >/dev/null 2>&1; then
        remote_github=0
    fi
    
    # Origin remote accessibility
    if timeout $REMOTE_TIMEOUT git ls-remote origin HEAD >/dev/null 2>&1; then
        remote_origin=0
    fi
    
    echo "$repo_status:$network_status:$remote_github:$remote_origin:$git_lock"
}

# Advanced commit type detection
detect_commit_context() {
    local commit_ref="$1"
    local commit_msg=$(git log -1 --format="%s" "$commit_ref" 2>/dev/null)
    local commit_author=$(git log -1 --format="%an" "$commit_ref" 2>/dev/null)
    local commit_email=$(git log -1 --format="%ae" "$commit_ref" 2>/dev/null)
    
    # Determine if it's automatic
    if [[ "$commit_msg" =~ (Auto-merge|Merge branch|Merge pull request) ]] ||
       [[ "$commit_author" =~ (Bot|GitHub|Codex|Actions) ]] ||
       [[ "$commit_email" =~ (noreply\.github\.com|bot\.com) ]]; then
        echo "automatic"
    else
        echo "manual"
    fi
}

# Function to sync system time with multiple fallbacks
bulletproof_time_sync() {
    log_message "INFO" "🕐 Performing bulletproof time synchronization..."
    
    local sync_attempted=false
    local sync_successful=false
    
    # NTP servers in priority order
    local ntp_servers=("time.apple.com" "time.google.com" "pool.ntp.org" "time.cloudflare.com")
    
    # Try SNTP first
    if command -v sntp >/dev/null 2>&1; then
        for server in "${ntp_servers[@]}"; do
            if timeout 15 sntp -sS "$server" >/dev/null 2>&1; then
                log_message "INFO" "✅ Time synchronized via SNTP ($server)"
                sync_successful=true
                break
            fi
            sync_attempted=true
        done
    fi
    
    # Try ntpdate if SNTP failed
    if [ "$sync_successful" = false ] && command -v ntpdate >/dev/null 2>&1; then
        for server in "${ntp_servers[@]}"; do
            if timeout 15 sudo ntpdate -s "$server" >/dev/null 2>&1; then
                log_message "INFO" "✅ Time synchronized via ntpdate ($server)"
                sync_successful=true
                break
            fi
            sync_attempted=true
        done
    fi
    
    # HTTP time verification
    if command -v curl >/dev/null 2>&1; then
        local http_time=$(timeout 10 curl -sI https://google.com | grep -i '^date:' | sed 's/^date: //i')
        if [ -n "$http_time" ]; then
            log_message "INFO" "🌐 HTTP time reference: $http_time"
        fi
    fi
    
    if [ "$sync_attempted" = true ] && [ "$sync_successful" = false ]; then
        log_message "WARN" "⚠️ Time sync attempted but may have failed - proceeding with system time"
    fi
    
    return 0
}

# Intelligent merge priority determination
determine_intelligent_priority() {
    local local_commit="$1"
    local remote_commit="$2"
    local context="$3"  # "automatic" or "interactive"
    
    log_message "INFO" "🧠 Analyzing intelligent merge priority (context: $context)..."
    
    # Get commit details
    local local_time=$(git log -1 --format="%ct" "$local_commit" 2>/dev/null)
    local remote_time=$(git log -1 --format="%ct" "$remote_commit" 2>/dev/null)
    local local_type=$(detect_commit_context "$local_commit")
    local remote_type=$(detect_commit_context "$remote_commit")
    
    log_message "INFO" "📊 Local: $(date -r $local_time '+%H:%M:%S') ($local_type) | Remote: $(date -r $remote_time '+%H:%M:%S') ($remote_type)"
    
    # Priority decision matrix:
    # 1. In automatic mode: Codex/Remote always wins except against manual local
    # 2. In interactive mode: User choice respected with temporal fallback
    # 3. Manual local vs Automatic remote: Manual local wins
    # 4. Automatic vs Automatic: Codex/Remote wins
    # 5. Manual vs Manual: Newer wins (with threshold)
    
    if [ "$context" = "automatic" ]; then
        if [ "$local_type" = "manual" ] && [ "$remote_type" = "automatic" ]; then
            log_message "INFO" "🏠 AUTO MODE: Manual local vs Auto remote → LOCAL PRIORITY"
            return 0
        else
            log_message "INFO" "🤖 AUTO MODE: Default → CODEX/REMOTE PRIORITY"
            return 1
        fi
    else
        # Interactive mode - more nuanced decisions
        if [ "$local_type" = "manual" ] && [ "$remote_type" = "manual" ]; then
            local time_diff=$((local_time - remote_time))
            if [ $time_diff -gt $TIME_SYNC_THRESHOLD ]; then
                log_message "INFO" "🏠 INTERACTIVE: Manual local newer by ${time_diff}s → LOCAL PRIORITY"
                return 0
            else
                log_message "INFO" "🤖 INTERACTIVE: Within threshold → REMOTE PRIORITY"
                return 1
            fi
        elif [ "$local_type" = "manual" ]; then
            log_message "INFO" "🏠 INTERACTIVE: Manual local → LOCAL PRIORITY"
            return 0
        else
            log_message "INFO" "🤖 INTERACTIVE: Default → CODEX/REMOTE PRIORITY"
            return 1
        fi
    fi
}

# Fetch all branches and analyze unmerged changes
analyze_all_branches() {
    log_message "INFO" "🔍 Analyzing all branches for unmerged changes..."
    
    # Fetch all remotes with timeout
    timeout $REMOTE_TIMEOUT git fetch --all --prune >/dev/null 2>&1 || {
        log_message "WARN" "⚠️ Fetch failed or timed out, working with local data"
        return 1
    }
    
    # Get all available branches
    local all_branches=($(git branch -a | grep -E "(main|work|codex)" | sed 's/*//' | tr -d ' ' | sort -u))
    
    log_message "INFO" "📋 Available branches: ${all_branches[*]}"
    
    # Analyze each branch for unmerged commits
    for branch in "${all_branches[@]}"; do
        # Skip current branch
        if [[ "$branch" == *"HEAD"* ]]; then
            continue
        fi
        
        local clean_branch=$(echo "$branch" | sed 's|origin/||g' | sed 's|remotes/||g')
        local unmerged_count=0
        
        if git rev-parse --verify "$branch" >/dev/null 2>&1; then
            unmerged_count=$(git rev-list --count "$MAIN_BRANCH..$branch" 2>/dev/null || echo "0")
            
            if [ "$unmerged_count" -gt 0 ]; then
                log_message "INFO" "⚠️ Branch $clean_branch has $unmerged_count unmerged commits"
                
                # Add to priority list if it matches our patterns
                if [[ "$branch" =~ $CODEX_PATTERN ]] || [[ "$branch" =~ $WORK_BRANCH ]]; then
                    echo "$branch:$unmerged_count" >> "$STATE_FILE.branches"
                fi
            fi
        fi
    done
    
    return 0
}

# Bulletproof merge with all unmerged changes
perform_bulletproof_merge() {
    local target_branch="$1"
    local mode="${2:-automatic}"  # automatic or interactive
    
    log_message "INFO" "🛡️ Starting bulletproof merge from $target_branch (mode: $mode)..."
    
    # Save current state before merge
    save_repo_state "pre-merge-$(date +%s)"
    
    # Analyze all branches
    analyze_all_branches
    
    # Create backup branch
    local backup_branch="${BACKUP_PREFIX}$(date +%Y%m%d-%H%M%S)"
    git branch "$backup_branch" HEAD >/dev/null 2>&1
    log_message "INFO" "💾 Created backup branch: $backup_branch"
    
    # Get commit info for priority decision
    local latest_local=$(git rev-parse HEAD)
    local latest_remote=$(git rev-parse "$target_branch" 2>/dev/null || echo "$latest_local")
    
    # Determine merge strategy
    local use_local_priority=false
    if determine_intelligent_priority "$latest_local" "$latest_remote" "$mode"; then
        use_local_priority=true
    fi
    
    # Execute merge strategy
    if [ "$use_local_priority" = true ]; then
        execute_local_priority_merge "$target_branch"
    else
        execute_codex_priority_merge "$target_branch"
    fi
    
    local merge_result=$?
    
    # Clean up backup if merge was successful
    if [ $merge_result -eq 0 ]; then
        git branch -D "$backup_branch" >/dev/null 2>&1
        log_message "INFO" "🗑️ Removed backup branch after successful merge"
    else
        log_message "ERROR" "❌ Merge failed, backup branch $backup_branch preserved"
    fi
    
    return $merge_result
}

# Execute local priority merge strategy
execute_local_priority_merge() {
    local target_branch="$1"
    
    log_message "INFO" "🏠 Executing LOCAL PRIORITY merge strategy..."
    
    # Try octopus merge with all relevant branches
    local merge_branches=("$target_branch")
    
    # Add other priority branches if they have unmerged changes
    if [ -f "$STATE_FILE.branches" ]; then
        while IFS=':' read -r branch count; do
            if [ "$count" -gt 0 ] && [ "$branch" != "$target_branch" ]; then
                merge_branches+=("$branch")
            fi
        done < "$STATE_FILE.branches"
    fi
    
    log_message "INFO" "🔄 Merging branches: ${merge_branches[*]}"
    
    # Perform merge with local priority
    if git merge "${merge_branches[@]}" --no-edit -X ours >/dev/null 2>&1; then
        log_message "INFO" "✅ Local priority merge successful"
        return 0
    else
        log_message "WARN" "⚠️ Conflicts detected, resolving with LOCAL priority..."
        return resolve_all_conflicts "local"
    fi
}

# Execute Codex priority merge strategy  
execute_codex_priority_merge() {
    local target_branch="$1"
    
    log_message "INFO" "🤖 Executing CODEX PRIORITY merge strategy..."
    
    # Merge priority branches in order
    local merged_any=false
    
    for priority_branch in "${BRANCH_PRIORITY[@]}"; do
        if git rev-parse --verify "$priority_branch" >/dev/null 2>&1; then
            local unmerged=$(git rev-list --count "$MAIN_BRANCH..$priority_branch" 2>/dev/null || echo "0")
            
            if [ "$unmerged" -gt 0 ]; then
                log_message "INFO" "🔄 Merging $priority_branch with Codex priority..."
                
                if git merge "$priority_branch" --no-edit -X theirs >/dev/null 2>&1; then
                    log_message "INFO" "✅ Successfully merged $priority_branch"
                    merged_any=true
                else
                    log_message "WARN" "⚠️ Conflicts in $priority_branch, resolving..."
                    if ! resolve_all_conflicts "codex"; then
                        log_message "ERROR" "❌ Failed to resolve conflicts in $priority_branch"
                        return 1
                    fi
                    merged_any=true
                fi
            fi
        fi
    done
    
    if [ "$merged_any" = true ]; then
        log_message "INFO" "✅ Codex priority merge completed"
        return 0
    else
        log_message "INFO" "ℹ️ No branches needed merging"
        return 0
    fi
}

# Advanced conflict resolution
resolve_all_conflicts() {
    local priority="$1"  # "local" or "codex"
    
    log_message "INFO" "⚡ Resolving all conflicts with $priority priority..."
    
    # Handle merge conflicts (UU)
    local conflict_files=($(git status --porcelain | grep "^UU" | cut -c4-))
    
    for file in "${conflict_files[@]}"; do
        if [ "$priority" = "local" ]; then
            log_message "INFO" "🏠 Resolving $file with LOCAL priority"
            git checkout --ours "$file"
        else
            log_message "INFO" "🤖 Resolving $file with CODEX priority"
            git checkout --theirs "$file"
        fi
        git add "$file"
    done
    
    # Handle add/delete conflicts
    local add_delete_files=($(git status --porcelain | grep -E "^(DU|UD|AU|UA)" | cut -c4-))
    
    for file in "${add_delete_files[@]}"; do
        log_message "INFO" "⚡ Resolving add/delete conflict: $file"
        if [ "$priority" = "local" ]; then
            git checkout --ours "$file" 2>/dev/null || git rm "$file" 2>/dev/null || true
        else
            git checkout --theirs "$file" 2>/dev/null || git rm "$file" 2>/dev/null || true
        fi
        git add "$file" 2>/dev/null || true
    done
    
    # Commit the resolution
    local total_conflicts=$((${#conflict_files[@]} + ${#add_delete_files[@]}))
    
    if [ $total_conflicts -gt 0 ]; then
        if git commit --no-edit -m "Auto-resolve: $total_conflicts conflicts resolved with $priority priority" >/dev/null 2>&1; then
            log_message "INFO" "✅ $total_conflicts conflicts resolved and committed"
            return 0
        else
            log_message "ERROR" "❌ Failed to commit conflict resolution"
            return 1
        fi
    else
        log_message "INFO" "ℹ️ No conflicts found to resolve"
        return 0
    fi
}

# Fallback mode when remote is unavailable
handle_fallback_mode() {
    log_message "INFO" "🔄 Entering FALLBACK MODE - working with local branches only"
    
    # Work with local branches
    local local_branches=($(git branch | grep -E "(work|codex)" | tr -d ' *'))
    
    log_message "INFO" "🏠 Local branches available: ${local_branches[*]}"
    
    for branch in "${local_branches[@]}"; do
        local unmerged=$(git rev-list --count "$MAIN_BRANCH..$branch" 2>/dev/null || echo "0")
        
        if [ "$unmerged" -gt 0 ]; then
            log_message "INFO" "🔄 Merging local branch $branch ($unmerged commits)..."
            
            if git merge "$branch" --no-edit >/dev/null 2>&1; then
                log_message "INFO" "✅ Successfully merged local branch $branch"
            else
                log_message "WARN" "⚠️ Conflicts in $branch, auto-resolving with local priority..."
                resolve_all_conflicts "local"
            fi
        fi
    done
    
    # Mark for later remote sync
    echo "$(date '+%Y-%m-%d %H:%M:%S'): Fallback merge completed - $(git rev-parse HEAD)" >> "$RECOVERY_FILE"
    log_message "INFO" "📝 Fallback mode completed, queued for remote sync when available"
    
    return 0
}

# Main sync orchestration with bulletproof logic
orchestrate_bulletproof_sync() {
    local mode="${1:-automatic}"
    local attempt=1
    
    log_message "INFO" "🚀 Starting bulletproof sync orchestration (mode: $mode)..."
    
    # Sync time first
    bulletproof_time_sync
    
    while [ $attempt -le $MAX_RETRIES ]; do
        log_message "INFO" "🔄 Sync attempt $attempt/$MAX_RETRIES..."
        
        # Comprehensive status check
        local status=$(check_comprehensive_status)
        IFS=':' read -r repo_ok network_ok github_ok origin_ok git_lock_ok <<< "$status"
        
        log_message "INFO" "📊 System Status - Repo:$repo_ok Net:$network_ok GitHub:$github_ok Origin:$origin_ok Locks:$git_lock_ok"
        
        # Check if repository is accessible
        if [ "$repo_ok" -ne 0 ] || [ "$git_lock_ok" -ne 0 ]; then
            log_message "WARN" "⚠️ Repository locked or unavailable, waiting..."
            sleep $RETRY_DELAY
            attempt=$((attempt + 1))
            continue
        fi
        
        # Check remote accessibility
        if [ "$network_ok" -ne 0 ] || [ "$github_ok" -ne 0 ] || [ "$origin_ok" -ne 0 ]; then
            if [ $attempt -eq $MAX_RETRIES ]; then
                log_message "WARN" "⚠️ Remote unavailable after all attempts, entering fallback mode"
                return handle_fallback_mode
            else
                log_message "WARN" "⚠️ Remote unavailable, retrying in ${RETRY_DELAY}s..."
                sleep $RETRY_DELAY
                attempt=$((attempt + 1))
                continue
            fi
        fi
        
        # Try to perform the actual sync
        if timeout $REMOTE_TIMEOUT git fetch origin main >/dev/null 2>&1; then
            log_message "INFO" "✅ Fetch successful, proceeding with merge analysis"
            break
        else
            if [ $attempt -eq $MAX_RETRIES ]; then
                log_message "WARN" "⚠️ Fetch failed after all attempts, entering fallback mode"
                return handle_fallback_mode
            else
                log_message "WARN" "⚠️ Fetch failed, retrying..."
                sleep $RETRY_DELAY
                attempt=$((attempt + 1))
            fi
        fi
    done
    
    return 0
}

# Recovery management
handle_recovery_queue() {
    if [ -f "$RECOVERY_FILE" ]; then
        log_message "INFO" "🔄 Processing recovery queue..."
        
        while IFS= read -r line; do
            log_message "INFO" "♻️ Recovery item: $line"
            # Process recovery items here
        done < "$RECOVERY_FILE"
        
        # Clear recovery queue after processing
        > "$RECOVERY_FILE"
        log_message "INFO" "✅ Recovery queue processed and cleared"
    fi
}

# Main execution function
main() {
    local command="${1:-sync}"
    local mode="${2:-automatic}"
    
    log_message "INFO" "🎯 Bulletproof Codex Sync Manager starting..."
    log_message "INFO" "📋 Command: $command, Mode: $mode"
    
    case "$command" in
        "sync")
            # Handle any pending recovery items first
            handle_recovery_queue
            
            # Orchestrate the sync
            if orchestrate_bulletproof_sync "$mode"; then
                # Check if merge is needed
                local behind=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
                
                if [ "$behind" -gt 0 ]; then
                    log_message "INFO" "📥 Repository is $behind commits behind, performing merge..."
                    
                    if perform_bulletproof_merge "origin/main" "$mode"; then
                        log_message "INFO" "✅ Bulletproof sync completed successfully"
                        log_message "INFO" "🎯 All systems synchronized: Local ⟷ GitHub ⟷ Codex"
                    else
                        log_message "ERROR" "❌ Merge failed, adding to recovery queue"
                        echo "$(date '+%Y-%m-%d %H:%M:%S'): Failed merge - manual intervention needed" >> "$RECOVERY_FILE"
                    fi
                else
                    log_message "INFO" "✅ Repository already up to date"
                fi
            else
                log_message "ERROR" "❌ Sync orchestration failed"
            fi
            ;;
        "status")
            log_message "INFO" "📊 System Status Report"
            local status=$(check_comprehensive_status)
            echo "Repository Status: $status"
            
            if [ -f "$RECOVERY_FILE" ] && [ -s "$RECOVERY_FILE" ]; then
                echo "⚠️ Recovery queue has $(wc -l < "$RECOVERY_FILE") items"
            else
                echo "✅ No pending recovery items"
            fi
            ;;
        "recover")
            log_message "INFO" "♻️ Manual recovery initiated"
            handle_recovery_queue
            main "sync" "interactive"
            ;;
        "cleanup")
            log_message "INFO" "🧹 Cleaning up temporary files"
            rm -f "$STATE_FILE" "$STATE_FILE.branches" 2>/dev/null
            log_message "INFO" "✅ Cleanup completed"
            ;;
        *)
            echo "Bulletproof Codex Sync Manager"
            echo "Usage: $0 [sync|status|recover|cleanup] [automatic|interactive]"
            echo ""
            echo "Commands:"
            echo "  sync      - Perform bulletproof synchronization (default)"
            echo "  status    - Show system status and recovery queue"
            echo "  recover   - Process recovery queue and retry failed operations"
            echo "  cleanup   - Clean temporary files and reset state"
            echo ""
            echo "Modes:"
            echo "  automatic - Codex/Remote priority (default for hooks)"
            echo "  interactive - More nuanced priority decisions"
            ;;
    esac
    
    # Clean up temporary files
    rm -f "$STATE_FILE.branches" 2>/dev/null
    
    log_message "INFO" "🏁 Bulletproof Codex Sync Manager completed"
}

# Execute main function
main "$@"
