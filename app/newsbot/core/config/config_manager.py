import yaml
from pydantic import BaseModel, Field
from enum import Enum
from pathlib import Path
import threading


# 🧠 LLM Providers
class LLMProvider(str, Enum):
    GROQ = "Groq"
    RAKUTEN = "Rakuten"
    OPENAI = "OpenAI"
    ANTHROPIC = "Anthropic"

    @property
    def normalized(self) -> str:
        """Return the standardized provider name."""
        match self:
            case LLMProvider.RAKUTEN:
                return "openai"
        return self.value.lower()


class UsecaseOption(str, Enum):
    BASIC_CHATBOT = "Basic Chatbot"
    CHATBOT_WITH_WEB_SEARCH = "Chatbot With Web Search"
    AI_NEWS = "AI News"


# ⚙️ Model per provider
class ProviderConfig(BaseModel):
    api_url: str | None = None
    models: list[str]


# 🏗️ LLM section
class LLMConfig(BaseModel):
    providers: dict[LLMProvider, ProviderConfig] = Field(..., validate_default=True)


# 🧩 Usecases section
class UsecaseConfig(BaseModel):
    options: list[UsecaseOption]


# 🏠 Root config
class AppConfig(BaseModel):
    page_title: str
    llm_config: LLMConfig
    usecases: UsecaseConfig

    # other settings
    temperature: float = 0.7
    # Tool settings
    max_search_results: int = 5
    search_topic: str = "general"

    def get_provider_config(self, provider: LLMProvider) -> ProviderConfig:
        """Get provider configuration with detiled error context."""
        try:
            provider_config = self.llm_config.providers.get(provider)
            if provider_config is None:
                available = list(self.llm_config.providers.keys())
                raise ValueError(
                    f"Provider '{provider}' not found. Available {available}"
                )

            return provider_config
        except AttributeError as e:
            raise ValueError(f"Invalid config structure: {e}")


class ConfigManager:
    """Load the configuration from yaml file"""

    _instance = None
    _initialized = False
    _lock = threading.Lock()

    # Singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_file=None):
        if self._initialized:
            return

        self._initialized = True
        if config_file is None:
            config_file = Path(__file__).parent / "uiconfig.yml"

        try:
            with open(config_file, "r") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {config_file}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {config_file}: {e}")

        self.config = AppConfig(**data)

        self._validate_config()

    def _validate_config(self):
        """Ensure config has required fields"""
        if not self.config.llm_config.providers:
            raise ValueError("No LLM providers configured")

        for provider, config in self.config.llm_config.providers.items():
            if not config.models:
                raise ValueError(f"No models configured for {provider}")
