from langchain_core.runnables import Runnable

from newsbot.features.common import BaseAgent
from ..llm.ai_news_llm import AINewsLLM
from ..graph.ai_news_graph_builder import AINewsGraphBuilder

class AINewsAgentManager(BaseAgent):
    """Agent manager for the AI news application workflow."""
    
    def create_agent(self) -> Runnable:
        """Create and configure the AI news agent based on session configuration."""
        
        # Extract session configuration
        llm_api_key = self.session_config.llm_api_key
        model = self.session_config.selected_model
        model_provider = self.session_config.selected_llm_provider        
        api_url = self.session_config.llm_api_url

        if llm_api_key is None:
            raise ValueError(
                "API key must be provided either in session config or environment variable."
            )

        if model is None:
            raise ValueError("Model must be selected in session config.")

        # Create LLM instance
        llm = AINewsLLM(
            model_provider=model_provider,
            model_name=model, 
            api_url=api_url,
            api_key=llm_api_key            
        ).llm
        
        # Build and return the AI news graph
        if not llm:
            raise ValueError("Failed to initialize AI news LLM")
        
        graph_builder = AINewsGraphBuilder(llm=llm, session_config=self.session_config)
        return graph_builder.build()