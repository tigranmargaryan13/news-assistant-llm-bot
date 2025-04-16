from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseLLMSettings(BaseSettings):
    OPENAI_API_KEY: str
    MINI_LLM_MODEL: str
    BOT_TOKEN: str
    CHANNEL_ID: int
    SQLALCHEMY_CONNECTION_STRING: str | None = None  # Optional DB string

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = BaseLLMSettings()
