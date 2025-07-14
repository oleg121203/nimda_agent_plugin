"""
NIMDA Agent GUI Package
Complete graphical user interface with self-improvement capabilities
"""

from pathlib import Path

# Package information
__version__ = "1.0.0"
__author__ = "NIMDA Project"
__description__ = "Intelligent GUI with self-improvement buttons"

# Package root
GUI_ROOT = Path(__file__).parent

# Check for PySide6 availability
try:
    import PySide6

    PYSIDE6_AVAILABLE = True
    PYSIDE6_VERSION = PySide6.__version__
except ImportError:
    PYSIDE6_AVAILABLE = False
    PYSIDE6_VERSION = None

# Export main components
__all__ = [
    "main_window",
    "theme",
    "gui_controller",
    "adaptive_widget",
    "nimda_gui",
    "PYSIDE6_AVAILABLE",
    "PYSIDE6_VERSION",
]


def check_gui_requirements():
    """Check if GUI requirements are met"""
    requirements = {"PySide6": PYSIDE6_AVAILABLE}

    missing = [req for req, available in requirements.items() if not available]

    return {
        "requirements_met": len(missing) == 0,
        "missing_packages": missing,
        "available_packages": [
            req for req, available in requirements.items() if available
        ],
    }


def get_gui_info():
    """Get GUI package information"""
    return {
        "version": __version__,
        "description": __description__,
        "pyside6_available": PYSIDE6_AVAILABLE,
        "pyside6_version": PYSIDE6_VERSION,
        "requirements": check_gui_requirements(),
    }
