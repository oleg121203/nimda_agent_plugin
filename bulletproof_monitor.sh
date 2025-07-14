#!/bin/bash

# Bulletproof Monitor - Continuous health monitoring and recovery system
# Monitors the sync process and automatically recovers from failures
# Part of the NIMDA Agent Bulletproof Sync System

# Enable strict error handling
set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/.bulletproof_sync_config"
SYNC_MANAGER="${SCRIPT_DIR}/bulletproof_sync_manager.sh"
LOG_FILE="${SCRIPT_DIR}/bulletproof_monitor.log"
PID_FILE="${SCRIPT_DIR}/.bulletproof_monitor.pid"

# Default configuration
MONITOR_INTERVAL=30
MAX_FAILURES=5
RECOVERY_COOLDOWN=300
HEALTH_CHECK_TIMEOUT=10

# Load configuration
if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
fi

# Logging function
log() {
    local level="$1"
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOG_FILE"
}

# Display usage information
usage() {
    cat << EOF
Bulletproof Monitor - Continuous health monitoring and recovery system

Usage: $0 [OPTIONS]

Options:
    --start             Start monitoring daemon
    --stop              Stop monitoring daemon
    --status            Show monitor status
    --health-check      Perform single health check
    --reset-failures    Reset failure counter
    --config            Show current configuration
    -h, --help          Show this help

Configuration:
    MONITOR_INTERVAL    Check interval in seconds (default: 30)
    MAX_FAILURES        Max failures before alert (default: 5)
    RECOVERY_COOLDOWN   Recovery delay in seconds (default: 300)
    HEALTH_CHECK_TIMEOUT Timeout for health checks (default: 10)

Examples:
    $0 --start          # Start monitoring daemon
    $0 --stop           # Stop monitoring daemon
    $0 --health-check   # Single health check
EOF
}

# Check if another monitor instance is running
check_running() {
    if [[ -f "$PID_FILE" ]]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            return 0  # Running
        else
            rm -f "$PID_FILE"
            return 1  # Not running
        fi
    fi
    return 1  # Not running
}

# Write PID file
write_pid() {
    echo $$ > "$PID_FILE"
}

# Clean up PID file
cleanup_pid() {
    rm -f "$PID_FILE"
}

# Trap to clean up on exit
trap cleanup_pid EXIT

# Perform health check on sync system
health_check() {
    local timeout="${1:-$HEALTH_CHECK_TIMEOUT}"
    
    log "INFO" "Performing health check with timeout: ${timeout}s"
    
    # Check if sync manager exists and is executable
    if [[ ! -x "$SYNC_MANAGER" ]]; then
        log "ERROR" "Sync manager not found or not executable: $SYNC_MANAGER"
        return 1
    fi
    
    # Check git repository status
    if ! timeout "$timeout" git -C "$SCRIPT_DIR" status --porcelain >/dev/null 2>&1; then
        log "ERROR" "Git repository health check failed"
        return 1
    fi
    
    # Check if we can reach remote (if configured)
    if git -C "$SCRIPT_DIR" remote get-url origin >/dev/null 2>&1; then
        if ! timeout "$timeout" git -C "$SCRIPT_DIR" ls-remote origin HEAD >/dev/null 2>&1; then
            log "WARN" "Remote repository unreachable (will use local fallback)"
            # This is not a failure, just a warning
        fi
    fi
    
    # Check configuration file
    if [[ ! -f "$CONFIG_FILE" ]]; then
        log "WARN" "Configuration file not found: $CONFIG_FILE"
        # This is not a failure, defaults will be used
    fi
    
    # Check for zombie processes
    local zombie_count=$(ps aux | grep -c '[Zz]ombie' || echo "0")
    if [[ "$zombie_count" -gt 0 ]]; then
        log "WARN" "Found $zombie_count zombie processes"
    fi
    
    log "INFO" "Health check completed successfully"
    return 0
}

# Recovery function
recover_system() {
    log "INFO" "Starting system recovery"
    
    # Kill any stuck sync processes
    pkill -f "bulletproof_sync" || true
    pkill -f "sync_codex_repo" || true
    
    # Clean up temporary files
    find "$SCRIPT_DIR" -name "*.tmp" -delete 2>/dev/null || true
    find "$SCRIPT_DIR" -name ".sync_lock*" -delete 2>/dev/null || true
    
    # Reset git state if needed
    git -C "$SCRIPT_DIR" reset --hard HEAD 2>/dev/null || true
    git -C "$SCRIPT_DIR" clean -fd 2>/dev/null || true
    
    # Wait for cooldown
    log "INFO" "Recovery cooldown: ${RECOVERY_COOLDOWN}s"
    sleep "$RECOVERY_COOLDOWN"
    
    log "INFO" "System recovery completed"
}

# Main monitoring loop
monitor_loop() {
    local failure_count=0
    local last_failure_time=0
    
    log "INFO" "Starting monitor loop (interval: ${MONITOR_INTERVAL}s)"
    
    while true; do
        local current_time=$(date +%s)
        
        # Perform health check
        if health_check; then
            # Reset failure count on success
            if [[ "$failure_count" -gt 0 ]]; then
                log "INFO" "Health check passed, resetting failure count"
                failure_count=0
            fi
        else
            failure_count=$((failure_count + 1))
            last_failure_time="$current_time"
            
            log "ERROR" "Health check failed (failure count: $failure_count/$MAX_FAILURES)"
            
            # Trigger recovery if max failures reached
            if [[ "$failure_count" -ge "$MAX_FAILURES" ]]; then
                log "CRITICAL" "Maximum failures reached, triggering recovery"
                recover_system
                failure_count=0
            fi
        fi
        
        # Sleep until next check
        sleep "$MONITOR_INTERVAL"
    done
}

# Start monitoring daemon
start_monitor() {
    if check_running; then
        log "INFO" "Monitor already running (PID: $(cat "$PID_FILE"))"
        return 0
    fi
    
    log "INFO" "Starting bulletproof monitor daemon"
    write_pid
    
    # Run monitoring loop
    monitor_loop
}

# Stop monitoring daemon
stop_monitor() {
    if ! check_running; then
        log "INFO" "Monitor not running"
        return 0
    fi
    
    local pid=$(cat "$PID_FILE")
    log "INFO" "Stopping monitor daemon (PID: $pid)"
    
    if kill "$pid" 2>/dev/null; then
        # Wait for graceful shutdown
        local count=0
        while kill -0 "$pid" 2>/dev/null && [[ "$count" -lt 10 ]]; do
            sleep 1
            count=$((count + 1))
        done
        
        # Force kill if still running
        if kill -0 "$pid" 2>/dev/null; then
            log "WARN" "Force killing monitor daemon"
            kill -9 "$pid" 2>/dev/null || true
        fi
    fi
    
    cleanup_pid
    log "INFO" "Monitor daemon stopped"
}

# Show monitor status
show_status() {
    echo "=== Bulletproof Monitor Status ==="
    
    if check_running; then
        local pid=$(cat "$PID_FILE")
        echo "Status: RUNNING (PID: $pid)"
        echo "Started: $(stat -c %y "$PID_FILE" 2>/dev/null || echo "Unknown")"
    else
        echo "Status: STOPPED"
    fi
    
    echo ""
    echo "Configuration:"
    echo "  Monitor interval: ${MONITOR_INTERVAL}s"
    echo "  Max failures: $MAX_FAILURES"
    echo "  Recovery cooldown: ${RECOVERY_COOLDOWN}s"
    echo "  Health check timeout: ${HEALTH_CHECK_TIMEOUT}s"
    
    echo ""
    echo "Files:"
    echo "  Config: $CONFIG_FILE"
    echo "  Log: $LOG_FILE"
    echo "  PID: $PID_FILE"
    
    echo ""
    echo "Recent log entries:"
    if [[ -f "$LOG_FILE" ]]; then
        tail -5 "$LOG_FILE" | sed 's/^/  /'
    else
        echo "  No log file found"
    fi
}

# Reset failure counters
reset_failures() {
    log "INFO" "Resetting failure counters"
    # This is mainly for manual intervention
    echo "Failure counters reset"
}

# Show current configuration
show_config() {
    echo "=== Bulletproof Monitor Configuration ==="
    
    if [[ -f "$CONFIG_FILE" ]]; then
        echo "Configuration file: $CONFIG_FILE"
        echo ""
        grep -E "^[A-Z_]+" "$CONFIG_FILE" | sed 's/^/  /' || echo "  No configuration variables found"
    else
        echo "No configuration file found: $CONFIG_FILE"
        echo "Using default values:"
        echo "  MONITOR_INTERVAL=$MONITOR_INTERVAL"
        echo "  MAX_FAILURES=$MAX_FAILURES"
        echo "  RECOVERY_COOLDOWN=$RECOVERY_COOLDOWN"
        echo "  HEALTH_CHECK_TIMEOUT=$HEALTH_CHECK_TIMEOUT"
    fi
}

# Main function
main() {
    case "${1:-}" in
        --start)
            start_monitor
            ;;
        --stop)
            stop_monitor
            ;;
        --status)
            show_status
            ;;
        --health-check)
            if health_check; then
                echo "Health check: PASSED"
                exit 0
            else
                echo "Health check: FAILED"
                exit 1
            fi
            ;;
        --reset-failures)
            reset_failures
            ;;
        --config)
            show_config
            ;;
        -h|--help)
            usage
            ;;
        "")
            usage
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Use --help for usage information" >&2
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
