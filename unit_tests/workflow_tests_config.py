"""
Configuration for workflow_tests component
Configuration and settings for workflow_tests

This configuration file defines all settings and parameters for the workflow_tests component.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class WorkflowTestsConfig:
    """Configuration class for workflow_tests component."""
    
    # Component identification
    component_name: str = "workflow_tests"
    version: str = "1.0.0"
    
    # Operational settings
    enabled: bool = True
    debug_mode: bool = False
    
    # Logging configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Performance settings
    max_concurrent_operations: int = 10
    timeout_seconds: int = 30
    
    # Integration settings
    enable_monitoring: bool = True
    enable_caching: bool = True
    
    @classmethod
    def from_env(cls) -> "WorkflowTestsConfig":
        """Create configuration from environment variables."""
        return cls(
            component_name=os.getenv("COMPONENT_NAME", "workflow_tests"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            max_concurrent_operations=int(os.getenv("MAX_CONCURRENT_OPS", "10")),
            timeout_seconds=int(os.getenv("TIMEOUT_SECONDS", "30")),
            enable_monitoring=os.getenv("ENABLE_MONITORING", "true").lower() == "true",
            enable_caching=os.getenv("ENABLE_CACHING", "true").lower() == "true"
        )
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "WorkflowTestsConfig":
        """Create configuration from dictionary."""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__dataclass_fields__})
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            field.name: getattr(self, field.name) 
            for field in self.__dataclass_fields__.values()
        }
    
    def validate(self) -> bool:
        """Validate configuration parameters."""
        if self.max_concurrent_operations <= 0:
            raise ValueError("max_concurrent_operations must be positive")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        return True


# Default configuration instance
DEFAULT_CONFIG = WorkflowTestsConfig()


def get_config(config_source: Optional[str] = None) -> WorkflowTestsConfig:
    """
    Get configuration from various sources.
    
    Args:
        config_source: Source of configuration ('env', 'default', or path to config file)
    
    Returns:
        Configuration instance
    """
    if config_source == "env":
        return WorkflowTestsConfig.from_env()
    elif config_source is None or config_source == "default":
        return DEFAULT_CONFIG
    else:
        # Load from file (placeholder for file loading logic)
        return DEFAULT_CONFIG


if __name__ == "__main__":
    # Configuration testing
    config = get_config("env")
    print(f"Configuration for {config.component_name}:")
    print(f"  Version: {config.version}")
    print(f"  Log Level: {config.log_level}")
    print(f"  Max Operations: {config.max_concurrent_operations}")
    print(f"  Validation: {config.validate()}")
