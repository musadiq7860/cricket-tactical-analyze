import httpx
from config import settings
from mock_data import get_mock_matches, get_mock_match_detail, generate_ball_by_ball_data

_matches_cache = []

def _map_match_item(em):
    # Map Entity Sport match item to frontend expected structure
    t1 = em.get("teama", {})
    t2 = em.get("teamb", {})
    
    def parse_score(s, o):
        if not s: return {"r": 0, "w": 0, "o": 0.0}
        parts = str(s).split('/')
        r = int(parts[0]) if parts[0].isdigit() else 0
        w = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        o_val = float(o) if o else 0.0
        return {"r": r, "w": w, "o": o_val}

    t1_score = parse_score(t1.get("scores"), t1.get("overs"))
    t2_score = parse_score(t2.get("scores"), t2.get("overs"))
    
    score_arr = []
    if t1_score["r"] > 0 or t1_score["w"] > 0 or t1_score["o"] > 0:
        score_arr.append({
            "team": t1.get("name"),
            "inning": f"{t1.get('short_name', '')} Inning",
            "r": t1_score["r"], "w": t1_score["w"], "o": t1_score["o"]
        })
    if t2_score["r"] > 0 or t2_score["w"] > 0 or t2_score["o"] > 0:
        score_arr.append({
            "team": t2.get("name"),
            "inning": f"{t2.get('short_name', '')} Inning",
            "r": t2_score["r"], "w": t2_score["w"], "o": t2_score["o"]
        })
        
    v = em.get("venue", {})
    v_name = v.get('name', '')
    v_loc = v.get('location', '')
    v_str = f"{v_name}, {v_loc}".strip(", ")
    if not v_str:
        v_str = "Unknown Venue"
        
    return {
        "id": str(em.get("match_id")),
        "name": em.get("title") or em.get("short_title", "Match"),
        "status": em.get("status_note") or em.get("status_str", "Live"),
        "venue": v_str,
        "date": em.get("date_start_ist", ""),
        "matchType": em.get("format_str", "T20"),
        "teams": [t1.get("name", "Team A"), t2.get("name", "Team B")],
        "score": score_arr,
        "tpiTeam1": {"name": t1.get("name", "Team A"), "shortname": t1.get("short_name", "A"), "img": t1.get("logo_url", "")},
        "tpiTeam2": {"name": t2.get("name", "Team B"), "shortname": t2.get("short_name", "B"), "img": t2.get("logo_url", "")}
    }


async def get_current_matches():
    global _matches_cache
    if settings.USE_MOCK_DATA or not settings.ENTITY_SPORT_API_TOKEN:
        _matches_cache = get_mock_matches()
        return _matches_cache

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{settings.ENTITY_API_BASE}/matches/",
                params={"status": 2, "token": settings.ENTITY_SPORT_API_TOKEN},
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "ok":
                items = data.get("response", {}).get("items", [])
                matches = [_map_match_item(em) for em in items]
                if matches:
                    _matches_cache = matches
                return _matches_cache
            return get_mock_matches()
    except Exception as e:
        print(f"Error fetching matches: {e}")
        return get_mock_matches()


async def get_match_info(match_id: str):
    """Fetch detailed match info/scorecard."""
    if settings.USE_MOCK_DATA or not settings.ENTITY_SPORT_API_TOKEN:
        return get_mock_match_detail(match_id)

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{settings.ENTITY_API_BASE}/matches/{match_id}/scorecard",
                params={"token": settings.ENTITY_SPORT_API_TOKEN},
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "ok":
                res = data.get("response", {})
                
                base_match = _map_match_item(res)
                
                # Parse batting/bowling from latest inning
                innings = res.get("innings", [])
                latest_inning = None
                if innings:
                    innings.sort(key=lambda x: x.get("number", 0), reverse=True)
                    latest_inning = innings[0]
                    
                batting_arr = []
                bowling_arr = []
                
                if latest_inning:
                    for b in latest_inning.get("batsmen", []):
                        batting_arr.append({
                            "name": b.get("name", ""),
                            "r": int(b.get("runs") or 0),
                            "b": int(b.get("balls_faced") or 0),
                            "4s": int(b.get("fours") or 0),
                            "6s": int(b.get("sixes") or 0),
                            "sr": float(b.get("strike_rate") or 0.0),
                            "batting": str(b.get("batting", "false")).lower() == "true",
                            "dismissal": b.get("how_out", "")
                        })
                        
                    for bw in latest_inning.get("bowlers", []):
                        bowling_arr.append({
                            "name": bw.get("name", ""),
                            "o": float(bw.get("overs") or 0.0),
                            "m": int(bw.get("maidens") or 0),
                            "r": int(bw.get("runs_conceded") or 0),
                            "w": int(bw.get("wickets") or 0),
                            "eco": float(bw.get("econ") or 0.0)
                        })
                        
                base_match["batting"] = batting_arr
                base_match["bowling"] = bowling_arr
                return base_match
                
    except Exception as e:
        print(f"Error fetching scorecard: {e}")
        
    for m in _matches_cache:
        if m["id"] == match_id:
            return m
    return get_mock_match_detail(match_id)


async def get_match_scorecard(match_id: str):
    return await get_match_info(match_id)


async def get_ball_by_ball(match_id: str, match_info: dict = None):
    # Entity Sport `innings` endpoint requires specific syntax or doesn't exist for ball by ball.
    # Fallback to pure generator / mock logic to guarantee zero-rate-limit demonstration.
    return generate_ball_by_ball_data(match_id, match_info)
