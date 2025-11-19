import logging

from typing import Any
from abc import ABC, abstractmethod
from pydantic import BaseModel, SecretStr, Field, model_validator, field_validator
from langchain_core.tools import BaseTool
from langchain_core.runnables import Runnable

# from src.core import LLMProvider
from newsbot.core import LLMProvider

logger = logging.getLogger(__name__)


class BaseLLM(BaseModel, ABC):
    """Abstract base class for Language Model implementations."""
    
    model_config = {"arbitrary_types_allowed": True}

    # fields
    api_key: SecretStr = Field(
        ..., description="API key for accessing the language model service.",
        exclude=True
    )
    model_provider: LLMProvider = Field(
        ..., description="Provider of the language model."
    )
    model_name: str = Field(
        ..., description="Name of the language model."
    )
    api_url: str | None = Field(
        default=None, description="URL endpoint for the language model API."
    )
    temperature: float = Field(
        default=0.7, description="Sampling temperature for the language model."
    )
    tools: list[BaseTool] = Field(
        default_factory=list, description="List of tools available to the language model."
    )

    llm: Runnable | None = Field(default=None, exclude=True)

    # validators
    @field_validator("temperature")
    def _validate_temperature(cls, v):
        if not 0.0 <= v <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v
    
    # methods
    @model_validator(mode="after")
    def _post_init(self) -> "BaseLLM":
        """Run setup AFTER Pydantic creates the object."""
        try:
            self.build_llm()
            logger.info(f"Successfully initialized {self.model_provider} {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            
        return self

    @abstractmethod
    def build_llm(self):
        """Subclasses must build and assign the underlying LLM model."""
        pass
