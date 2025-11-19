import logging

from langchain.chat_models import init_chat_model
from newsbot.features.common import BaseLLM

logger = logging.getLogger(__name__)

class ChatBotLLM(BaseLLM):
    """A chatbot LLM that integrates with a LLM model and supports tools."""

    def build_llm(self):
        try:    
            llm = init_chat_model(
                model_provider=self.model_provider.normalized,
                model=self.model_name,
                api_key=self.api_key,
                base_url=self.api_url,
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM {self.model_name} from {self.model_provider.value}: {e}")
            raise

        if not self.tools:
            logger.info(f"Initialized LLM (NO TOOLS) with model: {self.model_name}")
            self.llm = llm
            return
        
        self.llm = llm.bind_tools(self.tools)
        logger.info(f"Initialized LLM (WITH {len(self.tools)} TOOLS) with model: {self.model_name}")        

