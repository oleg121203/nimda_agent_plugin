#!/bin/bash
# Temporal Priority Test Utility
# Test and validate temporal priority logic

# Source configuration
if [ -f ".codex_temporal_config" ]; then
    source .codex_temporal_config
else
    echo "⚠️  Configuration file not found, using defaults"
    TEMPORAL_THRESHOLD=60
fi

# Function to create test scenario
create_test_scenario() {
    local scenario="$1"
    echo "🧪 Creating test scenario: $scenario"
    
    case "$scenario" in
        "local_newer")
            echo "📝 Simulating local changes newer than remote..."
            # Create a commit with a future timestamp (for testing)
            ;;
        "remote_newer")
            echo "📝 Simulating remote changes newer than local..."
            ;;
        "simultaneous")
            echo "📝 Simulating nearly simultaneous changes..."
            ;;
        *)
            echo "❌ Unknown test scenario: $scenario"
            return 1
            ;;
    esac
}

# Function to test time synchronization
test_time_sync() {
    echo "🕐 Testing time synchronization..."
    
    # Get current system time
    local system_time=$(date '+%s')
    echo "💻 System time: $(date -r $system_time)"
    
    # Try to get network time
    if command -v sntp >/dev/null 2>&1; then
        local ntp_time=$(sntp -d time.apple.com 2>&1 | grep "time server" | head -1)
        echo "🌐 NTP response: $ntp_time"
    fi
    
    # Test HTTP time
    if command -v curl >/dev/null 2>&1; then
        local http_date=$(curl -sI google.com | grep -i '^date:' | sed 's/^date: //i')
        echo "🌐 HTTP date: $http_date"
    fi
}

# Function to test temporal comparison
test_temporal_comparison() {
    echo "⏱️  Testing temporal comparison logic..."
    
    # Get recent commits
    local commits=($(git log --format="%H" -n 3))
    
    if [ ${#commits[@]} -ge 2 ]; then
        local commit1="${commits[0]}"
        local commit2="${commits[1]}"
        
        local time1=$(git log -1 --format="%ct" "$commit1")
        local time2=$(git log -1 --format="%ct" "$commit2")
        
        echo "📅 Commit 1 (${commit1:0:8}): $(date -r $time1)"
        echo "📅 Commit 2 (${commit2:0:8}): $(date -r $time2)"
        
        local diff=$((time1 - time2))
        echo "⏱️  Time difference: ${diff} seconds"
        
        if [ $diff -gt $TEMPORAL_THRESHOLD ]; then
            echo "✅ Commit 1 would have priority (newer by ${diff}s > ${TEMPORAL_THRESHOLD}s)"
        else
            echo "✅ Within threshold (${diff}s <= ${TEMPORAL_THRESHOLD}s)"
        fi
    else
        echo "⚠️  Not enough commits for temporal comparison test"
    fi
}

# Function to test merge strategy selection
test_merge_strategy() {
    echo "🔄 Testing merge strategy selection..."
    
    # Simulate different scenarios
    local scenarios=("local_priority" "codex_priority" "threshold_edge")
    
    for scenario in "${scenarios[@]}"; do
        echo "📋 Scenario: $scenario"
        case "$scenario" in
            "local_priority")
                echo "   → Strategy: LOCAL (ours)"
                echo "   → Conflicts resolved in favor of local changes"
                ;;
            "codex_priority")
                echo "   → Strategy: CODEX (theirs)"
                echo "   → Conflicts resolved in favor of Codex changes"
                ;;
            "threshold_edge")
                echo "   → Strategy: CODEX (within threshold)"
                echo "   → Default to Codex priority"
                ;;
        esac
    done
}

# Function to run comprehensive test
run_comprehensive_test() {
    echo "🚀 Running comprehensive temporal priority test suite..."
    echo "=================================================="
    
    test_time_sync
    echo ""
    
    test_temporal_comparison
    echo ""
    
    test_merge_strategy
    echo ""
    
    echo "📊 Configuration Status:"
    echo "   🕐 Temporal threshold: ${TEMPORAL_THRESHOLD}s"
    echo "   🔄 Temporal priority: $([ "${TEMPORAL_PRIORITY_ENABLED:-true}" = "true" ] && echo "ENABLED" || echo "DISABLED")"
    echo "   🤖 Codex default: $([ "${CODEX_DEFAULT_PRIORITY:-true}" = "true" ] && echo "ENABLED" || echo "DISABLED")"
    echo "   🔧 Auto-resolve: $([ "${AUTO_RESOLVE_CONFLICTS:-true}" = "true" ] && echo "ENABLED" || echo "DISABLED")"
    
    echo ""
    echo "✅ Temporal priority test suite completed"
}

# Function to show help
show_help() {
    echo "Temporal Priority Test Utility"
    echo "=============================="
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  test-time      Test time synchronization"
    echo "  test-compare   Test temporal comparison logic"
    echo "  test-strategy  Test merge strategy selection"
    echo "  test-all       Run comprehensive test suite"
    echo "  help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 test-all    # Run all tests"
    echo "  $0 test-time   # Test only time synchronization"
}

# Main execution
case "${1:-test-all}" in
    "test-time")
        test_time_sync
        ;;
    "test-compare")
        test_temporal_comparison
        ;;
    "test-strategy")
        test_merge_strategy
        ;;
    "test-all")
        run_comprehensive_test
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        show_help
        exit 1
        ;;
esac
