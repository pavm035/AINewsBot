from typing import NotRequired, Any
from typing_extensions import TypedDict

from ..model.types import AISummaryType


class AINewsState(TypedDict):
    """
    State representation for the AI news processing workflow.
    
    This TypedDict defines the structure of state that flows through
    the AI news processing graph nodes (fetch → summarize → save).
    
    Fields:
        query: The news query/topic to process
        time_frame: Optional time frame for news filtering (e.g., "24h", "week")
        fetch_results: Optional list of fetched news articles as dictionaries
        summary: Optional generated summary text from the LLM
    """
    query: str    
    time_frame: NotRequired[str]
    fetch_results: NotRequired[list[dict]]
    summary: NotRequired[str]