# 🏏 CricketAI — Real-Time Tactical Match Analyzer

AI-powered real-time cricket match analysis with tactical insights, live scoring, and match momentum visualization.

![CricketAI](https://img.shields.io/badge/CricketAI-Tactical%20Analyzer-06d6a0?style=for-the-badge)
![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange?style=flat-square)

## Features

- ⚡ **Over-by-over live polling** — 1 API call per over (40 calls for 2 T20 matches/day, free tier friendly)
- 🧠 **AI Tactical Insights** — LLaMA 3.3 70B via Groq analyzes bowling patterns, batting pressure, field placement
- 📊 **Match Momentum Charts** — Recharts-powered run rate visualization with wicket markers
- 🔴 **SSE Streaming** — Real-time insights stream to the browser, no page refresh
- 💾 **Session History** — Supabase stores full match analysis for replay

## Architecture

```
React (Next.js) Frontend  ←— SSE Stream —→  FastAPI Backend
   Three-Panel UI                          CricketData.org API
   (Score | Insights | Chart)              Groq AI (LLaMA 3.3 70B)
                                           Supabase (PostgreSQL)
```

## Quick Start

### Backend
```bash
cd backend
cp .env.example .env        # Add your API keys
pip install -r requirements.txt
uvicorn main:app --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev                  # Opens at http://localhost:3000
```

### Required API Keys (all free tier)
| Service | Get Key | Free Limit |
|---------|---------|------------|
| [CricketData.org](https://cricketdata.org) | Dashboard → API Key | 100 calls/day |
| [Groq](https://console.groq.com) | API Keys → Create | 14,400 calls/day |
| [Supabase](https://supabase.com) | Project Settings → API | 500MB + unlimited API |

## Deployment

- **Frontend**: Vercel
- **Backend**: HuggingFace Spaces (Docker)

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 16, React, Recharts, TypeScript |
| Backend | FastAPI, Python, SSE-Starlette |
| AI | Groq API, LLaMA 3.3 70B Versatile |
| Database | Supabase (PostgreSQL) |
| Cricket Data | CricketData.org API |

## License
MIT
