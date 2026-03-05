"""
Tests for Upload Router — data processing and interpolation
"""

import pytest
import io
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient
from unittest.mock import patch

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app
from routers.upload import interpolate_dataframe

client = TestClient(app)


# ============================================================
# UNIT TESTS — interpolate_dataframe
# ============================================================

def test_interpolate_basic():
    """Test basic interpolation between two data points"""
    import datetime
    df = pd.DataFrame(
        {"USA": [100, 200], "China": [50, 150]},
        index=[
            datetime.datetime(2020, 12, 31),
            datetime.datetime(2021, 12, 31),
        ]
    )
    result = interpolate_dataframe(df, 10)
    assert len(result) > 2
    assert "USA" in result.columns
    assert "China" in result.columns


def test_interpolate_year_index():
    """Test that integer year index is converted to datetime"""
    df = pd.DataFrame(
        {"A": [10, 20, 30]},
        index=[2020, 2021, 2022]
    )
    result = interpolate_dataframe(df, 30)
    assert len(result) > 3


def test_interpolate_values_between_points():
    """Test that interpolated values are between original values"""
    import datetime
    df = pd.DataFrame(
        {"X": [0.0, 100.0]},
        index=[
            datetime.datetime(2020, 12, 31),
            datetime.datetime(2021, 12, 31),
        ]
    )
    result = interpolate_dataframe(df, 10)
    # All values should be between 0 and 100
    assert result["X"].min() >= 0
    assert result["X"].max() <= 100


# ============================================================
# INTEGRATION TESTS — Upload API
# ============================================================

def create_test_excel() -> bytes:
    """Create a minimal test Excel file in memory"""
    df = pd.DataFrame(
        {
            "USA": [100, 150, 200],
            "China": [80, 120, 180],
            "Germany": [50, 60, 70],
        },
        index=[2020, 2021, 2022]
    )
    df.index.name = "Year"
    buffer = io.BytesIO()
    df.to_excel(buffer, index=True)
    buffer.seek(0)
    return buffer.read()


def create_test_csv() -> bytes:
    """Create a minimal test CSV file in memory"""
    content = "Year,USA,China,Germany\n2020,100,80,50\n2021,150,120,60\n2022,200,180,70\n"
    return content.encode()


def test_upload_excel():
    """Test uploading a valid Excel file"""
    excel_data = create_test_excel()
    response = client.post(
        "/api/upload",
        files={"file": ("test_data.xlsx", excel_data, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "data_id" in data
    assert "columns" in data
    assert len(data["columns"]) == 3
    assert "USA" in data["columns"]
    assert data["rows"] == 3


def test_upload_csv():
    """Test uploading a valid CSV file"""
    csv_data = create_test_csv()
    response = client.post(
        "/api/upload",
        files={"file": ("test_data.csv", csv_data, "text/csv")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "data_id" in data
    assert data["rows"] == 3


def test_upload_invalid_extension():
    """Test that invalid file extensions are rejected"""
    response = client.post(
        "/api/upload",
        files={"file": ("test.txt", b"some text", "text/plain")}
    )
    assert response.status_code == 400


def test_upload_and_get_data():
    """Test upload then retrieve interpolated data"""
    excel_data = create_test_excel()
    upload_response = client.post(
        "/api/upload",
        files={"file": ("test_data.xlsx", excel_data, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    )
    assert upload_response.status_code == 200
    data_id = upload_response.json()["data_id"]

    # Get interpolated data
    get_response = client.get(f"/api/upload/{data_id}?frames=30")
    assert get_response.status_code == 200
    data = get_response.json()
    assert "frames" in data
    assert len(data["frames"]) > 3  # Should have more frames than original


def test_get_nonexistent_data():
    """Test that requesting non-existent data returns 404"""
    response = client.get("/api/upload/nonexistent-id-12345")
    assert response.status_code == 404


def test_upload_date_range():
    """Test that date range is correctly extracted"""
    excel_data = create_test_excel()
    response = client.post(
        "/api/upload",
        files={"file": ("test_data.xlsx", excel_data, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    )
    data = response.json()
    assert "date_range" in data
    assert "start" in data["date_range"]
    assert "end" in data["date_range"]
    assert "2020" in data["date_range"]["start"]
    assert "2022" in data["date_range"]["end"]
