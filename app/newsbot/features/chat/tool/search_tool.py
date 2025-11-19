import logging
from typing import Optional

from langchain_tavily import TavilySearch
from langchain_core.tools import BaseTool
from pydantic import SecretStr

logger = logging.getLogger(__name__)


class SearchTool:
    """
    A search tool that uses Tavily Search to perform web searches.
    
    This class provides a clean interface for web search functionality
    that can be integrated into LangChain tool workflows.
    """

    def __init__(self, api_key: SecretStr, max_results: int = 5, topic: str = "general") -> None:
        """
        Initialize the search tool.
        
        Args:
            api_key: Tavily API key for authentication
            max_results: Maximum number of search results to return
            topic: Search topic filter (general, news, etc.)
        """
        try:
            self.tool = TavilySearch(
                tavily_api_key=api_key, 
                max_results=max_results, 
                topic=topic
            )
            logger.info(f"Initialized Tavily search tool with max_results={max_results}, topic={topic}")
        except Exception as e:
            logger.error(f"Failed to initialize Tavily search tool: {e}")
            raise

    def get_tool(self) -> BaseTool:
        """
        Get the LangChain-compatible search tool.
        
        Returns:
            BaseTool: The configured Tavily search tool
        """
        return self.tool

    @property
    def name(self) -> str:
        """Get the tool name."""
        return "tavily_search"

    @property  
    def description(self) -> str:
        """Get the tool description."""
        return "Search the web for current information on any topic"
