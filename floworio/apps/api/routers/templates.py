"""
Template Router — Upravljanje chart template-ima
Omogućava snimanje, učitavanje i upravljanje template-ima za različite tipove chart-a
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import os
from datetime import datetime

router = APIRouter(prefix="/api/templates", tags=["templates"])

# Template storage directory
TEMPLATES_DIR = "templates"
os.makedirs(TEMPLATES_DIR, exist_ok=True)

class ChartTemplate(BaseModel):
    """Template za chart"""
    name: str
    chart_type: str  # "bar_race", "pie_race", "line_chart", "area_chart", "world_map"
    description: Optional[str] = None
    config: Dict[str, Any]  # Chart-specific configuration
    colors: Optional[Dict[str, tuple]] = None
    styling: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class TemplateResponse(BaseModel):
    """Response za template"""
    id: str
    name: str
    chart_type: str
    description: Optional[str]
    created_at: str
    updated_at: str

@router.post("/save")
async def save_template(template: ChartTemplate):
    """Spremi novi template"""
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
            "message": f"Template '{template.name}' saved successfully",
            "path": template_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_templates(chart_type: Optional[str] = None):
    """Lista svih template-a"""
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
                    "created_at": template_data.get("created_at"),
                    "updated_at": template_data.get("updated_at")
                })
        
        return {"templates": templates, "count": len(templates)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{template_id}")
async def get_template(template_id: str):
    """Učitaj template po ID-u"""
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
async def update_template(template_id: str, template: ChartTemplate):
    """Ažuriraj postojeći template"""
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
            "message": f"Template '{template.name}' updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{template_id}")
async def delete_template(template_id: str):
    """Obriši template"""
    try:
        template_path = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
        
        if not os.path.exists(template_path):
            raise HTTPException(status_code=404, detail="Template not found")
        
        os.remove(template_path)
        
        return {"message": f"Template '{template_id}' deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/defaults/bar-race")
async def get_default_bar_race_template():
    """Vrati default template za Bar Race"""
    return {
        "name": "Default Bar Race",
        "chart_type": "bar_race",
        "description": "Default template for bar race animations",
        "config": {
            "fps": 60,
            "duration": 30,
            "aspect_ratio": "16:9",
            "animation_speed": 1.0
        },
        "colors": {
            "background": (255, 255, 255),
            "text": (12, 27, 42),
            "accent": (255, 215, 0)
        },
        "styling": {
            "title_font": "Inter",
            "title_size": 32,
            "subtitle_font": "Sans Serif",
            "subtitle_size": 18
        }
    }

@router.get("/defaults/pie-race")
async def get_default_pie_race_template():
    """Vrati default template za Pie Race"""
    return {
        "name": "Default Pie Race",
        "chart_type": "pie_race",
        "description": "Default template for pie race animations",
        "config": {
            "fps": 60,
            "duration": 30,
            "aspect_ratio": "1:1",
            "animation_speed": 1.0,
            "pie_size": 0.75,
            "pie_position": "center"
        },
        "colors": {
            "background": (255, 255, 255),
            "text": (12, 27, 42),
            "accent": (255, 215, 0)
        },
        "styling": {
            "title_font": "Inter",
            "title_size": 32,
            "subtitle_font": "Sans Serif",
            "subtitle_size": 18,
            "legend_position": "right"
        }
    }

@router.get("/defaults/line-chart")
async def get_default_line_chart_template():
    """Vrati default template za Line Chart"""
    return {
        "name": "Default Line Chart",
        "chart_type": "line_chart",
        "description": "Default template for line chart animations",
        "config": {
            "fps": 60,
            "duration": 30,
            "aspect_ratio": "16:9",
            "animation_speed": 1.0,
            "grid": True,
            "legend": True
        },
        "colors": {
            "background": (255, 255, 255),
            "text": (12, 27, 42),
            "grid": (200, 200, 200),
            "accent": (255, 215, 0)
        },
        "styling": {
            "title_font": "Inter",
            "title_size": 32,
            "subtitle_font": "Sans Serif",
            "subtitle_size": 18,
            "line_width": 2
        }
    }

@router.get("/defaults/area-chart")
async def get_default_area_chart_template():
    """Vrati default template za Area Chart"""
    return {
        "name": "Default Area Chart",
        "chart_type": "area_chart",
        "description": "Default template for area chart animations",
        "config": {
            "fps": 60,
            "duration": 30,
            "aspect_ratio": "16:9",
            "animation_speed": 1.0,
            "stacked": True,
            "grid": True
        },
        "colors": {
            "background": (255, 255, 255),
            "text": (12, 27, 42),
            "grid": (200, 200, 200),
            "accent": (255, 215, 0)
        },
        "styling": {
            "title_font": "Inter",
            "title_size": 32,
            "subtitle_font": "Sans Serif",
            "subtitle_size": 18,
            "opacity": 0.7
        }
    }

@router.get("/defaults/world-map")
async def get_default_world_map_template():
    """Vrati default template za World Map"""
    return {
        "name": "Default World Map",
        "chart_type": "world_map",
        "description": "Default template for world map animations",
        "config": {
            "fps": 60,
            "duration": 30,
            "aspect_ratio": "16:9",
            "animation_speed": 1.0,
            "projection": "mercator"
        },
        "colors": {
            "background": (255, 255, 255),
            "text": (12, 27, 42),
            "water": (173, 216, 230),
            "accent": (255, 215, 0)
        },
        "styling": {
            "title_font": "Inter",
            "title_size": 32,
            "subtitle_font": "Sans Serif",
            "subtitle_size": 18
        }
    }
