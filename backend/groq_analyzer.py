import asyncio
import random
from typing import AsyncGenerator
from config import settings

MOCK_INSIGHTS = [
    "🎯 **Bowling Pattern Alert**: The bowler is consistently targeting the off-stump corridor with back-of-a-length deliveries. The batsman has scored just 3 runs from the last 8 balls in this zone. Expect a change — either a yorker or a bouncer is due next.",
    "📊 **Scoring Pressure**: The run rate has dipped below 7 in the last 3 overs after being above 9 in the powerplay. The batting side needs to find boundaries soon — the dot ball percentage has climbed to 45% in this phase.",
    "🏏 **Partnership Building**: This pair has added 34 runs in 28 balls with excellent running between wickets. Their rotation of strike (8 singles) is keeping the scoreboard ticking while waiting for loose deliveries.",
    "🔄 **Tactical Shift**: The captain has brought on the spinner from the pavilion end — a clear tactical move. The left-hander has a strike rate of just 95 against spin in this tournament. Watch for a mid-wicket trap.",
    "⚡ **Momentum Swing**: Three boundaries in the last over have shifted the momentum dramatically. The bowling team needs to regroup — bringing in the death-over specialist here could stem the flow.",
    "🎯 **Field Placement Insight**: With the batsman favoring the leg side (73% of runs), the captain should consider moving a fielder from cover to deep midwicket. The pull shot has fetched 18 runs in the last 4 overs.",
    "📈 **Required Rate Analysis**: At {rr}/over needed, the equation is still in the batting side's favor. But the next 3 overs (15-17) have historically been the toughest phase in T20s at this ground — average scoring rate drops to 6.8.",
    "🏆 **Key Wicket Alert**: This batsman has scored 60% of the team's runs in this innings. Getting this wicket now could trigger a collapse — the middle order has a combined average of just 18 in this series.",
    "🌡️ **Pressure Index**: The bowling team has bowled 4 dot balls in the last over, building enormous pressure. The batsman's false-shot percentage has jumped to 35% — a wicket feels imminent.",
    "⚔️ **Battle Within The Battle**: The pace bowler vs right-hander matchup has been fascinating — 14 deliveries, 12 runs, 2 edges, and 1 dropped catch. The bowler is winning this duel slightly with an economy of 5.1.",
]


async def generate_tactical_insight(match_context: str) -> AsyncGenerator[str, None]:
    """
    Generate tactical insight using Groq API (LLaMA 3.3 70B).
    Falls back to mock insights if API key is not configured.
    """
    if not settings.GROQ_API_KEY or settings.USE_MOCK_DATA:
        # Mock streaming: pick a random insight and stream word by word
        insight = random.choice(MOCK_INSIGHTS)
        words = insight.split(" ")
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
            await asyncio.sleep(0.04)
        return

    try:
        from groq import Groq

        client = Groq(api_key=settings.GROQ_API_KEY)

        system_prompt = """You are an elite cricket tactical analyst with deep knowledge of T20, ODI, and Test cricket. 
You analyze ball-by-ball match data and provide sharp, actionable tactical insights.

Your analysis should cover:
1. **Bowling Patterns**: Identify the bowler's strategy — line, length, variations, and predictability
2. **Batting Pressure Points**: Spot when batsmen are under pressure, playing false shots, or finding rhythm
3. **Field Placement Suggestions**: Recommend field changes based on the batsman's scoring zones
4. **Momentum Shifts**: Identify when the momentum is swinging and what caused it
5. **Partnership Dynamics**: Analyze how the batting pair is working together
6. **Tactical Predictions**: What should the captain do next?

Rules:
- Be specific and data-driven, reference actual numbers from the match context
- Keep insights to 2-3 concise paragraphs
- Use cricket terminology naturally
- Start with an emoji category indicator
- Be bold with predictions — coaches love decisive analysis
- Focus on the CURRENT situation, not generic advice"""

        user_prompt = f"""Analyze this current match situation and provide a tactical insight:

{match_context}

Provide a sharp, specific tactical insight about what's happening RIGHT NOW in this match. Focus on the most interesting tactical storyline emerging from the data."""

        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=300,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        # Fallback to mock on any API error
        insight = f"⚠️ AI Analysis unavailable ({str(e)[:50]}). "
        insight += random.choice(MOCK_INSIGHTS)
        words = insight.split(" ")
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
            await asyncio.sleep(0.04)
