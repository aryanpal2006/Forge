from typing import Dict, Any, Optional

DISTRICT_SOIL_PROFILES = {
    "solapur": {
        "soil_name": "Deep Black Cotton Soil (Vertisol)",
        "ph": 8.1,
        "organic_carbon_g_kg": 5.4, # Low-Medium
        "clay_content_pct": 52.0, # High clay -> high water holding, crack formation
        "sand_content_pct": 18.0,
        "silt_content_pct": 30.0,
        "nitrogen_status": "Low (160 kg/ha)",
        "phosphorus_status": "Low to Medium (14 kg/ha)",
        "potassium_status": "High (340 kg/ha)",
        "drainage_class": "Poor internal drainage, high swell-shrink",
        "water_retention_capacity_mm_m": 190.0,
        "source": "SoilGrids / ICAR-NBSS&LUP Regional Profile"
    },
    "darbhanga": {
        "soil_name": "Calcareous Alluvial Silt Loam (Inceptisol/Entisol)",
        "ph": 7.4,
        "organic_carbon_g_kg": 6.8,
        "clay_content_pct": 24.0,
        "sand_content_pct": 28.0,
        "silt_content_pct": 48.0, # High silt -> fertile, prone to waterlogging
        "nitrogen_status": "Medium (230 kg/ha)",
        "phosphorus_status": "Medium (22 kg/ha)",
        "potassium_status": "Medium (190 kg/ha)",
        "drainage_class": "Moderate surface, high regional water table",
        "water_retention_capacity_mm_m": 155.0,
        "source": "SoilGrids / RAU Pusa Soil Health Survey"
    },
    "cuddalore": {
        "soil_name": "Coastal Deltaic Sandy Clay Loam (Alfisol)",
        "ph": 7.8,
        "organic_carbon_g_kg": 4.2,
        "clay_content_pct": 32.0,
        "sand_content_pct": 50.0,
        "silt_content_pct": 18.0,
        "nitrogen_status": "Low (145 kg/ha)",
        "phosphorus_status": "Medium (18 kg/ha)",
        "potassium_status": "Medium to High (260 kg/ha)",
        "drainage_class": "Moderate to rapid, susceptible to coastal salinity intrusion",
        "water_retention_capacity_mm_m": 120.0,
        "source": "SoilGrids / TNAU Soil Resources Database"
    }
}

class SoilAdapter:
    """SoilGrids Adapter with regional baseline profiles and fallback data."""

    def get_soil_data(self, district: str = "Solapur", user_soil_override: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        norm = district.strip().lower()
        profile = dict(DISTRICT_SOIL_PROFILES.get(norm, DISTRICT_SOIL_PROFILES["solapur"]))
        
        # Merge any user entered field overrides
        if user_soil_override:
            for k, v in user_soil_override.items():
                if v is not None:
                    profile[k] = v
            profile["source"] = "User Tested Soil Card + SoilGrids Profile"
            
        return profile

soil_adapter = SoilAdapter()

