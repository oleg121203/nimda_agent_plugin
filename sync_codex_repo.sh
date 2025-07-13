#!/bin/bash
# Auto-sync script to check and sync with remote repository
# Enhanced with retry mechanism and availability waiting

# Configuration
MAX_RETRIES=5
RETRY_DELAY=10
WAIT_INTERVAL=30
MAX_WAIT_TIME=600
LOG_FILE="./.codex_sync.log"

# Logging function
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# Function to check repository availability
check_repo_availability() {
    git status --porcelain >/dev/null 2>&1 && \
    [ -f ".git/config" ] && \
    [ ! -f ".git/index.lock" ] && \
    [ ! -f ".git/HEAD.lock" ]
    return $?
}

# Function to check network connectivity
check_network() {
    if command -v ping >/dev/null 2>&1; then
        ping -c 1 github.com >/dev/null 2>&1
    else
        git ls-remote origin HEAD >/dev/null 2>&1
    fi
    return $?
}

# Function to sync system time and determine temporal priority
sync_time_and_determine_priority() {
    local local_ref="$1"
    local remote_ref="$2"
    
    log_message "🕐 Synchronizing system time for accurate comparison..."
    
    # Try to sync time using available methods
    if command -v sntp >/dev/null 2>&1; then
        sntp -sS time.apple.com >/dev/null 2>&1 && log_message "✅ Time synchronized via SNTP"
    elif command -v ntpdate >/dev/null 2>&1; then
        sudo ntpdate -s time.nist.gov >/dev/null 2>&1 && log_message "✅ Time synchronized via ntpdate"
    else
        log_message "⚠️  No time sync tool available, using system time"
    fi
    
    # Get commit timestamps
    local local_time=$(git log -1 --format="%ct" "$local_ref" 2>/dev/null)
    local remote_time=$(git log -1 --format="%ct" "$remote_ref" 2>/dev/null)
    
    if [ -z "$local_time" ] || [ -z "$remote_time" ]; then
        log_message "⚠️  Cannot determine timestamps, defaulting to Codex priority"
        return 1  # Default to Codex priority
    fi
    
    local time_diff=$((local_time - remote_time))
    local threshold=60  # 60 seconds threshold
    
    log_message "📅 Local commit: $(date -r $local_time '+%Y-%m-%d %H:%M:%S')"
    log_message "📅 Remote commit: $(date -r $remote_time '+%Y-%m-%d %H:%M:%S')"
    log_message "⏱️  Time difference: ${time_diff}s"
    
    # If local changes are significantly newer, prioritize local
    if [ $time_diff -gt $threshold ]; then
        log_message "🏠 Local changes are newer by ${time_diff}s - LOCAL PRIORITY"
        return 0  # Local priority
    else
        log_message "🤖 Remote/Codex changes are newer or within threshold - CODEX PRIORITY"
        return 1  # Codex priority
    fi
}

# Function to perform smart merge with temporal logic
perform_temporal_merge() {
    local behind_count="$1"
    local ahead_count="$2"
    
    log_message "🧠 Performing temporal priority analysis for merge strategy..."
    
    # Determine priority based on timestamps
    if sync_time_and_determine_priority "HEAD" "origin/main"; then
        # LOCAL PRIORITY
        log_message "🏠 Applying LOCAL PRIORITY merge strategy"
        
        if [ "$ahead_count" -gt 0 ]; then
            log_message "📤 Local repository has newer changes, merging remote with local priority"
            if execute_with_retries "git merge origin/main --no-edit -X ours" "Local priority merge"; then
                log_message "✅ Successfully merged with local priority"
                return 0
            else
                log_message "⚠️  Conflicts detected, resolving with local priority..."
                # Resolve conflicts favoring local changes
                git status --porcelain | grep "^UU" | while read -r line; do
                    file=$(echo "$line" | cut -c4-)
                    log_message "⚡ Resolving conflict in $file with LOCAL priority"
                    git checkout --ours "$file"
                    git add "$file"
                done
                
                if git commit --no-edit 2>/dev/null; then
                    log_message "✅ Conflicts resolved with local priority"
                    return 0
                fi
            fi
        else
            # Fast-forward merge but log that local would have priority
            log_message "📥 Fast-forward merge (local priority noted for future conflicts)"
            if execute_with_retries "git merge origin/main --ff-only" "Fast-forward merge with local priority context"; then
                return 0
            fi
        fi
    else
        # CODEX PRIORITY
        log_message "🤖 Applying CODEX PRIORITY merge strategy"
        
        if [ "$ahead_count" -eq 0 ]; then
            # Safe to fast-forward
            if execute_with_retries "git merge origin/main --ff-only" "Fast-forward merge with Codex priority"; then
                log_message "✅ Successfully synchronized with fast-forward merge"
                return 0
            fi
        else
            log_message "⚠️  Local has commits ahead of remote"
            log_message "🔄 Attempting rebase to maintain Codex priority..."
            if execute_with_retries "git rebase origin/main" "Rebase with Codex priority"; then
                log_message "✅ Successfully rebased onto remote Codex changes"
                return 0
            else
                log_message "⚠️  Rebase failed, trying merge with Codex priority..."
                if execute_with_retries "git merge origin/main --no-edit -X theirs" "Merge with Codex priority"; then
                    return 0
                else
                    # Manual conflict resolution with Codex priority
                    git status --porcelain | grep "^UU" | while read -r line; do
                        file=$(echo "$line" | cut -c4-)
                        log_message "⚡ Resolving conflict in $file with CODEX priority"
                        git checkout --theirs "$file"
                        git add "$file"
                    done
                    
                    if git commit --no-edit 2>/dev/null; then
                        log_message "✅ Conflicts resolved with Codex priority"
                        return 0
                    fi
                fi
            fi
        fi
    fi
    
    log_message "❌ All merge strategies failed"
    return 1
}
execute_with_retries() {
    local operation="$1"
    local description="$2"
    local attempt=1
    
    while [ $attempt -le $MAX_RETRIES ]; do
        log_message "🔄 $description (attempt $attempt/$MAX_RETRIES)"
        
        # Check prerequisites
        if ! check_repo_availability; then
            log_message "⚠️  Repository unavailable (attempt $attempt)"
        elif ! check_network; then
            log_message "⚠️  Network unavailable (attempt $attempt)"
        else
            # Execute the operation
            if eval "$operation" 2>/dev/null; then
                log_message "✅ $description successful"
                return 0
            else
                log_message "⚠️  $description failed (attempt $attempt)"
            fi
        fi
        
        if [ $attempt -lt $MAX_RETRIES ]; then
            log_message "⏳ Waiting ${RETRY_DELAY}s before retry..."
            sleep $RETRY_DELAY
            # Exponential backoff
            RETRY_DELAY=$((RETRY_DELAY * 2))
            if [ $RETRY_DELAY -gt 60 ]; then
                RETRY_DELAY=60
            fi
        fi
        
        attempt=$((attempt + 1))
    done
    
    log_message "❌ $description failed after $MAX_RETRIES attempts"
    return 1
}

# Function to wait for repository availability
wait_for_availability() {
    local wait_time=0
    
    log_message "⏳ Repository/network unavailable, entering wait mode..."
    log_message "🔍 Checking every ${WAIT_INTERVAL}s (max wait: ${MAX_WAIT_TIME}s)"
    
    while [ $wait_time -lt $MAX_WAIT_TIME ]; do
        if check_repo_availability && check_network; then
            log_message "✅ Repository and network became available after ${wait_time}s"
            return 0
        fi
        
        if [ $((wait_time % 120)) -eq 0 ] && [ $wait_time -gt 0 ]; then
            log_message "⏳ Still waiting... (${wait_time}/${MAX_WAIT_TIME}s)"
        fi
        
        sleep $WAIT_INTERVAL
        wait_time=$((wait_time + WAIT_INTERVAL))
    done
    
    log_message "❌ Repository did not become available within ${MAX_WAIT_TIME}s"
    return 1
}

# Function to create recovery task
create_recovery_task() {
    local task_file="./.codex_sync_pending"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    cat > "$task_file" << EOF
# Codex Sync Recovery Task
# Created: $timestamp
# Status: PENDING

# This file indicates a pending sync operation
# Run './sync_codex_repo.sh --recover' to retry
PENDING_OPERATION=true
CREATED_AT="$timestamp"
REASON="Repository or network unavailable during auto-sync"
EOF
    
    log_message "📝 Created recovery task file: $task_file"
}

# Function to handle recovery
handle_recovery() {
    local task_file="./.codex_sync_pending"
    
    if [ -f "$task_file" ]; then
        log_message "🔄 Found pending sync task, attempting recovery..."
        rm "$task_file"
        log_message "📝 Removed recovery task file"
        return 0
    else
        log_message "ℹ️  No pending recovery tasks found"
        return 1
    fi
}

# Main sync function
perform_sync() {
    log_message "🔄 Checking repository synchronization status..."
    
    # Check initial availability
    if ! check_repo_availability || ! check_network; then
        if ! wait_for_availability; then
            create_recovery_task
            return 1
        fi
    fi
    
    # Fetch latest changes from remote with retries
    if ! execute_with_retries "git fetch origin main --quiet" "Fetching from remote"; then
        create_recovery_task
        return 1
    fi
    
    # Check synchronization status
    BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
    AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
    
    if [ "$BEHIND" -gt 0 ]; then
        log_message "📥 Local repository is $BEHIND commits behind remote"
        
        # Check if the latest remote commits are Codex auto-merges
        LATEST_REMOTE_COMMITS=$(git log --oneline origin/main~$BEHIND..origin/main --grep="Auto-merge.*Codex" 2>/dev/null | wc -l | tr -d ' ')
        
        if [ "$LATEST_REMOTE_COMMITS" -gt 0 ]; then
            log_message "🤖 Detected Codex auto-merge commits on remote"
            log_message "🔄 Performing temporal priority synchronization..."
            
            # Use temporal merge logic
            if perform_temporal_merge "$BEHIND" "$AHEAD"; then
                log_message "✅ Successfully synchronized with temporal priority logic"
            else
                create_recovery_task
                return 1
            fi
        else
            log_message "📋 Remote changes detected but not Codex auto-merges"
            log_message "� Applying standard merge with temporal priority logic..."
            
            # Still use temporal logic for non-Codex merges
            if perform_temporal_merge "$BEHIND" "$AHEAD"; then
                log_message "✅ Successfully synchronized with temporal priority logic"
            else
                log_message "🔧 Manual review recommended"
            fi
        fi
    elif [ "$AHEAD" -gt 0 ]; then
        log_message "📤 Local repository is $AHEAD commits ahead of remote"
        log_message "🚀 Ready to push local changes"
    else
        log_message "✅ Repository is already synchronized"
    fi
    
    log_message "🎯 Codex priority system status: ACTIVE"
    return 0
}

# Main execution
main() {
    # Handle command line arguments
    if [ "$1" = "--recover" ]; then
        if handle_recovery; then
            perform_sync
        fi
    elif [ "$1" = "--status" ]; then
        if [ -f "./.codex_sync_pending" ]; then
            echo "⚠️  Pending sync task exists"
            cat "./.codex_sync_pending"
        else
            echo "✅ No pending sync tasks"
        fi
    else
        perform_sync
    fi
}

# Run main function
main "$@"
