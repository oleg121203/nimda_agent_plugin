"""
macOS Integration Module
Handles macOS-specific functionality and native integrations
"""
import logging
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path


class MacOSIntegration:
    """Handle macOS-specific integrations and functionality"""
    
    def __init__(self):
        self.logger = logging.getLogger("MacOSIntegration")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get macOS system information"""
        try:
            # Get macOS version
            result = subprocess.run(
                ["sw_vers", "-productVersion"], 
                capture_output=True, text=True
            )
            macos_version = result.stdout.strip() if result.returncode == 0 else "Unknown"
            
            # Get hardware info
            result = subprocess.run(
                ["sysctl", "-n", "hw.model"], 
                capture_output=True, text=True
            )
            hardware_model = result.stdout.strip() if result.returncode == 0 else "Unknown"
            
            return {
                "macos_version": macos_version,
                "hardware_model": hardware_model,
                "platform": "macOS"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system info: {e}")
            return {"error": str(e)}
    
    def send_notification(self, title: str, message: str) -> bool:
        """Send native macOS notification"""
        try:
            subprocess.run([
                "osascript", "-e", 
                f'display notification "{message}" with title "{title}"'
            ], check=True)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")
            return False
    
    def open_finder(self, path: str) -> bool:
        """Open Finder at specified path"""
        try:
            subprocess.run(["open", str(path)], check=True)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to open Finder: {e}")
            return False


if __name__ == "__main__":
    integration = MacOSIntegration()
    print("MacOSIntegration loaded successfully")
    
    # Test system info
    info = integration.get_system_info()
    print(f"System info: {info}")
