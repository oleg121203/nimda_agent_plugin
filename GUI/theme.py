#!/usr/bin/env python3
"""
NIMDA Agent - GUI Theme
Dark hacker-style theme with Matrix-inspired elements
"""

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect, Qt, QTimer
from PySide6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPainter, QPalette
from PySide6.QtWidgets import QApplication, QWidget


class MatrixAnimation(QWidget):
    """Matrix-style digital rain animation for background"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 1400, 900)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Animation setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # Update every 100ms

        # Matrix characters
        self.matrix_chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        self.columns = []
        self.init_columns()

    def init_columns(self):
        """Initialize matrix columns"""
        column_width = 20
        num_columns = self.width() // column_width

        for i in range(num_columns):
            column = {
                "x": i * column_width,
                "drops": [],
                "speed": 1 + (i % 3),  # Varying speeds
            }

            # Initialize some drops
            for j in range(3):
                drop = {
                    "y": j * 50,
                    "char": self.matrix_chars[j % len(self.matrix_chars)],
                    "alpha": 255 - (j * 80),
                }
                column["drops"].append(drop)

            self.columns.append(column)

    def paintEvent(self, event):
        """Paint matrix rain effect"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dark background with subtle gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 100))
        gradient.setColorAt(1, QColor(0, 20, 0, 150))
        painter.fillRect(self.rect(), QBrush(gradient))

        # Draw matrix characters
        font = QFont("Courier", 12, QFont.Bold)
        painter.setFont(font)

        for column in self.columns:
            for drop in column["drops"]:
                color = QColor(0, 255, 70, drop["alpha"])
                painter.setPen(color)
                painter.drawText(column["x"], drop["y"], drop["char"])

                # Move drop down
                drop["y"] += column["speed"]

                # Reset drop if it goes off screen
                if drop["y"] > self.height():
                    drop["y"] = -50
                    drop["char"] = self.matrix_chars[
                        hash(drop["y"]) % len(self.matrix_chars)
                    ]
                    drop["alpha"] = 255


class NIMDATheme:
    """NIMDA Agent dark hacker theme"""

    def __init__(self):
        self.primary_color = QColor(0, 255, 70)  # Matrix green
        self.secondary_color = QColor(0, 150, 255)  # Cyber blue
        self.background_color = QColor(15, 15, 15)  # Dark background
        self.surface_color = QColor(25, 25, 25)  # Card background
        self.text_color = QColor(220, 220, 220)  # Light text
        self.accent_color = QColor(255, 165, 0)  # Warning orange

        self.font_family = "Fira Code"  # Monospace font
        self.font_size = 10

        self.stylesheet = self._create_stylesheet()

    def _create_stylesheet(self) -> str:
        """Create comprehensive QSS stylesheet"""
        return f"""
        /* Main window styling */
        QMainWindow {{
            background-color: {self.background_color.name()};
            color: {self.text_color.name()};
            font-family: '{self.font_family}', 'Courier New', monospace;
            font-size: {self.font_size}pt;
        }}
        
        /* Group boxes */
        QGroupBox {{
            background-color: {self.surface_color.name()};
            border: 2px solid {self.primary_color.name()};
            border-radius: 8px;
            margin-top: 1ex;
            padding-top: 15px;
            font-weight: bold;
            color: {self.primary_color.name()};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            color: {self.primary_color.name()};
            font-weight: bold;
            font-size: 12pt;
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 {self.surface_color.lighter(120).name()},
                                            stop: 1 {self.surface_color.name()});
            border: 2px solid {self.primary_color.name()};
            border-radius: 6px;
            padding: 8px 16px;
            color: {self.text_color.name()};
            font-weight: bold;
            font-size: 11pt;
        }}
        
        QPushButton:hover {{
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 {self.primary_color.darker(200).name()},
                                            stop: 1 {self.surface_color.lighter(150).name()});
            border-color: {self.secondary_color.name()};
            color: {self.secondary_color.name()};
        }}
        
        QPushButton:pressed {{
            background-color: {self.primary_color.darker(300).name()};
            border-color: {self.accent_color.name()};
        }}
        
        QPushButton:disabled {{
            background-color: {self.surface_color.darker(150).name()};
            border-color: {QColor(100, 100, 100).name()};
            color: {QColor(120, 120, 120).name()};
        }}
        
        /* Special styling for improvement buttons */
        QPushButton[text*="📋"] {{
            border-color: {self.secondary_color.name()};
            color: {self.secondary_color.name()};
        }}
        
        QPushButton[text*="🧠"] {{
            border-color: {self.accent_color.name()};
            color: {self.accent_color.name()};
        }}
        
        QPushButton[text*="⚡"] {{
            border-color: {QColor(255, 50, 50).name()};
            color: {QColor(255, 100, 100).name()};
            font-weight: bold;
        }}
        
        /* Text areas */
        QTextEdit {{
            background-color: {self.background_color.darker(120).name()};
            border: 1px solid {self.primary_color.darker(200).name()};
            border-radius: 4px;
            padding: 8px;
            color: {self.text_color.name()};
            font-family: '{self.font_family}', 'Courier New', monospace;
            font-size: {self.font_size}pt;
            selection-background-color: {self.primary_color.darker(300).name()};
        }}
        
        QTextEdit:focus {{
            border-color: {self.primary_color.name()};
            background-color: {self.background_color.name()};
        }}
        
        /* Labels */
        QLabel {{
            color: {self.text_color.name()};
            font-family: '{self.font_family}', 'Courier New', monospace;
        }}
        
        /* Progress bars */
        QProgressBar {{
            background-color: {self.surface_color.name()};
            border: 2px solid {self.primary_color.darker(200).name()};
            border-radius: 4px;
            text-align: center;
            color: {self.text_color.name()};
            font-weight: bold;
        }}
        
        QProgressBar::chunk {{
            background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                            stop: 0 {self.primary_color.name()},
                                            stop: 1 {self.secondary_color.name()});
            border-radius: 2px;
        }}
        
        /* Tab widget */
        QTabWidget::pane {{
            border: 1px solid {self.primary_color.darker(200).name()};
            background-color: {self.surface_color.name()};
        }}
        
        QTabBar::tab {{
            background-color: {self.surface_color.darker(120).name()};
            border: 1px solid {self.primary_color.darker(200).name()};
            padding: 8px 16px;
            margin-right: 2px;
            color: {self.text_color.name()};
        }}
        
        QTabBar::tab:selected {{
            background-color: {self.surface_color.name()};
            border-bottom-color: {self.primary_color.name()};
            color: {self.primary_color.name()};
            font-weight: bold;
        }}
        
        QTabBar::tab:hover {{
            background-color: {self.surface_color.lighter(120).name()};
            color: {self.secondary_color.name()};
        }}
        
        /* Status bar */
        QStatusBar {{
            background-color: {self.surface_color.name()};
            border-top: 1px solid {self.primary_color.darker(200).name()};
            color: {self.text_color.name()};
        }}
        
        /* Splitter */
        QSplitter::handle {{
            background-color: {self.primary_color.darker(300).name()};
            width: 3px;
            height: 3px;
        }}
        
        QSplitter::handle:hover {{
            background-color: {self.primary_color.name()};
        }}
        
        /* Scrollbars */
        QScrollBar:vertical {{
            background-color: {self.surface_color.name()};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {self.primary_color.darker(200).name()};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {self.primary_color.name()};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* Dialog boxes */
        QDialog {{
            background-color: {self.background_color.name()};
            color: {self.text_color.name()};
            border: 2px solid {self.primary_color.name()};
            border-radius: 8px;
        }}
        
        QDialogButtonBox QPushButton {{
            min-width: 80px;
            padding: 6px 12px;
        }}
        
        /* Message boxes */
        QMessageBox {{
            background-color: {self.background_color.name()};
            color: {self.text_color.name()};
        }}
        
        QMessageBox QPushButton {{
            min-width: 60px;
        }}
        """

    def apply_theme(self, widget: QWidget):
        """Apply theme to widget"""
        widget.setStyleSheet(self.stylesheet)

        # Set application palette for better consistency
        palette = QPalette()

        # Window colors
        palette.setColor(QPalette.Window, self.background_color)
        palette.setColor(QPalette.WindowText, self.text_color)

        # Base colors (for input widgets)
        palette.setColor(QPalette.Base, self.background_color.darker(120))
        palette.setColor(QPalette.AlternateBase, self.surface_color)

        # Text colors
        palette.setColor(QPalette.Text, self.text_color)
        palette.setColor(QPalette.PlaceholderText, self.text_color.darker(150))

        # Button colors
        palette.setColor(QPalette.Button, self.surface_color)
        palette.setColor(QPalette.ButtonText, self.text_color)

        # Highlight colors
        palette.setColor(QPalette.Highlight, self.primary_color.darker(200))
        palette.setColor(QPalette.HighlightedText, self.text_color)

        # Apply palette
        widget.setPalette(palette)

    def get_font(self, size: int = None, bold: bool = False) -> QFont:
        """Get themed font"""
        font = QFont(self.font_family, size or self.font_size)
        if bold:
            font.setBold(True)
        return font

    def get_color(self, color_name: str) -> QColor:
        """Get color by name"""
        colors = {
            "primary": self.primary_color,
            "secondary": self.secondary_color,
            "background": self.background_color,
            "surface": self.surface_color,
            "text": self.text_color,
            "accent": self.accent_color,
        }
        return colors.get(color_name, self.text_color)

    def create_matrix_background(self, parent: QWidget) -> MatrixAnimation:
        """Create Matrix-style animated background"""
        matrix_bg = MatrixAnimation(parent)
        matrix_bg.show()
        matrix_bg.lower()  # Put behind other widgets
        return matrix_bg
