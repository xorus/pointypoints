from pydantic import BaseSettings


class Settings(BaseSettings):
    twitch_client_id: str
    twitch_client_secret: str
    base_url: str
    # openssl rand -hex 32
    jwt_secret: str
    session_secret: str
    database_url: str

    class Config:
        env_prefix = ""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
