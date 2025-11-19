import logging
from enum import Enum

from langchain_core.runnables import Runnable
from langgraph.graph import StateGraph, START, END

from newsbot.core.config import SessionConfig
from ..node.fetch_news import FetchNewsNode
from ..node.summarize import NewsSummarizeNode
from ..node.save_result import SaveNewsNode
from ..state.ai_news_state import AINewsState

class NodeId(str, Enum):
    """Node identifiers for the AI news processing graph."""
    FETCH_NEWS = "fetch_news"
    SUMMARIZE = "summarize"
    SAVE_RESULT = "save_result"  # Fixed naming consistency
    

class AINewsGraphBuilder:
    """Builds a LangGraph workflow for AI news processing."""
    
    def __init__(self, llm: Runnable, session_config: SessionConfig) -> None:
        self.llm = llm
        self.session_config = session_config
    
    def build(self) -> Runnable:
        """Builds the AI news processing graph."""
        
        graph_builder = StateGraph(AINewsState)
        
        # Add nodes
        news_node = FetchNewsNode(session_config=self.session_config)
        graph_builder.add_node(NodeId.FETCH_NEWS.value, news_node.fetch_news)
        
        summarizer_node = NewsSummarizeNode(self.llm, self.session_config)
        graph_builder.add_node(NodeId.SUMMARIZE.value, summarizer_node.summarize)
        
        save_news_node = SaveNewsNode(session_config=self.session_config)  # Fixed parameter name
        graph_builder.add_node(NodeId.SAVE_RESULT.value, save_news_node.save_result)
        
        # Add edges (linear pipeline: fetch → summarize → save)
        graph_builder.add_edge(START, NodeId.FETCH_NEWS.value)
        graph_builder.add_edge(NodeId.FETCH_NEWS.value, NodeId.SUMMARIZE.value)
        graph_builder.add_edge(NodeId.SUMMARIZE.value, NodeId.SAVE_RESULT.value)
        graph_builder.add_edge(NodeId.SAVE_RESULT.value, END)
                
        # Compile the graph
        agent = graph_builder.compile()    
                
        return agent
        
    
    
        
                
        