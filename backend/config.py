import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    CRICKET_API_KEY: str = os.getenv("CRICKET_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    USE_MOCK_DATA: bool = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
    CRICKET_API_BASE: str = "https://api.cricapi.com/v1"


settings = Settings()
