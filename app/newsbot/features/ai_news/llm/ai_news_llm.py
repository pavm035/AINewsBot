import logging

from langchain.chat_models import init_chat_model
from newsbot.features.common import BaseLLM

logger = logging.getLogger(__name__)


class AINewsLLM(BaseLLM):
    """AI news LLM that integrates with language models for news processing."""

    def build_llm(self) -> None:
        """Build and initialize the AI news LLM."""
        try:    
            self.llm = init_chat_model(
                model_provider=self.model_provider.normalized,
                model=self.model_name,
                api_key=self.api_key,  # Already a SecretStr from BaseLLM
                base_url=self.api_url,
            )
            logger.info(f"Initialized AI news LLM with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize AI news LLM {self.model_name}: {e}")
            raise