from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BowlerSpell:
    name: str = ""
    overs: float = 0.0
    maidens: int = 0
    runs: int = 0
    wickets: int = 0
    dots: int = 0
    boundaries_conceded: int = 0

    @property
    def economy(self) -> float:
        if self.overs == 0:
            return 0.0
        return round(self.runs / self.overs, 2)


@dataclass
class Partnership:
    batsman1: str = ""
    batsman2: str = ""
    runs: int = 0
    balls: int = 0

    @property
    def run_rate(self) -> float:
        if self.balls == 0:
            return 0.0
        return round((self.runs / self.balls) * 6, 2)


@dataclass
class MatchState:
    """Maintains rolling match state for context-aware AI analysis."""

    match_id: str = ""
    batting_team: str = ""
    bowling_team: str = ""
    match_format: str = "T20"

    # Score tracking
    total_runs: int = 0
    total_wickets: int = 0
    current_over: int = 0
    current_ball: int = 0
    target: Optional[int] = None

    # Rate tracking
    current_run_rate: float = 0.0
    required_run_rate: Optional[float] = None

    # Current batsmen
    striker: str = ""
    striker_runs: int = 0
    striker_balls: int = 0
    non_striker: str = ""
    non_striker_runs: int = 0
    non_striker_balls: int = 0

    # Partnership
    partnership: Partnership = field(default_factory=Partnership)

    # Bowler spell
    current_bowler: BowlerSpell = field(default_factory=BowlerSpell)
    bowler_spells: dict = field(default_factory=dict)

    # Recent history
    last_12_balls: list = field(default_factory=list)
    over_by_over_runs: list = field(default_factory=list)
    boundaries_in_last_3_overs: int = 0
    dots_in_last_3_overs: int = 0

    # Wickets
    recent_wickets: list = field(default_factory=list)

    # Ball counter for AI trigger
    balls_since_last_insight: int = 0

    def update(self, ball_data: dict):
        """Process a new ball delivery and update state."""
        self.current_over = ball_data.get("over", self.current_over)
        self.current_ball = ball_data.get("ball", self.current_ball)
        runs = ball_data.get("runs", 0)
        is_wicket = ball_data.get("is_wicket", False)
        is_boundary = ball_data.get("is_boundary", False)

        self.total_runs += runs
        self.batting_team = ball_data.get("batting_team", self.batting_team)
        self.bowling_team = ball_data.get("bowling_team", self.bowling_team)

        # Update striker
        self.striker = ball_data.get("batsman", self.striker)
        self.striker_runs += runs
        self.striker_balls += 1

        # Bowler tracking
        bowler_name = ball_data.get("bowler", "")
        if bowler_name:
            if bowler_name not in self.bowler_spells:
                self.bowler_spells[bowler_name] = BowlerSpell(name=bowler_name)
            spell = self.bowler_spells[bowler_name]
            spell.runs += runs
            if runs == 0 and not is_wicket:
                spell.dots += 1
            if is_boundary:
                spell.boundaries_conceded += 1
            if is_wicket:
                spell.wickets += 1
            spell.overs = round((self.current_over * 6 + self.current_ball) / 6, 1)
            self.current_bowler = spell

        # Recent ball history
        ball_summary = {
            "over_ball": ball_data.get("over_ball", ""),
            "runs": runs,
            "is_wicket": is_wicket,
            "is_boundary": is_boundary,
            "batsman": self.striker,
            "bowler": bowler_name,
            "shot_type": ball_data.get("shot_type", ""),
        }
        self.last_12_balls.append(ball_summary)
        if len(self.last_12_balls) > 12:
            self.last_12_balls = self.last_12_balls[-12:]

        # Run rate
        overs_bowled = self.current_over + (self.current_ball / 6)
        self.current_run_rate = round(self.total_runs / max(overs_bowled, 0.1), 2)
        if self.target and self.match_format == "T20":
            remaining_overs = max(20 - overs_bowled, 0.1)
            remaining_runs = self.target - self.total_runs
            self.required_run_rate = round(remaining_runs / remaining_overs, 2) if remaining_runs > 0 else 0.0

        # Partnership
        if is_wicket:
            self.total_wickets += 1
            self.recent_wickets.append({
                "batsman": self.striker,
                "bowler": bowler_name,
                "dismissal": ball_data.get("dismissal_type", ""),
                "runs": self.striker_runs,
                "balls": self.striker_balls,
            })
            self.partnership = Partnership()
            self.striker_runs = 0
            self.striker_balls = 0
        else:
            self.partnership.runs += runs
            self.partnership.balls += 1

        # Over-by-over tracking
        if self.current_ball == 6 or is_wicket:
            current_over_total = sum(
                b["runs"] for b in self.last_12_balls
                if b["over_ball"].startswith(f"{self.current_over}.")
            )
            if self.current_ball == 6:
                if len(self.over_by_over_runs) <= self.current_over:
                    self.over_by_over_runs.append(current_over_total)

        self.balls_since_last_insight += 1

    def should_generate_insight(self) -> bool:
        """Check if we should generate a new AI insight (every 2-3 balls)."""
        return self.balls_since_last_insight >= 3

    def reset_insight_counter(self):
        self.balls_since_last_insight = 0

    def get_context_for_prompt(self) -> str:
        """Build structured match context for AI prompt."""
        recent_balls_str = " | ".join(
            f"{b['over_ball']}: {b['runs']}r {'(W)' if b['is_wicket'] else ''}"
            f"{'(4)' if b['is_boundary'] and b['runs']==4 else ''}"
            f"{'(6)' if b['is_boundary'] and b['runs']==6 else ''}"
            f" [{b['shot_type']}]"
            for b in self.last_12_balls[-6:]
        )

        bowler_stats = ""
        if self.current_bowler.name:
            b = self.current_bowler
            bowler_stats = f"{b.name}: {b.overs}ov, {b.runs}/{b.wickets}, Econ: {b.economy}, Dots: {b.dots}"

        wickets_str = ""
        if self.recent_wickets:
            wickets_str = " | ".join(
                f"{w['batsman']} {w['dismissal']} b {w['bowler']} ({w['runs']}({w['balls']}))"
                for w in self.recent_wickets[-3:]
            )

        context = f"""
MATCH STATE — {self.batting_team} vs {self.bowling_team} ({self.match_format})
Score: {self.total_runs}/{self.total_wickets} in {self.current_over}.{self.current_ball} overs
Current Run Rate: {self.current_run_rate}
{f'Required Run Rate: {self.required_run_rate}' if self.required_run_rate else ''}
Partnership: {self.partnership.runs} runs off {self.partnership.balls} balls (RR: {self.partnership.run_rate})
Current Striker: {self.striker} — {self.striker_runs}({self.striker_balls})
Current Bowler: {bowler_stats}
Last 6 Deliveries: {recent_balls_str}
{f'Recent Wickets: {wickets_str}' if wickets_str else ''}
Over-by-over: {', '.join(str(r) for r in self.over_by_over_runs[-5:])}
""".strip()

        return context
