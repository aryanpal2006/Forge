from typing import Dict, Any, List

CROP_THERMAL_THRESHOLDS = {
    "wheat": 32.0,
    "soybean": 35.0,
    "cotton": 38.0,
    "rice": 35.0,
    "potato": 30.0
}

class HeatwaveStressModel:
    """Computes crop-specific heat stress index from consecutive thermal exceedance days."""

    def compute_heat_stress(
        self,
        weather_data: Dict[str, Any],
        crop: str = "wheat"
    ) -> float:
        crop_norm = crop.strip().lower()
        threshold = CROP_THERMAL_THRESHOLDS.get(crop_norm, 35.0)
        
        forecast = weather_data.get("forecast_7d", [])
        if not forecast:
            max_t = weather_data.get("max_temp", 33.0)
            exceedance = max(0.0, max_t - threshold)
            return round(min(1.0, exceedance / 6.0), 3)

        exceedance_days = 0
        cumulative_degree_exceedance = 0.0

        for day in forecast:
            day_max = day.get("max_temp", 30.0)
            if day_max > threshold:
                exceedance_days += 1
                cumulative_degree_exceedance += (day_max - threshold)

        # Humidity multiplier: high humidity + high temp increases latent heat stress
        rh = weather_data.get("relative_humidity", 50.0)
        humidity_factor = 1.0 + max(0.0, (rh - 60.0) / 100.0)

        # Base index: 3+ days above threshold triggers high heatwave warning
        day_ratio = exceedance_days / 7.0
        degree_ratio = min(1.0, cumulative_degree_exceedance / 18.0)
        
        raw_stress = ((day_ratio * 0.55) + (degree_ratio * 0.45)) * humidity_factor
        return round(float(min(1.0, max(0.05, raw_stress))), 3)

heatwave_model = HeatwaveStressModel()

