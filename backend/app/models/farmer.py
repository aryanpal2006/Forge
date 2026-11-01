from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.app.database import Base

class FarmerProfile(Base):
    __tablename__ = "farmer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    language = Column(String(10), default="en") # en, hi, bn, mr, ta, te
    district = Column(String(100), nullable=False) # e.g. "Solapur", "Darbhanga", "Cuddalore"
    village = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    crop_type = Column(String(50), nullable=False) # rice, wheat, cotton, soybean, potato
    land_size_acres = Column(Float, default=2.5)
    soil_type = Column(String(50), default="Alluvial") # Black, Alluvial, Red, Sandy Loam, Clay
    irrigation_type = Column(String(50), default="Rainfed") # Rainfed, Canal, Borewell, Drip/Sprinkler
    created_at = Column(DateTime, default=datetime.utcnow)

