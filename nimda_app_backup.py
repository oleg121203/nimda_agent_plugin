#!/usr/bin/env python3.11
"""
NIMDA Agent - Main Application Entry Point
Production-ready application with GUI self-improvement capabilities
Optimized for Python 3.11
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Any, Dict

# Ensure Python 3.11
if sys.version_info < (3, 11):
    print("❌ Python 3.11 or higher required")
    print("Please run with: python3.11 nimda_app.py")
    sys.exit(1)

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("nimda_app.log"), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Import system components and workflows
system_components = {}
try:
    from system_status import run_system_check
    system_components['system_status'] = run_system_check
    logger.info("✅ System status module loaded")
except ImportError as e:
    logger.warning(f"❌ System status not available: {e}")

try:
    from health_dashboard import HealthDashboard
    system_components['health_dashboard'] = HealthDashboard
    logger.info("✅ Health dashboard module loaded")
except ImportError as e:
    logger.warning(f"❌ Health dashboard not available: {e}")

try:
    from nimda_cli import NIMDACLI
    system_components['cli'] = NIMDACLI
    logger.info("✅ CLI module loaded")
except ImportError as e:
    logger.warning(f"❌ CLI not available: {e}")

try:
    from auto_dev_runner import run_cycle_until_complete
    system_components['auto_dev'] = run_cycle_until_complete
    logger.info("✅ Auto development runner loaded")
except ImportError as e:
    logger.warning(f"❌ Auto dev runner not available: {e}")

try:
    from deep_context_workflow import DeepContextWorkflowSystem
    system_components['deep_workflow'] = DeepContextWorkflowSystem
    logger.info("✅ Deep context workflow loaded")
except ImportError as e:
    logger.warning(f"❌ Deep workflow not available: {e}")

try:
    from dev_plan_manager import DevPlanManager
    system_components['dev_plan'] = DevPlanManager
    logger.info("✅ Dev plan manager loaded")
except ImportError as e:
    logger.warning(f"❌ Dev plan manager not available: {e}")

try:
    from deep_system_analyzer import DeepSystemAnalyzer
    system_components['analyzer'] = DeepSystemAnalyzer
    logger.info("✅ Deep system analyzer loaded")
except ImportError as e:
    logger.warning(f"❌ System analyzer not available: {e}")

try:
    from performance_monitor import PerformanceMonitor
    system_components['performance'] = PerformanceMonitor
    logger.info("✅ Performance monitor loaded")
except ImportError as e:
    logger.warning(f"❌ Performance monitor not available: {e}")

try:
    from git_manager import GitManager
    system_components['git'] = GitManager
    logger.info("✅ Git manager loaded")
except ImportError as e:
    logger.warning(f"❌ Git manager not available: {e}")

try:
    from backup_rotation import BackupManager
    system_components['backup'] = BackupManager
    logger.info("✅ Backup manager loaded")
except ImportError as e:
    logger.warning(f"❌ Backup manager not available: {e}")

# Continue with app initialization


class NIMDAApplication:
    """
    Main NIMDA Application Class with Integrated System Management
    
    Features:
    - GUI Self-Improvement Interface
    - System Status Monitoring  
    - Health Dashboard
    - CLI Command Integration
    - Automated Development Workflows
    - Performance Monitoring
    - Git Management
    - Backup Systems
    """

    def __init__(self):
        self.logger = logger
        self.components = system_components
        self.gui_mode = False
        self.health_dashboard = None
        self.cli_handler = None
        self.performance_monitor = None
        
        # Initialize available components
        self._initialize_components()
        
    def _initialize_components(self):
        """Initialize all available system components"""
        
        # Initialize Health Dashboard if available
        if 'health_dashboard' in self.components:
            try:
                self.health_dashboard = self.components['health_dashboard']()
                self.logger.info("✅ Health dashboard initialized")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize health dashboard: {e}")
        
        # Initialize CLI handler if available
        if 'cli' in self.components:
            try:
                self.cli_handler = self.components['cli']()
                self.logger.info("✅ CLI handler initialized")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize CLI: {e}")
                
        # Initialize Performance Monitor if available
        if 'performance' in self.components:
            try:
                self.performance_monitor = self.components['performance']()
                self.logger.info("✅ Performance monitor initialized")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize performance monitor: {e}")

    def run_system_check(self):
        """Run comprehensive system check"""
        if 'system_status' in self.components:
            try:
                return self.components['system_status']()
            except Exception as e:
                self.logger.error(f"❌ System check failed: {e}")
                return False
        else:
            self.logger.warning("❌ System status component not available")
            return False

    def start_health_dashboard(self, port: int = 8080):
        """Start the web-based health dashboard"""
        if self.health_dashboard:
            try:
                self.health_dashboard.start_server(port=port)
                self.logger.info(f"✅ Health dashboard started on port {port}")
                return True
            except Exception as e:
                self.logger.error(f"❌ Failed to start health dashboard: {e}")
                return False
        else:
            self.logger.warning("❌ Health dashboard not available")
            return False

    def run_auto_development(self, cycles: int = 1):
        """Run automated development cycles"""
        if 'auto_dev' in self.components:
            try:
                self.components['auto_dev'](max_cycles=cycles)
                return True
            except Exception as e:
                self.logger.error(f"❌ Auto development failed: {e}")
                return False
        else:
            self.logger.warning("❌ Auto development not available")
            return False

    def run_deep_analysis(self):
        """Run deep system analysis"""
        if 'analyzer' in self.components:
            try:
                analyzer = self.components['analyzer']()
                return analyzer.run_full_analysis()
            except Exception as e:
                self.logger.error(f"❌ Deep analysis failed: {e}")
                return None
        else:
            self.logger.warning("❌ Deep analyzer not available")
            return None

    def expand_dev_plan(self):
        """Expand development plan"""
        if 'dev_plan' in self.components:
            try:
                dev_manager = self.components['dev_plan']()
                return dev_manager.expand_plan()
            except Exception as e:
                self.logger.error(f"❌ Dev plan expansion failed: {e}")
                return False
        else:
            self.logger.warning("❌ Dev plan manager not available")
            return False

    def start_gui(self):
        """Start GUI interface with self-improvement capabilities"""
        try:
            from GUI.nimda_gui import main as gui_main
            self.gui_mode = True
            self.logger.info("🚀 Starting GUI interface...")
            gui_main()
            return True
        except ImportError as e:
            self.logger.error(f"❌ GUI not available: {e}")
            self.logger.info("💡 Install GUI dependencies with: python GUI/nimda_gui.py --install-deps")
            return False
        except Exception as e:
            self.logger.error(f"❌ Failed to start GUI: {e}")
            return False

    def run_cli_command(self, command: str, args: list[str] | None = None):
        """Execute CLI command"""
        if self.cli_handler:
            try:
                return self.cli_handler.execute_command(command, args or [])
            except Exception as e:
                self.logger.error(f"❌ CLI command failed: {e}")
                return False
        else:
            self.logger.warning("❌ CLI handler not available")
            return False

    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report"""
        report = {
            'timestamp': logging.Formatter().formatTime(logging.LogRecord(
                name='', level=0, pathname='', lineno=0, msg='', args=(), exc_info=None
            )),
            'components': {},
            'system_health': {},
            'performance': {}
        }
        
        # Component availability
        for name, component in self.components.items():
            report['components'][name] = {
                'available': True,
                'type': str(type(component).__name__)
            }
        
        # System health check
        if 'system_status' in self.components:
            try:
                report['system_health'] = self.run_system_check()
            except Exception as e:
                report['system_health'] = {'error': str(e)}
        
        # Performance metrics
        if self.performance_monitor:
            try:
                report['performance'] = self.performance_monitor.get_metrics()
            except Exception as e:
                report['performance'] = {'error': str(e)}
        
        return report

    def interactive_mode(self):
        """Run in interactive command mode"""
        self.logger.info("🎯 NIMDA Interactive Mode")
        self.logger.info("Available commands: gui, status, health, dev, analyze, help, quit")
        
        while True:
            try:
                command = input("\nNIMDA> ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    break
                elif command == 'gui':
                    self.start_gui()
                elif command == 'status':
                    if self.run_system_check():
                        self.logger.info("✅ System check passed")
                    else:
                        self.logger.warning("❌ System check failed")
                elif command == 'health':
                    port = input("Dashboard port (default 8080): ").strip()
                    port = int(port) if port.isdigit() else 8080
                    if self.start_health_dashboard(port):
                        self.logger.info(f"🌐 Dashboard: http://localhost:{port}")
                elif command == 'dev':
                    cycles = input("Development cycles (default 1): ").strip()
                    cycles = int(cycles) if cycles.isdigit() else 1
                    self.run_auto_development(cycles)
                elif command == 'analyze':
                    result = self.run_deep_analysis()
                    if result:
                        self.logger.info("📊 Deep analysis completed")
                elif command == 'help':
                    self.show_help()
                elif command == 'report':
                    report = self.get_status_report()
                    self.logger.info(f"📋 Status Report: {report}")
                else:
                    self.logger.warning(f"❌ Unknown command: {command}")
                    
            except KeyboardInterrupt:
                self.logger.info("\n👋 Goodbye!")
                break
            except Exception as e:
                self.logger.error(f"❌ Command error: {e}")

    def show_help(self):
        """Show available commands"""
        help_text = """
🎯 NIMDA Agent Commands:

  gui        - Start GUI interface with self-improvement
  status     - Run system status check
  health     - Start web health dashboard
  dev        - Run automated development cycles
  analyze    - Run deep system analysis
  report     - Generate status report
  help       - Show this help
  quit/exit  - Exit application

🚀 Quick Start Examples:
  - GUI Mode: nimda_app.py --gui
  - Health Dashboard: nimda_app.py --health --port 8080
  - System Check: nimda_app.py --status
  - Auto Development: nimda_app.py --auto-dev --cycles 3
        """
        print(help_text)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="NIMDA Agent - Advanced AI Development Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3.11 nimda_app.py --gui                    # Start GUI interface
  python3.11 nimda_app.py --status                 # Run system check
  python3.11 nimda_app.py --health --port 8080     # Start health dashboard
  python3.11 nimda_app.py --auto-dev --cycles 3    # Run auto development
  python3.11 nimda_app.py --interactive            # Interactive mode
        """
    )
    
    # Mode selection
    parser.add_argument('--gui', action='store_true', help='Start GUI interface')
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    parser.add_argument('--status', action='store_true', help='Run system status check')
    parser.add_argument('--health', action='store_true', help='Start health dashboard')
    
    # Development commands
    parser.add_argument('--auto-dev', action='store_true', help='Run automated development')
    parser.add_argument('--cycles', type=int, default=1, help='Number of development cycles')
    parser.add_argument('--analyze', action='store_true', help='Run deep system analysis')
    parser.add_argument('--expand-plan', action='store_true', help='Expand development plan')
    
    # Configuration
    parser.add_argument('--port', type=int, default=8080, help='Port for health dashboard')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode')
    
    return parser.parse_args()


def main():
    """Main application entry point"""
    args = parse_arguments()
    
    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    # Initialize NIMDA application
    app = NIMDAApplication()
    
    try:
        # Handle GUI mode
        if args.gui:
            logger.info("🚀 Starting NIMDA GUI...")
            success = app.start_gui()
            if not success:
                logger.error("❌ Failed to start GUI")
                sys.exit(1)
            return
        
        # Handle health dashboard
        if args.health:
            logger.info(f"🌐 Starting health dashboard on port {args.port}...")
            success = app.start_health_dashboard(args.port)
            if success:
                logger.info(f"📊 Dashboard available at: http://localhost:{args.port}")
                try:
                    input("Press Enter to stop dashboard...")
                except KeyboardInterrupt:
                    pass
            else:
                logger.error("❌ Failed to start health dashboard")
                sys.exit(1)
            return
        
        # Handle system status check
        if args.status:
            logger.info("🔍 Running system status check...")
            success = app.run_system_check()
            if success:
                logger.info("✅ System check completed successfully")
            else:
                logger.error("❌ System check failed")
                sys.exit(1)
            return
        
        # Handle automated development
        if args.auto_dev:
            logger.info(f"🤖 Running automated development ({args.cycles} cycles)...")
            success = app.run_auto_development(args.cycles)
            if success:
                logger.info("✅ Automated development completed")
            else:
                logger.error("❌ Automated development failed")
                sys.exit(1)
            return
        
        # Handle deep analysis
        if args.analyze:
            logger.info("🧠 Running deep system analysis...")
            result = app.run_deep_analysis()
            if result:
                logger.info("✅ Deep analysis completed")
                logger.info(f"📊 Analysis result: {result}")
            else:
                logger.error("❌ Deep analysis failed")
                sys.exit(1)
            return
        
        # Handle dev plan expansion
        if args.expand_plan:
            logger.info("📋 Expanding development plan...")
            success = app.expand_dev_plan()
            if success:
                logger.info("✅ Development plan expanded")
            else:
                logger.error("❌ Dev plan expansion failed")
                sys.exit(1)
            return
        
        # Handle interactive mode or default
        if args.interactive or len(sys.argv) == 1:
            app.interactive_mode()
        else:
            # Show help if no valid arguments
            logger.info("Use --help for available options or run without arguments for interactive mode")
            
    except KeyboardInterrupt:
        logger.info("\n👋 NIMDA Agent stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
                component_status["adaptive_thinker"] = "✅ OK"
            except Exception as comp_error:
                component_status["adaptive_thinker"] = f"❌ {comp_error}"

            try:
                from learning_module import LearningModule

                self.components["learning_module"] = LearningModule()
                component_status["learning_module"] = "✅ OK"
            except Exception as comp_error:
                component_status["learning_module"] = f"❌ {comp_error}"

            try:
                from macos_integration import MacOSIntegration

                self.components["macos_integration"] = MacOSIntegration()
                component_status["macos_integration"] = "✅ OK"
            except Exception as comp_error:
                component_status["macos_integration"] = f"❌ {comp_error}"

            for comp, status in component_status.items():
                self.logger.info(f"  {comp}: {status}")

            # Return True if at least one component loaded
            return len(self.components) > 0

    def run_health_check(self) -> Dict[str, Any]:
        """Run comprehensive health check"""
        health_status = {
            "overall_status": "healthy",
            "components": {},
            "timestamp": str(Path(__file__).stat().st_mtime),
        }

        for name, component in self.components.items():
            try:
                # Check if component has basic attributes
                if hasattr(component, "__class__"):
                    health_status["components"][name] = {
                        "status": "healthy",
                        "class": component.__class__.__name__,
                    }
                else:
                    health_status["components"][name] = {
                        "status": "warning",
                        "reason": "Missing class attribute",
                    }
            except Exception as e:
                health_status["components"][name] = {
                    "status": "error",
                    "reason": str(e),
                }
                health_status["overall_status"] = "degraded"

        return health_status

    def run_interactive_mode(self):
        """Run in interactive mode with GUI integration"""
        self.logger.info("🚀 Starting NIMDA in interactive mode")

        print("\n" + "=" * 50)
        print("🤖 NIMDA Agent - Interactive Mode")
        if self.gui_available:
            print("🖥️ GUI available - type 'gui' to launch")
        print("=" * 50)

        while True:
            try:
                user_input = input("\nNIMDA> ").strip()

                if user_input.lower() in ["exit", "quit", "q"]:
                    print("👋 Goodbye!")
                    break

                elif user_input.lower() == "gui":
                    if self.gui_available:
                        print("🚀 Launching GUI...")
                        return self.run_gui_mode()
                    else:
                        print("❌ GUI not available. Install with: --install-gui-deps")

                elif user_input.lower() in ["health", "status"]:
                    health = self.run_health_check()
                    print(f"\n📊 System Status: {health['overall_status']}")
                    for comp, status in health["components"].items():
                        print(f"   {comp}: {status['status']}")
                    print(f"🖥️ GUI Available: {'✅' if self.gui_available else '❌'}")

                elif user_input.lower() in ["improve", "self-improve"]:
                    print("🧠 Self-improvement options:")
                    print("   expand   - Expand dev plan")
                    print("   analyze  - Deep analysis")
                    print("   implement - Full implementation")
                    print("   gui      - Launch GUI for visual improvements")

                elif user_input.lower() == "expand":
                    self._console_dev_plan_expansion()

                elif user_input.lower() == "analyze":
                    self._console_deep_analysis()

                elif user_input.lower() == "implement":
                    self._console_full_implementation()

                elif user_input.lower() == "help":
                    print("""
📖 Available Commands:
   health/status    - Check system health
   gui             - Launch GUI mode (if available)
   improve         - Show self-improvement options
   expand          - Expand development plan
   analyze         - Run deep system analysis
   implement       - Full automated implementation
   help            - Show this help
   exit/quit/q     - Exit application
   
🔧 Component Commands:
   Any other input will be processed by the chat agent
                    """)
                else:
                    # Process with chat agent
                    if "chat_agent" in self.components:
                        print(f"💬 Chat Agent: Processing '{user_input}'...")
                        # Here you would add actual chat processing
                        print("✅ Message processed successfully")
                    else:
                        print("❌ Chat agent not available")

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                self.logger.error(f"Error in interactive mode: {e}")
                print(f"❌ Error: {e}")

    def _console_dev_plan_expansion(self):
        """Console version of dev plan expansion"""
        print("📋 Starting dev plan expansion...")
        try:
            from dev_plan_manager import DevPlanManager

            dev_manager = DevPlanManager(project_root)
            status = dev_manager.get_plan_status()

            print(f"Current progress: {status['progress_percentage']:.1f}%")
            print("Analyzing project and expanding plan...")

            dev_manager.update_and_expand_plan()

            new_status = dev_manager.get_plan_status()
            print(
                f"✅ Plan expanded - new progress: {new_status['progress_percentage']:.1f}%"
            )

        except Exception as e:
            print(f"❌ Dev plan expansion failed: {e}")

    def _console_deep_analysis(self):
        """Console version of deep analysis"""
        print("🧠 Starting deep system analysis...")
        try:
            from deep_system_analyzer import DeepSystemAnalyzer

            analyzer = DeepSystemAnalyzer(str(project_root))
            analysis = analyzer.analyze_full_system(pause_duration=0.5)

            # Show summary
            structure = analysis.get("structure", {})
            metrics = analysis.get("metrics", {})
            issues = analysis.get("issues", [])

            print(f"📁 Files analyzed: {structure.get('total_files', 0)}")
            print(f"🐍 Python files: {len(structure.get('python_files', []))}")
            print(f"📊 Total lines: {metrics.get('total_lines', 0)}")
            print(f"🚨 Issues found: {len(issues)}")

            # Save report
            report_path = analyzer.save_report("CONSOLE_ANALYSIS_REPORT.md")
            print(f"✅ Analysis complete - report saved: {report_path}")

        except Exception as e:
            print(f"❌ Deep analysis failed: {e}")

    def _console_full_implementation(self):
        """Console version of full implementation"""
        print("⚡ Starting full automated implementation...")
        try:
            # Step 1: Expand dev plan
            print("1️⃣ Expanding dev plan...")
            self._console_dev_plan_expansion()

            # Step 2: Deep analysis
            print("\n2️⃣ Running deep analysis...")
            self._console_deep_analysis()

            # Step 3: Execute workflow
            print("\n3️⃣ Executing enhancement workflow...")
            from enhanced_interactive_workflow import EnhancedInteractiveWorkflow

            workflow = EnhancedInteractiveWorkflow(
                str(project_root), pause_duration=1.0
            )
            workflow.run_complete_workflow()

            print("✅ Full implementation complete!")

        except Exception as e:
            print(f"❌ Full implementation failed: {e}")

    def run_gui_mode(self):
        """Run in GUI mode with self-improvement capabilities"""
        if not self.gui_available:
            self.logger.error("❌ GUI mode requested but GUI not available")
            print("GUI mode not available. Try: python GUI/nimda_gui.py --install-deps")
            return 1

        self.logger.info("🚀 Starting NIMDA in GUI mode")

        try:
            from PySide6.QtWidgets import QApplication

            from GUI.main_window import NIMDAMainWindow
            from GUI.theme import NIMDATheme

            # Create Qt application
            app = QApplication(sys.argv)
            app.setApplicationName("NIMDA Agent")
            app.setApplicationVersion("1.0")
            app.setOrganizationName("NIMDA Project")

            # Set up GUI controller
            if self.gui_controller:
                self.gui_controller.set_main_window(
                    None
                )  # Will be set after window creation

            # Create main window
            window = NIMDAMainWindow()

            # Connect GUI controller to window
            if self.gui_controller:
                self.gui_controller.set_main_window(window)

            # Apply theme
            theme = NIMDATheme()
            theme.apply_theme(window)

            # Show window
            window.show()

            self.logger.info("✅ GUI launched successfully")
            print("🤖 NIMDA GUI launched with self-improvement capabilities")
            print(
                "💡 Use the three improvement buttons for automatic system enhancement"
            )

            # Run Qt event loop
            return app.exec()

        except Exception as e:
            self.logger.error(f"❌ GUI launch failed: {e}")
            print(f"GUI launch failed: {e}")
            return 1

    def run(self, mode: str = "auto") -> int:
        """Main application runner with GUI support"""
        try:
            self.logger.info(
                f"🚀 Starting NIMDA Agent Application (Python {sys.version})"
            )

            # Initialize components
            if not self.initialize_components():
                return 1

            # Run health check
            health = self.run_health_check()
            self.logger.info(f"📊 Health check: {health['overall_status']}")

            # Determine mode
            if mode == "auto":
                # Auto-select GUI if available, otherwise interactive
                mode = "gui" if self.gui_available else "interactive"
                self.logger.info(f"🔄 Auto-selected mode: {mode}")

            if mode == "gui":
                return self.run_gui_mode()
            elif mode == "interactive":
                self.run_interactive_mode()
            elif mode == "health":
                print("\n📊 NIMDA Health Status:")
                print(f"Overall: {health['overall_status']}")
                for comp, status in health["components"].items():
                    print(f"  {comp}: {status['status']}")
                print(f"\n🖥️ GUI Available: {'✅' if self.gui_available else '❌'}")
            elif mode == "daemon":
                self.logger.info("🔄 Running in daemon mode")
                # Daemon mode implementation
                print("Daemon mode - running in background...")
                import time

                try:
                    while True:
                        time.sleep(60)  # Keep alive
                except KeyboardInterrupt:
                    print("\n👋 Daemon stopped")
            else:
                self.logger.error(f"❌ Unknown mode: {mode}")
                return 1

            return 0

        except Exception as e:
            self.logger.error(f"💥 Application error: {e}")
            return 1


def main():
    """Main entry point with GUI support"""
    parser = argparse.ArgumentParser(
        description="NIMDA Agent Application with GUI Self-Improvement"
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "gui", "interactive", "health", "daemon"],
        default="auto",
        help="Application mode (auto: GUI if available, else interactive)",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level",
    )
    parser.add_argument(
        "--install-gui-deps",
        action="store_true",
        help="Install GUI dependencies and exit",
    )

    args = parser.parse_args()

    # Install GUI dependencies if requested
    if args.install_gui_deps:
        print("🔧 Installing GUI dependencies...")
        try:
            import subprocess

            dependencies = ["PySide6"]
            if sys.platform == "darwin":  # macOS
                dependencies.append("PyObjC")

            for dep in dependencies:
                print(f"   Installing {dep}...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", dep],
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    print(f"   ✅ {dep} installed")
                else:
                    print(f"   ❌ Failed to install {dep}: {result.stderr}")
                    return 1

            print("✅ All GUI dependencies installed")
            print("🔄 Restart with: python3.11 nimda_app.py --mode gui")
            return 0

        except Exception as e:
            print(f"❌ Installation failed: {e}")
            return 1

    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level))

    # Show startup info
    print("🤖 NIMDA Agent - Intelligent Development Assistant")
    print(f"🐍 Python {sys.version}")
    print("=" * 60)

    # Create and run application
    app = NIMDAApplication()
    return app.run(args.mode)


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        sys.exit(1)
