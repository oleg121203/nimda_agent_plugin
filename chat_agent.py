#!/usr/bin/env python3
"""
ChatAgent - Розумний чат-агент з глибоким розумінням контексту
============================================================
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime

class ChatAgent:
    """Інтелектуальний чат-агент для взаємодії з користувачем"""
    
    def __init__(self):
        self.context_memory = []
        self.conversation_history = []
        self.skills = ['coding', 'analysis', 'planning', 'debugging']
        
    async def process_message(self, message: str, context: Dict = None) -> str:
        """Обробити повідомлення користувача з розумінням контексту"""
        
        # Аналіз контексту
        understood_context = await self._analyze_context(message, context)
        
        # Генерація відповіді
        response = await self._generate_intelligent_response(message, understood_context)
        
        # Збереження в історії
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user_message': message,
            'agent_response': response,
            'context': understood_context
        })
        
        return response
        
    async def _analyze_context(self, message: str, context: Dict = None) -> Dict:
        """Аналіз контексту повідомлення"""
        return {
            'intent': self._detect_intent(message),
            'entities': self._extract_entities(message),
            'sentiment': self._analyze_sentiment(message),
            'complexity': self._assess_complexity(message)
        }
        
    def _detect_intent(self, message: str) -> str:
        """Виявити намір користувача"""
        if any(word in message.lower() for word in ['create', 'generate', 'build']):
            return 'creation'
        elif any(word in message.lower() for word in ['fix', 'debug', 'error']):
            return 'debugging'
        elif any(word in message.lower() for word in ['explain', 'how', 'what']):
            return 'explanation'
        else:
            return 'general'
            
    def _extract_entities(self, message: str) -> List[str]:
        """Витягнути сутності з повідомлення"""
        entities = []
        # Простий витяг технічних термінів
        tech_terms = ['python', 'api', 'database', 'ai', 'machine learning']
        for term in tech_terms:
            if term in message.lower():
                entities.append(term)
        return entities
        
    def _analyze_sentiment(self, message: str) -> str:
        """Аналіз тональності"""
        positive_words = ['good', 'great', 'excellent', 'love']
        negative_words = ['bad', 'terrible', 'hate', 'problem']
        
        if any(word in message.lower() for word in positive_words):
            return 'positive'
        elif any(word in message.lower() for word in negative_words):
            return 'negative'
        else:
            return 'neutral'
            
    def _assess_complexity(self, message: str) -> str:
        """Оцінити складність запиту"""
        if len(message.split()) > 20:
            return 'high'
        elif len(message.split()) > 10:
            return 'medium'
        else:
            return 'low'
            
    async def _generate_intelligent_response(self, message: str, context: Dict) -> str:
        """Згенерувати розумну відповідь"""
        
        intent = context.get('intent', 'general')
        complexity = context.get('complexity', 'low')
        
        if intent == 'creation':
            return f"Розумію, ви хочете щось створити. Розкажу детально про процес..."
        elif intent == 'debugging':
            return f"Аналізую проблему. Ось кроки для вирішення..."
        elif intent == 'explanation':
            return f"Пояснення з урахуванням складності '{complexity}'..."
        else:
            return "Як ваш AI-асистент, готовий допомогти з будь-яким питанням!"
            
    def get_conversation_summary(self) -> Dict:
        """Отримати підсумок розмови"""
        return {
            'total_messages': len(self.conversation_history),
            'dominant_intent': self._get_dominant_intent(),
            'user_satisfaction': self._estimate_satisfaction(),
            'topics_covered': self._extract_topics()
        }
        
    def _get_dominant_intent(self) -> str:
        """Визначити домінуючий намір в розмові"""
        intents = [conv['context']['intent'] for conv in self.conversation_history]
        return max(set(intents), key=intents.count) if intents else 'unknown'
        
    def _estimate_satisfaction(self) -> float:
        """Оцінити задоволеність користувача"""
        positive_responses = sum(1 for conv in self.conversation_history 
                               if conv['context']['sentiment'] == 'positive')
        total = len(self.conversation_history)
        return positive_responses / total if total > 0 else 0.5
        
    def _extract_topics(self) -> List[str]:
        """Витягнути основні теми розмови"""
        all_entities = []
        for conv in self.conversation_history:
            all_entities.extend(conv['context']['entities'])
        return list(set(all_entities))
        

# Приклад використання
async def main():
    agent = ChatAgent()
    
    # Тестові повідомлення
    messages = [
        "How can I create a Python API?",
        "I'm having trouble with database errors",
        "Explain machine learning concepts please"
    ]
    
    for msg in messages:
        response = await agent.process_message(msg)
        print(f"User: {msg}")
        print(f"Agent: {response}")
        print("-" * 50)
        
    # Підсумок
    summary = agent.get_conversation_summary()
    print("Conversation Summary:", summary)

if __name__ == "__main__":
    asyncio.run(main())
