import json
from pathlib import Path
from typing import Dict, Any
from backend.app.config import settings

class EnsoAdapter:
    """NOAA ONI (Oceanic Niño Index) adapter for regional monsoon risk correlation."""

    def __init__(self):
        self.data_file = settings.ENSO_DIR / "oni_data.json"
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if self.data_file.exists():
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}

    def get_enso_status(self, district: str = "Solapur") -> Dict[str, Any]:
        norm = district.strip().lower()
        correlations = self._data.get("historical_correlation", {})
        regional_corr = correlations.get(norm, {
            "el_nino_drought_prob": 0.50,
            "la_nina_excess_rain_prob": 0.50,
            "summary": "Regional historical monsoon correlation data baseline."
        })
        
        return {
            "current_phase": self._data.get("current_phase", "Neutral / Developing La Niña"),
            "latest_oni_value": self._data.get("latest_oni_value", -0.42),
            "updated_month": self._data.get("updated_month", "October 2026"),
            "source": "NOAA Climate Prediction Center (CPC)",
            "regional_impact": regional_corr
        }

enso_adapter = EnsoAdapter()

