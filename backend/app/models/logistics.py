from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from backend.app.database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(String(50), primary_key=True) # e.g. "supp_solapur_seed_01"
    name = Column(String(150), nullable=False)
    district_id = Column(String(50), nullable=False, index=True)
    category = Column(String(50), nullable=False) # "seeds", "fodder", "water", "equipment", "tarpaulins", "medicines"
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    contact_phone = Column(String(20), nullable=True)
    # inventory dictionary: e.g. {"certified_seeds_kg": 5000, "unit_price_inr": 80}
    inventory_data = Column(JSON, nullable=False, default=dict)
    is_active = Column(Boolean, default=True)

class FleetVehicle(Base):
    __tablename__ = "fleet_vehicles"

    id = Column(String(50), primary_key=True) # e.g. "VEH-TN-01"
    vehicle_code = Column(String(50), unique=True, nullable=False)
    vehicle_type = Column(String(50), nullable=False) # "Water Tanker", "4x4 Relief Truck", "Emergency Van", "Tractor"
    capacity_kg = Column(Float, nullable=False)
    fuel_level_pct = Column(Float, default=100.0)
    current_lat = Column(Float, nullable=False)
    current_lon = Column(Float, nullable=False)
    status = Column(String(30), default="idle") # "idle", "dispatched", "in_transit", "returning", "maintenance"
    active_order_id = Column(String(50), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DispatchOrder(Base):
    __tablename__ = "dispatch_orders"

    id = Column(String(50), primary_key=True) # e.g. "ORD-20261031-001"
    tracking_number = Column(String(100), unique=True, nullable=False)
    district_id = Column(String(50), nullable=False)
    supplier_id = Column(String(50), nullable=False)
    vehicle_id = Column(String(50), nullable=True)
    destination_village = Column(String(100), nullable=False)
    destination_lat = Column(Float, nullable=False)
    destination_lon = Column(Float, nullable=False)
    
    items_ordered = Column(JSON, nullable=False) # [{"item": "certified_seeds", "qty": 500, "unit": "kg", "value_inr": 40000}]
    total_value_inr = Column(Float, default=0.0)
    
    status = Column(String(30), default="pending_approval") # "pending_approval", "dispatched", "in_transit", "delivered", "cancelled"
    requires_approval = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True)
    
    route_geojson = Column(JSON, nullable=True)
    rerouted_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    trigger_event = Column(String(100), nullable=False) # e.g. "FLASH_FLOOD_SIMULATION", "SCHEDULED_MONITOR"
    district_id = Column(String(50), nullable=False)
    reasoning_text = Column(Text, nullable=False)
    tool_calls = Column(JSON, nullable=True) # list of tools invoked with parameters and results
    action_taken = Column(String(200), nullable=False)
    status = Column(String(30), default="SUCCESS")

