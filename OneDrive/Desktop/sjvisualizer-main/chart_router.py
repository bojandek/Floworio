# chart_router.py

import importlib
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Map chart types to renderer modules
RENDERER_MAP = {
    "bar_race": "renderers.bar_race_renderer",
    "bar": "renderers.bar_renderer",
    "pie": "renderers.pie_renderer",
    "line": "renderers.line_renderer",
    "map": "renderers.map_renderer",
}

def get_renderer(chart_type: str):
    """
    Dynamically import and return the renderer function for the given chart type.
    
    Args:
        chart_type: The type of chart to render (e.g., "bar_race", "pie", "line")
    
    Returns:
        A tuple of (module, render_function)
    
    Raises:
        ValueError: If the chart type is not supported
    """
    if chart_type not in RENDERER_MAP:
        raise ValueError(
            f"Unsupported chart type: {chart_type}. "
            f"Supported types: {list(RENDERER_MAP.keys())}"
        )
    
    module_name = RENDERER_MAP[chart_type]
    try:
        module = importlib.import_module(module_name)
        render_func = getattr(module, "render", None)
        
        if render_func is None:
            raise AttributeError(f"Module {module_name} does not have a 'render' function")
        
        logger.info(f"Loaded renderer for chart type: {chart_type}")
        return module, render_func
    
    except ImportError as e:
        raise ImportError(
            f"Renderer module for '{chart_type}' not found. "
            f"Make sure {module_name}.py exists in the renderers/ folder."
        ) from e

def render_chart(config: Dict[str, Any]) -> Path:
    """
    Main entry point to render a chart based on the configuration.
    
    Args:
        config: Dictionary containing at least 'chart_type' key
    
    Returns:
        Path to the rendered video file
    """
    chart_type = config.get("chart_type", "bar_race")
    logger.info(f"Rendering chart of type: {chart_type}")
    
    _, render_func = get_renderer(chart_type)
    output_path = render_func(config)
    
    logger.info(f"Chart rendered successfully: {output_path}")
    return output_path