"""
Story Router — AI-powered narrative generation for data visualizations
Uses OpenAI/Anthropic to analyze data and generate compelling stories
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import json
from typing import Optional

router = APIRouter()


class StoryRequest(BaseModel):
    data_id: str
    title: str
    chart_type: str
    duration: int  # seconds
    language: Optional[str] = "en"
    tone: Optional[str] = "engaging"  # engaging, professional, dramatic


class StoryResponse(BaseModel):
    script: str
    word_count: int
    estimated_duration: float  # seconds
    key_insights: list[str]


def build_story_prompt(data_summary: dict, title: str, chart_type: str, duration: int, tone: str) -> str:
    """Build a prompt for AI story generation"""
    chart_descriptions = {
        "bar_race": "animated bar chart race showing rankings over time",
        "pie_race": "animated pie chart showing proportional changes over time",
        "line_chart": "animated line chart showing trends over time",
        "area_chart": "animated stacked area chart showing cumulative changes",
        "world_map": "animated world map showing geographic distribution over time",
    }

    chart_desc = chart_descriptions.get(chart_type, "animated data visualization")
    words_per_second = 2.5  # average speaking pace
    target_words = int(duration * words_per_second)

    prompt = f"""You are a data storyteller creating a voiceover script for a viral social media video.

VIDEO TITLE: {title}
CHART TYPE: {chart_desc}
TARGET DURATION: {duration} seconds (~{target_words} words)
TONE: {tone}

DATA SUMMARY:
- Categories: {', '.join(data_summary.get('columns', [])[:10])}
- Time range: {data_summary.get('date_start', 'unknown')} to {data_summary.get('date_end', 'unknown')}
- Number of data points: {data_summary.get('rows', 0)}

Write a compelling voiceover script that:
1. Opens with a hook that grabs attention in the first 3 seconds
2. Narrates the key trends and changes shown in the data
3. Highlights surprising or dramatic moments
4. Ends with a memorable conclusion or call-to-action
5. Is exactly {target_words} words (±10%)
6. Uses simple, conversational language suitable for social media
7. Does NOT include stage directions, timestamps, or formatting — just the spoken words

Write ONLY the script text, nothing else."""

    return prompt


@router.post("/generate", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    """
    Generate an AI-powered story script for the data visualization
    """
    # Import data store from upload router
    from routers.upload import data_store

    if request.data_id not in data_store:
        raise HTTPException(status_code=404, detail="Data not found. Please upload a file first.")

    stored = data_store[request.data_id]

    data_summary = {
        "columns": stored["columns"],
        "rows": stored["rows"],
        "date_start": stored["date_start"],
        "date_end": stored["date_end"],
    }

    prompt = build_story_prompt(
        data_summary=data_summary,
        title=request.title,
        chart_type=request.chart_type,
        duration=request.duration,
        tone=request.tone or "engaging",
    )

    script = ""

    # Try OpenAI first
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if openai_key:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=openai_key)
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert data storyteller for social media."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.7,
            )
            script = response.choices[0].message.content or ""
        except Exception as e:
            print(f"OpenAI failed: {e}")

    elif anthropic_key:
        try:
            import anthropic
            client = anthropic.AsyncAnthropic(api_key=anthropic_key)
            message = await client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )
            script = message.content[0].text
        except Exception as e:
            print(f"Anthropic failed: {e}")

    # Fallback: generate a template script
    if not script:
        script = generate_template_script(
            title=request.title,
            columns=stored["columns"],
            date_start=stored["date_start"],
            date_end=stored["date_end"],
            duration=request.duration,
        )

    # Extract key insights (simple heuristic)
    sentences = [s.strip() for s in script.split(".") if len(s.strip()) > 20]
    key_insights = sentences[:3]

    word_count = len(script.split())
    estimated_duration = word_count / 2.5  # words per second

    return StoryResponse(
        script=script,
        word_count=word_count,
        estimated_duration=estimated_duration,
        key_insights=key_insights,
    )


def generate_template_script(title: str, columns: list, date_start: str, date_end: str, duration: int) -> str:
    """Fallback template script when no AI API is available"""
    top_categories = ", ".join(columns[:3]) if columns else "various categories"
    remaining = len(columns) - 3 if len(columns) > 3 else 0
    remaining_text = f" and {remaining} others" if remaining > 0 else ""

    return f"""What happened between {date_start} and {date_end}? The data tells a fascinating story.

We're looking at {title}. The key players include {top_categories}{remaining_text}.

Watch as the rankings shift dramatically over the years. Some categories rise to dominance, while others fade into the background.

The changes you're seeing represent real shifts in our world — driven by technology, economics, and human behavior.

By {date_end}, the landscape looks completely different from where we started. The data doesn't lie.

Which trend surprised you the most? Let us know in the comments below."""
