const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Match {
  id: string;
  name: string;
  status: string;
  venue: string;
  date: string;
  matchType: string;
  teams: string[];
  score: {
    team: string;
    inning: string;
    r: number;
    w: number;
    o: number;
  }[];
  tpiTeam1?: { name: string; shortname: string; img: string };
  tpiTeam2?: { name: string; shortname: string; img: string };
  batting?: {
    name: string;
    r: number;
    b: number;
    "4s": number;
    "6s": number;
    sr: number;
    batting: boolean;
  }[];
  bowling?: {
    name: string;
    o: number;
    m: number;
    r: number;
    w: number;
    eco: number;
  }[];
}

export interface MatchState {
  total_runs: number;
  total_wickets: number;
  current_over: number;
  current_ball: number;
  current_rr: number;
  required_rr: number | null;
  striker: string;
  striker_runs: number;
  striker_balls: number;
  partnership_runs: number;
  partnership_balls: number;
  bowler: string;
  bowler_figures: string;
}

export interface BallData {
  id: string;
  over: number;
  ball: number;
  over_ball: string;
  batsman: string;
  bowler: string;
  runs: number;
  is_wicket: boolean;
  is_boundary: boolean;
  is_extra: boolean;
  shot_type: string;
  dismissal_type: string | null;
  batting_team: string;
  bowling_team: string;
}

export interface OverData {
  over: number;
  runs: number;
  total_runs: number;
  total_wickets: number;
  run_rate: number;
  wicket_in_over: boolean;
}

export async function fetchMatches(): Promise<Match[]> {
  try {
    const res = await fetch(`${API_BASE}/api/matches`);
    const data = await res.json();
    return data.matches || [];
  } catch {
    return [];
  }
}

export async function fetchMatchDetail(matchId: string): Promise<Match | null> {
  try {
    const res = await fetch(`${API_BASE}/api/match/${matchId}`);
    const data = await res.json();
    return data.match || null;
  } catch {
    return null;
  }
}

export function getStreamUrl(matchId: string): string {
  return `${API_BASE}/api/match/${matchId}/stream`;
}
