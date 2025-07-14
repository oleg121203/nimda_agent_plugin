"""
Worker Agent - Technical Executor & UI Orchestrator
Handles task execution and file operations
"""
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any

class WorkerAgent:
    """Agent responsible for technical task execution"""
    
    def __init__(self, project_path: Path):
        self.logger = logging.getLogger("WorkerAgent")
        self.project_path = project_path
        self.task_queue = []
    
    def execute_task(self, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task"""
        try:
            task_type = task_info.get("type")
            self.logger.info(f"Executing task: {task_type}")
            
            if task_type == "create_file":
                return self._create_file_task(task_info)
            elif task_type == "create_directory":
                return self._create_directory_task(task_info)
            else:
                return self._handle_generic_task(task_info)
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_file_task(self, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create a file with specified content"""
        try:
            file_path = Path(task_info["file_path"])
            content = task_info.get("content", "")
            
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            return {"success": True, "file_path": str(file_path)}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_directory_task(self, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create a directory structure"""
        try:
            dir_path = Path(task_info["directory_path"])
            dir_path.mkdir(parents=True, exist_ok=True)
            
            return {"success": True, "directory_path": str(dir_path)}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _handle_generic_task(self, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generic tasks"""
        return {"success": True, "message": "Generic task completed"}

if __name__ == "__main__":
    worker = WorkerAgent(Path("."))
    print("WorkerAgent module loaded successfully")
