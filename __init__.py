"""
NIMDA Agent Plugin - Універсальний автономний агент розробки
Може бути доданий до будь-якого проекту як окремий плагін.
"""

# Версія плагіна
__version__ = "1.0.0"
__author__ = "NIMDA Development Team"

# Список компонентів що будуть доступні при імпорті
__all__ = [
    'NIMDAAgent',
    'CommandProcessor',
    'DevPlanManager',
    'GitManager',
    'ProjectInitializer',
    'ChangelogManager'
]

# Lazy import для уникнення циклічних залежностей
def get_nimda_agent():
    """Отримати клас NIMDAAgent"""
    from .agent import NIMDAAgent
    return NIMDAAgent

def get_command_processor():
    """Отримати клас CommandProcessor"""
    from .command_processor import CommandProcessor
    return CommandProcessor

def get_dev_plan_manager():
    """Отримати клас DevPlanManager"""
    from .dev_plan_manager import DevPlanManager
    return DevPlanManager

def get_git_manager():
    """Отримати клас GitManager"""
    from .git_manager import GitManager
    return GitManager

def get_project_initializer():
    """Отримати клас ProjectInitializer"""
    from .project_initializer import ProjectInitializer
    return ProjectInitializer

def get_changelog_manager():
    """Отримати клас ChangelogManager"""
    from .changelog_manager import ChangelogManager
    return ChangelogManager

# Головна функція для зручного запуску
def run_agent(project_path=None, command=None):
    """
    Зручна функція для запуску NIMDA Agent

    Args:
        project_path: Шлях до проекту
        command: Команда для виконання

    Returns:
        Результат виконання або агент для подальшої роботи
    """
    agent_class = get_nimda_agent()
    agent = agent_class(project_path)

    if command:
        return agent.process_command(command)
    else:
        return agent
