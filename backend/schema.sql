-- Supabase Schema for Cricket Tactical Analyzer
-- Run this SQL in your Supabase SQL Editor

-- Analysis Sessions table
CREATE TABLE IF NOT EXISTS analysis_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    match_id TEXT NOT NULL,
    match_name TEXT NOT NULL,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tactical Insights table
CREATE TABLE IF NOT EXISTS tactical_insights (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id UUID REFERENCES analysis_sessions(id) ON DELETE CASCADE,
    over_number INTEGER NOT NULL,
    ball_number INTEGER NOT NULL,
    insight_text TEXT NOT NULL,
    insight_type TEXT DEFAULT 'tactical' CHECK (insight_type IN ('tactical', 'bowling', 'batting', 'field', 'momentum')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_sessions_match_id ON analysis_sessions(match_id);
CREATE INDEX IF NOT EXISTS idx_insights_session_id ON tactical_insights(session_id);
CREATE INDEX IF NOT EXISTS idx_insights_created_at ON tactical_insights(created_at);

-- Enable Row Level Security (optional for Supabase)
ALTER TABLE analysis_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE tactical_insights ENABLE ROW LEVEL SECURITY;

-- Allow public read/write (adjust for production)
CREATE POLICY "Allow all access to analysis_sessions"
    ON analysis_sessions FOR ALL
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow all access to tactical_insights"
    ON tactical_insights FOR ALL
    USING (true)
    WITH CHECK (true);
