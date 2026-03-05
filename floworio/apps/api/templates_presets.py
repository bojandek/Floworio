"""
Pre-configured Templates — Ekstraktovani iz sjvisualizer primjera
Omogućava brzo korišćenje proven template-a sa svim detaljima
"""

# B Bar V1 Template - Tomatoes Production
BAR_RACE_V1_TEMPLATE = {
    "name": "Bar Race - Tomatoes Production (B Bar V1)",
    "chart_type": "bar_race",
    "description": "Professional bar race template sa Tomatoes Production naslovom - ekstraktovano iz B Bar V1.py",
    "style": {
        "title": "Tomatoes Production",
        "subtitle": "Data presented in metric tons",
        "title_font": "Inter",
        "title_size": 32,
        "subtitle_font": "Sans Serif",
        "subtitle_size": 18,
        "background_color": [255, 255, 255],
        "text_color": [12, 27, 42],
        "accent_color": [255, 99, 71]  # Dark red iz B Bar V1
    },
    "colors": {
        "primary_colors": [
            [255, 99, 71]  # Dark red - sve boje su iste kao u B Bar V1
        ],
        "background": [255, 255, 255],
        "text": [12, 27, 42],
        "grid": [200, 200, 200],
        "accent": [255, 99, 71]
    },
    "layout": {
        "chart_type": "bar_race",
        "aspect_ratio": "1:1",
        "fps": 60,
        "duration": 33,  # 0.55 * 60 = 33 sekunde
        "animation_speed": 1.0,
        "chart_scale_factor": 1.0,
        "x_offset": 0,
        "y_offset": 0
    },
    "positioning": {
        "bar_chart_width_factor": 3.4,
        "bar_chart_height_factor": 1.2,
        "title_x_factor": 0.06,
        "title_y_factor": 0.06,
        "logo_x_factor": 0.81,
        "logo_y_factor": 0.76,
        "date_x_factor": 0.95,
        "date_y_factor": 0.04,
        "data_source_x_factor": 0.02,
        "data_source_y_factor": 0.015,
        "floworio_x_factor": 0.83,
        "floworio_y_factor": 0.0165,
        "cc_icon_x_factor": 0.04,
        "cc_icon_y_factor": 0.905
    },
    "logo_url": None,
    "data_source": "Data Source: https://www.fao.org/faostat/",
    "show_date": True,
    "show_logo": True,
    "show_data_source": True,
    "show_floworio_branding": True,
    "show_cc_icon": True,
    "accent_box": {
        "enabled": True,
        "color": [255, 99, 71],
        "x_factor": 0.03,
        "y_factor": 0.028,
        "width_factor": 0.018,
        "height_factor": 0.10,
        "radius": 10
    }
}

# Pie Race Template - Beeswax Production
PIE_RACE_TEMPLATE = {
    "name": "Pie Race - Beeswax Production",
    "chart_type": "pie_race",
    "description": "Professional pie race template sa Beeswax Production naslovom - 1:1 format",
    "style": {
        "title": "Beeswax Production Qty",
        "subtitle": "Data presented in metric tons",
        "title_font": "Inter",
        "title_size": 32,
        "subtitle_font": "Sans Serif",
        "subtitle_size": 18,
        "background_color": [255, 255, 255],
        "text_color": [12, 27, 42],
        "accent_color": [255, 215, 0]
    },
    "colors": {
        "primary_colors": [
            [255, 107, 107], [255, 159, 67], [255, 206, 84], [220, 221, 225],
            [116, 185, 255], [162, 155, 254], [223, 230, 233], [116, 255, 177]
        ],
        "background": [255, 255, 255],
        "text": [12, 27, 42],
        "grid": [200, 200, 200],
        "accent": [255, 215, 0]
    },
    "layout": {
        "chart_type": "pie_race",
        "aspect_ratio": "1:1",
        "fps": 60,
        "duration": 30,
        "animation_speed": 1.0,
        "pie_size": 0.75,
        "pie_position": "center"
    },
    "positioning": {
        "pie_x_factor": 0.5,
        "pie_y_factor": 0.35,
        "title_x_factor": 0.06,
        "title_y_factor": 0.06,
        "logo_x_factor": 0.85,
        "logo_y_factor": 0.83,
        "date_x_factor": 0.95,
        "date_y_factor": 0.04,
        "data_source_x_factor": 0.02,
        "data_source_y_factor": 0.015,
        "floworio_x_factor": 0.83,
        "floworio_y_factor": 0.0165,
        "cc_icon_x_factor": 0.04,
        "cc_icon_y_factor": 0.905
    },
    "logo_url": None,
    "data_source": "Data Source: https://www.fao.org/faostat/",
    "show_date": True,
    "show_logo": True,
    "show_data_source": True,
    "show_floworio_branding": True,
    "show_cc_icon": True,
    "accent_box": {
        "enabled": True,
        "color": [255, 215, 0],
        "x_factor": 0.03,
        "y_factor": 0.028,
        "width_factor": 0.018,
        "height_factor": 0.10,
        "radius": 10
    }
}

# Line Chart Template
LINE_CHART_TEMPLATE = {
    "name": "Line Chart - Trend Analysis",
    "chart_type": "line_chart",
    "description": "Professional line chart template sa trend analizom",
    "style": {
        "title": "Trend Analysis",
        "subtitle": "Historical Data",
        "title_font": "Inter",
        "title_size": 40,
        "subtitle_font": "Sans Serif",
        "subtitle_size": 20,
        "background_color": [255, 255, 255],
        "text_color": [12, 27, 42],
        "accent_color": [52, 152, 219]
    },
    "colors": {
        "primary_colors": [
            [52, 152, 219], [155, 89, 182], [26, 188, 156], [46, 204, 113]
        ],
        "background": [255, 255, 255],
        "text": [12, 27, 42],
        "grid": [200, 200, 200],
        "accent": [52, 152, 219]
    },
    "layout": {
        "chart_type": "line_chart",
        "aspect_ratio": "16:9",
        "fps": 60,
        "duration": 30,
        "animation_speed": 1.0,
        "grid": True,
        "legend": True
    },
    "positioning": {
        "title_x_factor": 0.06,
        "title_y_factor": 0.06,
        "logo_x_factor": 0.85,
        "logo_y_factor": 0.83,
        "date_x_factor": 0.95,
        "date_y_factor": 0.04,
        "data_source_x_factor": 0.02,
        "data_source_y_factor": 0.015,
        "floworio_x_factor": 0.83,
        "floworio_y_factor": 0.0165
    },
    "logo_url": None,
    "data_source": "Data Source: https://www.fao.org/faostat/",
    "show_date": True,
    "show_logo": True,
    "show_data_source": True,
    "show_floworio_branding": True,
    "show_cc_icon": False,
    "accent_box": {
        "enabled": False
    }
}

# Area Chart Template
AREA_CHART_TEMPLATE = {
    "name": "Area Chart - Stacked Data",
    "chart_type": "area_chart",
    "description": "Professional area chart template sa stacked podacima",
    "style": {
        "title": "Stacked Area Chart",
        "subtitle": "Cumulative Data",
        "title_font": "Inter",
        "title_size": 40,
        "subtitle_font": "Sans Serif",
        "subtitle_size": 20,
        "background_color": [255, 255, 255],
        "text_color": [12, 27, 42],
        "accent_color": [39, 174, 96]
    },
    "colors": {
        "primary_colors": [
            [39, 174, 96], [142, 68, 173], [230, 126, 34], [231, 76, 60]
        ],
        "background": [255, 255, 255],
        "text": [12, 27, 42],
        "grid": [200, 200, 200],
        "accent": [39, 174, 96]
    },
    "layout": {
        "chart_type": "area_chart",
        "aspect_ratio": "16:9",
        "fps": 60,
        "duration": 30,
        "animation_speed": 1.0,
        "stacked": True,
        "grid": True
    },
    "positioning": {
        "title_x_factor": 0.06,
        "title_y_factor": 0.06,
        "logo_x_factor": 0.85,
        "logo_y_factor": 0.83,
        "date_x_factor": 0.95,
        "date_y_factor": 0.04,
        "data_source_x_factor": 0.02,
        "data_source_y_factor": 0.015,
        "floworio_x_factor": 0.83,
        "floworio_y_factor": 0.0165
    },
    "logo_url": None,
    "data_source": "Data Source: https://www.fao.org/faostat/",
    "show_date": True,
    "show_logo": True,
    "show_data_source": True,
    "show_floworio_branding": True,
    "show_cc_icon": False,
    "accent_box": {
        "enabled": False
    }
}

# World Map Template
WORLD_MAP_TEMPLATE = {
    "name": "World Map - Global Distribution",
    "chart_type": "world_map",
    "description": "Professional world map template sa globalnom distribucijom",
    "style": {
        "title": "Global Distribution",
        "subtitle": "By Country",
        "title_font": "Inter",
        "title_size": 40,
        "subtitle_font": "Sans Serif",
        "subtitle_size": 20,
        "background_color": [255, 255, 255],
        "text_color": [12, 27, 42],
        "accent_color": [52, 152, 219]
    },
    "colors": {
        "primary_colors": [
            [52, 152, 219], [155, 89, 182], [26, 188, 156], [46, 204, 113]
        ],
        "background": [255, 255, 255],
        "text": [12, 27, 42],
        "water": [173, 216, 230],
        "accent": [52, 152, 219]
    },
    "layout": {
        "chart_type": "world_map",
        "aspect_ratio": "16:9",
        "fps": 60,
        "duration": 30,
        "animation_speed": 1.0,
        "projection": "mercator"
    },
    "positioning": {
        "title_x_factor": 0.06,
        "title_y_factor": 0.06,
        "logo_x_factor": 0.85,
        "logo_y_factor": 0.83,
        "date_x_factor": 0.95,
        "date_y_factor": 0.04,
        "data_source_x_factor": 0.02,
        "data_source_y_factor": 0.015,
        "floworio_x_factor": 0.83,
        "floworio_y_factor": 0.0165
    },
    "logo_url": None,
    "data_source": "Data Source: https://www.fao.org/faostat/",
    "show_date": True,
    "show_logo": True,
    "show_data_source": True,
    "show_floworio_branding": True,
    "show_cc_icon": False,
    "accent_box": {
        "enabled": False
    }
}

# Dictionary sa svim template-ima
PRESET_TEMPLATES = {
    "bar_race_v1": BAR_RACE_V1_TEMPLATE,
    "pie_race": PIE_RACE_TEMPLATE,
    "line_chart": LINE_CHART_TEMPLATE,
    "area_chart": AREA_CHART_TEMPLATE,
    "world_map": WORLD_MAP_TEMPLATE,
}

def get_preset_template(template_key: str):
    """Vrati preset template po ključu"""
    return PRESET_TEMPLATES.get(template_key)

def get_all_preset_templates():
    """Vrati sve preset template-e"""
    return PRESET_TEMPLATES

def get_preset_templates_by_chart_type(chart_type: str):
    """Vrati sve preset template-e za određeni tip chart-a"""
    return {
        key: template 
        for key, template in PRESET_TEMPLATES.items() 
        if template.get("chart_type") == chart_type
    }
