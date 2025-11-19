from langchain_core.tools import BaseTool
from langchain_core.runnables import Runnable
from dataclasses import dataclass

from abc import ABC, abstractmethod

from newsbot.core import SessionConfig

# Base model for agents
@dataclass
class BaseAgent(ABC):
    """Base class for all agents in the system."""

    session_config: SessionConfig

    @abstractmethod
    def create_agent(self) -> Runnable:     
        """Method to create and configure the agent."""
        pass
