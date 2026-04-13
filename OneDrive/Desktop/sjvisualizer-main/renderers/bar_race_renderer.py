# renderers/bar_race_renderer.py

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
    """Patch canvas.play to record only the central region of the screen."""

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
                print(f"Recording area: ({center_x}, {center_y}) to ({center_x + target_width}, {center_y + target_height})")
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
                img = ImageGrab.grab(bbox=(center_x, center_y, center_x + target_width, center_y + target_height))
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
                pass

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
                print("Animacija uspešno završena!")
            except OSError:
                pass

    canvas.play = center_play


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df_clean = df.dropna(how="all", subset=df.columns[1:])
    return df_clean.fillna(0)


def _draw_rounded_rect(canvas, x, y, w, h, r=10, **kwargs):
    """Draw a rounded rectangle on a tkinter canvas."""
    x2, y2 = x + w, y + h
    points = [
        x + r, y,   x2 - r, y,
        x2, y,       x2, y + r,
        x2, y2 - r,  x2, y2,
        x2 - r, y2,  x + r, y2,
        x, y2,       x, y2 - r,
        x, y + r,    x, y,
        x + r, y
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def render(config: dict) -> Path:
    """Render a bar-race video with flags, data source, and CC logo."""

    # ── config ────────────────────────────────────────────────────────────────
    title        = config.get("title", "Tomatoes Production")
    subtitle     = config.get("subtitle", "Data presented in metric tons")
    source_url   = config.get("source_url", "https://www.fao.org/faostat/")
    excel_file   = config.get("excel_file", "sjvisualizer-main/sjvisualizer-main/Examples/Data/FAOSTAT.xlsx")
    aspect_ratio = config.get("aspect_ratio", "1:1")
    fps          = int(config.get("fps", 60))
    duration     = float(config.get("duration", 0.55))
    record       = bool(config.get("record", False))

    number_of_frames = int(duration * 60 * fps)

    # ── download missing flags before rendering ───────────────────────────────
    try:
        from flag_downloader import download_flags_for_excel
        download_flags_for_excel(excel_file, output_dir="assets")
    except Exception as e:
        print(f"Flag download skipped: {e}")

    # ── data ──────────────────────────────────────────────────────────────────
    print("Loading data...")
    df = DataHandler.DataHandler(excel_file=excel_file, number_of_frames=number_of_frames).df
    df = _clean_dataframe(df)

    if df.shape[0] < 2 or df.shape[1] < 2:
        raise RuntimeError("Insufficient data after cleaning")

    # ── canvas ────────────────────────────────────────────────────────────────
    canvas = Canvas.canvas()

    aspect_ratios = {
        "16:9": (1920, 1080),
        "4:5":  (1080, 1350),
        "1:1":  (1080, 1080),
        "9:16": (1080, 1920),
    }
    custom_width, custom_height = aspect_ratios.get(aspect_ratio, (1080, 1080))

    canvas.canvas.config(width=custom_width, height=custom_height)
    canvas.width  = custom_width
    canvas.height = custom_height
    canvas.canvas["width"]  = custom_width
    canvas.canvas["height"] = custom_height

    width, height = custom_width, custom_height

    if record:
        _setup_center_recording(canvas, target_width=width, target_height=height)

    # ── bar colors ────────────────────────────────────────────────────────────
    bar_color = (255, 99, 71)
    colors = {col: bar_color for col in df.columns[1:]}

    # ── bar chart (BarRace – supports flags) ──────────────────────────────────
    chart_scale  = 1.0
    bar_w = int(width / 4 * 3.4 * chart_scale)
    bar_h = int(height / 2 * 1.2 * chart_scale)
    bar_x = int(width / 1.95 - bar_w / 1.8)
    bar_y = int(height / 8 + height * 0.05)

    bar_chart = BarRaceOld.bar_race(
        canvas=canvas.canvas,
        df=df,
        colors=colors,
        height=bar_h,
        width=bar_w,
        x_pos=bar_x,
        y_pos=bar_y,
    )
    canvas.add_sub_plot(bar_chart)

    # ── helper: add static image ──────────────────────────────────────────────
    def _add_image(path: str, w: int, h: int, x: int, y: int) -> None:
        if os.path.exists(path):
            img = StaticImage.static_image(
                canvas=canvas.canvas, file=path,
                width=w, height=h, x_pos=x, y_pos=y,
            )
            canvas.add_sub_plot(img)

    # ── logo (top-right) ──────────────────────────────────────────────────────
    _add_image(
        "assets/double.png",
        int(height / 6), int(height / 6),
        int(width * 0.81), int(height * 0.76),
    )

    # ── CC icon (bottom-left) ─────────────────────────────────────────────────
    _add_image(
        "assets/CC.png",
        int(height / 22), int(height / 22),
        int(width * 0.02), int(height * 0.905),
    )

    # ── colored accent bar (top-left) ─────────────────────────────────────────
    line_hex = "#{:02x}{:02x}{:02x}".format(*bar_color)
    _draw_rounded_rect(
        canvas.canvas,
        int(width * 0.03), int(height * 0.028),
        int(width * 0.018), int(height * 0.10),
        r=10, fill=line_hex, outline="", tags="accent_bar"
    )

    # ── title & subtitle ──────────────────────────────────────────────────────
    title_font    = font.Font(family="Inter",      size=int(height / 30), weight="bold")
    subtitle_font = font.Font(family="Sans Serif", size=int(height / 45), weight="bold")
    tx = int(width * 0.06)
    ty = int(height * 0.06)
    sy = ty + int(height / 35) + 15

    canvas.canvas.create_text(tx, ty, text=title,
        fill=Canvas._from_rgb((12, 27, 42)), anchor="w", font=title_font)
    canvas.canvas.create_text(tx, sy, text=subtitle,
        fill=Canvas._from_rgb((140, 140, 140)), anchor="w", font=subtitle_font)

    # ── date indicator (top-right) ────────────────────────────────────────────
    try:
        date_obj = Date.date(
            canvas=canvas.canvas,
            height=int(height / 10), width=int(width / 10),
            x_pos=int(width - int(width * 0.18)), y_pos=int(height * 0.04),
            time_indicator="year", df=df, font_color=(12, 27, 42),
        )
        bold_font = font.Font(family="Lato", size=int(height / 20), weight="bold")
        canvas.canvas.coords(date_obj, width - int(width * 0.05), int(height * 0.08))
        canvas.canvas.itemconfig(date_obj, anchor="ne", font=bold_font)
        canvas.add_sub_plot(date_obj)
    except Exception as exc:
        print(f"Could not add date: {exc}")

    # ── data source (bottom-left) — read from config ──────────────────────────
    src_font = font.Font(family="Sans Serif", size=int(height / 65))
    canvas.canvas.create_text(
        int(width * 0.09),
        height - int(height * 0.015),
        text=f"Data Source: {source_url}",
        fill=Canvas._from_rgb((12, 27, 42)),
        anchor="sw",
        font=src_font,
    )

    # ── "floworio" branding (bottom-right) ────────────────────────────────────
    brand_font = font.Font(family="Lato", size=int(height / 39), weight="bold")
    canvas.canvas.create_text(
        int(width * 0.83),
        height - int(height * 0.0165),
        text="floworio",
        fill=Canvas._from_rgb((12, 27, 42)),
        anchor="sw",
        font=brand_font,
    )

    # ── output path ───────────────────────────────────────────────────────────
    excel_name  = Path(excel_file).stem
    output_file = f"{excel_name}_{aspect_ratio.replace(':', 'x')}_horizontal_bar_animation.mp4"
    output_path = Path("output") / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Starting animation with video output: {output_path}")
    canvas.play(fps=fps, record=record, file_name=str(output_path))
    return output_path
