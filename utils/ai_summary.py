import os
from openai import OpenAI

def summarize_disaster(disaster: str, location: str, sample_rows: str) -> str:
    """
    Generates a real-data summary and preparedness guide.
    Falls back to offline tips if the OpenAI API key isn't available or hits quota.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            f"🧭 **Offline Insight**\n\n"
            f"Historical {disaster.lower()} data for {location} suggests patterns worth preparing for.\n\n"
            f"**Quick Tips:**\n"
            f"- Keep emergency kits updated.\n"
            f"- Protect important documents in waterproof/fireproof containers.\n"
            f"- Review evacuation plans and local shelters.\n\n"
            f"(Add your OpenAI API key in `.env` to unlock personalized AI analysis.)"
        )

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""
You are a disaster-readiness analyst.
Using this real {disaster} data for {location}, summarize patterns and preparedness recommendations.

Dataset sample:
{sample_rows}

1. Write a concise **Trend Summary** (what has changed over time).
2. Write a **5-Year Outlook** prediction (based on trajectory).
3. List **3 Family-Level Preparedness Actions** (numbered 1-3).

Use markdown, factual tone, and clear formatting (max 200 words).
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            f"⚠️ **Insight unavailable due to connection or key issue.**\n\n"
            f"Based on trends, prioritize early warnings, stronger infrastructure, "
            f"and improved family communication plans.\n\n"
            f"_Error details: {e}_"
        )
