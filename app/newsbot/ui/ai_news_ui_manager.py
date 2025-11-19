import streamlit as st

from newsbot.core import SessionConfig
from newsbot.features import AISummaryType
from newsbot.features.ai_news.agent.ai_news_agent import AINewsAgentManager

class AINewsUIManager:
    """Manager for AI News UI interactions."""
    
    def __init__(self, session_config: SessionConfig):
        self.session_config = session_config
    

    def run(self):
        """Method that uses ai news agent to fetch and display it"""
        
        if "news_agent" not in st.session_state:
            st.session_state.news_agent = None
        
        news_agent_mgr = AINewsAgentManager(session_config=self.session_config)
        st.session_state.news_agent = news_agent_mgr
        news_agent = news_agent_mgr.create_agent()
        
        # Execute without additional spinner (handled by parent)
        response_state = news_agent.invoke({
            "query": "Fetch latest news on AI",
            "time_frame": self.session_config.selected_ai_news_frame
        })
        
        summary = response_state.get("summary", "N/A")
        st.markdown(summary)
