import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from backend.app.config import settings

class MockServicesManager:
    """Manages mock microservices for suppliers, fleet telemetry, and road network."""

    def __init__(self):
        self._suppliers: List[Dict[str, Any]] = []
        self._fleet: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        supp_file = settings.SEED_DATA_DIR / "suppliers.json"
        if supp_file.exists():
            with open(supp_file, "r", encoding="utf-8") as f:
                self._suppliers = json.load(f)

        fleet_file = settings.SEED_DATA_DIR / "fleet.json"
        if fleet_file.exists():
            with open(fleet_file, "r", encoding="utf-8") as f:
                self._fleet = json.load(f)

    def list_suppliers(self, district_id: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
        results = self._suppliers
        if district_id:
            results = [s for s in results if s.get("district_id") == district_id.lower()]
        if category:
            results = [s for s in results if s.get("category") == category.lower()]
        return results

    def get_supplier(self, supplier_id: str) -> Optional[Dict[str, Any]]:
        for s in self._suppliers:
            if s.get("id") == supplier_id:
                return s
        return None

    def find_supplier_for_item(self, item_keyword: str, district_id: str) -> Optional[Dict[str, Any]]:
        kw = item_keyword.lower()
        district_suppliers = self.list_suppliers(district_id=district_id)
        
        # Priority match within district
        for s in district_suppliers:
            cat = s.get("category", "").lower()
            inv = json.dumps(s.get("inventory_data", {})).lower()
            if kw in cat or kw in inv:
                return s
                
        # Fallback to any active supplier in district
        if district_suppliers:
            return district_suppliers[0]
            
        return self._suppliers[0] if self._suppliers else None

    def list_fleet(self, district_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        results = self._fleet
        if district_id:
            results = [v for v in results if v.get("district_id") == district_id.lower()]
        if status:
            results = [v for v in results if v.get("status") == status.lower()]
        return results

    def get_vehicle(self, vehicle_id: str) -> Optional[Dict[str, Any]]:
        for v in self._fleet:
            if v.get("id") == vehicle_id:
                return v
        return None

    def update_vehicle_status(self, vehicle_id: str, status: str, current_lat: Optional[float] = None, current_lon: Optional[float] = None, order_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        for v in self._fleet:
            if v.get("id") == vehicle_id:
                v["status"] = status
                if current_lat is not None:
                    v["current_lat"] = current_lat
                if current_lon is not None:
                    v["current_lon"] = current_lon
                if order_id is not None:
                    v["active_order_id"] = order_id
                return v
        return None

mock_services = MockServicesManager()

