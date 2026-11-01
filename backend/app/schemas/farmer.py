from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class FarmerProfileCreate(BaseModel):
    name: str = Field(..., example="Ramesh Patil")
    phone: Optional[str] = Field(None, example="+91 9876543210")
    language: str = Field("en", example="mr")
    district: str = Field(..., example="Solapur")
    village: str = Field(..., example="Mohol")
    latitude: float = Field(..., example=17.7000)
    longitude: float = Field(..., example=75.8000)
    crop_type: str = Field(..., example="soybean")
    land_size_acres: float = Field(2.5, example=3.0)
    soil_type: str = Field("Black", example="Black")
    irrigation_type: str = Field("Rainfed", example="Rainfed")

class FarmerProfileOut(FarmerProfileCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

