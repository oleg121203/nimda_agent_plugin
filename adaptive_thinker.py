#!/usr/bin/env python3
"""
AdaptiveThinker - Система адаптивного та творчого мислення
========================================================
"""

import asyncio
import random
from typing import Dict, List, Optional, Any
from datetime import datetime

class AdaptiveThinker:
    """Система адаптивного мислення для творчого вирішення проблем"""
    
    def __init__(self):
        self.thinking_patterns = ['analytical', 'creative', 'systematic', 'intuitive']
        self.solution_approaches = []
        self.learned_strategies = {}
        self.success_metrics = {}
        
    async def think_creatively(self, problem: Dict) -> Dict:
        """Творче мислення для вирішення проблеми"""
        
        # Аналіз проблеми
        problem_analysis = await self._analyze_problem(problem)
        
        # Генерація множинних підходів
        approaches = await self._generate_multiple_approaches(problem_analysis)
        
        # Оцінка підходів
        evaluated_approaches = await self._evaluate_approaches(approaches, problem)
        
        # Вибір найкращого рішення
        best_solution = await self._select_best_solution(evaluated_approaches)
        
        # Навчання з досвіду
        await self._learn_from_solution(problem, best_solution)
        
        return best_solution
        
    async def _analyze_problem(self, problem: Dict) -> Dict:
        """Глибокий аналіз проблеми"""
        return {
            'complexity': self._assess_complexity(problem),
            'domain': self._identify_domain(problem),
            'constraints': self._extract_constraints(problem),
            'goals': self._identify_goals(problem),
            'similar_problems': self._find_similar_problems(problem)
        }
        
    def _assess_complexity(self, problem: Dict) -> str:
        """Оцінити складність проблеми"""
        description = problem.get('description', '')
        factors = problem.get('factors', [])
        
        complexity_score = len(description.split()) + len(factors) * 2
        
        if complexity_score > 50:
            return 'high'
        elif complexity_score > 20:
            return 'medium'
        else:
            return 'low'
            
    def _identify_domain(self, problem: Dict) -> str:
        """Ідентифікувати домен проблеми"""
        description = problem.get('description', '').lower()
        
        domains = {
            'technical': ['code', 'programming', 'algorithm', 'software'],
            'business': ['market', 'customer', 'revenue', 'strategy'],
            'creative': ['design', 'artistic', 'innovative', 'creative'],
            'analytical': ['data', 'analysis', 'statistics', 'research']
        }
        
        for domain, keywords in domains.items():
            if any(keyword in description for keyword in keywords):
                return domain
                
        return 'general'
        
    def _extract_constraints(self, problem: Dict) -> List[str]:
        """Витягнути обмеження"""
        constraints = problem.get('constraints', [])
        
        # Автоматично виявити обмеження з опису
        description = problem.get('description', '').lower()
        implicit_constraints = []
        
        if 'time' in description or 'deadline' in description:
            implicit_constraints.append('time_constraint')
        if 'budget' in description or 'cost' in description:
            implicit_constraints.append('budget_constraint')
        if 'resource' in description:
            implicit_constraints.append('resource_constraint')
            
        return constraints + implicit_constraints
        
    def _identify_goals(self, problem: Dict) -> List[str]:
        """Ідентифікувати цілі"""
        goals = problem.get('goals', [])
        description = problem.get('description', '').lower()
        
        # Автоматично виявити цілі
        goal_indicators = {
            'optimize': 'optimization',
            'improve': 'improvement', 
            'solve': 'solution',
            'create': 'creation',
            'automate': 'automation'
        }
        
        implicit_goals = []
        for indicator, goal in goal_indicators.items():
            if indicator in description:
                implicit_goals.append(goal)
                
        return goals + implicit_goals
        
    def _find_similar_problems(self, problem: Dict) -> List[Dict]:
        """Знайти схожі проблеми з досвіду"""
        # В реальній системі тут була б база знань
        return self.learned_strategies.get('similar_problems', [])
        
    async def _generate_multiple_approaches(self, analysis: Dict) -> List[Dict]:
        """Генерація множинних підходів до вирішення"""
        approaches = []
        
        # Підхід 1: Аналітичний
        approaches.append(await self._analytical_approach(analysis))
        
        # Підхід 2: Творчий
        approaches.append(await self._creative_approach(analysis))
        
        # Підхід 3: Систематичний  
        approaches.append(await self._systematic_approach(analysis))
        
        # Підхід 4: Інтуїтивний
        approaches.append(await self._intuitive_approach(analysis))
        
        return approaches
        
    async def _analytical_approach(self, analysis: Dict) -> Dict:
        """Аналітичний підхід"""
        return {
            'type': 'analytical',
            'steps': [
                'Декомпозиція проблеми на частини',
                'Аналіз кожної частини окремо',
                'Пошук логічних зв'язків',
                'Синтез рішення з частин'
            ],
            'confidence': 0.8,
            'estimated_time': 'medium',
            'resources_needed': ['analytical_tools', 'data']
        }
        
    async def _creative_approach(self, analysis: Dict) -> Dict:
        """Творчий підхід"""
        return {
            'type': 'creative',
            'steps': [
                'Брейнсторм ідей без обмежень',
                'Аналогії з інших областей',
                'Комбінування несподіваних елементів',
                'Прототипування рішень'
            ],
            'confidence': 0.6,
            'estimated_time': 'variable',
            'resources_needed': ['creative_tools', 'inspiration']
        }
        
    async def _systematic_approach(self, analysis: Dict) -> Dict:
        """Систематичний підхід"""
        return {
            'type': 'systematic',
            'steps': [
                'Створення детального плану',
                'Поетапне виконання',
                'Постійний моніторинг прогресу',
                'Корекція при необхідності'
            ],
            'confidence': 0.9,
            'estimated_time': 'long',
            'resources_needed': ['planning_tools', 'time']
        }
        
    async def _intuitive_approach(self, analysis: Dict) -> Dict:
        """Інтуїтивний підхід"""
        return {
            'type': 'intuitive',
            'steps': [
                'Спонтанна генерація ідей',
                'Швидке прототипування',
                'Тестування на практиці',
                'Ітеративне покращення'
            ],
            'confidence': 0.5,
            'estimated_time': 'short',
            'resources_needed': ['flexibility', 'courage']
        }
        
    async def _evaluate_approaches(self, approaches: List[Dict], problem: Dict) -> List[Dict]:
        """Оцінити підходи за різними критеріями"""
        evaluated = []
        
        for approach in approaches:
            score = await self._calculate_approach_score(approach, problem)
            approach['evaluation_score'] = score
            evaluated.append(approach)
            
        return sorted(evaluated, key=lambda x: x['evaluation_score'], reverse=True)
        
    async def _calculate_approach_score(self, approach: Dict, problem: Dict) -> float:
        """Розрахувати оцінку підходу"""
        base_confidence = approach.get('confidence', 0.5)
        
        # Модифікатори на основі проблеми
        complexity = problem.get('complexity', 'medium')
        domain = problem.get('domain', 'general')
        
        # Корекція оцінки
        if complexity == 'high' and approach['type'] == 'systematic':
            base_confidence += 0.2
        elif complexity == 'low' and approach['type'] == 'intuitive':
            base_confidence += 0.1
            
        return min(base_confidence, 1.0)
        
    async def _select_best_solution(self, evaluated_approaches: List[Dict]) -> Dict:
        """Вибрати найкраще рішення"""
        if not evaluated_approaches:
            return {'error': 'No approaches generated'}
            
        best_approach = evaluated_approaches[0]
        
        return {
            'selected_approach': best_approach,
            'reasoning': f"Обрано підхід '{best_approach['type']}' з оцінкою {best_approach['evaluation_score']:.2f}",
            'implementation_plan': best_approach['steps'],
            'confidence': best_approach['evaluation_score'],
            'alternatives': evaluated_approaches[1:3]  # Топ альтернативи
        }
        
    async def _learn_from_solution(self, problem: Dict, solution: Dict):
        """Навчитися з досвіду вирішення"""
        problem_signature = self._create_problem_signature(problem)
        
        if problem_signature not in self.learned_strategies:
            self.learned_strategies[problem_signature] = []
            
        self.learned_strategies[problem_signature].append({
            'solution': solution,
            'timestamp': datetime.now(),
            'success_rate': solution.get('confidence', 0.5)
        })
        
    def _create_problem_signature(self, problem: Dict) -> str:
        """Створити підпис проблеми для навчання"""
        domain = problem.get('domain', 'unknown')
        complexity = problem.get('complexity', 'unknown')
        return f"{domain}_{complexity}"
        
    def get_thinking_stats(self) -> Dict:
        """Отримати статистику мислення"""
        return {
            'total_problems_solved': len(self.learned_strategies),
            'preferred_approach': self._get_preferred_approach(),
            'success_rate': self._calculate_overall_success_rate(),
            'learning_progress': len(self.learned_strategies)
        }
        
    def _get_preferred_approach(self) -> str:
        """Визначити улюблений підхід"""
        approaches = ['analytical', 'creative', 'systematic', 'intuitive']
        return random.choice(approaches)  # В реальності базувалося б на статистиці
        
    def _calculate_overall_success_rate(self) -> float:
        """Розрахувати загальний рівень успіху"""
        if not self.learned_strategies:
            return 0.0
            
        total_confidence = 0
        total_solutions = 0
        
        for problem_solutions in self.learned_strategies.values():
            for solution_data in problem_solutions:
                total_confidence += solution_data['success_rate']
                total_solutions += 1
                
        return total_confidence / total_solutions if total_solutions > 0 else 0.0


# Приклад використання
async def main():
    thinker = AdaptiveThinker()
    
    # Тестова проблема
    problem = {
        'description': 'Need to optimize database performance in Python application',
        'complexity': 'medium',
        'domain': 'technical',
        'constraints': ['limited_memory', 'time_constraint'],
        'goals': ['performance_improvement', 'maintainability']
    }
    
    solution = await thinker.think_creatively(problem)
    
    print("Problem:", problem['description'])
    print("Selected Approach:", solution['selected_approach']['type'])
    print("Confidence:", solution['confidence'])
    print("Implementation Plan:")
    for step in solution['implementation_plan']:
        print(f"  - {step}")
    
    stats = thinker.get_thinking_stats()
    print("Thinking Stats:", stats)

if __name__ == "__main__":
    asyncio.run(main())
