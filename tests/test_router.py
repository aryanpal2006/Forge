import pytest
from backend.app.logistics.router import road_router

def test_road_router_basic_path():
    route = road_router.compute_safe_route(
        district_id="darbhanga",
        origin_node="Darbhanga_Center",
        dest_node="Kalyanpur_Village"
    )
    assert len(route["path_nodes"]) >= 2
    assert route["distance_km"] > 0
    assert route["is_rerouted"] is False

def test_road_router_hazard_avoidance():
    # Place a severe flood polygon covering the direct connection between Darbhanga_Center and Kalyanpur_Village
    # Kalyanpur is at lat ~26.22, lon ~85.94; Darbhanga is at 26.15, 85.89
    hazard_poly = [{
        "bbox": [85.88, 26.14, 85.95, 26.23],
        "severity": 0.95
    }]
    
    route = road_router.compute_safe_route(
        district_id="darbhanga",
        origin_node="Darbhanga_Center",
        dest_node="Keoti_Junction",
        hazard_polygons=hazard_poly
    )
    assert route["route_geojson"]["geometry"]["type"] == "LineString"
    assert len(route["blocked_segments"]) > 0
    assert route["is_rerouted"] is True

