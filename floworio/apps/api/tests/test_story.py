"""
Tests for Story Router — AI story generation
"""

import pytest
import io
import pandas as pd
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app
from routers.story import generate_template_script, build_story_prompt

client = TestClient(app)


# ============================================================
# UNIT TESTS
# ============================================================

def test_template_script_basic():
    """Test template script generation"""
    script = generate_template_script(
        title="World GDP Rankings",
        columns=["USA", "China", "Germany"],
        date_start="2000",
        date_end="2023",
        duration=30,
    )
    assert len(script) > 50
    assert "2000" in script
    assert "2023" in script


def test_template_script_many_columns():
    """Test template script with many columns"""
    columns = [f"Country{i}" for i in range(20)]
    script = generate_template_script(
        title="Test",
        columns=columns,
        date_start="2000",
        date_end="2020",
        duration=30,
    )
    assert "others" in script  # Should mention remaining count


def test_build_story_prompt():
    """Test prompt building"""
    prompt = build_story_prompt(
        data_summary={
            "columns": ["USA", "China"],
            "rows": 10,
            "date_start": "2000",
            "date_end": "2023",
        },
        title="GDP Rankings",
        chart_type="bar_race",
        duration=30,
        tone="engaging",
    )
    assert "GDP Rankings" in prompt
    assert "bar chart race" in prompt
    assert "30 seconds" in prompt
    assert "USA" in prompt


# ============================================================
# INTEGRATION TESTS
# ============================================================

def upload_test_data() -> str:
    """Helper: upload test data and return data_id"""
    df = pd.DataFrame(
        {"USA": [100, 200], "China": [80, 160]},
        index=[2020, 2021]
    )
    df.index.name = "Year"
    buffer = io.BytesIO()
    df.to_excel(buffer, index=True)
    buffer.seek(0)

    response = client.post(
        "/api/upload",
        files={"file": ("test.xlsx", buffer.read(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    )
    return response.json()["data_id"]


def test_generate_story_template_fallback():
    """Test story generation falls back to template when no AI key"""
    data_id = upload_test_data()

    with patch.dict(os.environ, {"OPENAI_API_KEY": "", "ANTHROPIC_API_KEY": ""}):
        response = client.post(
            "/api/story/generate",
            json={
                "data_id": data_id,
                "title": "Test Chart",
                "chart_type": "bar_race",
                "duration": 30,
            }
        )

    assert response.status_code == 200
    data = response.json()
    assert "script" in data
    assert len(data["script"]) > 50
    assert "word_count" in data
    assert data["word_count"] > 0


def test_generate_story_invalid_data_id():
    """Test story generation with invalid data_id"""
    response = client.post(
        "/api/story/generate",
        json={
            "data_id": "invalid-id-xyz",
            "title": "Test",
            "chart_type": "bar_race",
            "duration": 30,
        }
    )
    assert response.status_code == 404
