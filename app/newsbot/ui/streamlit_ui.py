from langchain_core.runnables import RunnableConfig
from pydantic import SecretStr
import streamlit as st

from newsbot.core import ConfigManager, SessionConfig, UsecaseOption, LLMProvider
from .chatui_manager import ChatUIManager
from .ai_news_ui_manager import AINewsUIManager
from newsbot.features.ai_news.model.types import AISummaryType


class StreamlitUI:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.session_config = SessionConfig()

    def load_ui(self):
        st.set_page_config(
            page_title="🤖 " + self.config_manager.config.page_title, layout="wide"
        )

        st.header("🤖 " + self.config_manager.config.page_title)

        with st.sidebar:
            # LLM Provider selection
            llm_providers = [
                provider.value
                for provider in self.config_manager.config.llm_config.providers.keys()
            ]
            selected_provider = st.selectbox(
                "Select LLM Provider:", 
                llm_providers,
                key="llm_provider_select"
            )
            self.session_config.selected_llm_provider = LLMProvider(selected_provider)
            if selected_provider is not None:
                self.session_config.llm_api_url = (
                    self.config_manager.config.get_provider_config(
                        self.session_config.selected_llm_provider
                    ).api_url
                )

            # Model selections
            models = self.config_manager.config.llm_config.providers[
                self.session_config.selected_llm_provider
            ].models

            self.session_config.selected_model = st.selectbox(
                f"Select Model ({self.session_config.selected_llm_provider.value}):",
                models,
                key="llm_model_select"
            )

            # usecase selection
            usecase_options = [
                option.value for option in self.config_manager.config.usecases.options
            ]
            selected_usecase = st.selectbox(
                "Select Use Case:", 
                usecase_options,
                key="usecase_select"
            )
            self.session_config.selected_usecase = UsecaseOption(selected_usecase)

            # API Key Input
            api_key = st.text_input(
                "API Key:",
                type="password",
                key="api_key_input",
                value=self.session_config.llm_api_key or "",
            )
            
            if api_key is None:
                raise ValueError("LLM API key can't be None")
            
            self.session_config.llm_api_key = SecretStr(api_key)

            # Validation
            if not self.session_config.llm_api_key:
                if self.session_config.selected_llm_provider == LLMProvider.GROQ:
                    st.warning(
                        "Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys",
                        icon="⚠️",
                    )
                elif self.session_config.selected_llm_provider == LLMProvider.OPENAI:
                    st.warning(
                        "Please enter your OpenAI API key to proceed. Don't have? refer : https://platform.openai.com/account/api-keys",
                        icon="⚠️",
                    )
                else:
                    st.warning(
                        "Please enter your API key to proceed.",
                        icon="⚠️",
                    )

            match self.session_config.selected_usecase:
                case UsecaseOption.BASIC_CHATBOT:
                    pass
                case UsecaseOption.CHATBOT_WITH_WEB_SEARCH:
                    self._build_chatbot_web_search()
                case UsecaseOption.AI_NEWS:
                    self._build_tavily_api_selection()
                    self._build_ai_news_ui()
                case _:
                    st.warning("Use case not supported yet, please come back", icon="⚠️")

        return self.session_config

    def run(self, session_config: SessionConfig) -> None:
        """Runs the streamlit UI based on the selected use case."""        

        match session_config.selected_usecase:
            case UsecaseOption.BASIC_CHATBOT | UsecaseOption.CHATBOT_WITH_WEB_SEARCH:
                print("selected AI CHATBOT")
                if not session_config.llm_api_key:
                    st.chat_input("Enter API Key first…", disabled=True)
                    return

                chat_manager = ChatUIManager(session_config)
                chat_manager.start_chat()
            case UsecaseOption.AI_NEWS:            
                self._display_ai_news_main_area()
            case _:
                st.error("Selected use case is not implemented yet.")

    # UI builders - PRIVATE API
    def _build_tavily_api_selection(self):
        tavily_api_key = st.text_input(
            "TAVILY API Key:",
            type="password",
            key="tavily_api_key_input",
            value=self.session_config.tavily_api_key or "",
        )
        
        if tavily_api_key is None:
            raise ValueError("Tavily API can't be None")
        
        self.session_config.tavily_api_key = SecretStr(tavily_api_key)

        # Validation
        if not self.session_config.tavily_api_key:
            st.warning(
                "Please enter your TAVILY API key to proceed. Don't have? refer : https://tavily.com/docs/getting-started/api-keys",
                icon="⚠️",
            )

    def _build_chatbot_web_search(self):
        """Builds UI for chatbot with web searh in sidebar"""
        self._build_tavily_api_selection()

    def _build_ai_news_ui(self):
        """Builds the ai news ui in streamlit in sidebar"""

        st.subheader("📰 AI News Explorer ")
        # Time frame
        self.session_config.selected_ai_news_frame = st.selectbox(
            "📅 Select Time Frame",
            AISummaryType.values(),
            index=0,
            key="ai_news_time_frame_select",
        )
        
        # Fetch news button - immediate execution instead of callback
        fetch_clicked = st.button(
            "🔍 Fetch Latest AI News",
            use_container_width=True,
            disabled=not self.session_config.llm_api_key or not self.session_config.tavily_api_key
        )
        
        # Execute immediately when button is clicked - set flag for main area display
        if fetch_clicked and self.session_config.llm_api_key and self.session_config.tavily_api_key:
            st.session_state.fetch_news = True
            st.rerun()  # Force immediate rerun to show spinner in main area

    def did_click_fetch_ai_news_button(self):
        """Callback sets a flag in session state"""
        st.session_state.fetch_news = True
        
    def _display_ai_news_main_area(self):
        """Display AI news content in main area with immediate spinner"""
        if st.session_state.get('fetch_news', False):
            st.session_state.fetch_news = False  # Reset flag
            
            # Show spinner immediately in main area
            with st.spinner("Fetching AI News...⏳"):
                ai_news_manager = AINewsUIManager(self.session_config)
                ai_news_manager.run()
        else:
            # Show placeholder when no news is being fetched
            st.info("👈 Click 'Fetch Latest AI News' in the sidebar to get started!")
                