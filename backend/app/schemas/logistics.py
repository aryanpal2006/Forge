from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class SupplierOut(BaseModel):
    id: str
    name: str
    district_id: str
    category: str
    latitude: float
    longitude: float
    contact_phone: Optional[str]
    inventory_data: Dict[str, Any]
    is_active: bool

class FleetVehicleOut(BaseModel):
    id: str
    vehicle_code: str
    vehicle_type: str
    capacity_kg: float
    fuel_level_pct: float
    current_lat: float
    current_lon: float
    status: str
    active_order_id: Optional[str]

class DispatchOrderCreate(BaseModel):
    district_id: str
    supplier_id: str
    destination_village: str
    destination_lat: float
    destination_lon: float
    items_ordered: List[Dict[str, Any]]
    vehicle_id: Optional[str] = None
    total_value_inr: float

class DispatchOrderOut(BaseModel):
    id: str
    tracking_number: str
    district_id: str
    supplier_id: str
    vehicle_id: Optional[str]
    destination_village: str
    destination_lat: float
    destination_lon: float
    items_ordered: List[Dict[str, Any]]
    total_value_inr: float
    status: str
    requires_approval: bool
    is_approved: bool
    route_geojson: Optional[Dict[str, Any]]
    rerouted_count: int
    created_at: datetime

class AuditLogOut(BaseModel):
    id: int
    timestamp: datetime
    trigger_event: str
    district_id: str
    reasoning_text: str
    tool_calls: Optional[List[Dict[str, Any]]]
    action_taken: str
    status: str

class SimulateEventRequest(BaseModel):
    district_id: str # "solapur", "darbhanga", "cuddalore"
    event_type: str # "FLASH_FLOOD", "SEVERE_DROUGHT", "EXTREME_HEATWAVE"
    severity: float = 0.85 # 0.0 to 1.0

