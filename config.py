from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    OPENROUTER_API_KEY: str
    OPENROUTER_QWEN_MODEL: str
    OPENROUTER_DEEPSEEK_MODEL: str
    EMBEDDING_MODEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()