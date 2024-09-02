from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_ID: int
    WRITER_ID: int

    POSTGRES_SERVER: str
    POSTGRES_SERVER_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_SERVER_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()