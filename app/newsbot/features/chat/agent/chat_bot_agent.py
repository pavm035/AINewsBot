from langchain_core.tools import BaseTool
from langchain_core.runnables import Runnable

from newsbot.core import UsecaseOption
from newsbot.features.common import BaseAgent

from ..tool.search_tool import SearchTool
from ..llm.chat_bot_llm import ChatBotLLM
from ..graph.chat_bot_graph_builder import ChatBotGraphBuilder

class ChatBotAgent(BaseAgent):
    """Agent class for the chatbot application."""

    def create_agent(self) -> Runnable:        
        """Create and configure the chatbot agent based on session configuration."""
        self._validate_configuration()
        tools = self._build_tools()
        llm = self._build_llm(tools)
        return self._build_graph(llm, tools)
                        
    def _validate_configuration(self):
        """Validate session configuration"""
        if self.session_config.llm_api_key is None:
            raise ValueError("API key must be provided in session config.")
        
        if self.session_config.selected_model is None:
            raise ValueError("Model must be selected in session config.")
        
        if (self.session_config.selected_usecase == UsecaseOption.CHATBOT_WITH_WEB_SEARCH
             and self.session_config.tavily_api_key is None):
            raise ValueError(
                    "Tavily API key must be provided for web search use case."
                )
    def _build_tools(self) -> list[BaseTool]:
        """Build tools based on configuration"""
        
        tools: list[BaseTool] = []
        if (self.session_config.selected_usecase == UsecaseOption.CHATBOT_WITH_WEB_SEARCH
            and self.session_config.tavily_api_key):
            searchTool = SearchTool(api_key=self.session_config.tavily_api_key)
            tools = [searchTool.tool]
        return tools
    
    def _build_llm(self, tools: list[BaseTool]) -> Runnable:
        """Builds and configure LLM with tools."""
        
        # No need for additional validation here - _validate_configuration() already handled it
        # We can safely assert these are not None after validation
        assert self.session_config.selected_model is not None
        assert self.session_config.llm_api_key is not None
        
        llm = ChatBotLLM(
            model_provider=self.session_config.selected_llm_provider,
            model_name=self.session_config.selected_model,
            api_url=self.session_config.llm_api_url,
            api_key=self.session_config.llm_api_key,
            tools=tools
        ).llm
        
        if llm is None:
            raise ValueError("Failed to create LLM instance")
            
        return llm
        
    def _build_graph(self, llm: Runnable, tools: list[BaseTool]) -> Runnable:
        """Builds the chatbot graph with given llm and tools"""
        graph_builder = ChatBotGraphBuilder(llm=llm, tools=tools)
        return graph_builder.build()