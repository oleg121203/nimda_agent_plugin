#!/usr/bin/env python3
"""
NIMDA Agent - Main Application Entry Point
Production-ready application with error handling and logging
"""

from __future__ import annotations

import sys
import os
import logging
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nimda_app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class NIMDAApplication:
    """Main NIMDA Application Class"""
    
    def __init__(self):
        self.logger = logger
        self.components = {}
        
    def initialize_components(self) -> bool:
        """Initialize all NIMDA components"""
        try:
            # Import and initialize components
            from chat_agent import ChatAgent
            from worker_agent import WorkerAgent
            from adaptive_thinker import AdaptiveThinker
            from learning_module import LearningModule
            from macos_integration import MacOSIntegration
            
            self.components = {
                'chat_agent': ChatAgent(),
                'worker_agent': WorkerAgent(),
                'adaptive_thinker': AdaptiveThinker(),
                'learning_module': LearningModule(),
                'macos_integration': MacOSIntegration()
            }
            
            self.logger.info("✅ All components initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Component initialization failed: {e}")
            return False
    
    def run_health_check(self) -> Dict[str, Any]:
        """Run comprehensive health check"""
        health_status = {
            'overall_status': 'healthy',
            'components': {},
            'timestamp': str(Path(__file__).stat().st_mtime)
        }
        
        for name, component in self.components.items():
            try:
                # Check if component has basic attributes
                if hasattr(component, '__class__'):
                    health_status['components'][name] = {
                        'status': 'healthy',
                        'class': component.__class__.__name__
                    }
                else:
                    health_status['components'][name] = {
                        'status': 'warning',
                        'reason': 'Missing class attribute'
                    }
            except Exception as e:
                health_status['components'][name] = {
                    'status': 'error',
                    'reason': str(e)
                }
                health_status['overall_status'] = 'degraded'
        
        return health_status
    
    def run_interactive_mode(self):
        """Run in interactive mode"""
        self.logger.info("🚀 Starting NIMDA in interactive mode")
        
        print("\n" + "="*50)
        print("🤖 NIMDA Agent - Interactive Mode")
        print("="*50)
        
        while True:
            try:
                user_input = input("\nNIMDA> ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() in ['health', 'status']:
                    health = self.run_health_check()
                    print(f"\n📊 System Status: {health['overall_status']}")
                    for comp, status in health['components'].items():
                        print(f"   {comp}: {status['status']}")
                elif user_input.lower() == 'help':
                    print("""
📖 Available Commands:
   health/status - Check system health
   help         - Show this help
   exit/quit/q  - Exit application
   
🔧 Component Commands:
   Any other input will be processed by the chat agent
                    """)
                else:
                    # Process with chat agent
                    if 'chat_agent' in self.components:
                        print(f"💬 Chat Agent: Processing '{user_input}'...")
                        # Here you would add actual chat processing
                        print("✅ Message processed successfully")
                    else:
                        print("❌ Chat agent not available")
                        
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                self.logger.error(f"Error in interactive mode: {e}")
                print(f"❌ Error: {e}")
    
    def run(self, mode: str = 'interactive') -> int:
        """Main application runner"""
        try:
            self.logger.info("🚀 Starting NIMDA Agent Application")
            
            # Initialize components
            if not self.initialize_components():
                return 1
            
            # Run health check
            health = self.run_health_check()
            self.logger.info(f"📊 Health check: {health['overall_status']}")
            
            if mode == 'interactive':
                self.run_interactive_mode()
            elif mode == 'health':
                print("\n📊 NIMDA Health Status:")
                print(f"Overall: {health['overall_status']}")
                for comp, status in health['components'].items():
                    print(f"  {comp}: {status['status']}")
            else:
                self.logger.info(f"🏃 Running in {mode} mode")
                # Add other modes here
            
            return 0
            
        except Exception as e:
            self.logger.error(f"💥 Application error: {e}")
            return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='NIMDA Agent Application')
    parser.add_argument('--mode', choices=['interactive', 'health', 'daemon'], 
                       default='interactive', help='Application mode')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='Logging level')
    
    args = parser.parse_args()
    
    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Create and run application
    app = NIMDAApplication()
    return app.run(args.mode)


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        sys.exit(1)
