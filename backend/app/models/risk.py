from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base

class District(Base):
    __tablename__ = "districts"

    id = Column(String(50), primary_key=True) # "solapur", "darbhanga", "cuddalore"
    name = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    center_lat = Column(Float, nullable=False)
    center_lon = Column(Float, nullable=False)
    agro_zone = Column(String(100), nullable=False) # e.g. "Semi-Arid Deccan", "Gangetic Plain", "Eastern Coastal"
    primary_hazard = Column(String(50), nullable=False) # "drought", "flood", "heatwave"
    description = Column(Text, nullable=True)

    grid_cells = relationship("RiskGridCell", back_populates="district_rel", cascade="all, delete-orphan")

class RiskGridCell(Base):
    __tablename__ = "risk_grid_cells"

    id = Column(String(100), primary_key=True) # e.g. "solapur_cell_01"
    district_id = Column(String(50), ForeignKey("districts.id"), nullable=False, index=True)
    cell_code = Column(String(50), nullable=False)
    min_lat = Column(Float, nullable=False)
    min_lon = Column(Float, nullable=False)
    max_lat = Column(Float, nullable=False)
    max_lon = Column(Float, nullable=False)
    center_lat = Column(Float, nullable=False)
    center_lon = Column(Float, nullable=False)
    
    # Risk indices [0.0 to 1.0]
    drought_index = Column(Float, default=0.0)
    flood_risk = Column(Float, default=0.0)
    heatwave_stress = Column(Float, default=0.0)
    ndvi_stress = Column(Float, default=0.0)
    
    # Yield deviation percent (e.g. -18.5%)
    yield_deviation_pct = Column(Float, default=0.0)
    uncertainty_lower = Column(Float, default=0.0)
    uncertainty_upper = Column(Float, default=0.0)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    district_rel = relationship("District", back_populates="grid_cells")

