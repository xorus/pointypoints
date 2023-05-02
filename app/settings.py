from pydantic import BaseSettings


class Settings(BaseSettings):
    twitch_client_id: str
    twitch_client_secret: str
    base_url: str
    # openssl rand -hex 32
    jwt_secret: str
    session_secret: str


settings = Settings()
