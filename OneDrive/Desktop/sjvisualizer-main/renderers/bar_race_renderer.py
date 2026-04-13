# renderers/bar_race_renderer.py
"""Bar race renderer module.

This module provides a :func:`render` function that generates a bar‑race video
based on a configuration dictionary. The implementation is extracted from the
original example script ``Examples/B Bar V1.py`` and adapted to be reusable
within the pipeline.

Expected keys in the *config* dictionary:

- ``title`` (str): Chart title.
- ``subtitle`` (str): Subtitle text.
- ``excel_file`` (str): Path to the source Excel file.
- ``aspect_ratio`` (str): One of ``"16:9"``, ``"4:5"``, ``"1:1"`` or ``"9:16"``.
- ``fps`` (int, optional): Frames per second for the output video. Default ``60``.
- ``duration`` (float, optional): Desired video duration in seconds. Default ``0.55``.
- ``record`` (bool, optional): If ``True`` the video is recorded to a file.

The function returns a :class:`pathlib.Path` pointing to the generated video
file.
"""

from __future__ import annotations

import os
import time
import json
from pathlib import Path
from tkinter import font

import pandas as pd
import numpy as np

from sjvisualizer import Canvas, DataHandler, BarRaceOld, Date, StaticImage


def _setup_center_recording(canvas: Canvas.canvas, target_width: int = 1080, target_height: int = 1080) -> None:
    """Patch ``canvas.play`` to record only the central region.

    The original script modifies the ``play`` method to capture a central
    ``target_width`` × ``target_height`` region of the screen. This helper
    reproduces that behaviour.
    """

    original_play = canvas.play

    def center_play(df=None, fps=30, record=False, width=None, height=None, file_name="output.mp4"):
        if not df:
            for sub in canvas.sub_canvas:
                if sub.df is not None:
                    df = sub.df
                    break

        if record:
            canvas.frames = []
            import cv2
            fourc = cv2.VideoWriter_fourcc(*"mp4v")

            screen_width = canvas.tk.winfo_screenwidth()
            screen_height = canvas.tk.winfo_screenheight()

            center_x = (screen_width - target_width) // 2
            center_y = (screen_height - target_height) // 2

            capture_video = cv2.VideoWriter(file_name, fourc, fps, (target_width, target_height))

            try:
                print(f"SNIMANJE CENTRALNOG DIJELA:")
                print(f"Screen: {screen_width}x{screen_height}")
                print(
                    f"Recording area: ({center_x}, {center_y}) to ({center_x + target_width}, {center_y + target_height})"
                )
            except OSError:
                pass

        canvas._add_sj_logo()

        for i, date_time in enumerate(df.index):
            start = time.time()
            canvas.update(date_time)
            if i == 0:
                time.sleep(1)

            if record and i > 1:
                from PIL import ImageGrab, Image

                img = ImageGrab.grab(
                    bbox=(
                        center_x,
                        center_y,
                        center_x + target_width,
                        center_y + target_height,
                    )
                )
                if img.size != (target_width, target_height):
                    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                canvas.frames.append(img)
                if len(canvas.frames) > 10:
                    for f in canvas.frames:
                        img_np = np.array(f)
                        img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                        capture_video.write(img_final)
                    canvas.frames = []

            while time.time() - start < 1 / fps:
                time.sleep(0.0001)

            time_used = time.time() - start
            try:
                print(f"FPS: {1 / time_used:.2f}")
            except OSError:
                pass  # Skip printing if output stream is unavailable

        if record:
            if canvas.frames:
                for f in canvas.frames:
                    img_np = np.array(f)
                    img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                    capture_video.write(img_final)
            capture_video.release()
            time.sleep(1)
            canvas.tk.destroy()
            cv2.destroyAllWindows()
            try:
                print(f"Video snimljen: {file_name}")
            except OSError:
                pass

    canvas.play = center_play


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Convert all columns (except the first) to numeric and fill NaNs with 0."""
    for col in df.columns[1:]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            # Handle non-numeric columns (e.g., convert to 0 or skip)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df_clean = df.dropna(how="all", subset=df.columns[1:])
    return df_clean.fillna(0)


def render(config: dict) -> Path:
    """Render a bar‑race video according to *config*.

    Returns the path to the generated video file.
    """
    # ---------------------------------------------------------------------
    # Configuration handling
    # ---------------------------------------------------------------------
    title = config.get("title", "Tomatoes Production")
    subtitle = config.get("subtitle", "Data presented in metric tons")
    excel_file = config.get("excel_file", "sjvisualizer-main/sjvisualizer-main/Examples/Data/FAOSTAT.xlsx")
    aspect_ratio = config.get("aspect_ratio", "1:1")
    fps = int(config.get("fps", 60))
    duration = float(config.get("duration", 0.55))
    record = bool(config.get("record", False))

    number_of_frames = int(duration * 60 * fps)

    # ---------------------------------------------------------------------
    # Data loading and cleaning
    # ---------------------------------------------------------------------
    print("Loading data...")
    df_handler = DataHandler.DataHandler(excel_file=excel_file, number_of_frames=number_of_frames)
    df = df_handler.df
    df = _clean_dataframe(df)

    if df.shape[0] < 2 or df.shape[1] < 2:
        raise RuntimeError("Insufficient data after cleaning")

    # ---------------------------------------------------------------------
    # Canvas preparation
    # ---------------------------------------------------------------------
    canvas = Canvas.canvas()

    # Aspect‑ratio dimensions
    aspect_ratios = {
        "16:9": (1920, 1080),
        "4:5": (1080, 1350),
        "1:1": (1080, 1080),
        "9:16": (1080, 1920),
    }
    if aspect_ratio in aspect_ratios:
        custom_width, custom_height = aspect_ratios[aspect_ratio]
        canvas.canvas.config(width=custom_width, height=custom_height)
        canvas.width = custom_width
        canvas.height = custom_height
        canvas.canvas["width"] = custom_width
        canvas.canvas["height"] = custom_height
    else:
        custom_width = int(canvas.canvas["width"])
        custom_height = int(canvas.canvas["height"])

    width, height = custom_width, custom_height

    if record:
        _setup_center_recording(canvas, target_width=width, target_height=height)

    # ---------------------------------------------------------------------
    # Bar colours – use a single dark‑red colour for all bars
    # ---------------------------------------------------------------------
    bar_color = (255, 99, 71)  # RGB dark red
    colors = {col: bar_color for col in df.columns[1:]}
    for country in ["Russia", "United States", "France", "United Kingdom", "Israel", "India", "Pakistan", "North Korea"]:
        if country in colors:
            colors[country] = bar_color

    # ---------------------------------------------------------------------
    # Bar chart positioning and scaling
    # ---------------------------------------------------------------------
    chart_scale_factor = 1.0
    base_chart_height = int(height / 2)
    base_chart_width = int(width / 4)
    bar_chart_width = int(base_chart_width * 3.4 * chart_scale_factor)
    bar_chart_height = int(base_chart_height * 1.2 * chart_scale_factor)
    x_offset = 0
    y_offset = 0
    base_x_pos = int(width / 1.95 - bar_chart_width / 1.8)
    base_y_pos = int(height / 8 + height * 0.05)
    bar_x_pos = base_x_pos + x_offset
    chart_y_pos = base_y_pos + y_offset

    # ---------------------------------------------------------------------
    # Create the bar‑race visualisation
    # ---------------------------------------------------------------------
    bar_chart = BarRaceOld.bar_race(
        canvas=canvas.canvas,
        df=df,
        colors=colors,
        height=bar_chart_height,
        width=bar_chart_width,
        x_pos=bar_x_pos,
        y_pos=chart_y_pos,
    )
    canvas.add_sub_plot(bar_chart)

    # ---------------------------------------------------------------------
    # Static assets (logo, CC icon, etc.) – paths are resolved relative to the
    # project root. Missing assets are ignored gracefully.
    # ---------------------------------------------------------------------
    def _add_image(rel_path: str, w: int, h: int, x: int, y: int) -> None:
        img_path = rel_path if os.path.exists(rel_path) else None
        if img_path:
            img = StaticImage.static_image(
                canvas=canvas.canvas,
                file=img_path,
                width=w,
                height=h,
                x_pos=x,
                y_pos=y,
            )
            canvas.add_sub_plot(img)

    # Example logo (double.png) – top‑right corner
    _add_image(
        "assets/double.png",
        int(height / 6),
        int(height / 6),
        int(width * 0.81),
        int(height * 0.76),
    )

    # CC icon – bottom‑left corner
    _add_image(
        "assets/CC.png",
        int(height / 22),
        int(height / 22),
        int(width * 0.07),
        int(height * 0.905),
    )

    # ---------------------------------------------------------------------
    # Title and subtitle text
    # ---------------------------------------------------------------------
    title_font = font.Font(family="Inter", size=int(height / 30), weight="bold")
    subtitle_font = font.Font(family="Sans Serif", size=int(height / 45), weight="bold")
    title_x = int(width * 0.06)
    title_y = int(height * 0.06)
    subtitle_y = title_y + int(height / 35) + 15

    canvas.canvas.create_text(
        title_x,
        title_y,
        text=title,
        fill=Canvas._from_rgb((12, 27, 42)),
        anchor="w",
        font=title_font,
    )
    canvas.canvas.create_text(
        title_x,
        subtitle_y,
        text=subtitle,
        fill=Canvas._from_rgb((140, 140, 140)),
        anchor="w",
        font=subtitle_font,
    )

    # ---------------------------------------------------------------------
    # Date indicator (top‑right)
    # ---------------------------------------------------------------------
    try:
        date_obj = Date.date(
            canvas=canvas.canvas,
            height=int(height / 10),
            width=int(width / 10),
            x_pos=int(width - int(width * 0.18)),
            y_pos=int(height * 0.04),
            time_indicator="year",
            df=df,
            font_color=(12, 27, 42),
        )
        bold_font = font.Font(family="Lato", size=int(height / 20), weight="bold")
        canvas.canvas.coords(date_obj, width - int(width * 0.05), int(height * 0.08))
        canvas.canvas.itemconfig(date_obj, anchor="ne", font=bold_font)
        canvas.add_sub_plot(date_obj)
    except Exception as exc:
        print(f"Could not add date indicator: {exc}")

    # ---------------------------------------------------------------------
    # Data source caption (bottom‑right)
    # ---------------------------------------------------------------------
    source_font = font.Font(family="Lato", size=int(height / 39), weight="bold")
    canvas.canvas.create_text(
        int(width * 0.83),
        height - int(height * 0.0165),
        text="floworio",
        fill=Canvas._from_rgb((12, 27, 42)),
        anchor="sw",
        font=source_font,
    )

    # ---------------------------------------------------------------------
    # Output file name generation
    # ---------------------------------------------------------------------
    excel_name = Path(excel_file).stem
    output_file = f"{excel_name}_{aspect_ratio.replace(':', 'x')}_horizontal_bar_animation.mp4"
    output_path = Path("output") / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Starting animation with video output: {output_path}")
    canvas.play(fps=fps, record=record, file_name=str(output_path))
    print("Animacija uspešno završena!")
    return output_path
