#!/usr/bin/env python3
"""
NIMDA Agent - Main GUI Window
PySide6-based interface with self-improvement buttons
"""

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QThread, QTimer, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# Import system components
try:
    from deep_system_analyzer import DeepSystemAnalyzer
    from dev_plan_manager import DevPlanManager
    from enhanced_interactive_workflow import EnhancedInteractiveWorkflow
    from GUI.gui_controller import GUIController
    from GUI.theme import NIMDATheme
except ImportError as e:
    print(f"Warning: Some GUI components not available: {e}")


class SelfImprovementWorker(QThread):
    """Worker thread for self-improvement operations"""

    progress_updated = Signal(int)
    status_updated = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, improvement_type: str, project_path: Path):
        super().__init__()
        self.improvement_type = improvement_type
        self.project_path = project_path
        self.is_cancelled = False

    def run(self):
        """Execute self-improvement process"""
        try:
            if self.improvement_type == "dev_plan_expansion":
                self._expand_dev_plan()
            elif self.improvement_type == "deep_analysis":
                self._deep_analysis()
            elif self.improvement_type == "full_implementation":
                self._full_implementation()

            if not self.is_cancelled:
                self.finished.emit(True, "Самовдосконалення завершено успішно!")

        except Exception as e:
            self.finished.emit(False, f"Помилка самовдосконалення: {str(e)}")

    def cancel(self):
        """Cancel improvement process"""
        self.is_cancelled = True

    def _expand_dev_plan(self):
        """Expand development plan based on current context"""
        self.status_updated.emit("📋 Аналіз поточного dev plan...")
        self.progress_updated.emit(10)

        if self.is_cancelled:
            return

        dev_manager = DevPlanManager(self.project_path)

        self.status_updated.emit("🔍 Сканування структури проекту...")
        self.progress_updated.emit(30)

        if self.is_cancelled:
            return

        # Load and analyze current plan
        dev_manager.get_plan_status()

        self.status_updated.emit("💡 Генерація нових завдань...")
        self.progress_updated.emit(50)

        if self.is_cancelled:
            return

        # Update and expand plan
        dev_manager.update_and_expand_plan()

        self.status_updated.emit("✅ Розширення dev plan завершено")
        self.progress_updated.emit(100)

    def _deep_analysis(self):
        """Perform deep system analysis with context awareness"""
        self.status_updated.emit("🧠 Ініціалізація глибокого аналізу...")
        self.progress_updated.emit(5)

        if self.is_cancelled:
            return

        analyzer = DeepSystemAnalyzer(str(self.project_path))

        self.status_updated.emit("📊 Аналіз структури проекту...")
        self.progress_updated.emit(20)

        if self.is_cancelled:
            return

        # Perform full analysis with context
        analyzer.analyze_full_system(pause_duration=0.5)

        self.status_updated.emit("🔍 Детекція проблем та можливостей...")
        self.progress_updated.emit(60)

        if self.is_cancelled:
            return

        # Save comprehensive report
        analyzer.save_report("DEEP_ANALYSIS_SELF_IMPROVEMENT.md")

        self.status_updated.emit("📄 Звіт збережено, генерація рекомендацій...")
        self.progress_updated.emit(90)

        if self.is_cancelled:
            return

        self.status_updated.emit("✅ Глибокий аналіз завершено")
        self.progress_updated.emit(100)

    def _full_implementation(self):
        """Full implementation based on dev plan and deep analysis"""
        self.status_updated.emit("🚀 Початок повної реалізації...")
        self.progress_updated.emit(5)

        if self.is_cancelled:
            return

        # Initialize workflow
        workflow = EnhancedInteractiveWorkflow(
            str(self.project_path), pause_duration=1.0
        )

        self.status_updated.emit("📋 Виконання завдань з dev plan...")
        self.progress_updated.emit(15)

        if self.is_cancelled:
            return

        # Execute dev plan tasks
        dev_manager = DevPlanManager(self.project_path)
        dev_manager.execute_full_plan()

        self.status_updated.emit("🔧 Створення компонентів системи...")
        self.progress_updated.emit(40)

        if self.is_cancelled:
            return

        # Run enhanced workflow phases
        try:
            workflow.run_complete_workflow()
        except Exception as e:
            self.status_updated.emit(f"⚠️ Workflow warning: {str(e)}")

        self.status_updated.emit("🧪 Тестування та валідація...")
        self.progress_updated.emit(80)

        if self.is_cancelled:
            return

        # Final analysis
        analyzer = DeepSystemAnalyzer(str(self.project_path))
        analyzer.analyze_full_system(pause_duration=0.2)

        self.status_updated.emit("✅ Повна реалізація завершена")
        self.progress_updated.emit(100)


class SelfImprovementDialog(QDialog):
    """Dialog for self-improvement confirmation and progress"""

    def __init__(self, improvement_type: str, description: str, parent=None):
        super().__init__(parent)
        self.improvement_type = improvement_type
        self.setWindowTitle("Підтвердження самовдосконалення")
        self.setModal(True)
        self.resize(500, 300)

        # Apply theme
        theme = NIMDATheme()
        theme.apply_theme(self)

        self._setup_ui(description)

    def _setup_ui(self, description: str):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("🤖 Самовдосконалення NIMDA Agent")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Description
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)

        # Warning
        warning = QLabel(
            "⚠️ Цей процес може внести зміни до проекту. Переконайтеся, що у вас є резервна копія."
        )
        warning.setStyleSheet("color: orange; font-weight: bold;")
        warning.setWordWrap(True)
        warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(warning)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            Qt.Orientation.Horizontal,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


class NIMDAMainWindow(QMainWindow):
    """Main NIMDA Agent GUI Window with self-improvement capabilities"""

    def __init__(self):
        super().__init__()
        self.project_path = Path(__file__).parent.parent
        self.theme = NIMDATheme()
        self.gui_controller = GUIController()
        self.improvement_worker = None

        self.setWindowTitle("🤖 NIMDA Agent - Intelligent Development Assistant")
        self.setGeometry(100, 100, 1400, 900)

        # Setup UI
        self._setup_ui()
        self._setup_status_bar()
        self._setup_timers()

        # Apply theme
        self.theme.apply_theme(self)

        # Load initial data
        self._load_initial_data()

    def _setup_ui(self):
        """Setup main UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)

        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel - Self-improvement controls
        left_panel = self._create_improvement_panel()
        splitter.addWidget(left_panel)

        # Center panel - Chat and interaction
        center_panel = self._create_chat_panel()
        splitter.addWidget(center_panel)

        # Right panel - System status and analysis
        right_panel = self._create_status_panel()
        splitter.addWidget(right_panel)

        # Set splitter proportions
        splitter.setSizes([350, 700, 350])

    def _create_improvement_panel(self) -> QWidget:
        """Create self-improvement control panel"""
        panel = QGroupBox("🚀 Самовдосконалення")
        layout = QVBoxLayout(panel)

        # Title
        title = QLabel("Безпечне вдосконалення системи")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Button 1: Dev Plan Expansion
        btn_dev_plan = QPushButton("📋 Розширити Dev Plan")
        btn_dev_plan.setToolTip(
            "Автоматично проаналізує поточний стан проекту та розширить "
            "план розробки новими завданнями на основі контексту"
        )
        btn_dev_plan.clicked.connect(
            lambda: self._start_improvement("dev_plan_expansion")
        )
        btn_dev_plan.setMinimumHeight(50)
        layout.addWidget(btn_dev_plan)

        # Button 2: Deep Analysis
        btn_deep_analysis = QPushButton("🧠 Глибокий Аналіз")
        btn_deep_analysis.setToolTip(
            "Виконає комплексний аналіз всього проекту з урахуванням "
            "контексту кожного файла та workflow. Генерує детальний звіт."
        )
        btn_deep_analysis.clicked.connect(
            lambda: self._start_improvement("deep_analysis")
        )
        btn_deep_analysis.setMinimumHeight(50)
        layout.addWidget(btn_deep_analysis)

        # Button 3: Full Implementation
        btn_full_impl = QPushButton("⚡ Повна Реалізація")
        btn_full_impl.setToolTip(
            "Виконає повний цикл розробки: розширення dev plan → "
            "глибокий аналіз → автоматична реалізація завдань"
        )
        btn_full_impl.clicked.connect(
            lambda: self._start_improvement("full_implementation")
        )
        btn_full_impl.setMinimumHeight(50)
        layout.addWidget(btn_full_impl)

        # Progress section
        progress_group = QGroupBox("📊 Прогрес")
        progress_layout = QVBoxLayout(progress_group)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)

        self.progress_status = QLabel("Готово до роботи")
        self.progress_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(self.progress_status)

        # Cancel button
        self.btn_cancel = QPushButton("❌ Скасувати")
        self.btn_cancel.clicked.connect(self._cancel_improvement)
        self.btn_cancel.setVisible(False)
        progress_layout.addWidget(self.btn_cancel)

        layout.addWidget(progress_group)

        # Dev Plan status
        dev_plan_group = QGroupBox("📋 Статус Dev Plan")
        dev_plan_layout = QVBoxLayout(dev_plan_group)

        self.dev_plan_status = QLabel("Завантаження...")
        self.dev_plan_status.setWordWrap(True)
        dev_plan_layout.addWidget(self.dev_plan_status)

        layout.addWidget(dev_plan_group)

        # Spacer
        layout.addStretch()

        return panel

    def _create_chat_panel(self) -> QWidget:
        """Create main chat and interaction panel"""
        panel = QGroupBox("💬 Взаємодія з Агентом")
        layout = QVBoxLayout(panel)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(400)
        layout.addWidget(self.chat_display)

        # Input area
        input_layout = QHBoxLayout()

        self.chat_input = QTextEdit()
        self.chat_input.setMaximumHeight(60)
        self.chat_input.setPlaceholderText("Введіть повідомлення для NIMDA Agent...")
        input_layout.addWidget(self.chat_input)

        send_btn = QPushButton("📤 Надіслати")
        send_btn.clicked.connect(self._send_message)
        send_btn.setMaximumWidth(100)
        input_layout.addWidget(send_btn)

        layout.addLayout(input_layout)

        # Initial welcome message
        self.chat_display.append(
            "🤖 <b>NIMDA Agent</b>: Вітаю! Я готовий допомогти з розробкою.<br>"
            "Використовуйте кнопки самовдосконалення зліва для автоматичного покращення системи.<br><br>"
        )

        return panel

    def _create_status_panel(self) -> QWidget:
        """Create system status and analysis panel"""
        panel = QGroupBox("📊 Статус Системи")
        layout = QVBoxLayout(panel)

        # Tabs for different status views
        tab_widget = QTabWidget()

        # System Overview Tab
        overview_tab = QWidget()
        overview_layout = QVBoxLayout(overview_tab)

        self.system_overview = QTextEdit()
        self.system_overview.setReadOnly(True)
        self.system_overview.setMaximumHeight(200)
        overview_layout.addWidget(self.system_overview)

        tab_widget.addTab(overview_tab, "🏠 Огляд")

        # Recent Analysis Tab
        analysis_tab = QWidget()
        analysis_layout = QVBoxLayout(analysis_tab)

        self.analysis_results = QTextEdit()
        self.analysis_results.setReadOnly(True)
        analysis_layout.addWidget(self.analysis_results)

        tab_widget.addTab(analysis_tab, "🔍 Аналіз")

        # Recommendations Tab
        recommendations_tab = QWidget()
        recommendations_layout = QVBoxLayout(recommendations_tab)

        self.recommendations_display = QTextEdit()
        self.recommendations_display.setReadOnly(True)
        recommendations_layout.addWidget(self.recommendations_display)

        tab_widget.addTab(recommendations_tab, "💡 Рекомендації")

        layout.addWidget(tab_widget)

        # Action buttons
        action_layout = QHBoxLayout()

        refresh_btn = QPushButton("🔄 Оновити")
        refresh_btn.clicked.connect(self._refresh_status)
        action_layout.addWidget(refresh_btn)

        export_btn = QPushButton("📁 Експорт")
        export_btn.clicked.connect(self._export_analysis)
        action_layout.addWidget(export_btn)

        layout.addLayout(action_layout)

        return panel

    def _setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Add permanent widgets
        self.status_label = QLabel("Готово")
        self.status_bar.addWidget(self.status_label)

        # Project path
        project_label = QLabel(f"📁 {self.project_path.name}")
        self.status_bar.addPermanentWidget(project_label)

    def _setup_timers(self):
        """Setup timers for periodic updates"""
        # Status update timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_system_status)
        self.status_timer.start(30000)  # Update every 30 seconds

    def _load_initial_data(self):
        """Load initial data and status"""
        self._update_dev_plan_status()
        self._update_system_status()

    def _start_improvement(self, improvement_type: str):
        """Start self-improvement process"""
        # Prepare descriptions
        descriptions = {
            "dev_plan_expansion": (
                "🔍 Розширення Dev Plan\n\n"
                "Система проаналізує поточний стан проекту та автоматично "
                "розширить план розробки новими завданнями на основі:\n"
                "• Існуючої структури файлів\n"
                "• Незавершених компонентів\n"
                "• Можливостей для покращення\n"
                "• Контексту всього workflow"
            ),
            "deep_analysis": (
                "🧠 Глибокий Контекстний Аналіз\n\n"
                "Виконає комплексний аналіз всього проекту з урахуванням "
                "контексту кожного файла:\n"
                "• Структурний аналіз та метрики\n"
                "• Аналіз залежностей та інтеграцій\n"
                "• Виявлення проблем та можливостей\n"
                "• Генерація персоналізованих рекомендацій"
            ),
            "full_implementation": (
                "⚡ Повна Автоматична Реалізація\n\n"
                "Виконає повний цикл автоматичного вдосконалення:\n"
                "1. Розширення та оптимізація dev plan\n"
                "2. Глибокий контекстний аналіз\n"
                "3. Автоматична реалізація завдань\n"
                "4. Тестування та валідація\n"
                "5. Фінальний звіт з рекомендаціями"
            ),
        }

        # Show confirmation dialog
        dialog = SelfImprovementDialog(
            improvement_type, descriptions[improvement_type], self
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._execute_improvement(improvement_type)

    def _execute_improvement(self, improvement_type: str):
        """Execute the improvement process"""
        # Disable improvement buttons
        for btn in self.findChildren(QPushButton):
            if "📋" in btn.text() or "🧠" in btn.text() or "⚡" in btn.text():
                btn.setEnabled(False)

        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.btn_cancel.setVisible(True)
        self.progress_status.setText("Ініціалізація...")

        # Start worker thread
        self.improvement_worker = SelfImprovementWorker(
            improvement_type, self.project_path
        )
        self.improvement_worker.progress_updated.connect(self.progress_bar.setValue)
        self.improvement_worker.status_updated.connect(self.progress_status.setText)
        self.improvement_worker.finished.connect(self._improvement_finished)
        self.improvement_worker.start()

        # Log to chat
        type_names = {
            "dev_plan_expansion": "Розширення Dev Plan",
            "deep_analysis": "Глибокий Аналіз",
            "full_implementation": "Повна Реалізація",
        }

        self.chat_display.append(
            f"🚀 <b>Система</b>: Починаю {type_names[improvement_type]}...<br>"
        )

    def _cancel_improvement(self):
        """Cancel current improvement process"""
        if self.improvement_worker:
            self.improvement_worker.cancel()
            self.chat_display.append(
                "⚠️ <b>Система</b>: Процес самовдосконалення скасовано користувачем.<br>"
            )

    def _improvement_finished(self, success: bool, message: str):
        """Handle improvement process completion"""
        # Re-enable buttons
        for btn in self.findChildren(QPushButton):
            if "📋" in btn.text() or "🧠" in btn.text() or "⚡" in btn.text():
                btn.setEnabled(True)

        # Hide progress
        self.progress_bar.setVisible(False)
        self.btn_cancel.setVisible(False)

        if success:
            self.progress_status.setText("✅ Завершено успішно")
            self.chat_display.append(f"✅ <b>Система</b>: {message}<br>")

            # Update status displays
            self._update_dev_plan_status()
            self._update_system_status()

        else:
            self.progress_status.setText("❌ Помилка")
            self.chat_display.append(f"❌ <b>Система</b>: {message}<br>")

        # Cleanup worker
        self.improvement_worker = None

    def _send_message(self):
        """Send message to agent"""
        message = self.chat_input.toPlainText().strip()
        if not message:
            return

        self.chat_display.append(f"👤 <b>Користувач</b>: {message}<br>")
        self.chat_input.clear()

        # Process message (placeholder for actual agent integration)
        self.chat_display.append(
            f"🤖 <b>NIMDA Agent</b>: Отримав повідомлення: '{message}'. "
            f"Функція обробки повідомлень буде реалізована в наступних ітераціях.<br><br>"
        )

    def _update_dev_plan_status(self):
        """Update dev plan status display"""
        try:
            dev_manager = DevPlanManager(self.project_path)
            status = dev_manager.get_plan_status()

            status_text = (
                f"📊 Прогрес: {status['progress_percentage']:.1f}%\n"
                f"✅ Завершено: {status['completed_subtasks']}/{status['total_subtasks']} підзадач\n"
                f"📝 Завдань: {status['completed_tasks']}/{status['total_tasks']}\n"
            )

            if status["last_modified"]:
                status_text += f"🕒 Оновлено: {status['last_modified'][:19]}"

            self.dev_plan_status.setText(status_text)

        except Exception as e:
            self.dev_plan_status.setText(f"❌ Помилка завантаження: {str(e)}")

    def _update_system_status(self):
        """Update system status display"""
        try:
            # Basic system information
            python_files = list(self.project_path.glob("**/*.py"))

            overview_text = (
                f"📁 Проект: {self.project_path.name}\n"
                f"🐍 Python файлів: {len(python_files)}\n"
                f"📂 Директорій: {len([d for d in self.project_path.iterdir() if d.is_dir()])}\n"
                f"🔧 GUI компоненти: {'✅' if (self.project_path / 'GUI').exists() else '❌'}\n"
                f"📋 Dev Plan: {'✅' if (self.project_path / 'DEV_PLAN.md').exists() else '❌'}\n"
            )

            self.system_overview.setText(overview_text)

        except Exception as e:
            self.system_overview.setText(f"❌ Помилка: {str(e)}")

    def _refresh_status(self):
        """Refresh all status displays"""
        self._update_dev_plan_status()
        self._update_system_status()
        self.status_label.setText("🔄 Статус оновлено")

        QTimer.singleShot(2000, lambda: self.status_label.setText("Готово"))

    def _export_analysis(self):
        """Export analysis results"""
        # Placeholder for export functionality
        QMessageBox.information(
            self, "Експорт", "Функція експорту буде реалізована в наступних ітераціях."
        )


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("NIMDA Agent GUI")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("NIMDA Project")

    # Create and show main window
    window = NIMDAMainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
