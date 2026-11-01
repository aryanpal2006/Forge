import pytest
from backend.app.adapters.weather_adapter import weather_adapter
from backend.app.adapters.mandi_adapter import mandi_adapter
from backend.app.adapters.soil_adapter import soil_adapter
from backend.app.adapters.satellite_adapter import satellite_adapter
from backend.app.adapters.enso_adapter import enso_adapter

def test_weather_adapter_fallback_and_cache():
    # Solapur coordinates
    res = weather_adapter.get_forecast(17.6599, 75.9064, district_hint="solapur")
    assert "current_temp" in res
    assert "rainfall_7d_total_mm" in res
    assert len(res["forecast_7d"]) == 7
    assert res["max_temp"] >= res["min_temp"]

def test_mandi_adapter_signals():
    res = mandi_adapter.get_price_info("soybean", district="Solapur")
    assert res["commodity"] == "Soybean"
    assert res["modal_price"] > 0
    assert res["signal"] in ["HOLD", "SELL_NOW", "GRADUAL_SELL"]
    assert "Agmarknet" in res["data_source"]

def test_soil_adapter_profiles():
    res = soil_adapter.get_soil_data("solapur")
    assert "Vertisol" in res["soil_name"]
    assert res["clay_content_pct"] > 40.0
    assert res["ph"] > 7.0

def test_satellite_adapter_ndvi():
    res = satellite_adapter.get_ndvi_metrics("darbhanga")
    assert 0.0 <= res["mean_ndvi"] <= 1.0
    assert "Sentinel-2" in res["sensor"]

def test_enso_adapter_oni():
    res = enso_adapter.get_enso_status("solapur")
    assert "current_phase" in res
    assert "latest_oni_value" in res
    assert "el_nino_drought_prob" in res["regional_impact"]

