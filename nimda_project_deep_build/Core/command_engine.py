#!/usr/bin/env python3
"""
Command Engine for NIMDA System
Processes CLI commands and integrates with existing plugins
"""

import asyncio
import logging
import subprocess
import shlex
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class CommandEngine:
    """
    Advanced command processing engine with plugin integration
    and deep context awareness
    """
    
    def __init__(self, project_path: Optional[str] = None):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.command_registry = {}
        self.plugin_paths = []
        self.command_history = []
        
    async def initialize(self):
        """Initialize command engine"""
        logger.info("⚙️  Initializing Command Engine...")
        
        # Register built-in commands
        await self._register_builtin_commands()
        
        # Discover and load plugins
        await self._discover_plugins()
        
        logger.info("✅ Command Engine initialized")

    async def execute_command(self, command: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a command with context"""
        logger.info(f"🔧 Executing command: {command}")
        
        # Parse command
        parsed = self._parse_command(command)
        
        # Execute with context
        result = await self._execute_parsed_command(parsed, context or {})
        
        # Store in history
        self.command_history.append({
            "command": command,
            "result": result,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        return result

    def _parse_command(self, command: str) -> Dict[str, Any]:
        """Parse command into components"""
        parts = shlex.split(command)
        
        return {
            "command": parts[0] if parts else "",
            "args": parts[1:] if len(parts) > 1 else [],
            "raw": command
        }

    async def _execute_parsed_command(self, parsed: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute parsed command"""
        command_name = parsed["command"]
        
        # Check if it's a registered command
        if command_name in self.command_registry:
            handler = self.command_registry[command_name]
            return await handler(parsed["args"], context)
        
        # Try to execute as system command
        return await self._execute_system_command(parsed, context)

    async def _execute_system_command(self, parsed: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system command"""
        try:
            process = await asyncio.create_subprocess_exec(
                parsed["command"], *parsed["args"],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_path
            )
            
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "return_code": process.returncode,
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
                "command": parsed["raw"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": parsed["raw"]
            }

    async def _register_builtin_commands(self):
        """Register built-in commands"""
        
        async def status_command(args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
            """Get system status"""
            return {
                "success": True,
                "status": "Command engine operational",
                "commands_registered": len(self.command_registry),
                "command_history_count": len(self.command_history)
            }
        
        async def help_command(args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
            """Show help information"""
            return {
                "success": True,
                "available_commands": list(self.command_registry.keys()),
                "help": "Available commands listed above"
            }
        
        # Register commands
        self.command_registry["status"] = status_command
        self.command_registry["help"] = help_command

    async def _discover_plugins(self):
        """Discover and load command plugins"""
        # Look for plugin files
        plugin_patterns = ["*_plugin.py", "*_command.py"]
        
        for pattern in plugin_patterns:
            for plugin_file in self.project_path.rglob(pattern):
                try:
                    await self._load_plugin(plugin_file)
                except Exception as e:
                    logger.warning(f"Failed to load plugin {plugin_file}: {e}")

    async def _load_plugin(self, plugin_path: Path):
        """Load a command plugin"""
        # Basic plugin loading - would be enhanced with proper module loading
        logger.info(f"📦 Loading plugin: {plugin_path.name}")
        self.plugin_paths.append(str(plugin_path))

    def register_command(self, name: str, handler):
        """Register a new command"""
        self.command_registry[name] = handler
        logger.info(f"📝 Registered command: {name}")

    def get_status(self) -> Dict[str, Any]:
        """Get command engine status"""
        return {
            "commands_registered": len(self.command_registry),
            "plugins_loaded": len(self.plugin_paths),
            "command_history_count": len(self.command_history),
            "available_commands": list(self.command_registry.keys())
        }


if __name__ == "__main__":
    async def test_command_engine():
        engine = CommandEngine()
        await engine.initialize()
        
        # Test built-in commands
        result = await engine.execute_command("status")
        print(f"Status result: {result}")
        
        result = await engine.execute_command("help")
        print(f"Help result: {result}")
        
        # Test system command
        result = await engine.execute_command("echo 'Hello from command engine'")
        print(f"Echo result: {result}")
    
    asyncio.run(test_command_engine())
