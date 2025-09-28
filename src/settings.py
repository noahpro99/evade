from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        cli_parse_args=True,
        extra="ignore",
    )

    TOGETHER_API_KEY: str | None = Field(
        default=None, description="API key for Together"
    )
    INSTAGRAM_USERNAME: str | None = Field(
        default=None, description="Instagram username for login"
    )
    INSTAGRAM_PASSWORD: str | None = Field(
        default=None, description="Instagram password for login"
    )
    INSTAGRAM_DM_RECIPIENT: str = Field(description="Instagram username to send DMs to")
    TITLE_KEYWORD: str = Field(
        default="Messenger call", description="Keyword to identify target window"
    )


settings = AppSettings()  # pyright: ignore[reportCallIssue]
