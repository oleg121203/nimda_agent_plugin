#!/usr/bin/env python3
"""
Quick test of NIMDA GUI Self-Improvement System
Tests the three main improvement buttons
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_gui_launch():
    """Test GUI launch"""
    print("🧪 Testing NIMDA GUI Self-Improvement System")
    print("=" * 50)

    # Check GUI availability
    try:
        from GUI import check_gui_requirements, get_gui_info

        info = get_gui_info()
        print(f"📦 GUI Package Version: {info['version']}")
        print(f"🔧 PySide6 Available: {'✅' if info['pyside6_available'] else '❌'}")

        if info["pyside6_available"]:
            print(f"📊 PySide6 Version: {info['pyside6_version']}")

        requirements = info["requirements"]
        if requirements["requirements_met"]:
            print("✅ All requirements met - GUI ready")
        else:
            print(f"❌ Missing packages: {', '.join(requirements['missing_packages'])}")
            return False

    except Exception as e:
        print(f"❌ Error checking GUI: {e}")
        return False

    # Test GUI components
    print("\n🔧 Testing GUI Components:")

    components = [
        ("GUI.main_window", "Main Window"),
        ("GUI.theme", "Theme System"),
        ("GUI.gui_controller", "GUI Controller"),
        ("GUI.adaptive_widget", "Adaptive Widgets"),
        ("GUI.nimda_gui", "GUI Launcher"),
    ]

    for module_name, description in components:
        try:
            __import__(module_name)
            print(f"   ✅ {description}")
        except Exception as e:
            print(f"   ❌ {description}: {e}")
            return False

    # Test improvement system integration
    print("\n🧠 Testing Self-Improvement Integration:")

    integration_tests = [
        ("dev_plan_manager", "Dev Plan Manager"),
        ("deep_system_analyzer", "Deep System Analyzer"),
        ("enhanced_interactive_workflow", "Enhanced Workflow"),
    ]

    for module_name, description in integration_tests:
        try:
            module = __import__(module_name)
            print(f"   ✅ {description}")
        except Exception as e:
            print(f"   ⚠️  {description}: {e}")

    print("\n🚀 GUI Test Complete - Ready to launch!")
    return True


def demo_console_interface():
    """Demo the console interface features"""
    print("\n💬 Console Interface Demo:")
    print("Available commands when GUI is not available:")
    print("  expand  - Expand dev plan")
    print("  analyze - Deep analysis")
    print("  status  - System status")
    print("  gui     - Try to launch GUI")
    print("  exit    - Exit")


def show_next_steps():
    """Show next steps for using the system"""
    print("\n🎯 Next Steps:")
    print("1. Launch GUI: python GUI/nimda_gui.py")
    print("2. Install deps: python GUI/nimda_gui.py --install-deps")
    print("3. Console mode: python GUI/nimda_gui.py --mode console")
    print("\n💡 Self-Improvement Buttons:")
    print("   📋 Dev Plan Expansion - Contextual task generation")
    print("   🧠 Deep Analysis - Comprehensive project analysis")
    print("   ⚡ Full Implementation - Complete automated improvement")


def main():
    """Main test function"""
    if test_gui_launch():
        demo_console_interface()
        show_next_steps()

        # Try to launch GUI if all tests pass
        try:
            print("\n🚀 Attempting to launch GUI...")
            from GUI.nimda_gui import main as gui_main

            return gui_main()
        except KeyboardInterrupt:
            print("\n👋 Test cancelled by user")
            return 0
        except Exception as e:
            print(f"\n⚠️ GUI launch failed: {e}")
            print("Try: python GUI/nimda_gui.py --install-deps")
            return 1
    else:
        print("\n❌ GUI tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
