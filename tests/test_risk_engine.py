import pytest
from backend.app.risk_engine.grid_generator import grid_generator
from backend.app.risk_engine.drought_model import drought_model
from backend.app.risk_engine.flood_model import flood_model
from backend.app.risk_engine.heatwave_model import heatwave_model
from backend.app.risk_engine.yield_model import yield_model
from backend.app.risk_engine.risk_service import risk_service

def test_grid_generator():
    cells = grid_generator.generate_grid_for_district("solapur")
    assert len(cells) > 5
    assert cells[0]["geometry"]["type"] == "Polygon"
    assert "cell_code" in cells[0]["properties"]

def test_drought_model_range():
    weather = {"rainfall_7d_total_mm": 2.0, "drought_spell_days": 15}
    soil = {"clay_content_pct": 50.0}
    ndvi = {"ndvi_anomaly": -0.15}
    enso = {"regional_impact": {"el_nino_drought_prob": 0.65}}
    
    score = drought_model.compute_drought_risk("solapur", weather, soil, ndvi, enso)
    assert 0.0 <= score <= 1.0
    assert score > 0.4 # Under severe deficit, score should be elevated

def test_flood_model_range():
    weather = {"rainfall_today_mm": 65.0, "rainfall_7d_total_mm": 140.0}
    soil = {"drainage_class": "poor silt"}
    
    score = flood_model.compute_flood_risk("darbhanga", weather, soil)
    assert 0.0 <= score <= 1.0
    assert score > 0.6 # High rainfall in flood plain yields high flood risk

def test_yield_model_uncertainty_bounds():
    pred = yield_model.predict_yield_deviation("soybean", 0.75, 0.20, 0.40, -0.12)
    assert pred["point_deviation_pct"] < 0 # Negative yield impact
    assert pred["uncertainty_lower"] < pred["point_deviation_pct"]
    assert pred["uncertainty_upper"] > pred["point_deviation_pct"]
    assert "dominant_driver" in pred

def test_full_risk_service_geojson():
    res = risk_service.get_district_risk_grid("darbhanga", crop="rice")
    assert res["type"] == "FeatureCollection"
    assert len(res["features"]) > 0
    props = res["features"][0]["properties"]
    assert "flood_risk" in props
    assert "yield_deviation_pct" in props

