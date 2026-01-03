"""
Base Tool Class
All tools should inherit from this base class to ensure a consistent interface
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pathlib import Path


class BaseTool(ABC):
    """Base tool class"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description"""
        pass
    
    @abstractmethod
    async def process(self, *args, **kwargs) -> Any:
        """
        Processing logic
        Subclasses must implement this method
        """
        pass
    
    def validate_input(self, *args, **kwargs) -> bool:
        """
        Input validation
        Subclasses can override this method for custom validation
        """
        return True
