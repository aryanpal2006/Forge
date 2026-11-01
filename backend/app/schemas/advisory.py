from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AdvisoryRequest(BaseModel):
    farmer_id: Optional[int] = None
    district: str = Field(..., example="Solapur")
    village: Optional[str] = Field("Mohol", example="Mohol")
    crop_type: str = Field(..., example="soybean") # rice, wheat, cotton, soybean, potato
    crop_stage: Optional[str] = Field("Vegetative", example="Pod formation")
    soil_type: Optional[str] = Field("Black", example="Black")
    irrigation_type: Optional[str] = Field("Rainfed", example="Rainfed")
    language: str = Field("en", example="mr") # en, hi, bn, mr, ta, te
    query_text: Optional[str] = Field(None, example="Should I irrigate this week given the heat forecast?")

class ActionDayCard(BaseModel):
    day_range: str # e.g. "Day 1-2", "Day 3-4", "Day 5-7"
    action: str
    urgency: str # "low", "medium", "critical"

class MandiSignal(BaseModel):
    crop: str
    current_modal_price: float # INR / Quintal
    price_trend: str # "upward", "downward", "stable"
    signal: str # "HOLD", "SELL_NOW", "GRADUAL_SELL"
    rationale: str
    data_source: str # "data.gov.in Agmarknet (Verified)"

class AdvisoryResponse(BaseModel):
    spoken_advisory: str # Max ~80 words, spoken friendly, in selected language
    english_translation: Optional[str] = None # For judge audit if language is non-English
    why_rationale: str # One-line explanation
    confidence_level: float # e.g. 0.92
    confidence_label: str # "High (92%)"
    rule_cited: str # e.g. "ICAR-SOY-DRG-04 (Soil Moisture Stress Prevention)"
    next_7_days: List[ActionDayCard]
    mandi_signal: MandiSignal
    weather_summary: Dict[str, Any]
    provenance: Dict[str, str] # e.g. {"weather": "Open-Meteo Live", "mandi": "Agmarknet", "icar": "ICAR-Kisan 2024"}

