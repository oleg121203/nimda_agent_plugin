#!/usr/bin/env python3
"""
Universal Advanced Task Management System
- Fully driven by DEV_PLAN.md
- No hardcoded technologies or versions
- 3-level subtasks with automatic analysis
- Creative AI/Codex expansion support
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class UniversalTaskManager:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.task_structure = {
            "project_type": "unknown",
            "technologies": [],
            "phases": [],
            "current_phase": 0,
            "total_tasks": 0,
            "completed_tasks": 0,
            "auto_generated_subtasks": [],
            "creative_extensions": [],
        }
        self.project_config = {}
        self.creative_hooks = []

    def initialize_from_dev_plan(self) -> Dict[str, Any]:
        """Initialize universal task structure from DEV_PLAN.md"""
        print("📋 Initializing Universal Task Management from DEV_PLAN.md")

        # Read and analyze DEV_PLAN.md
        dev_plan_path = self.project_path / "DEV_PLAN.md"
        if not dev_plan_path.exists():
            print("⚠️  DEV_PLAN.md not found, creating adaptive structure")
            return self._create_adaptive_structure()

        # Parse plan and create universal structure
        return self._parse_and_create_universal_structure(dev_plan_path)

    def _parse_and_create_universal_structure(
        self, dev_plan_path: Path
    ) -> Dict[str, Any]:
        """Parse DEV_PLAN.md and create adaptive task structure"""
        try:
            content = dev_plan_path.read_text()

            # Extract project information
            self.project_config = self._extract_project_info(content)

            # Parse existing phases from DEV_PLAN.md
            phases = self._extract_phases_from_content(content)

            # Create 3-level adaptive structure
            self.task_structure["project_type"] = self.project_config.get(
                "type", "universal"
            )
            self.task_structure["technologies"] = self.project_config.get(
                "technologies", []
            )
            self.task_structure["phases"] = self._create_3_level_tasks(phases)

            # Count total tasks
            self._count_total_tasks()

            print(f"✅ Parsed {len(self.task_structure['phases'])} phases")
            print(f"📊 Total tasks: {self.task_structure['total_tasks']}")

            return self.task_structure

        except Exception as e:
            print(f"⚠️  Error parsing DEV_PLAN.md: {e}")
            return self._create_adaptive_structure()

    def _extract_project_info(self, content: str) -> Dict[str, Any]:
        """Extract project information from DEV_PLAN.md content"""
        config = {
            "type": "universal",
            "technologies": [],
            "languages": [],
            "frameworks": [],
            "requirements": {},
            "goals": [],
        }

        # Extract project type
        if any(
            keyword in content.lower()
            for keyword in ["web", "frontend", "backend", "api"]
        ):
            config["type"] = "web_application"
        elif any(
            keyword in content.lower()
            for keyword in ["gui", "desktop", "qt", "tkinter"]
        ):
            config["type"] = "desktop_application"
        elif any(
            keyword in content.lower() for keyword in ["cli", "command", "terminal"]
        ):
            config["type"] = "cli_application"
        elif any(
            keyword in content.lower() for keyword in ["agent", "ai", "ml", "learning"]
        ):
            config["type"] = "ai_system"
        elif any(
            keyword in content.lower() for keyword in ["library", "package", "module"]
        ):
            config["type"] = "library"

        # Extract languages
        languages = re.findall(
            r"\\b(Python|JavaScript|TypeScript|Java|Go|Rust|C\\+\\+|C#|PHP|Ruby|Swift|Kotlin)\\b",
            content,
            re.IGNORECASE,
        )
        config["languages"] = list(set(lang.lower() for lang in languages))

        # Extract frameworks and technologies
        frameworks = re.findall(
            r"\\b(React|Vue|Angular|Django|Flask|Express|Spring|Laravel|Rails|SwiftUI|Flutter|PySide6|Qt|Electron|FastAPI)\\b",
            content,
            re.IGNORECASE,
        )
        config["frameworks"] = list(set(fw.lower() for fw in frameworks))

        # Extract version requirements (no hardcoding)
        versions = re.findall(
            r"(Python|Node|Java|Go)\\s*(\\d+\\.?\\d*)", content, re.IGNORECASE
        )
        for lang, version in versions:
            config["requirements"][lang.lower()] = version

        # Combine all technologies
        config["technologies"] = config["languages"] + config["frameworks"]

        return config

    def _extract_phases_from_content(self, content: str) -> List[Dict[str, Any]]:
        """Extract phases from DEV_PLAN.md content"""
        phases = []

        # Look for numbered sections (## 1. Phase Name, ## 2. Phase Name, etc.)
        phase_pattern = r"^##\\s*(\\d+)\\.\\s*(.+)$"
        subtask_pattern = r"^###\\s*(.+)$"
        task_pattern = r"^-\\s*\\[\\s*\\]\\s*(.+)$"

        current_phase = None
        current_subtask = None

        for line in content.split("\\n"):
            line = line.strip()

            # Check for phase headers
            phase_match = re.match(phase_pattern, line)
            if phase_match:
                if current_phase:
                    phases.append(current_phase)

                phase_num = int(phase_match.group(1))
                phase_name = phase_match.group(2).strip()

                current_phase = {
                    "id": phase_num,
                    "name": phase_name,
                    "description": "",
                    "status": "pending",
                    "subtasks": [],
                }
                current_subtask = None
                continue

            # Check for subtask headers
            subtask_match = re.match(subtask_pattern, line)
            if subtask_match and current_phase:
                if current_subtask:
                    current_phase["subtasks"].append(current_subtask)

                subtask_name = subtask_match.group(1).strip()
                current_subtask = {"name": subtask_name, "description": "", "tasks": []}
                continue

            # Check for individual tasks
            task_match = re.match(task_pattern, line)
            if task_match and current_subtask:
                task_name = task_match.group(1).strip()
                current_subtask["tasks"].append(
                    {"name": task_name, "status": "pending"}
                )
                continue

            # Add to description if we're in a phase or subtask
            if line and not line.startswith("#") and not line.startswith("-"):
                if current_subtask:
                    current_subtask["description"] += line + " "
                elif current_phase:
                    current_phase["description"] += line + " "

        # Add the last phase
        if current_phase:
            if current_subtask:
                current_phase["subtasks"].append(current_subtask)
            phases.append(current_phase)

        return phases

    def _create_3_level_tasks(
        self, phases: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create 3-level task structure from extracted phases"""
        structured_phases = []

        for phase in phases:
            phase_id = phase.get("id", len(structured_phases) + 1)

            structured_phase = {
                "id": phase_id,
                "name": phase["name"],
                "description": phase["description"].strip(),
                "status": "pending",
                "level_1_tasks": [],
            }

            # Convert subtasks to level_1_tasks
            for i, subtask in enumerate(phase.get("subtasks", []), 1):
                level_1_id = f"{phase_id}.{i}"

                level_1_task = {
                    "id": level_1_id,
                    "name": subtask["name"],
                    "description": subtask["description"].strip(),
                    "status": "pending",
                    "level_2_tasks": [],
                }

                # Convert tasks to level_2_tasks and auto-generate level_3_tasks
                for j, task in enumerate(subtask.get("tasks", []), 1):
                    level_2_id = f"{level_1_id}.{j}"

                    level_2_task = {
                        "id": level_2_id,
                        "name": task["name"],
                        "status": task.get("status", "pending"),
                        "level_3_tasks": self._generate_level_3_tasks(
                            task["name"], level_2_id
                        ),
                    }

                    level_1_task["level_2_tasks"].append(level_2_task)

                # If no level_2 tasks were found, create some based on the subtask name
                if not level_1_task["level_2_tasks"]:
                    level_1_task["level_2_tasks"] = self._generate_level_2_tasks(
                        subtask["name"], level_1_id
                    )

                structured_phase["level_1_tasks"].append(level_1_task)

            # If no level_1 tasks were found, create some based on the phase name
            if not structured_phase["level_1_tasks"]:
                structured_phase["level_1_tasks"] = self._generate_level_1_tasks(
                    phase["name"], phase_id
                )

            structured_phases.append(structured_phase)

        return structured_phases

    def _generate_level_1_tasks(
        self, phase_name: str, phase_id: int
    ) -> List[Dict[str, Any]]:
        """Generate Level 1 tasks based on phase name and project type"""
        tasks = []

        # Universal task generation based on phase content
        if any(
            keyword in phase_name.lower()
            for keyword in ["setup", "initialization", "environment"]
        ):
            tasks.extend(
                [
                    {
                        "id": f"{phase_id}.1",
                        "name": "Environment Configuration",
                        "description": "Setup development environment",
                        "status": "pending",
                        "level_2_tasks": self._generate_environment_tasks(
                            f"{phase_id}.1"
                        ),
                    },
                    {
                        "id": f"{phase_id}.2",
                        "name": "Project Structure Setup",
                        "description": "Create project directory structure",
                        "status": "pending",
                        "level_2_tasks": self._generate_structure_tasks(
                            f"{phase_id}.2"
                        ),
                    },
                ]
            )
        elif any(
            keyword in phase_name.lower()
            for keyword in ["core", "component", "development"]
        ):
            tasks.extend(
                [
                    {
                        "id": f"{phase_id}.1",
                        "name": "Core Component Implementation",
                        "description": "Implement main components",
                        "status": "pending",
                        "level_2_tasks": self._generate_component_tasks(
                            f"{phase_id}.1"
                        ),
                    },
                    {
                        "id": f"{phase_id}.2",
                        "name": "Integration Setup",
                        "description": "Setup component integration",
                        "status": "pending",
                        "level_2_tasks": self._generate_integration_tasks(
                            f"{phase_id}.2"
                        ),
                    },
                ]
            )
        elif any(
            keyword in phase_name.lower()
            for keyword in ["test", "validation", "quality"]
        ):
            tasks.extend(
                [
                    {
                        "id": f"{phase_id}.1",
                        "name": "Testing Framework Setup",
                        "description": "Setup testing infrastructure",
                        "status": "pending",
                        "level_2_tasks": self._generate_testing_tasks(f"{phase_id}.1"),
                    },
                    {
                        "id": f"{phase_id}.2",
                        "name": "Quality Assurance",
                        "description": "Implement QA processes",
                        "status": "pending",
                        "level_2_tasks": self._generate_qa_tasks(f"{phase_id}.2"),
                    },
                ]
            )
        else:
            # Generic tasks for unrecognized phases
            tasks.append(
                {
                    "id": f"{phase_id}.1",
                    "name": f"Implement {phase_name}",
                    "description": f"Implementation tasks for {phase_name}",
                    "status": "pending",
                    "level_2_tasks": self._generate_generic_tasks(
                        f"{phase_id}.1", phase_name
                    ),
                }
            )

        return tasks

    def _generate_level_2_tasks(
        self, task_name: str, parent_id: str
    ) -> List[Dict[str, Any]]:
        """Generate Level 2 tasks based on task name and context"""
        tasks = []

        # Analyze task name to generate appropriate subtasks
        if any(
            keyword in task_name.lower()
            for keyword in ["install", "setup", "configure"]
        ):
            tasks.extend(
                [
                    {
                        "id": f"{parent_id}.1",
                        "name": f"Prerequisites for {task_name}",
                        "status": "pending",
                        "level_3_tasks": self._generate_prerequisite_tasks(
                            f"{parent_id}.1"
                        ),
                    },
                    {
                        "id": f"{parent_id}.2",
                        "name": f"Execute {task_name}",
                        "status": "pending",
                        "level_3_tasks": self._generate_execution_tasks(
                            f"{parent_id}.2"
                        ),
                    },
                    {
                        "id": f"{parent_id}.3",
                        "name": f"Verify {task_name}",
                        "status": "pending",
                        "level_3_tasks": self._generate_verification_tasks(
                            f"{parent_id}.3"
                        ),
                    },
                ]
            )
        elif any(
            keyword in task_name.lower()
            for keyword in ["create", "implement", "develop"]
        ):
            tasks.extend(
                [
                    {
                        "id": f"{parent_id}.1",
                        "name": f"Design {task_name}",
                        "status": "pending",
                        "level_3_tasks": self._generate_design_tasks(f"{parent_id}.1"),
                    },
                    {
                        "id": f"{parent_id}.2",
                        "name": f"Code {task_name}",
                        "status": "pending",
                        "level_3_tasks": self._generate_coding_tasks(f"{parent_id}.2"),
                    },
                    {
                        "id": f"{parent_id}.3",
                        "name": f"Test {task_name}",
                        "status": "pending",
                        "level_3_tasks": self._generate_testing_subtasks(
                            f"{parent_id}.3"
                        ),
                    },
                ]
            )
        else:
            # Generic level 2 tasks
            tasks.extend(
                [
                    {
                        "id": f"{parent_id}.1",
                        "name": f"Prepare {task_name}",
                        "status": "pending",
                        "level_3_tasks": self._generate_preparation_tasks(
                            f"{parent_id}.1"
                        ),
                    },
                    {
                        "id": f"{parent_id}.2",
                        "name": f"Execute {task_name}",
                        "status": "pending",
                        "level_3_tasks": self._generate_execution_tasks(
                            f"{parent_id}.2"
                        ),
                    },
                ]
            )

        return tasks

    def _generate_level_3_tasks(
        self, task_name: str, parent_id: str
    ) -> List[Dict[str, Any]]:
        """Generate Level 3 tasks (atomic actions)"""
        tasks = []

        # Generate specific atomic tasks based on the task name
        if "environment" in task_name.lower():
            tasks.extend(
                [
                    {
                        "id": f"{parent_id}.1",
                        "name": "Check system requirements",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.2",
                        "name": "Setup development tools",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.3",
                        "name": "Configure environment variables",
                        "status": "pending",
                    },
                ]
            )
        elif "install" in task_name.lower() or "dependencies" in task_name.lower():
            tasks.extend(
                [
                    {
                        "id": f"{parent_id}.1",
                        "name": "Check package manager",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.2",
                        "name": "Install required packages",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.3",
                        "name": "Verify installation",
                        "status": "pending",
                    },
                ]
            )
        elif "create" in task_name.lower() or "file" in task_name.lower():
            tasks.extend(
                [
                    {
                        "id": f"{parent_id}.1",
                        "name": "Define file structure",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.2",
                        "name": "Create file content",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.3",
                        "name": "Validate file creation",
                        "status": "pending",
                    },
                ]
            )
        elif "test" in task_name.lower():
            tasks.extend(
                [
                    {
                        "id": f"{parent_id}.1",
                        "name": "Write test cases",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.2",
                        "name": "Execute tests",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.3",
                        "name": "Analyze test results",
                        "status": "pending",
                    },
                ]
            )
        else:
            # Generic atomic tasks
            tasks.extend(
                [
                    {
                        "id": f"{parent_id}.1",
                        "name": f"Initialize {task_name}",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.2",
                        "name": f"Process {task_name}",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.3",
                        "name": f"Complete {task_name}",
                        "status": "pending",
                    },
                ]
            )

        return tasks

    def _generate_environment_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate environment-specific tasks based on project configuration"""
        tasks = []

        # Adapt to detected technologies
        if "python" in self.project_config.get("languages", []):
            version = self.project_config.get("requirements", {}).get("python", "3.8+")
            tasks.append(
                {
                    "id": f"{parent_id}.1",
                    "name": f"Setup Python {version} Environment",
                    "status": "pending",
                    "level_3_tasks": [
                        {
                            "id": f"{parent_id}.1.1",
                            "name": f"Check Python {version} availability",
                            "status": "pending",
                        },
                        {
                            "id": f"{parent_id}.1.2",
                            "name": "Create virtual environment",
                            "status": "pending",
                        },
                        {
                            "id": f"{parent_id}.1.3",
                            "name": "Activate environment",
                            "status": "pending",
                        },
                    ],
                }
            )

        if "javascript" in self.project_config.get(
            "languages", []
        ) or "typescript" in self.project_config.get("languages", []):
            tasks.append(
                {
                    "id": f"{parent_id}.2",
                    "name": "Setup Node.js Environment",
                    "status": "pending",
                    "level_3_tasks": [
                        {
                            "id": f"{parent_id}.2.1",
                            "name": "Check Node.js availability",
                            "status": "pending",
                        },
                        {
                            "id": f"{parent_id}.2.2",
                            "name": "Initialize npm project",
                            "status": "pending",
                        },
                        {
                            "id": f"{parent_id}.2.3",
                            "name": "Configure package.json",
                            "status": "pending",
                        },
                    ],
                }
            )

        if not tasks:
            # Generic environment tasks
            tasks.append(
                {
                    "id": f"{parent_id}.1",
                    "name": "Setup Development Environment",
                    "status": "pending",
                    "level_3_tasks": [
                        {
                            "id": f"{parent_id}.1.1",
                            "name": "Check system requirements",
                            "status": "pending",
                        },
                        {
                            "id": f"{parent_id}.1.2",
                            "name": "Configure development tools",
                            "status": "pending",
                        },
                        {
                            "id": f"{parent_id}.1.3",
                            "name": "Verify environment setup",
                            "status": "pending",
                        },
                    ],
                }
            )

        return tasks

    def _generate_structure_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate project structure tasks"""
        return [
            {
                "id": f"{parent_id}.1",
                "name": "Create Directory Structure",
                "status": "pending",
                "level_3_tasks": [
                    {
                        "id": f"{parent_id}.1.1",
                        "name": "Create src directory",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.1.2",
                        "name": "Create tests directory",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.1.3",
                        "name": "Create docs directory",
                        "status": "pending",
                    },
                ],
            },
            {
                "id": f"{parent_id}.2",
                "name": "Initialize Configuration Files",
                "status": "pending",
                "level_3_tasks": [
                    {
                        "id": f"{parent_id}.2.1",
                        "name": "Create main config file",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.2.2",
                        "name": "Setup gitignore",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.2.3",
                        "name": "Initialize README",
                        "status": "pending",
                    },
                ],
            },
        ]

    def _generate_component_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate component implementation tasks"""
        return [
            {
                "id": f"{parent_id}.1",
                "name": "Design Component Architecture",
                "status": "pending",
                "level_3_tasks": self._generate_design_tasks(f"{parent_id}.1"),
            },
            {
                "id": f"{parent_id}.2",
                "name": "Implement Core Components",
                "status": "pending",
                "level_3_tasks": self._generate_coding_tasks(f"{parent_id}.2"),
            },
        ]

    def _generate_integration_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate integration tasks"""
        return [
            {
                "id": f"{parent_id}.1",
                "name": "Setup Component Integration",
                "status": "pending",
                "level_3_tasks": [
                    {
                        "id": f"{parent_id}.1.1",
                        "name": "Define interfaces",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.1.2",
                        "name": "Create integration layer",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.1.3",
                        "name": "Test integration",
                        "status": "pending",
                    },
                ],
            }
        ]

    def _generate_testing_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate testing framework tasks"""
        return [
            {
                "id": f"{parent_id}.1",
                "name": "Setup Testing Framework",
                "status": "pending",
                "level_3_tasks": self._generate_testing_subtasks(f"{parent_id}.1"),
            }
        ]

    def _generate_qa_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate QA tasks"""
        return [
            {
                "id": f"{parent_id}.1",
                "name": "Code Quality Checks",
                "status": "pending",
                "level_3_tasks": [
                    {
                        "id": f"{parent_id}.1.1",
                        "name": "Setup linting",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.1.2",
                        "name": "Configure code formatting",
                        "status": "pending",
                    },
                    {
                        "id": f"{parent_id}.1.3",
                        "name": "Run quality checks",
                        "status": "pending",
                    },
                ],
            }
        ]

    def _generate_generic_tasks(
        self, parent_id: str, phase_name: str
    ) -> List[Dict[str, Any]]:
        """Generate generic tasks for unrecognized phases"""
        return [
            {
                "id": f"{parent_id}.1",
                "name": f"Plan {phase_name}",
                "status": "pending",
                "level_3_tasks": self._generate_planning_tasks(f"{parent_id}.1"),
            },
            {
                "id": f"{parent_id}.2",
                "name": f"Execute {phase_name}",
                "status": "pending",
                "level_3_tasks": self._generate_execution_tasks(f"{parent_id}.2"),
            },
        ]

    def _generate_prerequisite_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate prerequisite check tasks"""
        return [
            {
                "id": f"{parent_id}.1",
                "name": "Check system requirements",
                "status": "pending",
            },
            {
                "id": f"{parent_id}.2",
                "name": "Verify dependencies",
                "status": "pending",
            },
            {
                "id": f"{parent_id}.3",
                "name": "Prepare environment",
                "status": "pending",
            },
        ]

    def _generate_execution_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate execution tasks"""
        return [
            {"id": f"{parent_id}.1", "name": "Start execution", "status": "pending"},
            {"id": f"{parent_id}.2", "name": "Monitor progress", "status": "pending"},
            {"id": f"{parent_id}.3", "name": "Complete execution", "status": "pending"},
        ]

    def _generate_verification_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate verification tasks"""
        return [
            {"id": f"{parent_id}.1", "name": "Validate results", "status": "pending"},
            {
                "id": f"{parent_id}.2",
                "name": "Check functionality",
                "status": "pending",
            },
            {"id": f"{parent_id}.3", "name": "Confirm completion", "status": "pending"},
        ]

    def _generate_design_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate design tasks"""
        return [
            {
                "id": f"{parent_id}.1",
                "name": "Create design specifications",
                "status": "pending",
            },
            {
                "id": f"{parent_id}.2",
                "name": "Review design patterns",
                "status": "pending",
            },
            {"id": f"{parent_id}.3", "name": "Finalize design", "status": "pending"},
        ]

    def _generate_coding_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate coding tasks"""
        return [
            {
                "id": f"{parent_id}.1",
                "name": "Write core implementation",
                "status": "pending",
            },
            {"id": f"{parent_id}.2", "name": "Add error handling", "status": "pending"},
            {
                "id": f"{parent_id}.3",
                "name": "Code review and cleanup",
                "status": "pending",
            },
        ]

    def _generate_testing_subtasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate testing subtasks"""
        return [
            {"id": f"{parent_id}.1", "name": "Write unit tests", "status": "pending"},
            {"id": f"{parent_id}.2", "name": "Execute test suite", "status": "pending"},
            {
                "id": f"{parent_id}.3",
                "name": "Analyze test coverage",
                "status": "pending",
            },
        ]

    def _generate_preparation_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate preparation tasks"""
        return [
            {
                "id": f"{parent_id}.1",
                "name": "Gather requirements",
                "status": "pending",
            },
            {"id": f"{parent_id}.2", "name": "Prepare resources", "status": "pending"},
            {"id": f"{parent_id}.3", "name": "Setup workspace", "status": "pending"},
        ]

    def _generate_planning_tasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Generate planning tasks"""
        return [
            {"id": f"{parent_id}.1", "name": "Define objectives", "status": "pending"},
            {"id": f"{parent_id}.2", "name": "Create timeline", "status": "pending"},
            {"id": f"{parent_id}.3", "name": "Allocate resources", "status": "pending"},
        ]

    def _create_adaptive_structure(self) -> Dict[str, Any]:
        """Create adaptive task structure when DEV_PLAN.md is missing"""
        self.task_structure = {
            "project_type": "universal",
            "technologies": [],
            "phases": [
                {
                    "id": 1,
                    "name": "Project Initialization",
                    "description": "Setup universal project environment",
                    "status": "pending",
                    "level_1_tasks": [
                        {
                            "id": "1.1",
                            "name": "Environment Analysis",
                            "description": "Analyze and setup development environment",
                            "status": "pending",
                            "level_2_tasks": [
                                {
                                    "id": "1.1.1",
                                    "name": "Detect Available Technologies",
                                    "status": "pending",
                                    "level_3_tasks": [
                                        {
                                            "id": "1.1.1.1",
                                            "name": "Check programming language runtimes",
                                            "status": "pending",
                                        },
                                        {
                                            "id": "1.1.1.2",
                                            "name": "Detect available frameworks",
                                            "status": "pending",
                                        },
                                        {
                                            "id": "1.1.1.3",
                                            "name": "Identify system capabilities",
                                            "status": "pending",
                                        },
                                    ],
                                },
                                {
                                    "id": "1.1.2",
                                    "name": "Setup Development Environment",
                                    "status": "pending",
                                    "level_3_tasks": [
                                        {
                                            "id": "1.1.2.1",
                                            "name": "Configure project workspace",
                                            "status": "pending",
                                        },
                                        {
                                            "id": "1.1.2.2",
                                            "name": "Initialize version control",
                                            "status": "pending",
                                        },
                                        {
                                            "id": "1.1.2.3",
                                            "name": "Setup build tools",
                                            "status": "pending",
                                        },
                                    ],
                                },
                            ],
                        }
                    ],
                },
                {
                    "id": 2,
                    "name": "Universal Project Setup",
                    "description": "Create adaptive project structure",
                    "status": "pending",
                    "level_1_tasks": [
                        {
                            "id": "2.1",
                            "name": "Adaptive Structure Creation",
                            "description": "Create project structure based on detected requirements",
                            "status": "pending",
                            "level_2_tasks": [
                                {
                                    "id": "2.1.1",
                                    "name": "Create Base Directories",
                                    "status": "pending",
                                    "level_3_tasks": [
                                        {
                                            "id": "2.1.1.1",
                                            "name": "Create src directory",
                                            "status": "pending",
                                        },
                                        {
                                            "id": "2.1.1.2",
                                            "name": "Create tests directory",
                                            "status": "pending",
                                        },
                                        {
                                            "id": "2.1.1.3",
                                            "name": "Create docs directory",
                                            "status": "pending",
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                },
            ],
            "current_phase": 0,
            "total_tasks": 0,
            "completed_tasks": 0,
            "auto_generated_subtasks": [],
        }

        self._count_total_tasks()
        return self.task_structure

    def _count_total_tasks(self):
        """Count total tasks in the structure"""
        total = 0
        for phase in self.task_structure["phases"]:
            for level_1 in phase.get("level_1_tasks", []):
                for level_2 in level_1.get("level_2_tasks", []):
                    total += len(level_2.get("level_3_tasks", []))

        self.task_structure["total_tasks"] = total

    def print_task_summary(self):
        """Print a summary of the task structure"""
        print("\\n📋 Universal Task Structure Summary")
        print("=" * 50)
        print(f"Project Type: {self.task_structure.get('project_type', 'Universal')}")
        print(
            f"Technologies: {', '.join(self.task_structure.get('technologies', ['Auto-detect']))}"
        )
        print(f"Total Phases: {len(self.task_structure['phases'])}")
        print(f"Total Tasks: {self.task_structure['total_tasks']}")

        for phase in self.task_structure["phases"]:
            print(f"\\n📁 Phase {phase['id']}: {phase['name']}")
            for level_1 in phase.get("level_1_tasks", []):
                print(f"  📝 {level_1['id']}: {level_1['name']}")
                for level_2 in level_1.get("level_2_tasks", []):
                    print(f"    🔧 {level_2['id']}: {level_2['name']}")
                    level_3_count = len(level_2.get("level_3_tasks", []))
                    if level_3_count > 0:
                        print(f"      ⚡ {level_3_count} atomic tasks")

    def save_task_structure(
        self, filename: str = "UNIVERSAL_TASK_STRUCTURE.json"
    ) -> str:
        """Save the task structure to a JSON file"""
        try:
            output_path = self.project_path / filename
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(self.task_structure, f, indent=2, ensure_ascii=False)

            print(f"💾 Task structure saved to: {output_path}")
            return str(output_path)

        except Exception as e:
            print(f"❌ Failed to save task structure: {e}")
            return ""

    def analyze_system_and_add_tasks(self, analysis_report: Dict[str, Any]):
        """Add tasks based on system analysis"""
        print("🤖 Analyzing system and adding adaptive tasks...")

        # Extract issues and add corresponding tasks
        issues = analysis_report.get("issues", [])
        new_tasks = []

        for issue in issues:
            if issue.get("severity") in ["high", "critical"]:
                task_id = (
                    f"auto_{len(self.task_structure['auto_generated_subtasks']) + 1}"
                )
                new_task = {
                    "id": task_id,
                    "name": f"Resolve: {issue['description']}",
                    "type": "auto_generated",
                    "severity": issue["severity"],
                    "status": "pending",
                    "source": "system_analysis",
                }
                new_tasks.append(new_task)

        # Add system improvement tasks
        system_info = analysis_report.get("system_info", {})
        if system_info:
            improvement_task = {
                "id": f"auto_{len(self.task_structure['auto_generated_subtasks']) + len(new_tasks) + 1}",
                "name": "System Optimization",
                "type": "auto_generated",
                "status": "pending",
                "source": "system_analysis",
                "details": "Optimize system based on analysis",
            }
            new_tasks.append(improvement_task)

        self.task_structure["auto_generated_subtasks"].extend(new_tasks)
        print(f"✅ Added {len(new_tasks)} adaptive tasks based on system analysis")

    def execute_next_task(self) -> Optional[Dict[str, Any]]:
        """Execute the next pending task"""
        # Find next pending task
        for phase in self.task_structure["phases"]:
            if phase["status"] != "completed":
                for level_1 in phase.get("level_1_tasks", []):
                    if level_1["status"] != "completed":
                        for level_2 in level_1.get("level_2_tasks", []):
                            if level_2["status"] != "completed":
                                for level_3 in level_2.get("level_3_tasks", []):
                                    if level_3["status"] == "pending":
                                        return {
                                            "task": level_3,
                                            "level": 3,
                                            "parent_level_2": level_2,
                                            "parent_level_1": level_1,
                                            "parent_phase": phase,
                                        }

        return None

    def register_creative_hook(self, hook_function):
        """Register a creative hook for task generation"""
        self.creative_hooks.append(hook_function)
        print(f"🎨 Registered creative hook: {hook_function.__name__}")

    def apply_creative_extensions(
        self, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Apply creative hooks to extend task generation"""
        extensions = []

        for hook in self.creative_hooks:
            try:
                result = hook(context)
                if result:
                    extensions.extend(result if isinstance(result, list) else [result])
            except Exception as e:
                print(f"⚠️  Creative hook failed: {e}")

        return extensions


# Alias for backwards compatibility
AdvancedTaskManager = UniversalTaskManager
