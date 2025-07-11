#!/usr/bin/env python3
"""
NIMDA Agent Smart Setup Script
Auto-adapts to existing Python 3.11 environment and VS Code
"""

import os
import sys
import json
import subprocess
from pathlib import Path


def detect_environment():
    """Detect current environment"""
    env_info = {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": sys.platform,
        "has_nimda_env": False,
        "venv_path": None,
        "working_dir": str(Path.cwd())
    }
    
    # Check for NIMDA virtual environment
    nimda_env_paths = [
        Path("nimda_env"),
        Path("../nimda_env"), 
        Path("../../nimda_env")
    ]
    
    for env_path in nimda_env_paths:
        if env_path.exists() and (env_path / "bin" / "python").exists():
            env_info["has_nimda_env"] = True
            env_info["venv_path"] = str(env_path.resolve())
            break
    
    return env_info


def create_vscode_integration(env_info):
    """Create VS Code integration"""
    print("🆚 Setting up VS Code integration...")
    
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    # Determine Python path
    if env_info["has_nimda_env"]:
        if env_info["platform"] == "win32":
            python_path = f"{env_info['venv_path']}/Scripts/python.exe"
        else:
            python_path = f"{env_info['venv_path']}/bin/python"
    else:
        python_path = sys.executable
    
    # Create settings.json
    settings = {
        "python.defaultInterpreterPath": python_path,
        "python.terminal.activateEnvironment": True,
        "python.linting.enabled": True,
        "python.linting.flake8Enabled": True,
        "python.formatting.provider": "black",
        "files.associations": {
            "*.md": "markdown"
        },
        "terminal.integrated.env.linux": {
            "NIMDA_AGENT_PATH": "${workspaceFolder}/nimda_agent_plugin"
        }
    }
    
    settings_file = vscode_dir / "settings.json"
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    
    print(f"✅ VS Code settings created: {settings_file}")
    
    # Create tasks.json
    if env_info["platform"] == "win32":
        activate_cmd = f"& '{env_info['venv_path']}/Scripts/Activate.ps1'"
    else:
        activate_cmd = f"source {env_info['venv_path']}/bin/activate"
    
    tasks = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Activate NIMDA Environment",
                "type": "shell",
                "command": f"{activate_cmd} && python --version && echo 'NIMDA Environment activated'",
                "group": "build"
            },
            {
                "label": "Run NIMDA Agent Status",
                "type": "shell",
                "command": f"{activate_cmd} && python nimda_agent_plugin/run_nimda_agent.py --command 'статус'",
                "group": "test"
            }
        ]
    }
    
    tasks_file = vscode_dir / "tasks.json"
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    
    print(f"✅ VS Code tasks created: {tasks_file}")


def test_nimda_agent(env_info):
    """Test NIMDA Agent"""
    print("🧪 Testing NIMDA Agent...")
    
    nimda_script = Path("nimda_agent_plugin/run_nimda_agent.py")
    
    if not nimda_script.exists():
        print("❌ NIMDA Agent not found")
        return False
    
    # Choose correct Python executable
    if env_info["has_nimda_env"]:
        venv_path = Path(env_info["venv_path"])
        if env_info["platform"] == "win32":
            python_exe = venv_path / "Scripts" / "python.exe"
        else:
            python_exe = venv_path / "bin" / "python"
    else:
        python_exe = sys.executable
    
    try:
        print("🚀 Running test command...")
        result = subprocess.run([
            str(python_exe), str(nimda_script), "--command", "статус"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ NIMDA Agent working successfully!")
            return True
        else:
            print(f"⚠️ NIMDA Agent completed with code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout while testing NIMDA Agent")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False


def main():
    """Main setup function"""
    print("🤖 NIMDA Agent Smart Setup")
    print("=" * 40)
    
    # Detect environment
    env_info = detect_environment()
    
    print("🔍 Environment detection:")
    print(f"  🐍 Python: {env_info['python_version']}")
    print(f"  💻 Platform: {env_info['platform']}")
    print(f"  📁 Working Directory: {env_info['working_dir']}")
    print(f"  🔧 NIMDA Environment: {'✅' if env_info['has_nimda_env'] else '❌'}")
    
    if env_info["venv_path"]:
        print(f"  📍 Environment Path: {env_info['venv_path']}")
    
    # Setup steps
    steps = [
        ("VS Code integration", lambda: create_vscode_integration(env_info)),
        ("NIMDA Agent test", lambda: test_nimda_agent(env_info))
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        try:
            if step_func():
                success_count += 1
                print(f"✅ {step_name} - success")
            else:
                print(f"⚠️ {step_name} - completed with warnings")
        except Exception as e:
            print(f"❌ {step_name} - error: {e}")
    
    print(f"\n🎯 Setup completed: {success_count}/{len(steps)} steps successful")
    
    if success_count >= len(steps) - 1:
        print("\n🎉 NIMDA Agent is ready!")
        print("\n📚 Next steps:")
        print("  1. Open project in VS Code")
        print("  2. Choose recommended extensions")
        print("  3. Configure GitHub token in .env file")
        print("  4. Run: Ctrl+Shift+P -> 'Tasks: Run Task' -> 'Run NIMDA Agent Status'")
    else:
        print("\n⚠️ Some steps failed")
        print("Check errors above and try again")


if __name__ == "__main__":
    main()
