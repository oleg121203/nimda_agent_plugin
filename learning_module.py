#!/usr/bin/env python3
"""
LearningModule - Модуль навчання з векторною базою знань
======================================================
"""

import asyncio
import json
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

class LearningModule:
    """Модуль навчання та адаптації в реальному часі з векторною базою"""
    
    def __init__(self, knowledge_base_path: str = "knowledge_base.json"):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.vector_embeddings = {}
        self.learning_patterns = []
        self.adaptation_rules = {}
        self.performance_metrics = {}
        
        # Ініціалізація
        asyncio.create_task(self._initialize_knowledge_base())
        
    async def _initialize_knowledge_base(self):
        """Ініціалізація бази знань"""
        if self.knowledge_base_path.exists():
            await self._load_knowledge_base()
        else:
            await self._create_initial_knowledge_base()
            
    async def _load_knowledge_base(self):
        """Завантажити існуючу базу знань"""
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.learning_patterns = data.get('patterns', [])
                self.adaptation_rules = data.get('rules', {})
                self.performance_metrics = data.get('metrics', {})
        except Exception:
            await self._create_initial_knowledge_base()
            
    async def _create_initial_knowledge_base(self):
        """Створити початкову базу знань"""
        initial_data = {
            'patterns': [],
            'rules': {
                'adaptation_threshold': 0.7,
                'learning_rate': 0.1,
                'forget_threshold': 0.3
            },
            'metrics': {
                'total_learning_sessions': 0,
                'successful_adaptations': 0,
                'knowledge_retention_rate': 1.0
            }
        }
        
        await self._save_knowledge_base(initial_data)
        
    async def learn_from_experience(self, experience: Dict) -> Dict:
        """Навчитися з досвіду"""
        
        # Векторне представлення досвіду
        experience_vector = await self._vectorize_experience(experience)
        
        # Пошук схожих досвідів
        similar_experiences = await self._find_similar_experiences(experience_vector)
        
        # Генерація патерну навчання
        learning_pattern = await self._generate_learning_pattern(experience, similar_experiences)
        
        # Оновлення бази знань
        await self._update_knowledge_base(learning_pattern)
        
        # Адаптація правил
        adaptation_result = await self._adapt_rules(learning_pattern)
        
        return {
            'pattern_id': learning_pattern['id'],
            'similarity_score': learning_pattern.get('similarity_score', 0.0),
            'adaptation_applied': adaptation_result['adapted'],
            'learning_confidence': learning_pattern['confidence'],
            'knowledge_growth': self._calculate_knowledge_growth()
        }
        
    async def _vectorize_experience(self, experience: Dict) -> np.ndarray:
        """Перетворити досвід у вектор"""
        # Простий підхід до векторизації
        features = []
        
        # Числові характеристики
        features.append(experience.get('success_rate', 0.5))
        features.append(experience.get('complexity', 0.5))
        features.append(experience.get('time_taken', 1.0))
        features.append(experience.get('user_satisfaction', 0.5))
        
        # Категоріальні характеристики (one-hot encoding)
        categories = ['technical', 'creative', 'analytical', 'social']
        category = experience.get('category', 'technical')
        for cat in categories:
            features.append(1.0 if cat == category else 0.0)
            
        # Текстові характеристики (довжина опису)
        description = experience.get('description', '')
        features.append(len(description) / 100.0)  # Нормалізована довжина
        
        return np.array(features)
        
    async def _find_similar_experiences(self, experience_vector: np.ndarray) -> List[Dict]:
        """Знайти схожі досвіди"""
        similar = []
        
        for pattern in self.learning_patterns:
            if 'vector' in pattern:
                pattern_vector = np.array(pattern['vector'])
                similarity = self._calculate_cosine_similarity(experience_vector, pattern_vector)
                
                if similarity > 0.7:  # Поріг схожості
                    similar.append({
                        'pattern': pattern,
                        'similarity': similarity
                    })
                    
        return sorted(similar, key=lambda x: x['similarity'], reverse=True)[:5]
        
    def _calculate_cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Розрахувати косинусну подібність"""
        try:
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
                
            return dot_product / (norm1 * norm2)
        except:
            return 0.0
            
    async def _generate_learning_pattern(self, experience: Dict, similar_experiences: List[Dict]) -> Dict:
        """Згенерувати патерн навчання"""
        
        pattern_id = f"pattern_{len(self.learning_patterns)}_{int(datetime.now().timestamp())}"
        
        # Розрахувати впевненість на основі схожих досвідів
        confidence = self._calculate_pattern_confidence(experience, similar_experiences)
        
        # Визначити вагу важливості
        importance = self._calculate_importance(experience)
        
        return {
            'id': pattern_id,
            'experience': experience,
            'vector': (await self._vectorize_experience(experience)).tolist(),
            'similar_count': len(similar_experiences),
            'confidence': confidence,
            'importance': importance,
            'timestamp': datetime.now().isoformat(),
            'usage_count': 0,
            'success_rate': experience.get('success_rate', 0.5)
        }
        
    def _calculate_pattern_confidence(self, experience: Dict, similar_experiences: List[Dict]) -> float:
        """Розрахувати впевненість патерну"""
        base_confidence = experience.get('success_rate', 0.5)
        
        # Бонус за схожі успішні досвіди
        if similar_experiences:
            similar_success_rates = [
                exp['pattern'].get('success_rate', 0.5) 
                for exp in similar_experiences
            ]
            avg_similar_success = sum(similar_success_rates) / len(similar_success_rates)
            base_confidence = (base_confidence + avg_similar_success) / 2
            
        # Бонус за кількість схожих досвідів
        similarity_bonus = min(len(similar_experiences) * 0.1, 0.3)
        
        return min(base_confidence + similarity_bonus, 1.0)
        
    def _calculate_importance(self, experience: Dict) -> float:
        """Розрахувати важливість досвіду"""
        importance_factors = [
            experience.get('impact', 0.5),
            experience.get('uniqueness', 0.5),
            experience.get('user_feedback', 0.5),
            1.0 if experience.get('critical', False) else 0.3
        ]
        
        return sum(importance_factors) / len(importance_factors)
        
    async def _update_knowledge_base(self, learning_pattern: Dict):
        """Оновити базу знань"""
        self.learning_patterns.append(learning_pattern)
        
        # Обмежити розмір бази знань
        max_patterns = 1000
        if len(self.learning_patterns) > max_patterns:
            # Видалити найменш важливі патерни
            self.learning_patterns.sort(key=lambda x: x['importance'], reverse=True)
            self.learning_patterns = self.learning_patterns[:max_patterns]
            
        # Оновити метрики
        self.performance_metrics['total_learning_sessions'] += 1
        
    async def _adapt_rules(self, learning_pattern: Dict) -> Dict:
        """Адаптувати правила на основі нового патерну"""
        adaptation_applied = False
        
        # Адаптація порогу схожості
        if learning_pattern['confidence'] > 0.8:
            current_threshold = self.adaptation_rules.get('adaptation_threshold', 0.7)
            new_threshold = (current_threshold + learning_pattern['confidence']) / 2
            self.adaptation_rules['adaptation_threshold'] = new_threshold
            adaptation_applied = True
            
        # Адаптація швидкості навчання
        success_rate = learning_pattern['success_rate']
        if success_rate > 0.8:
            current_lr = self.adaptation_rules.get('learning_rate', 0.1)
            self.adaptation_rules['learning_rate'] = min(current_lr * 1.1, 0.5)
            adaptation_applied = True
        elif success_rate < 0.3:
            current_lr = self.adaptation_rules.get('learning_rate', 0.1)
            self.adaptation_rules['learning_rate'] = max(current_lr * 0.9, 0.01)
            adaptation_applied = True
            
        if adaptation_applied:
            self.performance_metrics['successful_adaptations'] += 1
            
        return {'adapted': adaptation_applied}
        
    def _calculate_knowledge_growth(self) -> float:
        """Розрахувати ріст знань"""
        if not self.learning_patterns:
            return 0.0
            
        # Середня впевненість всіх патернів
        avg_confidence = sum(p['confidence'] for p in self.learning_patterns) / len(self.learning_patterns)
        
        # Ріст відносно початкового стану
        baseline_confidence = 0.5
        growth = (avg_confidence - baseline_confidence) / baseline_confidence
        
        return max(growth, 0.0)
        
    async def predict_outcome(self, scenario: Dict) -> Dict:
        """Передбачити результат сценарію"""
        
        scenario_vector = await self._vectorize_experience(scenario)
        similar_patterns = await self._find_similar_experiences(scenario_vector)
        
        if not similar_patterns:
            return {
                'predicted_success_rate': 0.5,
                'confidence': 0.1,
                'recommendations': ['Новий сценарій, збирайте досвід обережно']
            }
            
        # Зважене передбачення
        weighted_success = 0.0
        total_weight = 0.0
        
        for similar in similar_patterns:
            weight = similar['similarity']
            success_rate = similar['pattern']['success_rate']
            weighted_success += weight * success_rate
            total_weight += weight
            
        predicted_success = weighted_success / total_weight if total_weight > 0 else 0.5
        prediction_confidence = min(total_weight / len(similar_patterns), 1.0)
        
        # Генерація рекомендацій
        recommendations = self._generate_recommendations(similar_patterns, scenario)
        
        return {
            'predicted_success_rate': predicted_success,
            'confidence': prediction_confidence,
            'similar_cases': len(similar_patterns),
            'recommendations': recommendations
        }
        
    def _generate_recommendations(self, similar_patterns: List[Dict], scenario: Dict) -> List[str]:
        """Згенерувати рекомендації"""
        recommendations = []
        
        # Аналіз успішних патернів
        successful_patterns = [p for p in similar_patterns if p['pattern']['success_rate'] > 0.7]
        
        if successful_patterns:
            recommendations.append("Використовуйте стратегії з успішних схожих випадків")
            
        # Аналіз категорій
        categories = [p['pattern']['experience'].get('category') for p in similar_patterns]
        most_common_category = max(set(categories), key=categories.count) if categories else None
        
        if most_common_category:
            recommendations.append(f"Розгляньте підходи категорії '{most_common_category}'")
            
        # Загальні рекомендації
        if not recommendations:
            recommendations = [
                "Почніть з простих кроків",
                "Збирайте зворотний зв'язок рано",
                "Будьте готові до адаптації"
            ]
            
        return recommendations
        
    async def _save_knowledge_base(self, data: Dict = None):
        """Зберегти базу знань"""
        if data is None:
            data = {
                'patterns': self.learning_patterns,
                'rules': self.adaptation_rules,
                'metrics': self.performance_metrics
            }
            
        try:
            with open(self.knowledge_base_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # Ігноруємо помилки збереження
            
    def get_learning_stats(self) -> Dict:
        """Отримати статистику навчання"""
        return {
            'total_patterns': len(self.learning_patterns),
            'knowledge_growth': self._calculate_knowledge_growth(),
            'adaptation_rules': self.adaptation_rules.copy(),
            'performance_metrics': self.performance_metrics.copy(),
            'average_confidence': sum(p['confidence'] for p in self.learning_patterns) / len(self.learning_patterns) if self.learning_patterns else 0.0
        }
        
    async def forget_outdated_knowledge(self, age_threshold_days: int = 30):
        """Забути застарілі знання"""
        current_time = datetime.now()
        forget_threshold = self.adaptation_rules.get('forget_threshold', 0.3)
        
        patterns_to_keep = []
        
        for pattern in self.learning_patterns:
            pattern_time = datetime.fromisoformat(pattern['timestamp'])
            age_days = (current_time - pattern_time).days
            
            # Зберегти якщо: важливе АБО недавнє АБО успішне
            keep = (
                pattern['importance'] > forget_threshold or
                age_days < age_threshold_days or
                pattern['success_rate'] > 0.8
            )
            
            if keep:
                patterns_to_keep.append(pattern)
                
        forgotten_count = len(self.learning_patterns) - len(patterns_to_keep)
        self.learning_patterns = patterns_to_keep
        
        # Оновити метрики
        if forgotten_count > 0:
            retention_rate = len(patterns_to_keep) / (len(patterns_to_keep) + forgotten_count)
            self.performance_metrics['knowledge_retention_rate'] = retention_rate
            
        return {'forgotten_patterns': forgotten_count}


# Приклад використання
async def main():
    learning_module = LearningModule("test_knowledge.json")
    
    # Симуляція досвіду навчання
    experience = {
        'description': 'Successfully implemented AI task prioritization',
        'category': 'technical',
        'success_rate': 0.9,
        'complexity': 0.7,
        'time_taken': 2.5,
        'user_satisfaction': 0.8,
        'impact': 0.9,
        'uniqueness': 0.6,
        'critical': True
    }
    
    # Навчання
    result = await learning_module.learn_from_experience(experience)
    print("Learning Result:", result)
    
    # Передбачення
    new_scenario = {
        'description': 'Implementing error detection system',
        'category': 'technical',
        'complexity': 0.8
    }
    
    prediction = await learning_module.predict_outcome(new_scenario)
    print("Prediction:", prediction)
    
    # Статистика
    stats = learning_module.get_learning_stats()
    print("Learning Stats:", stats)

if __name__ == "__main__":
    asyncio.run(main())
