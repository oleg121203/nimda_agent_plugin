#!/usr/bin/env python3
"""
Advanced Task Management System with 3-level subtasks and automatic analysis
Based on DEV_PLAN.md with Codex-driven expansion
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class AdvancedTaskManager:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.task_structure = {
            "phases": [],
            "current_phase": 0,
            "total_tasks": 0,
            "completed_tasks": 0,
            "auto_generated_subtasks": [],
        }
        self.python_version = "3.11"  # Force Python 3.11

    def initialize_from_dev_plan(self) -> Dict[str, Any]:
        """Initialize task structure from DEV_PLAN.md"""
        print("📋 Initializing Advanced Task Management from DEV_PLAN.md")

        # Read DEV_PLAN.md
        dev_plan_path = self.project_path / "DEV_PLAN.md"
        if not dev_plan_path.exists():
            print("⚠️  DEV_PLAN.md not found, creating basic structure")
            return self._create_basic_structure()

        # Parse existing plan and expand with 3 levels
        return self._parse_and_expand_dev_plan(dev_plan_path)

    def _create_basic_structure(self) -> Dict[str, Any]:
        """Create basic 3-level task structure if DEV_PLAN.md is missing"""
        self.task_structure = {
            "phases": [
                {
                    "id": 1,
                    "name": "Environment Setup & Analysis",
                    "description": "Setup Python 3.11 environment and analyze system",
                    "status": "pending",
                    "level_1_tasks": [
                        {
                            "id": "1.1",
                            "name": "Python 3.11 Environment Setup",
                            "status": "pending",
                            "level_2_tasks": [
                                {
                                    "id": "1.1.1",
                                    "name": "Create virtual environment with Python 3.11",
                                    "status": "pending",
                                    "level_3_tasks": [
                                        {
                                            "id": "1.1.1.1",
                                            "name": "Check Python 3.11 availability",
                                            "status": "pending",
                                        },
                                        {
                                            "id": "1.1.1.2",
                                            "name": "Create venv with python3.11",
                                            "status": "pending",
                                        },
                                        {
                                            "id": "1.1.1.3",
                                            "name": "Activate environment",
                                            "status": "pending",
                                        },
                                    ],
                                },
                                {
                                    "id": "1.1.2",
                                    "name": "Install dependencies",
                                    "status": "pending",
                                    "level_3_tasks": [
                                        {
                                            "id": "1.1.2.1",
                                            "name": "Install PySide6",
                                            "status": "pending",
                                        },
                                        {
                                            "id": "1.1.2.2",
                                            "name": "Install PyObjC for macOS",
                                            "status": "pending",
                                        },
                                        {
                                            "id": "1.1.2.3",
                                            "name": "Install FAISS and other deps",
                                            "status": "pending",
                                        },
                                    ],
                                },
                            ],
                        }
                    ],
                }
            ],
            "current_phase": 0,
            "total_tasks": 6,
            "completed_tasks": 0,
            "auto_generated_subtasks": [],
        }
        return self.task_structure

    def _parse_and_expand_dev_plan(self, plan_path: Path) -> Dict[str, Any]:
        """Parse DEV_PLAN.md and expand with automatic subtasks"""
        print("🔍 Parsing DEV_PLAN.md and expanding with subtasks...")

        with open(plan_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract phases/sections from markdown
        phases = self._extract_phases_from_markdown(content)

        # Expand each phase with 3 levels of subtasks
        expanded_phases = []
        total_tasks = 0

        for i, phase in enumerate(phases):
            expanded_phase = self._expand_phase_with_subtasks(phase, i + 1)
            expanded_phases.append(expanded_phase)
            total_tasks += self._count_all_tasks(expanded_phase)

        self.task_structure = {
            "phases": expanded_phases,
            "current_phase": 0,
            "total_tasks": total_tasks,
            "completed_tasks": 0,
            "auto_generated_subtasks": [],
            "python_version": self.python_version,
        }

        return self.task_structure

    def _extract_phases_from_markdown(self, content: str) -> List[Dict[str, Any]]:
        """Extract main phases from DEV_PLAN.md"""
        phases = []
        lines = content.split("\n")
        current_phase = None

        for line in lines:
            # Look for main sections (## 1. Project Initialization)
            if line.startswith("## ") and any(char.isdigit() for char in line):
                if current_phase:
                    phases.append(current_phase)

                # Extract phase info
                title = line.replace("#", "").strip()
                phase_number = "".join(filter(str.isdigit, title.split(".")[0]))

                current_phase = {
                    "number": int(phase_number) if phase_number else len(phases) + 1,
                    "title": title,
                    "description": "",
                    "subtasks": [],
                }

            # Look for subtasks (### 2.1. Core/main_controller.py)
            elif line.startswith("### ") and current_phase:
                subtask_title = line.replace("#", "").strip()
                current_phase["subtasks"].append({"title": subtask_title, "items": []})

            # Look for checklist items (- [ ] Create and activate...)
            elif (
                line.strip().startswith("- [ ]")
                and current_phase
                and current_phase["subtasks"]
            ):
                item = line.strip().replace("- [ ]", "").strip()
                current_phase["subtasks"][-1]["items"].append(item)

        if current_phase:
            phases.append(current_phase)

        return phases

    def _expand_phase_with_subtasks(
        self, phase: Dict[str, Any], phase_id: int
    ) -> Dict[str, Any]:
        """Expand a phase with 3 levels of automatically generated subtasks"""
        print(f"🔧 Expanding Phase {phase_id}: {phase['title']}")

        expanded_phase = {
            "id": phase_id,
            "name": phase["title"],
            "description": phase.get("description", ""),
            "status": "pending",
            "level_1_tasks": [],
        }

        # Level 1: Main subtasks from DEV_PLAN.md
        for i, subtask in enumerate(phase.get("subtasks", [])):
            level_1_task = {
                "id": f"{phase_id}.{i + 1}",
                "name": subtask["title"],
                "status": "pending",
                "level_2_tasks": [],
            }

            # Level 2: Break down each item into implementation steps
            for j, item in enumerate(subtask.get("items", [])):
                level_2_task = {
                    "id": f"{phase_id}.{i + 1}.{j + 1}",
                    "name": item,
                    "status": "pending",
                    "level_3_tasks": self._generate_level_3_tasks(
                        item, f"{phase_id}.{i + 1}.{j + 1}"
                    ),
                }
                level_1_task["level_2_tasks"].append(level_2_task)

            # If no items, create auto-generated level 2 tasks
            if not subtask.get("items"):
                auto_level_2 = self._auto_generate_level_2_tasks(
                    subtask["title"], f"{phase_id}.{i + 1}"
                )
                level_1_task["level_2_tasks"] = auto_level_2

            expanded_phase["level_1_tasks"].append(level_1_task)

        return expanded_phase

    def _generate_level_3_tasks(
        self, task_description: str, parent_id: str
    ) -> List[Dict[str, Any]]:
        """Generate Level 3 micro-tasks based on task description"""
        # Analyze task description and create micro-tasks
        level_3_tasks = []

        # Common patterns and their micro-tasks
        if "install" in task_description.lower():
            level_3_tasks = [
                {
                    "id": f"{parent_id}.1",
                    "name": "Check if already installed",
                    "status": "pending",
                },
                {
                    "id": f"{parent_id}.2",
                    "name": "Download/install package",
                    "status": "pending",
                },
                {
                    "id": f"{parent_id}.3",
                    "name": "Verify installation",
                    "status": "pending",
                },
            ]
        elif (
            "create" in task_description.lower() and "class" in task_description.lower()
        ):
            level_3_tasks = [
                {
                    "id": f"{parent_id}.1",
                    "name": "Design class structure",
                    "status": "pending",
                },
                {
                    "id": f"{parent_id}.2",
                    "name": "Implement basic methods",
                    "status": "pending",
                },
                {
                    "id": f"{parent_id}.3",
                    "name": "Add error handling",
                    "status": "pending",
                },
                {
                    "id": f"{parent_id}.4",
                    "name": "Write unit tests",
                    "status": "pending",
                },
            ]
        elif "implement" in task_description.lower():
            level_3_tasks = [
                {
                    "id": f"{parent_id}.1",
                    "name": "Analyze requirements",
                    "status": "pending",
                },
                {
                    "id": f"{parent_id}.2",
                    "name": "Write core logic",
                    "status": "pending",
                },
                {
                    "id": f"{parent_id}.3",
                    "name": "Test implementation",
                    "status": "pending",
                },
            ]
        elif "configure" in task_description.lower():
            level_3_tasks = [
                {
                    "id": f"{parent_id}.1",
                    "name": "Create configuration file",
                    "status": "pending",
                },
                {
                    "id": f"{parent_id}.2",
                    "name": "Set default values",
                    "status": "pending",
                },
                {
                    "id": f"{parent_id}.3",
                    "name": "Validate configuration",
                    "status": "pending",
                },
            ]
        else:
            # Generic micro-tasks
            level_3_tasks = [
                {
                    "id": f"{parent_id}.1",
                    "name": "Analyze requirements",
                    "status": "pending",
                },
                {
                    "id": f"{parent_id}.2",
                    "name": "Execute main action",
                    "status": "pending",
                },
                {
                    "id": f"{parent_id}.3",
                    "name": "Verify completion",
                    "status": "pending",
                },
            ]

        return level_3_tasks

    def _auto_generate_level_2_tasks(
        self, task_title: str, parent_id: str
    ) -> List[Dict[str, Any]]:
        """Auto-generate Level 2 tasks when DEV_PLAN.md doesn't have detailed items"""
        level_2_tasks = []

        if "controller" in task_title.lower():
            level_2_tasks = [
                {
                    "id": f"{parent_id}.1",
                    "name": "Design controller architecture",
                    "status": "pending",
                    "level_3_tasks": self._generate_level_3_tasks(
                        "Design controller architecture", f"{parent_id}.1"
                    ),
                },
                {
                    "id": f"{parent_id}.2",
                    "name": "Implement main controller class",
                    "status": "pending",
                    "level_3_tasks": self._generate_level_3_tasks(
                        "Implement main controller class", f"{parent_id}.2"
                    ),
                },
                {
                    "id": f"{parent_id}.3",
                    "name": "Add integration methods",
                    "status": "pending",
                    "level_3_tasks": self._generate_level_3_tasks(
                        "Add integration methods", f"{parent_id}.3"
                    ),
                },
            ]
        elif "agent" in task_title.lower():
            level_2_tasks = [
                {
                    "id": f"{parent_id}.1",
                    "name": "Create agent base class",
                    "status": "pending",
                    "level_3_tasks": self._generate_level_3_tasks(
                        "Create agent base class", f"{parent_id}.1"
                    ),
                },
                {
                    "id": f"{parent_id}.2",
                    "name": "Implement agent logic",
                    "status": "pending",
                    "level_3_tasks": self._generate_level_3_tasks(
                        "Implement agent logic", f"{parent_id}.2"
                    ),
                },
                {
                    "id": f"{parent_id}.3",
                    "name": "Add communication methods",
                    "status": "pending",
                    "level_3_tasks": self._generate_level_3_tasks(
                        "Add communication methods", f"{parent_id}.3"
                    ),
                },
            ]
        else:
            # Generic Level 2 structure
            level_2_tasks = [
                {
                    "id": f"{parent_id}.1",
                    "name": f"Plan {task_title.lower()}",
                    "status": "pending",
                    "level_3_tasks": self._generate_level_3_tasks(
                        f"Plan {task_title.lower()}", f"{parent_id}.1"
                    ),
                },
                {
                    "id": f"{parent_id}.2",
                    "name": f"Implement {task_title.lower()}",
                    "status": "pending",
                    "level_3_tasks": self._generate_level_3_tasks(
                        f"Implement {task_title.lower()}", f"{parent_id}.2"
                    ),
                },
                {
                    "id": f"{parent_id}.3",
                    "name": f"Test {task_title.lower()}",
                    "status": "pending",
                    "level_3_tasks": self._generate_level_3_tasks(
                        f"Test {task_title.lower()}", f"{parent_id}.3"
                    ),
                },
            ]

        return level_2_tasks

    def _count_all_tasks(self, phase: Dict[str, Any]) -> int:
        """Count all tasks across all 3 levels"""
        count = 0
        for level_1 in phase.get("level_1_tasks", []):
            count += 1  # Level 1 task
            for level_2 in level_1.get("level_2_tasks", []):
                count += 1  # Level 2 task
                count += len(level_2.get("level_3_tasks", []))  # Level 3 tasks
        return count

    def analyze_system_and_add_tasks(self, analysis_report: Dict[str, Any]):
        """Analyze system state and automatically add necessary subtasks"""
        print("🧠 Analyzing system state and adding automatic subtasks...")

        issues = analysis_report.get("issues", [])
        structure = analysis_report.get("structure", {})

        auto_tasks = []

        # Add tasks based on missing files
        python_files = structure.get("python_files", [])
        required_files = [
            "main.py",
            "chat_agent.py",
            "worker_agent.py",
            "adaptive_thinker.py",
        ]

        for required_file in required_files:
            if required_file not in python_files:
                auto_tasks.append(
                    {
                        "type": "create_missing_file",
                        "file": required_file,
                        "priority": "high",
                        "estimated_time": "15 minutes",
                    }
                )

        # Add tasks based on issues
        for issue in issues:
            if issue.get("severity") == "high":
                auto_tasks.append(
                    {
                        "type": "fix_critical_issue",
                        "description": issue.get("description", ""),
                        "priority": "critical",
                        "estimated_time": "30 minutes",
                    }
                )

        # Add Python version fix task if needed
        if self.python_version != "3.11":
            auto_tasks.append(
                {
                    "type": "fix_python_version",
                    "description": "Switch to Python 3.11",
                    "priority": "high",
                    "estimated_time": "20 minutes",
                }
            )

        self.task_structure["auto_generated_subtasks"] = auto_tasks
        print(f"   ✅ Added {len(auto_tasks)} automatic subtasks")

    def save_task_structure(self, filename: str = "ADVANCED_TASK_STRUCTURE.json"):
        """Save task structure to JSON file"""
        task_file = self.project_path / filename

        with open(task_file, "w", encoding="utf-8") as f:
            json.dump(self.task_structure, f, indent=2, ensure_ascii=False)

        print(f"📝 Task structure saved to {task_file}")
        return task_file

    def print_task_summary(self):
        """Print detailed task summary"""
        print("\n" + "=" * 70)
        print("📋 ADVANCED TASK MANAGEMENT SUMMARY")
        print("=" * 70)

        print(f"🐍 Target Python Version: {self.python_version}")
        print(f"📊 Total Phases: {len(self.task_structure['phases'])}")
        print(f"📝 Total Tasks: {self.task_structure['total_tasks']}")
        print(f"✅ Completed: {self.task_structure['completed_tasks']}")
        print(
            f"🤖 Auto-generated: {len(self.task_structure.get('auto_generated_subtasks', []))}"
        )

        print("\n📋 Phase Overview:")
        for i, phase in enumerate(self.task_structure["phases"]):
            status_icon = (
                "🟢"
                if phase["status"] == "completed"
                else "🟡"
                if phase["status"] == "in_progress"
                else "⚪"
            )
            print(f"   {status_icon} Phase {phase['id']}: {phase['name']}")
            print(f"      └── Level 1 Tasks: {len(phase['level_1_tasks'])}")

            total_level_2 = sum(
                len(t.get("level_2_tasks", [])) for t in phase["level_1_tasks"]
            )
            total_level_3 = sum(
                len(t2.get("level_3_tasks", []))
                for t1 in phase["level_1_tasks"]
                for t2 in t1.get("level_2_tasks", [])
            )

            print(f"      └── Level 2 Tasks: {total_level_2}")
            print(f"      └── Level 3 Tasks: {total_level_3}")

        # Show auto-generated tasks
        if self.task_structure.get("auto_generated_subtasks"):
            print("\n🤖 Auto-Generated Subtasks:")
            for task in self.task_structure["auto_generated_subtasks"]:
                priority_icon = (
                    "🔴"
                    if task["priority"] == "critical"
                    else "🟠"
                    if task["priority"] == "high"
                    else "🟢"
                )
                print(
                    f"   {priority_icon} {task['type']}: {task.get('description', task.get('file', 'N/A'))}"
                )

    def execute_next_task(self) -> Optional[Dict[str, Any]]:
        """Get the next task to execute and mark it as in progress"""
        # Find first pending task across all levels
        for phase in self.task_structure["phases"]:
            if phase["status"] == "pending":
                phase["status"] = "in_progress"

                for level_1 in phase["level_1_tasks"]:
                    if level_1["status"] == "pending":
                        level_1["status"] = "in_progress"

                        for level_2 in level_1["level_2_tasks"]:
                            if level_2["status"] == "pending":
                                level_2["status"] = "in_progress"

                                for level_3 in level_2["level_3_tasks"]:
                                    if level_3["status"] == "pending":
                                        level_3["status"] = "in_progress"
                                        return {
                                            "level": 3,
                                            "task": level_3,
                                            "parent_level_2": level_2,
                                            "parent_level_1": level_1,
                                            "phase": phase,
                                        }

                                # If no level 3 tasks, return level 2
                                return {
                                    "level": 2,
                                    "task": level_2,
                                    "parent_level_1": level_1,
                                    "phase": phase,
                                }

                        # If no level 2 tasks, return level 1
                        return {"level": 1, "task": level_1, "phase": phase}

        return None
