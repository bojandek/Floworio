"""
Advanced Template Router — Upravljanje naprednim chart template-ima
Omogućava snimanje template-a sa naslovom, logom, bojama, data source-om
"""

from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import os
from datetime import datetime
import shutil

router = APIRouter(prefix="/api/templates/advanced", tags=["advanced-templates"])

# Template storage directory
TEMPLATES_DIR = "templates/advanced"
LOGOS_DIR = "templates/logos"
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(LOGOS_DIR, exist_ok=True)

class TemplateStyle(BaseModel):
    """Stil template-a"""
    title: str
    subtitle: str
    title_font: str = "Inter"
    title_size: int = 32
    subtitle_font: str = "Sans Serif"
    subtitle_size: int = 18
    background_color: tuple = (255, 255, 255)
    text_color: tuple = (12, 27, 42)
    accent_color: tuple = (255, 215, 0)

class TemplateColors(BaseModel):
    """Boje za chart"""
    primary_colors: List[tuple]  # Boje za chart elementy
    background: tuple = (255, 255, 255)
    text: tuple = (12, 27, 42)
    grid: tuple = (200, 200, 200)
    accent: tuple = (255, 215, 0)

class TemplateLayout(BaseModel):
    """Layout template-a"""
    chart_type: str  # "bar_race", "pie_race", "line_chart", "area_chart", "world_map"
    aspect_ratio: str = "16:9"  # "16:9", "9:16", "1:1", "4:5"
    fps: int = 60
    duration: int = 30
    animation_speed: float = 1.0

class AdvancedTemplate(BaseModel):
    """Napredni template sa svim detaljima"""
    name: str
    chart_type: str
    description: Optional[str] = None
    style: TemplateStyle
    colors: TemplateColors
    layout: TemplateLayout
    logo_url: Optional[str] = None  # URL ili path do loga
    data_source: str = "Data Source: https://www.fao.org/faostat/"
    show_date: bool = True
    show_logo: bool = True
    show_data_source: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@router.post("/save")
async def save_advanced_template(template: AdvancedTemplate):
    """Spremi napredni template"""
    try:
        # Generiši ID
        template_id = f"{template.chart_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Postavi timestamp-e
        now = datetime.now().isoformat()
        template.created_at = now
        template.updated_at = now
        
        # Spremi template kao JSON
        template_path = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
        
        with open(template_path, "w") as f:
            json.dump(template.dict(), f, indent=4, default=str)
        
        return {
            "id": template_id,
            "message": f"Advanced template '{template.name}' saved successfully",
            "path": template_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-logo")
async def upload_logo(file: UploadFile = File(...)):
    """Učitaj logo za template"""
    try:
        # Generiši filename
        filename = f"logo_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(LOGOS_DIR, filename)
        
        # Spremi fajl
        with open(filepath, "wb") as f:
            content = await file.read()
            f.write(content)
        
        return {
            "filename": filename,
            "path": filepath,
            "url": f"/templates/logos/{filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_advanced_templates(chart_type: Optional[str] = None):
    """Lista svih naprednih template-a"""
    try:
        templates = []
        
        for filename in os.listdir(TEMPLATES_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(TEMPLATES_DIR, filename)
                
                with open(filepath, "r") as f:
                    template_data = json.load(f)
                
                # Filtriraj po chart_type ako je specificiran
                if chart_type and template_data.get("chart_type") != chart_type:
                    continue
                
                templates.append({
                    "id": filename.replace(".json", ""),
                    "name": template_data.get("name"),
                    "chart_type": template_data.get("chart_type"),
                    "description": template_data.get("description"),
                    "style": template_data.get("style"),
                    "colors": template_data.get("colors"),
                    "layout": template_data.get("layout"),
                    "created_at": template_data.get("created_at"),
                    "updated_at": template_data.get("updated_at")
                })
        
        return {"templates": templates, "count": len(templates)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{template_id}")
async def get_advanced_template(template_id: str):
    """Učitaj napredni template po ID-u"""
    try:
        template_path = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
        
        if not os.path.exists(template_path):
            raise HTTPException(status_code=404, detail="Template not found")
        
        with open(template_path, "r") as f:
            template = json.load(f)
        
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{template_id}")
async def update_advanced_template(template_id: str, template: AdvancedTemplate):
    """Ažuriraj napredni template"""
    try:
        template_path = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
        
        if not os.path.exists(template_path):
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Učitaj stari template da sačuvaš created_at
        with open(template_path, "r") as f:
            old_template = json.load(f)
        
        # Ažuriraj timestamp
        template.created_at = old_template.get("created_at")
        template.updated_at = datetime.now().isoformat()
        
        # Spremi ažurirani template
        with open(template_path, "w") as f:
            json.dump(template.dict(), f, indent=4, default=str)
        
        return {
            "id": template_id,
            "message": f"Advanced template '{template.name}' updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{template_id}")
async def delete_advanced_template(template_id: str):
    """Obriši napredni template"""
    try:
        template_path = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
        
        if not os.path.exists(template_path):
            raise HTTPException(status_code=404, detail="Template not found")
        
        os.remove(template_path)
        
        return {"message": f"Advanced template '{template_id}' deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Default templates sa svim detaljima

@router.get("/defaults/pie-race-full")
async def get_pie_race_full_template():
    """Vrati kompletan default template za Pie Race sa svim detaljima"""
    return {
        "name": "Pie Race - Professional",
        "chart_type": "pie_race",
        "description": "Professional pie race template sa naslovom, logom i data source-om",
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
            "animation_speed": 1.0
        },
        "logo_url": None,
        "data_source": "Data Source: https://www.fao.org/faostat/",
        "show_date": True,
        "show_logo": True,
        "show_data_source": True
    }

@router.get("/defaults/bar-race-full")
async def get_bar_race_full_template():
    """Vrati kompletan default template za Bar Race"""
    return {
        "name": "Bar Race - Professional",
        "chart_type": "bar_race",
        "description": "Professional bar race template sa naslovom, logom i data source-om",
        "style": {
            "title": "Country Rankings",
            "subtitle": "2020-2024",
            "title_font": "Inter",
            "title_size": 40,
            "subtitle_font": "Sans Serif",
            "subtitle_size": 20,
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
            "chart_type": "bar_race",
            "aspect_ratio": "16:9",
            "fps": 60,
            "duration": 30,
            "animation_speed": 1.0
        },
        "logo_url": None,
        "data_source": "Data Source: https://www.fao.org/faostat/",
        "show_date": True,
        "show_logo": True,
        "show_data_source": True
    }

@router.get("/defaults/line-chart-full")
async def get_line_chart_full_template():
    """Vrati kompletan default template za Line Chart"""
    return {
        "name": "Line Chart - Professional",
        "chart_type": "line_chart",
        "description": "Professional line chart template",
        "style": {
            "title": "Trend Analysis",
            "subtitle": "Historical Data",
            "title_font": "Inter",
            "title_size": 40,
            "subtitle_font": "Sans Serif",
            "subtitle_size": 20,
            "background_color": [255, 255, 255],
            "text_color": [12, 27, 42],
            "accent_color": [255, 215, 0]
        },
        "colors": {
            "primary_colors": [
                [52, 152, 219], [155, 89, 182], [26, 188, 156], [46, 204, 113]
            ],
            "background": [255, 255, 255],
            "text": [12, 27, 42],
            "grid": [200, 200, 200],
            "accent": [255, 215, 0]
        },
        "layout": {
            "chart_type": "line_chart",
            "aspect_ratio": "16:9",
            "fps": 60,
            "duration": 30,
            "animation_speed": 1.0
        },
        "logo_url": None,
        "data_source": "Data Source: https://www.fao.org/faostat/",
        "show_date": True,
        "show_logo": True,
        "show_data_source": True
    }

@router.get("/defaults/area-chart-full")
async def get_area_chart_full_template():
    """Vrati kompletan default template za Area Chart"""
    return {
        "name": "Area Chart - Professional",
        "chart_type": "area_chart",
        "description": "Professional area chart template",
        "style": {
            "title": "Stacked Area Chart",
            "subtitle": "Cumulative Data",
            "title_font": "Inter",
            "title_size": 40,
            "subtitle_font": "Sans Serif",
            "subtitle_size": 20,
            "background_color": [255, 255, 255],
            "text_color": [12, 27, 42],
            "accent_color": [255, 215, 0]
        },
        "colors": {
            "primary_colors": [
                [39, 174, 96], [142, 68, 173], [230, 126, 34], [231, 76, 60]
            ],
            "background": [255, 255, 255],
            "text": [12, 27, 42],
            "grid": [200, 200, 200],
            "accent": [255, 215, 0]
        },
        "layout": {
            "chart_type": "area_chart",
            "aspect_ratio": "16:9",
            "fps": 60,
            "duration": 30,
            "animation_speed": 1.0
        },
        "logo_url": None,
        "data_source": "Data Source: https://www.fao.org/faostat/",
        "show_date": True,
        "show_logo": True,
        "show_data_source": True
    }

@router.get("/defaults/world-map-full")
async def get_world_map_full_template():
    """Vrati kompletan default template za World Map"""
    return {
        "name": "World Map - Professional",
        "chart_type": "world_map",
        "description": "Professional world map template",
        "style": {
            "title": "Global Distribution",
            "subtitle": "By Country",
            "title_font": "Inter",
            "title_size": 40,
            "subtitle_font": "Sans Serif",
            "subtitle_size": 20,
            "background_color": [255, 255, 255],
            "text_color": [12, 27, 42],
            "accent_color": [255, 215, 0]
        },
        "colors": {
            "primary_colors": [
                [52, 152, 219], [155, 89, 182], [26, 188, 156], [46, 204, 113]
            ],
            "background": [255, 255, 255],
            "text": [12, 27, 42],
            "water": [173, 216, 230],
            "accent": [255, 215, 0]
        },
        "layout": {
            "chart_type": "world_map",
            "aspect_ratio": "16:9",
            "fps": 60,
            "duration": 30,
            "animation_speed": 1.0
        },
        "logo_url": None,
        "data_source": "Data Source: https://www.fao.org/faostat/",
        "show_date": True,
        "show_logo": True,
        "show_data_source": True
    }
