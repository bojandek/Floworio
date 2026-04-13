# voice_script_generator.py
"""
Generate voiceover script from data for bar race videos.
"""

import logging
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional

from sjvisualizer import DataHandler

logger = logging.getLogger(__name__)


def generate_voice_script(config: dict, df: pd.DataFrame) -> str:
    """
    Generate a voiceover script based on the data in the DataFrame.

    Args:
        config: Configuration dict with title, subtitle, etc.
        df: DataFrame with time-series data

    Returns:
        Generated voiceover script as a string
    """
    title = config.get('title', 'Data Visualization')
    subtitle = config.get('subtitle', 'Data presented in metric tons')

    # Get column names (countries)
    countries = list(df.columns[1:])  # Skip first column (dates)

    # Get latest values (sorted)
    latest_row = df.iloc[-1]
    latest_values = [(country, latest_row[country]) for country in countries if not pd.isna(latest_row[country])]
    latest_values.sort(key=lambda x: x[1], reverse=True)

    # Get top 5 countries
    top_countries = latest_values[:5]

    # Get data range
    all_values = []
    for country in countries:
        values = df[country].dropna()
        if len(values) > 0:
            all_values.extend(values.tolist())

    min_val = min(all_values) if all_values else 0
    max_val = max(all_values) if all_values else 1
    total_changes = len(df) - 1

    # Generate script
    script_parts = []

    # Introduction
    script_parts.append(f"{title}. {subtitle}")

    # Time period
    dates = df.index.tolist()
    if len(dates) >= 2:
        script_parts.append(f"Showing data from {dates[0]} to {dates[-1]}.")

    # Top country analysis
    if top_countries:
        script_parts.append(f"At the end of the period, {top_countries[0][0]} leads with {format_number(top_countries[0][1])}.")

        if len(top_countries) >= 2:
            script_parts.append(f"Second place goes to {top_countries[1][0]} with {format_number(top_countries[1][1])}.")

        if len(top_countries) >= 3:
            script_parts.append(f"And in third place, {top_countries[2][0]} with {format_number(top_countries[2][1])}.")

    # Notable changes
    script_parts.extend(_find_notable_changes(df, countries))

    # Overall trend
    script_parts.append(f"Throughout this period, values ranged from {format_number(min_val)} to {format_number(max_val)}.")

    # Closing
    script_parts.append(f"That's {title}.")

    return " ".join(script_parts)


def _find_notable_changes(df: pd.DataFrame, countries: List[str]) -> List[str]:
    """Find and describe notable changes in the data."""
    changes = []

    # Get first and last values
    first_row = df.iloc[0]
    last_row = df.iloc[-1]

    # Find countries with largest growth
    growth_rates = []
    for country in countries:
        if country in first_row.index and country in last_row.index:
            first_val = first_row[country]
            last_val = last_row[country]
            if pd.notna(first_val) and pd.notna(last_val) and first_val > 0:
                growth = ((last_val - first_val) / first_val) * 100
                growth_rates.append((country, growth, first_val, last_val))

    # Sort by growth rate
    growth_rates.sort(key=lambda x: x[1], reverse=True)

    # Find top growers and decliners
    top_growers = [g for g in growth_rates if g[1] > 0][:2]
    top_decliners = [g for g in growth_rates if g[1] < 0][:2]

    if top_growers:
        country, rate, _, _ = top_growers[0]
        changes.append(f"{country} showed the strongest growth, increasing by {rate:.1f}%.")

    if top_decliners:
        country, rate, _, _ = top_decliners[0]
        changes.append(f"{country} experienced the largest decline, decreasing by {abs(rate):.1f}%.")

    return changes


def format_number(value: float) -> str:
    """Format a number for speech."""
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f} billion"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f} million"
    elif value >= 1_000:
        return f"{value / 1_000:.1f} thousand"
    else:
        return f"{value:.0f}"


def get_country_names(df: pd.DataFrame) -> List[str]:
    """Get list of country names from DataFrame columns."""
    return list(df.columns[1:]) if len(df.columns) > 1 else []


if __name__ == '__main__':
    # Test with FAOSTAT data
    excel_file = 'sjvisualizer-main/sjvisualizer-main/Examples/Data/FAOSTAT.xlsx'
    df_handler = DataHandler.DataHandler(excel_file=excel_file, number_of_frames=100)
    df = df_handler.df

    # Clean data
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(how='all', subset=df.columns[1:]).fillna(0)

    config = {
        'title': 'FAOSTAT Data',
        'subtitle': 'Food and Agriculture Organization statistics'
    }

    script = generate_voice_script(config, df)
    print("Generated voiceover script:")
    print(script)
