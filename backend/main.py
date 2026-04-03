from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI(
    title="Cricket Tactical Analyzer API",
    description="Real-time AI-powered tactical cricket match analysis",
    version="1.0.0",
)

# CORS — allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health_check():
    from config import settings
    return {
        "status": "ok",
        "mock_mode": settings.USE_MOCK_DATA,
        "cricket_api_configured": bool(settings.CRICKET_API_KEY),
        "groq_api_configured": bool(settings.GROQ_API_KEY),
        "supabase_configured": bool(settings.SUPABASE_URL and settings.SUPABASE_KEY),
    }
