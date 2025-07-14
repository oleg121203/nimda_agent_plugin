#!/usr/bin/env python3
"""Test Codex session integration"""

import time


# Simulate what command_processor does
def mark_codex_session_active():
    """Mark Codex session as active for local monitor"""
    try:
        codex_session_file = "./.codex_session_active"
        last_activity_file = "./.last_codex_activity"

        # Create session file
        with open(codex_session_file, "w") as f:
            f.write(str(time.time()))

        # Update last activity
        with open(last_activity_file, "w") as f:
            f.write(str(int(time.time())))

        print("✅ Codex session marked as active")
        return True
    except Exception as e:
        print(f"❌ Failed to mark Codex session active: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing Codex session creation...")

    # Test session creation
    if mark_codex_session_active():
        import os

        print(f"📁 Session file exists: {os.path.exists('.codex_session_active')}")
        print(f"📁 Activity file exists: {os.path.exists('.last_codex_activity')}")

        # Show file contents
        try:
            with open(".codex_session_active", "r") as f:
                print(f"🕒 Session timestamp: {f.read().strip()}")
            with open(".last_codex_activity", "r") as f:
                print(f"🕒 Activity timestamp: {f.read().strip()}")
        except Exception as e:
            print(f"Error reading files: {e}")
    else:
        print("❌ Test failed")
