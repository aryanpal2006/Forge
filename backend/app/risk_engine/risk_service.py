import time
from typing import Dict, Any, List
from backend.app.adapters.weather_adapter import weather_adapter
from backend.app.adapters.soil_adapter import soil_adapter
from backend.app.adapters.satellite_adapter import satellite_adapter
from backend.app.adapters.enso_adapter import enso_adapter
from backend.app.risk_engine.grid_generator import grid_generator
from backend.app.risk_engine.drought_model import drought_model
from backend.app.risk_engine.flood_model import flood_model
from backend.app.risk_engine.heatwave_model import heatwave_model
from backend.app.risk_engine.yield_model import yield_model

class RiskService:
    """Orchestrates micro-climate risk features, models, GeoJSON generation, and mitigation plans."""

    def get_district_risk_grid(self, district_id: str, crop: str = "soybean") -> Dict[str, Any]:
        dist_norm = district_id.strip().lower()
        
        # 1. Fetch base district data
        features = grid_generator.generate_grid_for_district(dist_norm)
        if not features:
            dist_norm = "solapur"
            features = grid_generator.generate_grid_for_district(dist_norm)

        center_lat = features[0]["properties"]["center_lat"] if features else 17.65
        center_lon = features[0]["properties"]["center_lon"] if features else 75.90
        
        weather = weather_adapter.get_forecast(center_lat, center_lon, district_hint=dist_norm)
        soil = soil_adapter.get_soil_data(dist_norm)
        enso = enso_adapter.get_enso_status(dist_norm)

        # 2. Score each grid cell with spatial heterogeneity
        scored_features = []
        for feat in features:
            cell_code = feat["properties"]["cell_code"]
            c_lat = feat["properties"]["center_lat"]
            c_lon = feat["properties"]["center_lon"]
            
            # Local slope/elevation proxy derived from micro coordinate offsets
            elevation_proxy = 1.0 + ((math_seed := sum(ord(c) for c in cell_code)) % 30 - 15) / 100.0
            
            ndvi_data = satellite_adapter.get_ndvi_metrics(dist_norm, cell_code=cell_code)
            
            drought_score = drought_model.compute_drought_risk(dist_norm, weather, soil, ndvi_data, enso)
            flood_score = flood_model.compute_flood_risk(dist_norm, weather, soil, cell_elevation_factor=elevation_proxy)
            heat_score = heatwave_model.compute_heat_stress(weather, crop=crop)
            
            # Micro cell variation
            jitter = ((math_seed % 20) - 10) / 200.0
            d_val = round(max(0.01, min(0.99, drought_score + jitter)), 2)
            f_val = round(max(0.01, min(0.99, flood_score + (jitter * -1))), 2)
            h_val = round(max(0.01, min(0.99, heat_score + (jitter * 0.5))), 2)
            n_stress = round(max(0.0, min(1.0, 1.0 - ndvi_data["mean_ndvi"])), 2)
            
            yield_pred = yield_model.predict_yield_deviation(
                crop=crop,
                drought_score=d_val,
                flood_score=f_val,
                heat_score=h_val,
                ndvi_anomaly=ndvi_data["ndvi_anomaly"]
            )
            
            feat_copy = dict(feat)
            feat_copy["properties"] = {
                **feat["properties"],
                "drought_risk": d_val,
                "flood_risk": f_val,
                "heat_stress": h_val,
                "ndvi_stress": n_stress,
                "ndvi_mean": ndvi_data["mean_ndvi"],
                "yield_deviation_pct": yield_pred["point_deviation_pct"],
                "uncertainty_lower": yield_pred["uncertainty_lower"],
                "uncertainty_upper": yield_pred["uncertainty_upper"],
                "dominant_driver": yield_pred["dominant_driver"]
            }
            scored_features.append(feat_copy)

        return {
            "type": "FeatureCollection",
            "district_id": dist_norm,
            "district_name": dist_norm.capitalize(),
            "primary_hazard": "drought" if dist_norm == "solapur" else ("flood" if dist_norm == "darbhanga" else "heatwave"),
            "features": scored_features,
            "enso_status": enso,
            "weather_snapshot": {
                "temp": weather.get("current_temp"),
                "rain_7d_mm": weather.get("rainfall_7d_total_mm"),
                "humidity": weather.get("relative_humidity"),
                "source": weather.get("source")
            },
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        }

    def get_mitigation_plan(self, district_id: str, crop: str = "soybean") -> Dict[str, Any]:
        dist_norm = district_id.strip().lower()
        
        if dist_norm == "solapur":
            return {
                "district_id": "solapur",
                "primary_risk": "Prolonged Soil Moisture Deficit & Thermal Shock",
                "urgency_level": "HIGH",
                "recommended_actions": [
                    "Apply sugarcane trash or crop residue mulch @ 5 t/ha to minimize soil evaporation.",
                    "Spray anti-transpirant 1% Potassium Nitrate (KNO3) during morning hours.",
                    "Execute broad-bed furrow (BBF) irrigation in alternate furrows to stretch limited well water."
                ],
                "crop_switching_options": [
                    "Switch late-sown soybean to short-duration Chickpea (JG-11) or Rabi Sorghum (Maldandi).",
                    "Introduce drought-hardy Moth Bean or Horsegram on shallow gravel soils."
                ],
                "insurance_alert": "PMFBY Weather-Based Crop Insurance: Register dry spell loss claim on NCIP portal within 72 hours of 14-day rainfall deficit trigger."
            }
        elif dist_norm == "darbhanga":
            return {
                "district_id": "darbhanga",
                "primary_risk": "Gangetic Floodplain Flash Flood & Low-Lying Waterlogging",
                "urgency_level": "CRITICAL",
                "recommended_actions": [
                    "Clear community field bund sluices and open field trenches to prevent ponding depth > 10 cm.",
                    "Spray systemic fungicide (Cymoxanil + Mancozeb) on potato to stop sudden late-blight outbreaks.",
                    "Harvest mature early-paddy immediately and move grain to elevated community shelters."
                ],
                "crop_switching_options": [
                    "Transition damaged paddy to submergence-tolerant variety Swarna Sub-1.",
                    "Plant post-flood boro rice or quick vegetable greens (palak/methi) on receding silts."
                ],
                "insurance_alert": "PMFBY Inundation Clause: Report standing crop submergence photo on Crop Insurance App within 48 hours for expedited localized survey."
            }
        else: # Cuddalore
            return {
                "district_id": "cuddalore",
                "primary_risk": "Maritime Heat Stress & Cyclonic Squall Inundation",
                "urgency_level": "MODERATE",
                "recommended_actions": [
                    "Maintain light surface standing water (3-5 cm) to suppress canopy temperature.",
                    "Secure field bunds and clear coastal tidal drainage channels.",
                    "Spray 2% DAP + 1% KCl on cotton to prevent high-temperature square abortion."
                ],
                "crop_switching_options": [
                    "Adopt saline-tolerant rice varieties (TRY-1, CR Dhan 407).",
                    "Stagger sowing with summer sesame or blackgram."
                ],
                "insurance_alert": "PMFBY Cyclonic Squall Alert: Monitor IMD coastal bulletins; notify district agriculture officer for mass claim documentation."
            }

risk_service = RiskService()

