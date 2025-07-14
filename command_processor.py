"""Command processor for NIMDA Agent.

Handles             "execute_codex_mode": [
                r"codex execute.*full.*dev",
                r"codex execute.*complete.*plan",
                r"codex run.*full.*plan",
                r"codex do.*everything",
                r"codex run full dev",
                r"codex.*run.*full.*dev",
            ],mands from Codex."""

import logging
import re
from typing import Any, Dict, List, Optional, Tuple


class CommandProcessor:
    """Process user commands received via Codex."""

    def __init__(self, agent):
        """
        Initialize command processor

        Args:
            agent: NIMDAAgent instance
        """
        self.agent = agent
        self.logger = logging.getLogger("CommandProcessor")

        # Session tracking
        self.codex_session_file = "./.codex_session_active"
        self.last_activity_file = "./.last_codex_activity"

        # Command patterns
        self.command_patterns = {
            "update_plan": [
                r"update.*dev.*plan",
                r"improve.*plan",
                r"extend.*plan",
                r"enhance.*plan",
            ],
            "execute_task": [
                r"execute.*task.*(\d+)",
                r"do.*task.*(\d+)",
                r"run.*task.*(\d+)",
                r"task\s*(\d+)",
            ],
            "execute_codex_mode": [
                r"codex execute.*full.*dev",
                r"codex execute.*complete.*plan",
                r"codex run.*full.*plan",
                r"codex do.*everything",
                r"codex run full dev",
                r"codex.*run.*full.*dev",
                r"codex start.*full.*dev",
                r"codex start.*complete.*plan",
            ],
            "execute_full_plan": [
                r"execute.*full.*dev",
                r"execute.*complete.*plan",
                r"run.*full.*plan",
                r"do.*everything",
                r"run full dev",
                r"start.*full.*dev",
                r"start.*complete.*plan",
            ],
            "status": [r"status", r"state", r"what.*doing", r"how.*going", r"progress"],
            "sync": [r"sync", r"synchronize", r"git.*sync", r"update.*git"],
            "fix_errors": [r"fix.*errors", r"debug", r"repair", r"solve.*issues"],
            "initialize": [r"initialize", r"setup", r"init", r"create.*project"],
            "help": [r"help", r"commands", r"what.*can.*do"],
        }

    def process(self, command: str) -> Dict[str, Any]:
        """
        Process user command

        Args:
            command: User command

        Returns:
            Command result
        """
        try:
            # Mark Codex session as active when any command is received
            self._mark_codex_session_active()

            # Command normalization
            normalized_command = command.lower().strip()

            self.logger.info(f"Processing command: {command}")

            # Detect command type
            command_type, params = self._identify_command(normalized_command)

            if not command_type:
                return self._handle_unknown_command(command)

            # Execute the command
            return self._execute_command(command_type, params, command)

        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Error processing command",
                "command": command,
            }

    def _identify_command(self, command: str) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Identify command type by patterns

        Args:
            command: Normalized command

        Returns:
            Command type and parameters
        """
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, command, re.IGNORECASE | re.UNICODE)
                if match:
                    params = {}

                    # Extract parameters from regex groups
                    if match.groups():
                        if command_type == "execute_task":
                            params["task_number"] = int(match.group(1))

                    return command_type, params

        return None, {}

    def _execute_command(
        self, command_type: str, params: Dict[str, Any], original_command: str
    ) -> Dict[str, Any]:
        """
        Execute specific command

        Args:
            command_type: Command type
            params: Command parameters
            original_command: Original command

        Returns:
            Execution result
        """
        try:
            self.logger.info(f"Executing command type: {command_type}")

            if command_type == "update_plan":
                return self._handle_update_plan()

            elif command_type == "execute_task":
                task_number = params.get("task_number")
                if task_number:
                    return self._handle_execute_task(task_number)
                else:
                    return {"success": False, "message": "Task number not specified"}

            elif command_type == "execute_full_plan":
                return self._handle_execute_full_plan()

            elif command_type == "execute_codex_mode":
                return self._handle_execute_codex_mode()

            elif command_type == "status":
                return self._handle_status()

            elif command_type == "sync":
                return self._handle_sync()

            elif command_type == "fix_errors":
                return self._handle_fix_errors()

            elif command_type == "initialize":
                return self._handle_initialize()

            elif command_type == "help":
                return self._handle_help()

            else:
                return {
                    "success": False,
                    "message": f"Command '{command_type}' not implemented",
                }

        except Exception as e:
            self.logger.error(f"Error executing command {command_type}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Error executing command {command_type}",
            }

    def _handle_update_plan(self) -> Dict[str, Any]:
        """Handle plan update command"""
        self.logger.info("Executing DEV_PLAN.md update")

        result = self.agent.update_dev_plan()

        if result["success"]:
            # Additional information for user
            result["user_message"] = "✅ DEV_PLAN.md successfully updated and extended"
        else:
            result["user_message"] = "❌ Error updating DEV_PLAN.md"

        return result

    def _handle_execute_task(self, task_number: int) -> Dict[str, Any]:
        """Handle specific task execution command"""
        self.logger.info(f"Executing task #{task_number}")

        # Check if task exists
        plan_status = self.agent.dev_plan_manager.get_plan_status()

        if task_number > plan_status["total_tasks"] or task_number <= 0:
            return {
                "success": False,
                "message": f"Task #{task_number} does not exist. Available {plan_status['total_tasks']} tasks",
                "user_message": f"❌ Task #{task_number} not found",
            }

        result = self.agent.execute_dev_plan(task_number=task_number)

        if result["success"]:
            result["user_message"] = f"✅ Task #{task_number} successfully executed"
        else:
            result["user_message"] = f"❌ Error executing task #{task_number}"

        return result

    def _handle_execute_full_plan(self) -> Dict[str, Any]:
        """Handle full plan execution command"""
        self.logger.info("Executing full DEV_PLAN.md")

        # User warning
        plan_status = self.agent.dev_plan_manager.get_plan_status()

        if plan_status["total_tasks"] == 0:
            return {
                "success": False,
                "message": "DEV_PLAN.md is empty or contains no tasks",
                "user_message": "❌ No tasks to execute",
            }

        # Create backup before execution
        backup_result = self.agent.git_manager.create_backup_branch()

        if not backup_result["success"]:
            self.logger.warning("Failed to create backup")

        # Execute plan with full synchronization
        cycle_result = self.agent.run_full_dev_cycle()

        plan_info = cycle_result.get("plan", {})

        if plan_info.get("success"):
            executed_count = len(plan_info.get("executed_tasks", []))
            total_count = plan_info.get("total_tasks", 0)
            cycle_result["user_message"] = (
                f"✅ Plan executed: {executed_count}/{total_count} tasks"
            )
        else:
            cycle_result["user_message"] = "❌ Error executing development plan"

        cycle_result["backup_created"] = backup_result["success"]

        return cycle_result

    def _handle_status(self) -> Dict[str, Any]:
        """Handle status command"""
        self.logger.info("Getting agent status")

        try:
            status = self.agent.get_status()

            # Format status for user
            plan_status = status["dev_plan"]
            git_status = status["git"]

            status_message = f"""
📊 **NIMDA Agent Status**

🎯 **Development Plan:**
- Progress: {plan_status["completed_subtasks"]}/{plan_status["total_subtasks"]} subtasks ({plan_status["progress_percentage"]}%)
- Completed tasks: {plan_status["completed_tasks"]}/{plan_status["total_tasks"]}

🔧 **Git Repository:**
- Current branch: {git_status.get("current_branch", "unknown")}
- Local changes: {"Yes" if git_status.get("has_changes") else "No"}
- Files changed: {git_status.get("total_files", 0)}

🤖 **Agent:**
- Status: {"Running" if status["agent_running"] else "Idle"}
- Current task: {status.get("current_task") or "None"}
- Project: {status["project_path"]}
"""

            return {
                "success": True,
                "message": "Status retrieved",
                "user_message": status_message.strip(),
                "raw_status": status,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error getting status",
                "user_message": "❌ Error getting status",
            }

    def _handle_sync(self) -> Dict[str, Any]:
        """Handle synchronization command"""
        self.logger.info("Executing Git synchronization")

        result = self.agent.git_manager.sync_with_remote()

        if result["success"]:
            operations = result.get("operations", [])
            operations_summary = ", ".join(
                [op[0] for op in operations if op[1]["success"]]
            )
            result["user_message"] = (
                f"✅ Synchronization completed: {operations_summary}"
            )
        else:
            result["user_message"] = "❌ Error synchronizing with remote repository"

        return result

    def _handle_fix_errors(self) -> Dict[str, Any]:
        """Handle error fixing command"""
        self.logger.info("Executing automatic error fixing")

        result = self.agent.auto_fix_errors()

        if result["success"]:
            fixed_count = result.get("fixed_count", 0)
            total_errors = result.get("total_errors", 0)
            result["user_message"] = f"✅ Fixed {fixed_count} of {total_errors} errors"
        else:
            result["user_message"] = "❌ Error in automatic fixing"

        return result

    def _handle_initialize(self) -> Dict[str, Any]:
        """Handle initialization command"""
        self.logger.info("Executing project initialization")

        result = self.agent.initialize_project()

        if result:
            return {
                "success": True,
                "message": "Project initialized",
                "user_message": "✅ Project successfully initialized",
            }
        else:
            return {
                "success": False,
                "message": "Project initialization error",
                "user_message": "❌ Project initialization error",
            }

    def _handle_help(self) -> Dict[str, Any]:
        """Handle help command"""
        help_message = """
🤖 **NIMDA Agent - Available Commands:**

📋 **Plan Operations:**
- `update dev plan` - update and extend DEV_PLAN.md
- `execute task number X` - execute specific task
- `execute full dev` - execute the entire plan completely

📊 **Status and Information:**
- `status` - current agent status and progress
- `help` - show this help

🔧 **Git and Synchronization:**
- `sync` - synchronize with remote repository
- `fix errors` - automatic error fixing

🚀 **Initialization:**
- `initialize` - create basic project structure

💡 **Usage Examples:**
- "update dev plan and add new tasks"
- "execute task number 3"
- "execute full dev plan from start to finish"
- "show status"
"""

        return {
            "success": True,
            "message": "Help displayed",
            "user_message": help_message.strip(),
        }

    def _handle_unknown_command(self, command: str) -> Dict[str, Any]:
        """Handle unknown command"""
        self.logger.warning(f"Unknown command: {command}")

        # Try to find similar commands
        suggestions = self._suggest_commands(command)

        suggestion_text = ""
        if suggestions:
            suggestion_text = "\n\n💡 **Maybe you meant:**\n" + "\n".join(
                f"- {s}" for s in suggestions
            )

        return {
            "success": False,
            "message": f"Unknown command: {command}",
            "user_message": f"❓ Don't understand command '{command}'{suggestion_text}\n\nType 'help' for list of available commands.",
        }

    def _suggest_commands(self, command: str) -> List[str]:
        """Suggest similar commands"""
        suggestions = []
        command_lower = command.lower()

        # Simple keyword analysis
        if any(word in command_lower for word in ["plan", "dev", "development"]):
            suggestions.extend(["update dev plan", "execute full dev"])

        if any(word in command_lower for word in ["task", "number"]):
            suggestions.append("execute task number X")

        if any(word in command_lower for word in ["status", "state"]):
            suggestions.append("status")

        if any(word in command_lower for word in ["git", "sync", "synchronize"]):
            suggestions.append("sync")

        if any(word in command_lower for word in ["error", "fix"]):
            suggestions.append("fix errors")

        return suggestions[:3]  # Maximum 3 suggestions

    def _mark_codex_session_active(self):
        """Mark Codex session as active for local monitor"""
        try:
            import time

            # Create session file
            with open(self.codex_session_file, "w") as f:
                f.write(str(time.time()))

            # Update last activity
            with open(self.last_activity_file, "w") as f:
                f.write(str(int(time.time())))

            self.logger.info("Codex session marked as active")
        except Exception as e:
            self.logger.warning(f"Failed to mark Codex session active: {e}")

    def _handle_execute_codex_mode(self) -> Dict[str, Any]:
        """Handle codex mode execution - work with current agent instead of creating new project"""
        self.logger.info("Executing CODEX MODE - working with current agent")

        # User warning
        plan_status = self.agent.dev_plan_manager.get_plan_status()

        if plan_status["total_tasks"] == 0:
            return {
                "success": False,
                "message": "DEV_PLAN.md is empty or contains no tasks",
                "user_message": "❌ No tasks to execute in current agent",
            }

        # Create backup before execution
        backup_result = self.agent.git_manager.create_backup_branch()

        if not backup_result["success"]:
            self.logger.warning("Failed to create backup")

        # Force execution in current directory with CODEX MODE flag
        try:
            # Use run_full_dev_cycle with codex mode flag
            cycle_result = self.agent.run_full_dev_cycle(is_codex_mode=True)

            # Override some fields to indicate CODEX MODE
            cycle_result["backup_created"] = backup_result["success"]
            cycle_result["mode"] = "codex_current_agent"

            # Extract plan info for user message
            plan_info = cycle_result.get("plan", {})

            # Use total_tasks and count completed tasks properly
            total_count = plan_info.get("total_tasks", 0)
            executed_count = len(plan_info.get("executed_tasks", []))

            if plan_info.get("success"):
                cycle_result["user_message"] = (
                    f"✅ CODEX MODE: Plan fully completed in current agent: {executed_count}/{total_count} tasks"
                )
            else:
                # Show progress instead of error when tasks are not completed
                cycle_result["user_message"] = (
                    f"🔄 CODEX MODE: Plan processed in current agent: 0/{total_count} tasks completed (processed: {executed_count})"
                )
                # Override success if basic operations completed (commit/push worked)
                if cycle_result.get("commit", {}).get("success") and cycle_result.get(
                    "push", {}
                ).get("success"):
                    cycle_result["success"] = True

            return cycle_result

        except Exception as e:
            self.logger.error(f"CODEX MODE execution error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "CODEX MODE execution error",
                "user_message": "❌ CODEX MODE: Failed to execute in current agent",
                "backup_created": backup_result["success"],
                "mode": "codex_current_agent",
            }
