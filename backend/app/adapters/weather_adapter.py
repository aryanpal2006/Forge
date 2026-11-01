import time
import requests
from typing import Dict, Any, Optional

# In-memory cache for weather calls: key -> (timestamp, data)
_WEATHER_CACHE: Dict[str, Any] = {}
CACHE_TTL_SECONDS = 3600 # 1 hour

FALLBACK_WEATHER = {
    "solapur": {
        "district": "Solapur",
        "current_temp": 34.2,
        "max_temp": 38.5,
        "min_temp": 23.1,
        "relative_humidity": 42.0,
        "rainfall_today_mm": 0.0,
        "rainfall_7d_total_mm": 4.5,
        "forecast_7d": [
            {"day": "Day 1", "max_temp": 38.0, "min_temp": 23.0, "rain_mm": 0.0, "humidity": 40},
            {"day": "Day 2", "max_temp": 38.5, "min_temp": 23.5, "rain_mm": 0.0, "humidity": 38},
            {"day": "Day 3", "max_temp": 39.0, "min_temp": 24.0, "rain_mm": 0.0, "humidity": 36},
            {"day": "Day 4", "max_temp": 37.5, "min_temp": 23.0, "rain_mm": 1.2, "humidity": 48},
            {"day": "Day 5", "max_temp": 36.0, "min_temp": 22.5, "rain_mm": 3.3, "humidity": 52},
            {"day": "Day 6", "max_temp": 36.5, "min_temp": 22.0, "rain_mm": 0.0, "humidity": 45},
            {"day": "Day 7", "max_temp": 37.0, "min_temp": 22.8, "rain_mm": 0.0, "humidity": 43}
        ],
        "heatwave_risk": "HIGH",
        "drought_spell_days": 18,
        "source": "NASA POWER / Open-Meteo Cache (Offline Fallback)",
        "is_fallback": True
    },
    "darbhanga": {
        "district": "Darbhanga",
        "current_temp": 27.5,
        "max_temp": 30.2,
        "min_temp": 21.0,
        "relative_humidity": 88.0,
        "rainfall_today_mm": 48.0,
        "rainfall_7d_total_mm": 135.0,
        "forecast_7d": [
            {"day": "Day 1", "max_temp": 29.5, "min_temp": 21.0, "rain_mm": 48.0, "humidity": 88},
            {"day": "Day 2", "max_temp": 29.0, "min_temp": 20.5, "rain_mm": 52.0, "humidity": 92},
            {"day": "Day 3", "max_temp": 30.0, "min_temp": 21.5, "rain_mm": 24.0, "humidity": 84},
            {"day": "Day 4", "max_temp": 31.0, "min_temp": 22.0, "rain_mm": 8.0, "humidity": 78},
            {"day": "Day 5", "max_temp": 31.5, "min_temp": 22.5, "rain_mm": 3.0, "humidity": 72},
            {"day": "Day 6", "max_temp": 32.0, "min_temp": 23.0, "rain_mm": 0.0, "humidity": 68},
            {"day": "Day 7", "max_temp": 32.5, "min_temp": 23.2, "rain_mm": 0.0, "humidity": 65}
        ],
        "flood_alert": "CRITICAL",
        "soil_saturation_pct": 94.0,
        "source": "IMD Gridded Rainfall / Open-Meteo Cache (Offline Fallback)",
        "is_fallback": True
    },
    "cuddalore": {
        "district": "Cuddalore",
        "current_temp": 33.0,
        "max_temp": 36.8,
        "min_temp": 26.4,
        "relative_humidity": 76.0,
        "rainfall_today_mm": 12.0,
        "rainfall_7d_total_mm": 62.0,
        "forecast_7d": [
            {"day": "Day 1", "max_temp": 36.0, "min_temp": 26.0, "rain_mm": 12.0, "humidity": 76},
            {"day": "Day 2", "max_temp": 35.5, "min_temp": 26.2, "rain_mm": 18.0, "humidity": 80},
            {"day": "Day 3", "max_temp": 34.0, "min_temp": 25.5, "rain_mm": 22.0, "humidity": 84},
            {"day": "Day 4", "max_temp": 35.0, "min_temp": 26.0, "rain_mm": 10.0, "humidity": 79},
            {"day": "Day 5", "max_temp": 36.2, "min_temp": 26.5, "rain_mm": 0.0, "humidity": 74},
            {"day": "Day 6", "max_temp": 37.0, "min_temp": 27.0, "rain_mm": 0.0, "humidity": 72},
            {"day": "Day 7", "max_temp": 36.8, "min_temp": 26.8, "rain_mm": 0.0, "humidity": 75}
        ],
        "cyclonic_squall_risk": "MODERATE",
        "heat_index_c": 43.5,
        "source": "Open-Meteo Maritime / Fallback Cache",
        "is_fallback": True
    }
}

class WeatherAdapter:
    """Resilient Weather Adapter querying Open-Meteo with 1-hour cache and instant offline fallback."""

    def __init__(self, timeout_sec: int = 4):
        self.timeout_sec = timeout_sec

    def get_forecast(self, latitude: float, longitude: float, district_hint: str = "solapur") -> Dict[str, Any]:
        cache_key = f"{round(latitude, 2)}_{round(longitude, 2)}"
        now = time.time()
        
        if cache_key in _WEATHER_CACHE:
            timestamp, cached_data = _WEATHER_CACHE[cache_key]
            if now - timestamp < CACHE_TTL_SECONDS:
                return cached_data

        norm_dist = district_hint.strip().lower()
        fallback_data = FALLBACK_WEATHER.get(norm_dist, FALLBACK_WEATHER["solapur"])

        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
                "timezone": "Asia/Kolkata",
                "forecast_days": 7
            }
            resp = requests.get(url, params=params, timeout=self.timeout_sec)
            if resp.status_code == 200:
                data = resp.json()
                current = data.get("current", {})
                daily = data.get("daily", {})
                
                forecast_7d = []
                days = daily.get("time", [])
                max_temps = daily.get("temperature_2m_max", [])
                min_temps = daily.get("temperature_2m_min", [])
                rain_sums = daily.get("precipitation_sum", [])
                
                for idx, day_str in enumerate(days):
                    forecast_7d.append({
                        "day": f"Day {idx + 1}",
                        "date": day_str,
                        "max_temp": max_temps[idx] if idx < len(max_temps) else 32.0,
                        "min_temp": min_temps[idx] if idx < len(min_temps) else 22.0,
                        "rain_mm": rain_sums[idx] if idx < len(rain_sums) else 0.0,
                        "humidity": current.get("relative_humidity_2m", 60)
                    })
                
                rain_7d = sum(rain_sums) if rain_sums else 0.0
                
                result = {
                    "district": district_hint.capitalize(),
                    "current_temp": current.get("temperature_2m", 30.0),
                    "max_temp": max_temps[0] if max_temps else 32.0,
                    "min_temp": min_temps[0] if min_temps else 22.0,
                    "relative_humidity": current.get("relative_humidity_2m", 60.0),
                    "rainfall_today_mm": rain_sums[0] if rain_sums else 0.0,
                    "rainfall_7d_total_mm": round(rain_7d, 1),
                    "wind_speed_kmh": current.get("wind_speed_10m", 12.0),
                    "forecast_7d": forecast_7d,
                    "source": "Open-Meteo Live API",
                    "is_fallback": False,
                    "cached_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
                }
                _WEATHER_CACHE[cache_key] = (now, result)
                return result
        except Exception:
            pass # Network error, SSL, timeout -> gracefully fall through to bundled fallback
            
        # Return fallback with timestamp
        res = dict(fallback_data)
        res["cached_at"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
        _WEATHER_CACHE[cache_key] = (now, res)
        return res

weather_adapter = WeatherAdapter()

