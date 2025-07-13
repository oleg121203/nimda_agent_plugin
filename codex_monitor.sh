#!/bin/bash
# Codex Sync Monitor - continuous monitoring and recovery service

# Configuration
MONITOR_INTERVAL=60  # Check every minute
SERVICE_NAME="Codex Sync Monitor"
PID_FILE="./.codex_monitor.pid"
LOG_FILE="./.codex_monitor.log"

# Logging function
log_monitor() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [MONITOR] $message" | tee -a "$LOG_FILE"
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
    echo $$ > "$PID_FILE"
    
    while true; do
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
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the Codex sync monitor"
        echo "  stop    - Stop the Codex sync monitor"
        echo "  restart - Restart the Codex sync monitor"
        echo "  status  - Show monitor status"
        exit 1
        ;;
esac
