from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL : str
    DB_NAME : str  = "live_db"

    class Config:
        env_file = ".env"
        case_sensitivity = True

settings = Settings()