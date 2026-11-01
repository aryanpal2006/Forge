import math
from typing import Dict, Any

class DroughtRiskModel:
    """Computes drought probability index (30-day horizon) combining SPI, soil moisture, and NDVI."""

    def compute_drought_risk(
        self,
        district_id: str,
        weather_data: Dict[str, Any],
        soil_data: Dict[str, Any],
        ndvi_data: Dict[str, Any],
        enso_data: Dict[str, Any]
    ) -> float:
        # 1. Rainfall deficit factor
        # Baseline expected 30-day rainfall for region
        baseline_rain_30d = 85.0 if district_id == "solapur" else (160.0 if district_id == "darbhanga" else 110.0)
        forecast_7d_rain = weather_data.get("rainfall_7d_total_mm", 0.0)
        projected_30d_rain = forecast_7d_rain * 3.5 # Extrapolate 30d
        
        rain_deficit_ratio = max(0.0, (baseline_rain_30d - projected_30d_rain) / baseline_rain_30d)
        
        # 2. Consecutive dry spell factor
        dry_spell_days = weather_data.get("drought_spell_days", 0)
        dry_spell_factor = min(1.0, dry_spell_days / 21.0)
        
        # 3. NDVI vegetation stress anomaly
        ndvi_anomaly = ndvi_data.get("ndvi_anomaly", 0.0)
        ndvi_stress_factor = max(0.0, min(1.0, (-ndvi_anomaly) * 4.0)) if ndvi_anomaly < 0 else 0.0
        
        # 4. Soil water holding capacity buffer
        # High clay Vertisols buffer early drought, sandy soils succumb faster
        clay_pct = soil_data.get("clay_content_pct", 30.0)
        soil_buffer = 1.0 - (clay_pct / 120.0) # Vertisols (~50% clay) gives ~0.58 multiplier
        
        # 5. ENSO El Nino regional vulnerability multiplier
        el_nino_vuln = enso_data.get("regional_impact", {}).get("el_nino_drought_prob", 0.5)
        enso_weight = 1.15 if "el niño" in enso_data.get("current_phase", "").lower() else 1.0
        
        raw_score = (
            (rain_deficit_ratio * 0.40) +
            (dry_spell_factor * 0.25) +
            (ndvi_stress_factor * 0.25) +
            (el_nino_vuln * 0.10)
        ) * soil_buffer * enso_weight
        
        # Sigmoid calibration to bound within [0.0, 1.0]
        calibrated_score = 1.0 / (1.0 + math.exp(-6.0 * (raw_score - 0.45)))
        return round(float(max(0.05, min(0.98, calibrated_score))), 3)

drought_model = DroughtRiskModel()

