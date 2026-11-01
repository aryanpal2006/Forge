import math
from typing import Dict, Any

class FlashFloodRiskModel:
    """Computes flash-flood and waterlogging risk per grid cell using rainfall intensity and slope proxy."""

    def compute_flood_risk(
        self,
        district_id: str,
        weather_data: Dict[str, Any],
        soil_data: Dict[str, Any],
        cell_elevation_factor: float = 1.0
    ) -> float:
        # 1. Rainfall intensity factor
        today_rain = weather_data.get("rainfall_today_mm", 0.0)
        week_rain = weather_data.get("rainfall_7d_total_mm", 0.0)
        
        # Flash flood alert threshold in plains: >50mm/day or >120mm/week
        intensity_score = min(1.0, (today_rain / 60.0) * 0.65 + (week_rain / 140.0) * 0.35)
        
        # 2. Regional floodplain / terrain factor
        # Darbhanga Kosi basin has extreme low-gradient drainage; Solapur has rolling plateau
        if district_id == "darbhanga":
            terrain_vulnerability = 1.45
        elif district_id == "cuddalore":
            terrain_vulnerability = 1.20
        else: # Solapur
            terrain_vulnerability = 0.60
            
        # 3. Soil drainage impedance factor
        drainage_class = soil_data.get("drainage_class", "").lower()
        if "poor" in drainage_class or "silt" in drainage_class:
            soil_impedance = 1.25
        else:
            soil_impedance = 0.95
            
        raw_flood = intensity_score * terrain_vulnerability * soil_impedance * cell_elevation_factor
        
        # Bounded between 0.0 and 1.0
        score = 1.0 / (1.0 + math.exp(-7.0 * (raw_flood - 0.50)))
        return round(float(max(0.02, min(0.99, score))), 3)

flood_model = FlashFloodRiskModel()

