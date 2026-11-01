from typing import Dict, Any, Tuple

class YieldRiskModel:
    """Predicts yield deviation (% deviation from regional baseline) with 90% confidence uncertainty intervals."""

    def predict_yield_deviation(
        self,
        crop: str,
        drought_score: float,
        flood_score: float,
        heat_score: float,
        ndvi_anomaly: float
    ) -> Dict[str, Any]:
        # Sensitivity coefficients per crop
        crop_sensitivities = {
            "soybean": {"drought": 0.42, "flood": 0.28, "heat": 0.30},
            "rice": {"drought": 0.50, "flood": 0.22, "heat": 0.28},
            "cotton": {"drought": 0.30, "flood": 0.35, "heat": 0.35},
            "wheat": {"drought": 0.35, "flood": 0.15, "heat": 0.50},
            "potato": {"drought": 0.25, "flood": 0.50, "heat": 0.25}
        }
        
        weights = crop_sensitivities.get(crop.lower(), {"drought": 0.35, "flood": 0.35, "heat": 0.30})
        
        # Combined compound risk stress factor [0 to 1]
        compound_stress = (
            (drought_score * weights["drought"]) +
            (flood_score * weights["flood"]) +
            (heat_score * weights["heat"])
        )
        
        # Adjust with observed NDVI anomaly
        if ndvi_anomaly < 0:
            compound_stress += abs(ndvi_anomaly) * 0.5
            
        compound_stress = min(1.0, max(0.0, compound_stress))
        
        # Max expected yield decline under catastrophic stress is ~45-55%
        point_deviation_pct = -round(compound_stress * 48.0, 1)
        
        # 90% Confidence Interval: uncertainty widens as compound stress increases
        margin = round(3.5 + (compound_stress * 5.0), 1)
        uncertainty_lower = round(point_deviation_pct - margin, 1)
        uncertainty_upper = round(min(5.0, point_deviation_pct + margin), 1)
        
        # Determine dominant driver
        drivers = [
            ("Moisture Deficit (Drought)", drought_score * weights["drought"]),
            ("Waterlogging / Flash Flood", flood_score * weights["flood"]),
            ("Thermal Heatwave Stress", heat_score * weights["heat"])
        ]
        drivers.sort(key=lambda x: x[1], reverse=True)
        dominant_driver = drivers[0][0]
        
        return {
            "point_deviation_pct": point_deviation_pct,
            "uncertainty_lower": uncertainty_lower,
            "uncertainty_upper": uncertainty_upper,
            "confidence_band_90": f"[{uncertainty_lower}%, {uncertainty_upper}%]",
            "dominant_driver": dominant_driver,
            "compound_stress_index": round(compound_stress, 3)
        }

yield_model = YieldRiskModel()

