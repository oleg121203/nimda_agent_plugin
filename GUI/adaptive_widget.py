#!/usr/bin/env python3
"""
NIMDA Agent - Adaptive Widget
Universal widget for dynamic child windows with self-adjustment capabilities
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class WidgetType(Enum):
    """Types of adaptive widgets"""

    LOG_VIEWER = "log_viewer"
    STATUS_DISPLAY = "status_display"
    ANALYSIS_VIEWER = "analysis_viewer"
    CHAT_WINDOW = "chat_window"
    PROGRESS_TRACKER = "progress_tracker"
    SYSTEM_MONITOR = "system_monitor"


@dataclass
class WidgetConfig:
    """Configuration for adaptive widgets"""

    widget_type: WidgetType
    title: str
    auto_update: bool = True
    update_interval: int = 1000  # milliseconds
    max_lines: int = 1000
    word_wrap: bool = True
    font_size: int = 10
    theme: str = "default"
    scrollable: bool = True
    resizable: bool = True


class AdaptiveLogViewer(QWidget):
    """Log viewer widget with auto-scroll and filtering"""

    log_updated = Signal(str)

    def __init__(self, config: WidgetConfig):
        super().__init__()
        self.config = config
        self.log_entries: List[str] = []
        self._setup_ui()
        self._setup_auto_update()

    def _setup_ui(self):
        """Setup log viewer UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel(self.config.title)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Courier New", self.config.font_size))
        self.log_display.setWordWrapMode(
            QTextEdit.WrapMode.WordWrap
            if self.config.word_wrap
            else QTextEdit.WrapMode.NoWrap
        )
        layout.addWidget(self.log_display)

        # Controls
        controls_layout = QHBoxLayout()

        clear_btn = QPushButton("🗑️ Очистити")
        clear_btn.clicked.connect(self.clear_logs)
        controls_layout.addWidget(clear_btn)

        export_btn = QPushButton("💾 Експорт")
        export_btn.clicked.connect(self.export_logs)
        controls_layout.addWidget(export_btn)

        controls_layout.addStretch()

        auto_scroll_btn = QPushButton("⬇️ Авто-скрол")
        auto_scroll_btn.setCheckable(True)
        auto_scroll_btn.setChecked(True)
        auto_scroll_btn.clicked.connect(self._toggle_auto_scroll)
        controls_layout.addWidget(auto_scroll_btn)

        layout.addLayout(controls_layout)

        self.auto_scroll = True

    def _setup_auto_update(self):
        """Setup auto-update timer"""
        if self.config.auto_update:
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self._refresh_display)
            self.update_timer.start(self.config.update_interval)

    def add_log_entry(self, entry: str, timestamp: bool = True):
        """Add new log entry"""
        from datetime import datetime

        if timestamp:
            timestamp_str = datetime.now().strftime("[%H:%M:%S]")
            formatted_entry = f"{timestamp_str} {entry}"
        else:
            formatted_entry = entry

        self.log_entries.append(formatted_entry)

        # Limit max lines
        if len(self.log_entries) > self.config.max_lines:
            self.log_entries = self.log_entries[-self.config.max_lines :]

        self._refresh_display()
        self.log_updated.emit(formatted_entry)

    def _refresh_display(self):
        """Refresh log display"""
        self.log_display.clear()
        for entry in self.log_entries:
            self.log_display.append(entry)

        if self.auto_scroll:
            cursor = self.log_display.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.log_display.setTextCursor(cursor)

    def _toggle_auto_scroll(self, checked: bool):
        """Toggle auto-scroll"""
        self.auto_scroll = checked

    def clear_logs(self):
        """Clear all logs"""
        self.log_entries.clear()
        self.log_display.clear()

    def export_logs(self):
        """Export logs to file (placeholder)"""
        # Would implement file dialog and export
        pass


class AdaptiveStatusDisplay(QWidget):
    """Status display widget with real-time updates"""

    status_changed = Signal(str, str)  # category, status

    def __init__(self, config: WidgetConfig):
        super().__init__()
        self.config = config
        self.status_items: Dict[str, Dict[str, Any]] = {}
        self._setup_ui()
        self._setup_auto_update()

    def _setup_ui(self):
        """Setup status display UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel(self.config.title)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # Status area
        self.status_area = QScrollArea()
        self.status_widget = QWidget()
        self.status_layout = QVBoxLayout(self.status_widget)

        self.status_area.setWidget(self.status_widget)
        self.status_area.setWidgetResizable(True)
        layout.addWidget(self.status_area)

        # Refresh button
        refresh_btn = QPushButton("🔄 Оновити")
        refresh_btn.clicked.connect(self._refresh_status)
        layout.addWidget(refresh_btn)

    def _setup_auto_update(self):
        """Setup auto-update timer"""
        if self.config.auto_update:
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self._refresh_status)
            self.update_timer.start(self.config.update_interval)

    def add_status_item(
        self, category: str, status: str, details: str = "", color: str = "green"
    ):
        """Add or update status item"""
        self.status_items[category] = {
            "status": status,
            "details": details,
            "color": color,
            "updated": True,
        }
        self._update_display()
        self.status_changed.emit(category, status)

    def _update_display(self):
        """Update status display"""
        # Clear existing items
        for i in reversed(range(self.status_layout.count())):
            child = self.status_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        # Add status items
        for category, info in self.status_items.items():
            item_widget = self._create_status_item(category, info)
            self.status_layout.addWidget(item_widget)

        # Add stretch
        self.status_layout.addStretch()

    def _create_status_item(self, category: str, info: Dict[str, Any]) -> QWidget:
        """Create status item widget"""
        item = QWidget()
        layout = QHBoxLayout(item)

        # Status indicator
        indicator = QLabel("●")
        color_map = {
            "green": "#00ff00",
            "red": "#ff0000",
            "yellow": "#ffff00",
            "blue": "#0000ff",
            "gray": "#808080",
        }
        color = color_map.get(info["color"], "#00ff00")
        indicator.setStyleSheet(f"color: {color}; font-size: 16px;")
        layout.addWidget(indicator)

        # Category
        category_label = QLabel(category)
        category_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(category_label)

        # Status
        status_label = QLabel(info["status"])
        layout.addWidget(status_label)

        layout.addStretch()

        # Details tooltip
        if info["details"]:
            item.setToolTip(info["details"])

        return item

    def _refresh_status(self):
        """Refresh status display"""
        self._update_display()


class AdaptiveAnalysisViewer(QWidget):
    """Analysis results viewer with tabbed interface"""

    def __init__(self, config: WidgetConfig):
        super().__init__()
        self.config = config
        self.analysis_data: Dict[str, Any] = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup analysis viewer UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel(self.config.title)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # Tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Add default tabs
        self._add_overview_tab()
        self._add_details_tab()
        self._add_recommendations_tab()

    def _add_overview_tab(self):
        """Add overview tab"""
        overview_widget = QWidget()
        layout = QVBoxLayout(overview_widget)

        self.overview_display = QTextEdit()
        self.overview_display.setReadOnly(True)
        layout.addWidget(self.overview_display)

        self.tab_widget.addTab(overview_widget, "📊 Огляд")

    def _add_details_tab(self):
        """Add details tab"""
        details_widget = QWidget()
        layout = QVBoxLayout(details_widget)

        self.details_display = QTextEdit()
        self.details_display.setReadOnly(True)
        layout.addWidget(self.details_display)

        self.tab_widget.addTab(details_widget, "🔍 Деталі")

    def _add_recommendations_tab(self):
        """Add recommendations tab"""
        recommendations_widget = QWidget()
        layout = QVBoxLayout(recommendations_widget)

        self.recommendations_display = QTextEdit()
        self.recommendations_display.setReadOnly(True)
        layout.addWidget(self.recommendations_display)

        self.tab_widget.addTab(recommendations_widget, "💡 Рекомендації")

    def update_analysis(self, analysis_data: Dict[str, Any]):
        """Update analysis data"""
        self.analysis_data = analysis_data
        self._refresh_all_tabs()

    def _refresh_all_tabs(self):
        """Refresh all tabs with latest data"""
        self._refresh_overview()
        self._refresh_details()
        self._refresh_recommendations()

    def _refresh_overview(self):
        """Refresh overview tab"""
        if not self.analysis_data:
            return

        overview_text = "📊 Аналіз Проекту\n\n"

        if "structure" in self.analysis_data:
            structure = self.analysis_data["structure"]
            overview_text += f"📁 Файлів: {structure.get('total_files', 0)}\n"
            overview_text += (
                f"🐍 Python файлів: {len(structure.get('python_files', []))}\n"
            )
            overview_text += (
                f"📂 Директорій: {structure.get('total_directories', 0)}\n\n"
            )

        if "metrics" in self.analysis_data:
            metrics = self.analysis_data["metrics"]
            overview_text += f"📊 Ліній коду: {metrics.get('total_lines', 0)}\n"
            overview_text += f"🔧 Функцій: {metrics.get('total_functions', 0)}\n"
            overview_text += f"🏗️ Класів: {metrics.get('total_classes', 0)}\n\n"

        if "issues" in self.analysis_data:
            issues = self.analysis_data["issues"]
            overview_text += f"🚨 Проблем: {len(issues)}\n"

        self.overview_display.setText(overview_text)

    def _refresh_details(self):
        """Refresh details tab"""
        if not self.analysis_data:
            return

        details_text = "🔍 Детальний Аналіз\n\n"

        # Add detailed information from analysis
        for key, value in self.analysis_data.items():
            if isinstance(value, dict):
                details_text += f"📋 {key.upper()}:\n"
                for subkey, subvalue in value.items():
                    details_text += f"  • {subkey}: {subvalue}\n"
                details_text += "\n"

        self.details_display.setText(details_text)

    def _refresh_recommendations(self):
        """Refresh recommendations tab"""
        if not self.analysis_data:
            return

        recommendations_text = "💡 Рекомендації\n\n"

        if "recommendations" in self.analysis_data:
            recommendations = self.analysis_data["recommendations"]
            for i, rec in enumerate(recommendations, 1):
                recommendations_text += f"{i}. {rec.get('title', 'Рекомендація')}\n"
                recommendations_text += f"   {rec.get('description', '')}\n"
                if "actions" in rec:
                    recommendations_text += "   Дії:\n"
                    for action in rec["actions"]:
                        recommendations_text += f"   • {action}\n"
                recommendations_text += "\n"

        self.recommendations_display.setText(recommendations_text)


class AdaptiveProgressTracker(QWidget):
    """Progress tracker widget for monitoring operations"""

    progress_updated = Signal(int, str)

    def __init__(self, config: WidgetConfig):
        super().__init__()
        self.config = config
        self.current_progress = 0
        self.tasks: List[Dict[str, Any]] = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup progress tracker UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel(self.config.title)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # Main progress bar
        self.main_progress = QProgressBar()
        self.main_progress.setRange(0, 100)
        layout.addWidget(self.main_progress)

        # Current task label
        self.current_task_label = QLabel("Готово до роботи")
        layout.addWidget(self.current_task_label)

        # Task list
        self.task_area = QScrollArea()
        self.task_widget = QWidget()
        self.task_layout = QVBoxLayout(self.task_widget)

        self.task_area.setWidget(self.task_widget)
        self.task_area.setWidgetResizable(True)
        layout.addWidget(self.task_area)

    def set_progress(self, progress: int, message: str = ""):
        """Set main progress"""
        self.current_progress = progress
        self.main_progress.setValue(progress)
        if message:
            self.current_task_label.setText(message)
        self.progress_updated.emit(progress, message)

    def add_task(self, task_name: str, status: str = "pending"):
        """Add task to tracker"""
        task = {"name": task_name, "status": status, "widget": None}
        self.tasks.append(task)
        self._update_task_display()

    def update_task_status(self, task_name: str, status: str):
        """Update task status"""
        for task in self.tasks:
            if task["name"] == task_name:
                task["status"] = status
                self._update_task_display()
                break

    def _update_task_display(self):
        """Update task display"""
        # Clear existing widgets
        for i in reversed(range(self.task_layout.count())):
            child = self.task_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        # Add task widgets
        for task in self.tasks:
            task_widget = self._create_task_widget(task)
            self.task_layout.addWidget(task_widget)

        self.task_layout.addStretch()

    def _create_task_widget(self, task: Dict[str, Any]) -> QWidget:
        """Create task widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Status indicator
        status_map = {
            "pending": ("⏳", "gray"),
            "running": ("🔄", "blue"),
            "completed": ("✅", "green"),
            "failed": ("❌", "red"),
        }

        status_icon, color = status_map.get(task["status"], ("❓", "gray"))

        indicator = QLabel(status_icon)
        indicator.setStyleSheet(f"font-size: 16px;")
        layout.addWidget(indicator)

        # Task name
        name_label = QLabel(task["name"])
        layout.addWidget(name_label)

        layout.addStretch()

        return widget


class AdaptiveWidget(QWidget):
    """Main adaptive widget that can switch between different types"""

    def __init__(self, config: WidgetConfig):
        super().__init__()
        self.config = config
        self.current_widget = None
        self._setup_ui()
        self._create_content_widget()

    def _setup_ui(self):
        """Setup main UI"""
        self.main_layout = QVBoxLayout(self)

        # Apply theme
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

    def _create_content_widget(self):
        """Create appropriate content widget based on type"""
        if self.current_widget:
            self.current_widget.setParent(None)

        if self.config.widget_type == WidgetType.LOG_VIEWER:
            self.current_widget = AdaptiveLogViewer(self.config)
        elif self.config.widget_type == WidgetType.STATUS_DISPLAY:
            self.current_widget = AdaptiveStatusDisplay(self.config)
        elif self.config.widget_type == WidgetType.ANALYSIS_VIEWER:
            self.current_widget = AdaptiveAnalysisViewer(self.config)
        elif self.config.widget_type == WidgetType.PROGRESS_TRACKER:
            self.current_widget = AdaptiveProgressTracker(self.config)
        else:
            # Default text widget
            self.current_widget = QTextEdit()
            self.current_widget.setPlaceholderText(
                f"Adaptive Widget: {self.config.widget_type.value}"
            )

        self.main_layout.addWidget(self.current_widget)

    def change_type(self, new_type: WidgetType):
        """Change widget type dynamically"""
        self.config.widget_type = new_type
        self._create_content_widget()

    def get_content_widget(self):
        """Get the current content widget"""
        return self.current_widget


# Factory function for creating adaptive widgets
def create_adaptive_widget(
    widget_type: WidgetType, title: str, **kwargs
) -> AdaptiveWidget:
    """
    Factory function to create adaptive widgets

    Args:
        widget_type: Type of widget to create
        title: Widget title
        **kwargs: Additional configuration options

    Returns:
        Configured AdaptiveWidget
    """
    config = WidgetConfig(widget_type=widget_type, title=title, **kwargs)
    return AdaptiveWidget(config)
