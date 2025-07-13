"""NIMDA Agent Plugin - Universal autonomous development agent.
Can be added to any project as a standalone plugin."""

# Plugin version
__version__ = "1.0.0"
__author__ = "NIMDA Development Team"

# Components exported on import
__all__ = [
    'NIMDAAgent',
    'CommandProcessor',
    'DevPlanManager',
    'GitManager',
    'ProjectInitializer',
    'ChangelogManager'
]

# Lazy imports to avoid circular dependencies
def get_nimda_agent():
    """Get the NIMDAAgent class"""
    from .agent import NIMDAAgent
    return NIMDAAgent

def get_command_processor():
    """Get the CommandProcessor class"""
    from .command_processor import CommandProcessor
    return CommandProcessor

def get_dev_plan_manager():
    """Get the DevPlanManager class"""
    from .dev_plan_manager import DevPlanManager
    return DevPlanManager

def get_git_manager():
    """Get the GitManager class"""
    from .git_manager import GitManager
    return GitManager

def get_project_initializer():
    """Get the ProjectInitializer class"""
    from .project_initializer import ProjectInitializer
    return ProjectInitializer

def get_changelog_manager():
    """Get the ChangelogManager class"""
    from .changelog_manager import ChangelogManager
    return ChangelogManager

# Convenience function for running the agent
def run_agent(project_path=None, command=None):
    """Simple helper to run NIMDA Agent

    Args:
        project_path: Path to the project
        command: Command to execute

    Returns:
        Execution result or the agent instance
    """
    agent_class = get_nimda_agent()
    agent = agent_class(project_path)

    if command:
        return agent.process_command(command)
    else:
        return agent
