import asyncio
import json
from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse
from cricket_api import get_current_matches, get_match_info, get_match_scorecard, get_ball_by_ball
from match_state import MatchState
from groq_analyzer import generate_tactical_insight
from supabase_client import create_session, save_insight, get_sessions, get_session_history
from config import settings


router = APIRouter(prefix="/api")


@router.get("/matches")
async def list_matches():
    """Get all available matches (live + recent). 1 API call."""
    matches = await get_current_matches()
    return {"matches": matches}


@router.get("/match/{match_id}")
async def match_detail(match_id: str):
    """Get detailed match information and scorecard. 1 API call."""
    match = await get_match_info(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return {"match": match}


@router.get("/match/{match_id}/stream")
async def match_stream(match_id: str, mode: str = "auto"):
    """
    SSE endpoint: streams match updates with AI tactical insights.

    Polling strategy (over-by-over):
    - Mock mode: replays all ball-by-ball data from mock generator
    - Complete match: fetches full historical ball-by-ball data and replays it
    - Live match: polls scorecard API ONCE PER OVER (~20 calls for T20)
    """
    match = await get_match_info(match_id)
    status = match.get("status", "").lower() if match else "live"
    is_complete = "won" in status or "tied" in status or "draw" in status or "complete" in status or "abandoned" in status or "stumps" in status

    force_mock = mode == "demo"
    if force_mock or settings.USE_MOCK_DATA:
        return EventSourceResponse(_historical_replay_generator(match_id, mode="demo"))

    if is_complete:
        return EventSourceResponse(_historical_replay_generator(match_id, mode="historical"))
    else:
        return EventSourceResponse(_live_over_by_over_generator(match_id, match))


async def _live_over_by_over_generator(match_id: str):
    """
    LIVE MODE: Over-by-over polling.
    Polls scorecard API once per over. Total API calls = number of overs.
    For 2 T20 matches: 20 + 20 = 40 calls. For 2 ODIs: 50 + 50 = 100 calls.
    """
    match = await get_match_info(match_id)  # 1 API call
    match_name = match.get("name", f"Match {match_id}") if match else f"Match {match_id}"
    session = await create_session(match_id, match_name)
    session_id = session.get("id", "local") if session else "local"

    yield {
        "event": "session_start",
        "data": json.dumps({
            "session_id": session_id,
            "match_name": match_name,
            "mode": "live",
            "polling": "over-by-over",
        }),
    }

    state = MatchState(match_id=match_id)
    if match:
        state.match_format = match.get("matchType", "T20")
        scores = match.get("score", [])
        if len(scores) >= 2:
            state.target = scores[0].get("r", 0) + 1

    last_over = -1
    last_total_runs = 0
    max_overs = 50 if state.match_format == "ODI" else 20
    poll_interval = 30  # seconds between polls

    # Initial scorecard state
    scorecard = await get_match_scorecard(match_id)  # 1 API call
    api_calls = 2  # match_info + first scorecard

    while True:
        # Extract current over from scorecard
        current_score = _extract_score_from_api(scorecard)
        current_over = current_score.get("overs", 0)
        current_runs = current_score.get("runs", 0)
        current_wickets = current_score.get("wickets", 0)
        batting_team = current_score.get("batting_team", "")
        bowling_team = current_score.get("bowling_team", "")

        over_int = int(current_over)

        # New over detected — send update
        if over_int > last_over:
            over_runs = current_runs - last_total_runs

            # Update match state
            state.total_runs = current_runs
            state.total_wickets = current_wickets
            state.current_over = over_int
            state.current_ball = int(round((current_over - over_int) * 10))
            state.batting_team = batting_team
            state.bowling_team = bowling_team
            overs_bowled = current_over if current_over > 0 else 0.1
            state.current_run_rate = round(current_runs / overs_bowled, 2)
            if state.target:
                remaining_overs = max(max_overs - current_over, 0.1)
                remaining_runs = state.target - current_runs
                state.required_run_rate = round(remaining_runs / remaining_overs, 2) if remaining_runs > 0 else 0.0

            # Track over-by-over runs
            state.over_by_over_runs.append(over_runs)

            # Send ball summary (aggregate for the over)
            yield {
                "event": "ball",
                "data": json.dumps({
                    "ball": {
                        "over": over_int,
                        "ball": 6,
                        "over_ball": f"{over_int}.6",
                        "runs": over_runs,
                        "is_wicket": current_wickets > (state.total_wickets - (1 if over_runs == 0 and current_wickets > 0 else 0)),
                        "is_boundary": over_runs >= 4,
                        "batting_team": batting_team,
                        "bowling_team": bowling_team,
                    },
                    "state": {
                        "total_runs": state.total_runs,
                        "total_wickets": state.total_wickets,
                        "current_over": state.current_over,
                        "current_ball": state.current_ball,
                        "current_rr": state.current_run_rate,
                        "required_rr": state.required_run_rate,
                        "striker": current_score.get("striker", ""),
                        "striker_runs": current_score.get("striker_runs", 0),
                        "striker_balls": current_score.get("striker_balls", 0),
                        "partnership_runs": current_score.get("partnership_runs", 0),
                        "partnership_balls": current_score.get("partnership_balls", 0),
                        "bowler": current_score.get("bowler", ""),
                        "bowler_figures": current_score.get("bowler_figures", "0/0"),
                    },
                }),
            }

            # Send over complete event for chart
            wicket_in_over = current_wickets > (state.total_wickets - current_wickets) if over_int == last_over + 1 else False
            yield {
                "event": "over_complete",
                "data": json.dumps({
                    "over": over_int,
                    "runs": over_runs,
                    "total_runs": current_runs,
                    "total_wickets": current_wickets,
                    "run_rate": state.current_run_rate,
                    "wicket_in_over": wicket_in_over,
                }),
            }

            # Generate AI insight ONCE per over
            yield {
                "event": "insight_start",
                "data": json.dumps({"over": over_int, "ball": 6}),
            }

            context = state.get_context_for_prompt()
            full_insight = ""
            async for chunk in generate_tactical_insight(context):
                full_insight += chunk
                yield {
                    "event": "insight_chunk",
                    "data": json.dumps({"text": chunk}),
                }

            await save_insight(session_id, over_int, 6, full_insight, "tactical")

            yield {
                "event": "insight_complete",
                "data": json.dumps({
                    "over": over_int,
                    "ball": 6,
                    "full_text": full_insight,
                }),
            }

            last_over = over_int
            last_total_runs = current_runs

        # Check if match is over
        match_status = _get_match_status(scorecard)
        if match_status in ("complete", "abandoned") or over_int >= max_overs:
            yield {
                "event": "match_end",
                "data": json.dumps({
                    "final_score": f"{current_runs}/{current_wickets}",
                    "overs": str(current_over),
                    "session_id": session_id,
                    "api_calls_used": api_calls,
                }),
            }
            break

        # Wait before next poll (over-by-over = ~2-3 min between overs in T20)
        await asyncio.sleep(poll_interval)

        # Poll scorecard — 1 API call per over
        scorecard = await get_match_scorecard(match_id)
        api_calls += 1

        # Send heartbeat to keep SSE alive
        yield {
            "event": "heartbeat",
            "data": json.dumps({"api_calls_used": api_calls, "waiting_for_over": last_over + 1}),
        }


async def _historical_replay_generator(match_id: str, mode: str = "demo"):
    """
    DEMO/HISTORICAL MODE: Replays ball-by-ball data with AI insights.
    If mode='demo' or API disabled, uses mock data. 
    Otherwise uses real historical data from API.
    """
    match = await get_match_info(match_id)
    match_name = match.get("name", f"Match {match_id}") if match else f"Match {match_id}"
    session = await create_session(match_id, match_name)
    session_id = session.get("id", "local") if session else "local"

    yield {
        "event": "session_start",
        "data": json.dumps({
            "session_id": session_id,
            "match_name": match_name,
            "mode": mode,
        }),
    }

    balls = await get_ball_by_ball(match_id, match)
    state = MatchState(match_id=match_id)

    if match:
        state.match_format = match.get("matchType", "T20")
        scores = match.get("score", [])
        if len(scores) >= 2:
            state.target = scores[0].get("r", 0) + 1

    over_runs_accumulator = 0

    for i, ball in enumerate(balls):
        state.update(ball)

        # Send ball update
        yield {
            "event": "ball",
            "data": json.dumps({
                "ball": ball,
                "state": {
                    "total_runs": state.total_runs,
                    "total_wickets": state.total_wickets,
                    "current_over": state.current_over,
                    "current_ball": state.current_ball,
                    "current_rr": state.current_run_rate,
                    "required_rr": state.required_run_rate,
                    "striker": state.striker,
                    "striker_runs": state.striker_runs,
                    "striker_balls": state.striker_balls,
                    "partnership_runs": state.partnership.runs,
                    "partnership_balls": state.partnership.balls,
                    "bowler": state.current_bowler.name,
                    "bowler_figures": f"{state.current_bowler.wickets}/{state.current_bowler.runs}",
                },
            }),
        }

        over_runs_accumulator += ball.get("runs", 0)

        # Send over summary for chart
        if ball.get("ball") == 6:
            yield {
                "event": "over_complete",
                "data": json.dumps({
                    "over": state.current_over,
                    "runs": over_runs_accumulator,
                    "total_runs": state.total_runs,
                    "total_wickets": state.total_wickets,
                    "run_rate": state.current_run_rate,
                    "wicket_in_over": any(
                        b.get("is_wicket") for b in balls[max(0, i - 5):i + 1]
                    ),
                }),
            }
            over_runs_accumulator = 0

            # Generate AI insight at end of each over
            yield {
                "event": "insight_start",
                "data": json.dumps({"over": state.current_over, "ball": state.current_ball}),
            }

            context = state.get_context_for_prompt()
            full_insight = ""
            async for chunk in generate_tactical_insight(context):
                full_insight += chunk
                yield {
                    "event": "insight_chunk",
                    "data": json.dumps({"text": chunk}),
                }

            await save_insight(
                session_id, state.current_over, state.current_ball,
                full_insight, "tactical"
            )

            yield {
                "event": "insight_complete",
                "data": json.dumps({
                    "over": state.current_over,
                    "ball": state.current_ball,
                    "full_text": full_insight,
                }),
            }

        # Simulate ball-by-ball timing
        await asyncio.sleep(0.3)

    # Match end
    yield {
        "event": "match_end",
        "data": json.dumps({
            "final_score": f"{state.total_runs}/{state.total_wickets}",
            "overs": f"{state.current_over}.{state.current_ball}",
            "session_id": session_id,
        }),
    }


def _extract_score_from_api(scorecard: dict) -> dict:
    """Extract current score info from API scorecard response."""
    if not scorecard:
        return {"overs": 0, "runs": 0, "wickets": 0}

    scores = scorecard.get("score", [])
    if not scores:
        return {"overs": 0, "runs": 0, "wickets": 0}

    # Get the latest innings score
    latest = scores[-1] if scores else {}
    batting = scorecard.get("batting", [])
    bowling = scorecard.get("bowling", [])

    # Find current batsmen
    striker = ""
    striker_runs = 0
    striker_balls = 0
    for b in batting:
        if b.get("batting", False):
            striker = b.get("name", "")
            striker_runs = b.get("r", 0)
            striker_balls = b.get("b", 0)
            break

    bowler = ""
    bowler_figures = "0/0"
    if bowling:
        last_bowler = bowling[-1]
        bowler = last_bowler.get("name", "")
        bowler_figures = f"{last_bowler.get('w', 0)}/{last_bowler.get('r', 0)}"

    return {
        "overs": latest.get("o", 0),
        "runs": latest.get("r", 0),
        "wickets": latest.get("w", 0),
        "batting_team": latest.get("team", ""),
        "bowling_team": "",
        "striker": striker,
        "striker_runs": striker_runs,
        "striker_balls": striker_balls,
        "partnership_runs": 0,
        "partnership_balls": 0,
        "bowler": bowler,
        "bowler_figures": bowler_figures,
    }


def _get_match_status(scorecard: dict) -> str:
    """Get match status from scorecard data."""
    if not scorecard:
        return "unknown"
    status = scorecard.get("status", "").lower()
    if "won" in status or "tied" in status or "draw" in status:
        return "complete"
    if "abandon" in status:
        return "abandoned"
    return "live"


@router.get("/sessions")
async def list_sessions():
    """List saved analysis sessions."""
    sessions = await get_sessions()
    return {"sessions": sessions}


@router.get("/sessions/{session_id}")
async def session_detail(session_id: str):
    """Get session replay data."""
    history = await get_session_history(session_id)
    if not history:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session": history}
