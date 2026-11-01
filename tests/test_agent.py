import pytest
from backend.app.logistics.agent import relief_agent

def test_agent_orchestration_loop():
    res = relief_agent.orchestrate_emergency_response(
        district_id="darbhanga",
        event_trigger="TEST_FLASH_FLOOD_SIMULATION",
        injected_severity=0.90
    )
    assert res["status"] == "SUCCESS"
    assert "dispatch_order" in res
    assert res["dispatch_order"]["order_id"].startswith("ORD-")
    assert len(res["tool_calls"]) >= 5
    assert any(t["tool"] == "compute_safe_route" for t in res["tool_calls"])
    assert any(t["tool"] == "create_dispatch_order" for t in res["tool_calls"])

def test_agent_mid_transit_rerouting():
    # 1. Trigger initial emergency order
    initial_res = relief_agent.orchestrate_emergency_response(
        district_id="darbhanga",
        event_trigger="INITIAL_FLOOD_DISPATCH"
    )
    order_id = initial_res["dispatch_order"]["order_id"]
    
    # 2. Inject mid-transit hazard emergence
    hazard_bbox = [85.90, 26.13, 85.93, 26.16]
    reroute_res = relief_agent.trigger_mid_transit_rerouting(order_id, hazard_bbox)
    
    assert reroute_res["status"] == "REROUTED"
    assert reroute_res["rerouted_count"] >= 1
    assert "new_route_geojson" in reroute_res

