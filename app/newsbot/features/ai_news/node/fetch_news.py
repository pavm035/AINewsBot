import logging
from langchain_tavily import TavilySearch
from pydantic import BaseModel

from newsbot.core.config import SessionConfig
from ..state.ai_news_state import AINewsState

logger = logging.getLogger(__name__)

class FetchNewsNode(BaseModel):
    """Node for fetching AI news articles using Tavily search."""
    session_config: SessionConfig
    
    def fetch_news(self, state: AINewsState) -> dict:
        """Retrieves AI news articles using Tavily search API."""
        logger.info("Starting Tavily news search")
        
        # Validate required configuration
        if self.session_config.selected_ai_news_frame is None:
            raise ValueError("Time frame for AI news must be specified")
            
        if self.session_config.tavily_api_key is None:
            raise ValueError("Tavily API key is required for news fetching")
            
        query = state.get("query", "").strip()
        if not query:
            raise ValueError("Query cannot be empty for news search")
        
        # Map UI time frames to Tavily API values
        TIME_RANGE_MAP = {
            "Daily": "day",
            "Weekly": "week", 
            "Monthly": "month"
        }
        
        time_range = TIME_RANGE_MAP.get(self.session_config.selected_ai_news_frame)
        if not time_range:
            raise ValueError(f"Unsupported time frame: {self.session_config.selected_ai_news_frame}")
        
        try:
            tavily_search = TavilySearch(
                topic="news",
                query=query,
                time_range=time_range,
                tavily_api_key=self.session_config.tavily_api_key
            )
            
            logger.info(f"Searching for '{query}' with time range '{time_range}'")
            response = tavily_search.invoke(query)
            
            logger.debug(f"Tavily response type: {type(response)}")
            results = response.get("results", [])
            
            logger.info(f"Found {len(results)} news articles")
            return {"fetch_results": results}
            
        except Exception as e:
            logger.error(f"Failed to fetch news: {e}")
            raise RuntimeError(f"News fetching failed: {e}")