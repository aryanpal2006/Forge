from fastapi import APIRouter, Query
from typing import Optional
from backend.app.logistics.mock_services import mock_services
from backend.app.logistics.router import road_router

router = APIRouter(prefix="/mock", tags=["Mock Microservices"])

@router.get("/suppliers")
def mock_suppliers(district: Optional[str] = Query(None), category: Optional[str] = Query(None)):
    return mock_services.list_suppliers(district_id=district, category=category)

@router.get("/fleet")
def mock_fleet(district: Optional[str] = Query(None), status: Optional[str] = Query(None)):
    return mock_services.list_fleet(district_id=district, status=status)

@router.get("/roads")
def mock_roads(district: str = Query("solapur")):
    dist_norm = district.lower()
    if dist_norm in road_router.graphs:
        g = road_router.graphs[dist_norm]
        nodes = road_router.node_coords[dist_norm]
        edges = []
        for u, v, data in g.edges(data=True):
            edges.append({
                "from_node": u,
                "to_node": v,
                "base_distance_km": data.get("base_distance_km"),
                "hazard_penalty": data.get("hazard_penalty", 1.0)
            })
        return {
            "district": dist_norm,
            "nodes": nodes,
            "edges": edges
        }
    return {"error": "District not found in road network"}

