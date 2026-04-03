import httpx
from config import settings
from mock_data import get_mock_matches, get_mock_match_detail, generate_ball_by_ball_data


_matches_cache = []

async def get_current_matches():
    """Fetch current/live matches from CricketData.org API. (1 API call)"""
    global _matches_cache
    if settings.USE_MOCK_DATA or not settings.CRICKET_API_KEY:
        _matches_cache = get_mock_matches()
        return _matches_cache

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{settings.CRICKET_API_BASE}/currentMatches",
                params={"apikey": settings.CRICKET_API_KEY, "offset": 0},
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "success":
                matches = data.get("data", [])
                _matches_cache = matches
                return matches
            return get_mock_matches()
    except Exception:
        return get_mock_matches()


async def get_match_info(match_id: str):
    """
    Fetch detailed match info. 
    If the API fails, we check the _matches_cache for partial data.
    """
    if settings.USE_MOCK_DATA or not settings.CRICKET_API_KEY:
        return get_mock_match_detail(match_id)

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{settings.CRICKET_API_BASE}/match_info",
                params={"apikey": settings.CRICKET_API_KEY, "id": match_id},
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "success":
                return data.get("data", {})
            
            # API failure: check cache
            for m in _matches_cache:
                if m["id"] == match_id:
                    return m
            return get_mock_match_detail(match_id)
    except Exception:
        for m in _matches_cache:
            if m["id"] == match_id:
                return m
        return get_mock_match_detail(match_id)


async def get_match_scorecard(match_id: str):
    """
    Fetch scorecard for over-by-over polling. (1 API call)
    Returns the current match state — we call this once per over.
    """
    if settings.USE_MOCK_DATA or not settings.CRICKET_API_KEY:
        return get_mock_match_detail(match_id)

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{settings.CRICKET_API_BASE}/match_scoreCard",
                params={"apikey": settings.CRICKET_API_KEY, "id": match_id},
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "success":
                return data.get("data", {})
            return get_mock_match_detail(match_id)
    except Exception:
        return get_mock_match_detail(match_id)


async def get_ball_by_ball(match_id: str, match_info: dict = None):
    """Fetch ball-by-ball data for replay/demo mode only."""
    if settings.USE_MOCK_DATA or not settings.CRICKET_API_KEY:
        return generate_ball_by_ball_data(match_id, match_info)

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{settings.CRICKET_API_BASE}/match_bbb",
                params={"apikey": settings.CRICKET_API_KEY, "id": match_id},
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "success":
                return data.get("data", [])
            return generate_ball_by_ball_data(match_id)
    except Exception:
        return generate_ball_by_ball_data(match_id)
