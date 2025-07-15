"""
NIMDA Agent Plugin System
Універсальна система плагінів для агента NIMDA
"""

__version__ = "1.0.0"
__author__ = "NIMDA Development Team"

from .base_plugin import BasePlugin
from .dev_plan_executor_plugin import DevPlanExecutorPlugin
from .plugin_manager import PluginManager

__all__ = ["BasePlugin", "PluginManager", "DevPlanExecutorPlugin"]
