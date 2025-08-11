"""
Base command class for Modular Command Pattern (MCP)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)

class BaseCommand(ABC):
    """Abstract base class for all commands using MCP pattern"""
    
    def __init__(self, params: Dict[str, Any]):
        self.params = params
        self.result = {"success": False, "message": "", "data": {}}
    
    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """Execute the command and return result"""
        pass
    
    def validate_params(self) -> bool:
        """Validate required parameters"""
        return True
    
    def log_execution(self, action: str) -> None:
        """Log command execution"""
        logger.info(f"Executing {self.__class__.__name__}: {action}")
    
    def set_success(self, message: str, data: Dict[str, Any] = None) -> None:
        """Set successful result"""
        self.result = {
            "success": True,
            "message": message,
            "data": data or {}
        }
    
    def set_error(self, message: str, data: Dict[str, Any] = None) -> None:
        """Set error result"""
        self.result = {
            "success": False,
            "message": message,
            "data": data or {}
        }
