#!/bin/bash
# Codex Sync Monitor - continuous monitoring and recovery service

# Configuration
MONITOR_INTERVAL=30  # Check every 30 seconds
CODEX_SESSION_TIMEOUT=60  # 1 minute timeout for Codex session
SERVICE_NAME="Codex Sync Monitor"
PID_FILE="./.codex_monitor.pid"
LOG_FILE="./.codex_monitor.log"
CODEX_SESSION_FILE="./.codex_session_active"
LAST_CODEX_ACTIVITY_FILE="./.last_codex_activity"

# Logging function
log_monitor() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [MONITOR] $message" | tee -a "$LOG_FILE"
}

# Function to check Codex session activity
check_codex_session() {
    local current_time=$(date +%s)
    
    # Check if Codex session file exists and is recent
    if [ -f "$CODEX_SESSION_FILE" ]; then
        local session_time=$(stat -f %m "$CODEX_SESSION_FILE" 2>/dev/null || echo 0)
        local time_diff=$((current_time - session_time))
        
        if [ $time_diff -lt $CODEX_SESSION_TIMEOUT ]; then
            echo "$current_time" > "$LAST_CODEX_ACTIVITY_FILE"
            return 0  # Session is active
        fi
    fi
    
    # Check if there was recent activity
    if [ -f "$LAST_CODEX_ACTIVITY_FILE" ]; then
        local last_activity=$(cat "$LAST_CODEX_ACTIVITY_FILE")
        local time_since_activity=$((current_time - last_activity))
        
        if [ $time_since_activity -ge $CODEX_SESSION_TIMEOUT ]; then
            return 1  # Session timed out
        fi
    fi
    
    return 2  # No session detected
}

# Function to mark Codex session as active
mark_codex_active() {
    touch "$CODEX_SESSION_FILE"
    echo "$(date +%s)" > "$LAST_CODEX_ACTIVITY_FILE"
    log_monitor "Codex session marked as active"
}

# Function to restart development execution
restart_dev_execution() {
    log_monitor "Codex session timeout detected - starting local execution"
    
    # Check if there's a dev plan to continue
    if [ -f "./DEV_PLAN.md" ]; then
        log_monitor "Attempting to continue DEV_PLAN execution locally..."
        
        # Try to run auto dev runner
        if python3 auto_dev_runner.py . 2>&1 | tee -a "$LOG_FILE"; then
            log_monitor "Local DEV_PLAN execution completed successfully"
        else
            log_monitor "Local DEV_PLAN execution failed"
        fi
    else
        log_monitor "No DEV_PLAN.md found to continue"
    fi
}

# Function to cleanup stale session files on startup
cleanup_stale_sessions() {
    local current_time=$(date +%s)
    local cleaned=false
    
    # Check session file age
    if [ -f "$CODEX_SESSION_FILE" ]; then
        local session_time=$(stat -f %m "$CODEX_SESSION_FILE" 2>/dev/null || echo 0)
        local time_diff=$((current_time - session_time))
        
        if [ $time_diff -ge $CODEX_SESSION_TIMEOUT ]; then
            log_monitor "Removing stale session file (age: ${time_diff}s > ${CODEX_SESSION_TIMEOUT}s)"
            rm -f "$CODEX_SESSION_FILE"
            cleaned=true
        fi
    fi
    
    # Check activity file age
    if [ -f "$LAST_CODEX_ACTIVITY_FILE" ]; then
        local activity_time_content=$(cat "$LAST_CODEX_ACTIVITY_FILE" 2>/dev/null || echo 0)
        local time_diff=$((current_time - activity_time_content))
        
        if [ $time_diff -ge $CODEX_SESSION_TIMEOUT ]; then
            log_monitor "Removing stale activity file (age: ${time_diff}s > ${CODEX_SESSION_TIMEOUT}s)"
            rm -f "$LAST_CODEX_ACTIVITY_FILE"
            cleaned=true
        fi
    fi
    
    if [ "$cleaned" = true ]; then
        log_monitor "Startup cleanup completed - stale session files removed"
    else
        log_monitor "Startup cleanup completed - no stale files found"
    fi
}

# Function to check if monitor is already running
is_monitor_running() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" >/dev/null 2>&1; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

# Function to start monitoring
start_monitor() {
    if is_monitor_running; then
        log_monitor "Monitor is already running (PID: $(cat $PID_FILE))"
        return 1
    fi
    
    log_monitor "Starting $SERVICE_NAME..."
    
    # Clean up stale session files on startup
    cleanup_stale_sessions
    
    echo $$ > "$PID_FILE"
    
    while true; do
        # Check Codex session status
        session_status=$(check_codex_session)
        case $session_status in
            0)
                log_monitor "Codex session is active"
                ;;
            1)
                log_monitor "Codex session timed out - triggering local execution"
                restart_dev_execution
                # Reset session tracking after restart
                rm -f "$CODEX_SESSION_FILE" "$LAST_CODEX_ACTIVITY_FILE"
                ;;
            2)
                log_monitor "No Codex session detected - monitoring..."
                ;;
        esac
        
        # Check for pending sync tasks
        if [ -f "./.codex_sync_pending" ]; then
            log_monitor "Found pending sync task, attempting recovery..."
            if ./sync_codex_repo.sh --recover; then
                log_monitor "Recovery successful"
            else
                log_monitor "Recovery failed, will retry in ${MONITOR_INTERVAL}s"
            fi
        fi
        
        # Check repository health
        if ! git status >/dev/null 2>&1; then
            log_monitor "Repository health check failed"
        fi
        
        sleep $MONITOR_INTERVAL
    done
}

# Function to stop monitoring
stop_monitor() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" >/dev/null 2>&1; then
            kill "$pid"
            rm -f "$PID_FILE"
            log_monitor "Monitor stopped"
        else
            rm -f "$PID_FILE"
            log_monitor "Monitor was not running"
        fi
    else
        log_monitor "Monitor is not running"
    fi
}

# Function to show status
show_status() {
    if is_monitor_running; then
        echo "✅ $SERVICE_NAME is running (PID: $(cat $PID_FILE))"
        
        # Check Codex session status
        session_status=$(check_codex_session)
        case $session_status in
            0)
                echo "🟢 Codex session is active"
                ;;
            1)
                echo "🔴 Codex session timed out"
                ;;
            2)
                echo "🟡 No Codex session detected"
                ;;
        esac
        
        if [ -f "./.codex_sync_pending" ]; then
            echo "⚠️  Pending sync task exists"
        else
            echo "✅ No pending sync tasks"
        fi
    else
        echo "❌ $SERVICE_NAME is not running"
    fi
}

# Main execution
case "$1" in
    start)
        start_monitor
        ;;
    stop)
        stop_monitor
        ;;
    restart)
        stop_monitor
        sleep 2
        start_monitor
        ;;
    status)
        show_status
        ;;
    mark-active)
        mark_codex_active
        ;;
    cleanup)
        cleanup_stale_sessions
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|mark-active|cleanup}"
        echo ""
        echo "Commands:"
        echo "  start       - Start the Codex sync monitor"
        echo "  stop        - Stop the Codex sync monitor"
        echo "  restart     - Restart the Codex sync monitor"
        echo "  status      - Show monitor status"
        echo "  mark-active - Mark Codex session as active (call from Codex)"
        echo "  cleanup     - Clean up stale session files manually"
        exit 1
        ;;
esac
