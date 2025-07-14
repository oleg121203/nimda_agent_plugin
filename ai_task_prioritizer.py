#!/usr/bin/env python3
"""
AI-Driven Task Prioritizer - Intelligent task management with machine learning
Features:
- Context-aware task prioritization
- Learning from user behavior
- Adaptive scheduling based on workload
- Creative problem-solving for complex tasks
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

from creative_hooks_examples import CreativeHookRegistry


class AITaskPrioritizer:
    """
    Intelligent task prioritizer using AI and machine learning
    """

    def __init__(self, project_path: str = "/Users/dev/Documents/nimda_agent_plugin"):
        self.project_path = Path(project_path)
        self.creative_hooks = CreativeHookRegistry()

        # Task management state
        self.tasks = []
        self.completed_tasks = []
        self.task_history = []
        self.user_patterns = {}
        self.context_weights = {
            "urgency": 0.3,
            "complexity": 0.2,
            "dependencies": 0.25,
            "user_preference": 0.15,
            "resource_availability": 0.1,
        }

        # Learning system
        self.learning_enabled = True
        self.adaptation_threshold = 5  # Minimum tasks to start learning

        # Load previous data
        self._load_historical_data()

    def add_task(self, task: Dict[str, Any]) -> str:
        """Add a new task with AI-driven metadata extraction"""
        task_id = f"task_{int(time.time())}_{len(self.tasks)}"

        enhanced_task = {
            "id": task_id,
            "title": task.get("title", "Unnamed Task"),
            "description": task.get("description", ""),
            "priority": task.get("priority", "medium"),
            "estimated_time": task.get("estimated_time", 60),  # minutes
            "dependencies": task.get("dependencies", []),
            "tags": task.get("tags", []),
            "created_at": datetime.now().isoformat(),
            "status": "pending",
            "context": self._extract_task_context(task),
            "ai_score": 0.0,
            "user_interaction_count": 0,
        }

        # Use creative hooks for intelligent task enhancement
        enhanced_task = self._enhance_task_with_ai(enhanced_task)

        self.tasks.append(enhanced_task)
        self._save_data()

        print(f"✅ Added task: {enhanced_task['title']} (ID: {task_id})")
        return task_id

    def _extract_task_context(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Extract contextual information from task using AI"""
        context = {
            "type": "general",
            "domain": "unknown",
            "urgency_indicators": [],
            "complexity_factors": [],
            "resource_requirements": [],
        }

        description = (
            task.get("description", "") + " " + task.get("title", "")
        ).lower()

        # AI-driven context extraction
        if any(
            word in description for word in ["bug", "fix", "error", "issue", "broken"]
        ):
            context["type"] = "bugfix"
            context["urgency_indicators"].append("error_correction")

        elif any(
            word in description for word in ["feature", "new", "implement", "add"]
        ):
            context["type"] = "feature_development"
            context["complexity_factors"].append("new_implementation")

        elif any(
            word in description for word in ["test", "testing", "validate", "verify"]
        ):
            context["type"] = "testing"
            context["complexity_factors"].append("validation_required")

        elif any(
            word in description
            for word in ["deploy", "release", "production", "launch"]
        ):
            context["type"] = "deployment"
            context["urgency_indicators"].append("release_critical")

        # Domain detection
        if any(
            word in description
            for word in ["ai", "ml", "machine learning", "neural", "model"]
        ):
            context["domain"] = "artificial_intelligence"
            context["complexity_factors"].append("ai_complexity")

        elif any(
            word in description
            for word in ["gui", "interface", "ui", "frontend", "design"]
        ):
            context["domain"] = "user_interface"
            context["resource_requirements"].append("design_skills")

        elif any(
            word in description for word in ["database", "db", "sql", "data", "storage"]
        ):
            context["domain"] = "data_management"
            context["resource_requirements"].append("database_expertise")

        return context

    def _enhance_task_with_ai(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance task using creative hooks and AI analysis"""
        try:
            # Use creative hooks for task enhancement
            enhancement_context = {
                "action": "enhance_task",
                "task": task,
                "project_config": {"type": "ai_system"},
            }

            # Apply creative enhancement if available
            creative_result = self.creative_hooks.creative_solution_hook(
                enhancement_context
            )

            if creative_result:
                print(f"🎨 Enhanced task '{task['title']}' with creative AI")

        except Exception as e:
            print(f"⚠️ Task enhancement warning: {e}")

        return task

    def prioritize_tasks(self) -> List[Dict[str, Any]]:
        """Prioritize all pending tasks using AI algorithms"""
        pending_tasks = [t for t in self.tasks if t["status"] == "pending"]

        if not pending_tasks:
            return []

        print(f"🧠 Prioritizing {len(pending_tasks)} tasks with AI...")

        # Calculate AI scores for each task
        for task in pending_tasks:
            task["ai_score"] = self._calculate_ai_score(task)

        # Sort by AI score (higher is better)
        prioritized = sorted(pending_tasks, key=lambda x: x["ai_score"], reverse=True)

        # Apply learning-based adjustments
        if (
            self.learning_enabled
            and len(self.completed_tasks) >= self.adaptation_threshold
        ):
            prioritized = self._apply_learning_adjustments(prioritized)

        print(f"✅ Tasks prioritized. Top task: {prioritized[0]['title']}")
        return prioritized

    def _calculate_ai_score(self, task: Dict[str, Any]) -> float:
        """Calculate AI-driven priority score for a task"""
        score = 0.0
        context = task.get("context", {})

        # Base priority score
        priority_scores = {"high": 1.0, "medium": 0.6, "low": 0.3}
        score += (
            priority_scores.get(task.get("priority", "medium"), 0.6)
            * self.context_weights["urgency"]
        )

        # Urgency indicators
        urgency_count = len(context.get("urgency_indicators", []))
        score += min(urgency_count * 0.2, 0.5) * self.context_weights["urgency"]

        # Complexity factors (inverse relationship - simpler tasks get higher scores for quick wins)
        complexity_count = len(context.get("complexity_factors", []))
        complexity_score = max(0.1, 1.0 - (complexity_count * 0.15))
        score += complexity_score * self.context_weights["complexity"]

        # Dependencies (fewer dependencies = higher score)
        dep_count = len(task.get("dependencies", []))
        dep_score = max(0.1, 1.0 - (dep_count * 0.2))
        score += dep_score * self.context_weights["dependencies"]

        # User preference learning
        if self.learning_enabled:
            user_pref_score = self._get_user_preference_score(task)
            score += user_pref_score * self.context_weights["user_preference"]

        # Resource availability
        resource_score = self._assess_resource_availability(task)
        score += resource_score * self.context_weights["resource_availability"]

        # Time-based adjustments
        score = self._apply_time_based_adjustments(task, score)

        return round(score, 3)

    def _get_user_preference_score(self, task: Dict[str, Any]) -> float:
        """Get user preference score based on historical patterns"""
        task_type = task.get("context", {}).get("type", "general")
        domain = task.get("context", {}).get("domain", "unknown")

        # Check user patterns
        type_preference = self.user_patterns.get(f"type_{task_type}", 0.5)
        domain_preference = self.user_patterns.get(f"domain_{domain}", 0.5)

        return (type_preference + domain_preference) / 2

    def _assess_resource_availability(self, task: Dict[str, Any]) -> float:
        """Assess current resource availability for the task"""
        # Simplified resource assessment
        current_hour = datetime.now().hour

        # Higher scores during typical work hours
        if 9 <= current_hour <= 17:
            return 1.0
        elif 18 <= current_hour <= 22:
            return 0.7
        else:
            return 0.3

    def _apply_time_based_adjustments(
        self, task: Dict[str, Any], base_score: float
    ) -> float:
        """Apply time-based adjustments to the score"""
        created_at = datetime.fromisoformat(task["created_at"])
        age_hours = (datetime.now() - created_at).total_seconds() / 3600

        # Slightly increase score for older tasks (anti-starvation)
        age_bonus = min(age_hours * 0.01, 0.2)

        return base_score + age_bonus

    def _apply_learning_adjustments(
        self, prioritized_tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Apply learning-based adjustments to task prioritization"""
        print("🧠 Applying learning-based adjustments...")

        # Analyze completion patterns
        self._update_user_patterns()

        # Re-score with updated patterns
        for task in prioritized_tasks:
            original_score = task["ai_score"]
            task["ai_score"] = self._calculate_ai_score(task)

            if task["ai_score"] != original_score:
                print(
                    f"   📊 Adjusted score for '{task['title']}': {original_score:.3f} → {task['ai_score']:.3f}"
                )

        # Re-sort with new scores
        return sorted(prioritized_tasks, key=lambda x: x["ai_score"], reverse=True)

    def _update_user_patterns(self):
        """Update user patterns based on completed tasks"""
        if len(self.completed_tasks) < self.adaptation_threshold:
            return

        # Analyze completion patterns
        type_counts = {}
        domain_counts = {}
        total_completed = len(self.completed_tasks)

        for task in self.completed_tasks:
            task_type = task.get("context", {}).get("type", "general")
            domain = task.get("context", {}).get("domain", "unknown")

            type_counts[task_type] = type_counts.get(task_type, 0) + 1
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

        # Calculate preferences (normalized)
        for task_type, count in type_counts.items():
            self.user_patterns[f"type_{task_type}"] = count / total_completed

        for domain, count in domain_counts.items():
            self.user_patterns[f"domain_{domain}"] = count / total_completed

    def complete_task(
        self, task_id: str, completion_data: Optional[Dict] = None
    ) -> bool:
        """Mark a task as completed and learn from the completion"""
        task_index = next(
            (i for i, t in enumerate(self.tasks) if t["id"] == task_id), None
        )

        if task_index is None:
            print(f"❌ Task {task_id} not found")
            return False

        task = self.tasks[task_index]
        task["status"] = "completed"
        task["completed_at"] = datetime.now().isoformat()

        if completion_data:
            task["actual_time"] = completion_data.get("actual_time")
            task["satisfaction_rating"] = completion_data.get("satisfaction_rating")
            task["difficulty_rating"] = completion_data.get("difficulty_rating")

        # Move to completed tasks
        self.completed_tasks.append(task)
        del self.tasks[task_index]

        # Learn from completion
        if self.learning_enabled:
            self._learn_from_completion(task)

        self._save_data()
        print(f"✅ Completed task: {task['title']}")
        return True

    def _learn_from_completion(self, task: Dict[str, Any]):
        """Learn from task completion patterns"""
        # Analyze prediction accuracy
        estimated_time = task.get("estimated_time", 60)
        actual_time = task.get("actual_time")

        if actual_time:
            accuracy = 1.0 - abs(estimated_time - actual_time) / max(
                estimated_time, actual_time
            )
            task["time_prediction_accuracy"] = accuracy

        # Update learning patterns
        satisfaction = task.get("satisfaction_rating")
        if satisfaction and satisfaction >= 4:  # High satisfaction (1-5 scale)
            task_type = task.get("context", {}).get("type", "general")
            self.user_patterns[f"type_{task_type}"] = (
                self.user_patterns.get(f"type_{task_type}", 0.5) + 0.1
            )

    def get_next_recommended_task(self) -> Optional[Dict[str, Any]]:
        """Get the next recommended task using AI prioritization"""
        prioritized = self.prioritize_tasks()

        if not prioritized:
            return None

        next_task = prioritized[0]
        next_task["user_interaction_count"] += 1

        print(
            f"🎯 Next recommended task: {next_task['title']} (Score: {next_task['ai_score']:.3f})"
        )
        return next_task

    def generate_task_insights(self) -> Dict[str, Any]:
        """Generate insights about task patterns and productivity"""
        insights = {
            "total_tasks": len(self.tasks) + len(self.completed_tasks),
            "pending_tasks": len(self.tasks),
            "completed_tasks": len(self.completed_tasks),
            "completion_rate": 0.0,
            "average_completion_time": 0.0,
            "most_productive_hours": [],
            "preferred_task_types": [],
            "learning_status": "enabled" if self.learning_enabled else "disabled",
        }

        if insights["total_tasks"] > 0:
            insights["completion_rate"] = (
                insights["completed_tasks"] / insights["total_tasks"]
            )

        if self.completed_tasks:
            # Calculate average completion time
            times = [
                t.get("actual_time", t.get("estimated_time", 60))
                for t in self.completed_tasks
            ]
            insights["average_completion_time"] = sum(times) / len(times)

            # Find most productive hours
            completion_hours = []
            for task in self.completed_tasks:
                if "completed_at" in task:
                    hour = datetime.fromisoformat(task["completed_at"]).hour
                    completion_hours.append(hour)

            if completion_hours:
                from collections import Counter

                hour_counts = Counter(completion_hours)
                insights["most_productive_hours"] = [
                    h for h, c in hour_counts.most_common(3)
                ]

        # Preferred task types
        if self.user_patterns:
            type_preferences = {
                k: v for k, v in self.user_patterns.items() if k.startswith("type_")
            }
            insights["preferred_task_types"] = sorted(
                type_preferences.items(), key=lambda x: x[1], reverse=True
            )[:3]

        return insights

    def _save_data(self):
        """Save task data and learning patterns"""
        data = {
            "tasks": self.tasks,
            "completed_tasks": self.completed_tasks,
            "user_patterns": self.user_patterns,
            "context_weights": self.context_weights,
            "last_updated": datetime.now().isoformat(),
        }

        data_file = self.project_path / "ai_task_data.json"
        with open(data_file, "w") as f:
            json.dump(data, f, indent=2)

    def _load_historical_data(self):
        """Load historical task data and patterns"""
        data_file = self.project_path / "ai_task_data.json"

        if data_file.exists():
            try:
                with open(data_file, "r") as f:
                    data = json.load(f)

                self.tasks = data.get("tasks", [])
                self.completed_tasks = data.get("completed_tasks", [])
                self.user_patterns = data.get("user_patterns", {})
                self.context_weights = data.get("context_weights", self.context_weights)

                print(
                    f"📚 Loaded {len(self.completed_tasks)} completed tasks for learning"
                )

            except Exception as e:
                print(f"⚠️ Could not load historical data: {e}")


def main():
    """Example usage of AI Task Prioritizer"""
    print("🧠 AI-Driven Task Prioritizer Demo")
    print("=" * 50)

    prioritizer = AITaskPrioritizer()

    # Add some example tasks
    sample_tasks = [
        {
            "title": "Fix critical authentication bug",
            "description": "Users cannot log in due to token validation error",
            "priority": "high",
            "estimated_time": 120,
            "tags": ["bug", "security", "urgent"],
        },
        {
            "title": "Implement new AI learning module",
            "description": "Add machine learning capabilities to the adaptive thinker",
            "priority": "medium",
            "estimated_time": 480,
            "tags": ["feature", "ai", "ml"],
        },
        {
            "title": "Update user interface theme",
            "description": "Refresh the GUI with modern design elements",
            "priority": "low",
            "estimated_time": 240,
            "tags": ["ui", "design", "enhancement"],
        },
        {
            "title": "Write unit tests for chat agent",
            "description": "Add comprehensive test coverage for chat functionality",
            "priority": "medium",
            "estimated_time": 180,
            "tags": ["testing", "quality"],
        },
    ]

    # Add tasks
    task_ids = []
    for task in sample_tasks:
        task_id = prioritizer.add_task(task)
        task_ids.append(task_id)

    print("\n🎯 Getting prioritized task list...")
    prioritized = prioritizer.prioritize_tasks()

    print("\n📊 Task Priority Ranking:")
    for i, task in enumerate(prioritized, 1):
        print(f"{i}. {task['title']} (Score: {task['ai_score']:.3f})")

    print("\n🎯 Next recommended task:")
    next_task = prioritizer.get_next_recommended_task()
    if next_task:
        print(f"   {next_task['title']}")

    print("\n📈 Task Insights:")
    insights = prioritizer.generate_task_insights()
    for key, value in insights.items():
        print(f"   {key}: {value}")


if __name__ == "__main__":
    main()
