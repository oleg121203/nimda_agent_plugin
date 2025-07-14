#!/usr/bin/env python3
"""
NIMDA Agent - GUI Controller
Central API for GUI manipulation and window management
"""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PySide6.QtCore import QObject, QThread, QTimer, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox, QWidget


@dataclass
class WindowConfig:
    """Configuration for adaptive windows"""

    title: str
    width: int = 400
    height: int = 300
    x: int = 100
    y: int = 100
    resizable: bool = True
    always_on_top: bool = False
    content_type: str = "text"  # text, log, status, analysis
    auto_scroll: bool = True
    theme: str = "default"


class AdaptiveWindow(QWidget):
    """Dynamic window that can be controlled by agents"""

    content_updated = Signal(str, str)  # window_id, content
    window_closed = Signal(str)  # window_id

    def __init__(self, window_id: str, config: WindowConfig):
        super().__init__()
        self.window_id = window_id
        self.config = config
        self.content = ""

        self._setup_window()
        self._apply_theme()

    def _setup_window(self):
        """Setup window properties"""
        self.setWindowTitle(self.config.title)
        self.setGeometry(
            self.config.x, self.config.y, self.config.width, self.config.height
        )

        if not self.config.resizable:
            self.setFixedSize(self.config.width, self.config.height)

        if self.config.always_on_top:
            self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def _apply_theme(self):
        """Apply theme based on configuration"""
        if self.config.theme == "matrix":
            self.setStyleSheet("""
                QWidget {
                    background-color: #0f0f0f;
                    color: #00ff46;
                    font-family: 'Courier New', monospace;
                }
            """)
        elif self.config.theme == "cyber":
            self.setStyleSheet("""
                QWidget {
                    background-color: #1a1a2e;
                    color: #0096ff;
                    font-family: 'Fira Code', monospace;
                }
            """)

    def update_content(self, content: str):
        """Update window content"""
        self.content = content
        self.content_updated.emit(self.window_id, content)

    def append_content(self, content: str):
        """Append content to existing"""
        self.content += content
        self.content_updated.emit(self.window_id, self.content)

    def closeEvent(self, event):
        """Handle window close event"""
        self.window_closed.emit(self.window_id)
        super().closeEvent(event)


class GUIController(QObject):
    """Central controller for GUI operations"""

    window_created = Signal(str, WindowConfig)
    window_updated = Signal(str, str)
    window_closed = Signal(str)
    status_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.windows: Dict[str, AdaptiveWindow] = {}
        self.main_window = None
        self.app = None
        self.window_counter = 0

        # Initialize application if not exists
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
            self.app.setApplicationName("NIMDA Agent")

    def set_main_window(self, main_window):
        """Set reference to main window"""
        self.main_window = main_window

    def create_window(self, config: WindowConfig, window_id: str = None) -> str:
        """
        Create a new adaptive window

        Args:
            config: Window configuration
            window_id: Optional window ID, auto-generated if not provided

        Returns:
            Window ID for future operations
        """
        if window_id is None:
            self.window_counter += 1
            window_id = f"window_{self.window_counter}"

        # Create window
        window = AdaptiveWindow(window_id, config)

        # Connect signals
        window.content_updated.connect(self.window_updated.emit)
        window.window_closed.connect(self._handle_window_closed)

        # Store and show
        self.windows[window_id] = window
        window.show()

        self.window_created.emit(window_id, config)
        self.status_changed.emit(f"Created window: {config.title}")

        return window_id

    def resize_window(self, window_id: str, width: int, height: int) -> bool:
        """
        Resize window

        Args:
            window_id: Window identifier
            width: New width
            height: New height

        Returns:
            True if successful
        """
        if window_id not in self.windows:
            return False

        window = self.windows[window_id]
        window.resize(width, height)
        window.config.width = width
        window.config.height = height

        self.status_changed.emit(f"Resized window {window_id}: {width}x{height}")
        return True

    def move_window(self, window_id: str, x: int, y: int) -> bool:
        """
        Move window to new position

        Args:
            window_id: Window identifier
            x: New X coordinate
            y: New Y coordinate

        Returns:
            True if successful
        """
        if window_id not in self.windows:
            return False

        window = self.windows[window_id]
        window.move(x, y)
        window.config.x = x
        window.config.y = y

        self.status_changed.emit(f"Moved window {window_id}: ({x}, {y})")
        return True

    def update_content(self, window_id: str, content: str) -> bool:
        """
        Update window content

        Args:
            window_id: Window identifier
            content: New content

        Returns:
            True if successful
        """
        if window_id not in self.windows:
            return False

        window = self.windows[window_id]
        window.update_content(content)

        return True

    def append_content(self, window_id: str, content: str) -> bool:
        """
        Append content to window

        Args:
            window_id: Window identifier
            content: Content to append

        Returns:
            True if successful
        """
        if window_id not in self.windows:
            return False

        window = self.windows[window_id]
        window.append_content(content)

        return True

    def close_window(self, window_id: str) -> bool:
        """
        Close window

        Args:
            window_id: Window identifier

        Returns:
            True if successful
        """
        if window_id not in self.windows:
            return False

        window = self.windows[window_id]
        window.close()

        return True

    def get_window_info(self, window_id: str) -> Optional[Dict[str, Any]]:
        """
        Get window information

        Args:
            window_id: Window identifier

        Returns:
            Window information dict or None
        """
        if window_id not in self.windows:
            return None

        window = self.windows[window_id]
        return {
            "id": window_id,
            "title": window.config.title,
            "size": (window.width(), window.height()),
            "position": (window.x(), window.y()),
            "visible": window.isVisible(),
            "content_length": len(window.content),
            "content_type": window.config.content_type,
        }

    def list_windows(self) -> List[Dict[str, Any]]:
        """
        List all windows

        Returns:
            List of window information
        """
        return [self.get_window_info(window_id) for window_id in self.windows.keys()]

    def _handle_window_closed(self, window_id: str):
        """Handle window close event"""
        if window_id in self.windows:
            del self.windows[window_id]
            self.window_closed.emit(window_id)
            self.status_changed.emit(f"Closed window: {window_id}")

    # Convenience methods for common window types

    def create_log_window(self, title: str, x: int = 100, y: int = 100) -> str:
        """Create a log window with appropriate configuration"""
        config = WindowConfig(
            title=title,
            width=600,
            height=400,
            x=x,
            y=y,
            content_type="log",
            auto_scroll=True,
            theme="matrix",
        )
        return self.create_window(config)

    def create_status_window(self, title: str, x: int = 100, y: int = 100) -> str:
        """Create a status window"""
        config = WindowConfig(
            title=title,
            width=300,
            height=200,
            x=x,
            y=y,
            content_type="status",
            theme="cyber",
            always_on_top=True,
        )
        return self.create_window(config)

    def create_analysis_window(self, title: str, x: int = 100, y: int = 100) -> str:
        """Create an analysis results window"""
        config = WindowConfig(
            title=title,
            width=800,
            height=600,
            x=x,
            y=y,
            content_type="analysis",
            theme="default",
        )
        return self.create_window(config)

    def show_message(self, title: str, message: str, message_type: str = "info"):
        """
        Show message dialog

        Args:
            title: Dialog title
            message: Message text
            message_type: Type of message (info, warning, error, question)
        """
        if message_type == "info":
            QMessageBox.information(self.main_window, title, message)
        elif message_type == "warning":
            QMessageBox.warning(self.main_window, title, message)
        elif message_type == "error":
            QMessageBox.critical(self.main_window, title, message)
        elif message_type == "question":
            return QMessageBox.question(self.main_window, title, message)

    def show_progress_dialog(self, title: str, message: str):
        """Show progress dialog (placeholder for future implementation)"""
        # This would create a progress dialog
        # For now, just show info message
        self.show_message(title, message, "info")

    def get_application(self) -> QApplication:
        """Get QApplication instance"""
        return self.app or QApplication.instance()

    def start_gui_loop(self):
        """Start GUI event loop if not already running"""
        if self.app and not self.app.instance():
            return self.app.exec()
        return 0

    def quit_application(self):
        """Quit application"""
        # Close all windows
        for window_id in list(self.windows.keys()):
            self.close_window(window_id)

        # Quit app
        if self.app:
            self.app.quit()


# Global controller instance
_gui_controller = None


def get_gui_controller() -> GUIController:
    """Get global GUI controller instance"""
    global _gui_controller
    if _gui_controller is None:
        _gui_controller = GUIController()
    return _gui_controller


# Agent Integration API - These functions can be called directly by agents


def agent_create_window(
    title: str,
    width: int = 400,
    height: int = 300,
    content_type: str = "text",
    theme: str = "default",
) -> str:
    """
    Agent API: Create a new window

    Args:
        title: Window title
        width: Window width
        height: Window height
        content_type: Type of content (text, log, status, analysis)
        theme: Theme to apply (default, matrix, cyber)

    Returns:
        Window ID for future operations
    """
    controller = get_gui_controller()
    config = WindowConfig(
        title=title, width=width, height=height, content_type=content_type, theme=theme
    )
    return controller.create_window(config)


def agent_update_window(window_id: str, content: str) -> bool:
    """
    Agent API: Update window content

    Args:
        window_id: Window identifier
        content: New content

    Returns:
        True if successful
    """
    controller = get_gui_controller()
    return controller.update_content(window_id, content)


def agent_append_to_window(window_id: str, content: str) -> bool:
    """
    Agent API: Append content to window

    Args:
        window_id: Window identifier
        content: Content to append

    Returns:
        True if successful
    """
    controller = get_gui_controller()
    return controller.append_content(window_id, content)


def agent_resize_window(window_id: str, width: int, height: int) -> bool:
    """
    Agent API: Resize window

    Args:
        window_id: Window identifier
        width: New width
        height: New height

    Returns:
        True if successful
    """
    controller = get_gui_controller()
    return controller.resize_window(window_id, width, height)


def agent_close_window(window_id: str) -> bool:
    """
    Agent API: Close window

    Args:
        window_id: Window identifier

    Returns:
        True if successful
    """
    controller = get_gui_controller()
    return controller.close_window(window_id)


def agent_show_message(title: str, message: str, message_type: str = "info"):
    """
    Agent API: Show message dialog

    Args:
        title: Dialog title
        message: Message text
        message_type: Type of message (info, warning, error)
    """
    controller = get_gui_controller()
    return controller.show_message(title, message, message_type)


if __name__ == "__main__":
    # Test the GUI controller
    app = QApplication(sys.argv)

    controller = GUIController()

    # Create test window
    test_config = WindowConfig(
        title="Test Window", width=500, height=300, theme="matrix"
    )

    window_id = controller.create_window(test_config)
    controller.update_content(window_id, "🤖 Test content from GUI Controller")

    sys.exit(app.exec())
