import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENTITY_SPORT_API_TOKEN: str = os.getenv("ENTITY_SPORT_API_TOKEN", "ec471071441bb2ac538a0ff901abd249")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    USE_MOCK_DATA: bool = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
    ENTITY_API_BASE: str = os.getenv("ENTITY_API_BASE", "https://rest.entitysport.com/v2")


settings = Settings()
