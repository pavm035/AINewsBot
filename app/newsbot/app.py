import logging
from dotenv import load_dotenv

from newsbot.ui import StreamlitUI
from newsbot.core import SessionConfig, ConfigManager

load_dotenv()
logger = logging.getLogger(__name__)


class BasicChatBotApp:
    """Main application class for the Basic chatbot."""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.ui = StreamlitUI(self.config_manager)
        self.session_config: SessionConfig | None = None

    def run(self):
        """Main function to run the application."""
        # Load the UI and get user selections
        self.session_config = self.ui.load_ui()

        # call llm and usecase handlers based on selections
        logger.info(f"Selected LLM Provider: {self.session_config.selected_llm_provider}")
        logger.info(f"Selected LLM API URL: {self.session_config.llm_api_url}")
        logger.info(f"Selected LLM Model: {self.session_config.selected_model}")
        logger.info(f"Selected Use Case: {self.session_config.selected_usecase}")
        logger.info(f"LLM API Key: {self.session_config.llm_api_key}")
        logger.info(f"Tavily API Key: {self.session_config.tavily_api_key}")
        logger.info(f"Selected AI News Frame: {self.session_config.selected_ai_news_frame}")

        # Pass session_config to chat, create agent on demand
        self.ui.run(self.session_config)
