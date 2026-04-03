import random
import uuid
from datetime import datetime, timedelta


MOCK_MATCHES = [
    {
        "id": "mock_ipl_1",
        "name": "Mumbai Indians vs Chennai Super Kings",
        "status": "Live - 2nd Innings",
        "venue": "Wankhede Stadium, Mumbai",
        "date": datetime.now().isoformat(),
        "matchType": "T20",
        "teams": ["Mumbai Indians", "Chennai Super Kings"],
        "score": [
            {"team": "Chennai Super Kings", "inning": "CSK Inning 1", "r": 187, "w": 5, "o": 20.0},
            {"team": "Mumbai Indians", "inning": "MI Inning 2", "r": 0, "w": 0, "o": 0.0},
        ],
        "tpiTeam1": {"name": "Mumbai Indians", "shortname": "MI", "img": ""},
        "tpiTeam2": {"name": "Chennai Super Kings", "shortname": "CSK", "img": ""},
    },
    {
        "id": "mock_intl_1",
        "name": "India vs Australia - 3rd T20I",
        "status": "Live - 1st Innings",
        "venue": "Rajiv Gandhi Intl. Stadium, Hyderabad",
        "date": datetime.now().isoformat(),
        "matchType": "T20",
        "teams": ["India", "Australia"],
        "score": [
            {"team": "India", "inning": "IND Inning 1", "r": 0, "w": 0, "o": 0.0},
        ],
        "tpiTeam1": {"name": "India", "shortname": "IND", "img": ""},
        "tpiTeam2": {"name": "Australia", "shortname": "AUS", "img": ""},
    },
    {
        "id": "mock_odi_1",
        "name": "England vs South Africa - 2nd ODI",
        "status": "Complete",
        "venue": "Lord's, London",
        "date": (datetime.now() - timedelta(days=2)).isoformat(),
        "matchType": "ODI",
        "teams": ["England", "South Africa"],
        "score": [
            {"team": "England", "inning": "ENG Inning 1", "r": 312, "w": 7, "o": 50.0},
            {"team": "South Africa", "inning": "SA Inning 2", "r": 298, "w": 10, "o": 48.3},
        ],
        "tpiTeam1": {"name": "England", "shortname": "ENG", "img": ""},
        "tpiTeam2": {"name": "South Africa", "shortname": "SA", "img": ""},
    },
    {
        "id": "mock_test_1",
        "name": "Pakistan vs New Zealand - 1st Test",
        "status": "Day 2 - Stumps",
        "venue": "National Stadium, Karachi",
        "date": (datetime.now() - timedelta(days=1)).isoformat(),
        "matchType": "Test",
        "teams": ["Pakistan", "New Zealand"],
        "score": [
            {"team": "Pakistan", "inning": "PAK Inning 1", "r": 345, "w": 10, "o": 98.2},
            {"team": "New Zealand", "inning": "NZ Inning 1", "r": 112, "w": 3, "o": 38.0},
        ],
        "tpiTeam1": {"name": "Pakistan", "shortname": "PAK", "img": ""},
        "tpiTeam2": {"name": "New Zealand", "shortname": "NZ", "img": ""},
    },
]


BATSMEN = {
    "mock_ipl_1": [
        {"name": "Rohit Sharma", "r": 0, "b": 0, "4s": 0, "6s": 0, "sr": 0.0, "batting": True},
        {"name": "Ishan Kishan", "r": 0, "b": 0, "4s": 0, "6s": 0, "sr": 0.0, "batting": True},
        {"name": "Suryakumar Yadav", "r": 0, "b": 0, "4s": 0, "6s": 0, "sr": 0.0, "batting": False},
        {"name": "Tilak Varma", "r": 0, "b": 0, "4s": 0, "6s": 0, "sr": 0.0, "batting": False},
        {"name": "Hardik Pandya", "r": 0, "b": 0, "4s": 0, "6s": 0, "sr": 0.0, "batting": False},
    ],
    "mock_intl_1": [
        {"name": "Yashasvi Jaiswal", "r": 0, "b": 0, "4s": 0, "6s": 0, "sr": 0.0, "batting": True},
        {"name": "Shubman Gill", "r": 0, "b": 0, "4s": 0, "6s": 0, "sr": 0.0, "batting": True},
        {"name": "Virat Kohli", "r": 0, "b": 0, "4s": 0, "6s": 0, "sr": 0.0, "batting": False},
        {"name": "Suryakumar Yadav", "r": 0, "b": 0, "4s": 0, "6s": 0, "sr": 0.0, "batting": False},
        {"name": "Hardik Pandya", "r": 0, "b": 0, "4s": 0, "6s": 0, "sr": 0.0, "batting": False},
    ],
}

BOWLERS = {
    "mock_ipl_1": [
        {"name": "Deepak Chahar", "o": 0, "m": 0, "r": 0, "w": 0, "eco": 0.0},
        {"name": "Matheesha Pathirana", "o": 0, "m": 0, "r": 0, "w": 0, "eco": 0.0},
        {"name": "Ravindra Jadeja", "o": 0, "m": 0, "r": 0, "w": 0, "eco": 0.0},
        {"name": "Moeen Ali", "o": 0, "m": 0, "r": 0, "w": 0, "eco": 0.0},
    ],
    "mock_intl_1": [
        {"name": "Mitchell Starc", "o": 0, "m": 0, "r": 0, "w": 0, "eco": 0.0},
        {"name": "Pat Cummins", "o": 0, "m": 0, "r": 0, "w": 0, "eco": 0.0},
        {"name": "Josh Hazlewood", "o": 0, "m": 0, "r": 0, "w": 0, "eco": 0.0},
        {"name": "Adam Zampa", "o": 0, "m": 0, "r": 0, "w": 0, "eco": 0.0},
    ],
}

SHOT_TYPES = [
    "straight drive", "cover drive", "pull shot", "cut shot", "flick",
    "sweep", "reverse sweep", "lofted drive", "edge", "defended",
    "leave", "paddle", "upper cut", "hook shot", "inside edge",
]

DISMISSAL_TYPES = ["bowled", "caught", "lbw", "run out", "stumped", "caught behind"]

FIELD_POSITIONS = [
    "mid-off", "mid-on", "cover", "point", "square leg", "fine leg",
    "third man", "long-on", "long-off", "deep midwicket", "slip",
    "gully", "short leg", "silly point", "deep square leg",
]


def generate_ball_by_ball_data(match_id: str, real_match_info: dict = None, total_overs: int = 20):
    """Generate realistic ball-by-ball mock data for a T20 match."""
    balls = []
    
    match_info = real_match_info or next((m for m in MOCK_MATCHES if m["id"] == match_id), MOCK_MATCHES[0])
    teams = match_info.get("teams", [])
    batting_team = teams[0] if len(teams) > 0 else "Team A"
    bowling_team = teams[1] if len(teams) > 1 else "Team B"

    # Use predefined mock pools if it's our hardcoded mock ID, else generate realistic placeholders
    if match_id in BATSMEN:
        batsmen_pool = BATSMEN[match_id]
        bowlers_pool = BOWLERS[match_id]
    else:
        bat_abbr = batting_team.split()[0] if batting_team else "BAT"
        bowl_abbr = bowling_team.split()[0] if bowling_team else "BOWL"
        batsmen_pool = [{"name": f"{bat_abbr} Batter {i}", "r": 0, "b": 0, "4s": 0, "6s": 0, "sr": 0.0, "batting": True} for i in range(1, 12)]
        bowlers_pool = [{"name": f"{bowl_abbr} Bowler {i}", "o": 0, "m": 0, "r": 0, "w": 0, "eco": 0.0} for i in range(1, 6)]

    current_batsman_idx = 0
    non_striker_idx = 1
    total_runs = 0
    total_wickets = 0
    partnership_runs = 0
    partnership_balls = 0

    for over in range(total_overs):
        bowler = bowlers_pool[over % len(bowlers_pool)]
        for ball_num in range(1, 7):
            if total_wickets >= 10:
                break

            # Weighted run distribution (realistic T20)
            run_weights = [30, 25, 10, 5, 15, 2, 8, 5]  # 0,1,2,3,4,5(W),6,extra
            run_choice = random.choices(range(8), weights=run_weights, k=1)[0]

            is_wicket = run_choice == 5
            is_extra = run_choice == 7
            runs = 0 if is_wicket else (random.choice([1, 2]) if is_extra else min(run_choice, 6))
            if run_choice == 6:
                runs = 6
            elif run_choice == 4:
                runs = 4

            ball_data = {
                "id": str(uuid.uuid4()),
                "over": over,
                "ball": ball_num,
                "over_ball": f"{over}.{ball_num}",
                "batsman": batsmen_pool[current_batsman_idx]["name"],
                "bowler": bowler["name"],
                "runs": runs,
                "is_wicket": is_wicket,
                "is_boundary": runs in [4, 6],
                "is_extra": is_extra,
                "extra_type": random.choice(["wide", "no-ball"]) if is_extra else None,
                "shot_type": random.choice(SHOT_TYPES),
                "dismissal_type": random.choice(DISMISSAL_TYPES) if is_wicket else None,
                "field_position": random.choice(FIELD_POSITIONS),
                "batting_team": batting_team,
                "bowling_team": bowling_team,
                "total_runs": total_runs + runs,
                "total_wickets": total_wickets + (1 if is_wicket else 0),
                "current_rr": round((total_runs + runs) / max((over * 6 + ball_num) / 6, 0.1), 2),
                "partnership": {
                    "runs": partnership_runs + (0 if is_wicket else runs),
                    "balls": partnership_balls + 1,
                },
            }

            total_runs += runs
            if is_wicket:
                total_wickets += 1
                partnership_runs = 0
                partnership_balls = 0
                current_batsman_idx = min(current_batsman_idx + 1, len(batsmen_pool) - 1)
                non_striker_idx = min(non_striker_idx + 1, len(batsmen_pool) - 1)
            else:
                partnership_runs += runs
                partnership_balls += 1
                if runs in [1, 3]:
                    current_batsman_idx, non_striker_idx = non_striker_idx, current_batsman_idx

            balls.append(ball_data)

        if total_wickets >= 10:
            break

    return balls


def get_mock_matches():
    """Return list of mock matches."""
    return MOCK_MATCHES


def get_mock_match_detail(match_id: str):
    """Return detailed mock data for a specific match."""
    match = next((m for m in MOCK_MATCHES if m["id"] == match_id), None)
    if not match:
        return None

    batsmen = BATSMEN.get(match_id, BATSMEN["mock_ipl_1"])
    bowlers = BOWLERS.get(match_id, BOWLERS["mock_ipl_1"])

    return {
        **match,
        "batting": batsmen,
        "bowling": bowlers,
    }
