#!/usr/bin/env python3
"""
Agent Manager for NIMDA System
Manages ChatAgent and WorkerAgent with intelligent coordination
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Task:
    """Task data structure"""
    id: str
    type: str
    content: str
    priority: int = 1
    status: str = "pending"
    assigned_agent: Optional[str] = None


class AgentManager:
    """
    Manages all agents in the system with intelligent task distribution
    and deep context awareness
    """
    
    def __init__(self):
        self.agents = {}
        self.task_queue = asyncio.Queue()
        self.task_history = []
        self.running = False
        
    async def initialize(self):
        """Initialize agent manager"""
        logger.info("🤖 Initializing Agent Manager...")
        
        # Initialize agents
        await self._initialize_agents()
        
        # Setup task processing
        await self._setup_task_processing()
        
        logger.info("✅ Agent Manager initialized")

    async def start(self):
        """Start the agent manager"""
        if not self.running:
            self.running = True
            logger.info("🚀 Starting Agent Manager...")
            
            # Start task processing loop
            asyncio.create_task(self._task_processing_loop())

    async def stop(self):
        """Stop the agent manager"""
        self.running = False
        logger.info("🛑 Stopping Agent Manager...")

    async def submit_task(self, task: Task):
        """Submit a task for processing"""
        logger.info(f"📝 Submitting task: {task.id}")
        await self.task_queue.put(task)

    async def _initialize_agents(self):
        """Initialize individual agents"""
        # This will be expanded with actual agent implementations
        self.agents["chat_agent"] = None    # Will implement ChatAgent
        self.agents["worker_agent"] = None  # Will implement WorkerAgent

    async def _setup_task_processing(self):
        """Setup task processing system"""
        # Initialize task processing infrastructure
        pass

    async def _task_processing_loop(self):
        """Main task processing loop"""
        while self.running:
            try:
                # Get task from queue (wait up to 1 second)
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                
                # Process the task
                await self._process_task(task)
                
            except asyncio.TimeoutError:
                # No task available, continue
                continue
            except Exception as e:
                logger.error(f"❌ Error in task processing loop: {e}")

    async def _process_task(self, task: Task):
        """Process individual task"""
        logger.info(f"⚙️  Processing task: {task.id}")
        
        # Determine best agent for the task
        assigned_agent = self._assign_task_to_agent(task)
        
        if assigned_agent:
            task.assigned_agent = assigned_agent
            task.status = "processing"
            
            # Process with assigned agent
            # This will be implemented with actual agent logic
            
            task.status = "completed"
            self.task_history.append(task)
            
            logger.info(f"✅ Task completed: {task.id}")

    def _assign_task_to_agent(self, task: Task) -> Optional[str]:
        """Assign task to the most appropriate agent"""
        # Simple assignment logic - will be enhanced
        if task.type in ["chat", "conversation"]:
            return "chat_agent"
        elif task.type in ["work", "execution", "development"]:
            return "worker_agent"
        else:
            return "worker_agent"  # Default

    def get_status(self) -> Dict[str, Any]:
        """Get agent manager status"""
        return {
            "running": self.running,
            "agents": list(self.agents.keys()),
            "queue_size": self.task_queue.qsize(),
            "completed_tasks": len(self.task_history)
        }


if __name__ == "__main__":
    async def test_agent_manager():
        manager = AgentManager()
        await manager.initialize()
        await manager.start()
        
        # Submit test task
        test_task = Task(
            id="test_001",
            type="development",
            content="Test task for development"
        )
        await manager.submit_task(test_task)
        
        # Let it run for a bit
        await asyncio.sleep(2)
        
        await manager.stop()
        print(f"Status: {manager.get_status()}")
    
    asyncio.run(test_agent_manager())
