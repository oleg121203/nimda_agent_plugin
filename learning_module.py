"""
Learning System
Handles pattern recognition and knowledge base management
"""
import logging
from typing import Dict, List, Any
from datetime import datetime


class LearningModule:
    """System for learning patterns and building knowledge base"""
    
    def __init__(self):
        self.logger = logging.getLogger("LearningModule")
        self.knowledge_base = {}
        self.learning_history = []
    
    def learn_from_experience(self, experience: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from a specific experience"""
        try:
            self.logger.info("Learning from new experience")
            
            learning_entry = {
                "timestamp": datetime.now().isoformat(),
                "experience": experience,
                "success": experience.get("success", False)
            }
            
            self.learning_history.append(learning_entry)
            
            return {
                "success": True,
                "total_experiences": len(self.learning_history)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get comprehensive learning statistics"""
        total_experiences = len(self.learning_history)
        successful = sum(1 for exp in self.learning_history if exp.get("success"))
        
        return {
            "total_experiences": total_experiences,
            "successful_experiences": successful,
            "success_rate": successful / total_experiences if total_experiences > 0 else 0
        }


if __name__ == "__main__":
    learner = LearningModule()
    print("LearningModule loaded successfully")
