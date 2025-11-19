from .config_manager import UsecaseOption, LLMProvider
from pydantic import BaseModel, Field, SecretStr

class SessionConfig(BaseModel):
    """User's session-specific configuration."""
    
    selected_llm_provider: LLMProvider = LLMProvider.GROQ
    selected_usecase: UsecaseOption | None = None
    selected_model: str | None = None
    llm_api_key: SecretStr | None = Field(default=None, description="User-provided API key")
    llm_api_url: str | None = None  # User-provided API URL (overrides settings)
    tavily_api_key: SecretStr | None = Field(default=None, description="Tavily API key for search")
    thread_id: str | None = None
    selected_ai_news_frame: str | None = None
