from config import settings


_client = None


def get_supabase_client():
    """Get or create Supabase client. Returns None if not configured."""
    global _client
    if _client:
        return _client

    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        return None

    try:
        from supabase import create_client
        _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return _client
    except Exception:
        return None


async def create_session(match_id: str, match_name: str) -> dict | None:
    """Create a new analysis session in Supabase."""
    client = get_supabase_client()
    if not client:
        return {"id": f"local_{match_id}", "match_id": match_id, "match_name": match_name}

    try:
        result = client.table("analysis_sessions").insert({
            "match_id": match_id,
            "match_name": match_name,
            "status": "active",
        }).execute()
        return result.data[0] if result.data else None
    except Exception:
        return {"id": f"local_{match_id}", "match_id": match_id, "match_name": match_name}


async def save_insight(session_id: str, over_number: int, ball_number: int,
                       insight_text: str, insight_type: str = "tactical") -> dict | None:
    """Save a tactical insight to Supabase."""
    client = get_supabase_client()
    if not client:
        return None

    try:
        result = client.table("tactical_insights").insert({
            "session_id": session_id,
            "over_number": over_number,
            "ball_number": ball_number,
            "insight_text": insight_text,
            "insight_type": insight_type,
        }).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None


async def get_sessions() -> list:
    """Get all analysis sessions."""
    client = get_supabase_client()
    if not client:
        return []

    try:
        result = client.table("analysis_sessions").select("*").order(
            "created_at", desc=True
        ).limit(20).execute()
        return result.data or []
    except Exception:
        return []


async def get_session_history(session_id: str) -> dict | None:
    """Get full session with all insights for replay."""
    client = get_supabase_client()
    if not client:
        return None

    try:
        session = client.table("analysis_sessions").select("*").eq(
            "id", session_id
        ).single().execute()

        insights = client.table("tactical_insights").select("*").eq(
            "session_id", session_id
        ).order("created_at").execute()

        return {
            "session": session.data,
            "insights": insights.data or [],
        }
    except Exception:
        return None
