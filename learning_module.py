"""
Enhanced Learning System v2.0
Handles pattern recognition, knowledge base management, and intelligent message processing
"""

import json
import logging
import pickle
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class LearningModule:
    """Enhanced system for learning patterns and building knowledge base with intelligent message processing"""

    def __init__(self, data_dir: Optional[Path] = None):
        self.logger = logging.getLogger("LearningModule")
        self.data_dir = data_dir or Path("data/learning")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Core data structures
        self.knowledge_base = {}
        self.learning_history = []
        self.conversation_patterns = defaultdict(list)
        self.user_preferences = {}
        self.intent_patterns = {}
        self.response_templates = {}

        # Statistics tracking
        self.interaction_stats = {
            "total_messages": 0,
            "successful_responses": 0,
            "failed_responses": 0,
            "learning_events": 0,
        }

        # Load existing data
        self._load_persistent_data()

    def _load_persistent_data(self):
        """Load learning data from persistent storage"""
        try:
            # Load knowledge base
            kb_file = self.data_dir / "knowledge_base.json"
            if kb_file.exists():
                with open(kb_file, "r", encoding="utf-8") as f:
                    self.knowledge_base = json.load(f)

            # Load learning history
            history_file = self.data_dir / "learning_history.pkl"
            if history_file.exists():
                with open(history_file, "rb") as f:
                    self.learning_history = pickle.load(f)

            # Load conversation patterns
            patterns_file = self.data_dir / "conversation_patterns.json"
            if patterns_file.exists():
                with open(patterns_file, "r", encoding="utf-8") as f:
                    loaded_patterns = json.load(f)
                    self.conversation_patterns = defaultdict(list, loaded_patterns)

            # Load user preferences
            prefs_file = self.data_dir / "user_preferences.json"
            if prefs_file.exists():
                with open(prefs_file, "r", encoding="utf-8") as f:
                    self.user_preferences = json.load(f)

            self.logger.info("Persistent learning data loaded successfully")

        except Exception as e:
            self.logger.warning(f"Error loading persistent data: {e}")

    def _save_persistent_data(self):
        """Save learning data to persistent storage"""
        try:
            # Save knowledge base
            with open(
                self.data_dir / "knowledge_base.json", "w", encoding="utf-8"
            ) as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)

            # Save learning history
            with open(self.data_dir / "learning_history.pkl", "wb") as f:
                pickle.dump(self.learning_history, f)

            # Save conversation patterns
            with open(
                self.data_dir / "conversation_patterns.json", "w", encoding="utf-8"
            ) as f:
                json.dump(
                    dict(self.conversation_patterns), f, indent=2, ensure_ascii=False
                )

            # Save user preferences
            with open(
                self.data_dir / "user_preferences.json", "w", encoding="utf-8"
            ) as f:
                json.dump(self.user_preferences, f, indent=2, ensure_ascii=False)

        except Exception as e:
            self.logger.error(f"Error saving persistent data: {e}")

    def analyze_message(
        self, message: str, context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Analyze incoming message for patterns, intent, and context"""
        try:
            analysis = {
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "context": context or {},
                "language": self._detect_language(message),
                "intent": self._extract_intent(message),
                "entities": self._extract_entities(message),
                "sentiment": self._analyze_sentiment(message),
                "complexity": self._assess_complexity(message),
                "patterns": self._find_patterns(message),
            }

            # Update conversation patterns
            self._update_conversation_patterns(analysis)

            return analysis

        except Exception as e:
            self.logger.error(f"Error analyzing message: {e}")
            return {"error": str(e), "message": message}

    def generate_response(self, message_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent response based on message analysis"""
        try:
            intent = message_analysis.get("intent", "unknown")
            language = message_analysis.get("language", "en")
            context = message_analysis.get("context", {})

            # Find appropriate response template
            response_template = self._get_response_template(intent, language)

            # Generate contextual response
            response = self._generate_contextual_response(
                message_analysis, response_template, context
            )

            # Track response generation
            self.interaction_stats["total_messages"] += 1

            return {
                "response": response,
                "confidence": response.get("confidence", 0.7),
                "intent": intent,
                "language": language,
                "generated_at": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            self.interaction_stats["failed_responses"] += 1
            return {
                "response": "Вибачте, я не можу обробити ваш запит зараз. Спробуйте ще раз.",
                "error": str(e),
            }

    def _detect_language(self, text: str) -> str:
        """Detect language of the text"""
        # Simple language detection based on character patterns
        cyrillic_pattern = re.compile(r"[а-яё]", re.IGNORECASE)
        ukrainian_pattern = re.compile(r"[іїєґ]", re.IGNORECASE)

        if ukrainian_pattern.search(text):
            return "uk"
        elif cyrillic_pattern.search(text):
            return "ru"
        else:
            return "en"

    def _extract_intent(self, message: str) -> str:
        """Extract user intent from message"""
        message_lower = message.lower()

        # Define intent patterns
        intent_patterns = {
            "greeting": ["привіт", "hello", "hi", "добрий день", "вітаю"],
            "question": [
                "що",
                "як",
                "чому",
                "де",
                "коли",
                "what",
                "how",
                "why",
                "where",
                "when",
                "?",
            ],
            "request": [
                "можеш",
                "зроби",
                "допоможи",
                "покращ",
                "обнови",
                "can you",
                "please",
                "help",
            ],
            "dev_plan": [
                "план",
                "dev plan",
                "розширити",
                "expand",
                "update",
                "оновити",
            ],
            "analysis": ["аналіз", "analysis", "проаналізуй", "analyze"],
            "improvement": [
                "покращення",
                "improvement",
                "самовдосконалення",
                "self-improvement",
            ],
        }

        for intent, patterns in intent_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                return intent

        return "general"

    def _extract_entities(self, message: str) -> List[str]:
        """Extract entities from message"""
        entities = []

        # Extract file names
        file_pattern = re.compile(r"\b\w+\.\w+\b")
        entities.extend(file_pattern.findall(message))

        # Extract technical terms
        tech_terms = ["python", "gui", "pyside6", "agent", "module", "система", "файл"]
        for term in tech_terms:
            if term.lower() in message.lower():
                entities.append(term)

        return list(set(entities))

    def _analyze_sentiment(self, message: str) -> str:
        """Analyze sentiment of the message"""
        positive_words = [
            "добре",
            "чудово",
            "відмінно",
            "good",
            "great",
            "excellent",
            "дякую",
            "thank",
        ]
        negative_words = [
            "погано",
            "не працює",
            "помилка",
            "error",
            "bad",
            "wrong",
            "fail",
        ]

        message_lower = message.lower()
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)

        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

    def _assess_complexity(self, message: str) -> str:
        """Assess complexity of the message"""
        word_count = len(message.split())

        if word_count < 5:
            return "simple"
        elif word_count < 20:
            return "medium"
        else:
            return "complex"

    def _find_patterns(self, message: str) -> List[str]:
        """Find conversation patterns in message"""
        patterns = []

        # Check for common patterns
        if re.search(r"\b(можеш|can you)\b", message, re.IGNORECASE):
            patterns.append("polite_request")

        if re.search(r"\?", message):
            patterns.append("question")

        if re.search(r"\b(план|plan|розширити|expand)\b", message, re.IGNORECASE):
            patterns.append("planning_request")

        return patterns

    def _update_conversation_patterns(self, analysis: Dict[str, Any]):
        """Update conversation patterns based on analysis"""
        intent = analysis.get("intent", "unknown")
        patterns = analysis.get("patterns", [])

        # Store conversation pattern
        pattern_key = f"{intent}_{analysis.get('language', 'unknown')}"
        self.conversation_patterns[pattern_key].append(
            {
                "timestamp": analysis["timestamp"],
                "message_length": len(analysis["message"]),
                "complexity": analysis.get("complexity", "unknown"),
                "patterns": patterns,
            }
        )

        # Keep only recent patterns (last 100 per type)
        if len(self.conversation_patterns[pattern_key]) > 100:
            self.conversation_patterns[pattern_key] = self.conversation_patterns[
                pattern_key
            ][-100:]

    def _get_response_template(self, intent: str, language: str) -> str:
        """Get response template for given intent and language"""
        templates = {
            "greeting": {
                "uk": "Привіт! Я NIMDA Agent, готовий допомогти з розробкою та покращенням системи.",
                "ru": "Привет! Я NIMDA Agent, готов помочь с разработкой и улучшением системы.",
                "en": "Hello! I'm NIMDA Agent, ready to help with development and system improvement.",
            },
            "dev_plan": {
                "uk": "Розумію, ви хочете оновити план розробки. Я проаналізую поточний стан і запропоную покращення.",
                "ru": "Понимаю, вы хотите обновить план разработки. Я проанализирую текущее состояние и предложу улучшения.",
                "en": "I understand you want to update the development plan. I'll analyze the current state and suggest improvements.",
            },
            "analysis": {
                "uk": "Починаю глибокий аналіз системи. Це може зайняти деякий час для отримання детальних результатів.",
                "ru": "Начинаю глубокий анализ системы. Это может занять некоторое время для получения детальных результатов.",
                "en": "Starting deep system analysis. This may take some time to get detailed results.",
            },
            "request": {
                "uk": "Звичайно! Я допоможу вам з цим завданням. Що саме потрібно зробити?",
                "ru": "Конечно! Я помогу вам с этой задачей. Что именно нужно сделать?",
                "en": "Of course! I'll help you with this task. What exactly needs to be done?",
            },
            "general": {
                "uk": "Дякую за повідомлення. Функція обробки цього типу запитів буде покращена в наступних ітераціях.",
                "ru": "Спасибо за сообщение. Функция обработки этого типа запросов будет улучшена в следующих итерациях.",
                "en": "Thank you for your message. The function for processing this type of request will be improved in future iterations.",
            },
        }

        return templates.get(intent, templates["general"]).get(
            language, templates["general"]["en"]
        )

    def _generate_contextual_response(
        self, analysis: Dict[str, Any], template: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate contextual response based on analysis and template"""
        response = {
            "text": template,
            "confidence": 0.8,
            "suggestions": [],
            "actions": [],
        }

        # Add context-specific suggestions
        intent = analysis.get("intent", "unknown")

        if intent == "dev_plan":
            response["actions"] = ["expand_dev_plan", "analyze_current_state"]
            response["suggestions"] = [
                "Рекомендую почати з аналізу поточного стану",
                "Додати нові функції для покращення інтелектуальної взаємодії",
                "Оновити модуль навчання для кращої обробки повідомлень",
            ]

        elif intent == "analysis":
            response["actions"] = ["deep_analysis", "generate_report"]
            response["suggestions"] = [
                "Буде виконано аналіз архітектури системи",
                "Перевірка всіх компонентів на помилки",
                "Генерація рекомендацій для покращення",
            ]

        return response

    def learn_from_experience(self, experience: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from a specific experience with enhanced pattern recognition"""
        try:
            self.logger.info("Learning from new experience")

            learning_entry = {
                "timestamp": datetime.now().isoformat(),
                "experience": experience,
                "success": experience.get("success", False),
                "type": experience.get("type", "general"),
                "context": experience.get("context", {}),
                "patterns_identified": self._identify_experience_patterns(experience),
            }

            self.learning_history.append(learning_entry)
            self.interaction_stats["learning_events"] += 1

            # Update knowledge base
            self._update_knowledge_base(learning_entry)

            # Save to persistent storage
            self._save_persistent_data()

            return {
                "success": True,
                "total_experiences": len(self.learning_history),
                "patterns_learned": len(learning_entry["patterns_identified"]),
            }

        except Exception as e:
            self.logger.error(f"Error learning from experience: {e}")
            return {"success": False, "error": str(e)}

    def _identify_experience_patterns(self, experience: Dict[str, Any]) -> List[str]:
        """Identify patterns in the experience"""
        patterns = []

        if experience.get("success"):
            patterns.append("successful_action")
        else:
            patterns.append("failed_action")

        exp_type = experience.get("type", "")
        if "message" in exp_type:
            patterns.append("communication_pattern")
        elif "task" in exp_type:
            patterns.append("task_execution_pattern")

        return patterns

    def _update_knowledge_base(self, learning_entry: Dict[str, Any]):
        """Update knowledge base with new learning"""
        experience_type = learning_entry["experience"].get("type", "general")

        if experience_type not in self.knowledge_base:
            self.knowledge_base[experience_type] = {
                "patterns": [],
                "success_rate": 0.0,
                "common_issues": [],
                "best_practices": [],
            }

        # Update patterns
        for pattern in learning_entry["patterns_identified"]:
            if pattern not in self.knowledge_base[experience_type]["patterns"]:
                self.knowledge_base[experience_type]["patterns"].append(pattern)

    def get_learning_stats(self) -> Dict[str, Any]:
        """Get comprehensive learning statistics"""
        total_experiences = len(self.learning_history)
        successful = sum(1 for exp in self.learning_history if exp.get("success"))

        # Calculate recent success rate (last 10 experiences)
        recent_experiences = (
            self.learning_history[-10:]
            if len(self.learning_history) >= 10
            else self.learning_history
        )
        recent_successful = sum(1 for exp in recent_experiences if exp.get("success"))
        recent_success_rate = (
            recent_successful / len(recent_experiences) if recent_experiences else 0
        )

        # Get most common patterns
        all_patterns = []
        for exp in self.learning_history:
            all_patterns.extend(exp.get("patterns_identified", []))

        pattern_counts = {}
        for pattern in all_patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        most_common_patterns = sorted(
            pattern_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]

        return {
            "total_experiences": total_experiences,
            "successful_experiences": successful,
            "success_rate": successful / total_experiences
            if total_experiences > 0
            else 0,
            "recent_success_rate": recent_success_rate,
            "most_common_patterns": most_common_patterns,
            "knowledge_base_size": len(self.knowledge_base),
            "interaction_stats": self.interaction_stats,
            "conversation_patterns_count": len(self.conversation_patterns),
        }

    def get_recommendations(
        self, context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Get recommendations based on learning history and context"""
        recommendations = []

        stats = self.get_learning_stats()

        # Based on success rate
        if stats["success_rate"] < 0.7:
            recommendations.append(
                "Рекомендується покращити алгоритми обробки для підвищення успішності"
            )

        # Based on recent patterns
        recent_patterns = [pattern for pattern, count in stats["most_common_patterns"]]

        if "failed_action" in recent_patterns:
            recommendations.append(
                "Виявлено частотні помилки - рекомендується аналіз та оптимізація"
            )

        if "communication_pattern" in recent_patterns:
            recommendations.append(
                "Активна комунікація - рекомендується покращення шаблонів відповідей"
            )

        # Context-specific recommendations
        if context:
            if context.get("message_complexity") == "complex":
                recommendations.append(
                    "Складні повідомлення - рекомендується покращення аналізу контексту"
                )

        return recommendations

    def export_learning_data(self, export_format: str = "json") -> Dict[str, Any]:
        """Export learning data for analysis or backup"""
        try:
            export_data = {
                "metadata": {
                    "export_timestamp": datetime.now().isoformat(),
                    "total_experiences": len(self.learning_history),
                    "export_format": export_format,
                },
                "learning_history": self.learning_history,
                "knowledge_base": self.knowledge_base,
                "conversation_patterns": dict(self.conversation_patterns),
                "user_preferences": self.user_preferences,
                "statistics": self.get_learning_stats(),
            }

            if export_format == "json":
                export_file = (
                    self.data_dir
                    / f"learning_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )
                with open(export_file, "w", encoding="utf-8") as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)

                return {
                    "success": True,
                    "export_file": str(export_file),
                    "data_size": len(json.dumps(export_data)),
                }
            else:
                return {"success": False, "error": "Unsupported export format"}

        except Exception as e:
            self.logger.error(f"Error exporting learning data: {e}")
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    # Test the enhanced learning module
    learner = LearningModule()

    # Test message analysis
    test_message = "Чи можеш ти оновити dev план і розширити його?"
    analysis = learner.analyze_message(test_message)
    print("Message Analysis:", analysis)

    # Test response generation
    response = learner.generate_response(analysis)
    print("Generated Response:", response)

    # Test learning from experience
    experience = {
        "type": "message_processing",
        "message": test_message,
        "response": response,
        "success": True,
        "context": {"user_language": "uk", "complexity": "medium"},
    }

    learning_result = learner.learn_from_experience(experience)
    print("Learning Result:", learning_result)

    # Get statistics
    stats = learner.get_learning_stats()
    print("Learning Statistics:", stats)

    print("✅ Enhanced LearningModule loaded and tested successfully!")
