from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class GridCellFeature(BaseModel):
    type: str = "Feature"
    geometry: Dict[str, Any]
    properties: Dict[str, Any]

class RiskGridGeoJSON(BaseModel):
    type: str = "FeatureCollection"
    district_id: str
    district_name: str
    primary_hazard: str
    features: List[GridCellFeature]
    enso_status: Dict[str, Any]
    updated_at: str

class MitigationPlan(BaseModel):
    district_id: str
    primary_risk: str
    urgency_level: str
    recommended_actions: List[str]
    crop_switching_options: List[str]
    insurance_alert: str

