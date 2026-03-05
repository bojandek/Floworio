"""
Upload Router — handles Excel/CSV file uploads and data processing
Ports the sjvisualizer DataHandler logic to a REST API
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import uuid
import os
import json
import datetime
from typing import Optional

router = APIRouter()

# In-memory store for uploaded data (use Redis/DB in production)
data_store: dict = {}


def interpolate_dataframe(df: pd.DataFrame, number_of_frames: int) -> pd.DataFrame:
    """
    Port of sjvisualizer DataHandler._prep_data()
    Interpolates data between time points to create smooth animation frames
    """
    # Convert year integers to datetime if needed
    if isinstance(df.index[0], (int, float, np.integer)):
        df.index = [datetime.datetime(year=int(i), month=12, day=31) for i in df.index]

    total_time = list(df.index)[-1] - list(df.index)[1]
    if number_of_frames > 0:
        dt = total_time / number_of_frames
    else:
        dt = datetime.timedelta(days=1)

    temp_df = pd.DataFrame(columns=df.columns)
    time = list(df.index)[0]

    for i, (index, row) in enumerate(df.iterrows()):
        if i > 0:
            while time < index:
                temp_df = pd.concat([temp_df, pd.DataFrame(None, index=[time], columns=df.columns)])
                time = time + dt
            temp_df = pd.concat([temp_df, pd.DataFrame([list(row)], index=[index], columns=df.columns)])
            time = index + dt
        elif i == 0:
            temp_df = pd.concat([temp_df, pd.DataFrame([list(row)], index=[index], columns=df.columns)])
            time = time + dt

    # Convert to numeric for interpolation
    for col in temp_df:
        try:
            temp_df[col] = pd.to_numeric(temp_df[col])
        except (ValueError, TypeError):
            pass

    # Interpolate
    try:
        temp_df = temp_df.interpolate(method='time', limit_area='inside')
    except Exception:
        temp_df = temp_df.interpolate(limit_area='inside')

    # Fill NaN with 0
    temp_df = temp_df.fillna(0)

    return temp_df


@router.post("")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload an Excel or CSV file and process it for animation
    Returns: data_id, columns, date_range, preview data
    """
    # Validate file type
    allowed_extensions = [".xlsx", ".xls", ".csv"]
    file_ext = os.path.splitext(file.filename or "")[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Read file
    try:
        content = await file.read()

        if file_ext == ".csv":
            df = pd.read_csv(pd.io.common.BytesIO(content), index_col=0)
        else:
            df = pd.read_excel(pd.io.common.BytesIO(content), index_col=0)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    # Clean data
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(how='all')
    df = df.fillna(0)

    if df.shape[0] < 2:
        raise HTTPException(status_code=400, detail="File must have at least 2 data rows")

    if df.shape[1] < 1:
        raise HTTPException(status_code=400, detail="File must have at least 1 data column")

    # Generate unique ID
    data_id = str(uuid.uuid4())

    # Get date range
    try:
        if isinstance(df.index[0], (int, float, np.integer)):
            date_start = str(int(df.index[0]))
            date_end = str(int(df.index[-1]))
        else:
            date_start = str(df.index[0])
            date_end = str(df.index[-1])
    except Exception:
        date_start = "Unknown"
        date_end = "Unknown"

    # Store raw dataframe (serialize to JSON)
    df_serializable = df.copy()
    df_serializable.index = df_serializable.index.astype(str)

    data_store[data_id] = {
        "df_json": df_serializable.to_json(),
        "columns": list(df.columns),
        "rows": len(df),
        "date_start": date_start,
        "date_end": date_end,
        "filename": file.filename,
    }

    # Preview: first 5 rows
    preview = []
    for idx, row in df.head(5).iterrows():
        preview.append({
            "date": str(idx),
            **{col: float(val) for col, val in row.items()}
        })

    return {
        "data_id": data_id,
        "filename": file.filename,
        "columns": list(df.columns),
        "rows": len(df),
        "date_range": {
            "start": date_start,
            "end": date_end,
        },
        "preview": preview,
        "message": "File uploaded and processed successfully",
    }


@router.get("/{data_id}")
async def get_data(data_id: str, frames: Optional[int] = 1800):
    """
    Get processed (interpolated) data for a given data_id
    frames: number of animation frames (fps * duration * 60)
    """
    if data_id not in data_store:
        raise HTTPException(status_code=404, detail="Data not found")

    stored = data_store[data_id]
    df = pd.read_json(stored["df_json"])

    # Interpolate for animation
    try:
        interpolated_df = interpolate_dataframe(df, frames)
        # Convert to list of frame data
        frames_data = []
        for idx, row in interpolated_df.iterrows():
            frames_data.append({
                "timestamp": str(idx),
                "values": {col: float(val) for col, val in row.items()}
            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interpolation failed: {str(e)}")

    return {
        "data_id": data_id,
        "columns": stored["columns"],
        "frames": frames_data,
        "total_frames": len(frames_data),
    }


@router.get("/{data_id}/raw")
async def get_raw_data(data_id: str):
    """Get raw (non-interpolated) data"""
    if data_id not in data_store:
        raise HTTPException(status_code=404, detail="Data not found")

    stored = data_store[data_id]
    df = pd.read_json(stored["df_json"])

    rows = []
    for idx, row in df.iterrows():
        rows.append({
            "date": str(idx),
            **{col: float(val) for col, val in row.items()}
        })

    return {
        "data_id": data_id,
        "columns": stored["columns"],
        "rows": rows,
        "date_range": {
            "start": stored["date_start"],
            "end": stored["date_end"],
        }
    }
