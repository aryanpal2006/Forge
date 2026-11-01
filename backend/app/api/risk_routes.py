from fastapi import APIRouter, Query
from typing import Dict, Any, Optional
from backend.app.risk_engine.risk_service import risk_service
from backend.app.adapters.enso_adapter import enso_adapter

router = APIRouter(prefix="/risk", tags=["Risk Engine"])

@router.get("/grid")
def get_risk_grid(
    district: str = Query("solapur", description="District ID: solapur, darbhanga, or cuddalore"),
    crop: str = Query("soybean", description="Crop: soybean, rice, cotton, wheat, potato")
):
    return risk_service.get_district_risk_grid(district_id=district, crop=crop)

@router.get("/summary")
def get_risk_summary(district: str = Query("solapur")):
    grid = risk_service.get_district_risk_grid(district_id=district)
    enso = enso_adapter.get_enso_status(district)
    
    # Calculate district aggregated metrics
    features = grid.get("features", [])
    n = len(features) or 1
    avg_drought = sum(f["properties"].get("drought_risk", 0.0) for f in features) / n
    avg_flood = sum(f["properties"].get("flood_risk", 0.0) for f in features) / n
    avg_heat = sum(f["properties"].get("heat_stress", 0.0) for f in features) / n
    avg_yield_dev = sum(f["properties"].get("yield_deviation_pct", 0.0) for f in features) / n

    return {
        "district_id": district.lower(),
        "district_name": district.capitalize(),
        "primary_hazard": grid.get("primary_hazard"),
        "aggregated_metrics": {
            "drought_risk": round(avg_drought, 2),
            "flood_risk": round(avg_flood, 2),
            "heat_stress": round(avg_heat, 2),
            "mean_yield_deviation_pct": round(avg_yield_dev, 1)
        },
        "weather_snapshot": grid.get("weather_snapshot"),
        "enso_status": enso,
        "grid_cells_count": len(features),
        "updated_at": grid.get("updated_at")
    }

@router.get("/mitigation")
def get_mitigation_plan(
    district: str = Query("solapur"),
    crop: str = Query("soybean")
):
    return risk_service.get_mitigation_plan(district_id=district, crop=crop)

