import json
import math
from typing import List, Dict, Any
from backend.app.config import settings

class GridGenerator:
    """Generates ~2-3 km micro-location grid cells (GeoJSON) covering the 3 demo districts."""

    def __init__(self):
        self.districts_file = settings.SEED_DATA_DIR / "districts.json"
        self._districts: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if self.districts_file.exists():
            with open(self.districts_file, "r", encoding="utf-8") as f:
                self._districts = json.load(f)

    def generate_grid_for_district(self, district_id: str, step_deg: float = 0.05) -> List[Dict[str, Any]]:
        """Generates ~3-5km cells across the bounding box (0.05 deg ~ 5.5 km)."""
        dist = None
        for d in self._districts:
            if d["id"] == district_id.lower():
                dist = d
                break
                
        if not dist:
            return []

        bbox = dist["bbox"] # [min_lon, min_lat, max_lon, max_lat]
        min_lon, min_lat, max_lon, max_lat = bbox

        features = []
        cell_idx = 1
        
        lat = min_lat
        while lat < max_lat:
            lon = min_lon
            while lon < max_lon:
                c_min_lat = round(lat, 4)
                c_max_lat = round(lat + step_deg, 4)
                c_min_lon = round(lon, 4)
                c_max_lon = round(lon + step_deg, 4)
                center_lat = round((c_min_lat + c_max_lat) / 2.0, 4)
                center_lon = round((c_min_lon + c_max_lon) / 2.0, 4)
                
                cell_code = f"{district_id}_{cell_idx:02d}"
                
                # GeoJSON Polygon coordinates: [[ [lon, lat], [lon, lat], ... ]]
                polygon_coords = [
                    [c_min_lon, c_min_lat],
                    [c_max_lon, c_min_lat],
                    [c_max_lon, c_max_lat],
                    [c_min_lon, c_max_lat],
                    [c_min_lon, c_min_lat]
                ]
                
                feature = {
                    "type": "Feature",
                    "id": cell_code,
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [polygon_coords]
                    },
                    "properties": {
                        "cell_code": cell_code,
                        "district_id": district_id,
                        "district_name": dist["name"],
                        "center_lat": center_lat,
                        "center_lon": center_lon,
                        "min_lat": c_min_lat,
                        "min_lon": c_min_lon,
                        "max_lat": c_max_lat,
                        "max_lon": c_max_lon
                    }
                }
                features.append(feature)
                cell_idx += 1
                lon += step_deg
            lat += step_deg
            
        return features

grid_generator = GridGenerator()

